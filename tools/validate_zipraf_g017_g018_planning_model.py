#!/usr/bin/env python3
from fractions import Fraction
import json

sigma0 = Fraction(12, 5)  # 2.4
phi = Fraction(7, 10)     # planning value 0.7
target = Fraction(1, 2)   # strict target < 0.5

series = [sigma0 * (phi ** n) for n in range(0, 7)]
first_below = next(n for n, value in enumerate(series) if value < target)
cycle4 = series[4]
cycle5 = series[5]
shrink_score = Fraction(1, 1) - (cycle4 / sigma0) ** 2

assert cycle4 == Fraction(7203, 12500)
assert cycle4 > target
assert cycle5 == Fraction(50421, 125000)
assert cycle5 < target
assert first_below == 5
assert shrink_score == Fraction(94235199, 100000000)

receipt = {
    "schema_version": "rafaelia.zipraf-g017-g018-planning-recompute.v1",
    "model_scope": "planning_algebra_only",
    "sigma0": {"fraction": "12/5", "decimal": float(sigma0)},
    "phi_planning": {
        "fraction": "7/10",
        "decimal": float(phi),
        "empirical_status": "TOKEN_VAZIO_EVIDENCE"
    },
    "target": {"relation": "<", "fraction": "1/2", "decimal": 0.5},
    "cycle4": {
        "fraction": "7203/12500",
        "decimal": float(cycle4),
        "meets_target": cycle4 < target
    },
    "cycle5": {
        "fraction": "50421/125000",
        "decimal": float(cycle5),
        "meets_target": cycle5 < target
    },
    "first_cycle_below_target": first_below,
    "displayed_r2_recomputed": {
        "fraction": "94235199/100000000",
        "decimal": float(shrink_score),
        "classification": "CUSTOM_SHRINK_SCORE_NOT_STATISTICAL_R2"
    },
    "confidence_interpretation": "TOKEN_VAZIO_VALIDATION",
    "g017": "OPEN_TOKEN_VAZIO_EVIDENCE",
    "g018": "OPEN_TOKEN_VAZIO_VALIDATION",
    "claim_allowed": False
}

print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2))
