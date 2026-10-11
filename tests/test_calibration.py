"""Model must reproduce every captured calculator probe (see research/HOW_TO_PROBE.md)."""
import pytest

from calibrate import implied, load_probes, replay

PROBES = [p for p in load_probes() if p["eligible_shown"] == "Y"]


@pytest.mark.parametrize("probe", [p for p in PROBES if p["lender_id"] == "_benchmark"],
                         ids=lambda p: p["probe_id"])
def test_benchmark_calculator_implies_50pct_foir(probe):
    foir, _ = implied(probe)
    assert foir == pytest.approx(0.50, abs=0.01)


@pytest.mark.parametrize("probe", [p for p in PROBES if not p["lender_id"].startswith("_") and p.get("replay", "Y") == "Y"],
                         ids=lambda p: p["probe_id"])
def test_engine_reproduces_lender_calculator(probe, lenders):
    assert replay(probe, lenders) == pytest.approx(probe["max_loan_shown"], rel=0.03)
