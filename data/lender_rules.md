# Lender rule sheet

Generated from `data/rules_long.csv` by `python scripts/build_rules.py`. Tier: **O** = lender's own site, **A** = aggregator, **E** = estimate (method given). All sources read on the date shown. A rule ending in `@govt`, `@rel` or `@govt_rel` applies only to government/PSU employees, applicants with a salary account at this lender, or both, and overrides the plain rule for them.

## State Bank of India (`sbi`, psu_bank)

35 rules, 10 estimated. Why chosen: Largest PL book in the PSB segment; Xpress Credit is the benchmark govt-salary product.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 |  |
| max_age_at_maturity | 60 | years | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | Loan to close by retirement / 60 years |
| max_age_at_maturity_se | 65 | years | E | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Not published by State Bank of India. psu bank default, the value Bank of Baroda publishes for this rule (linked) |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by State Bank of India. psu bank default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 25000 | INR/month | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | Corporate sector employees |
| min_income_metro@govt | 20000 | INR/month | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | Government / defence employees |
| min_income_non_metro | 25000 | INR/month | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | Corporate sector employees |
| min_income_non_metro@govt | 20000 | INR/month | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | Government / defence employees |
| min_total_exp_months | 12 | months | E | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Not published by State Bank of India. psu bank default, the value Bank of Baroda publishes for this rule (linked) |
| min_current_job_months | 12 | months | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | Corporate sector minimum service |
| min_current_job_months@govt | 6 | months | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | Government / defence minimum service |
| allowed_employer_categories | govt, psu, mnc, listed, pvt_ltd | list | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | Government (central/state/railway/police/PSU), defence and corporate sector |
| salary_account_required | true | flag | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | 'Employee should have Salary Package Account with SBI' |
| self_employed_allowed | false | flag | O | [SBI-P4](https://sbi.bank.in/documents/16012/74139/10062022_MITC-+Personal+Loans.pdf/c6daf9fa-9c12-f2e4-bd7b-b125b225498b?t=1654855715349) | 2026-10-12 | Salaried employees only |
| se_min_vintage_months | 36 | months | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by State Bank of India. psu bank default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_annual_income | 300000 | INR/year | E | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | State Bank of India's eligibility page (linked) is silent on this rule. Lender-type default (psu bank) |
| min_credit_score | 700 | score | E | [PNB-A3](https://www.bankbazaar.com/punjab-national-bank-personal-loan-interest-rates.html) | 2026-10-12 | Not published by State Bank of India. psu bank default, the value Punjab National Bank publishes for this rule (linked) |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (psu bank). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 0 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 4 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.65 | ratio | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | 'subject to EMI/NMI Ratio upto 65%' |
| foir_50k_1l | 0.65 | ratio | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | 'subject to EMI/NMI Ratio upto 65%' |
| foir_ge_1l | 0.65 | ratio | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | 'subject to EMI/NMI Ratio upto 65%' |
| max_income_multiple | 30 | x monthly income | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | '& 30-times NMI, whichever is lower' |
| min_loan_amount | 100000 | INR | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 |  |
| max_loan_amount | 5000000 | INR | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 |  |
| min_tenure_months | 6 | months | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 |  |
| max_tenure_months | 84 | months | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 |  |
| rate_min_pct | 10.0 | % p.a. | O | [SBI-P3](https://sbi.bank.in/web/interest-rates/interest-rates/loan-schemes-interest-rates/personal-loans-schemes) | 2026-10-12 |  |
| rate_max_pct | 15.0 | % p.a. | O | [SBI-P3](https://sbi.bank.in/web/interest-rates/interest-rates/loan-schemes-interest-rates/personal-loans-schemes) | 2026-10-12 |  |
| processing_fee_pct | 0.015 | ratio | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | Min Rs 1,000 |
| processing_fee_pct@govt | 0.0075 | ratio | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 | 50% waiver for government sector employees |
| processing_fee_cap | 15000 | INR | O | [SBI-P2](https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan) | 2026-10-12 |  |
| rate_avg_pct | 11.54 | % p.a. | O | [SBI-P3](https://sbi.bank.in/web/interest-rates/interest-rates/loan-schemes-interest-rates/personal-loans-schemes) | 2026-10-12 | Mean ROI Q1 FY2026-27 |

## Bank of Baroda (`bob`, psu_bank)

48 rules, 11 estimated. Why chosen: Second PSB; publishes city-tier loan limits.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 |  |
| max_age_at_maturity | 60 | years | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Age plus repayment period within retirement age or 60 |
| max_age_at_maturity_se | 65 | years | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 |  |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by Bank of Baroda. psu bank default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 0 | INR/month | O | [BOB-P1](https://bankofbaroda.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 | 'There is no such stipulation' of a minimum salary; repayment capacity (FOIR) decides |
| min_income_non_metro | 0 | INR/month | O | [BOB-P1](https://bankofbaroda.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 | As above |
| min_total_exp_months | 12 | months | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Only continuous service is stated |
| min_current_job_months | 12 | months | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Minimum continuous service 1 year |
| allowed_employer_categories | govt, psu, mnc, listed, pvt_ltd, llp | list | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Govt, PSU, public ltd/MNC, educational institutions, private ltd, trusts, LLPs |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by Bank of Baroda. psu bank default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | true | flag | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 |  |
| se_min_vintage_months | 12 | months | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Minimum 1 year stable business |
| se_min_annual_income | 300000 | INR/year | E | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Bank of Baroda's eligibility page (linked) is silent on this rule. Lender-type default (psu bank) |
| min_credit_score | 701 | score | O | [BOB-P1](https://bankofbaroda.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 | 'CIBIL score must be above 701 and above' |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (psu bank). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 0 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 4 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.4 | ratio | E | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | BoB: '40% of GMI to 70% of GMI depending upon the income'; mapped low to high across income bands (BoB uses gross income, the model uses net) |
| foir_lt_50k@govt | 0.7 | ratio | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | 70% of GMI: govt/PSU employees with salary account in another bank |
| foir_lt_50k@govt_rel | 0.75 | ratio | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | 75% of GMI: govt/PSU employees with BoB salary account |
| foir_50k_1l | 0.55 | ratio | E | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | BoB: '40% of GMI to 70% of GMI depending upon the income'; mapped low to high across income bands (BoB uses gross income, the model uses net) |
| foir_50k_1l@govt | 0.7 | ratio | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | 70% of GMI: govt/PSU employees with salary account in another bank |
| foir_50k_1l@govt_rel | 0.75 | ratio | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | 75% of GMI: govt/PSU employees with BoB salary account |
| foir_ge_1l | 0.7 | ratio | E | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | BoB: '40% of GMI to 70% of GMI depending upon the income'; mapped low to high across income bands (BoB uses gross income, the model uses net) |
| foir_ge_1l@govt | 0.7 | ratio | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | 70% of GMI: govt/PSU employees with salary account in another bank |
| foir_ge_1l@govt_rel | 0.75 | ratio | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | 75% of GMI: govt/PSU employees with BoB salary account |
| min_loan_amount | 100000 | INR | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Metro and urban branches |
| max_loan_amount | 200000 | INR | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Private-sector and self-employed applicants without 6 months' BoB relationship |
| max_loan_amount@govt | 2000000 | INR | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Govt employees, salary with BoB or another bank |
| max_loan_amount@rel | 2000000 | INR | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | With BoB account relationship |
| max_loan_amount_non_metro | 1500000 | INR | O | [BOB-P1](https://bankofbaroda.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 |  |
| min_loan_amount_non_metro | 50000 | INR | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Rural and semi-urban branches |
| min_tenure_months | 12 | months | E | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | Not published by Bank of Baroda. psu bank default, the value HDB Financial Services publishes for this rule (linked) |
| max_tenure_months | 60 | months | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | 48-60 months for other applicants |
| max_tenure_months@govt | 72 | months | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 |  |
| max_tenure_months@govt_rel | 84 | months | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 |  |
| rate_min_pct | 13.9 | % p.a. | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Category A (no BoB relationship), floating, CIBIL-linked |
| rate_min_pct@govt | 11.15 | % p.a. | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Silver: govt employees with salary in another bank |
| rate_min_pct@rel | 11.9 | % p.a. | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Category B (BoB relationship) |
| rate_min_pct@govt_rel | 10.65 | % p.a. | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | Gold: govt employees with BoB salary account |
| rate_max_pct | 17.5 | % p.a. | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 |  |
| rate_max_pct@govt | 15.5 | % p.a. | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 |  |
| rate_max_pct@rel | 15.5 | % p.a. | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 |  |
| rate_max_pct@govt_rel | 15.5 | % p.a. | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 |  |
| processing_fee_pct | 0.02 | ratio | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | 1%-2% + GST, min Rs 1,000 |
| processing_fee_pct@govt_rel | 0.0 | ratio | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 | NIL for govt employees with BoB salary account |
| processing_fee_cap | 10000 | INR | O | [BOB-P2](https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan) | 2026-10-12 |  |

## Punjab National Bank (`pnb`, psu_bank)

37 rules, 12 estimated. Why chosen: Third PSB; salary-account scheme plus Swaagat loan for new customers.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | A | [PNB-A1](https://bankbazaar.com/punjab-national-bank-personal-loan-eligibility-calculator.html) | 2026-10-11 |  |
| max_age_at_maturity | 60 | years | A | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 |  |
| max_age_at_maturity_se | 65 | years | O | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 |  |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by Punjab National Bank. psu bank default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 15000 | INR/month | A | [PNB-A1](https://bankbazaar.com/punjab-national-bank-personal-loan-eligibility-calculator.html) | 2026-10-11 |  |
| min_income_non_metro | 12500 | INR/month | A | [PNB-A1](https://bankbazaar.com/punjab-national-bank-personal-loan-eligibility-calculator.html) | 2026-10-11 |  |
| min_total_exp_months | 24 | months | A | [PNB-A1](https://bankbazaar.com/punjab-national-bank-personal-loan-eligibility-calculator.html) | 2026-10-11 |  |
| min_total_exp_months@rel | 24 | months | O | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 | 2 years' service for govt/PSU/reputed companies (3 years for others) |
| min_current_job_months | 6 | months | E | [ABCL-P2](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/loan-of-5-lakh) | 2026-10-11 | Not published by Punjab National Bank. psu bank default, the value Aditya Birla Capital publishes for this rule (linked) |
| allowed_employer_categories | any | list | E | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 | The PNB scheme page (linked) limits its salary-account scheme to govt/PSU/reputed companies, but its 'others need 3 years' clause means others are accepted too; Swaagat, the new-to-bank base product, states no employer restriction, read as any. Lender-type default (psu bank) |
| salary_account_required | false | flag | A | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Swaagat is for new-to-bank customers; PNB salary-account holders use the public scheme (@rel rows) |
| self_employed_allowed | true | flag | O | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 | Self-employed professionals only (CA/CS, engineers, software developers etc.), metro/urban branches |
| se_min_vintage_months | 36 | months | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by Punjab National Bank. psu bank default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_annual_income | 600000 | INR/year | O | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 | Gross annual income for the last two years |
| se_min_credit_score | 750 | score | O | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 |  |
| min_credit_score | 700 | score | A | [PNB-A3](https://www.bankbazaar.com/punjab-national-bank-personal-loan-interest-rates.html) | 2026-10-12 |  |
| ntc_allowed | true | flag | A | [PNB-A3](https://www.bankbazaar.com/punjab-national-bank-personal-loan-interest-rates.html) | 2026-10-12 | '-1/0/no hit' priced in the 700-749 band |
| max_dpd_12m | 0 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 4 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.5 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by Punjab National Bank. Banks: HDFC FOIR blog (40-55%) and benchmark calculator CALC-B1 (50%); NBFCs +5pp (higher risk appetite); fintech flat 50% (low-income book) |
| foir_50k_1l | 0.55 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by Punjab National Bank. Banded FOIR: lenders allow a larger share of income as income rises (more residual income after expenses); base level from HDFC's FOIR article (40-55%, linked) |
| foir_ge_1l | 0.6 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by Punjab National Bank. Banded FOIR for high earners; base level from HDFC's FOIR article (40-55%, linked) |
| max_income_multiple | 10 | x monthly income | A | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Lower of Rs 10 lakh or 10x average net salary of last 10 of 12 months |
| max_income_multiple@rel | 24 | x monthly income | O | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 | 24x gross monthly salary (the model applies it to net salary) |
| min_loan_amount | 25000 | INR | A | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 |  |
| max_loan_amount | 1000000 | INR | A | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 |  |
| max_loan_amount@rel | 2000000 | INR | O | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 |  |
| min_tenure_months | 12 | months | E | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | Not published by Punjab National Bank. psu bank default, the value HDB Financial Services publishes for this rule (linked) |
| max_tenure_months | 72 | months | A | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 |  |
| rate_min_pct | 11.6 | % p.a. | A | [PNB-A3](https://www.bankbazaar.com/punjab-national-bank-personal-loan-interest-rates.html) | 2026-10-12 |  |
| rate_min_pct@rel | 10.6 | % p.a. | A | [PNB-A3](https://www.bankbazaar.com/punjab-national-bank-personal-loan-interest-rates.html) | 2026-10-12 | 'from 10.60%' (2026 page) |
| rate_max_pct | 13.6 | % p.a. | A | [PNB-A3](https://www.bankbazaar.com/punjab-national-bank-personal-loan-interest-rates.html) | 2026-10-12 |  |
| rate_max_pct@rel | 14.35 | % p.a. | A | [PNB-A3](https://www.bankbazaar.com/punjab-national-bank-personal-loan-interest-rates.html) | 2026-10-12 | Upper end quoted for govt employees |
| processing_fee_pct | 0.005 | ratio | A | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | 0.50%, min Rs 500 |
| rate_by_score | 800:11.60, 750:12.60, 700:13.60 | score:rate list | A | [PNB-A3](https://www.bankbazaar.com/punjab-national-bank-personal-loan-interest-rates.html) | 2026-10-12 | Rates as of 15-Sep-2025; the 700-749 band includes no-hit / new-to-credit |
| rate_by_score@rel | none | score:rate list | E | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 | The public scheme is not priced by CIBIL band, so the Swaagat bands are switched off |

## HDFC Bank (`hdfc`, pvt_bank)

32 rules, 12 estimated. Why chosen: Largest private-bank PL lender.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [HDFC-P5](https://www.hdfc.bank.in/personal-loan/eligibility-criteria) | 2026-10-12 | Re-read 2026-10-12 |
| max_age_at_maturity | 60 | years | O | [HDFC-P5](https://www.hdfc.bank.in/personal-loan/eligibility-criteria) | 2026-10-12 | Page says "aged 21 to 60"; whether 60 is at application or at loan end is not stated, treated as age at end of loan |
| max_age_at_maturity_se | 65 | years | A | [HDFC-A1](https://www.bankbazaar.com/hdfc-personal-loan-eligibility-calculator.html) | 2026-10-11 |  |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by HDFC Bank. pvt bank default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 25000 | INR/month | O | [HDFC-P5](https://www.hdfc.bank.in/personal-loan/eligibility-criteria) | 2026-10-12 | BankBazaar shows Rs 20k metro / 15k other; official page Rs 25k used |
| min_income_non_metro | 25000 | INR/month | O | [HDFC-P5](https://www.hdfc.bank.in/personal-loan/eligibility-criteria) | 2026-10-12 | Official page gives one figure for all cities |
| min_total_exp_months | 24 | months | O | [HDFC-P5](https://www.hdfc.bank.in/personal-loan/eligibility-criteria) | 2026-10-12 | Was BankBazaar (HDFC-A1); same value confirmed on HDFC page |
| min_current_job_months | 12 | months | O | [HDFC-P5](https://www.hdfc.bank.in/personal-loan/eligibility-criteria) | 2026-10-12 | Was BankBazaar (HDFC-A1); same value confirmed on HDFC page |
| allowed_employer_categories | govt, psu, mnc, listed, pvt_ltd, llp | list | O | [HDFC-P6](https://www.hdfc.bank.in/personal-loan) | 2026-10-12 | Product page: 'Private, Limited and LLP Companies' and PSUs; eligibility page lists only private limited companies and PSUs; proprietorships not listed |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by HDFC Bank. pvt bank default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | false | flag | O | [HDFC-P6](https://www.hdfc.bank.in/personal-loan) | 2026-10-12 | FAQ: self-employed are offered a Business Loan, not a Personal Loan |
| se_min_vintage_months | 36 | months | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by HDFC Bank. pvt bank default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_annual_income | 500000 | INR/year | A | [HDFC-A1](https://www.bankbazaar.com/hdfc-personal-loan-eligibility-calculator.html) | 2026-10-11 |  |
| min_credit_score | 720 | score | E | [HDFC-P4](https://www.hdfc.bank.in/blogs/personal-loan/what-are-the-eligibility-criteria-for-personal-loans) | 2026-10-11 | HDFC says >750 'favoured' (not a cut-off); hard floor set 30 pts below, scores 720-749 priced higher |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (pvt bank). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 0 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 4 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.45 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | HDFC's own FOIR article gives 40-55% as typical; spread from 45% (low income) to 55% (high income) |
| foir_50k_1l | 0.5 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | HDFC's own FOIR article gives 40-55% as typical; spread from 45% (low income) to 55% (high income) |
| foir_ge_1l | 0.55 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | HDFC's own FOIR article gives 40-55% as typical; spread from 45% (low income) to 55% (high income) |
| max_income_multiple | 24 | x monthly income | E | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 | Not published by HDFC Bank. 24x is the multiple PNB publishes (linked); SBI publishes 30x and the calculators read show 10-20x, so 24x sits mid-range; rarely binds before FOIR |
| min_loan_amount | 25000 | INR | O | [HDFC-P6](https://www.hdfc.bank.in/personal-loan) | 2026-10-12 | Was Rs 50,000 (BankBazaar) |
| max_loan_amount | 5000000 | INR | O | [HDFC-P6](https://www.hdfc.bank.in/personal-loan) | 2026-10-12 | FAQ: up to Rs 75 lakh subject to eligibility; Rs 50 lakh used |
| min_tenure_months | 12 | months | A | [HDFC-A2](https://bankbazaar.com/hdfc-personal-loan-interest-rates.html) | 2026-10-11 |  |
| max_tenure_months | 72 | months | O | [HDFC-P6](https://www.hdfc.bank.in/personal-loan) | 2026-10-12 | FAQ: up to 72 months (festive offer valid till 30-Nov-2026); EMI calculator slider goes to 7 years |
| rate_min_pct | 9.99 | % p.a. | O | [HDFC-P2](https://www.hdfc.bank.in/personal-loan/interest-rates-and-charges) | 2026-10-12 |  |
| rate_max_pct | 24.0 | % p.a. | O | [HDFC-P2](https://www.hdfc.bank.in/personal-loan/interest-rates-and-charges) | 2026-10-12 |  |
| processing_fee_pct | 0.025 | ratio | A | [HDFC-A3](https://groww.in/loans/hdfc-bank-personal-loan-interest-rates) | 2026-10-11 |  |
| processing_fee_cap | 6500 | INR | O | [HDFC-P2](https://www.hdfc.bank.in/personal-loan/interest-rates-and-charges) | 2026-10-12 | Re-read 2026-10-12 |
| rate_avg_pct | 10.89 | % p.a. | O | [HDFC-P2](https://www.hdfc.bank.in/personal-loan/interest-rates-and-charges) | 2026-10-12 | Average IRR on loans sanctioned Apr-Jun 2026 (Q1 FY2026-27) |
| rate_best_min_amount | 1500000 | INR | O | [HDFC-P7](https://www.hdfc.bank.in/personal-loan/emi-calculator) | 2026-10-12 | 'Get 9.99% p.a. on Rs 15 lakh+'; product page: 'above certain loan amount and good credit score' |

## ICICI Bank (`icici`, pvt_bank)

30 rules, 11 estimated. Why chosen: Top private lender; publishes self-employed rules.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 18 | years | O | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | Eligibility page: 18-58 for salaried; product page says 20-58 |
| max_age_at_maturity | 58 | years | O | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 |  |
| max_age_at_maturity_se | 65 | years | O | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 |  |
| se_min_age | 23 | years | O | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 |  |
| min_income_metro | 30000 | INR/month | O | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | 'will differ depending on the profile (type of employer, relationship with ICICI Bank)' |
| min_income_non_metro | 30000 | INR/month | O | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | One figure for all cities |
| min_total_exp_months | 24 | months | O | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 |  |
| min_current_job_months | 6 | months | E | [ABCL-P2](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/loan-of-5-lakh) | 2026-10-11 | Not published by ICICI Bank. pvt bank default, the value Aditya Birla Capital publishes for this rule (linked) |
| allowed_employer_categories | any | list | E | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | ICICI Bank's eligibility page (linked) lists no employer restriction, read as any. Lender-type default (pvt bank) |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by ICICI Bank. pvt bank default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | true | flag | O | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | Page lists self-employed criteria but says they are served through business instalment loans |
| se_min_vintage_months | 24 | months | O | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | 2 years in current business and total experience >= 3 years |
| se_min_annual_income | 200000 | INR/year | O | [ICICI-P1](https://www.icici.bank.in/blogs/personal-loan/eligibility-and-requirement-for-a-personal-loan) | 2026-10-11 | PAT Rs 2 lakh (professionals) |
| min_credit_score | 700 | score | O | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | 'A credit score of 700 and above is preferred'; FAQ lists score below 700 as a rejection reason |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (pvt bank). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 0 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 4 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.45 | ratio | E | [ICICI-P6](https://www.icici.bank.in/personal-banking/loans/personal-loan/personal-loans-faqs) | 2026-10-12 | ICICI FAQ: prefers FOIR below 40-45%, above 50% sharply cuts approval; its own calculator applies 70% to every employer (ICICI-P7), so 70% is only an upper bound |
| foir_50k_1l | 0.5 | ratio | E | [ICICI-P6](https://www.icici.bank.in/personal-banking/loans/personal-loan/personal-loans-faqs) | 2026-10-12 | ICICI FAQ: prefers FOIR below 40-45%, above 50% sharply cuts approval; its own calculator applies 70% to every employer (ICICI-P7), so 70% is only an upper bound |
| foir_ge_1l | 0.5 | ratio | E | [ICICI-P6](https://www.icici.bank.in/personal-banking/loans/personal-loan/personal-loans-faqs) | 2026-10-12 | ICICI FAQ: prefers FOIR below 40-45%, above 50% sharply cuts approval; its own calculator applies 70% to every employer (ICICI-P7), so 70% is only an upper bound |
| max_income_multiple | 24 | x monthly income | E | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 | Not published by ICICI Bank. 24x is the multiple PNB publishes (linked); SBI publishes 30x and the calculators read show 10-20x, so 24x sits mid-range; rarely binds before FOIR |
| min_loan_amount | 50000 | INR | O | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 |  |
| max_loan_amount | 5000000 | INR | O | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 |  |
| min_tenure_months | 12 | months | O | [ICICI-P8](https://www.icici.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 |  |
| max_tenure_months | 84 | months | O | [ICICI-P8](https://www.icici.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 |  |
| rate_min_pct | 9.99 | % p.a. | O | [ICICI-P5](https://www.icici.bank.in/personal-banking/loans/personal-loan/personal-loan-interest-rates) | 2026-10-12 |  |
| rate_max_pct | 16.5 | % p.a. | O | [ICICI-P5](https://www.icici.bank.in/personal-banking/loans/personal-loan/personal-loan-interest-rates) | 2026-10-12 |  |
| processing_fee_pct | 0.02 | ratio | O | [ICICI-P5](https://www.icici.bank.in/personal-banking/loans/personal-loan/personal-loan-interest-rates) | 2026-10-12 | Up to 2% + taxes |
| rate_avg_pct | 11.45 | % p.a. | O | [ICICI-P5](https://www.icici.bank.in/personal-banking/loans/personal-loan/personal-loan-interest-rates) | 2026-10-12 | Mean rate disclosed on the rates page |

## Axis Bank (`axis`, pvt_bank)

32 rules, 15 estimated. Why chosen: Publishes relationship-based income/amount rules.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 |  |
| max_age_at_maturity | 60 | years | O | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 |  |
| max_age_at_maturity_se | 65 | years | E | [HDFC-A1](https://www.bankbazaar.com/hdfc-personal-loan-eligibility-calculator.html) | 2026-10-11 | Not published by Axis Bank. pvt bank default, the value HDFC Bank publishes for this rule (linked) |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by Axis Bank. pvt bank default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 25000 | INR/month | O | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 | Non-Axis customers |
| min_income_metro@rel | 15000 | INR/month | O | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 | Axis Bank customers |
| min_income_non_metro | 25000 | INR/month | O | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 | Non-Axis customers |
| min_income_non_metro@rel | 15000 | INR/month | O | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 | Axis Bank customers |
| min_total_exp_months | 12 | months | E | [KOTAK-P3](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | Not published by Axis Bank. pvt bank default, the value Kotak Mahindra Bank publishes for this rule (linked) |
| min_current_job_months | 6 | months | E | [ABCL-P2](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/loan-of-5-lakh) | 2026-10-11 | Not published by Axis Bank. pvt bank default, the value Aditya Birla Capital publishes for this rule (linked) |
| allowed_employer_categories | govt, psu, mnc, listed, pvt_ltd | list | O | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 | Public and private limited companies; govt sector incl. PSU |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by Axis Bank. pvt bank default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | false | flag | O | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 | Page lists salaried applicants only |
| se_min_vintage_months | 36 | months | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by Axis Bank. pvt bank default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_annual_income | 500000 | INR/year | E | [HDFC-A1](https://www.bankbazaar.com/hdfc-personal-loan-eligibility-calculator.html) | 2026-10-11 | Not published by Axis Bank. pvt bank default, the value HDFC Bank publishes for this rule (linked) |
| min_credit_score | 700 | score | A | [AXIS-A1](https://bankbazaar.com/cibil/cibil-score-for-personal-loan-in-axis-bank.html) | 2026-10-11 |  |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (pvt bank). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 0 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 4 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| serviceable_cities | Bangalore, Chennai, Delhi, Mumbai, Hyderabad, Gurgaon, Noida, Ghaziabad, Faridabad, Pune, Ahmedabad, Kolkata, Coimbatore, Kochi, Jaipur, Lucknow, Patna, Jamshedpur, Vadodara, Trivandrum, Vishakhapatnam, Bhubaneshwar, Trichy, Surat, Nashik, Aurangabad, Goa, Guwahati, Nagpur, Chandigarh, Bhopal, Calicut, Jodhpur, Mysore, Pondicherry, Raipur, Rajkot, Durgapur, Dehradun, Hubli, Jalandhar, Kolhapur, Ludhiana, Madurai, Mangalore, Patiala, Siliguri, Ranchi, Tirunelveli, Udaipur, Vijaywada, Indore, Ajmer, Allahabad, Bhatinda, Belgaum, Bhavnagar, Bhilwara, Jamnagar, Kanpur, Kota, Salem, Ujjain, Warangal, Mehsana | list | O | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 | 'available only at the below mentioned locations'; 65 cities in Tiers 1-4 |
| foir_lt_50k | 0.4 | ratio | E | [AXIS-P4](https://www.axis.bank.in/loans/personal-loan/eligibility-documentations) | 2026-10-12 | Axis: existing EMIs should not exceed 40% of take-home pay; 40% kept for low incomes, +5 pp per higher income band |
| foir_50k_1l | 0.45 | ratio | E | [AXIS-P4](https://www.axis.bank.in/loans/personal-loan/eligibility-documentations) | 2026-10-12 | Axis: existing EMIs should not exceed 40% of take-home pay; 40% kept for low incomes, +5 pp per higher income band |
| foir_ge_1l | 0.5 | ratio | E | [AXIS-P4](https://www.axis.bank.in/loans/personal-loan/eligibility-documentations) | 2026-10-12 | Axis: existing EMIs should not exceed 40% of take-home pay; 40% kept for low incomes, +5 pp per higher income band |
| max_income_multiple | 15 | x monthly income | O | [AXIS-C1](https://www.axis.bank.in/calculators/personal-loan-eligibility-calculator) | 2026-10-12 | Calculator: 15 x net income at every income tested; its own cap is Rs 15 lakh (product page: up to Rs 50 lakh); it ignores existing EMIs, the model still applies FOIR |
| min_loan_amount | 50000 | INR | O | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 |  |
| max_loan_amount | 5000000 | INR | O | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 | Rs 50,000-50 lakh; the earlier Rs 25 lakh no-relationship cap is no longer stated |
| min_tenure_months | 12 | months | E | [HDFC-A2](https://bankbazaar.com/hdfc-personal-loan-interest-rates.html) | 2026-10-11 | Not published by Axis Bank. pvt bank default, the value HDFC Bank publishes for this rule (linked) |
| max_tenure_months | 84 | months | O | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 |  |
| rate_min_pct | 9.99 | % p.a. | O | [AXIS-P3](https://www.axis.bank.in/loans/personal-loan/interest-rates-charges) | 2026-10-12 |  |
| rate_max_pct | 22.0 | % p.a. | O | [AXIS-P3](https://www.axis.bank.in/loans/personal-loan/interest-rates-charges) | 2026-10-12 |  |
| processing_fee_pct | 0.02 | ratio | O | [AXIS-P3](https://www.axis.bank.in/loans/personal-loan/interest-rates-charges) | 2026-10-12 | Up to 2% + GST |

## Kotak Mahindra Bank (`kotak`, pvt_bank)

32 rules, 15 estimated. Why chosen: Publishes employer-type income floors.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [KOTAK-P1](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/personal-loan-on-30000-salary.html) | 2026-10-11 |  |
| max_age_at_maturity | 60 | years | O | [KOTAK-P1](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/personal-loan-on-30000-salary.html) | 2026-10-11 |  |
| max_age_at_maturity_se | 65 | years | E | [HDFC-A1](https://www.bankbazaar.com/hdfc-personal-loan-eligibility-calculator.html) | 2026-10-11 | Not published by Kotak Mahindra Bank. pvt bank default, the value HDFC Bank publishes for this rule (linked) |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by Kotak Mahindra Bank. pvt bank default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 30000 | INR/month | O | [KOTAK-P3](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | Non-Kotak salary account holders |
| min_income_metro@rel | 25000 | INR/month | O | [KOTAK-P3](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | Kotak salary account holders |
| min_income_non_metro | 30000 | INR/month | O | [KOTAK-P3](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | Non-Kotak salary account holders |
| min_income_non_metro@rel | 25000 | INR/month | O | [KOTAK-P3](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | Kotak salary account holders |
| min_total_exp_months | 12 | months | O | [KOTAK-P3](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 |  |
| min_current_job_months | 6 | months | E | [ABCL-P2](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/loan-of-5-lakh) | 2026-10-11 | Not published by Kotak Mahindra Bank. pvt bank default, the value Aditya Birla Capital publishes for this rule (linked) |
| allowed_employer_categories | psu, mnc, listed, pvt_ltd | list | O | [KOTAK-P3](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | 'Employed with an MNC, public limited company, or private limited company'; PSUs counted as public limited companies; govt departments not listed |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by Kotak Mahindra Bank. pvt bank default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | false | flag | O | [KOTAK-P1](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/personal-loan-on-30000-salary.html) | 2026-10-11 | Must be salaried |
| se_min_vintage_months | 36 | months | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by Kotak Mahindra Bank. pvt bank default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_annual_income | 500000 | INR/year | E | [HDFC-A1](https://www.bankbazaar.com/hdfc-personal-loan-eligibility-calculator.html) | 2026-10-11 | Not published by Kotak Mahindra Bank. pvt bank default, the value HDFC Bank publishes for this rule (linked) |
| min_credit_score | 685 | score | O | [KOTAK-P3](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | 'Cibil Score: 685 or higher' (listed next to an 'Age 21-80*' line that conflicts with the 21-60 stated elsewhere on the page) |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (pvt bank). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 0 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 4 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.5 | ratio | E | [KOTAK-C1](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | No Kotak FOIR published and its calculator applies none (it sizes by 20x income net of EMIs); private-bank default kept so very high EMI loads still bind |
| foir_50k_1l | 0.55 | ratio | E | [KOTAK-C1](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | No Kotak FOIR published and its calculator applies none (it sizes by 20x income net of EMIs); private-bank default kept so very high EMI loads still bind |
| foir_ge_1l | 0.6 | ratio | E | [KOTAK-C1](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | No Kotak FOIR published and its calculator applies none (it sizes by 20x income net of EMIs); private-bank default kept so very high EMI loads still bind |
| max_income_multiple | 20 | x monthly income | O | [KOTAK-C1](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | Calculator: 20 x (income - EMIs); explains the FAQ example (Rs 56,000 -> about Rs 10 lakh) |
| income_multiple_net_of_emi | true | flag | O | [KOTAK-C1](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 |  |
| min_loan_amount | 50000 | INR | E | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 | Not published by Kotak Mahindra Bank. pvt bank default, the value Axis Bank publishes for this rule (linked) |
| max_loan_amount | 10000000 | INR | O | [KOTAK-P3](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | 'up to Rs 1 Crore' |
| min_tenure_months | 12 | months | O | [KOTAK-P2](https://kotak.com/en/personal-banking/loans/personal-loan/personal-loan-for-10-lakhs.html) | 2026-10-11 |  |
| max_tenure_months | 72 | months | O | [KOTAK-P3](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 |  |
| rate_min_pct | 10.99 | % p.a. | O | [KOTAK-P4](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/fees-and-charges.html) | 2026-10-12 |  |
| rate_max_pct | 24.0 | % p.a. | E | [HDFC-P2](https://www.hdfc.bank.in/personal-loan/interest-rates-and-charges) | 2026-10-12 | Not published by Kotak Mahindra Bank. pvt bank default, the value HDFC Bank publishes for this rule (linked) |
| processing_fee_pct | 0.05 | ratio | O | [KOTAK-P4](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/fees-and-charges.html) | 2026-10-12 | Up to 5% + taxes |

## IndusInd Bank (`indusind`, pvt_bank)

30 rules, 10 estimated. Why chosen: Publishes full salaried and self-employed criteria.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 |  |
| max_age_at_maturity | 60 | years | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 |  |
| max_age_at_maturity_se | 65 | years | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 |  |
| se_min_age | 25 | years | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 |  |
| min_income_metro | 25000 | INR/month | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 |  |
| min_income_non_metro | 25000 | INR/month | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 |  |
| min_total_exp_months | 24 | months | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 |  |
| min_current_job_months | 12 | months | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 |  |
| allowed_employer_categories | any | list | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | IndusInd Bank's eligibility page (linked) lists no employer restriction, read as any. Lender-type default (pvt bank) |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by IndusInd Bank. pvt bank default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | true | flag | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 |  |
| se_min_vintage_months | 48 | months | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | 4 years post-qualification (professionals); 5 years for other self-employed |
| se_min_annual_income | 480000 | INR/year | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Annual net income post tax |
| min_credit_score | 730 | score | A | [INDUSIND-A1](https://www.paisabazaar.com/indusind-bank/5-lakh-personal-loan-pvamt) | 2026-10-11 |  |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (pvt bank). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 0 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 4 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.5 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by IndusInd Bank. Banks: HDFC FOIR blog (40-55%) and benchmark calculator CALC-B1 (50%); NBFCs +5pp (higher risk appetite); fintech flat 50% (low-income book) |
| foir_50k_1l | 0.55 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by IndusInd Bank. Banded FOIR: lenders allow a larger share of income as income rises (more residual income after expenses); base level from HDFC's FOIR article (40-55%, linked) |
| foir_ge_1l | 0.6 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by IndusInd Bank. Banded FOIR for high earners; base level from HDFC's FOIR article (40-55%, linked) |
| max_income_multiple | 24 | x monthly income | E | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 | Not published by IndusInd Bank. 24x is the multiple PNB publishes (linked); SBI publishes 30x and the calculators read show 10-20x, so 24x sits mid-range; rarely binds before FOIR |
| min_loan_amount | 30000 | INR | A | [INDUSIND-A2](https://www.bankbazaar.com/indusind-personal-loan-interest-rates.html) | 2026-10-11 |  |
| max_loan_amount | 500000 | INR | A | [INDUSIND-A2](https://www.bankbazaar.com/indusind-personal-loan-interest-rates.html) | 2026-10-11 | Online/instant product cap |
| min_tenure_months | 12 | months | A | [INDUSIND-A2](https://www.bankbazaar.com/indusind-personal-loan-interest-rates.html) | 2026-10-11 |  |
| max_tenure_months | 48 | months | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 |  |
| rate_min_pct | 12.0 | % p.a. | O | [INDUSIND-P2](https://www.indusind.bank.in/in/en/personal/rates.html) | 2026-10-12 | Rates offered Apr-Jun 2026, Personal Loan (Insta Funding) |
| rate_max_pct | 15.0 | % p.a. | O | [INDUSIND-P2](https://www.indusind.bank.in/in/en/personal/rates.html) | 2026-10-12 |  |
| processing_fee_pct | 0.02 | ratio | O | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | 2% processing fee (limited period offer) |
| rate_avg_pct | 12.8 | % p.a. | O | [INDUSIND-P2](https://www.indusind.bank.in/in/en/personal/rates.html) | 2026-10-12 |  |

## IDFC FIRST Bank (`idfc`, pvt_bank)

30 rules, 16 estimated. Why chosen: Retail-first bank with public eligibility calculator.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [IDFC-P4](https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 |  |
| max_age_at_maturity | 60 | years | O | [IDFC-P4](https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 |  |
| max_age_at_maturity_se | 60 | years | O | [IDFC-P1](https://www.idfcfirst.bank.in/finfirst-blogs/personal-loan/personal-loan-eligibility-criteria) | 2026-10-11 |  |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by IDFC FIRST Bank. pvt bank default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 20000 | INR/month | O | [IDFC-P3](https://www.idfcfirst.bank.in/finfirst-blogs/personal-loan/minimum-salary-required-for-personal-loan) | 2026-10-11 | Older blog Rs 20k Mumbai/Delhi; FIRSTmoney Rs 10k |
| min_income_non_metro | 15000 | INR/month | O | [IDFC-P3](https://www.idfcfirst.bank.in/finfirst-blogs/personal-loan/minimum-salary-required-for-personal-loan) | 2026-10-11 |  |
| min_total_exp_months | 12 | months | E | [KOTAK-P3](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | Not published by IDFC FIRST Bank. pvt bank default, the value Kotak Mahindra Bank publishes for this rule (linked) |
| min_current_job_months | 6 | months | E | [ABCL-P2](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/loan-of-5-lakh) | 2026-10-11 | Not published by IDFC FIRST Bank. pvt bank default, the value Aditya Birla Capital publishes for this rule (linked) |
| allowed_employer_categories | any | list | E | [IDFC-P4](https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 | IDFC FIRST Bank's eligibility page (linked) lists no employer restriction, read as any. Lender-type default (pvt bank) |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by IDFC FIRST Bank. pvt bank default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | true | flag | O | [IDFC-P4](https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 |  |
| se_min_vintage_months | 36 | months | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by IDFC FIRST Bank. pvt bank default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_annual_income | 500000 | INR/year | E | [HDFC-A1](https://www.bankbazaar.com/hdfc-personal-loan-eligibility-calculator.html) | 2026-10-11 | Not published by IDFC FIRST Bank. pvt bank default, the value HDFC Bank publishes for this rule (linked) |
| min_credit_score | 710 | score | O | [IDFC-P4](https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 |  |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (pvt bank). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 0 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 4 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.5 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by IDFC FIRST Bank. Banks: HDFC FOIR blog (40-55%) and benchmark calculator CALC-B1 (50%); NBFCs +5pp (higher risk appetite); fintech flat 50% (low-income book) |
| foir_50k_1l | 0.55 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by IDFC FIRST Bank. Banded FOIR: lenders allow a larger share of income as income rises (more residual income after expenses); base level from HDFC's FOIR article (40-55%, linked) |
| foir_ge_1l | 0.6 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by IDFC FIRST Bank. Banded FOIR for high earners; base level from HDFC's FOIR article (40-55%, linked) |
| max_income_multiple | 10 | x monthly income | O | [IDFC-C1](https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan/personal-loan-eligibility-calculator) | 2026-10-12 | Calculator: 10 x (income - EMIs), capped at Rs 15 lakh |
| income_multiple_net_of_emi | true | flag | O | [IDFC-C1](https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan/personal-loan-eligibility-calculator) | 2026-10-12 |  |
| min_loan_amount | 50000 | INR | E | [AXIS-P1](https://www.axis.bank.in/retail/loans/personal-loan) | 2026-10-12 | Not published by IDFC FIRST Bank. pvt bank default, the value Axis Bank publishes for this rule (linked) |
| max_loan_amount | 1500000 | INR | O | [IDFC-P4](https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 |  |
| min_tenure_months | 9 | months | O | [IDFC-P4](https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 |  |
| max_tenure_months | 60 | months | O | [IDFC-P4](https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 |  |
| rate_min_pct | 9.99 | % p.a. | O | [IDFC-P4](https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 |  |
| rate_max_pct | 24.0 | % p.a. | E | [HDFC-P2](https://www.hdfc.bank.in/personal-loan/interest-rates-and-charges) | 2026-10-12 | Not published by IDFC FIRST Bank. pvt bank default, the value HDFC Bank publishes for this rule (linked) |
| processing_fee_pct | 0.0297 | ratio | O | [IDFC-P4](https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan) | 2026-10-12 | 0%-3.5% including GST = up to 2.97% + GST |

## YES BANK (`yes`, pvt_bank)

29 rules, 17 estimated. Why chosen: Adds a mid-size private bank; large ticket (Rs 40 lakh).

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 22 | years | A | [YES-A2](https://www.wishfin.com/yes-bank-personal-loan-hyderabad-436/) | 2026-10-11 | 2020 page |
| max_age_at_maturity | 58 | years | A | [YES-A2](https://www.wishfin.com/yes-bank-personal-loan-hyderabad-436/) | 2026-10-11 | 2020 page |
| max_age_at_maturity_se | 65 | years | E | [HDFC-A1](https://www.bankbazaar.com/hdfc-personal-loan-eligibility-calculator.html) | 2026-10-11 | Not published by YES BANK. pvt bank default, the value HDFC Bank publishes for this rule (linked) |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by YES BANK. pvt bank default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 25000 | INR/month | A | [YES-A2](https://www.wishfin.com/yes-bank-personal-loan-hyderabad-436/) | 2026-10-11 | 2020 page |
| min_income_non_metro | 25000 | INR/month | A | [YES-A2](https://www.wishfin.com/yes-bank-personal-loan-hyderabad-436/) | 2026-10-11 |  |
| min_total_exp_months | 12 | months | E | [KOTAK-P3](https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html) | 2026-10-12 | Not published by YES BANK. pvt bank default, the value Kotak Mahindra Bank publishes for this rule (linked) |
| min_current_job_months | 6 | months | E | [ABCL-P2](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/loan-of-5-lakh) | 2026-10-11 | Not published by YES BANK. pvt bank default, the value Aditya Birla Capital publishes for this rule (linked) |
| allowed_employer_categories | any | list | E | [YES-P1](https://www.yes.bank.in/personal-banking/yes-individual/loans/personal-loan) | 2026-10-12 | YES BANK's eligibility page (linked) lists no employer restriction, read as any. Lender-type default (pvt bank) |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by YES BANK. pvt bank default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | true | flag | E | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | Not published by YES BANK. pvt bank default, the value ICICI Bank publishes for this rule (linked) |
| se_min_vintage_months | 36 | months | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by YES BANK. pvt bank default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_annual_income | 500000 | INR/year | E | [HDFC-A1](https://www.bankbazaar.com/hdfc-personal-loan-eligibility-calculator.html) | 2026-10-11 | Not published by YES BANK. pvt bank default, the value HDFC Bank publishes for this rule (linked) |
| min_credit_score | 700 | score | A | [YES-A1](https://www.bankbazaar.com/yes-bank-personal-loan-eligibility-calculator.html) | 2026-10-11 |  |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (pvt bank). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 0 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 4 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.5 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by YES BANK. Banks: HDFC FOIR blog (40-55%) and benchmark calculator CALC-B1 (50%); NBFCs +5pp (higher risk appetite); fintech flat 50% (low-income book) |
| foir_50k_1l | 0.55 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by YES BANK. Banded FOIR: lenders allow a larger share of income as income rises (more residual income after expenses); base level from HDFC's FOIR article (40-55%, linked) |
| foir_ge_1l | 0.6 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by YES BANK. Banded FOIR for high earners; base level from HDFC's FOIR article (40-55%, linked) |
| max_income_multiple | 24 | x monthly income | E | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 | Not published by YES BANK. 24x is the multiple PNB publishes (linked); SBI publishes 30x and the calculators read show 10-20x, so 24x sits mid-range; rarely binds before FOIR |
| min_loan_amount | 50000 | INR | O | [YES-P1](https://www.yes.bank.in/personal-banking/yes-individual/loans/personal-loan) | 2026-10-12 |  |
| max_loan_amount | 5000000 | INR | O | [YES-P1](https://www.yes.bank.in/personal-banking/yes-individual/loans/personal-loan) | 2026-10-12 |  |
| min_tenure_months | 12 | months | A | [YES-A1](https://www.bankbazaar.com/yes-bank-personal-loan-eligibility-calculator.html) | 2026-10-11 |  |
| max_tenure_months | 60 | months | A | [YES-A1](https://www.bankbazaar.com/yes-bank-personal-loan-eligibility-calculator.html) | 2026-10-11 |  |
| rate_min_pct | 10.85 | % p.a. | O | [YES-P1](https://www.yes.bank.in/personal-banking/yes-individual/loans/personal-loan) | 2026-10-12 |  |
| rate_max_pct | 20.25 | % p.a. | A | [YES-A2](https://www.wishfin.com/yes-bank-personal-loan-hyderabad-436/) | 2026-10-11 |  |
| processing_fee_pct | 0.025 | ratio | O | [YES-P2](https://www.yes.bank.in/sites/web/content/published/api/v1.1/assets/CONT383F22014BE04AB08FFB6E1E7C84E714/native/personalloan_pdf.pdf?download=false) | 2026-10-12 |  |

## Bajaj Finance (`bajaj`, nbfc)

29 rules, 13 estimated. Why chosen: Largest NBFC personal-loan lender.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [BAJAJ-P1](https://www.bajajfinserv.in/personal-loan-of-10-lakh-for-6-years) | 2026-10-11 |  |
| max_age_at_maturity | 80 | years | O | [BAJAJ-P1](https://www.bajajfinserv.in/personal-loan-of-10-lakh-for-6-years) | 2026-10-11 | At end of tenure |
| max_age_at_maturity_se | 65 | years | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by Bajaj Finance. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by Bajaj Finance. nbfc default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 35000 | INR/month | E | [BAJAJ-P1](https://www.bajajfinserv.in/personal-loan-of-10-lakh-for-6-years) | 2026-10-11 | Page says floor rises by city; metro estimated at Rs 35,000 |
| min_income_non_metro | 25001 | INR/month | O | [BAJAJ-P1](https://www.bajajfinserv.in/personal-loan-of-10-lakh-for-6-years) | 2026-10-11 | 'Starting Rs 25,001 based on city' |
| min_total_exp_months | 12 | months | E | [ABCL-P2](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/loan-of-5-lakh) | 2026-10-11 | Not published by Bajaj Finance. nbfc default, the value Aditya Birla Capital publishes for this rule (linked) |
| min_current_job_months | 3 | months | E | [BAJAJ-P4](https://www.bajajfinserv.in/personal-loan) | 2026-10-12 | Bajaj Finance's eligibility page (linked) is silent on this rule. Lender-type default (nbfc) |
| allowed_employer_categories | govt, psu, mnc, listed, pvt_ltd | list | O | [BAJAJ-P4](https://www.bajajfinserv.in/personal-loan) | 2026-10-12 | 'Employed with: Public, private, or MNC' |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by Bajaj Finance. nbfc default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | true | flag | O | [BAJAJ-P4](https://www.bajajfinserv.in/personal-loan) | 2026-10-12 | 'Customer profile: Self-employed or Salaried' |
| se_min_vintage_months | 36 | months | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by Bajaj Finance. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_annual_income | 300000 | INR/year | E | [BAJAJ-P4](https://www.bajajfinserv.in/personal-loan) | 2026-10-12 | Bajaj Finance's eligibility page (linked) is silent on this rule. Lender-type default (nbfc) |
| min_credit_score | 650 | score | O | [BAJAJ-P4](https://www.bajajfinserv.in/personal-loan) | 2026-10-12 |  |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (nbfc). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 30 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 6 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.75 | ratio | O | [BAJAJ-C1](https://www.bajajfinserv.in/personal-loan-eligibility-calculator) | 2026-10-12 | Calculator code: (75% - expenses/income) x income is the EMI room, at every income |
| foir_50k_1l | 0.75 | ratio | O | [BAJAJ-C1](https://www.bajajfinserv.in/personal-loan-eligibility-calculator) | 2026-10-12 | Calculator code: (75% - expenses/income) x income is the EMI room, at every income |
| foir_ge_1l | 0.75 | ratio | O | [BAJAJ-C1](https://www.bajajfinserv.in/personal-loan-eligibility-calculator) | 2026-10-12 | Calculator code: (75% - expenses/income) x income is the EMI room, at every income |
| max_income_multiple | 10 | x monthly income | O | [BAJAJ-C1](https://www.bajajfinserv.in/personal-loan-eligibility-calculator) | 2026-10-12 | Calculator code: capped at 10x monthly income |
| min_loan_amount | 40000 | INR | O | [BAJAJ-P4](https://www.bajajfinserv.in/personal-loan) | 2026-10-12 |  |
| max_loan_amount | 5500000 | INR | O | [BAJAJ-P4](https://www.bajajfinserv.in/personal-loan) | 2026-10-12 |  |
| min_tenure_months | 12 | months | E | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | Not published by Bajaj Finance. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| max_tenure_months | 108 | months | O | [BAJAJ-P4](https://www.bajajfinserv.in/personal-loan) | 2026-10-12 | 'The maximum personal loan tenure you can apply for is 108 months' |
| rate_min_pct | 10.0 | % p.a. | O | [BAJAJ-P4](https://www.bajajfinserv.in/personal-loan) | 2026-10-12 |  |
| rate_max_pct | 30.5 | % p.a. | O | [BAJAJ-P4](https://www.bajajfinserv.in/personal-loan) | 2026-10-12 |  |
| processing_fee_pct | 0.035 | ratio | O | [BAJAJ-P4](https://www.bajajfinserv.in/personal-loan) | 2026-10-12 | Up to 4.13% including taxes = 3.5% + GST |

## Tata Capital (`tata`, nbfc)

29 rules, 12 estimated. Why chosen: Large NBFC; low income floor (Rs 15k).

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [TATA-P1](https://www.tatacapital.com/personal-loan/3-lakhs-personal-loan.html) | 2026-10-11 |  |
| max_age_at_maturity | 58 | years | O | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 |  |
| max_age_at_maturity_se | 65 | years | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by Tata Capital. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by Tata Capital. nbfc default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 20000 | INR/month | O | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 |  |
| min_income_non_metro | 20000 | INR/month | O | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 |  |
| min_total_exp_months | 24 | months | O | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 |  |
| min_current_job_months | 12 | months | O | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 |  |
| allowed_employer_categories | any | list | E | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 | Tata Capital's eligibility page (linked) lists no employer restriction, read as any. Lender-type default (nbfc) |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by Tata Capital. nbfc default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | true | flag | A | [TATA-A1](https://bankbazaar.com/tata-capital-personal-loan-eligibility-calculator.html) | 2026-10-11 |  |
| se_min_vintage_months | 36 | months | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by Tata Capital. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_annual_income | 300000 | INR/year | E | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 | Tata Capital's eligibility page (linked) is silent on this rule. Lender-type default (nbfc) |
| se_min_credit_score | 750 | score | A | [TATA-A1](https://bankbazaar.com/tata-capital-personal-loan-eligibility-calculator.html) | 2026-10-11 | 750+ preferred for SE |
| min_credit_score | 725 | score | O | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 | '725+ preferred' |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (nbfc). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 30 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 6 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_bands | 25000:0.5, 50000:0.6, 75000:0.65, *:0.75 | income:ratio list | O | [TATA-C1](https://www.tatacapital.com/personal-loan/eligibility-calculator.html) | 2026-10-12 | Calculator code: 50% to Rs 25,000, 60% to 50,000, 65% to 75,000, 75% above (existing EMIs inside FOIR) |
| income_multiple_by_tenure | 12:6/7/7, 24:10/13/13, 36:14/18/18, 48:17/22/23, *:20/23/27 | tenure months:x income list | O | [TATA-C1](https://www.tatacapital.com/personal-loan/eligibility-calculator.html) | 2026-10-12 | Calculator code, 'cat a' employers (the model has no Tata employer list): x income by tenure and income band; the calculator stops at 60 months, so 61-72 months reuse the 60-month row |
| income_multiple_income_bands | 49999, 75000 | income list | O | [TATA-C1](https://www.tatacapital.com/personal-loan/eligibility-calculator.html) | 2026-10-12 | Calculator income bands: <50k / 50-75k / >75k |
| min_loan_amount | 40000 | INR | O | [TATA-P2](https://tatacapital.com/personal-loan/personal-loan-in-hyderabad.html) | 2026-10-11 |  |
| max_loan_amount | 3500000 | INR | O | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 |  |
| min_tenure_months | 12 | months | E | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | Not published by Tata Capital. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| max_tenure_months | 72 | months | O | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 |  |
| rate_min_pct | 10.99 | % p.a. | O | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 |  |
| rate_max_pct | 26.0 | % p.a. | E | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 | Tata Capital's eligibility page (linked) is silent on this rule. Upper end not published; set to typical rack-rate ceiling for this lender type |
| processing_fee_pct | 0.05 | ratio | O | [TATA-P3](https://www.tatacapital.com/personal-loan.html) | 2026-10-12 | Up to 5% + GST |

## Aditya Birla Capital (`abcl`, nbfc)

28 rules, 13 estimated. Why chosen: Large NBFC; strict published score cut-off (750).

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [ABCL-P4](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/eligibility-criteria) | 2026-10-12 | 21 or 23 depending on loan type |
| max_age_at_maturity | 60 | years | O | [ABCL-P4](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/eligibility-criteria) | 2026-10-12 | Extendable to 62 for some loan types |
| max_age_at_maturity_se | 65 | years | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by Aditya Birla Capital. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by Aditya Birla Capital. nbfc default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 20000 | INR/month | O | [ABCL-P3](https://www.adityabirlacapital.com/abc-of-money/things-that-affect-your-personal-loan-eligibility) | 2026-10-11 | Educational page |
| min_income_non_metro | 15000 | INR/month | O | [ABCL-P3](https://www.adityabirlacapital.com/abc-of-money/things-that-affect-your-personal-loan-eligibility) | 2026-10-11 |  |
| min_total_exp_months | 12 | months | O | [ABCL-P2](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/loan-of-5-lakh) | 2026-10-11 |  |
| min_current_job_months | 6 | months | O | [ABCL-P2](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/loan-of-5-lakh) | 2026-10-11 |  |
| allowed_employer_categories | any | list | E | [ABCL-P4](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/eligibility-criteria) | 2026-10-12 | Aditya Birla Capital's eligibility page (linked) lists no employer restriction, read as any. Lender-type default (nbfc) |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by Aditya Birla Capital. nbfc default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | false | flag | O | [ABCL-P1](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan) | 2026-10-11 | Eligibility shown for salaried |
| se_min_vintage_months | 36 | months | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by Aditya Birla Capital. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_annual_income | 300000 | INR/year | E | [ABCL-P4](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/eligibility-criteria) | 2026-10-12 | Aditya Birla Capital's eligibility page (linked) is silent on this rule. Lender-type default (nbfc) |
| min_credit_score | 700 | score | O | [ABCL-P4](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/eligibility-criteria) | 2026-10-12 | Eligibility page: 700+; the Rs 5 lakh product page says 750+ |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (nbfc). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 30 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 6 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| income_multiple_net_of_emi | true | flag | O | [ABCL-C1](https://www.adityabirlacapital.com/abc-of-calculators/personal-loan-eligibility-calculator) | 2026-10-12 | Calculator: multiple applies to income minus existing EMIs |
| foir_bands | 74999:0.65, 149999:0.7, *:0.75 | income:ratio list | O | [ABCL-C1](https://www.adityabirlacapital.com/abc-of-calculators/personal-loan-eligibility-calculator) | 2026-10-12 | Calculator: 65% below Rs 75,000, 70% below 1.5 lakh, 75% above |
| income_multiple_by_tenure | 12:4, 24:8, 36:11, 48:14, 60:17, 72:20, *:23 | tenure months:x income list | O | [ABCL-C1](https://www.adityabirlacapital.com/abc-of-calculators/personal-loan-eligibility-calculator) | 2026-10-12 | Calculator: 4x for 1 year up to 23x for 7 years |
| min_loan_amount | 50000 | INR | O | [ABCL-P1](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan) | 2026-10-11 |  |
| max_loan_amount | 5000000 | INR | O | [ABCL-C1](https://www.adityabirlacapital.com/abc-of-calculators/personal-loan-eligibility-calculator) | 2026-10-12 | Calculator cap Rs 50 lakh (was a lender-type estimate of Rs 40 lakh) |
| min_tenure_months | 12 | months | E | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | Not published by Aditya Birla Capital. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| max_tenure_months | 84 | months | O | [ABCL-P4](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/eligibility-criteria) | 2026-10-12 | Tenure 1-7 years |
| rate_min_pct | 13.0 | % p.a. | E | [ABCL-P1](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan) | 2026-10-11 | Reference rates 19.45-20.45% (Mar 2024) are old; band set around them |
| rate_max_pct | 28.0 | % p.a. | E | [ABCL-P1](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan) | 2026-10-11 | As above |
| processing_fee_pct | 0.04 | ratio | O | [ABCL-P1](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan) | 2026-10-11 |  |

## HDB Financial Services (`hdb`, nbfc)

30 rules, 12 estimated. Why chosen: Serves lower-income and tier-2/3 borrowers.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | A | [HDB-A1](https://bankbazaar.com/hdbfs-personal-loan.html) | 2026-10-11 |  |
| max_age_at_maturity | 60 | years | O | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | Or retirement, whichever is earlier |
| max_age_at_maturity@govt | 65 | years | O | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | Government employees (conditions apply) |
| max_age_at_maturity_se | 65 | years | O | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 |  |
| se_min_age | 22 | years | O | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 |  |
| min_income_metro | 20000 | INR/month | O | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | Ahmedabad, Bangalore, Chennai, Delhi, Hyderabad, Kolkata, Mumbai, Pune |
| min_income_non_metro | 15000 | INR/month | O | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 |  |
| min_total_exp_months | 12 | months | O | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | 1-2 years depending on organisation category |
| min_current_job_months | 1 | months | O | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | Minimum 1 month salary credit in current organisation |
| allowed_employer_categories | any | list | E | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | HDB Financial Services's eligibility page (linked) lists no employer restriction, read as any. Lender-type default (nbfc) |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by HDB Financial Services. nbfc default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | true | flag | A | [HDB-A1](https://bankbazaar.com/hdbfs-personal-loan.html) | 2026-10-11 |  |
| se_min_vintage_months | 36 | months | O | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Professionals 3 years; other self-employed 4 years |
| se_min_annual_income | 100000 | INR/year | A | [HDB-A1](https://bankbazaar.com/hdbfs-personal-loan.html) | 2026-10-11 | As published (metro) |
| min_credit_score | 700 | score | E | [ABCL-P4](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/eligibility-criteria) | 2026-10-12 | Not published by HDB Financial Services. nbfc default, the value Aditya Birla Capital publishes for this rule (linked) |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (nbfc). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 30 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 6 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.55 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by HDB Financial Services. Banks: HDFC FOIR blog (40-55%) and benchmark calculator CALC-B1 (50%); NBFCs +5pp (higher risk appetite); fintech flat 50% (low-income book) |
| foir_50k_1l | 0.6 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by HDB Financial Services. Banded FOIR: lenders allow a larger share of income as income rises (more residual income after expenses); base level from HDFC's FOIR article (40-55%, linked) |
| foir_ge_1l | 0.65 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by HDB Financial Services. Banded FOIR for high earners; base level from HDFC's FOIR article (40-55%, linked) |
| max_income_multiple | 24 | x monthly income | E | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 | Not published by HDB Financial Services. 24x is the multiple PNB publishes (linked); SBI publishes 30x and the calculators read show 10-20x, so 24x sits mid-range; rarely binds before FOIR |
| min_loan_amount | 50000 | INR | E | [ABCL-P1](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan) | 2026-10-11 | Not published by HDB Financial Services. nbfc default, the value Aditya Birla Capital publishes for this rule (linked) |
| max_loan_amount | 1000000 | INR | O | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | Salaried PL up to Rs 10 lakh (PL overall up to Rs 20 lakh) |
| min_tenure_months | 12 | months | O | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 |  |
| max_tenure_months | 60 | months | O | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 |  |
| rate_min_pct | 10.0 | % p.a. | A | [HDB-A2](https://paisabazaar.com/hdb/personal-loan) | 2026-10-11 |  |
| rate_max_pct | 36.0 | % p.a. | A | [HDB-A2](https://paisabazaar.com/hdb/personal-loan) | 2026-10-11 |  |
| processing_fee_pct | 0.03 | ratio | A | [HDB-A2](https://paisabazaar.com/hdb/personal-loan) | 2026-10-11 |  |

## Poonawalla Fincorp (`poonawalla`, nbfc)

28 rules, 12 estimated. Why chosen: Published employer-type restrictions.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [POONAWALLA-P2](https://poonawallafincorp.com/personal-loan/personal-loan-in-gujarat) | 2026-10-11 |  |
| max_age_at_maturity | 60 | years | O | [POONAWALLA-P5](https://poonawallafincorp.com/personal-loan/eligibility-and-documents) | 2026-10-12 |  |
| max_age_at_maturity_se | 65 | years | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by Poonawalla Fincorp. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by Poonawalla Fincorp. nbfc default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 30000 | INR/month | O | [POONAWALLA-P1](https://poonawallafincorp.com/personal-loan-for-salaried-employees.php) | 2026-10-11 |  |
| min_income_non_metro | 30000 | INR/month | O | [POONAWALLA-P1](https://poonawallafincorp.com/personal-loan-for-salaried-employees.php) | 2026-10-11 |  |
| min_total_exp_months | 12 | months | O | [POONAWALLA-P5](https://poonawallafincorp.com/personal-loan/eligibility-and-documents) | 2026-10-12 |  |
| min_current_job_months | 1 | months | O | [POONAWALLA-P5](https://poonawallafincorp.com/personal-loan/eligibility-and-documents) | 2026-10-12 |  |
| allowed_employer_categories | govt, psu, mnc, listed, pvt_ltd, llp | list | O | [POONAWALLA-P1](https://poonawallafincorp.com/personal-loan-for-salaried-employees.php) | 2026-10-11 |  |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by Poonawalla Fincorp. nbfc default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | false | flag | O | [POONAWALLA-P1](https://poonawallafincorp.com/personal-loan-for-salaried-employees.php) | 2026-10-11 | Salaried product |
| se_min_vintage_months | 36 | months | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by Poonawalla Fincorp. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_annual_income | 300000 | INR/year | E | [POONAWALLA-P5](https://poonawallafincorp.com/personal-loan/eligibility-and-documents) | 2026-10-12 | Poonawalla Fincorp's eligibility page (linked) is silent on this rule. Lender-type default (nbfc) |
| min_credit_score | 700 | score | O | [POONAWALLA-P5](https://poonawallafincorp.com/personal-loan/eligibility-and-documents) | 2026-10-12 |  |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (nbfc). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 30 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 6 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.55 | ratio | O | [POONAWALLA-C1](https://poonawallafincorp.com/personal-loan/eligibility-calculator) | 2026-10-12 | Calculator: 55% at Rs 30,000-50,000 (EMIs subtracted inside FOIR) |
| foir_50k_1l | 0.65 | ratio | O | [POONAWALLA-C1](https://poonawallafincorp.com/personal-loan/eligibility-calculator) | 2026-10-12 | Calculator: 65% from Rs 55,000 |
| foir_ge_1l | 0.65 | ratio | O | [POONAWALLA-C1](https://poonawallafincorp.com/personal-loan/eligibility-calculator) | 2026-10-12 | Calculator: 65% at Rs 1 lakh; above that its own Rs 20 lakh cap binds |
| min_loan_amount | 50000 | INR | E | [ABCL-P1](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan) | 2026-10-11 | Not published by Poonawalla Fincorp. nbfc default, the value Aditya Birla Capital publishes for this rule (linked) |
| max_loan_amount | 1500000 | INR | O | [POONAWALLA-P4](https://poonawallafincorp.com/personal-loan/prime-personal-loan-for-salaried-employees) | 2026-10-12 |  |
| min_tenure_months | 12 | months | E | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | Not published by Poonawalla Fincorp. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| max_tenure_months | 84 | months | O | [POONAWALLA-P4](https://poonawallafincorp.com/personal-loan/prime-personal-loan-for-salaried-employees) | 2026-10-12 |  |
| rate_min_pct | 9.99 | % p.a. | O | [POONAWALLA-P4](https://poonawallafincorp.com/personal-loan/prime-personal-loan-for-salaried-employees) | 2026-10-12 |  |
| rate_max_pct | 26.0 | % p.a. | E | [POONAWALLA-P5](https://poonawallafincorp.com/personal-loan/eligibility-and-documents) | 2026-10-12 | Poonawalla Fincorp's eligibility page (linked) is silent on this rule. Upper end not published; set to typical rack-rate ceiling for this lender type |
| processing_fee_pct | 0.04 | ratio | O | [POONAWALLA-P4](https://poonawallafincorp.com/personal-loan/prime-personal-loan-for-salaried-employees) | 2026-10-12 | Up to 4% + taxes |

## L&T Finance (`lt`, nbfc)

29 rules, 20 estimated. Why chosen: Large NBFC; income judged on net disposable income.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [LT-P1](https://www.ltfinance.com/personal-loan) | 2026-10-12 |  |
| max_age_at_maturity | 58 | years | O | [LT-P1](https://www.ltfinance.com/personal-loan) | 2026-10-12 |  |
| max_age_at_maturity_se | 65 | years | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by L&T Finance. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_age | 25 | years | E | [INDUSIND-P1](https://www.indusind.bank.in/in/en/personal/loans/personal-loan.html) | 2026-10-12 | Not published by L&T Finance. nbfc default, the value IndusInd Bank publishes for this rule (linked) |
| min_income_metro | 25000 | INR/month | O | [LT-P2](https://www.ltfinance.com/blog/personal-loan/personal-loan-for-salaried-employees) | 2026-10-11 | Tier-1 cities |
| min_income_non_metro | 15000 | INR/month | E | [LT-P1](https://www.ltfinance.com/personal-loan) | 2026-10-12 | 'No fixed minimum'; Rs 15,000 assumed outside tier-1 |
| min_total_exp_months | 12 | months | E | [ABCL-P2](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/loan-of-5-lakh) | 2026-10-11 | Not published by L&T Finance. nbfc default, the value Aditya Birla Capital publishes for this rule (linked) |
| min_current_job_months | 3 | months | E | [LT-P1](https://www.ltfinance.com/personal-loan) | 2026-10-12 | L&T Finance's eligibility page (linked) is silent on this rule. Lender-type default (nbfc) |
| allowed_employer_categories | any | list | E | [LT-P1](https://www.ltfinance.com/personal-loan) | 2026-10-12 | L&T Finance's eligibility page (linked) lists no employer restriction, read as any. Lender-type default (nbfc) |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by L&T Finance. nbfc default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | true | flag | O | [LT-P1](https://www.ltfinance.com/personal-loan) | 2026-10-12 | Business owners, freelancers and self-employed professionals |
| se_min_vintage_months | 36 | months | E | [HDB-P2](https://www.hdbfs.com/personal-loan) | 2026-10-12 | Not published by L&T Finance. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| se_min_annual_income | 300000 | INR/year | E | [LT-P1](https://www.ltfinance.com/personal-loan) | 2026-10-12 | L&T Finance's eligibility page (linked) is silent on this rule. Lender-type default (nbfc) |
| min_credit_score | 700 | score | E | [ABCL-P4](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan/eligibility-criteria) | 2026-10-12 | Not published by L&T Finance. nbfc default, the value Aditya Birla Capital publishes for this rule (linked) |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (nbfc). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 30 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 6 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.5 | ratio | E | [LT-P4](https://www.ltfinance.com/personal-loan-eligibility-calculator) | 2026-10-12 | L&T's eligibility page: most lenders cap FOIR at 50%-55%, its worked example uses 50% |
| foir_50k_1l | 0.5 | ratio | E | [LT-P4](https://www.ltfinance.com/personal-loan-eligibility-calculator) | 2026-10-12 | L&T's eligibility page: most lenders cap FOIR at 50%-55%, its worked example uses 50% |
| foir_ge_1l | 0.55 | ratio | E | [LT-P4](https://www.ltfinance.com/personal-loan-eligibility-calculator) | 2026-10-12 | L&T's eligibility page: most lenders cap FOIR at 50%-55%, its worked example uses 50% |
| max_income_multiple | 24 | x monthly income | E | [PNB-P1](https://www.pnb.bank.in/personalloanforpublic.html) | 2026-10-12 | Not published by L&T Finance. 24x is the multiple PNB publishes (linked); SBI publishes 30x and the calculators read show 10-20x, so 24x sits mid-range; rarely binds before FOIR |
| min_loan_amount | 50000 | INR | E | [ABCL-P1](https://www.adityabirlacapital.com/loans/personal-finance/personal-loan) | 2026-10-11 | Not published by L&T Finance. nbfc default, the value Aditya Birla Capital publishes for this rule (linked) |
| max_loan_amount | 3000000 | INR | O | [LT-P1](https://www.ltfinance.com/personal-loan) | 2026-10-12 |  |
| min_tenure_months | 12 | months | E | [HDB-P1](https://www.hdbfs.com/products/salaried-loan) | 2026-10-12 | Not published by L&T Finance. nbfc default, the value HDB Financial Services publishes for this rule (linked) |
| max_tenure_months | 72 | months | O | [LT-P1](https://www.ltfinance.com/personal-loan) | 2026-10-12 |  |
| rate_min_pct | 10.5 | % p.a. | O | [LT-P1](https://www.ltfinance.com/personal-loan) | 2026-10-12 |  |
| rate_max_pct | 27.0 | % p.a. | A | [LT-A1](https://paisabazaar.com/personal-loan/l-t-finance) | 2026-10-11 |  |
| processing_fee_pct | 0.04 | ratio | O | [LT-P1](https://www.ltfinance.com/personal-loan) | 2026-10-12 |  |

## Moneyview (`moneyview`, fintech)

29 rules, 16 estimated. Why chosen: Large digital PL platform; accepts low/thin scores.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | O | [MONEYVIEW-P1](https://moneyview.in/personal-loan-eligibility-check) | 2026-10-12 |  |
| max_age_at_maturity | 57 | years | O | [MONEYVIEW-P3](https://moneyview.in/personal-loan) | 2026-10-12 |  |
| max_age_at_maturity_se | 57 | years | O | [MONEYVIEW-P1](https://moneyview.in/personal-loan-eligibility-check) | 2026-10-12 |  |
| se_min_age | 23 | years | E | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | Not published by Moneyview. fintech default, the value ICICI Bank publishes for this rule (linked) |
| min_income_metro | 25000 | INR/month | O | [MONEYVIEW-P1](https://moneyview.in/personal-loan-eligibility-check) | 2026-10-12 |  |
| min_income_non_metro | 25000 | INR/month | O | [MONEYVIEW-P1](https://moneyview.in/personal-loan-eligibility-check) | 2026-10-12 |  |
| min_total_exp_months | 6 | months | E | [MONEYVIEW-P3](https://moneyview.in/personal-loan) | 2026-10-12 | Moneyview's eligibility page (linked) is silent on this rule. Lender-type default (fintech) |
| min_current_job_months | 3 | months | E | [MONEYVIEW-P3](https://moneyview.in/personal-loan) | 2026-10-12 | Moneyview's eligibility page (linked) is silent on this rule. Lender-type default (fintech) |
| allowed_employer_categories | any | list | E | [MONEYVIEW-P3](https://moneyview.in/personal-loan) | 2026-10-12 | Moneyview's eligibility page (linked) lists no employer restriction, read as any. Lender-type default (fintech) |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by Moneyview. fintech default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | true | flag | O | [MONEYVIEW-P3](https://moneyview.in/personal-loan) | 2026-10-12 |  |
| se_min_vintage_months | 24 | months | E | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | Not published by Moneyview. fintech default, the value ICICI Bank publishes for this rule (linked) |
| se_min_annual_income | 250000 | INR/year | E | [MONEYVIEW-P3](https://moneyview.in/personal-loan) | 2026-10-12 | Moneyview's eligibility page (linked) is silent on this rule. Lender-type default (fintech) |
| min_credit_score | 650 | score | O | [MONEYVIEW-P3](https://moneyview.in/personal-loan) | 2026-10-12 |  |
| ntc_allowed | true | flag | E | [MONEYVIEW-P1](https://moneyview.in/personal-loan-eligibility-check) | 2026-10-12 | Own credit model accepts low/thin scores |
| max_dpd_12m | 30 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 8 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.5 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by Moneyview. Banks: HDFC FOIR blog (40-55%) and benchmark calculator CALC-B1 (50%); NBFCs +5pp (higher risk appetite); fintech flat 50% (low-income book) |
| foir_50k_1l | 0.5 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by Moneyview. Banded FOIR: lenders allow a larger share of income as income rises (more residual income after expenses); base level from HDFC's FOIR article (40-55%, linked) |
| foir_ge_1l | 0.55 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by Moneyview. Banded FOIR for high earners; base level from HDFC's FOIR article (40-55%, linked) |
| max_income_multiple | 15 | x monthly income | E | [AXIS-C1](https://www.axis.bank.in/calculators/personal-loan-eligibility-calculator) | 2026-10-12 | Not published by Moneyview. fintech default, the value Axis Bank publishes for this rule (linked) |
| min_loan_amount | 5000 | INR | O | [MONEYVIEW-P1](https://moneyview.in/personal-loan-eligibility-check) | 2026-10-12 |  |
| max_loan_amount | 1000000 | INR | O | [MONEYVIEW-P3](https://moneyview.in/personal-loan) | 2026-10-12 |  |
| min_tenure_months | 3 | months | O | [MONEYVIEW-P3](https://moneyview.in/personal-loan) | 2026-10-12 |  |
| max_tenure_months | 60 | months | O | [MONEYVIEW-P3](https://moneyview.in/personal-loan) | 2026-10-12 |  |
| rate_min_pct | 14.0 | % p.a. | O | [MONEYVIEW-P3](https://moneyview.in/personal-loan) | 2026-10-12 |  |
| rate_max_pct | 36.0 | % p.a. | E | [MONEYVIEW-P2](https://www.moneyview.in/loans-faq-en) | 2026-10-11 | APR up to 45% includes fees; interest capped at 36% |
| processing_fee_pct | 0.02 | ratio | O | [MONEYVIEW-P3](https://moneyview.in/personal-loan) | 2026-10-12 |  |

## KreditBee (`kreditbee`, fintech)

29 rules, 17 estimated. Why chosen: Small-ticket lender; very low income floor.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | A | [KREDITBEE-A1](https://paisabazaar.com/personal-loan/kreditbee) | 2026-10-11 |  |
| max_age_at_maturity | 55 | years | E | [KREDITBEE-A2](https://gocredit.money/lender/kreditbee) | 2026-10-11 | One source says 45 at application; 55 at maturity assumed |
| max_age_at_maturity_se | 55 | years | E | [KREDITBEE-A2](https://gocredit.money/lender/kreditbee) | 2026-10-11 | Lender-type default (fintech); linked page does not state it |
| se_min_age | 23 | years | E | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | Not published by KreditBee. fintech default, the value ICICI Bank publishes for this rule (linked) |
| min_income_metro | 10000 | INR/month | O | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 | Personal income; household income must exceed Rs 25,000 |
| min_income_non_metro | 10000 | INR/month | O | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 | As above |
| min_total_exp_months | 6 | months | E | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 | KreditBee's eligibility page (linked) is silent on this rule. Lender-type default (fintech) |
| min_current_job_months | 2 | months | O | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 |  |
| allowed_employer_categories | any | list | E | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 | KreditBee's eligibility page (linked) lists no employer restriction, read as any. Lender-type default (fintech) |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by KreditBee. fintech default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | true | flag | E | [KREDITBEE-A1](https://paisabazaar.com/personal-loan/kreditbee) | 2026-10-11 | Lender-type default (fintech); linked page does not state it |
| se_min_vintage_months | 24 | months | E | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | Not published by KreditBee. fintech default, the value ICICI Bank publishes for this rule (linked) |
| se_min_annual_income | 250000 | INR/year | E | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 | KreditBee's eligibility page (linked) is silent on this rule. Lender-type default (fintech) |
| min_credit_score | 600 | score | E | [KREDITBEE-A2](https://gocredit.money/lender/kreditbee) | 2026-10-11 | Thin-file OK, but very low scores assumed declined |
| ntc_allowed | true | flag | A | [KREDITBEE-A2](https://gocredit.money/lender/kreditbee) | 2026-10-11 | No CIBIL required |
| max_dpd_12m | 30 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 8 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.5 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by KreditBee. Banks: HDFC FOIR blog (40-55%) and benchmark calculator CALC-B1 (50%); NBFCs +5pp (higher risk appetite); fintech flat 50% (low-income book) |
| foir_50k_1l | 0.5 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by KreditBee. Banded FOIR: lenders allow a larger share of income as income rises (more residual income after expenses); base level from HDFC's FOIR article (40-55%, linked) |
| foir_ge_1l | 0.55 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by KreditBee. Banded FOIR for high earners; base level from HDFC's FOIR article (40-55%, linked) |
| max_income_multiple | 15 | x monthly income | E | [AXIS-C1](https://www.axis.bank.in/calculators/personal-loan-eligibility-calculator) | 2026-10-12 | Not published by KreditBee. fintech default, the value Axis Bank publishes for this rule (linked) |
| min_loan_amount | 3000 | INR | O | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 |  |
| max_loan_amount | 1000000 | INR | O | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 |  |
| min_tenure_months | 3 | months | O | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 |  |
| max_tenure_months | 60 | months | O | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 |  |
| rate_min_pct | 12.0 | % p.a. | O | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 |  |
| rate_max_pct | 27.5 | % p.a. | O | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 |  |
| processing_fee_pct | 0.047 | ratio | O | [KREDITBEE-P1](https://www.kreditbee.in/personal-loan) | 2026-10-12 | Up to 4.7% + GST |

## Navi Finserv (`navi`, fintech)

29 rules, 16 estimated. Why chosen: Digital-only; long tenure (72 months).

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 21 | years | E | [NAVI-A1](https://www.paisabazaar.com/personal-loan/navi-finserv) | 2026-10-11 | Sources say 18 or 21; 21 used (contract-age + bureau norm) |
| max_age_at_maturity | 65 | years | A | [NAVI-A1](https://www.paisabazaar.com/personal-loan/navi-finserv) | 2026-10-11 |  |
| max_age_at_maturity_se | 65 | years | A | [NAVI-A1](https://www.paisabazaar.com/personal-loan/navi-finserv) | 2026-10-11 |  |
| se_min_age | 23 | years | E | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | Not published by Navi Finserv. fintech default, the value ICICI Bank publishes for this rule (linked) |
| min_income_metro | 25000 | INR/month | A | [NAVI-A1](https://www.paisabazaar.com/personal-loan/navi-finserv) | 2026-10-11 | Annual income > Rs 3 lakh |
| min_income_non_metro | 25000 | INR/month | A | [NAVI-A1](https://www.paisabazaar.com/personal-loan/navi-finserv) | 2026-10-11 |  |
| min_total_exp_months | 6 | months | E | [NAVI-P1](https://navi.com/personal-loan) | 2026-10-12 | Navi Finserv's eligibility page (linked) is silent on this rule. Lender-type default (fintech) |
| min_current_job_months | 3 | months | E | [NAVI-P1](https://navi.com/personal-loan) | 2026-10-12 | Navi Finserv's eligibility page (linked) is silent on this rule. Lender-type default (fintech) |
| allowed_employer_categories | any | list | E | [NAVI-P1](https://navi.com/personal-loan) | 2026-10-12 | Navi Finserv's eligibility page (linked) lists no employer restriction, read as any. Lender-type default (fintech) |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by Navi Finserv. fintech default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | true | flag | A | [NAVI-A1](https://www.paisabazaar.com/personal-loan/navi-finserv) | 2026-10-11 |  |
| se_min_vintage_months | 24 | months | E | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | Not published by Navi Finserv. fintech default, the value ICICI Bank publishes for this rule (linked) |
| se_min_annual_income | 250000 | INR/year | E | [NAVI-P1](https://navi.com/personal-loan) | 2026-10-12 | Navi Finserv's eligibility page (linked) is silent on this rule. Lender-type default (fintech) |
| min_credit_score | 650 | score | A | [NAVI-A2](https://gocredit.money/lender/navi) | 2026-10-11 | Paisabazaar says 750; conflict noted |
| ntc_allowed | false | flag | E | [BUREAU-SCORE](https://www.smfgindiacredit.com/knowledge-center/why-personal-loan-application-rejected.aspx) | 2026-10-12 | Lender-type default (fintech). Linked guide: most lenders want 700+ and no-score applicants may be rejected; this lender's own stance is not published |
| max_dpd_12m | 30 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 8 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.5 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by Navi Finserv. Banks: HDFC FOIR blog (40-55%) and benchmark calculator CALC-B1 (50%); NBFCs +5pp (higher risk appetite); fintech flat 50% (low-income book) |
| foir_50k_1l | 0.5 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by Navi Finserv. Banded FOIR: lenders allow a larger share of income as income rises (more residual income after expenses); base level from HDFC's FOIR article (40-55%, linked) |
| foir_ge_1l | 0.55 | ratio | E | [HDFC-P3](https://www.hdfc.bank.in/blogs/personal-loan/what-is-foir-does-it-affect-your-personal-loan-approval) | 2026-10-11 | Not published by Navi Finserv. Banded FOIR for high earners; base level from HDFC's FOIR article (40-55%, linked) |
| max_income_multiple | 15 | x monthly income | E | [AXIS-C1](https://www.axis.bank.in/calculators/personal-loan-eligibility-calculator) | 2026-10-12 | Not published by Navi Finserv. fintech default, the value Axis Bank publishes for this rule (linked) |
| min_loan_amount | 10000 | INR | A | [NAVI-A2](https://gocredit.money/lender/navi) | 2026-10-11 |  |
| max_loan_amount | 2000000 | INR | A | [NAVI-A2](https://gocredit.money/lender/navi) | 2026-10-11 |  |
| min_tenure_months | 3 | months | A | [NAVI-A2](https://gocredit.money/lender/navi) | 2026-10-11 |  |
| max_tenure_months | 84 | months | O | [NAVI-P1](https://navi.com/personal-loan) | 2026-10-12 | Product card on the page source; the page is script-rendered |
| rate_min_pct | 9.9 | % p.a. | A | [NAVI-A2](https://gocredit.money/lender/navi) | 2026-10-11 |  |
| rate_max_pct | 29.96 | % p.a. | O | [NAVI-P1](https://navi.com/personal-loan) | 2026-10-12 | 'Interest rates up to 29.96%' |
| processing_fee_pct | 0.0 | ratio | A | [NAVI-A2](https://gocredit.money/lender/navi) | 2026-10-11 | Nil per GoCredit |

## Fibe (EarlySalary) (`fibe`, fintech)

29 rules, 11 estimated. Why chosen: Lends to first-time borrowers.

| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |
|---|---|---|---|---|---|---|
| min_age | 19 | years | O | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 |  |
| max_age_at_maturity | 55 | years | O | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 | Stated as age 19-55; treated as the limit at loan end |
| max_age_at_maturity_se | 58 | years | E | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 | Fibe (EarlySalary)'s eligibility page (linked) is silent on this rule. Lender-type default (fintech) |
| se_min_age | 23 | years | E | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | Not published by Fibe (EarlySalary). fintech default, the value ICICI Bank publishes for this rule (linked) |
| min_income_metro | 25000 | INR/month | O | [FIBE-P2](https://www.fibe.in/personal-loan/eligibility-criteria/) | 2026-10-12 | Eligibility page Rs 25,000; product page says Rs 20,000 |
| min_income_non_metro | 25000 | INR/month | O | [FIBE-P2](https://www.fibe.in/personal-loan/eligibility-criteria/) | 2026-10-12 | As above |
| min_total_exp_months | 6 | months | E | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 | Fibe (EarlySalary)'s eligibility page (linked) is silent on this rule. Lender-type default (fintech) |
| min_current_job_months | 3 | months | E | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 | Fibe (EarlySalary)'s eligibility page (linked) is silent on this rule. Lender-type default (fintech) |
| allowed_employer_categories | any | list | E | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 | Fibe (EarlySalary)'s eligibility page (linked) lists no employer restriction, read as any. Lender-type default (fintech) |
| salary_account_required | false | flag | E | [PNB-N1](https://indianpsu.com/pnb-launches-pnb-swagat-a-seamless-digital-personal-loan-solution-for-new-customers) | 2026-10-12 | Not published by Fibe (EarlySalary). fintech default, the value Punjab National Bank publishes for this rule (linked) |
| self_employed_allowed | false | flag | O | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 | Salaried (private or public sector) |
| se_min_vintage_months | 24 | months | E | [ICICI-P4](https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility) | 2026-10-12 | Not published by Fibe (EarlySalary). fintech default, the value ICICI Bank publishes for this rule (linked) |
| se_min_annual_income | 250000 | INR/year | E | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 | Fibe (EarlySalary)'s eligibility page (linked) is silent on this rule. Lender-type default (fintech) |
| min_credit_score | 650 | score | O | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 | Preferably 650+; first-time borrowers considered |
| ntc_allowed | true | flag | O | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 |  |
| max_dpd_12m | 30 | days | E | [BUREAU-DPD](https://www.adityabirlacapital.com/abc-of-money/days-past-due-in-cibil-report) | 2026-10-12 | Not published. Industry practice: banks decline any 30+ DPD in last 12m; NBFC/fintech tolerate up to 30 days. Linked guide confirms high DPD leads to decline but gives no threshold; the day limit is the estimate |
| max_enquiries_6m | 8 | count | E | [BUREAU-ENQ](https://www.adityabirlacapital.com/abc-of-money/frequent-instant-personal-loan-applications) | 2026-10-12 | Not published. Credit-hungry flag; banks stricter than NBFC/fintech. Linked guide confirms frequent enquiries can lead to decline but gives no count; the count is the estimate |
| writeoff_allowed | false | flag | E | [BUREAU-WO](https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil) | 2026-10-12 | Not published. Written-off/settled accounts are a standard knock-out at all lenders. Linked guide: lenders may refuse a loan with a written-off or settled account |
| foir_lt_50k | 0.7 | ratio | O | [FIBE-C1](https://www.fibe.in/personal-loan-eligibility-calculator/) | 2026-10-12 | Calculator: all EMIs incl. the new one within 70% of income (its eligibility page says debt-to-income under 40%; the calculator is used) |
| foir_50k_1l | 0.7 | ratio | O | [FIBE-C1](https://www.fibe.in/personal-loan-eligibility-calculator/) | 2026-10-12 | Calculator: all EMIs incl. the new one within 70% of income (its eligibility page says debt-to-income under 40%; the calculator is used) |
| foir_ge_1l | 0.7 | ratio | O | [FIBE-C1](https://www.fibe.in/personal-loan-eligibility-calculator/) | 2026-10-12 | Calculator: all EMIs incl. the new one within 70% of income (its eligibility page says debt-to-income under 40%; the calculator is used) |
| max_new_emi_pct | 0.3 | ratio | O | [FIBE-C1](https://www.fibe.in/personal-loan-eligibility-calculator/) | 2026-10-12 | Calculator: the new EMI alone at most 30% of income |
| min_loan_amount | 5000 | INR | O | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 |  |
| max_loan_amount | 1000000 | INR | O | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 |  |
| min_tenure_months | 6 | months | O | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 |  |
| max_tenure_months | 36 | months | O | [FIBE-P1](https://fibe.in/personal-loan/) | 2026-10-12 |  |
| rate_min_pct | 18.0 | % p.a. | O | [FIBE-P3](https://www.fibe.in/personal-loan/personal-loan-interest-rate/) | 2026-10-12 |  |
| rate_max_pct | 30.0 | % p.a. | A | [FIBE-A1](https://www.paisabazaar.com/personal-loan/earlysalary) | 2026-10-11 |  |
| processing_fee_pct | 0.0 | ratio | O | [FIBE-P3](https://www.fibe.in/personal-loan/personal-loan-interest-rate/) | 2026-10-12 | 'no origination fee' |
