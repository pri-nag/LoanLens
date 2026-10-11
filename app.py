"""LoanLens: Streamlit UI for the eligibility engine.  python -m streamlit run app.py"""
import json
import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from loan_engine.engine import Profile, assess  # noqa: E402
from loan_engine.report import result_to_dict  # noqa: E402
from loan_engine.rules import load_catalog, load_lenders  # noqa: E402

EMPLOYERS = ["govt", "psu", "mnc", "listed", "pvt_ltd", "llp", "proprietorship"]
CITIES = ["Mumbai", "Delhi", "New Delhi", "Gurugram", "Noida", "Bengaluru", "Chennai", "Kolkata",
          "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Indore", "Surat", "Patna", "Sitapur"]
BLANK = {"profile_id": "UI", "description": "Custom profile", "age": 30, "employment_type": "salaried",
         "employer_category": "pvt_ltd", "city": "Pune", "net_monthly_income": 50000,
         "total_work_exp_months": 48, "current_job_months": 18, "credit_score": 750, "existing_emi": 0,
         "max_dpd_12m": 0, "enquiries_6m": 1, "requested_amount": 500000, "requested_tenure_months": 36,
         "annual_income_itr": 600000, "business_vintage_months": 48}
# Knock-out checks in the order the engine runs them: failure name -> rule keys that feed it
CHECKS = {
    "min_age": ["min_age", "se_min_age"],
    "age_at_maturity": ["max_age_at_maturity", "max_age_at_maturity_se", "min_tenure_months"],
    "serviceable_cities": ["serviceable_cities"],
    "allowed_employer_categories": ["allowed_employer_categories"],
    "salary_account_required": ["salary_account_required"],
    "min_income": ["min_income_metro", "min_income_non_metro", "min_income_small_employer"],
    "min_total_exp_months": ["min_total_exp_months"],
    "min_current_job_months": ["min_current_job_months"],
    "self_employed_allowed": ["self_employed_allowed"],
    "se_min_vintage_months": ["se_min_vintage_months"],
    "se_min_annual_income": ["se_min_annual_income"],
    "ntc_allowed": ["ntc_allowed"],
    "min_credit_score": ["min_credit_score", "se_min_credit_score"],
    "max_dpd_12m": ["max_dpd_12m"],
    "max_enquiries_6m": ["max_enquiries_6m"],
    "writeoff_allowed": ["writeoff_allowed"],
    "foir": ["foir_bands", "foir_lt_50k", "foir_50k_1l", "foir_ge_1l", "max_new_emi_pct"],
    "min_loan_amount": ["min_loan_amount", "min_loan_amount_non_metro"],
}
CHECK_NAMES = {
    "min_age": "Minimum age", "age_at_maturity": "Age at end of loan", "serviceable_cities": "City served",
    "allowed_employer_categories": "Employer category",
    "salary_account_required": "Salary account with lender", "min_income": "Minimum monthly income",
    "min_total_exp_months": "Total work experience", "min_current_job_months": "Time in current job",
    "self_employed_allowed": "Accepts self-employed", "se_min_vintage_months": "Business vintage",
    "se_min_annual_income": "Annual income (ITR)", "ntc_allowed": "Accepts new-to-credit",
    "min_credit_score": "Credit score", "max_dpd_12m": "Missed payments (DPD, 12m)",
    "max_enquiries_6m": "Credit enquiries (6m)", "writeoff_allowed": "Written-off / settled accounts",
    "foir": "Room for a new EMI (FOIR)", "min_loan_amount": "Request >= minimum loan",
}
CHECK_KEYS = {k for keys in CHECKS.values() for k in keys} - {"min_tenure_months", "min_loan_amount",
                                                              "min_loan_amount_non_metro"}


@st.cache_resource
def lenders():
    return load_lenders()


@st.cache_resource
def catalog():
    return load_catalog()


@st.cache_data
def presets():
    data = json.loads((ROOT / "test_profiles" / "profiles.json").read_text())
    return {"Custom": BLANK} | {f"{p['profile_id']} - {p['description']}": p for p in data}


def inr(x):
    return f"Rs {x:,.0f}"


