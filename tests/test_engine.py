import pytest

from loan_engine.engine import CONFIDENCE_MARGIN, assess, emi_room, evaluate_lender
from loan_engine.finance import pmt
from loan_engine.rules import Lender, Rule


def failed(res):
    return {f.rule for f in res.failures}


def test_baseline_profile_gets_many_offers(lenders, make_profile):
    out = assess(make_profile("P01"), lenders)
    assert out["eligible"] and len(out["approving_lenders"]) >= 15
    best = out["best"]
    assert best.offer_amount == 1_000_000
    # best option is the cheapest full-amount offer once low-confidence quotes carry their margin
    full = [r for r in out["approving_lenders"] if r.offer_amount >= 1_000_000]
    assert best.apr + CONFIDENCE_MARGIN[best.confidence] == min(r.apr + CONFIDENCE_MARGIN[r.confidence] for r in full)
    cheapest = min(full, key=lambda r: r.apr)
    if cheapest is not best:
        assert cheapest.lender_name in out["best_reason"] and "estimates" in out["best_reason"]


def test_offer_respects_foir(lenders, make_profile):
    p = make_profile("P03")
    for r in assess(p, lenders)["approving_lenders"]:
        _, _, room = emi_room(lenders[r.lender_id], p.monthly_income, p.existing_emi)
        assert pmt(r.offer_amount, r.rate_pct, r.offer_tenure) <= room + 1


def test_tenure_capped_by_age_at_maturity(lenders, make_profile):
    p = make_profile("P06")  # 56-year-old
    r = evaluate_lender(lenders["hdfc"], p)  # max age 60 at maturity
    assert r.tenure_range[1] == 48


def test_boundaries_are_inclusive(lenders, make_profile):
    # IndusInd: income >= 25,000; HDFC: age >= 21
    p = make_profile("P01", net_monthly_income=25_000, existing_emi=0)
    assert "min_income" not in failed(evaluate_lender(lenders["indusind"], p))
    p = make_profile("P01", net_monthly_income=24_999, existing_emi=0)
    assert "min_income" in failed(evaluate_lender(lenders["indusind"], p))
    assert "min_age" not in failed(evaluate_lender(lenders["hdfc"], make_profile("P01", age=21)))
    assert "min_age" in failed(evaluate_lender(lenders["hdfc"], make_profile("P01", age=20)))


def test_new_to_credit_only_thin_file_lenders(lenders, make_profile):
    out = assess(make_profile("P07"), lenders)
    assert {r.lender_id for r in out["approving_lenders"]} <= {
        l for l, v in lenders.items() if v.get("ntc_allowed")}


def test_writeoff_rejected_everywhere_with_counterfactual(lenders, make_profile):
    out = assess(make_profile("P09"), lenders)
    assert not out["eligible"]
    assert "Written-off" in out["what_would_change"]


@pytest.mark.parametrize("pid, blocker", [
    ("P14", "Too young"),
    ("P15", "Credit score below cut-off"),
    ("P16", "Existing EMIs leave no room (FOIR)"),
    ("P17", "Business vintage too short"),
])
def test_negative_profiles_rejected_everywhere(lenders, make_profile, pid, blocker):
    out = assess(make_profile(pid), lenders)
    assert not out["eligible"]
    assert next(iter(out["blocker_counts"])) == blocker
    assert out["what_would_change"]


def test_salary_account_rule(lenders, make_profile):
    p = make_profile("P06", salary_account_with=None)
    assert "salary_account_required" in failed(evaluate_lender(lenders["sbi"], p))
    p = make_profile("P06")  # holds SBI salary account
    assert evaluate_lender(lenders["sbi"], p).eligible


def test_self_employed_routed_to_se_rules(lenders, make_profile):
    p = make_profile("P05")
    assert "self_employed_allowed" in failed(evaluate_lender(lenders["axis"], p))
    assert evaluate_lender(lenders["icici"], p).eligible


def test_product_cap_binds_for_large_request(lenders, make_profile):
    r = evaluate_lender(lenders["indusind"], make_profile("P10"))
    assert r.max_loan == 500_000 and r.binding_constraint == "product_cap"


def test_more_emi_never_increases_max_loan(lenders, make_profile):
    for lid, lender in lenders.items():
        a = evaluate_lender(lender, make_profile("P01", existing_emi=0)).max_loan
        b = evaluate_lender(lender, make_profile("P01", existing_emi=40_000)).max_loan
        assert b <= a, lid


def test_request_below_lender_minimum_is_rejected(lenders, make_profile):
    out = assess(make_profile("P01", requested_amount=20_000, requested_tenure_months=12), lenders)
    for r in out["approving_lenders"]:
        assert r.offer_amount >= lenders[r.lender_id].get("min_loan_amount"), r.lender_id
    hdfc = evaluate_lender(lenders["hdfc"], make_profile("P01", requested_amount=20_000))  # min Rs 50,000
    assert "min_loan_amount" in failed(hdfc)
    assert "min_loan_amount" not in failed(evaluate_lender(lenders["hdfc"], make_profile("P01", requested_amount=50_000)))


