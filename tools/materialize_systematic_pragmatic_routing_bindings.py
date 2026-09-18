#!/usr/bin/env python3
"""Materialize routing descendants after explicit G3 decisions.

- SEMANTIC_SCHEMA -> schema-family review candidates.
- DISTINCT_GAP + PER_EXISTING_GAP_ID -> per-source-gap binding candidates.

No Gap Atlas id is created or bound automatically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA = "rafaelia.systematic-pragmatic-routing-bindings/v1"


def digest_id(prefix: str, *parts: str) -> str:
    raw = "\0".join(parts).encode("utf-8")
    return prefix + hashlib.sha256(raw).hexdigest()[:16]


def load_json(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError(f"{path}: expected object")
    return obj


def load_decisions(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        row = json.loads(raw)
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{lineno}: expected object")
        out.append(row)
    return out


def selected_actions(
    action_map: dict[str, Any],
    decision: dict[str, Any],
) -> list[dict[str, Any]]:
    observed = decision.get("observed", {})
    prefix = str(observed.get("domain", "")).rstrip("/") + "/"
    service = observed.get("service")
    nib = observed.get("nibiguiri_state")
    markers = list(observed.get("markers") or [])
    return sorted(
        [
            row
            for row in action_map.get("actions", [])
            if str(row.get("path", "")).startswith(prefix)
            and (service is None or row.get("service") == service)
            and (nib is None or row.get("nibiguiri_state") == nib)
            and (not markers or list(row.get("markers") or []) == markers)
        ],
        key=lambda row: str(row.get("path", "")),
    )


def read_record(repo_root: Path, rel: str) -> tuple[dict[str, Any], str]:
    raw = (repo_root / rel).read_text(encoding="utf-8")
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise ValueError(f"{rel}: top-level JSON must be object")
    return obj, raw


def materialize_schema_families(
    action_map: dict[str, Any],
    decision: dict[str, Any],
    repo_root: Path,
) -> list[dict[str, Any]]:
    cluster_id = str(decision["cluster_id"])
    groups: dict[str, list[tuple[str, dict[str, Any], str]]] = {}
    for row in selected_actions(action_map, decision):
        rel = str(row["path"])
        obj, raw = read_record(repo_root, rel)
        schema = obj.get("schema") or obj.get("schema_version") or "TOKEN_VAZIO_SCHEMA"
        groups.setdefault(str(schema), []).append((rel, obj, raw))

    families: list[dict[str, Any]] = []
    for schema, records in sorted(groups.items()):
        families.append(
            {
                "family_id": digest_id("SF-", cluster_id, schema),
                "parent_cluster_id": cluster_id,
                "schema_family": schema,
                "record_count": len(records),
                "claim_allowed_false": sum(
                    1 for _, obj, _ in records if obj.get("claim_allowed") is False
                ),
                "token_vazio_occurrences": sum(
                    raw.count("TOKEN_VAZIO") for _, _, raw in records
                ),
                "sample_paths": [rel for rel, _, _ in records[:10]],
                "g3": {
                    "state": "REVIEW_REQUIRED",
                    "automatic_decision": False,
                },
                "g4": {
                    "state": "BLOCKED_BY_G3",
                    "binding": "TOKEN_VAZIO",
                    "auto_create_gap_id": False,
                },
                "claim_allowed": False,
            }
        )
    return families


def _owner(obj: dict[str, Any]) -> Any:
    for key in ("owner_authority", "owner", "authority"):
        if key in obj:
            return obj[key]
    return None


def _state(obj: dict[str, Any]) -> Any:
    for key in ("status", "state", "uncertainty_state"):
        if key in obj:
            return obj[key]
    return None


def _has_closure(obj: Any) -> bool:
    wanted = {
        "closure_gate",
        "next_probe",
        "next_verifiable_step",
        "next_review_gate",
        "falsifier",
    }
    if isinstance(obj, dict):
        for key, value in obj.items():
            if str(key) in wanted:
                return True
            if _has_closure(value):
                return True
    elif isinstance(obj, list):
        return any(_has_closure(value) for value in obj)
    return False


def materialize_gap_bindings(
    action_map: dict[str, Any],
    decision: dict[str, Any],
    repo_root: Path,
) -> list[dict[str, Any]]:
    cluster_id = str(decision["cluster_id"])
    groups: dict[str, list[tuple[str, dict[str, Any], str]]] = {}
    for row in selected_actions(action_map, decision):
        rel = str(row["path"])
        obj, raw = read_record(repo_root, rel)
        gap_id = obj.get("gap_id")
        if not isinstance(gap_id, str) or not gap_id:
            raise ValueError(f"{rel}: DISTINCT_GAP decision requires source gap_id")
        groups.setdefault(gap_id, []).append((rel, obj, raw))

    bindings: list[dict[str, Any]] = []
    for gap_id, records in sorted(groups.items()):
        owners = sorted(
            {
                json.dumps(_owner(obj), ensure_ascii=False, sort_keys=True)
                for _, obj, _ in records
                if _owner(obj) not in (None, "", [], {})
            }
        )
        states = sorted(
            {
                json.dumps(_state(obj), ensure_ascii=False, sort_keys=True)
                for _, obj, _ in records
                if _state(obj) is not None
            }
        )
        bindings.append(
            {
                "binding_candidate_id": digest_id("GB-", cluster_id, gap_id),
                "parent_cluster_id": cluster_id,
                "source_gap_id": gap_id,
                "record_count": len(records),
                "source_paths": [rel for rel, _, _ in records],
                "owner_values": owners,
                "state_values": states,
                "claim_allowed_false": sum(
                    1 for _, obj, _ in records if obj.get("claim_allowed") is False
                ),
                "closure_or_next_gate": sum(
                    1 for _, obj, _ in records if _has_closure(obj)
                ),
                "token_vazio_occurrences": sum(
                    raw.count("TOKEN_VAZIO") for _, _, raw in records
                ),
                "g4": {
                    "state": "REVIEW_EXISTING_GAP_ID_BINDING",
                    "source_gap_id": gap_id,
                    "atlas_gap_id": "TOKEN_VAZIO",
                    "auto_create_gap_id": False,
                },
                "claim_allowed": False,
            }
        )
    return bindings


def materialize(
    action_map: dict[str, Any],
    decisions: list[dict[str, Any]],
    repo_root: Path,
) -> dict[str, Any]:
    if action_map.get("schema") != "rafaelia.systematic-pragmatic-map/v1":
        raise ValueError("unsupported action map schema")
    if action_map.get("claim_allowed") is not False:
        raise ValueError("action map claim boundary is open")

    semantic = [
        row
        for row in decisions
        if row.get("decision") == "SPLIT_REQUIRED"
        and row.get("split_strategy") == "SEMANTIC_SCHEMA"
    ]
    distinct = [
        row
        for row in decisions
        if row.get("decision") == "DISTINCT_GAP"
        and row.get("binding_strategy") == "PER_EXISTING_GAP_ID"
    ]

    schema_families: list[dict[str, Any]] = []
    gap_bindings: list[dict[str, Any]] = []
    for row in semantic:
        schema_families.extend(materialize_schema_families(action_map, row, repo_root))
    for row in distinct:
        gap_bindings.extend(materialize_gap_bindings(action_map, row, repo_root))

    return {
        "schema": SCHEMA,
        "claim_allowed": False,
        "policy": {
            "schema_family_is_not_same_situation": True,
            "source_gap_id_is_not_atlas_binding": True,
            "auto_create_gap_id": False,
        },
        "summary": {
            "semantic_schema_decisions": len(semantic),
            "schema_families": len(schema_families),
            "distinct_gap_decisions": len(distinct),
            "source_gap_binding_candidates": len(gap_bindings),
            "multi_record_gap_ids": sum(
                1 for row in gap_bindings if row["record_count"] > 1
            ),
        },
        "schema_families": sorted(
            schema_families,
            key=lambda row: (-row["record_count"], row["schema_family"]),
        ),
        "gap_binding_candidates": sorted(
            gap_bindings,
            key=lambda row: (-row["record_count"], row["source_gap_id"]),
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--action-map", type=Path, required=True)
    ap.add_argument("--decisions", type=Path, required=True)
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    try:
        payload = materialize(
            load_json(args.action_map),
            load_decisions(args.decisions),
            args.repo_root,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"routing-bindings: {exc}")
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
