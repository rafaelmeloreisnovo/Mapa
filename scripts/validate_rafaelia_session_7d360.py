#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ALLOWED_STATES = {
    "TOKEN_VAZIO",
    "HYPOTHESIS",
    "ANALOGY_ONLY",
    "FORMALIZED",
    "SUPPORTED",
    "CONTRADICTED",
    "INVALIDATED",
    "VERIFIED_LIMITED",
}


def validate(doc):
    errors = []
    if doc.get("claim_allowed") is not False:
        errors.append("claim_allowed must remain false")
    if doc.get("automatic_promotion") is not False:
        errors.append("automatic_promotion must remain false")
    space = doc.get("state_space", {})
    if space.get("directions") != 7:
        errors.append("state_space.directions must equal 7")
    if space.get("cells_per_generation_at_base_resolution") != 2520:
        errors.append("base generation must contain 7*360 = 2520 cells")
    sweep = doc.get("angular_sweep", {})
    if sweep.get("degrees") != 360 or sweep.get("base_bins") != 360:
        errors.append("angular sweep must be 360 degrees / 360 base bins")
    directions = doc.get("directions", [])
    if len(directions) != 7:
        errors.append("exactly seven directions are required")
    ids = [d.get("id") for d in directions]
    if len(ids) != len(set(ids)):
        errors.append("direction ids must be unique")
    for d in directions:
        missing = [k for k in ("id", "name", "session_tokens", "observables", "core_residual", "primary_falsifier", "state") if not d.get(k)]
        if missing:
            errors.append(f"{d.get('id','UNKNOWN')} missing {','.join(missing)}")
        if d.get("state") not in ALLOWED_STATES:
            errors.append(f"{d.get('id','UNKNOWN')} has invalid epistemic state")
        if len(d.get("session_tokens", [])) != 7:
            errors.append(f"{d.get('id','UNKNOWN')} must preserve seven session tokens")
    weights = doc.get("weight_policy", {})
    if weights.get("numeric_weights") != "TOKEN_VAZIO_UNCALIBRATED":
        errors.append("numeric weights must remain TOKEN_VAZIO_UNCALIBRATED until calibration")
    conflicts = doc.get("known_scope_conflicts", [])
    if not any(c.get("id") == "FORMULA_STOCK_486_VS_653" for c in conflicts):
        errors.append("486-vs-653 formula scope conflict must be preserved")
    outputs = set(doc.get("required_outputs", []))
    required_outputs = {
        "direction_state.jsonl",
        "angular_gap_map.jsonl",
        "hypothesis_ledger.jsonl",
        "falsifier_matrix.jsonl",
        "generation_receipt.json",
    }
    if outputs != required_outputs:
        errors.append("required_outputs set mismatch")
    return errors


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/control-plane/RAFAELIA_SESSION_7D360_EVOLUTION_CYCLE.v1.json")
    doc = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(doc)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: RAFAELIA session 7D x 360 evolution cycle is structurally valid")
    print("directions=7 angular_bins=360 cells_per_generation=2520 claim_allowed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
