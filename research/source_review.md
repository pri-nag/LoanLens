# Official-source review (read 2026-10-12)

The first pass (2026-10-11) filled most unpublished rules with one default per lender type. This review went
back to each lender's **own** pages and documents to find the rules they do not list on the eligibility page.
Every value below is in [`data/rules_long.csv`](../data/rules_long.csv) with its page in
[`data/sources.csv`](../data/sources.csv).

## Method

For each lender, the same public pages were read (no login): product page, eligibility page, rates and charges
page, FAQ, Most Important Terms and Conditions / schedule of charges PDFs, EMI and eligibility calculators. Pages
were downloaded and the text searched for age, income, experience, employer, score, FOIR, amount, tenure, rate
and fee terms. Where a page loads its content with JavaScript, the embedded page data and the calculator's own
script were read instead.

Two kinds of hidden rule turned up repeatedly:

* **Calculator code and configuration.** ICICI's eligibility calculator computes
  `max loan = PV(income × FOIR − existing EMIs, rate, tenure)`, caps it at Rs 50 lakh and rejects below
  Rs 50,000. Its configuration file (`organizations.json`, public) lists **71,164 employers in five tiers**
  (Elite, Super Prime, Preferred, Open Market, Government), each with FOIR 70%, 60 months and 10.50%.
* **RBI-mandated rate disclosures.** Lenders publish the minimum, maximum and **mean** rate they actually charged
  last quarter. These show where a typical borrower lands in the advertised band: HDFC 9.99-24% band, mean
  10.89%; ICICI 9.99-16.50%, mean 11.45%; SBI 10-15%, mean 11.54%; IndusInd online PL 12-15%, mean 12.80%. The
  model now prices a typical borrower at the mean instead of a straight line through the band.

## Calculators driven in a browser

Seven eligibility calculators were driven with Playwright (public pages, no login): income Rs 30,000-2 lakh, existing
EMIs Rs 0-20,000, and every tenure the calculator offers. The answers are in
[`research/probes.csv`](probes.csv); `scripts/calibrate.py` inverts them and replays them through the engine.

