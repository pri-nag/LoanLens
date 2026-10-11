from loan_engine.rules import _read, load_catalog, load_sources, validate


def test_rule_table_is_clean(lenders):
    assert len(lenders) == 20


def test_every_rule_has_source_and_date():
    sources = load_sources()
    for r in _read("rules_long.csv"):
        s = sources[r["source_id"]]
        assert s["accessed_on"], r
        assert s["url"].startswith("https://"), r  # estimates link the page they were based on


def test_validator_catches_bad_rows():
    rows = _read("rules_long.csv")
    bad = dict(rows[0], is_estimate="true", evidence_tier="estimate", estimation_method="")
    errors = validate([bad] + rows[1:], load_catalog(), load_sources(),
                      {r["lender_id"] for r in rows})
    assert any("estimate without estimation_method" in e for e in errors)
    errors = validate(rows + [rows[0]], load_catalog(), load_sources(), {r["lender_id"] for r in rows})
    assert any("duplicate rule" in e for e in errors)


def test_validator_checks_segment_rules():
    rows = _read("rules_long.csv")
    catalog, sources, ids = load_catalog(), load_sources(), {r["lender_id"] for r in rows}
    errors = validate(rows + [dict(rows[0], rule="foir_lt_50k@vip")], catalog, sources, ids)
    assert any("unknown segment" in e for e in errors)
    errors = validate(rows + [dict(rows[0], rule="rate_by_score", value="none")], catalog, sources, ids)
    assert any("only allowed on a segment rule" in e for e in errors)


def test_validator_catches_malformed_rows():
    rows = _read("rules_long.csv")
    errors = validate(rows + [{**rows[0], None: ["extra"]}], load_catalog(), load_sources(),
                      {r["lender_id"] for r in rows})
    assert any("malformed CSV row" in e for e in errors)
