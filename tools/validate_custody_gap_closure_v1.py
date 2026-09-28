#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "data/governance/custody/06_GAPS/CUSTODY_GAP_CLOSURE_MODEL_V1.json"

ALLOWED_STATES = {
    "IMPLEMENTED_UNTESTED", "PASS", "FAIL", "ROUTE_STATE_BLOCKED",
    "TOKEN_VAZIO", "NOT_RUN", "AUDIT",
}
EXTERNAL_CLASSES = {
    "PROVIDER_CONFIGURATION", "SERVER_ENFORCEMENT", "SECRET_BOUND", "HUMAN_REVIEW",
}


def validate(data: dict) -> list[str]:
    errors: list[str] = []

    def req(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    req(data.get("schema_version") == "rafaelia.custody-gap-closure-model/v1", "schema_version mismatch")
    req(data.get("claim_allowed") is False, "model claim_allowed must remain false")

    gaps = data.get("gaps")
    req(isinstance(gaps, list) and bool(gaps), "gaps must be a non-empty list")
    if not isinstance(gaps, list):
        return errors

    ids = [g.get("gap_id") for g in gaps if isinstance(g, dict)]
    req(len(ids) == len(set(ids)), "gap ids must be unique")

    index = {g.get("gap_id"): g for g in gaps if isinstance(g, dict)}
    for gap_id, gap in index.items():
        req(isinstance(gap_id, str) and bool(gap_id), "gap_id must be non-empty")
        req(gap.get("state") in ALLOWED_STATES, f"{gap_id}: invalid state")
        req(gap.get("claim_allowed") is False, f"{gap_id}: claim_allowed must remain false")
        for field in ("closure_authority", "closure_action"):
            req(isinstance(gap.get(field), str) and bool(gap.get(field).strip()), f"{gap_id}: {field} required")
        for field in ("known", "evidence_required", "source_refs"):
            value = gap.get(field)
            req(isinstance(value, list) and bool(value) and all(isinstance(x, str) and x.strip() for x in value),
                f"{gap_id}: {field} must be non-empty string list")
        for dep in gap.get("depends_on", []):
            req(dep in index, f"{gap_id}: unknown dependency {dep}")
        if gap.get("class") in EXTERNAL_CLASSES:
            req(gap.get("state") == "ROUTE_STATE_BLOCKED",
                f"{gap_id}: external-authority gap must remain ROUTE_STATE_BLOCKED until external evidence exists")

    c09 = index.get("CUST-20260927-001", {})
    req(c09.get("state") in {"IMPLEMENTED_UNTESTED", "PASS"},
        "CUST-20260927-001 must be implemented or passed, never silently closed")

    historical = index.get("CUST-20260927-007", {})
    req(historical.get("required_now") is False, "historical post-merge execution gap must not block current successor")
    req(historical.get("state") == "NOT_RUN", "historical non-execution must remain NOT_RUN")

    summary = data.get("summary", {})
    internal = sum(1 for g in gaps if isinstance(g, dict) and g.get("class") in {"MODEL_AUTHORITY", "CODE_DEFECT"})
    external = sum(1 for g in gaps if isinstance(g, dict) and g.get("class") in EXTERNAL_CLASSES)
    historical_count = sum(1 for g in gaps if isinstance(g, dict) and g.get("class") == "HISTORICAL_EVIDENCE")
    req(summary.get("internal_fixable") == internal, "summary internal_fixable mismatch")
    req(summary.get("external_blocked") == external, "summary external_blocked mismatch")
    req(summary.get("historical_nonretroactive") == historical_count, "summary historical_nonretroactive mismatch")

    return errors


def main() -> int:
    data = json.loads(MODEL.read_text(encoding="utf-8"))
    errors = validate(data)
    result = {
        "state": "PASS" if not errors else "FAIL",
        "model": str(MODEL.relative_to(ROOT)),
        "gap_count": len(data.get("gaps", [])),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
