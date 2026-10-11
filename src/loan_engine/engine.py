"""Three-stage eligibility engine.

Stage A  knock-out rules     -> every failed rule, with actual vs required value
Stage B  loan sizing         -> FOIR, salary multiple, product cap, age-capped tenure
Stage C  pricing and ranking -> expected rate, APR incl. fee, best option and why
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .finance import apr_pct, pmt, pv
from .rules import Lender

METRO_CITIES = {"mumbai", "delhi", "new delhi", "gurugram", "noida", "bengaluru", "bangalore",
                "chennai", "kolkata", "hyderabad", "pune", "ahmedabad"}
# Spelling variants, so a lender's published city list matches the applicant's city
CITY_ALIASES = {"bengaluru": "bangalore", "gurugram": "gurgaon", "new delhi": "delhi", "mysuru": "mysore",
                "thiruvananthapuram": "trivandrum", "visakhapatnam": "vishakhapatnam", "vizag": "vishakhapatnam",
                "vijayawada": "vijaywada", "bhubaneswar": "bhubaneshwar", "prayagraj": "allahabad",
                "kozhikode": "calicut", "puducherry": "pondicherry", "tiruchirappalli": "trichy",
                "belagavi": "belgaum", "hubballi": "hubli", "bathinda": "bhatinda", "panaji": "goa"}
SMALL_EMPLOYERS = {"llp", "proprietorship"}
GOVT_EMPLOYERS = {"govt", "psu"}
EMPLOYMENT_TYPES = {"salaried", "self_employed"}
EMPLOYER_CATEGORIES = {"govt", "psu", "mnc", "listed", "pvt_ltd", "llp", "proprietorship", "none"}
# Unpublished at every lender; one documented assumption applied to all, so excluded from
# the per-lender data-confidence score (see README "Assumptions").
UNIVERSAL_ASSUMPTIONS = {"max_dpd_12m", "max_enquiries_6m", "writeoff_allowed"}
# Risk position of a typical approved borrower: a lender's disclosed average rate is pinned here
TYPICAL_POSITION = 0.25
# APR points added when ranking, so a lender whose rules are mostly estimated must be clearly cheaper to be "best"
CONFIDENCE_MARGIN = {"high": 0.0, "medium": 1.0, "low": 2.0}
GST = 0.18

RULE_LABELS = {
    "min_age": "Too young",
    "age_at_maturity": "Too old for even the shortest tenure",
    "self_employed_allowed": "Self-employed not accepted",
    "se_min_vintage_months": "Business vintage too short",
    "se_min_annual_income": "Annual income (ITR) too low",
    "allowed_employer_categories": "Employer category not accepted",
    "salary_account_required": "Needs a salary account with this lender",
    "min_income": "Monthly income below lender floor",
    "min_total_exp_months": "Total work experience too short",
    "min_current_job_months": "Too new in current job",
    "ntc_allowed": "No credit history (new to credit)",
    "min_credit_score": "Credit score below cut-off",
    "max_dpd_12m": "Recent missed payments (DPD)",
    "max_enquiries_6m": "Too many recent credit enquiries",
    "writeoff_allowed": "Written-off / settled account",
    "foir": "Existing EMIs leave no room (FOIR)",
    "min_loan_amount": "Requested amount below lender's minimum loan",
    "serviceable_cities": "City not served by this lender",
}


def city_key(city: str) -> str:
    c = city.strip().lower()
    return CITY_ALIASES.get(c, c)


@dataclass
class Profile:
    profile_id: str
    description: str
    age: int
    employment_type: str
    employer_category: str
    city: str
    credit_score: int | None
    existing_emi: float
    requested_amount: float
    requested_tenure_months: int
    net_monthly_income: float = 0
    annual_income_itr: float = 0
    business_vintage_months: int = 0
    total_work_exp_months: int = 0
    current_job_months: int = 0
    max_dpd_12m: int = 0
    enquiries_6m: int = 0
    has_writeoff_or_settlement: bool = False
    salary_account_with: str | None = None

    def __post_init__(self):
        """Reject impossible inputs instead of returning a confident answer for them."""
        errors = []
        if not 18 <= self.age <= 100:
            errors.append(f"age {self.age} must be 18-100")
        if self.employment_type not in EMPLOYMENT_TYPES:
            errors.append(f"employment_type {self.employment_type!r} must be one of {sorted(EMPLOYMENT_TYPES)}")
        if self.employer_category not in EMPLOYER_CATEGORIES:
            errors.append(f"employer_category {self.employer_category!r} must be one of {sorted(EMPLOYER_CATEGORIES)}")
        if self.credit_score is not None and not 300 <= self.credit_score <= 900:
            errors.append(f"credit_score {self.credit_score} must be 300-900 or null")
        if self.requested_amount <= 0:
            errors.append("requested_amount must be > 0")
        if self.requested_tenure_months <= 0:
            errors.append("requested_tenure_months must be > 0")
        for name in ("existing_emi", "net_monthly_income", "annual_income_itr", "business_vintage_months",
                     "total_work_exp_months", "current_job_months", "max_dpd_12m", "enquiries_6m"):
            if getattr(self, name) < 0:
                errors.append(f"{name} must be >= 0")
        if errors:
            raise ValueError(f"Invalid profile {self.profile_id}: " + "; ".join(errors))

    @property
    def salaried(self) -> bool:
        return self.employment_type == "salaried"

    @property
    def city_tier(self) -> str:
        return "metro" if self.city.strip().lower() in METRO_CITIES else "non_metro"

    @property
    def monthly_income(self) -> float:
        return self.net_monthly_income if self.salaried else self.annual_income_itr / 12


@dataclass
class Failure:
    rule: str
    actual: object
    required: str

    @property
    def label(self) -> str:
        return RULE_LABELS.get(self.rule, self.rule)


@dataclass
class LenderResult:
    lender_id: str
    lender_name: str
    lender_type: str
    failures: list[Failure] = field(default_factory=list)
    rules_used: set[str] = field(default_factory=set)
    max_loan: int = 0
    binding_constraint: str = ""
    tenure_range: tuple[int, int] = (0, 0)
    rate_pct: float = 0.0
    rate_band: tuple[float, float] = (0.0, 0.0)
    offer_amount: int = 0
    offer_tenure: int = 0
    emi: int = 0
    fee: int = 0
    apr: float = 0.0
    total_cost: int = 0
    headroom: float = 0.0
    estimate_share: float = 0.0
    segments: tuple[str, ...] = ()
    applied: dict = field(default_factory=dict)  # rule -> Rule actually used (after segment overrides)

    @property
    def eligible(self) -> bool:
        return not self.failures

    @property
    def confidence(self) -> str:
        return "high" if self.estimate_share < 0.35 else "medium" if self.estimate_share < 0.55 else "low"


def risk_position(p: Profile) -> float:
    """0 = best risk tier (rate_min), 1 = worst accepted tier (rate_max)."""
    s = p.credit_score
    if s is None:
        pos = 0.80
    else:
        pos = next(v for cut, v in [(800, 0.0), (775, 0.08), (750, 0.15), (725, 0.30),
                                    (700, 0.45), (650, 0.65), (0, 0.85)] if s >= cut)
    pos += {"govt": -0.08, "psu": -0.08, "mnc": -0.04, "listed": -0.04,
            "llp": 0.05, "proprietorship": 0.05}.get(p.employer_category, 0.0)
    if not p.salaried:
        pos += 0.05
    if p.monthly_income >= 100_000:
        pos -= 0.05
    elif p.monthly_income < 25_000:
        pos += 0.05
    if p.monthly_income and p.existing_emi / p.monthly_income > 0.30:
        pos += 0.05
    return min(max(pos, 0.0), 1.0)


def expected_rate(lender: Lender, p: Profile, use) -> float:
    """Rate within the lender's published band for this applicant.

    rate_by_score (published CIBIL bands) wins when present. Otherwise the band is interpolated by risk
    position; if the lender discloses its average rate, a typical borrower is pinned to that average.
    rate_best_min_amount: the lowest rates are only offered on loans of at least that size.
    """
    lo, hi = lender.get("rate_min_pct"), lender.get("rate_max_pct")
    use("rate_min_pct"), use("rate_max_pct")
    if lender.has("rate_by_score"):
        use("rate_by_score")
        bands = sorted(((int(c), float(r)) for c, r in (b.split(":") for b in lender.get("rate_by_score").split("|"))),
                       reverse=True)
        score = p.credit_score if p.credit_score is not None else bands[-1][0]  # thin file: lowest band
        rate = next((r for cut, r in bands if score >= cut), bands[-1][1])
    else:
        pos = risk_position(p)
        if lender.has("rate_avg_pct"):
            use("rate_avg_pct")
            avg = lender.get("rate_avg_pct")
            rate = (lo + pos / TYPICAL_POSITION * (avg - lo) if pos <= TYPICAL_POSITION
                    else avg + (pos - TYPICAL_POSITION) / (1 - TYPICAL_POSITION) * (hi - avg))
        else:
            rate = lo + pos * (hi - lo)
    if lender.has("rate_best_min_amount") and p.requested_amount < lender.get("rate_best_min_amount"):
        use("rate_best_min_amount")
        floor = lender.get("rate_avg_pct") if lender.has("rate_avg_pct") else lo + 0.1 * (hi - lo)
        rate = max(rate, floor)
    return round(rate, 2)


def band_value(spec: str, x: float) -> float:
    """Look up "upper:value|upper:value|*:value" (upper bounds inclusive, ascending) for x."""
    parts = [b.split(":") for b in spec.split("|")]
    return float(next((v for k, v in parts if k == "*" or x <= float(k)), parts[-1][1]))


def foir_for(lender: Lender, income: float) -> tuple[str, float]:
    """FOIR for this income: the lender's own breakpoints (foir_bands) if known, else the three standard bands."""
    if lender.has("foir_bands"):  # e.g. Tata's calculator: 50% to Rs 25k, 60% to 50k, 65% to 75k, 75% above
        return "foir_bands", band_value(lender.get("foir_bands"), income)
    # bands measured on Poonawalla's calculator: Rs 50,000 itself is in the low band
    key = "foir_lt_50k" if income <= 50_000 else "foir_50k_1l" if income < 100_000 else "foir_ge_1l"
    return key, lender.get(key)


