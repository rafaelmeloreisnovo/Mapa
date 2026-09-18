#!/usr/bin/env python3
"""Finalize systematic-pragmatic routing without promoting external claims.

The final state binds each bounded operational-gap source record to exactly one
governed Atlas record and accepts cycle schema families structurally only.

SOURCE_RECORD_BINDING != EXTERNAL_CONDITION_CLOSURE
STRUCTURAL_FAMILY != SEMANTIC_EQUIVALENCE
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "rafaelia.systematic-pragmatic-finalization/v1"
POLICY_SCHEMA = "rafaelia.systematic-pragmatic-finalization-policy/v1"
APPEND_SCHEMA = "RAFAELIA_GAP_RECORD_APPEND_V1"
POLICY_PATH = "data/governance/SYSTEMATIC_PRAGMATIC_FINALIZATION_V1.json"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{lineno}: expected object")
        out.append(value)
    return out


def walk(value: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key), child
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def flatten_strings(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, str):
        if value.strip():
            out.append(value.strip())
    elif isinstance(value, (int, float, bool)):
        out.append(str(value))
    elif isinstance(value, list):
        for child in value:
            out.extend(flatten_strings(child))
    elif isinstance(value, dict):
        preferred = (
            "criterion",
            "evidence_needed",
            "next_probe",
            "next_verifiable_step",
            "next_review_gate",
            "falsifier",
            "result",
        )
        used = False
        for key in preferred:
            if key in value:
                out.extend(flatten_strings(value[key]))
                used = True
        if not used:
            for child in value.values():
                out.extend(flatten_strings(child))
    return out


def unique(values: Iterable[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        value = value.strip()
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def collect_recursive(records: list[dict[str, Any]], keys: set[str]) -> list[str]:
    values: list[str] = []
    for obj in records:
        for key, value in walk(obj):
            if key in keys:
                values.extend(flatten_strings(value))
    return unique(values)


def collect_top_level(records: list[dict[str, Any]], keys: tuple[str, ...]) -> list[str]:
    values: list[str] = []
    for obj in records:
        for key in keys:
            if key in obj:
                values.extend(flatten_strings(obj[key]))
    return unique(values)


def source_gap_hash(source_gap_id: str) -> str:
    return hashlib.sha256(source_gap_id.encode("utf-8")).hexdigest()[:16].upper()


def atlas_gap_id(source_gap_id: str) -> str:
    return "GAP-G4SRC-" + source_gap_hash(source_gap_id)


def artifact_id(source_gap_id: str) -> str:
    return "OPG_SOURCE::" + source_gap_id


def read_source_records(repo_root: Path, paths: list[str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for rel in paths:
        value = json.loads((repo_root / rel).read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"{rel}: source record must be object")
        records.append(value)
    return records


def expected_record(
    source_gap_id: str,
    source_paths: list[str],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    known = collect_recursive(records, {"evidence_for"})
    if not known:
        known = [
            "Operational-gap source record(s) are present at the exact GitHub paths listed in source_refs."
        ]

    authority = collect_top_level(records, ("owner_authority", "owner", "authority"))
    if not authority:
        authority = ["rafaelmeloreisnovo/Mapa control_plane governance"]

    evidence_required = collect_recursive(records, {"evidence_needed"})
    next_values = collect_recursive(
        records,
        {"next_probe", "next_verifiable_step", "next_review_gate", "closure_gate"},
    )
    if not evidence_required:
        evidence_required = [
            "Evidence satisfying governed next gate: " + value
            for value in next_values
        ]
    if not evidence_required:
        evidence_required = [
            "Explicit evidence receipt linked to the bounded source-gap identity and exact source paths."
        ]

    if next_values:
        next_gate = " | ".join(next_values)
    else:
        next_gate = "GOVERNED_SOURCE_GAP_EVIDENCE_REVIEW"

    refs = [f"Mapa: {path}" for path in source_paths]
    refs.append(POLICY_PATH)

    scope = (
        f"Governed operational-gap source binding for {source_gap_id}; "
        f"source_paths={';'.join(source_paths)}. "
        "This scope binds the source record only, not closure of its external/runtime/scientific subject."
    )

    return {
        "gap_id": atlas_gap_id(source_gap_id),
        "artifact_id": artifact_id(source_gap_id),
        "provider": "GitHub",
        "scope": scope,
        "gap_class": "GOVERNANCE",
        "priority": "P1",
        "state": "TOKEN_VAZIO",
        "known": known,
        "unknown": [
            "Subject-level closure remains unproven; this Atlas record binds only the operational-gap source artifact until evidence_required is satisfied."
        ],
        "contradictions": [],
        "authority_required": authority,
        "evidence_required": evidence_required,
        "falsifier": (
            "A different source identity/path is bound to this record, or the record is used as proof that the underlying external/runtime/scientific condition is closed."
        ),
        "acceptance_criterion": (
            "The exact source paths remain bound to this deterministic Atlas identity; required evidence is linked by receipt before any subject-level closure claim; unresolved external state remains explicit."
        ),
        "predecessors": [],
        "successors": [],
        "next_gate": next_gate,
        "source_refs": refs,
        "resolution_evidence": [],
        "claim_allowed": False,
    }


def generated_append_entries(
    routing_bindings: dict[str, Any],
    repo_root: Path,
) -> list[dict[str, Any]]:
    candidates = sorted(
        routing_bindings.get("gap_binding_candidates", []),
        key=lambda row: str(row.get("source_gap_id", "")),
    )
    entries: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates, 1):
        source_gap_id = candidate.get("source_gap_id")
        source_paths = [
            str(path)
            for path in candidate.get("source_paths", [])
            if isinstance(path, str) and path
        ]
        if not isinstance(source_gap_id, str) or not source_gap_id or not source_paths:
            raise ValueError("routing candidate missing bounded source identity")
        records = read_source_records(repo_root, source_paths)
        entries.append(
            {
                "schema": APPEND_SCHEMA,
                "append_id": f"RGA-APPEND-20260918-G4SRC-{index:04d}",
                "claim_allowed": False,
                "record": expected_record(source_gap_id, source_paths, records),
            }
        )
    return entries


def append_index(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in entries:
        rec = row.get("record")
        if not isinstance(rec, dict):
            continue
        gap_id = rec.get("gap_id")
        if isinstance(gap_id, str):
            out[gap_id] = row
    return out


def build(
    routing_bindings: dict[str, Any],
    reconciliation: dict[str, Any],
    append_entries: list[dict[str, Any]],
    policy: dict[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    if routing_bindings.get("schema") != "rafaelia.systematic-pragmatic-routing-bindings/v1":
        raise ValueError("unsupported routing bindings schema")
    if reconciliation.get("schema") != "rafaelia.systematic-pragmatic-g4-reconciliation/v1":
        raise ValueError("unsupported reconciliation schema")
    if policy.get("schema") != POLICY_SCHEMA or policy.get("claim_allowed") is not False:
        raise ValueError("invalid finalization policy")
    if routing_bindings.get("claim_allowed") is not False:
        raise ValueError("routing bindings claim boundary open")
    if reconciliation.get("claim_allowed") is not False:
        raise ValueError("reconciliation claim boundary open")

    expected = generated_append_entries(routing_bindings, repo_root)
    actual_by_gap = append_index(append_entries)

    source_bindings: list[dict[str, Any]] = []
    recon_by_source = {
        row["source_gap_id"]: row
        for row in reconciliation.get("reconciliation", [])
        if isinstance(row, dict) and isinstance(row.get("source_gap_id"), str)
    }

    for generated in expected:
        exp_rec = generated["record"]
        gap_id = exp_rec["gap_id"]
        actual = actual_by_gap.get(gap_id)
        if actual is None:
            raise ValueError(f"missing committed append record {gap_id}")
        act_rec = actual.get("record")
        if not isinstance(act_rec, dict):
            raise ValueError(f"{gap_id}: committed record missing")
        for field in (
            "gap_id",
            "artifact_id",
            "provider",
            "scope",
            "gap_class",
            "priority",
            "state",
            "known",
            "unknown",
            "authority_required",
            "evidence_required",
            "acceptance_criterion",
            "predecessors",
            "successors",
            "next_gate",
            "source_refs",
            "claim_allowed",
        ):
            if act_rec.get(field) != exp_rec.get(field):
                raise ValueError(f"{gap_id}: committed field mismatch: {field}")

        source_gap_id = exp_rec["artifact_id"].split("OPG_SOURCE::", 1)[1]
        recon = recon_by_source.get(source_gap_id)
        if not recon:
            raise ValueError(f"{source_gap_id}: reconciliation missing")
        candidates = recon.get("candidate_atlas_gap_ids", [])
        if recon.get("status") != "CANDIDATE_EXACT_MATCH":
            raise ValueError(f"{source_gap_id}: exact Atlas match not observed")
        if candidates != [gap_id]:
            raise ValueError(
                f"{source_gap_id}: expected unique target {gap_id}, observed {candidates}"
            )
        source_bindings.append(
            {
                "source_gap_id": source_gap_id,
                "atlas_gap_id": gap_id,
                "artifact_id": exp_rec["artifact_id"],
                "provider": "GitHub",
                "source_paths": [
                    ref.split(": ", 1)[1]
                    for ref in exp_rec["source_refs"]
                    if ref.startswith("Mapa: ")
                ],
                "state": "BOUND_GOVERNED_SOURCE_RECORD",
                "subject_level_closure": False,
                "claim_allowed": False,
            }
        )

    family_rows: list[dict[str, Any]] = []
    for family in routing_bindings.get("schema_families", []):
        if not isinstance(family, dict):
            raise ValueError("schema family row must be object")
        family_rows.append(
            {
                "family_id": family.get("family_id"),
                "schema_family": family.get("schema_family"),
                "record_count": family.get("record_count"),
                "state": "STRUCTURAL_FAMILY_ACCEPTED",
                "semantic_equivalence": False,
                "g4_state": "NOT_APPLICABLE_SCHEMA_FAMILY",
                "claim_allowed": False,
            }
        )

    return {
        "schema": SCHEMA,
        "claim_allowed": False,
        "publication_ready": False,
        "system_state": "COMPLETE_STRUCTURAL_ROUTING",
        "semantic_boundary": {
            "source_record_binding_is_external_closure": False,
            "structural_family_is_semantic_equivalence": False,
            "atlas_append_is_runtime_or_scientific_proof": False,
        },
        "summary": {
            "source_gap_bindings": len(source_bindings),
            "schema_families_structurally_resolved": len(family_rows),
            "remaining_internal_review_required": 0,
            "remaining_internal_binding_token_vazio": 0,
            "external_subjects_may_remain_open": True,
        },
        "source_bindings": sorted(
            source_bindings, key=lambda row: row["source_gap_id"]
        ),
        "schema_family_resolutions": sorted(
            family_rows, key=lambda row: str(row["family_id"])
        ),
    }


def validate(payload: dict[str, Any]) -> None:
    if payload.get("claim_allowed") is not False:
        raise ValueError("finalization claim boundary open")
    if payload.get("publication_ready") is not False:
        raise ValueError("publication boundary unexpectedly open")
    if payload.get("system_state") != "COMPLETE_STRUCTURAL_ROUTING":
        raise ValueError("system not structurally complete")
    summary = payload.get("summary", {})
    if summary.get("source_gap_bindings") != 35:
        raise ValueError("expected 35 governed source bindings")
    if summary.get("schema_families_structurally_resolved") != 25:
        raise ValueError("expected 25 structural schema families")
    if summary.get("remaining_internal_review_required") != 0:
        raise ValueError("internal review debt remains")
    if summary.get("remaining_internal_binding_token_vazio") != 0:
        raise ValueError("internal binding TOKEN_VAZIO remains")
    bindings = payload.get("source_bindings", [])
    targets = [row.get("atlas_gap_id") for row in bindings]
    if len(set(targets)) != 35:
        raise ValueError("Atlas binding targets not one-to-one")
    if any(row.get("subject_level_closure") is not False for row in bindings):
        raise ValueError("subject-level closure promoted")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--routing-bindings", type=Path, required=True)
    ap.add_argument("--reconciliation", type=Path, required=True)
    ap.add_argument("--append-ledger", type=Path, required=True)
    ap.add_argument("--policy", type=Path, required=True)
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    try:
        payload = build(
            load_json(args.routing_bindings),
            load_json(args.reconciliation),
            load_jsonl(args.append_ledger),
            load_json(args.policy),
            args.repo_root,
        )
        validate(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"systematic-pragmatic-finalization: {exc}")
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
