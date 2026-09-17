#!/usr/bin/env python3
"""Validate RAFAELIA Operational Excellence Gate V1 using only stdlib.

Fail-closed validator: verifies the control contract itself and optionally validates a
work-unit receipt against the contract. It does not promote claims.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_GUARDS = {
    "PROVENANCE",
    "CONTEXT",
    "EVIDENCE",
    "CONTRADICTION",
    "UNCERTAINTY",
    "REPRODUCTION",
    "ROLLBACK",
}
REQUIRED_FIRST_LINE = {"DIGNITY", "CHILD_SAFETY", "PRIVACY", "AUTHORITY", "TRUTH_GAP"}
ALLOWED_GATE_STATES = {"PASS", "FAIL", "NOT_APPLICABLE"}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        obj = json.load(fh)
    if not isinstance(obj, dict):
        raise ValueError("top-level JSON must be object")
    return obj


def validate_contract(c: dict) -> list[str]:
    errors: list[str] = []
    if c.get("schema_version") != "rafaelia.operational-excellence-gate/v1":
        errors.append("bad schema_version")
    if c.get("claim_allowed") is not False:
        errors.append("contract claim_allowed must be false")
    objective = c.get("objective_boundary", {})
    if objective.get("human_authorized_objective_required") is not True:
        errors.append("human authorization must be required")
    if objective.get("autonomous_goal_creation_allowed") is not False:
        errors.append("autonomous goal creation must be false")

    first = {g.get("id") for g in c.get("first_line", {}).get("gates", [])}
    if first != REQUIRED_FIRST_LINE:
        errors.append(f"first-line gate set mismatch: {sorted(first)}")

    guards = {g.get("id") for g in c.get("seven_guards", [])}
    if guards != REQUIRED_GUARDS:
        errors.append(f"seven-guard set mismatch: {sorted(guards)}")

    ids = c.get("identity_separation", [])
    required_identity = {
        "SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM",
        "TOKEN_ID != OCCURRENCE_ID != SENSE_VERSION != CLAIM",
        "SOURCE_ACTOR != AUTHORSHIP_AUTHORITY != SENSE_AUTHORITY != CLAIM_AUTHORITY",
        "TOKEN_VAZIO != 0",
        "RECOVERY_CANDIDATE != TRUTH != AUTHORSHIP != CLAIM",
    }
    if not required_identity.issubset(set(ids)):
        errors.append("identity-separation invariants incomplete")

    if c.get("six_sigma_boundary") != "NO_STATISTICAL_SIGMA_CLAIM_WITHOUT_DEFECT_OPPORTUNITY_METRICS":
        errors.append("Six Sigma statistical-claim boundary missing")
    return errors


def validate_receipt(c: dict, r: dict) -> list[str]:
    errors: list[str] = []
    required = c.get("receipt_required_fields", [])
    for field in required:
        if field not in r:
            errors.append(f"missing receipt field: {field}")

    gates = r.get("gates", {})
    if not isinstance(gates, dict):
        errors.append("gates must be object")
        gates = {}
    for gate in REQUIRED_FIRST_LINE:
        state = gates.get(gate, "TOKEN_VAZIO")
        if state not in ALLOWED_GATE_STATES:
            errors.append(f"{gate} unresolved or invalid: {state}")

    guards = r.get("seven_guards", {})
    if not isinstance(guards, dict):
        errors.append("seven_guards must be object")
        guards = {}
    for guard in REQUIRED_GUARDS:
        value = guards.get(guard)
        if value in (None, "", [], {}):
            errors.append(f"guard missing/empty: {guard}")

    # Promotion remains fail-closed unless every applicable first-line gate passes.
    if r.get("promotion_requested") is True:
        for gate, state in gates.items():
            if gate in REQUIRED_FIRST_LINE and state not in {"PASS", "NOT_APPLICABLE"}:
                errors.append(f"promotion blocked by {gate}={state}")
        if r.get("claim_allowed") is not False:
            errors.append("receipt claim_allowed must remain false in v1")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default="data/contracts/operational-excellence-gate.v1.json")
    parser.add_argument("--receipt")
    args = parser.parse_args()

    try:
        contract = load_json(Path(args.contract))
        errors = validate_contract(contract)
        if args.receipt:
            receipt = load_json(Path(args.receipt))
            errors.extend(validate_receipt(contract, receipt))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: operational excellence gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