def applicant_value(check: str, p: Profile):
    return {
        "min_age": p.age, "age_at_maturity": f"age {p.age}", "serviceable_cities": p.city,
        "allowed_employer_categories": p.employer_category,
        "salary_account_required": p.salary_account_with or "none",
        "min_income": f"{inr(p.net_monthly_income)} ({p.city_tier.replace('_', '-')})",
        "min_total_exp_months": f"{p.total_work_exp_months} months",
        "min_current_job_months": f"{p.current_job_months} months",
        "self_employed_allowed": "self-employed", "se_min_vintage_months": f"{p.business_vintage_months} months",
        "se_min_annual_income": inr(p.annual_income_itr),
        "ntc_allowed": "no score" if p.credit_score is None else "has score",
        "min_credit_score": p.credit_score, "max_dpd_12m": f"{p.max_dpd_12m} days",
        "max_enquiries_6m": p.enquiries_6m, "writeoff_allowed": "yes" if p.has_writeoff_or_settlement else "no",
        "foir": f"existing EMI {inr(p.existing_emi)} = "
                f"{p.existing_emi / p.monthly_income:.0%} of income" if p.monthly_income else "no income",
        "min_loan_amount": inr(p.requested_amount),
    }[check]


def show(value):
    text = str(value)
    return text if len(text) <= 60 else f"{text.count('|') + 1} listed" if "|" in text else text[:57] + "..."


def rule_check(lr, p: Profile):
    """Every knock-out check this lender ran, with pass/fail, plus the sizing and pricing rules it used.

    Values come from lr.applied: the rules after segment overrides (govt / salary-account holder)."""
    rules = lr.applied
    failed = {f.rule: f for f in lr.failures}
    checks = []
    for check, keys in CHECKS.items():
        used = [k for k in keys if k in lr.rules_used]
        if not used:
            continue
        f = failed.get(check)
        rule = rules[used[0]]
        checks.append({
            "Check": CHECK_NAMES[check],
            "Result": "FAIL" if f else "pass",
            "Lender requires": f.required if f else ", ".join(f"{k} = {show(rules[k].value)}" for k in used),
            "Applicant has": str(applicant_value(check, p)),
            "Source": "estimate" if rule.is_estimate else rule.tier,
        })
    sizing = [{"Rule": k, "Value": show(rules[k].value), "Used for": catalog()[k]["stage"],
               "Source": "estimate" if rules[k].is_estimate else rules[k].tier}
              for k in catalog() if k in rules and k not in CHECK_KEYS]
    return checks, sizing


APP_NAME = "LoanLens"
CONFIDENCE_COLORS = alt.Scale(domain=["high", "medium", "low"], range=["#1b7f3b", "#e0a100", "#c0392b"])

st.set_page_config(page_title=f"{APP_NAME} - Personal loan eligibility", page_icon="🔎", layout="wide")
st.markdown("""<style>
.block-container {padding-top: 2rem;}
div[data-testid="stMetric"] {background: rgba(128,128,128,0.08); border-radius: 10px; padding: 12px 16px;}
div[data-testid="stMetricValue"] {font-size: 1.6rem;}
.stTabs [data-baseweb="tab"] {font-size: 1.05rem; padding: 8px 16px;}
</style>""", unsafe_allow_html=True)
st.title(f"🔎 {APP_NAME}")
st.markdown("##### Can I get a personal loan, and from whom? Checks one profile against the rules of 20 Indian lenders.")
st.caption("Rule-based model over data/rules_long.csv; results update as you change any input. 'Eligible' "
           "means the profile passes published and inferred rules, not that a lender will approve.")


def bar_chart(df, x, y, title, color=None, fmt=None, sort="-x", integer=False):
    """Horizontal bar chart sized to its rows, with full-length labels and the value at the end of each bar."""
    axis = alt.Axis(format=fmt or ("d" if integer else ""), tickMinStep=1 if integer else alt.Undefined)
    enc = alt.Chart(df).mark_bar(cornerRadiusEnd=4, size=22).encode(
        x=alt.X(x, title=title, axis=axis, scale=alt.Scale(nice=True)),
        y=alt.Y(y, sort=sort, title=None, axis=alt.Axis(labelLimit=320, labelFontSize=13)),
        tooltip=list(df.columns))
    if color:
        enc = enc.encode(color=alt.Color(color, scale=CONFIDENCE_COLORS, legend=alt.Legend(title="Data confidence",
                                                                                              orient="bottom")))
    text = enc.mark_text(align="left", dx=4, fontSize=12).encode(text=alt.Text(x, format=fmt or ""), color=alt.value("gray"))
    chart = (enc + text).properties(height=alt.Step(36), padding={"left": 5, "top": 5, "right": 60, "bottom": 5})
    return chart.configure_axis(labelFontSize=12, titleFontSize=13).configure_view(strokeWidth=0)

L = lenders()
sb = st.sidebar
sb.header("Applicant profile")
choice = sb.selectbox("Start from a test profile", list(presets()),
                      help="P09 and P14-P17 are expected to be rejected everywhere")
p = {**BLANK, **presets()[choice]}
k = choice  # widget keys per preset, so switching presets resets every input