def test_lowest_applicable_cap_wins(lenders, make_profile):
    # BoB outside metros: Rs 15 lakh non-metro cap, but Rs 2 lakh without a BoB relationship -> 2 lakh binds
    r = evaluate_lender(lenders["bob"], make_profile("P10", city="Jaipur", salary_account_with=None))
    assert r.max_loan == 200_000 and r.binding_constraint == "product_cap"


def test_segment_rules_override_base_rules(lenders, make_profile):
    # Bank of Baroda prices and sizes govt employees by where their salary is credited
    base = dict(employer_category="pvt_ltd", salary_account_with=None, existing_emi=0, net_monthly_income=40_000)
    private = evaluate_lender(lenders["bob"], make_profile("P01", **base))
    govt = evaluate_lender(lenders["bob"], make_profile("P01", **dict(base, employer_category="govt")))
    govt_rel = evaluate_lender(lenders["bob"], make_profile("P01", **dict(base, employer_category="govt",
                                                                         salary_account_with="bob")))
    assert private.max_loan == 200_000 and private.rate_band == (13.90, 17.50)
    assert govt.tenure_range[1] == 72 and govt.rate_band == (11.15, 15.50)
    assert govt_rel.tenure_range[1] == 84 and govt_rel.rate_band == (10.65, 15.50) and govt_rel.fee == 0
    assert govt_rel.segments == ("govt", "govt_rel", "rel")
    assert govt_rel.max_loan > govt.max_loan > private.max_loan


def test_serviceable_cities(lenders, make_profile):
    axis = lenders["axis"]
    assert "serviceable_cities" in failed(evaluate_lender(axis, make_profile("P01", city="Sitapur")))
    for city in ["Bengaluru", "Gurugram", "New Delhi", "Ludhiana"]:  # spelling variants of listed cities
        assert "serviceable_cities" not in failed(evaluate_lender(axis, make_profile("P01", city=city))), city


def test_rate_by_cibil_band(lenders, make_profile):
    pnb = lenders["pnb"]
    rate = lambda **kw: evaluate_lender(pnb, make_profile("P01", **kw)).rate_pct
    assert rate(credit_score=805) == 11.60
    assert rate(credit_score=760) == 12.60
    assert rate(credit_score=None) == 13.60  # no-hit is priced in the lowest band
    # PNB salary-account holders get the public scheme, which switches the bands off
    assert evaluate_lender(pnb, make_profile("P01", salary_account_with="pnb")).rate_band == (10.60, 14.35)


def test_best_rate_needs_large_loan(lenders, make_profile):
    hdfc = lenders["hdfc"]  # 9.99% only on Rs 15 lakh+; below that the floor is the disclosed average 10.89%
    small = evaluate_lender(hdfc, make_profile("P01", credit_score=820, requested_amount=500_000))
    large = evaluate_lender(hdfc, make_profile("P01", credit_score=820, requested_amount=1_500_000))
    assert small.rate_pct >= 10.89 > large.rate_pct


@pytest.mark.parametrize("override", [
    {"age": 17}, {"requested_amount": -5}, {"requested_amount": 0}, {"requested_tenure_months": 0},
    {"credit_score": 950}, {"existing_emi": -1}, {"employment_type": "student"}, {"employer_category": "startup"},
])
def test_invalid_profiles_raise(make_profile, override):
    with pytest.raises(ValueError):
        make_profile("P01", **override)


def test_lender_own_foir_breakpoints_and_tenure_multiple(lenders):
    """Tata's calculator: FOIR 60% at Rs 50k, 65% at 50,001; multiple 20x / 23x at 60 months by income band."""
    from loan_engine.engine import foir_for, multiple_cap
    tata = lenders["tata"]
    assert foir_for(tata, 50_000)[1] == 0.6 and foir_for(tata, 50_001)[1] == 0.65 and foir_for(tata, 80_000)[1] == 0.75
    assert multiple_cap(tata, 40_000, 0, 60)[1] == 20 * 40_000
    assert multiple_cap(tata, 60_000, 0, 60)[1] == 23 * 60_000
    assert multiple_cap(tata, 60_000, 0, 12)[1] == 7 * 60_000
    abcl = lenders["abcl"]  # 17x of (income - EMIs) at 5 years
    assert multiple_cap(abcl, 50_000, 10_000, 60)[1] == 17 * 40_000


def test_new_emi_cap(lenders):
    """Fibe: the new EMI is capped at 30% of income even when total FOIR (70%) leaves more room."""
    _, _, room = emi_room(lenders["fibe"], 50_000, 0)
    assert room == 15_000
