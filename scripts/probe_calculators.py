"""Drive public lender eligibility calculators with controlled inputs and record each answer.

The answers were inverted in scripts/calibrate.py to recover the unpublished rules (FOIR, salary multiple, cap);
see research/HOW_TO_PROBE.md. Public pages only, no login, a pause between inputs.

Setup (not needed for the model or tests):
    pip install playwright && python -m playwright install chromium

Usage:
    python scripts/probe_calculators.py OUTDIR explore [lender ...]   one probe each, prints the answer + screenshot
    python scripts/probe_calculators.py OUTDIR sweep   [lender ...]   income / EMI / tenure sweep -> OUTDIR/probes_raw.csv

Set INCOMES=55000,60000 to probe chosen incomes only. Lender pages change; if a selector stops matching, run
`explore` and update CALCS. The raw rows were turned into research/probes.csv (calc_cap and replay columns added).
"""
import csv
import datetime
import os
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

RUPEES = r"\s*(?:₹|Rs\.?)\s*([\d,]+)"

# url, input selectors, tenures to try (months; absent = no tenure input or tenure ignored), regex for the answer
CALCS = {
    "axis": dict(url="https://www.axis.bank.in/calculators/personal-loan-eligibility-calculator",
                 income="#monIncome", emi="#exp_amount", dob="#datepicker",
                 result=r"eligible for up to" + RUPEES),
    "kotak": dict(url="https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html",
                  income="(//input[contains(@class,'rangedata')])[1]", emi="(//input[contains(@class,'rangedata')])[2]",
                  tenure_years="(//input[contains(@class,'rangedata')])[3]",
                  result=r"Loan Eligible Amount" + RUPEES, tenures=[36, 60, 72]),
    "idfc": dict(url="https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan/personal-loan-eligibility-calculator",
                 income="#emi-pl-amt", emi="#emi-pl-amt2",
                 result=r"eligible for a total loan amount of" + RUPEES),
    "poonawalla": dict(url="https://poonawallafincorp.com/personal-loan/eligibility-calculator",
                       income="#netSalary1", emi="#monthlyEMI1", tenure_months="#tenure1",
                       result=r"eligible for a Personal Loan of up to" + RUPEES, tenures=[24, 48, 84]),
    "abcl": dict(url="https://www.adityabirlacapital.com/abc-of-calculators/personal-loan-eligibility-calculator",
                 pre={"#loanAmount": 1000, "#monthlyIncomeVariable": 0}, income="#monthlyIncome",
                 emi="#monthlyExpenses", tenure_years="#tenurePeriod", rate="#interestRate", rates=[11.0], enter=True,
                 result=r"eligible for a Personal Loan of Rs\.?\s*([\d,]+)", tenures=[24, 60, 84]),
    # sliders only; the calculator picks the tenure itself (12 / 24 / 36 months by income) at 2% a month
    "fibe": dict(url="https://www.fibe.in/personal-loan-eligibility-calculator/",
                 income="js:#loan-slider-1", emi="js:#loan-slider-2", fixed_rate=24.0,
                 result=r"eligible for a loan of up to\s*₹\s*([\d,]+)", tenure_result=r"Tenure\s*(\d+)\s*Months"),
    # Its employer search API returned HTTP 503 (2026-10-12), so the page's own calculator class is run directly
    # for a "cat a" employer: same code the page runs once an employer is picked
    "tata": dict(url="https://www.tatacapital.com/personal-loan/eligibility-calculator.html", fixed_rate=10.99,
                 page_fn="(a) => new eligibilityCalculator.instance({companyCat: 'cat a', monthlyInc: a[0], "
                         "monthlyExp: a[1], tenure: a[2]}).calculate().finalAmount",
                 tenures=[12, 24, 36, 48, 60]),
    # Returns Rs 0 for every input: its script defines FOIR for home loans and LAP only (see data/sources.csv LT-P4)
    "lt": dict(url="https://www.ltfinance.com/personal-loan-eligibility-calculator",
               income="#nhloan-Requirement-input", emi="#monthlyObligations", tenure_months="#month-tenure",
               rate="#annualInterestRate", rates=[11.0],
               sliders={"income": "(//input[@type='range'])[1]", "emi": "(//input[@type='range'])[2]",
                        "tenure_months": "(//input[@type='range'])[3]", "rate": "(//input[@type='range'])[4]"},
               result=r"Eligible loan amount" + RUPEES, tenures=[24, 48, 72]),
}
SWEEP = [(inc, 0) for inc in (30000, 50000, 75000, 100000, 150000, 200000)] + [(50000, e) for e in (5000, 10000, 20000)]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
SET_JS = """(e, v) => { const d = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(e), 'value');
  e.focus(); d && d.set ? d.set.call(e, v) : (e.value = v);
  for (const t of ['input', 'keyup', 'change', 'blur']) e.dispatchEvent(new Event(t, {bubbles: true})); }"""


