"""Run the engine over a synthetic applicant population and write research/insights.md.

The population is SYNTHETIC (no approval data exists): its distributions are rough assumptions
about Indian personal-loan applicants, stated in POPULATION_ASSUMPTIONS below. Results show how the
rule set behaves (which rules bind, how lenders differ); they are not market approval rates.
"""
import random
from collections import Counter, defaultdict
from statistics import median

from _path import ROOT
from loan_engine.engine import Profile, assess
from loan_engine.rules import _read, load_lenders

N, SEED = 5000, 42
POPULATION_ASSUMPTIONS = """\
| Variable | Assumption |
|---|---|
| Employment | 80% salaried, 20% self-employed |
| Age | uniform 21-60 (self-employed 25-62) |
| City | 45% metro, 55% non-metro |
| Salaried income | log-normal, median Rs 35,000/month, sigma 0.6, floor Rs 8,000 |
| Self-employed ITR | log-normal, median Rs 6 lakh/year, sigma 0.7 |
| Employer | govt 12%, PSU 6%, MNC 12%, listed 15%, pvt ltd 40%, LLP 5%, proprietorship 10% |
| Credit score | 12% new-to-credit; others normal(725, 55), clipped 300-900 |
| DPD last 12m | 85% none, 10% 30 days, 5% 60+ days |
| Enquiries 6m | Poisson-like, mean 1.5 |
| Write-off/settlement | 3% (15% if score < 650) |
| Existing EMI | 45% none; others 5-55% of income |
| Request | 3-15x monthly income; tenure 12/24/36/48/60 months |
| Salary account | 30% hold one with a random bank in the list |
"""


def poisson(rng, lam):
    k, p, l = 0, 1.0, 2.718281828 ** -lam
    while True:
        p *= rng.random()
        if p <= l:
            return k
        k += 1


