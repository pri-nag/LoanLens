"""Load, type and validate the lender rule tables.

A rule key is either a base rule from rule_catalog.csv (``foir_lt_50k``) or a base rule plus an applicant
segment (``foir_lt_50k@govt_rel``). Segment values override the base value for applicants in that segment:

  govt      salaried employee of a government body or PSU
  rel       holds a salary account with this lender (existing relationship)
  govt_rel  both

The value ``none`` switches an inherited optional rule off for that segment.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data"

TYPES = {"int": int, "float": float, "bool": lambda v: v == "true", "str": str}
TIERS = {"lender_official", "aggregator", "estimate"}
SEGMENTS = ("govt", "rel", "govt_rel")  # least to most specific
OFF = "none"


@dataclass
class Rule:
    value: object
    source_id: str
    tier: str
    is_estimate: bool


@dataclass
class Lender:
    lender_id: str
    name: str
    lender_type: str
    rules: dict[str, Rule] = field(default_factory=dict)

    def get(self, rule: str, default=None):
        r = self.rules.get(rule)
        return default if r is None else r.value

    def has(self, rule: str) -> bool:
        return rule in self.rules

    def for_segments(self, segments: set[str]) -> "Lender":
        """The rules that apply to an applicant in ``segments``: base rules, overridden by segment rules."""
        resolved = {k: r for k, r in self.rules.items() if "@" not in k}
        for seg in SEGMENTS:
            if seg in segments:
                for key, r in self.rules.items():
                    base, _, s = key.partition("@")
                    if s == seg:
                        resolved[base] = r
        resolved = {k: r for k, r in resolved.items() if r.value != OFF}
        return Lender(self.lender_id, self.name, self.lender_type, resolved)


def _read(name: str) -> list[dict]:
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_catalog() -> dict[str, dict]:
    return {r["rule"]: r for r in _read("rule_catalog.csv")}


def load_sources() -> dict[str, dict]:
    return {r["source_id"]: r for r in _read("sources.csv")}


def validate(rows: list[dict], catalog: dict, sources: dict, lender_ids: set[str]) -> list[str]:
    """Return a list of data-quality errors (empty list = clean)."""
    errors, seen = [], set()
    for i, r in enumerate(rows, start=2):
        where = f"rules_long.csv line {i} ({r['lender_id']}.{r['rule']})"
        if None in r or None in r.values():  # unescaped quote or comma split the row
            errors.append(f"{where}: malformed CSV row (wrong number of columns)")
            continue
        base, _, seg = r["rule"].partition("@")
        if r["lender_id"] not in lender_ids:
            errors.append(f"{where}: unknown lender")
        if base not in catalog:
            errors.append(f"{where}: rule not in rule_catalog.csv")
            continue
        if seg and seg not in SEGMENTS:
            errors.append(f"{where}: unknown segment {seg!r} (use one of {', '.join(SEGMENTS)})")
        if (r["lender_id"], r["rule"]) in seen:
            errors.append(f"{where}: duplicate rule")
        seen.add((r["lender_id"], r["rule"]))
        if r["source_id"] not in sources:
            errors.append(f"{where}: unknown source_id {r['source_id']}")
        if r["evidence_tier"] not in TIERS:
            errors.append(f"{where}: bad evidence_tier")
        if r["is_estimate"] == "true" and not r["estimation_method"]:
            errors.append(f"{where}: estimate without estimation_method")
        if (r["is_estimate"] == "true") != (r["evidence_tier"] == "estimate"):
            errors.append(f"{where}: is_estimate disagrees with evidence_tier")
        if r["value"] == OFF and not seg:
            errors.append(f"{where}: '{OFF}' is only allowed on a segment rule")
        elif r["value"] != OFF:
            try:
                TYPES[catalog[base]["type"]](r["value"])
            except ValueError:
                errors.append(f"{where}: value {r['value']!r} is not {catalog[base]['type']}")
    required = [k for k, c in catalog.items() if "optional" not in c["description"]]
    for lid in lender_ids:
        for k in required:
            if k.startswith("foir_") and (lid, "foir_bands") in seen:  # the lender's own breakpoints replace them
                continue
            if (lid, k) not in seen:
                errors.append(f"{lid}: missing required rule {k}")
    return errors


def load_lenders() -> dict[str, Lender]:
    catalog, sources = load_catalog(), load_sources()
    lenders = {r["lender_id"]: Lender(r["lender_id"], r["lender_name"], r["lender_type"])
               for r in _read("lenders.csv")}
    rows = _read("rules_long.csv")
    errors = validate(rows, catalog, sources, set(lenders))
    if errors:
        raise ValueError("Rule table failed validation:\n" + "\n".join(errors))
    for r in rows:
        value = r["value"]
        if value != OFF:
            value = TYPES[catalog[r["rule"].partition("@")[0]]["type"]](value)
        lenders[r["lender_id"]].rules[r["rule"]] = Rule(
            value, r["source_id"], r["evidence_tier"], r["is_estimate"] == "true")
    return lenders
