#!/usr/bin/env python3
import json
import sys
from fractions import Fraction
from pathlib import Path

doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
failures = []
for row in doc.get("vectors", []):
    kind = row["type"]
    if kind == "rafaelian_recurrence":
        got = row["a"] + row["b"] + 1
        expected = row["expected"]
    elif kind == "toroidal_fold_distance":
        distance = abs(row["a"] - row["b"])
        got = min(distance, row["m"] - distance)
        expected = row["expected"]
    elif kind == "planning_decay":
        sigma0 = Fraction(row["sigma0_num"], row["sigma0_den"])
        phi = Fraction(row["phi_num"], row["phi_den"])
        got = sigma0 * (phi ** row["n"])
        expected = Fraction(row["expected_num"], row["expected_den"])
    elif kind == "custom_shrink_score":
        sigma0 = Fraction(row["sigma0_num"], row["sigma0_den"])
        sigman = Fraction(row["sigman_num"], row["sigman_den"])
        got = 1 - (sigman / sigma0) ** 2
        expected = Fraction(row["expected_num"], row["expected_den"])
    else:
        failures.append(row["id"] + ":unknown")
        continue
    if got != expected:
        failures.append(row["id"])
print(json.dumps({"status": "PASS" if not failures else "FAIL", "vectors": len(doc.get("vectors", [])), "failures": failures, "claim_allowed": False}, sort_keys=True))
raise SystemExit(0 if not failures else 1)
