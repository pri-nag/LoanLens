import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from loan_engine.engine import Profile  # noqa: E402
from loan_engine.rules import load_lenders  # noqa: E402


@pytest.fixture(scope="session")
def lenders():
    return load_lenders()


@pytest.fixture(scope="session")
def profiles():
    return {p["profile_id"]: p for p in json.loads((ROOT / "test_profiles/profiles.json").read_text())}


@pytest.fixture
def make_profile(profiles):
    def _make(base="P01", **overrides):
        return Profile(**{**profiles[base], **overrides})
    return _make