| Calculator | Inputs | What it computes |
|---|---|---|
| Poonawalla Fincorp | 45 | PV of (FOIR x income - EMIs) at a fixed 14%; FOIR 55% up to Rs 50,000, 65% from Rs 55,000 (income rounded to Rs 1,000); cap Rs 20 lakh; no salary multiple |
| Axis Bank | 9 | 15 x net income; existing EMIs ignored; cap Rs 15 lakh |
| Kotak Mahindra | 27 (9 kept) | 20 x (income - EMIs); identical at 36, 60 and 72 months |
| IDFC FIRST | 9 | 10 x (income - EMIs); cap Rs 15 lakh |
| L&T Finance | read from its script | Returns Rs 0 for every input: its shared script only defines FOIR for home loans (80/75/70/60%) and LAP |
| Tata Capital | 45 (page's own calculator class, 'cat a' employer) | min(multiple x income, PV of FOIR room at 10.99%); FOIR 50% to Rs 25k, 60% to 50k, 65% to 75k, 75% above; multiple by employer category x tenure x income (cat A 6-27x); employer API returned HTTP 503, so the class the page calls after an employer is picked was run directly |
| Aditya Birla Capital | 27 | (4/8/11/14/17/20/23)x (income - EMIs) for 1-7 years, unless FOIR 65% (<Rs 75k) / 70% (<1.5L) / 75% binds; cap Rs 50 lakh |
| Fibe | 9 | New EMI <= min(70% of income - expenses, 30% of income) at 2% a month; tenure 12/24/36 m by income; Rs 50,000 floor, Rs 10 lakh cap |
| Bajaj Finance | read from its code | PV of (75% - expenses/income) x income at 10% over 60 m, capped at 10x income; not driven: its city list API refuses a headless browser |
| HDFC, SBI, PNB, IndusInd, HDB, YES, Navi, Moneyview | none | No public personal-loan eligibility calculator; KreditBee's 'eligibility calculator' takes no income (EMI calculator) |

The Kotak result also corrects an earlier inference: its FAQ example (Rs 56,000 income -> about Rs 10 lakh) had been
read as FOIR of 34-39%, but it is the 20x multiple (Rs 11.2 lakh, rounded down in the FAQ).

## What changed, lender by lender

| Lender | Pages read | Main findings (official unless marked) |
|---|---|---|
| HDFC Bank | product, eligibility, rates & charges, EMI calculator, FOIR article | Rs 25,000-50 lakh; up to 72 months (festive offer; calculator to 84); **9.99% only on Rs 15 lakh+**; mean rate 10.89%; self-employed sent to Business Loan (was "accepted"); LLP employees accepted, proprietorships not; FOIR 40-55% (own article). Calculator EMIs reproduced to the rupee (`tests/test_finance.py`). |
| ICICI Bank | product, eligibility, rates, FAQ, calculator script + employer file | Age 18-58; Rs 30,000; 2 yrs experience; Rs 50,000-50 lakh; 12-84 months; 9.99-16.50%, mean 11.45%; fee up to 2%; **FAQ: FOIR preferred below 40-45%, above 50% sharply cuts approval**; calculator applies 70% (upper bound); employer master with 5 tiers. |
| Axis Bank | product, rates & charges, eligibility & documents | Rs 50,000-50 lakh; up to 84 months; 9.99-22%; Rs 15,000 for Axis customers vs Rs 25,000 others; **lends only in 65 listed cities, in four tiers**; existing EMIs should stay under 40% of take-home pay; **calculator: 15 x income**. |
| Kotak Mahindra | eligibility, rates, fees, FAQ | Up to Rs 1 crore; up to 72 months; from 10.99%; fee up to 5%; MNC / public / private ltd only; Rs 25,000 with Kotak salary account vs Rs 30,000 without; 1 yr experience; CIBIL 685+; **calculator: 20 x (income - EMIs)**. |
| IndusInd Bank | product, rates disclosure | Online PL Rs 30,000-5 lakh, 12-48 months; **actual rates 12-15%, mean 12.80%** (band was 10.49-24%); CIBIL 730+; 1 year at current address if renting (not modelled); self-employed Rs 4.8 lakh, 4-5 yrs. |
| IDFC FIRST Bank | product | Rs 50,000-15 lakh; 9-60 months; fee 0-3.5% incl. GST; CIBIL 710+; salaried or self-employed; **calculator: 10 x (income - EMIs)**. |
| YES BANK | product (embedded data), schedule of charges PDF | Rs 50,000-50 lakh; from 10.85%; fee up to 2.5%. Eligibility criteria are not published; aggregator values kept. |
| SBI | product, rates page, MITC PDF | **FOIR (EMI/NMI) up to 65% and 30x NMI** (was 50% and 24x); salary package account required; govt/defence vs corporate: Rs 20,000 vs Rs 25,000, 6 vs 12 months' service; Rs 1-50 lakh; 6-84 months; 10-15%, mean 11.54%; fee 1.5% capped at Rs 15,000, halved for govt and CIBIL 800+. |
| Bank of Baroda | product, scheme page, calculator page | **Full segment grid**: FOIR 75% / 70% / 40-70% and tenure 84 / 72 / 48-60 months for govt with BoB salary / govt elsewhere / others; CIBIL-linked rates 10.65-15.50% to 13.90-17.50% by segment; private and self-employed applicants without 6 months' BoB relationship capped at Rs 2 lakh; CIBIL 701+; no minimum salary; LLP employees accepted. |
| Punjab National Bank | scheme page; Swaagat via news and aggregator | **Scheme for public requires salary drawn from PNB** (was "not required", which made PNB the best option for most profiles); 24x gross salary, max Rs 20 lakh, 72 months, third-party guarantee. New-to-bank applicants get **Swaagat** (aggregator/news): up to Rs 10 lakh or 10x net salary, rate by CIBIL band 11.60 / 12.60 / 13.60%, no-hit accepted. |
| Bajaj Finance | product, fees, salaried page, eligibility calculator | Rs 40,000-55 lakh; up to 108 months; 10-30.5%; fee up to 4.13% incl. tax; CIBIL 650+ (was 685); **self-employed accepted** (was not); FOIR 50-60%. |
| Tata Capital | product, rates, eligibility calculator | Up to Rs 35 lakh; up to 72 months; age 21-58; Rs 20,000; 1 yr current / 2 yrs total; CIBIL 725+; fee up to 5%; FOIR 40-50%. |
| Aditya Birla Capital | eligibility, salaried page | CIBIL 700+ (another ABCL page says 750); age 21-60; up to 84 months. |
| HDB Financial | salaried page, PL page | Salaried PL up to Rs 10 lakh, 12-60 months; **Rs 20,000 in 8 metros, Rs 15,000 elsewhere**; 1 month in current job; max age 60 (65 for govt); self-employed 3-4 yrs vintage. |
| Poonawalla Fincorp | Prime PL page, eligibility | Up to Rs 15 lakh; 12-84 months; from 9.99%; fee up to 4%; 1 yr experience, 1 month with current employer; CIBIL 700+; **calculator: FOIR 55% / 65%**. |
| L&T Finance | product, fees, eligibility calculator | Up to Rs 30 lakh; 12-72 months; age 21-58; **self-employed accepted** (was not); fee up to 4%; FOIR 50-55%, example uses 50%. |
| Moneyview | product, eligibility check | Up to Rs 10 lakh; 3-60 months; from 14%; **income Rs 25,000** (was Rs 13,500); CIBIL 650+; salaried or self-employed. |
| KreditBee | product | Rs 3,000-10 lakh; 3-60 months; 12-27.5%; fee up to 4.7% + GST; Rs 10,000 personal and Rs 25,000 household income; 2 months in current job. |
| Navi | product (script-rendered) | Up to 84 months, rates up to 29.96%. Other criteria only on aggregators. |
| Fibe | product, eligibility, rates | Age 19-55; salaried only; from 18%; 6-36 months; no processing or foreclosure fee; new-to-credit considered; minimum salary Rs 20,000 (product page) vs Rs 25,000 (eligibility page): Rs 25,000 used. |

## Model changes this required

* **Segment rules** (`rule@govt`, `rule@rel`, `rule@govt_rel`): the same lender applies different FOIR, tenure,
  rate band, income floor or loan cap to government employees and to its own salary-account holders (SBI, BoB,
  Axis, Kotak, HDB, PNB). Four special-purpose rules were folded into this mechanism.
* **`serviceable_cities`**: Axis rejects applicants outside its 65 cities.
* **`rate_by_score`**: rates published per CIBIL band (PNB Swaagat).
* **`rate_avg_pct`**: the disclosed mean rate pins where a typical borrower is priced.
* **`rate_best_min_amount`**: HDFC's 9.99% applies only from Rs 15 lakh; smaller loans start at its mean rate.
* **`foir_bands`, `income_multiple_by_tenure`, `max_new_emi_pct`**: a lender's own FOIR breakpoints
  (Tata, ABCL), a salary multiple that grows with tenure (Tata, ABCL) and a cap on the new EMI alone (Fibe).
* **`max_income_multiple` made optional**: Bank of Baroda sizes loans by FOIR and caps only; the guessed 20x
  multiple was overriding its published FOIR.

## Still not from the lender

* **Bureau-behaviour rules** (days past due, enquiries, write-offs) and new-to-credit acceptance: no lender
  publishes them, so they remain lender-type defaults, marked as estimates.
* **YES BANK eligibility, Navi eligibility and PNB Swaagat**: the official pages do not show them; aggregator
  and news values are used and tiered `aggregator`.
* **FOIR for Kotak, IDFC, YES, HDB, Moneyview, KreditBee, Navi, IndusInd**: no lender-specific statement
  found (Kotak's and IDFC's calculators use a salary multiple instead); lender-type defaults remain.
