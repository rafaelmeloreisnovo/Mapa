#!/usr/bin/env python3
"""Fail-closed structural validator for GNSS_RUNTIME_RECEIPT_V1.

Stdlib only. This validator does not certify privacy compliance or GNSS capability.
It checks the evidence envelope needed before narrower claims are considered.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCHEMA_VERSION = "GNSS_RUNTIME_RECEIPT_V1"
GATES = {
    "HARDWARE_TO_ANDROID",
    "ANDROID_TO_APP",
    "APP_TO_SERVICE",
    "SERVICE_TO_TOOL",
    "TOOL_TO_ASSISTANT_CONTEXT",
    "ASSISTANT_CONTEXT_TO_MODEL",
    "APP_TO_THIRD_PARTY",
}
GATE_STATES = {"PASS", "FAIL", "TOKEN_VAZIO", "NOT_APPLICABLE"}
FIELD_STATES = {"OBSERVED", "NOT_OBSERVED", "TOKEN_VAZIO", "REDACTED"}


class ContractError(ValueError):
    pass


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{path}: unreadable JSON: {exc}") from exc


def _need_obj(doc, key):
    value = doc.get(key)
    if not isinstance(value, dict):
        raise ContractError(f"{key} must be an object")
    return value


def _need_list(doc, key):
    value = doc.get(key)
    if not isinstance(value, list):
        raise ContractError(f"{key} must be a list")
    return value


def validate(doc):
    required = (
        "schema_version", "receipt_id", "recorded_at", "scope", "device_context",
        "permission_state", "path_gates", "field_observations", "privacy_controls",
        "evidence", "claim_allowed", "F_ok", "F_gap", "F_next",
    )
    missing = [k for k in required if k not in doc]
    if missing:
        raise ContractError(f"missing top-level fields: {missing}")
    if doc["schema_version"] != SCHEMA_VERSION:
        raise ContractError(f"schema_version must be {SCHEMA_VERSION}")
    if doc["claim_allowed"] is not False:
        raise ContractError("claim_allowed must remain false")
    if not isinstance(doc["receipt_id"], str) or not doc["receipt_id"].strip():
        raise ContractError("receipt_id must be non-empty")
    if not isinstance(doc["recorded_at"], str) or not doc["recorded_at"].strip():
        raise ContractError("recorded_at must be non-empty")
    if not isinstance(doc["F_next"], str) or not doc["F_next"].strip():
        raise ContractError("F_next must be non-empty")
    _need_list(doc, "F_ok")
    _need_list(doc, "F_gap")

    scope = _need_obj(doc, "scope")
    if scope.get("authorized_test") is not True:
        raise ContractError("scope.authorized_test must be true")
    for key in ("purpose", "product_or_app", "jurisdiction"):
        if not isinstance(scope.get(key), str) or not scope[key].strip():
            raise ContractError(f"scope.{key} must be non-empty")

    privacy = _need_obj(doc, "privacy_controls")
    if privacy.get("minimized_scope") is not True:
        raise ContractError("privacy_controls.minimized_scope must be true")
    if privacy.get("unrelated_personal_data_excluded") is not True:
        raise ContractError("privacy_controls.unrelated_personal_data_excluded must be true")
    if privacy.get("precise_coordinates_retention") not in {
        "NOT_CAPTURED", "REDACTED", "TEMPORARY_TEST_ONLY", "TOKEN_VAZIO"
    }:
        raise ContractError("invalid precise_coordinates_retention")

    gates = _need_list(doc, "path_gates")
    seen = set()
    for item in gates:
        if not isinstance(item, dict):
            raise ContractError("path_gates items must be objects")
        gate = item.get("gate")
        state = item.get("state")
        if gate not in GATES:
            raise ContractError(f"unknown gate: {gate!r}")
        if gate in seen:
            raise ContractError(f"duplicate gate: {gate}")
        seen.add(gate)
        if state not in GATE_STATES:
            raise ContractError(f"invalid state for {gate}: {state!r}")
        if not isinstance(item.get("evidence_ref"), str) or not item["evidence_ref"].strip():
            raise ContractError(f"{gate}: evidence_ref is required")
    missing_gates = sorted(GATES - seen)
    if missing_gates:
        raise ContractError(f"missing path gates: {missing_gates}")

    fields = _need_list(doc, "field_observations")
    if not fields:
        raise ContractError("field_observations must be non-empty")
    field_seen = set()
    for item in fields:
        if not isinstance(item, dict):
            raise ContractError("field_observations items must be objects")
        field = item.get("field")
        state = item.get("state")
        if not isinstance(field, str) or not field:
            raise ContractError("field name is required")
        if field in field_seen:
            raise ContractError(f"duplicate field observation: {field}")
        field_seen.add(field)
        if state not in FIELD_STATES:
            raise ContractError(f"invalid field state for {field}: {state!r}")
        if not isinstance(item.get("source_boundary"), str) or not item["source_boundary"].strip():
            raise ContractError(f"{field}: source_boundary is required")
        if state in {"OBSERVED", "REDACTED"} and "value_retained" not in item:
            raise ContractError(f"{field}: value_retained required for {state}")

    evidence = _need_obj(doc, "evidence")
    if not isinstance(evidence.get("runtime_receipt_ref"), str) or not evidence["runtime_receipt_ref"].strip():
        raise ContractError("evidence.runtime_receipt_ref is required")
    if evidence.get("hash_state") not in {"RECORDED", "TOKEN_VAZIO"}:
        raise ContractError("invalid evidence.hash_state")
    if evidence.get("provenance_state") not in {"RECORDED", "TOKEN_VAZIO"}:
        raise ContractError("invalid evidence.provenance_state")

    return {
        "receipt_id": doc["receipt_id"],
        "gate_count": len(seen),
        "field_count": len(field_seen),
        "claim_allowed": False,
    }


def self_test():
    base = {
        "schema_version": SCHEMA_VERSION,
        "receipt_id": "TEST-GNSS-001",
        "recorded_at": "2026-08-26T20:51:00-03:00",
        "scope": {
            "purpose": "controlled boundary verification",
            "product_or_app": "test-app",
            "jurisdiction": "Brazil",
            "authorized_test": True,
        },
        "device_context": {
            "android_version": "test",
            "hardware_model_state": "REDACTED",
            "location_services_enabled": True,
        },
        "permission_state": {
            "coarse_location": "GRANTED",
            "fine_location": "GRANTED",
            "precise_location_toggle": "ENABLED",
        },
        "path_gates": [
            {"gate": g, "state": "TOKEN_VAZIO", "evidence_ref": "self-test"}
            for g in sorted(GATES)
        ],
        "field_observations": [
            {"field": "latitude", "state": "REDACTED", "source_boundary": "ANDROID_TO_APP", "value_retained": False},
            {"field": "cn0_dbhz", "state": "TOKEN_VAZIO", "source_boundary": "HARDWARE_TO_ANDROID"},
        ],
        "privacy_controls": {
            "minimized_scope": True,
            "unrelated_personal_data_excluded": True,
            "precise_coordinates_retention": "REDACTED",
            "redaction_applied": True,
        },
        "evidence": {
            "runtime_receipt_ref": "self-test",
            "hash_state": "TOKEN_VAZIO",
            "provenance_state": "RECORDED",
        },
        "claim_allowed": False,
        "F_ok": [],
        "F_gap": ["runtime evidence absent by design in self-test"],
        "F_next": "capture authorized runtime evidence",
    }
    validate(base)

    mutations = []
    x = json.loads(json.dumps(base)); x["claim_allowed"] = True; mutations.append(x)
    x = json.loads(json.dumps(base)); x["scope"]["authorized_test"] = False; mutations.append(x)
    x = json.loads(json.dumps(base)); x["path_gates"] = x["path_gates"][:-1]; mutations.append(x)
    x = json.loads(json.dumps(base)); x["privacy_controls"]["unrelated_personal_data_excluded"] = False; mutations.append(x)
    x = json.loads(json.dumps(base)); x["field_observations"].append(dict(x["field_observations"][0])); mutations.append(x)

    rejected = 0
    for mutation in mutations:
        try:
            validate(mutation)
        except ContractError:
            rejected += 1
    if rejected != len(mutations):
        raise ContractError(f"self-test rejected {rejected}/{len(mutations)} falsifiers")
    return {"positive": 1, "negative_rejected": rejected}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        out = {}
        if args.self_test:
            out["self_test"] = self_test()
        if args.path:
            out["receipt"] = validate(load_json(args.path))
        if not out:
            raise ContractError("provide a receipt path and/or --self-test")
        print(json.dumps({"status": "PASS", **out}, sort_keys=True))
        return 0
    except ContractError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc), "claim_allowed": False}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
