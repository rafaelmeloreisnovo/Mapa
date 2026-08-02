#!/usr/bin/env python3
"""Fail-closed validator for RAFAELIA geometric invariant contracts."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

FAMILIES = {
    "EUCLIDEAN_ISOMETRY": {
        "incidence", "distance", "angle", "area", "volume",
        "orientation", "connected_components", "betti_0", "betti_1",
        "euler_characteristic",
    },
    "SIMILARITY": {
        "incidence", "angle", "normalized_distance_ratio", "shape_class",
        "orientation", "connected_components", "betti_0", "betti_1",
        "euler_characteristic",
    },
    "AFFINE": {
        "incidence", "collinearity", "parallelism", "segment_ratio_collinear",
        "barycentric_coordinates", "area_ratio", "orientation",
        "connected_components", "betti_0", "betti_1", "euler_characteristic",
    },
    "PROJECTIVE": {
        "incidence", "collinearity", "cross_ratio", "connected_components",
        "betti_0", "betti_1", "euler_characteristic",
    },
    "HOMEOMORPHISM": {
        "connected_components", "betti_0", "betti_1", "betti_2",
        "euler_characteristic", "orientability", "boundary_components",
    },
    "DISCRETE_GLUE": {
        "incidence", "incidence_matrix", "vertex_count", "edge_count",
        "face_count", "glue_map", "combinatorial_orientation",
        "connected_components", "euler_characteristic",
    },
    "NUMERICAL_SIMULATION": {"measured_property"},
}

REQUIRED = {
    "contract_id", "object_id", "representation", "transformation_family",
    "invariants", "tolerance", "source_pointers", "falsifiers",
    "epistemic_state", "execution_level", "claim_allowed",
}


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED - data.keys())
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
        return errors

    family = data["transformation_family"]
    if family not in FAMILIES:
        errors.append(f"unknown transformation_family: {family}")
        return errors

    tolerance = data["tolerance"]
    if (
        not isinstance(tolerance, (int, float))
        or isinstance(tolerance, bool)
        or not math.isfinite(tolerance)
        or tolerance < 0
    ):
        errors.append("tolerance must be a finite number >= 0")

    if not isinstance(data["source_pointers"], list) or not data["source_pointers"]:
        errors.append("source_pointers must be a non-empty list")
    if not isinstance(data["falsifiers"], list) or not data["falsifiers"]:
        errors.append("falsifiers must be a non-empty list")
    if not isinstance(data["invariants"], list) or not data["invariants"]:
        errors.append("invariants must be a non-empty list")
        return errors

    allowed = FAMILIES[family]
    for index, item in enumerate(data["invariants"]):
        if not isinstance(item, dict):
            errors.append(f"invariants[{index}] must be an object")
            continue
        key = item.get("key")
        if key not in allowed:
            errors.append(
                f"invariant '{key}' is not permitted for {family}; "
                f"allowed={sorted(allowed)}"
            )
        override = item.get("tolerance_override")
        if override is not None and (
            not isinstance(override, (int, float))
            or isinstance(override, bool)
            or not math.isfinite(override)
            or override < 0
        ):
            errors.append(
                f"invariants[{index}].tolerance_override must be finite >= 0"
            )

    promoted = data["epistemic_state"] in {"MATH_FORMAL", "VERIFIED_LIMITED"}
    if promoted and not data.get("evidence_pointers"):
        errors.append("promoted state requires evidence_pointers")
    if data.get("claim_allowed") and data["epistemic_state"] not in {
        "MATH_FORMAL", "VERIFIED_LIMITED"
    }:
        errors.append(
            "claim_allowed=true requires MATH_FORMAL or VERIFIED_LIMITED"
        )
    if family == "DISCRETE_GLUE":
        keys = {
            item.get("key")
            for item in data["invariants"]
            if isinstance(item, dict)
        }
        if "glue_map" not in keys:
            errors.append(
                "DISCRETE_GLUE requires glue_map or explicit TOKEN_VAZIO glue_map entry"
            )
    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "usage: validate_geometric_invariant_contract.py FILE.json [...]",
            file=sys.stderr,
        )
        return 2

    failed = False
    for name in sys.argv[1:]:
        path = Path(name)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # fail closed at the file boundary
            print(f"FAIL {path}: invalid JSON: {exc}")
            failed = True
            continue

        errors = validate(data)
        if errors:
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
            failed = True
        else:
            print(f"PASS {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