def synth(rng, i, bank_ids):
    salaried = rng.random() < 0.8
    age = rng.randint(21, 60) if salaried else rng.randint(25, 62)
    city = rng.choice(["Mumbai", "Delhi", "Bengaluru", "Pune"]) if rng.random() < 0.45 \
        else rng.choice(["Jaipur", "Indore", "Lucknow", "Nagpur", "Patna"])
    score = None if rng.random() < 0.12 else int(min(900, max(300, rng.gauss(725, 55))))
    if salaried:
        income = max(8000, int(rng.lognormvariate(10.463, 0.6)))  # ln(35000)=10.463
        emp = rng.choices(["govt", "psu", "mnc", "listed", "pvt_ltd", "llp", "proprietorship"],
                          [12, 6, 12, 15, 40, 5, 10])[0]
        total = max(0, (age - 21) * 12 + rng.randint(0, 12))
        extra = dict(net_monthly_income=income, total_work_exp_months=total,
                     current_job_months=rng.randint(min(1, total), max(1, total)))
        monthly = income
    else:
        itr = int(rng.lognormvariate(13.305, 0.7))  # ln(600000)=13.305
        emp = "none"
        extra = dict(annual_income_itr=itr, business_vintage_months=rng.randint(6, max(7, (age - 22) * 12)))
        monthly = itr / 12
    dpd = rng.choices([0, 30, 90], [85, 10, 5])[0]
    wo = rng.random() < (0.15 if score is not None and score < 650 else 0.03)
    emi = 0 if rng.random() < 0.45 else int(monthly * rng.uniform(0.05, 0.55))
    return Profile(profile_id=f"S{i:05d}", description="synthetic", age=age,
                   employment_type="salaried" if salaried else "self_employed", employer_category=emp,
                   city=city, credit_score=score, existing_emi=emi,
                   requested_amount=int(monthly * rng.uniform(3, 15) // 1000 * 1000) or 10000,
                   requested_tenure_months=rng.choice([12, 24, 36, 48, 60]), max_dpd_12m=dpd,
                   enquiries_6m=poisson(rng, 1.5), has_writeoff_or_settlement=wo,
                   salary_account_with=rng.choice(bank_ids) if salaried and rng.random() < 0.3 else None,
                   **extra)


def pct(x):
    return f"{x:.0%}"


def main():
    lenders = load_lenders()
    rng = random.Random(SEED)
    bank_ids = [l.lender_id for l in lenders.values() if l.lender_type.endswith("bank")]
    pop = [synth(rng, i, bank_ids) for i in range(N)]
    res = [assess(p, lenders) for p in pop]

    pair_fail = Counter()        # (applicant, lender) pairs failing each rule
    sole_fail = Counter()        # pairs where this was the ONLY failed rule (the binding rule)
    hard_block = Counter()       # applicants rejected everywhere: rule failing at the most lenders
    approved = defaultdict(int)
    max_loans, rates = defaultdict(list), defaultdict(list)
    by_type = defaultdict(lambda: [0, 0])
    best_count = Counter()
    for r in res:
        for lr in r["rejected_lenders"]:
            labels = {f.label for f in lr.failures}
            pair_fail.update(labels)
            if len(labels) == 1:
                sole_fail.update(labels)
        for lr in r["approving_lenders"]:
            approved[lr.lender_id] += 1
            max_loans[lr.lender_id].append(lr.max_loan)
            rates[lr.lender_id].append(lr.rate_pct)
        for lr in r["approving_lenders"] + r["rejected_lenders"]:
            by_type[lr.lender_type][0] += lr.eligible
            by_type[lr.lender_type][1] += 1
        if r["eligible"]:
            best_count[r["best"].lender_name] += 1
        else:
            hard_block[next(iter(r["blocker_counts"]))] += 1

    n_pairs = N * len(lenders)
    elig = sum(r["eligible"] for r in res)
    n_lenders = [len(r["approving_lenders"]) for r in res]

    # sensitivity: +50 score points for scored applicants
    def lenders_open(p):
        return len(assess(p, lenders)["approving_lenders"])
    sample = [p for p in pop[:1000] if p.credit_score is not None and p.credit_score < 750]
    gain = []
    for p in sample:
        before = lenders_open(p)
        p.credit_score += 50
        gain.append(lenders_open(p) - before)
        p.credit_score -= 50
    emi_sample = [p for p in pop[:1000] if p.existing_emi > 0]
    emi_gain = []
    for p in emi_sample:
        before, old = lenders_open(p), p.existing_emi
        p.existing_emi = 0
        emi_gain.append(lenders_open(p) - before)
        p.existing_emi = old

    rules = _read("rules_long.csv")
    est_share = {lid: sum(r["is_estimate"] == "true" for r in rules if r["lender_id"] == lid) /
                 sum(r["lender_id"] == lid for r in rules) for lid in lenders}

    md = ["# Insights", "",
          f"Generated by `python scripts/insights.py`: the engine run on **{N:,} synthetic applicants** "
          f"(seed {SEED}) against all 20 lenders ({n_pairs:,} applicant-lender checks). "
          "The population is made up, because no approval data exists. The numbers show how the "
          "**rule set** behaves, not real approval rates.", "",
          "## Headline", "",
          f"* **{pct(elig / N)}** of synthetic applicants qualify at one or more lenders; "
          f"median {median(n_lenders):.0f} lenders each.",
          f"* {pct(sum(x == 0 for x in n_lenders) / N)} are rejected everywhere; "
          f"{pct(sum(x >= 10 for x in n_lenders) / N)} have 10 or more lenders to choose from.",
          f"* +50 score points opens on average **{sum(gain) / len(gain):.1f} more lenders** for applicants "
          f"below 750 (n={len(gain)}); clearing all existing EMIs opens **{sum(emi_gain) / len(emi_gain):.1f}** "
          f"more for applicants with EMIs (n={len(emi_gain)}).", "",
          "## Which rule fails the most applicants", "",
          "*Pair share* = share of all applicant-lender checks failing the rule. *Sole reason* = checks where it "
          "was the only failed rule (fix it and the loan is approved). *Rejected everywhere* = applicants "
          "with no lender, by the rule that failed at the most lenders.", "",
          "| Rule | Pair share | Sole reason (checks) | Rejected everywhere (applicants) |",
          "|---|---|---|---|"]
    for label, c in pair_fail.most_common():
        md.append(f"| {label} | {pct(c / n_pairs)} | {sole_fail[label]:,} | {hard_block[label]:,} |")

    md += ["", "## How lenders differ", "",
           "| Lender | Type | Approval rate | Median max loan (approved) | Median expected rate | Share of rules estimated | Times best option |",
           "|---|---|---|---|---|---|---|"]
    for lid, l in sorted(lenders.items(), key=lambda kv: -approved[kv[0]]):
        ml = f"Rs {median(max_loans[lid]):,.0f}" if max_loans[lid] else "-"
        rt = f"{median(rates[lid]):.1f}%" if rates[lid] else "-"
        md.append(f"| {l.name} | {l.lender_type} | {pct(approved[lid] / N)} | {ml} | {rt} | "
                  f"{pct(est_share[lid])} | {best_count[l.name]:,} |")

    md += ["", "### By lender type", "", "| Type | Approval rate (per check) |", "|---|---|"]
    for t, (a, n) in sorted(by_type.items(), key=lambda kv: -kv[1][0] / kv[1][1]):
        md.append(f"| {t} | {pct(a / n)} |")

    md += ["", "## Population assumptions", "", POPULATION_ASSUMPTIONS]
    (ROOT / "research/insights.md").write_text("\n".join(md))
    print(f"Wrote research/insights.md ({N} applicants)")


if __name__ == "__main__":
    main()