def emi_room(lender: Lender, income: float, existing_emi: float) -> tuple[list[str], float, float]:
    """(rules used, FOIR, monthly EMI the new loan may take). max_new_emi_pct caps the new EMI on its own."""
    key, foir = foir_for(lender, income)
    room, keys = foir * income - existing_emi, [key]
    if lender.has("max_new_emi_pct"):  # e.g. Fibe: new EMI <= 30% of income, total EMIs <= 70%
        room, keys = min(room, lender.get("max_new_emi_pct") * income), keys + ["max_new_emi_pct"]
    return keys, foir, room


def multiple_cap(lender: Lender, income: float, existing_emi: float, tenure: int) -> tuple[list[str], float]:
    """(rules used, salary-multiple cap at this tenure); no multiple published -> no cap."""
    if lender.has("income_multiple_by_tenure"):  # e.g. ABCL's calculator: 4x for 1 year ... 23x for 7 years
        keys = ["income_multiple_by_tenure"]
        parts = [t.split(":") for t in lender.get("income_multiple_by_tenure").split("|")]
        row = next((v for k, v in parts if k == "*" or tenure <= float(k)), parts[-1][1]).split("/")
        band = 0
        if len(row) > 1:  # one multiple per income band, e.g. Tata: 20/23/27 for <50k / 50-75k / >75k
            keys.append("income_multiple_income_bands")
            breaks = [float(x) for x in lender.get("income_multiple_income_bands").split("|")]
            band = next((i for i, cut in enumerate(breaks) if income <= cut), len(breaks))
        m = float(row[band])
    elif lender.has("max_income_multiple"):
        keys, m = ["max_income_multiple"], lender.get("max_income_multiple")
    else:
        return [], float("inf")
    base = income
    if lender.get("income_multiple_net_of_emi"):  # e.g. Kotak, IDFC: multiple of (income - existing EMIs)
        keys.append("income_multiple_net_of_emi")
        base = max(income - existing_emi, 0)
    return keys, m * base