sb.subheader("Applicant")
age = sb.number_input("Age (years)", 18, 80, p["age"], key=f"age{k}")
emp_type = sb.radio("Employment", ["salaried", "self_employed"],
                    index=0 if p["employment_type"] == "salaried" else 1, horizontal=True, key=f"et{k}")
city_opts = CITIES + ([p["city"]] if p["city"] not in CITIES else [])
city = sb.selectbox("City", city_opts, index=city_opts.index(p["city"]), key=f"city{k}")
salaried = emp_type == "salaried"
if salaried:
    emp_cat = sb.selectbox("Employer category", EMPLOYERS,
                           index=EMPLOYERS.index(p["employer_category"]) if p["employer_category"] in EMPLOYERS else 4,
                           key=f"ec{k}")
    income = sb.number_input("Net monthly income (Rs)", 0, 10_000_000, p.get("net_monthly_income") or 50000, 1000,
                             key=f"inc{k}")
    total_exp = sb.number_input("Total work experience (months)", 0, 600, p.get("total_work_exp_months") or 48,
                                key=f"te{k}")
    cur_job = sb.number_input("Months in current job", 0, 600, p.get("current_job_months") or 18, key=f"cj{k}")
    sal_ids = [None] + [lid for lid, l in L.items() if l.lender_type.endswith("bank")]
    sal_acct = sb.selectbox("Salary account with", sal_ids, format_func=lambda i: "none" if i is None else L[i].name,
                            index=sal_ids.index(p.get("salary_account_with")), key=f"sa{k}")
else:
    itr = sb.number_input("Annual income per ITR (Rs)", 0, 100_000_000, p.get("annual_income_itr") or 600000, 10000,
                          key=f"itr{k}")
    vintage = sb.number_input("Business vintage (months)", 0, 600, p.get("business_vintage_months") or 48,
                              key=f"bv{k}")

sb.subheader("Credit bureau")
ntc = sb.checkbox("New to credit (no score)", p["credit_score"] is None, key=f"ntc{k}")
score = None if ntc else sb.slider("Credit score", 300, 900, p["credit_score"] or 750, key=f"cs{k}")
existing_emi = sb.number_input("Existing EMIs (Rs/month)", 0, 10_000_000, p["existing_emi"], 500, key=f"emi{k}")
dpd_opts = [0, 30, 60, 90]
dpd = sb.selectbox("Worst days past due, last 12 months", dpd_opts,
                   index=dpd_opts.index(p["max_dpd_12m"]) if p["max_dpd_12m"] in dpd_opts else 0, key=f"dpd{k}")
enq = sb.number_input("Credit enquiries, last 6 months", 0, 50, p["enquiries_6m"], key=f"enq{k}")
wo = sb.checkbox("Written-off / settled account on record", p.get("has_writeoff_or_settlement", False), key=f"wo{k}")

sb.subheader("Loan wanted")
amount = sb.number_input("Amount (Rs)", 10000, 100_000_000, p["requested_amount"], 10000, key=f"amt{k}")
tenure = sb.slider("Tenure (months)", 6, 96, p["requested_tenure_months"], 6, key=f"ten{k}")

try:
    profile = Profile(
        profile_id=p["profile_id"], description=p["description"], age=age, employment_type=emp_type,
        employer_category=emp_cat if salaried else "none", city=city, credit_score=score,
        existing_emi=existing_emi, requested_amount=amount, requested_tenure_months=tenure,
        net_monthly_income=income if salaried else 0, annual_income_itr=0 if salaried else itr,
        business_vintage_months=0 if salaried else vintage,
        total_work_exp_months=total_exp if salaried else 0, current_job_months=cur_job if salaried else 0,
        max_dpd_12m=dpd, enquiries_6m=enq, has_writeoff_or_settlement=wo,
        salary_account_with=sal_acct if salaried else None)
except ValueError as e:
    st.error(str(e))
    st.stop()
res = assess(profile, L)
approving, rejected = res["approving_lenders"], res["rejected_lenders"]
everyone = {r.lender_id: r for r in approving + rejected}

best = res.get("best")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Decision", "✅ Eligible" if res["eligible"] else "❌ Not eligible")
c2.metric("Lenders that approve", f"{len(approving)} / {len(L)}")
c3.metric("Best lender", best.lender_name if best else "-")
c4.metric("Best APR", f"{best.apr}%" if best else "-")
facts = [f"City tier: {profile.city_tier.replace('_', '-')}", f"income used: {inr(profile.monthly_income)} a month"]
if best:
    facts.insert(0, f"Best offer: {inr(best.offer_amount)} for {best.offer_tenure} months, EMI {inr(best.emi)}")
st.caption(" · ".join(facts))

if res["eligible"]:
    b = res["best"]
    st.success(f"**Best option: {b.lender_name}** - offer {inr(b.offer_amount)} for {b.offer_tenure} months "
               f"at {b.rate_pct}% (APR {b.apr}%), EMI {inr(b.emi)}.\n\n{res['best_reason']}")
