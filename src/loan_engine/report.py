"""Render engine results as Markdown and JSON-friendly dicts."""
from __future__ import annotations

from .engine import LenderResult


def inr(x: float) -> str:
    return f"Rs {x:,.0f}"


def lender_to_dict(r: LenderResult) -> dict:
    d = {
        "lender_id": r.lender_id, "lender": r.lender_name, "type": r.lender_type,
        "eligible": r.eligible, "data_confidence": r.confidence,
        "max_loan": r.max_loan, "binding_constraint": r.binding_constraint,
        "tenure_range_months": list(r.tenure_range), "expected_rate_pct": r.rate_pct,
        "rate_band_pct": list(r.rate_band),
    }
    if r.eligible:
        d.update(offer_amount=r.offer_amount, offer_tenure_months=r.offer_tenure, emi=r.emi,
                 processing_fee_incl_gst=r.fee, apr_pct=r.apr, total_cost=r.total_cost)
    else:
        d["failed_rules"] = [{"rule": f.rule, "reason": f.label, "actual": f.actual, "required": f.required}
                             for f in r.failures]
    return d


def result_to_dict(res: dict) -> dict:
    p = res["profile"]
    out = {"profile_id": p.profile_id, "description": p.description, "eligible": res["eligible"]}
    if res["eligible"]:
        out["best_option"] = res["best"].lender_id
        out["best_reason"] = res["best_reason"]
    else:
        out["reason"] = res["reason"]
        out["nearest_lender"] = res["nearest"].lender_id
        out["what_would_change"] = res["what_would_change"]
    out["approving_lenders"] = [lender_to_dict(r) for r in res["approving_lenders"]]
    out["rejected_lenders"] = [lender_to_dict(r) for r in res["rejected_lenders"]]
    return out


def profile_markdown(res: dict) -> str:
    p = res["profile"]
    income = (f"{inr(p.net_monthly_income)}/month net" if p.salaried
              else f"{inr(p.annual_income_itr)}/year ITR, {p.business_vintage_months}m vintage")
    score = p.credit_score if p.credit_score is not None else "none (new to credit)"
    lines = [
        f"### {p.profile_id} - {p.description}",
        "",
        f"*Age {p.age}, {p.employment_type.replace('_', '-')} ({p.employer_category}), {p.city} ({p.city_tier}); "
        f"{income}; score {score}; existing EMI {inr(p.existing_emi)}; DPD {p.max_dpd_12m}, "
        f"enquiries {p.enquiries_6m}{', write-off on record' if p.has_writeoff_or_settlement else ''}. "
        f"Wants {inr(p.requested_amount)} for {p.requested_tenure_months} months.*",
        "",
    ]
    if res["eligible"]:
        best = res["best"]
        lines += [f"**Decision: ELIGIBLE with {len(res['approving_lenders'])} of 20 lenders.** "
                  f"Best option: **{best.lender_name}**. {res['best_reason']}", "",
                  "| # | Lender | Max loan | Offer | Tenure (offer / range) | Expected rate | APR | EMI | Total cost | Confidence |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(res["approving_lenders"], 1):
            lines.append(f"| {i} | {r.lender_name} | {inr(r.max_loan)} | {inr(r.offer_amount)} | "
                         f"{r.offer_tenure}m / {r.tenure_range[0]}-{r.tenure_range[1]}m | {r.rate_pct}% | "
                         f"{r.apr}% | {inr(r.emi)} | {inr(r.total_cost)} | {r.confidence} |")
    else:
        n = res["nearest"]
        lines += [f"**Decision: NOT ELIGIBLE at any of the 20 lenders.** Main reasons: {res['reason']}.", "",
                  f"Closest lender: **{n.lender_name}**. What would change it: {res['what_would_change']}."]
    if res["rejected_lenders"]:
        lines += ["", "<details><summary>Rejections by lender</summary>", "",
                  "| Lender | Failed rules (actual -> required) |", "|---|---|"]
        for r in res["rejected_lenders"]:
            why = "; ".join(f"{f.label}: {f.actual} -> {f.required}" for f in r.failures)
            lines.append(f"| {r.lender_name} | {why} |")
        lines += ["", "</details>"]
    return "\n".join(lines) + "\n"
