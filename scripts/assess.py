"""Assess one applicant from a JSON file:  python scripts/assess.py my_profile.json"""
import json
import sys

from _path import ROOT  # noqa: F401
from loan_engine.engine import Profile, assess
from loan_engine.report import profile_markdown
from loan_engine.rules import load_lenders

if __name__ == "__main__":
    data = json.loads(open(sys.argv[1]).read())
    print(profile_markdown(assess(Profile(**data), load_lenders())))
