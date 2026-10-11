# How unpublished rules are reverse-engineered from lender calculators

Lenders publish only some rules (age, minimum salary, sometimes a score cut-off). Their **eligibility
calculators** run the underwriting maths that the bank does not publish. Feeding a calculator controlled
inputs and inverting the output recovers those hidden rules.

## 1. Inputs to change, one at a time

| Probe set | Vary | Hold fixed | Reveals |
|---|---|---|---|
| Income sweep | 15k, 25k, 40k, 60k, 1L, 2L, 5L | EMI 0, 60 m | FOIR by income band; minimum income (where result turns "not eligible"); multiple/cap at high incomes |
| Existing-EMI sweep | 0, 5k, 10k, 20k | 60k income, 60 m | Whether existing EMIs are subtracted inside FOIR |
| Tenure sweep | 12 ... 84 m | 60k income, EMI 0 | Which rule binds (see below) |
| Age sweep | 25, 45, 55, 58, 60 | all | Age-at-maturity limit (tenure gets cut) |
| Drop-downs | city, employer, salaried/self-employed | all | Segment differences |
| Bisection | income or EMI near the flip point | all | Exact thresholds and >= vs > |

Which rule binds:

* Loan grows with tenure along the present-value curve -> **FOIR binds**.
* Loan flat across tenures but grows with income -> **salary multiple binds** (loan / income constant).
* Flat across tenure and income -> **product cap binds**.
* Existing EMI up by Rs 10k cuts the loan by exactly PV(Rs 10k) -> existing EMIs sit **inside FOIR**.

Worked example (probe `B1-01`): income Rs 50,000, no EMI, 60 months at 11% -> calculator shows Rs 11.5 lakh.
EMI on Rs 11.5 lakh = Rs 25,003, so implied FOIR = 25,003 / 50,000 = **50%**.

## 2. Getting the answer out of the calculator (best first)

1. **Read the formula.** DevTools -> Sources: search the JS for `foir`, `emi`, `eligib`, `0.5`. Or DevTools ->
   Network (Fetch/XHR): change an input and look for a JSON call returning the eligible amount. Save the JS or
   the request/response as evidence.
2. **Probe by hand** using the table above (about 15-20 probes per lender is enough).
3. **Automate** with Playwright (`scripts/probe_calculators.py`, used for the Axis, Kotak, IDFC, Poonawalla, Tata, ABCL and Fibe
   probes) only if more than about 30 probes are needed. Public pages only, no login, one request
   every few seconds, respect robots.txt and the site's terms.

## 3. Recording and using probes

1. Append each probe to `research/probes.csv` (one row per calculator answer, with URL and date).
2. Run `python scripts/calibrate.py` -> `research/calibration_report.md` shows implied FOIR / multiple per
   lender and income band, and **replays each probe through the engine** to show model error.
3. If the implied value differs from `data/rules_long.csv`, update the rule row: set
   `evidence_tier=lender_official` if it came from the lender's own calculator, set `is_estimate=false`, and put
   the probe ids in `notes`.
4. `tests/test_calibration.py` fails if any lender probe is reproduced with more than 3% error. This stops a later
   rule edit from silently breaking agreement with the lender's own calculator.

Calculators round (often to Rs 1k / 10k / 50k): report fitted values as ranges, e.g. "FOIR 49.6-50.3% -> 50%".
Use the rate the calculator itself applied, not the headline rate, and note whether it asks for net or gross income.

## Status in this repo

`research/probes.csv` holds 72 lender calculator answers captured on 2026-10-12 with Playwright (headless Chromium,
public pages): Poonawalla 45, Axis 9, Kotak 9, IDFC 9, plus two benchmark-calculator results from the first build.
Each row records the calculator's own rate, tenure and cap, and whether it is replayed (`replay`). Rows are not
replayed when the calculator ignores something the model keeps on purpose (Axis ignores EMIs; Kotak and IDFC apply
no FOIR); the reason is in `notes`.

What the sweeps showed:

* Poonawalla: the loan grows with tenure and falls one-for-one with EMIs inside FOIR, so FOIR binds. Inverting at its
  14% rate gives FOIR 55% (income <= Rs 50,000) and 65% (from Rs 55,000), stable to three decimals.
* Axis, Kotak, IDFC: the loan does not move with tenure, so a salary multiple binds: 15x income (Axis, EMIs
  ignored), 20x and 10x income net of EMIs (Kotak, IDFC).

Calculators read as code instead of probed: ICICI (formula and employer file `ICICI-P7`) and L&T (script defines no
personal-loan FOIR, so the page always shows Rs 0). Still to probe: Tata Capital (needs an employer from its list),
Bajaj (city and date of birth), ICICI and HDFC with an employer selected.
