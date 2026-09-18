#!/usr/bin/env python3
"""Materialize governed G4 append/link proposals without mutating the Gap Atlas.

The proposal state is derived only from already observed evidence:
- exact match candidates -> PROPOSE_LINK_EXISTING
- no exact evidence + complete bounded source identity -> PROPOSE_APPEND_NEW
- ambiguous or incomplete evidence -> NEEDS_MORE_EVIDENCE

All Atlas ids remain TOKEN_VAZIO until a governed binding/allocation event.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "rafaelia.systematic-pragmatic-g4-proposals/v1"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected object")
    return value


def walk_items(value: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key), child
            yield from walk_items(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_items(child)


def first_value(obj: dict[str, Any], names: tuple[str, ...]) -> Any:
    for name in names:
        if name in obj:
            return obj[name]
    return None


def owner_value(obj: dict[str, Any]) -> Any:
    return first_value(obj, ("owner_authority", "owner", "authority"))


def state_value(obj: dict[str, Any]) -> Any:
    return first_value(obj, ("status", "state", "uncertainty_state"))


def string_leaves(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, str) and value:
        out.append(value)
    elif isinstance(value, dict):
        for child in value.values():
            out.extend(string_leaves(child))
    elif isinstance(value, list):
        for child in value:
            out.extend(string_leaves(child))
    return out


def next_gate_values(obj: dict[str, Any]) -> list[str]:
    wanted = {
        "closure_gate",
        "next_probe",
        "next_verifiable_step",
        "next_review_gate",
        "falsifier",
    }
    out: list[str] = []
    for key, value in walk_items(obj):
        if key in wanted:
            out.extend(string_leaves(value))
    return sorted(set(out))


def read_sources(repo_root: Path, paths: list[str]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for rel in paths:
        path = repo_root / rel
        raw = path.read_text(encoding="utf-8")
        obj = json.loads(raw)
        if not isinstance(obj, dict):
            raise ValueError(f"{rel}: source record must be object")
        out.append(
            {
                "path": rel,
                "object": obj,
                "claim_allowed": obj.get("claim_allowed"),
                "owner": owner_value(obj),
                "state": state_value(obj),
                "next_gates": next_gate_values(obj),
            }
        )
    return out


def source_completeness(records: list[dict[str, Any]]) -> dict[str, Any]:
    record_count = len(records)
    claim_false = sum(1 for row in records if row["claim_allowed"] is False)
    owner_records = sum(
        1 for row in records if row["owner"] not in (None, "", [], {})
    )
    gate_records = sum(1 for row in records if row["next_gates"])
    owners = sorted(
        {
            json.dumps(row["owner"], ensure_ascii=False, sort_keys=True)
            for row in records
            if row["owner"] not in (None, "", [], {})
        }
    )
    states = sorted(
        {
            json.dumps(row["state"], ensure_ascii=False, sort_keys=True)
            for row in records
            if row["state"] is not None
        }
    )
    gates = sorted(
        {
            gate
            for row in records
            for gate in row["next_gates"]
        }
    )
    missing: list[str] = []
    if claim_false != record_count:
        missing.append("claim_allowed_false_for_every_source_record")
    if owner_records == 0:
        missing.append("owner_or_authority")
    if gate_records != record_count:
        missing.append("closure_or_next_gate_for_every_source_record")
    return {
        "record_count": record_count,
        "claim_allowed_false_records": claim_false,
        "owner_records": owner_records,
        "closure_or_next_gate_records": gate_records,
        "owner_values": owners,
        "source_state_values": states,
        "source_next_gates": gates,
        "missing_required_evidence": missing,
        "bounded_source_identity_complete": not missing,
    }


def build_proposals(
    reconciliation: dict[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    if reconciliation.get("schema") != "rafaelia.systematic-pragmatic-g4-reconciliation/v1":
        raise ValueError("unsupported reconciliation schema")
    if reconciliation.get("claim_allowed") is not False:
        raise ValueError("reconciliation claim boundary is open")

    proposals: list[dict[str, Any]] = []
    for row in reconciliation.get("reconciliation", []):
        if not isinstance(row, dict):
            raise ValueError("reconciliation row must be object")
        source_gap_id = row.get("source_gap_id")
        paths = [
            str(value)
            for value in row.get("source_paths", [])
            if isinstance(value, str) and value
        ]
        if not isinstance(source_gap_id, str) or not source_gap_id or not paths:
            raise ValueError("source identity/path missing")

        records = read_sources(repo_root, paths)
        completeness = source_completeness(records)
        status = row.get("status")
        candidates = list(row.get("candidate_atlas_gap_ids", []) or [])

        if status == "CANDIDATE_EXACT_MATCH" and len(candidates) == 1:
            proposal_action = "PROPOSE_LINK_EXISTING"
            proposal_state = "REVIEW_REQUIRED"
        elif (
            status == "NO_EXACT_EVIDENCE"
            and completeness["bounded_source_identity_complete"]
        ):
            proposal_action = "PROPOSE_APPEND_NEW"
            proposal_state = "REVIEW_REQUIRED"
        else:
            proposal_action = "NEEDS_MORE_EVIDENCE"
            proposal_state = "BLOCKED"

        proposals.append(
            {
                "proposal_id": "G4P-" + source_gap_id,
                "source_gap_id": source_gap_id,
                "source_paths": paths,
                "reconciliation_status": status,
                "candidate_atlas_gap_ids": candidates,
                "proposal_action": proposal_action,
                "proposal_state": proposal_state,
                "proposed_atlas_gap_id": "TOKEN_VAZIO",
                "source_evidence": completeness,
                "required_governed_fields": {
                    "atlas_gap_id": "TOKEN_VAZIO_GOVERNED_ALLOCATION_OR_LINK",
                    "artifact_id": "TOKEN_VAZIO",
                    "provider": "TOKEN_VAZIO",
                    "scope": "TOKEN_VAZIO",
                    "gap_class": "TOKEN_VAZIO",
                    "priority": "TOKEN_VAZIO",
                    "known": "TOKEN_VAZIO",
                    "unknown": "TOKEN_VAZIO",
                    "authority_required": completeness["owner_values"],
                    "evidence_required": "TOKEN_VAZIO",
                    "next_gate_candidates": completeness["source_next_gates"],
                },
                "g4": {
                    "state": "PROPOSAL_ONLY",
                    "atlas_mutation_allowed": False,
                    "auto_create_gap_id": False,
                    "governed_review_required": True,
                },
                "claim_allowed": False,
            }
        )

    by_action: dict[str, int] = {}
    for row in proposals:
        action = row["proposal_action"]
        by_action[action] = by_action.get(action, 0) + 1

    return {
        "schema": SCHEMA,
        "claim_allowed": False,
        "atlas_mutation_allowed": False,
        "policy": {
            "proposal_is_not_binding": True,
            "proposal_is_not_append": True,
            "missing_fields_stay_token_vazio": True,
            "auto_create_gap_id": False,
        },
        "summary": {
            "proposals": len(proposals),
            "by_action": dict(sorted(by_action.items())),
        },
        "proposals": sorted(proposals, key=lambda row: row["source_gap_id"]),
    }


def validate(payload: dict[str, Any]) -> None:
    if payload.get("claim_allowed") is not False:
        raise ValueError("claim boundary opened")
    if payload.get("atlas_mutation_allowed") is not False:
        raise ValueError("Atlas mutation must remain disabled")
    rows = payload.get("proposals", [])
    if payload.get("summary", {}).get("proposals") != len(rows):
        raise ValueError("proposal count mismatch")
    for row in rows:
        if row.get("proposed_atlas_gap_id") != "TOKEN_VAZIO":
            raise ValueError(f"{row.get('source_gap_id')}: premature Atlas id")
        if row.get("g4", {}).get("atlas_mutation_allowed") is not False:
            raise ValueError(f"{row.get('source_gap_id')}: Atlas mutation enabled")
        if row.get("g4", {}).get("auto_create_gap_id") is not False:
            raise ValueError(f"{row.get('source_gap_id')}: automatic gap id enabled")
        if row.get("claim_allowed") is not False:
            raise ValueError(f"{row.get('source_gap_id')}: claim boundary opened")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reconciliation", type=Path, required=True)
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    try:
        payload = build_proposals(
            load_json(args.reconciliation),
            args.repo_root,
        )
        validate(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"g4-proposals: {exc}")
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
