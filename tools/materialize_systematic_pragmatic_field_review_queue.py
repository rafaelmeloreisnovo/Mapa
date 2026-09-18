#!/usr/bin/env python3
"""Materialize field-level review/acquisition work from identity-semantics enrichment."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA = "rafaelia.systematic-pragmatic-field-review-queue/v1"
FIELD_PRIORITY = {
    "artifact_id": "P0",
    "provider": "P0",
    "scope": "P1",
    "evidence_required": "P1",
}
STATE_ACTION = {
    "EXACT_STRUCTURED": "REVIEW_STRUCTURED_EVIDENCE",
    "NORMALIZED_ENUM_CANDIDATE": "REVIEW_NORMALIZATION",
    "ALIAS_CANDIDATE": "REVIEW_ALIAS_MAPPING",
    "STRUCTURED_DERIVATION_CANDIDATE": "REVIEW_STRUCTURED_DERIVATION",
    "CONFLICT": "RECONCILE_CONFLICT",
    "TOKEN_VAZIO": "ACQUIRE_EXPLICIT_EVIDENCE",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected object")
    return value


def work_id(source_gap_id: str, field: str) -> str:
    digest = hashlib.sha256(f"{source_gap_id}\0{field}".encode("utf-8")).hexdigest()[:16]
    return "G4W-" + digest


def build(enrichment: dict[str, Any]) -> dict[str, Any]:
    if enrichment.get("schema") != "rafaelia.systematic-pragmatic-identity-semantics-enrichment/v1":
        raise ValueError("unsupported enrichment schema")
    if enrichment.get("claim_allowed") is not False:
        raise ValueError("enrichment claim boundary is open")
    if enrichment.get("atlas_mutation_allowed") is not False:
        raise ValueError("enrichment permits Atlas mutation")

    items: list[dict[str, Any]] = []
    by_action: dict[str, int] = {}
    by_field: dict[str, int] = {}
    by_priority: dict[str, int] = {}

    for row in enrichment.get("enrichments", []):
        source_gap_id = row.get("source_gap_id")
        if not isinstance(source_gap_id, str) or not source_gap_id:
            raise ValueError("source_gap_id missing")
        target_fields = row.get("target_fields")
        if not isinstance(target_fields, dict):
            raise ValueError(f"{source_gap_id}: target_fields missing")

        for field, priority in FIELD_PRIORITY.items():
            evidence = target_fields.get(field)
            if not isinstance(evidence, dict):
                raise ValueError(f"{source_gap_id}:{field}: evidence missing")
            state = evidence.get("state")
            action = STATE_ACTION.get(str(state))
            if action is None:
                raise ValueError(f"{source_gap_id}:{field}: unsupported state {state!r}")

            item = {
                "work_id": work_id(source_gap_id, field),
                "source_gap_id": source_gap_id,
                "field": field,
                "priority": priority,
                "evidence_state": state,
                "required_action": action,
                "candidate_value": evidence.get("value", "TOKEN_VAZIO"),
                "evidence_refs": evidence.get("evidence", []),
                "governance": {
                    "state": "PENDING_FIELD_REVIEW",
                    "promotion_allowed": False,
                    "atlas_mutation_allowed": False,
                    "auto_create_gap_id": False,
                },
                "claim_allowed": False,
            }
            items.append(item)
            by_action[action] = by_action.get(action, 0) + 1
            by_field[field] = by_field.get(field, 0) + 1
            by_priority[priority] = by_priority.get(priority, 0) + 1

    return {
        "schema": SCHEMA,
        "claim_allowed": False,
        "atlas_mutation_allowed": False,
        "policy": {
            "candidate_requires_governed_review": True,
            "token_vazio_requires_explicit_evidence": True,
            "field_review_does_not_allocate_atlas_id": True,
            "promotion_allowed": False,
        },
        "summary": {
            "work_items": len(items),
            "by_action": dict(sorted(by_action.items())),
            "by_field": dict(sorted(by_field.items())),
            "by_priority": dict(sorted(by_priority.items())),
        },
        "items": sorted(
            items,
            key=lambda item: (
                item["priority"],
                item["field"],
                item["source_gap_id"],
            ),
        ),
    }


def validate(payload: dict[str, Any]) -> None:
    if payload.get("claim_allowed") is not False:
        raise ValueError("queue claim boundary opened")
    if payload.get("atlas_mutation_allowed") is not False:
        raise ValueError("queue permits Atlas mutation")
    items = payload.get("items", [])
    if payload.get("summary", {}).get("work_items") != len(items):
        raise ValueError("work item count mismatch")
    seen: set[str] = set()
    for item in items:
        wid = item.get("work_id")
        if not isinstance(wid, str) or not wid or wid in seen:
            raise ValueError("invalid/duplicate work_id")
        seen.add(wid)
        if item.get("claim_allowed") is not False:
            raise ValueError(f"{wid}: claim boundary opened")
        gov = item.get("governance", {})
        if gov.get("promotion_allowed") is not False:
            raise ValueError(f"{wid}: premature promotion")
        if gov.get("atlas_mutation_allowed") is not False:
            raise ValueError(f"{wid}: Atlas mutation enabled")
        if gov.get("auto_create_gap_id") is not False:
            raise ValueError(f"{wid}: automatic gap ID enabled")
        if (
            item.get("evidence_state") == "TOKEN_VAZIO"
            and item.get("candidate_value") != "TOKEN_VAZIO"
        ):
            raise ValueError(f"{wid}: TOKEN_VAZIO carries unsupported candidate")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--enrichment", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    try:
        payload = build(load_json(args.enrichment))
        validate(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"field-review-queue: {exc}")
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload["summary"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