def evaluate_lender(lender: Lender, p: Profile) -> LenderResult:
    is_govt = p.salaried and p.employer_category in GOVT_EMPLOYERS
    has_relationship = p.salary_account_with == lender.lender_id
    segments = {s for s, on in [("govt", is_govt), ("rel", has_relationship),
                                ("govt_rel", is_govt and has_relationship)] if on}
    lender = lender.for_segments(segments)  # segment-specific rules override the base rules
    res = LenderResult(lender.lender_id, lender.name, lender.lender_type, segments=tuple(sorted(segments)))
    use = res.rules_used.add
    fail = res.failures.append

    # ---- Stage A: knock-out rules ----
    min_age_key = "min_age" if p.salaried or not lender.has("se_min_age") else "se_min_age"
    use(min_age_key)
    if p.age < lender.get(min_age_key):
        fail(Failure("min_age", p.age, f">= {lender.get(min_age_key)}"))

    age_key = "max_age_at_maturity" if p.salaried else "max_age_at_maturity_se"
    use(age_key)
    months_to_age_limit = (lender.get(age_key) - p.age) * 12
    use("min_tenure_months")
    if months_to_age_limit < lender.get("min_tenure_months"):
        fail(Failure("age_at_maturity", p.age,
                     f"age + tenure <= {lender.get(age_key)} (min tenure {lender.get('min_tenure_months')}m)"))

    if lender.has("serviceable_cities"):
        use("serviceable_cities")
        cities = {city_key(c) for c in lender.get("serviceable_cities").split("|")}
        if city_key(p.city) not in cities:
            fail(Failure("serviceable_cities", p.city, f"one of {len(cities)} listed cities"))

    if p.salaried:
        allowed = lender.get("allowed_employer_categories")
        use("allowed_employer_categories")
        if allowed != "any" and p.employer_category not in allowed.split("|"):
            fail(Failure("allowed_employer_categories", p.employer_category, allowed.replace("|", ", ")))
        use("salary_account_required")
        if lender.get("salary_account_required") and not has_relationship:
            fail(Failure("salary_account_required", p.salary_account_with or "none", lender.lender_id))

        floor_key = "min_income_metro" if p.city_tier == "metro" else "min_income_non_metro"
        floor = lender.get(floor_key)
        use(floor_key)
        if p.employer_category in SMALL_EMPLOYERS and lender.has("min_income_small_employer"):
            floor = max(floor, lender.get("min_income_small_employer"))
            use("min_income_small_employer")
        if p.net_monthly_income < floor:
            fail(Failure("min_income", p.net_monthly_income, f">= {floor:,} ({p.city_tier})"))

        for key, actual in [("min_total_exp_months", p.total_work_exp_months),
                            ("min_current_job_months", p.current_job_months)]:
            use(key)
            if actual < lender.get(key):
                fail(Failure(key, actual, f">= {lender.get(key)} months"))
    else:
        use("self_employed_allowed")
        if not lender.get("self_employed_allowed"):
            fail(Failure("self_employed_allowed", "self_employed", "salaried only"))
        else:
            for key, actual in [("se_min_vintage_months", p.business_vintage_months),
                                ("se_min_annual_income", p.annual_income_itr)]:
                use(key)
                if actual < lender.get(key):
                    fail(Failure(key, actual, f">= {lender.get(key):,}"))

    if p.credit_score is None:
        use("ntc_allowed")
        if not lender.get("ntc_allowed"):
            fail(Failure("ntc_allowed", "no score", "bureau history required"))
    else:
        score_key = "se_min_credit_score" if not p.salaried and lender.has("se_min_credit_score") \
            else "min_credit_score"
        use(score_key)
        if p.credit_score < lender.get(score_key):
            fail(Failure("min_credit_score", p.credit_score, f">= {lender.get(score_key)}"))

    for key, actual in [("max_dpd_12m", p.max_dpd_12m), ("max_enquiries_6m", p.enquiries_6m)]:
        use(key)
        if actual > lender.get(key):
            fail(Failure(key, actual, f"<= {lender.get(key)}"))
    use("writeoff_allowed")
    if p.has_writeoff_or_settlement and not lender.get("writeoff_allowed"):
        fail(Failure("writeoff_allowed", "yes", "none"))

    # ---- Stage B: loan sizing ----
    income = p.monthly_income
    room_keys, foir, room = emi_room(lender, income, p.existing_emi)
    for k in room_keys:
        use(k)
    use("max_tenure_months")
    min_t = lender.get("min_tenure_months")
    max_t = min(lender.get("max_tenure_months"), max(months_to_age_limit, 0))
    res.tenure_range = (min_t, max_t)

    res.rate_band = (lender.get("rate_min_pct"), lender.get("rate_max_pct"))
    res.rate_pct = expected_rate(lender, p, use)

    # every cap that applies to this applicant; the lowest one wins
    cap_keys = ["max_loan_amount"]
    if p.city_tier == "non_metro" and lender.has("max_loan_amount_non_metro"):
        cap_keys.append("max_loan_amount_non_metro")
    cap_key = min(cap_keys, key=lender.get)
    min_key = "min_loan_amount_non_metro" if (p.city_tier == "non_metro"
                                              and lender.has("min_loan_amount_non_metro")) else "min_loan_amount"
    use(cap_key), use(min_key)
    for k in multiple_cap(lender, income, p.existing_emi, max_t)[0]:
        use(k)

    def max_loan_at(tenure: int) -> tuple[float, str]:
        if room <= 0 or tenure <= 0:
            return 0.0, "foir"
        cap = multiple_cap(lender, income, p.existing_emi, tenure)[1]
        limits = {"foir": pv(room, res.rate_pct, tenure),
                  "income_multiple": cap,  # lenders without a salary multiple size by FOIR and caps only
                  "product_cap": lender.get(cap_key)}
        name = min(limits, key=limits.get)
        return limits[name], name

    amount, res.binding_constraint = max_loan_at(max_t)
    res.max_loan = int(amount // 1000 * 1000)
    min_loan = lender.get(min_key)
    if p.requested_amount < min_loan:
        fail(Failure("min_loan_amount", p.requested_amount, f">= {min_loan:,}"))
    if max_t >= min_t and res.max_loan < min_loan:
        used_pct = p.existing_emi / income * 100 if income else 0
        fail(Failure("foir", f"existing EMI {used_pct:.0f}% of income",
                     f"FOIR {foir:.0%} must leave room for >= Rs {min_loan:,} loan"))
    res.headroom = (res.max_loan - p.requested_amount) / p.requested_amount

    # ---- Stage C: offer for the requested amount ----
    if res.eligible:
        tenure = min(max(p.requested_tenure_months, min_t), max_t)
        offer = min(p.requested_amount, max_loan_at(tenure)[0])
        while offer < p.requested_amount and tenure < max_t:  # stretch tenure before cutting amount
            tenure = min(tenure + 6, max_t)
            offer = min(p.requested_amount, max_loan_at(tenure)[0])
        offer = int(offer // 1000 * 1000)
        fee = offer * lender.get("processing_fee_pct")
        use("processing_fee_pct")
        if lender.has("processing_fee_cap"):
            fee = min(fee, lender.get("processing_fee_cap"))
            use("processing_fee_cap")
        fee *= 1 + GST
        emi = pmt(offer, res.rate_pct, tenure)
        res.offer_amount, res.offer_tenure = offer, tenure
        res.emi, res.fee = round(emi), round(fee)
        res.apr = apr_pct(offer, res.rate_pct, tenure, fee)
        res.total_cost = round(emi * tenure - offer + fee)

    res.applied = {k: lender.rules[k] for k in res.rules_used if k in lender.rules}
    used = [r for k, r in res.applied.items() if k not in UNIVERSAL_ASSUMPTIONS]
    # estimates count fully, aggregator-only values half
    res.estimate_share = sum(1.0 if r.is_estimate else 0.5 if r.tier == "aggregator" else 0.0
                             for r in used) / len(used)
    return res


def _rank_key(r: LenderResult, requested: float):
    return (r.offer_amount < requested, -r.offer_amount if r.offer_amount < requested else 0,
            r.apr + CONFIDENCE_MARGIN[r.confidence], r.apr, -r.headroom)


def explain_best(best: LenderResult, ranked: list[LenderResult], requested: float) -> str:
    if best.offer_amount >= requested:
        full = [r for r in ranked if r.offer_amount >= requested]
        cheapest = min(full, key=lambda r: r.apr)
        if cheapest is best:
            why = f"Lowest APR ({best.apr}%) among the {len(full)} lender(s) that can lend the full Rs {requested:,.0f}"
        else:
            why = (f"Lowest well-sourced APR ({best.apr}%) among the {len(full)} lender(s) that can lend the full "
                   f"Rs {requested:,.0f}. {cheapest.lender_name} shows less ({cheapest.apr}%), but its rules are mostly aggregator values or "
                   f"estimates ({cheapest.confidence} confidence), so ranking adds "
                   f"{CONFIDENCE_MARGIN[cheapest.confidence]:g} points to its APR. {best.lender_name}")
    else:
        why = (f"No lender can lend the full Rs {requested:,.0f}; {best.lender_name} offers the most "
               f"(Rs {best.offer_amount:,})")
    why += f": EMI Rs {best.emi:,} for {best.offer_tenure} months, total cost Rs {best.total_cost:,}"
    runner = next((r for r in ranked[1:] if r.offer_amount >= best.offer_amount), None)
    if runner:
        why += f". Next best is {runner.lender_name} at {runner.apr}% APR"
        if runner.offer_tenure == best.offer_tenure:
            extra = runner.total_cost - best.total_cost
            why += (f" (Rs {extra:,} more over the loan)" if extra > 0 else
                    " (same total cost; ranked lower on headroom)" if extra == 0 else
                    f" (Rs {-extra:,} less over the loan, but {runner.confidence} data confidence)")
        else:
            why += f" (EMI Rs {runner.emi:,} over {runner.offer_tenure} months)"
    if best.confidence != "high":
        why += f". Note: {best.confidence} data confidence for this lender (several rules are estimates)"
    return why + "."


def assess(profile: Profile, lenders: dict[str, Lender]) -> dict:
    results = [evaluate_lender(l, profile) for l in lenders.values()]
    eligible = sorted([r for r in results if r.eligible], key=lambda r: _rank_key(r, profile.requested_amount))
    rejected = [r for r in results if not r.eligible]

    blockers: dict[str, int] = {}
    for r in rejected:
        for f in r.failures:
            blockers[f.label] = blockers.get(f.label, 0) + 1
    out = {
        "profile": profile,
        "eligible": bool(eligible),
        "approving_lenders": eligible,
        "rejected_lenders": rejected,
        "blocker_counts": dict(sorted(blockers.items(), key=lambda kv: -kv[1])),
    }
    if eligible:
        out["best"] = eligible[0]
        out["best_reason"] = explain_best(eligible[0], eligible, profile.requested_amount)
    else:
        nearest = min(rejected, key=lambda r: (len(r.failures), r.lender_type != "fintech"))
        out["reason"] = "; ".join(f"{k} ({v}/{len(rejected)} lenders)"
                                  for k, v in list(out["blocker_counts"].items())[:3])
        out["nearest"] = nearest
        out["what_would_change"] = "; ".join(f"{f.label}: has {f.actual}, needs {f.required}"
                                             for f in nearest.failures)
    return out