def loc(page, sel):
    return page.locator(f"xpath={sel}" if sel.startswith(("(", "//")) else sel).first


def set_text(page, sel, value):
    if sel.startswith("js:"):  # range sliders: set the value the way a React onChange sees it
        loc(page, sel[3:]).evaluate(SET_JS, str(value))
        page.wait_for_timeout(600)
        return
    el = loc(page, sel)
    try:
        el.scroll_into_view_if_needed(timeout=8000)
        el.click(timeout=5000)
        el.press("Control+A")
        el.press("Delete")
        el.type(str(value), delay=40)
        el.press("Tab")
    except Exception:  # covered or styled inputs: set the value and fire the events the page listens to
        el.evaluate(SET_JS, str(value))
    page.wait_for_timeout(1200)


def probe(page, cfg, income, emi, tenure_m=None):
    """Answer for one input set: (max loan, tenure the calculator used, page text)."""
    if "page_fn" in cfg:
        amount = page.evaluate(cfg["page_fn"], [income, emi, tenure_m])
        return (int(round(amount)) if amount and amount == amount and amount > 0 else 0), tenure_m, ""
    values = {"income": income, "emi": emi}
    for sel, v in cfg.get("pre", {}).items():
        set_text(page, sel, v)
    set_text(page, cfg["income"], income)
    set_text(page, cfg["emi"], emi)
    if tenure_m and "tenure_months" in cfg:
        set_text(page, cfg["tenure_months"], tenure_m)
        values["tenure_months"] = tenure_m
    if tenure_m and "tenure_years" in cfg:
        set_text(page, cfg["tenure_years"], tenure_m // 12)
    if "rate" in cfg:
        set_text(page, cfg["rate"], cfg["rates"][0])
        values["rate"] = cfg["rates"][0]
    for field, sel in cfg.get("sliders", {}).items():  # calculators that only recompute on slider events
        if field in values:
            loc(page, sel).evaluate(SET_JS, str(values[field]))
    if cfg.get("enter"):
        loc(page, cfg["income"]).press("Enter")
    page.wait_for_timeout(2500)
    text = page.evaluate("() => document.body.innerText")
    m = re.search(cfg["result"], text)
    t = re.search(cfg["tenure_result"], text) if "tenure_result" in cfg else None
    return (int(m.group(1).replace(",", "")) if m else None), (int(t.group(1)) if t else tenure_m), text


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    out, mode, only = Path(sys.argv[1]), sys.argv[2], set(sys.argv[3:])
    out.mkdir(parents=True, exist_ok=True)
    sweep = [(int(i), 0) for i in os.environ["INCOMES"].split(",")] if os.environ.get("INCOMES") else SWEEP
    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1366, "height": 900}, locale="en-IN", user_agent=UA)
        for name, cfg in CALCS.items():
            if only and name not in only:
                continue
            page = ctx.new_page()
            try:
                page.goto(cfg["url"], wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(6000)
                if "dob" in cfg:
                    try:
                        set_text(page, cfg["dob"], "15/06/1992")
                    except Exception:
                        pass
                tenures = cfg.get("tenures", [None])
                if mode == "explore":
                    amount, _, text = probe(page, cfg, 50000, 0, tenures[-1])
                    page.screenshot(path=str(out / f"{name}_probe.png"))
                    print(f"== {name}: income 50,000, EMI 0, tenure {tenures[-1]} -> {amount}")
                    for line in [l.strip() for l in text.split("\n") if re.search(r"(?i)eligible", l)][:4]:
                        print("    ", line[:150])
                    continue
                for t in tenures:
                    for inc, emi in sweep:
                        amount, used_t, _ = probe(page, cfg, inc, emi, t)
                        rows.append(dict(lender=name, url=cfg["url"], accessed_on=datetime.date.today().isoformat(),
                                         income=inc, emi=emi, tenure_months=used_t or "",
                                         rate=cfg.get("fixed_rate") or (cfg.get("rates") or [""])[0], amount=amount))
                        print(name, inc, emi, t, amount, flush=True)
            except Exception as e:
                print(f"== {name}: ERROR {type(e).__name__}: {str(e)[:200]}")
            finally:
                page.close()
        browser.close()
    if rows:
        path = out / "probes_raw.csv"
        new = not path.exists()
        with open(path, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            if new:
                w.writeheader()
            w.writerows(rows)
        print(f"{len(rows)} rows -> {path}")


if __name__ == "__main__":
    main()
