#!/usr/bin/env python3
"""Build canonical-field completion worksheets for governed G4 append proposals.

This tool does not create Atlas records. It classifies evidence for canonical fields as:
- EXACT_SOURCE_FIELD
- SOURCE_ALIAS_CANDIDATE
- MULTI_SOURCE_REVIEW
- TOKEN_VAZIO

Alias candidates are explicitly non-equivalent until governed review.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "rafaelia.systematic-pragmatic-canonical-completion/v1"
FIELD_STATES = {
    "EXACT_SOURCE_FIELD",
    "SOURCE_ALIAS_CANDIDATE",
    "MULTI_SOURCE_REVIEW",
    "TOKEN_VAZIO",
}

CANONICAL_FIELDS = (
    "artifact_id",
    "provider",
    "scope",
    "gap_class",
    "priority",
    "known",
    "unknown",
    "authority_required",
    "evidence_required",
    "next_gate",
)

ALIASES = {
    "gap_class": ("classification",),
    "priority": ("urgency",),
    "known": ("evidence_for", "F_ok"),
    "unknown": ("F_gap",),
    "next_gate": (
        "next_verifiable_step",
        "next_review_gate",
        "next_probe",
        "F_next",
        "closure_gate",
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError(f"{path}: expected object")
    return obj


def normalize_value(value: Any) -> Any:
    if isinstance(value, tuple):
        return list(value)
    return value


def canonical_key(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def collect_nested_aliases(obj: dict[str, Any], field: str) -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    if field == "known":
        ep = obj.get("epistemic_boundary")
        if isinstance(ep, dict) and ep.get("proven_scoped") not in (None, "", [], {}):
            out.append(("epistemic_boundary.proven_scoped", ep["proven_scoped"]))
    elif field == "unknown":
        ep = obj.get("epistemic_boundary")
        if isinstance(ep, dict) and ep.get("not_proven") not in (None, "", [], {}):
            out.append(("epistemic_boundary.not_proven", ep["not_proven"]))
    return out


def collect_field_evidence(
    field: str,
    source_records: list[tuple[str, dict[str, Any]]],
    proposal: dict[str, Any],
) -> dict[str, Any]:
    exact: list[dict[str, Any]] = []
    aliases: list[dict[str, Any]] = []

    if field == "authority_required":
        values = proposal.get("source_evidence", {}).get("effective_authority_values", [])
        if values:
            aliases.append(
                {
                    "path": "g4_proposal.source_evidence",
                    "source_key": "effective_authority_values",
                    "value": values,
                    "relation": "SCOPED_AUTHORITY_EVIDENCE",
                }
            )

    for path, obj in source_records:
        if field in obj and obj[field] not in (None, "", [], {}):
            exact.append(
                {
                    "path": path,
                    "source_key": field,
                    "value": normalize_value(obj[field]),
                    "relation": "EXACT_FIELD_NAME",
                }
            )
        for alias in ALIASES.get(field, ()):
            if alias in obj and obj[alias] not in (None, "", [], {}):
                aliases.append(
                    {
                        "path": path,
                        "source_key": alias,
                        "value": normalize_value(obj[alias]),
                        "relation": "ALIAS_NOT_EQUIVALENCE",
                    }
                )
        for source_key, value in collect_nested_aliases(obj, field):
            aliases.append(
                {
                    "path": path,
                    "source_key": source_key,
                    "value": normalize_value(value),
                    "relation": "ALIAS_NOT_EQUIVALENCE",
                }
            )

    if exact:
        unique = {canonical_key(item["value"]) for item in exact}
        if len(unique) == 1:
            return {
                "state": "EXACT_SOURCE_FIELD",
                "value": exact[0]["value"],
                "evidence": exact,
                "governed_review_required": True,
            }
        return {
            "state": "MULTI_SOURCE_REVIEW",
            "value": "TOKEN_VAZIO",
            "evidence": exact,
            "governed_review_required": True,
        }

    if aliases:
        unique = {canonical_key(item["value"]) for item in aliases}
        if len(unique) == 1:
            candidate_value: Any = aliases[0]["value"]
        else:
            candidate_value = [item["value"] for item in aliases]
        return {
            "state": "SOURCE_ALIAS_CANDIDATE",
            "value": candidate_value,
            "evidence": aliases,
            "governed_review_required": True,
        }

    return {
        "state": "TOKEN_VAZIO",
        "value": "TOKEN_VAZIO",
        "evidence": [],
        "governed_review_required": True,
    }


def load_source_records(
    repo_root: Path,
    paths: list[str],
) -> list[tuple[str, dict[str, Any]]]:
    out: list[tuple[str, dict[str, Any]]] = []
    for rel in paths:
        obj = json.loads((repo_root / rel).read_text(encoding="utf-8"))
        if not isinstance(obj, dict):
            raise ValueError(f"{rel}: source record must be object")
        out.append((rel, obj))
    return out


def build_completion(
    proposals: dict[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    if proposals.get("schema") != "rafaelia.systematic-pragmatic-g4-proposals/v1":
        raise ValueError("unsupported proposals schema")
    if proposals.get("claim_allowed") is not False:
        raise ValueError("proposal claim boundary is open")
    if proposals.get("atlas_mutation_allowed") is not False:
        raise ValueError("proposal input permits Atlas mutation")

    rows: list[dict[str, Any]] = []
    field_counts = {
        field: {state: 0 for state in sorted(FIELD_STATES)}
        for field in CANONICAL_FIELDS
    }

    for proposal in proposals.get("proposals", []):
        if not isinstance(proposal, dict):
            raise ValueError("proposal row must be object")
        if proposal.get("proposal_action") != "PROPOSE_APPEND_NEW":
            continue
        source_gap_id = proposal.get("source_gap_id")
        source_paths = [
            str(value)
            for value in proposal.get("source_paths", [])
            if isinstance(value, str) and value
        ]
        if not isinstance(source_gap_id, str) or not source_gap_id or not source_paths:
            raise ValueError("append proposal missing source identity/path")

        records = load_source_records(repo_root, source_paths)
        fields = {
            field: collect_field_evidence(field, records, proposal)
            for field in CANONICAL_FIELDS
        }
        for field, item in fields.items():
            state = item["state"]
            if state not in FIELD_STATES:
                raise ValueError(f"{source_gap_id}: invalid field state {state}")
            field_counts[field][state] += 1

        exact_count = sum(
            1 for item in fields.values() if item["state"] == "EXACT_SOURCE_FIELD"
        )
        alias_count = sum(
            1 for item in fields.values() if item["state"] == "SOURCE_ALIAS_CANDIDATE"
        )
        token_count = sum(
            1 for item in fields.values() if item["state"] == "TOKEN_VAZIO"
        )
        review_count = sum(
            1 for item in fields.values() if item["state"] == "MULTI_SOURCE_REVIEW"
        )

        rows.append(
            {
                "completion_id": "G4C-" + source_gap_id,
                "proposal_id": proposal.get("proposal_id"),
                "source_gap_id": source_gap_id,
                "source_paths": source_paths,
                "baseline_existing_proposal": (
                    not proposal.get("source_evidence", {}).get(
                        "authority_resolution_applied", False
                    )
                ),
                "authority_resolution_applied": proposal.get(
                    "source_evidence", {}
                ).get("authority_resolution_applied", False),
                "proposed_atlas_gap_id": "TOKEN_VAZIO",
                "canonical_field_candidates": fields,
                "field_summary": {
                    "exact_source_fields": exact_count,
                    "source_alias_candidates": alias_count,
                    "multi_source_review": review_count,
                    "token_vazio_fields": token_count,
                    "canonical_fields_total": len(CANONICAL_FIELDS),
                },
                "completion_state": (
                    "PARTIAL_EVIDENCE"
                    if exact_count + alias_count > 0
                    else "TOKEN_VAZIO_HEAVY"
                ),
                "g4": {
                    "state": "CANONICAL_FIELD_REVIEW_REQUIRED",
                    "atlas_mutation_allowed": False,
                    "auto_create_gap_id": False,
                    "governed_review_required": True,
                },
                "claim_allowed": False,
            }
        )

    authority_unblocked = sum(
        1 for row in rows if row["authority_resolution_applied"]
    )
    baseline_existing = len(rows) - authority_unblocked

    return {
        "schema": SCHEMA,
        "claim_allowed": False,
        "atlas_mutation_allowed": False,
        "policy": {
            "canonical_completion_is_not_atlas_record": True,
            "alias_is_not_equivalence": True,
            "token_vazio_preserved_for_unsupported_fields": True,
            "auto_create_gap_id": False,
        },
        "summary": {
            "completion_candidates": len(rows),
            "baseline_existing_proposals": baseline_existing,
            "newly_unblocked_by_authority": authority_unblocked,
            "field_state_counts": field_counts,
        },
        "completions": sorted(rows, key=lambda row: row["source_gap_id"]),
    }


def validate(payload: dict[str, Any]) -> None:
    if payload.get("claim_allowed") is not False:
        raise ValueError("completion claim boundary opened")
    if payload.get("atlas_mutation_allowed") is not False:
        raise ValueError("completion permits Atlas mutation")
    rows = payload.get("completions", [])
    if payload.get("summary", {}).get("completion_candidates") != len(rows):
        raise ValueError("completion count mismatch")
    for row in rows:
        if row.get("proposed_atlas_gap_id") != "TOKEN_VAZIO":
            raise ValueError(f"{row.get('source_gap_id')}: premature Atlas id")
        if row.get("g4", {}).get("atlas_mutation_allowed") is not False:
            raise ValueError(f"{row.get('source_gap_id')}: Atlas mutation enabled")
        if row.get("g4", {}).get("auto_create_gap_id") is not False:
            raise ValueError(f"{row.get('source_gap_id')}: gap id allocation enabled")
        if row.get("claim_allowed") is not False:
            raise ValueError(f"{row.get('source_gap_id')}: claim boundary opened")
        fields = row.get("canonical_field_candidates", {})
        if set(fields) != set(CANONICAL_FIELDS):
            raise ValueError(f"{row.get('source_gap_id')}: canonical field set mismatch")
        for field, item in fields.items():
            if item.get("state") not in FIELD_STATES:
                raise ValueError(
                    f"{row.get('source_gap_id')}:{field}: invalid state"
                )
            if item.get("state") == "TOKEN_VAZIO" and item.get("value") != "TOKEN_VAZIO":
                raise ValueError(
                    f"{row.get('source_gap_id')}:{field}: unsupported value promoted"
                )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--proposals", type=Path, required=True)
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    try:
        payload = build_completion(load_json(args.proposals), args.repo_root)
        validate(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"canonical-completion: {exc}")
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
