#!/usr/bin/env python3
"""RAFAELIA Operational Gap Assurance V1.

Stdlib-only validator and prioritizer for F_gap, TOKEN_VAZIO, uncertainty,
incident/near-miss and maintenance records.

This is an engineering-safety analogy inspired by repeatable safety-management
practices. It does NOT assert FAA/ICAO/NTSB certification, approval, compliance
or regulatory equivalence.

Core invariant:
    VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM

Open gaps remain claim_allowed=false until their closure gate is supported by
traceable evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ACTIONS = {
    "DETECTIVE",
    "PREVENTIVE",
    "PRECAUTIONARY",
    "ADAPTIVE",
    "CORRECTIVE",
    "MAINTENANCE",
    "INCIDENT_INVESTIGATION",
    "SAFETY_ASSURANCE",
    "LEARNING_ANTI_RECURRENCE",
}

OPEN_STATES = {
    "F_GAP",
    "TOKEN_VAZIO",
    "UNCERTAINTY",
    "BLOCKED",
    "CONTRADICTION",
    "REGRESSION",
    "NEAR_MISS",
    "INCIDENT",
}

CLOSED_STATE = "CLOSED_BY_EVIDENCE"

REQUIRED = {
    "schema_version",
    "gap_id",
    "status",
    "source_pointer",
    "owner_authority",
    "affected_routes",
    "observed_at",
    "provenance",
    "evidence_for",
    "evidence_against",
    "uncertainty_state",
    "urgency",
    "necessity",
    "impact",
    "unlock",
    "risk",
    "detectability",
    "recurrence_risk",
    "information_gain",
    "forgetting_risk",
    "failure_mode",
    "falsifier",
    "next_probe",
    "mitigation",
    "closure_gate",
    "review_or_expiry",
    "claim_allowed",
    "action_categories",
}

RANGE_FIELDS = {
    "urgency",
    "necessity",
    "impact",
    "unlock",
    "risk",
    "detectability",
    "recurrence_risk",
    "information_gain",
    "forgetting_risk",
}


def _nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return value is not None


def priority_score(record: dict[str, Any]) -> int:
    """Priority = impact × unlock × risk × urgency × information_gain × forgetting_risk.

    Zero is meaningful: a zero axis makes the product zero rather than being
    silently promoted. Necessity, detectability and recurrence_risk remain
    explicit decision axes but do not alter this canonical product.
    """
    keys = ("impact", "unlock", "risk", "urgency", "information_gain", "forgetting_risk")
    out = 1
    for key in keys:
        out *= int(record.get(key, 0))
    return out


def validate(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    missing = sorted(k for k in REQUIRED if k not in record)
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))

    if record.get("schema_version") != "rafaelia.operational-gap-assurance/v1":
        errors.append("schema_version must be rafaelia.operational-gap-assurance/v1")

    status = record.get("status")
    if status not in OPEN_STATES | {CLOSED_STATE}:
        errors.append(f"invalid status: {status!r}")

    for key in RANGE_FIELDS:
        value = record.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 3:
            errors.append(f"{key} must be integer 0..3")

    for key in ("gap_id", "source_pointer", "owner_authority", "observed_at", "uncertainty_state",
                "failure_mode", "falsifier", "next_probe", "review_or_expiry"):
        if not _nonempty(record.get(key)):
            errors.append(f"{key} must be non-empty")

    for key in ("affected_routes", "provenance", "evidence_for", "evidence_against", "action_categories"):
        if not isinstance(record.get(key), list):
            errors.append(f"{key} must be a list")

    actions = set(record.get("action_categories") or [])
    unknown_actions = sorted(actions - ACTIONS)
    if unknown_actions:
        errors.append("unknown action categories: " + ", ".join(unknown_actions))
    if not actions:
        errors.append("at least one action category is required")

    mitigation = record.get("mitigation")
    if not isinstance(mitigation, dict) or not mitigation:
        errors.append("mitigation must be a non-empty object")

    closure = record.get("closure_gate")
    if not isinstance(closure, dict):
        errors.append("closure_gate must be an object")
        closure = {}
    else:
        for key in ("criterion", "evidence_needed", "falsifier", "result"):
            if key not in closure:
                errors.append(f"closure_gate.{key} is required")

    claim_allowed = record.get("claim_allowed")
    if not isinstance(claim_allowed, bool):
        errors.append("claim_allowed must be boolean")
    if status in OPEN_STATES and claim_allowed is not False:
        errors.append("open gap states require claim_allowed=false")
    if status == CLOSED_STATE and claim_allowed is True:
        if closure.get("result") != "PASS":
            errors.append("claim_allowed=true requires closure_gate.result=PASS")
        if not _nonempty(closure.get("evidence")):
            errors.append("claim_allowed=true requires closure_gate.evidence")

    if "DETECTIVE" in actions:
        detector = record.get("detector")
        if not isinstance(detector, dict):
            errors.append("DETECTIVE requires detector object")
        else:
            for key in ("signal", "threshold", "false_positive", "false_negative", "evidence_needed"):
                if not _nonempty(detector.get(key)):
                    errors.append(f"detector.{key} is required for DETECTIVE")

    if "PRECAUTIONARY" in actions:
        if not isinstance(mitigation, dict) or mitigation.get("fail_closed") is not True:
            errors.append("PRECAUTIONARY requires mitigation.fail_closed=true")
        if claim_allowed is not False and status != CLOSED_STATE:
            errors.append("PRECAUTIONARY open record cannot allow claim")

    if "ADAPTIVE" in actions:
        adaptive = record.get("adaptive_control")
        if not isinstance(adaptive, dict):
            errors.append("ADAPTIVE requires adaptive_control object")
        else:
            for key in ("baseline", "delta", "justification", "rollback", "retest"):
                if not _nonempty(adaptive.get(key)):
                    errors.append(f"adaptive_control.{key} is required for ADAPTIVE")

    if "CORRECTIVE" in actions:
        corrective = record.get("corrective_control")
        if not isinstance(corrective, dict):
            errors.append("CORRECTIVE requires corrective_control object")
        else:
            for key in ("symptom", "mechanism_hypothesis", "before_after_test"):
                if not _nonempty(corrective.get(key)):
                    errors.append(f"corrective_control.{key} is required for CORRECTIVE")

    if "MAINTENANCE" in actions:
        maintenance = record.get("maintenance")
        if not isinstance(maintenance, dict):
            errors.append("MAINTENANCE requires maintenance object")
        else:
            mclass = maintenance.get("class")
            if mclass not in {"PREVENTIVE", "CONDITION_BASED", "CORRECTIVE"}:
                errors.append("maintenance.class must be PREVENTIVE, CONDITION_BASED or CORRECTIVE")
            for key in ("asset", "condition_or_interval", "verification"):
                if not _nonempty(maintenance.get(key)):
                    errors.append(f"maintenance.{key} is required")
            if mclass == "CONDITION_BASED" and not _nonempty(maintenance.get("measured_condition")):
                errors.append("CONDITION_BASED maintenance requires measured_condition")

    if "INCIDENT_INVESTIGATION" in actions:
        incident = record.get("incident_investigation")
        if not isinstance(incident, dict):
            errors.append("INCIDENT_INVESTIGATION requires incident_investigation object")
        else:
            for key in ("trigger", "facts", "timeline", "configuration", "recent_changes",
                        "competing_mechanisms", "contributing_factors", "recommendations"):
                if not _nonempty(incident.get(key)):
                    errors.append(f"incident_investigation.{key} is required")
            if incident.get("blame_assignment") not in (None, False):
                errors.append("incident investigation must be fact/mechanism oriented, not blame oriented")

    if "SAFETY_ASSURANCE" in actions:
        assurance = record.get("safety_assurance")
        if not isinstance(assurance, dict):
            errors.append("SAFETY_ASSURANCE requires safety_assurance object")
        else:
            for key in ("data_acquisition", "analysis", "system_reassessment", "corrective_trigger"):
                if not _nonempty(assurance.get(key)):
                    errors.append(f"safety_assurance.{key} is required")

    if "LEARNING_ANTI_RECURRENCE" in actions:
        learning = record.get("learning")
        if not isinstance(learning, dict):
            errors.append("LEARNING_ANTI_RECURRENCE requires learning object")
        else:
            for key in ("reusable_control", "index_or_test", "recurrence_check"):
                if not _nonempty(learning.get(key)):
                    errors.append(f"learning.{key} is required")

    if record.get("uncertainty_state") == "NONE" and status != CLOSED_STATE:
        errors.append("open gaps cannot silently set uncertainty_state=NONE")

    return errors


def build_report(record: dict[str, Any]) -> dict[str, Any]:
    errors = validate(record)
    return {
        "schema_version": "rafaelia.operational-gap-assurance-report/v1",
        "gap_id": record.get("gap_id"),
        "valid": not errors,
        "errors": errors,
        "priority_score": priority_score(record),
        "status": record.get("status"),
        "claim_allowed": record.get("claim_allowed"),
        "actions": record.get("action_categories", []),
        "next_probe": record.get("next_probe"),
        "closure_result": (record.get("closure_gate") or {}).get("result"),
    }


def self_test() -> int:
    good = {
        "schema_version": "rafaelia.operational-gap-assurance/v1",
        "gap_id": "gap:selftest:001",
        "status": "TOKEN_VAZIO",
        "source_pointer": "fixture://selftest/001",
        "owner_authority": "Mapa",
        "affected_routes": ["R5", "R11"],
        "observed_at": "2026-08-19T00:00:00-03:00",
        "provenance": [{"source": "fixture", "role": "self_test"}],
        "evidence_for": [],
        "evidence_against": [],
        "uncertainty_state": "EVIDENCE_INSUFFICIENT",
        "urgency": 3,
        "necessity": 3,
        "impact": 3,
        "unlock": 3,
        "risk": 2,
        "detectability": 2,
        "recurrence_risk": 2,
        "information_gain": 3,
        "forgetting_risk": 2,
        "failure_mode": "receipt without locally recomputed artifact hash",
        "falsifier": "recompute the artifact hash and compare against the expected identity",
        "next_probe": "obtain artifact bytes and recompute SHA-256 locally",
        "mitigation": {"fail_closed": True, "rollback": "retain previous state"},
        "closure_gate": {
            "criterion": "local artifact identity reproduced",
            "evidence_needed": "artifact bytes + local SHA-256 receipt",
            "falsifier": "mismatching local digest",
            "result": "TOKEN_VAZIO",
        },
        "review_or_expiry": "re-evaluate on next artifact/version change",
        "claim_allowed": False,
        "action_categories": ["DETECTIVE", "PRECAUTIONARY", "SAFETY_ASSURANCE"],
        "detector": {
            "signal": "publisher checksum exists but local_sha256 is TOKEN_VAZIO",
            "threshold": "any occurrence",
            "false_positive": "artifact intentionally unavailable",
            "false_negative": "unindexed artifact",
            "evidence_needed": "artifact locator and checksum metadata",
        },
        "safety_assurance": {
            "data_acquisition": "read receipt and artifact metadata",
            "analysis": "compare published and locally recomputed identities",
            "system_reassessment": "re-evaluate route state after verification",
            "corrective_trigger": "digest mismatch or missing artifact",
        },
    }

    good_errors = validate(good)
    if good_errors:
        print(json.dumps({"self_test": "FAIL", "case": "good", "errors": good_errors}, indent=2))
        return 1

    bad = dict(good)
    bad["claim_allowed"] = True
    bad_errors = validate(bad)
    if not any("claim_allowed=false" in e for e in bad_errors):
        print(json.dumps({"self_test": "FAIL", "case": "bad_claim_gate", "errors": bad_errors}, indent=2))
        return 1

    print(json.dumps({"self_test": "PASS", "priority_score": priority_score(good)}, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", nargs="?", help="JSON record to validate")
    parser.add_argument("--write-report", help="write deterministic JSON report")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()
    if not args.record:
        parser.error("record is required unless --self-test is used")

    record = json.loads(Path(args.record).read_text(encoding="utf-8"))
    report = build_report(record)
    payload = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.write_report:
        Path(args.write_report).write_text(payload, encoding="utf-8")
    sys.stdout.write(payload)
    return 0 if report["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
