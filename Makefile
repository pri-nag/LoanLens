.PHONY: all rules profiles calibrate insights test

all: rules profiles calibrate insights test

rules:      ; python3 scripts/build_rules.py && python3 scripts/export_excel.py
profiles:   ; python3 scripts/run_profiles.py
calibrate:  ; python3 scripts/calibrate.py
insights:   ; python3 scripts/insights.py
test:       ; python3 -m pytest -q