else:
    st.error(f"**Not eligible at any lender.** Main reasons: {res['reason']}.")
    st.info(f"Closest lender: **{res['nearest'].lender_name}**. What would change it: {res['what_would_change']}.")

tab_ok, tab_no, tab_check, tab_json = st.tabs(
    [f"Approving ({len(approving)})", f"Rejecting ({len(rejected)})", "Rule-by-rule check", "Raw JSON"])

with tab_ok:
    if approving:
        df = pd.DataFrame([{"Lender": r.lender_name, "APR %": r.apr, "Offer": r.offer_amount,
                            "Confidence": r.confidence} for r in approving])
        st.dataframe([{"Lender": r.lender_name, "Type": r.lender_type, "Max loan": r.max_loan,
                       "Limited by": r.binding_constraint, "Offer": r.offer_amount, "Tenure": r.offer_tenure,
                       "Tenure range": f"{r.tenure_range[0]}-{r.tenure_range[1]}m", "Rate %": r.rate_pct,
                       "Rate band %": f"{r.rate_band[0]}-{r.rate_band[1]}", "APR %": r.apr, "EMI": r.emi,
                       "Fee incl. GST": r.fee, "Total cost": r.total_cost, "Confidence": r.confidence}
                      for r in approving], use_container_width=True, hide_index=True, column_config={
            c: st.column_config.NumberColumn(format="Rs %d")
            for c in ["Max loan", "Offer", "EMI", "Fee incl. GST", "Total cost"]})
        st.caption("Income, existing EMIs, tenure and city mostly change these amounts and rates rather than "
                   "the list of lenders; the list changes only when an input crosses a lender's threshold.")
        left, right = st.columns(2)
        with left:
            st.markdown("**APR by lender** (lower is better; includes fees)")
            st.altair_chart(bar_chart(df, "APR %:Q", "Lender:N", "APR %", "Confidence:N", sort="x"), use_container_width=True)
        with right:
            st.markdown("**Loan each lender offers**")
            st.altair_chart(bar_chart(df, "Offer:Q", "Lender:N", "Rs", "Confidence:N", ",.0f"),
                            use_container_width=True)
    else:
        st.write("No lender approves this profile.")

with tab_no:
    if rejected:
        st.markdown("**Most common blockers** (number of lenders each rule rejects this profile at)")
        blockers = pd.DataFrame({"Blocker": list(res["blocker_counts"]), "Lenders": list(res["blocker_counts"].values())})
        st.altair_chart(bar_chart(blockers, "Lenders:Q", "Blocker:N", "Lenders rejecting", integer=True)
                        .configure_mark(color="#c0392b"), use_container_width=True)
        st.dataframe([{"Lender": r.lender_name, "Type": r.lender_type,
                       "Failed rules (has -> needs)": "; ".join(
                           f"{f.label}: {f.actual} -> {f.required}" for f in r.failures)}
                      for r in rejected], use_container_width=True, hide_index=True)
    else:
        st.write("No lender rejects this profile.")

with tab_check:
    order = [r.lender_id for r in approving + rejected]
    lid = st.selectbox("Lender", order, format_func=lambda i: f"{L[i].name} - "
                       f"{'approves' if everyone[i].eligible else 'rejects'}")
    checks, sizing = rule_check(everyone[lid], profile)
    st.markdown(f"**{len(checks)} eligibility checks** run by {L[lid].name}: "
                f"{sum(c['Result'] == 'pass' for c in checks)} passed, "
                f"{sum(c['Result'] == 'FAIL' for c in checks)} failed.")
    seg = everyone[lid].segments
    if seg:
        st.caption("Segment rules applied: " + ", ".join(
            {"govt": "government/PSU employee", "rel": "salary account with this lender",
             "govt_rel": "both"}[s] for s in seg) + " (these override the lender's general rules).")
    st.dataframe(pd.DataFrame(checks).style.map(
        lambda v: "color: #b00020; font-weight: bold" if v == "FAIL" else "color: #1b7f3b", subset=["Result"]),
        use_container_width=True, hide_index=True)
    st.markdown("**Rules used to size and price the loan**")
    st.dataframe(sizing, use_container_width=True, hide_index=True)
    r = everyone[lid]
    st.caption(f"Max loan {inr(r.max_loan)}, limited by {r.binding_constraint or '-'}; tenure range "
               f"{r.tenure_range[0]}-{r.tenure_range[1]} months; expected rate {r.rate_pct}% "
               f"(band {r.rate_band[0]}-{r.rate_band[1]}%).")

with tab_json:
    st.json(result_to_dict(res))
