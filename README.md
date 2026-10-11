# Personal loan eligibility in India

*"Can I get a personal loan, and from whom?"*

This repo collects the personal-loan rules of **20 Indian lenders**, including the ones they don't publish,
and uses them in a **rule-based model** (no ML). For one applicant it returns:

* **eligible or not**, and if not, why and what would need to change
* the **lenders that would approve**, each with maximum loan, expected rate and tenure
* the **best option** and why it is the best

## Demo Video



https://github.com/user-attachments/assets/c0f1477b-c728-4b64-8229-e45f9a74ba2f





## Quick start

```bash
pip install -r requirements.txt     # pytest, streamlit, openpyxl; the model itself needs only Python 3.10+
python -m pytest -q                 # 195 tests
streamlit run app.py                # LoanLens web UI: pick a test profile or enter your own
python scripts/assess.py my.json    # assess one profile from a JSON file (same fields as the test profiles)
```

`make all` rebuilds every generated file (rule tables, profile results, calibration report, insights) and runs the tests.

## Where to find each deliverable

| The task asks for | File |
|---|---|
| Input variables and their definitions | [`data/input_variables.csv`](data/input_variables.csv): 18 variables with unit, type, description and source (bureau / applicant / document) |
| Rules for 20 lenders, with source and date | [`data/lender_rules.csv`](data/lender_rules.csv): **one row per lender**; easier to read as [`data/lender_rules.md`](data/lender_rules.md) or [`data/lender_rules.xlsx`](data/lender_rules.xlsx) |
| Model code | [`src/loan_engine/engine.py`](src/loan_engine/engine.py) |
| Test profiles and output for each | [`test_profiles/profiles.json`](test_profiles/profiles.json) → [`test_profiles/results.md`](test_profiles/results.md) |
| How the hidden rules were found | [`research/source_review.md`](research/source_review.md) |

Supporting files: `data/rules_long.csv` is the source of truth (one row per lender × rule; the one-row-per-lender
table is generated from it), `data/sources.csv` lists every source with its URL and the date it was read,
`research/probes.csv` holds the calculator answers, and `research/insights.md` has the full analysis.

---

## 1. How the lenders were chosen

No one publishes comparable personal-loan book sizes per lender, so I chose in two steps:

1. **Split the 20 places by segment, using market share.** CRIF High Mark data
   ([MKT-1](https://crifhighmark.com/news-events/news/2025/jan/personal-loan-growth-slows-to-138-in-h1fy25-long-term-delinquencies-rise-crif),
   [MKT-2](https://www.crifhighmark.com/media/6260/how-india-lends-feb-2026.pdf)): by **value**, PSU banks hold
   38%, private banks 33%, NBFCs 24%. By **number of loans**, NBFCs and fintechs make 91%. To cover both, the
   split is **3 PSU banks, 7 private banks, 6 NBFCs, 4 fintechs**.
2. **Take the largest in each segment** that publishes eligibility information without a login.

| Segment | Lenders |
|---|---|
| PSU banks | SBI, Bank of Baroda, Punjab National Bank |
| Private banks | HDFC Bank, ICICI Bank, Axis Bank, Kotak Mahindra Bank, IndusInd Bank, IDFC FIRST Bank, YES BANK |
| NBFCs | Bajaj Finance, Tata Capital, Aditya Birla Capital, HDB Financial Services, Poonawalla Fincorp, L&T Finance |
| Fintechs | Moneyview, KreditBee, Navi, Fibe |

The reason for each lender is in [`data/lenders.csv`](data/lenders.csv).

## 2. Approach

<img width="3400" height="1520" alt="pipeline" src="https://github.com/user-attachments/assets/cc8e3723-b0b1-4000-8cae-d7979938fad1" />

**Data.** Each rule is one row: lender, rule, value, source, and whether it is **official**, from an
**aggregator** site, or an **estimate**. Every row links a source page and a date; estimates also say how
the value was set. A validator checks every row before the model runs.

| Evidence | Rows |
|---|---|
| Lender's own website, PDF or calculator | 295 |
| Comparison sites or news (only where the lender shows nothing) | 58 |
| Estimate (method explained on the row) | 271 |

**The model** runs three stages for every lender:

1. **Knock-out rules:** age, city, income floor, work experience, employer type, self-employed rules,
   credit score, missed payments (DPD), recent enquiries and write-offs. Every failed rule is recorded with
   "has X, needs Y", not just the first one.
2. **Loan size:** the smallest of three limits:
   * **FOIR:** how much EMI the income can carry after existing EMIs, turned into a loan amount;
   * **salary multiple:** for lenders that use one, e.g. Axis lends up to 15× monthly income;
   * **product cap:** the lender's maximum loan.

   Tenure is capped by the lender's maximum and by the age limit at the end of the loan.
3. **Price and rank:** the expected rate is placed within the lender's published rate band according to the
   applicant's risk; where the lender publishes the average rate it actually charged, that is used for a
   typical borrower. Lenders are ranked by **APR** (rate plus processing fee and GST). A lender whose rules are
   mostly estimates gets 1-2 APR points added in the ranking, so it only wins if it is clearly cheaper.

Some lenders treat groups differently: for example, Bank of Baroda gives government employees with a BoB salary
account a higher FOIR and a longer tenure. Such rules carry a tag (`@govt`, `@rel` for a salary account with the
lender, or `@govt_rel` for both) and replace the general rule for that group.

## 3. Assumptions, and how the unlisted rules were found

Each lender's own pages were read on **2026-10-11 and 2026-10-12**: product page, eligibility page, rates and
charges, FAQ, terms PDFs and calculators. The full list is in
[`research/source_review.md`](research/source_review.md). The unlisted rules came from five places:

1. **Eligibility calculators.** I drove 7 lender calculators with a script (`scripts/probe_calculators.py`),
   entering different incomes, existing EMIs and tenures, and read the formula in their page code. The answers
   (153 in all) reveal the hidden FOIR and salary multiples. Examples: Bajaj allows 75% FOIR but caps the loan at
   10× income; Kotak lends 20× (income − EMIs); Fibe caps the new EMI at 30% of income. The model reproduces
   **142 of 148** replayed calculator answers exactly and all of them within 3%; the tests check this.
2. **Scheme pages and terms PDFs.** For example, SBI allows EMIs up to 65% of income and 30× salary; PNB's
   public scheme is only for people whose salary goes into PNB.
3. **FAQs on the lender's own site.** For example, ICICI prefers FOIR below 40-45%, and Axis lends in only 65
   cities.
4. **Rate disclosures.** Lenders publish the average rate they actually charged last quarter (HDFC 10.89%
   within a 9.99-24% band), which shows where a typical borrower lands.
5. **Comparison sites**, only where the lender's own pages show nothing (YES BANK, Navi, PNB's Swaagat loan).

**Main assumptions**

* **Bureau rules are estimates.** No lender publishes its limits on missed payments, enquiries or write-offs.
  These use one value per lender type (for example, banks reject any missed payment in the last 12 months),
  each linked to a lender's credit guide that confirms the rule exists.
* **FOIR defaults.** Where a lender states no FOIR and has no calculator (Kotak, IDFC, YES, IndusInd, HDB,
  Moneyview, KreditBee, Navi), a default for its lender type is used: 50-60% for banks, 55-65% for NBFCs.
* **Calculator values are taken as the lender's rule.** Calculators use one fixed rate, so the model takes
  only the sizing rule from them. Tata's multiple depends on its own employer categories; category A is used
  for everyone.
* **Simple conventions:** "metro" means the 8 cities in HDB's list; self-employed monthly income = ITR / 12;
  "age 21 to 60" means age at the end of the loan; where a lender has two products, the one an ordinary
  salaried applicant gets is modelled.

## 4. Test profiles and results

17 profiles, including edge cases and 5 that should be rejected everywhere. The full output for each is in
[`test_profiles/results.md`](test_profiles/results.md); the UI can load any of them.

| Profile | Scenario | Result |
|---|---|---|
| P01 | Strong salaried applicant, ₹1.2L income, score 805 | 19 lenders; best ICICI |
| P02 | **Low score** (680) | 5 lenders, all fintechs or Bajaj; banks reject on score |
| P03 | **High existing EMI** (55% of income) | 6 lenders; only Bajaj can lend the full ₹8L |
| P04 | **New job** (3 months) | 4 lenders, all fintechs |
| P05 | **Self-employed** doctor | 13 lenders; best ICICI |
| P06 | **Age near the limit** (56, wants 5 years) | 17 lenders, most cut the tenure to 48 months |
| P07 | No credit history | 3 fintechs only, at 27-36% APR |
| P08 | Low income (₹14k), small town | 2 lenders: PNB and KreditBee |
| P09 | Write-off and missed payments | **Not eligible**: needs no write-off and DPD ≤ 30 |
| P10 | Large loan (₹45L) | 19 lenders, 6 can lend it all; best HDFC |
| P11 | 7 enquiries and a 30-day late payment | 4 fintechs only |
| P12 | Exactly at the usual thresholds | Checks that limits are inclusive (21 years, ₹25,000, score 700) |
| P13 | Self-employed, 2-year-old business | 5 lenders |
| P14 | Age 18, first job | **Not eligible**: too young |
| P15 | Score 580 | **Not eligible**: below every lender's cut-off |
| P16 | Existing EMIs = 75% of income | **Not eligible**: no room for a new EMI |
| P17 | Self-employed, 6-month-old business | **Not eligible**: business too new |

## 5. Insights

From running the model on 5,000 made-up applicants (details in [`research/insights.md`](research/insights.md);
these describe the rules, not real approval rates):

* **Credit score fails the most applicants:** 26% of all applicant-lender checks, followed by the income floor
  (18%), missed payments (10%) and having no credit history (10%).
* **Fixing the credit record helps more than paying off debt:** +50 score points opens about 2.5 more lenders;
  clearing all existing EMIs opens about 0.6.
* **People rejected everywhere are mostly rejected for their bureau record** (missed payments, low score,
  write-offs), not for income.
* **Lender types differ in risk appetite:** fintechs approve 51% of checks, NBFCs 34%, PSU banks 24%, private
  banks 21%. Rates move the other way: about 11-12% at the big banks against 19-23% at most fintechs.
* **NBFC calculators allow much more FOIR than banks say:** Tata, Aditya Birla and Bajaj go up to 75%, against
  40-55% in HDFC's and ICICI's guidance.
* **PSU banks favour their own customers:** SBI's and PNB's main schemes need your salary account with them,
  and Bank of Baroda caps private-sector applicants without a BoB relationship at ₹2L.
* **Advertised rates overstate the typical rate:** HDFC advertises 9.99-24% but charged 10.89% on average.

## 6. Limits and what to add next

**Limits**

* **43% of rule rows are estimates**, mostly bureau rules no lender publishes. Each one says how it was set.
* **No approval data**, so "eligible" means the profile passes the published and inferred rules, not that a
  lender will approve it.
* **The 1-2 point confidence margin in the ranking is a judgement call**, not calibrated.
* **Not modelled:** co-applicants, guarantors, residence stability, pre-approved offers, top-ups and balance
  transfers; one product per lender.

