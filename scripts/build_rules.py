"""Validate rules_long.csv and publish the one-row-per-lender views.

Outputs:
  data/lender_rules.csv      one row per lender; for each rule: value, source URL, date, estimate flag,
                           and how the value was estimated (blank when published)
  data/lender_rules.md     readable per-lender rule sheet with links
"""
import csv

from _path import ROOT
from loan_engine.rules import SEGMENTS, _read, load_catalog, load_lenders, load_sources


def main():
    load_lenders()  # raises if the long table fails validation
    catalog, sources = load_catalog(), load_sources()
    lenders = _read("lenders.csv")
    rows = _read("rules_long.csv")
    by_lender = {}
    for r in rows:
        by_lender.setdefault(r["lender_id"], {})[r["rule"]] = r

    # base rules in catalog order, each followed by its segment variants (rule@govt, rule@rel, rule@govt_rel)
    present = {r["rule"] for r in rows}
    rule_order = [k for base in catalog for k in [base] + [f"{base}@{s}" for s in SEGMENTS] if k == base or k in present]
    header = ["lender_id", "lender_name", "lender_type"]
    for rule in rule_order:
        header += [rule, f"{rule}__source_url", f"{rule}__accessed_on", f"{rule}__is_estimate",
                   f"{rule}__estimation_method"]
    with open(ROOT / "data/lender_rules.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for l in lenders:
            out = [l["lender_id"], l["lender_name"], l["lender_type"]]
            for rule in rule_order:
                r = by_lender[l["lender_id"]].get(rule)
                if r is None:
                    out += ["", "", "", "", ""]
                else:
                    s = sources[r["source_id"]]
                    out += [r["value"], s["url"], s["accessed_on"], r["is_estimate"], r["estimation_method"]]
            w.writerow(out)

    md = ["# Lender rule sheet", "",
          "Generated from `data/rules_long.csv` by `python scripts/build_rules.py`. "
          "Tier: **O** = lender's own site, **A** = aggregator, **E** = estimate (method given). "
          "All sources read on the date shown. A rule ending in `@govt`, `@rel` or `@govt_rel` applies only to "
          "government/PSU employees, applicants with a salary account at this lender, or both, and overrides "
          "the plain rule for them.", ""]
    tier_tag = {"lender_official": "O", "aggregator": "A", "estimate": "E"}
    for l in lenders:
        rules = by_lender[l["lender_id"]]
        n_est = sum(r["is_estimate"] == "true" for r in rules.values())
        md += [f"## {l['lender_name']} (`{l['lender_id']}`, {l['lender_type']})", "",
               f"{len(rules)} rules, {n_est} estimated. Why chosen: {l['selection_reason']}.", "",
               "| Rule | Value | Unit | Tier | Source | Date | Note / estimation method |",
               "|---|---|---|---|---|---|---|"]
        for rule in rule_order:
            r = rules.get(rule)
            if not r:
                continue
            s = sources[r["source_id"]]
            link = f"[{s['source_id']}]({s['url']})" if s["url"] else s["source_id"]
            note = (r["estimation_method"] or r["notes"]).replace("|", "/")
            md.append(f"| {rule} | {r['value'].replace('|', ', ')} | {catalog[rule.partition('@')[0]]['unit']} | {tier_tag[r['evidence_tier']]} | "
                      f"{link} | {s['accessed_on']} | {note} |")
        md.append("")
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "data/lender_rules.md").write_text("\n".join(md))
    print(f"Validated {len(rows)} rules; wrote data/lender_rules.csv and data/lender_rules.md")


if __name__ == "__main__":
    main()
