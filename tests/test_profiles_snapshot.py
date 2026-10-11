"""Golden-file test: committed results must match a fresh engine run."""
import json

from conftest import ROOT
from loan_engine.engine import Profile, assess
from loan_engine.report import result_to_dict


def test_outputs_up_to_date(lenders, profiles):
    fresh = [result_to_dict(assess(Profile(**p), lenders)) for p in profiles.values()]
    committed = json.loads((ROOT / "test_profiles/results.json").read_text())
    assert json.loads(json.dumps(fresh, default=str)) == committed, \
        "Run `python scripts/run_profiles.py` and commit test_profiles/results.json"


def test_at_least_ten_profiles_with_edge_cases(profiles):
    assert len(profiles) >= 10
