#!/usr/bin/env python3
"""Reconcile existing source gap identities against the effective Gap Atlas.

Only exact evidence is considered:
- source gap_id == Atlas gap_id
- source path == Atlas source_ref path, after an explicit "<authority>: <path>" prefix
- source gap_id appears exactly in Atlas predecessors/successors

The tool emits candidates only. It never binds or creates an Atlas gap_id.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA = "rafaelia.systematic-pragmatic-g4-reconciliation/v1"
ALLOWED_STATUS = {
    "CANDIDATE_EXACT_MATCH",
    "NO_EXACT_EVIDENCE",
    "AMBIGUOUS_EXACT_EVIDENCE",
}


def load_json(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError(f"{path}: expected JSON object")
    return obj


def explicit_ref_path(ref: str) -> str:
    """Return only an explicitly delimited path, never a fuzzy substring."""
    if ": " in ref:
        _, tail = ref.split(": ", 1)
        return tail.strip()
    return ref.strip()


def exact_evidence(
    source_gap_id: str,
    source_paths: list[str],
    atlas_record: dict[str, Any],
) -> list[dict[str, str]]:
    evidence: list[dict[str, str]] = []

    if atlas_record.get("gap_id") == source_gap_id:
        evidence.append(
            {
                "kind": "EXACT_ATLAS_GAP_ID",
                "value": source_gap_id,
            }
        )

    path_set = set(source_paths)
    for raw_ref in atlas_record.get("source_refs", []) or []:
        ref = str(raw_ref)
        normalized = explicit_ref_path(ref)
        if normalized in path_set:
            evidence.append(
                {
                    "kind": "EXACT_SOURCE_PATH_REF",
                    "value": normalized,
                }
            )

    for field in ("predecessors", "successors"):
        values = atlas_record.get(field, []) or []
        for value in values:
            if str(value) == source_gap_id:
                evidence.append(
                    {
                        "kind": f"EXACT_{field.upper()}_ID",
                        "value": source_gap_id,
                    }
                )

    return evidence


def reconcile(
    routing_bindings: dict[str, Any],
    effective_atlas: dict[str, Any],
) -> dict[str, Any]:
    if routing_bindings.get("schema") != "rafaelia.systematic-pragmatic-routing-bindings/v1":
        raise ValueError("unsupported routing bindings schema")
    if routing_bindings.get("claim_allowed") is not False:
        raise ValueError("routing bindings claim boundary is open")
    if effective_atlas.get("schema") != "RAFAELIA_EFFECTIVE_GAP_ATLAS_V1":
        raise ValueError("unsupported effective Atlas schema")
    if effective_atlas.get("claim_allowed") is not False:
        raise ValueError("effective Atlas claim boundary is open")

    atlas_records = effective_atlas.get("records", [])
    if not isinstance(atlas_records, list):
        raise ValueError("effective Atlas records must be an array")

    results: list[dict[str, Any]] = []
    for candidate in routing_bindings.get("gap_binding_candidates", []):
        if not isinstance(candidate, dict):
            raise ValueError("gap binding candidate must be object")
        source_gap_id = candidate.get("source_gap_id")
        if not isinstance(source_gap_id, str) or not source_gap_id:
            raise ValueError("source_gap_id missing")

        source_paths = [
            str(path)
            for path in candidate.get("source_paths", [])
            if isinstance(path, str) and path
        ]
        if not source_paths:
            raise ValueError(f"{source_gap_id}: source_paths missing")

        matches: list[dict[str, Any]] = []
        for atlas_record in atlas_records:
            if not isinstance(atlas_record, dict):
                continue
            evidence = exact_evidence(source_gap_id, source_paths, atlas_record)
            if evidence:
                matches.append(
                    {
                        "atlas_gap_id": atlas_record.get("gap_id"),
                        "effective_state": atlas_record.get("effective_state"),
                        "priority": atlas_record.get("priority"),
                        "evidence": evidence,
                    }
                )

        unique_targets = sorted(
            {
                str(match["atlas_gap_id"])
                for match in matches
                if match.get("atlas_gap_id")
            }
        )
        if len(unique_targets) == 1:
            status = "CANDIDATE_EXACT_MATCH"
            g4_state = "REVIEW_EXACT_CORRESPONDENCE"
        elif not unique_targets:
            status = "NO_EXACT_EVIDENCE"
            g4_state = "BLOCKED_NO_EXACT_EVIDENCE"
        else:
            status = "AMBIGUOUS_EXACT_EVIDENCE"
            g4_state = "BLOCKED_AMBIGUOUS"

        results.append(
            {
                "binding_candidate_id": candidate.get("binding_candidate_id"),
                "source_gap_id": source_gap_id,
                "source_paths": source_paths,
                "source_record_count": candidate.get("record_count"),
                "status": status,
                "candidate_atlas_gap_ids": unique_targets,
                "exact_evidence": matches,
                "g4": {
                    "state": g4_state,
                    "atlas_gap_id": "TOKEN_VAZIO",
                    "auto_create_gap_id": False,
                    "human_or_governed_confirmation_required": True,
                },
                "claim_allowed": False,
            }
        )

    by_status: dict[str, int] = {key: 0 for key in sorted(ALLOWED_STATUS)}
    for row in results:
        by_status[row["status"]] += 1

    return {
        "schema": SCHEMA,
        "claim_allowed": False,
        "policy": {
            "fuzzy_matching_forbidden": True,
            "exact_evidence_is_candidate_not_binding": True,
            "source_gap_id_is_not_atlas_gap_id_by_assumption": True,
            "auto_create_gap_id": False,
        },
        "summary": {
            "source_gap_candidates": len(results),
            "effective_atlas_records": len(atlas_records),
            "by_status": by_status,
        },
        "reconciliation": sorted(results, key=lambda row: row["source_gap_id"]),
    }


def validate_output(payload: dict[str, Any]) -> None:
    if payload.get("claim_allowed") is not False:
        raise ValueError("output claim boundary is open")
    rows = payload.get("reconciliation", [])
    if payload.get("summary", {}).get("source_gap_candidates") != len(rows):
        raise ValueError("summary/source candidate count mismatch")
    for row in rows:
        if row.get("status") not in ALLOWED_STATUS:
            raise ValueError(f"invalid status for {row.get('source_gap_id')}")
        g4 = row.get("g4", {})
        if g4.get("atlas_gap_id") != "TOKEN_VAZIO":
            raise ValueError(f"{row.get('source_gap_id')}: automatic binding detected")
        if g4.get("auto_create_gap_id") is not False:
            raise ValueError(f"{row.get('source_gap_id')}: automatic id creation detected")
        if g4.get("human_or_governed_confirmation_required") is not True:
            raise ValueError(f"{row.get('source_gap_id')}: confirmation gate missing")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--routing-bindings", type=Path, required=True)
    ap.add_argument("--effective-atlas", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    try:
        payload = reconcile(
            load_json(args.routing_bindings),
            load_json(args.effective_atlas),
        )
        validate_output(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"g4-reconcile: {exc}")
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
