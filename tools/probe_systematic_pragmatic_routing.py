#!/usr/bin/env python3
"""Bounded semantic probe for routing descendants selected by the pragmatic action map.

The probe observes structure only. It does not assign G3 decisions automatically.
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "rafaelia.systematic-pragmatic-routing-probe/v1"
CYCLES_PREFIX = "data/routing/cycles/"
GAPS_PREFIX = "data/routing/operational-gaps/"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


def first_present(value: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in value:
            return value[key]
    return None


def has_any_key(value: Any, wanted: set[str]) -> bool:
    return any(key in wanted for key in walk_keys(value))


def selected_paths(action_map: dict[str, Any], prefix: str) -> list[str]:
    return sorted(
        {
            str(row.get("path", ""))
            for row in action_map.get("actions", [])
            if str(row.get("path", "")).startswith(prefix)
            and row.get("service") == "SEMANTIC_TRIAGE"
            and row.get("nibiguiri_state") == "NIBIGUIRI:CAUSA_DESCONHECIDA"
            and "TOKEN_VAZIO" in (row.get("markers") or [])
        }
    )


def parse_records(repo_root: Path, paths: list[str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for rel in paths:
        path = repo_root / rel
        raw = path.read_text(encoding="utf-8")
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            records.append(
                {
                    "path": rel,
                    "parse_status": "FAIL",
                    "error": str(exc),
                    "token_vazio_occurrences": raw.count("TOKEN_VAZIO"),
                }
            )
            continue
        if not isinstance(obj, dict):
            records.append(
                {
                    "path": rel,
                    "parse_status": "FAIL",
                    "error": "top-level JSON is not object",
                    "token_vazio_occurrences": raw.count("TOKEN_VAZIO"),
                }
            )
            continue
        records.append(
            {
                "path": rel,
                "parse_status": "PASS",
                "object": obj,
                "token_vazio_occurrences": raw.count("TOKEN_VAZIO"),
            }
        )
    return records


def analyze_cycles(records: list[dict[str, Any]]) -> dict[str, Any]:
    schema_counts: collections.Counter[str] = collections.Counter()
    claim_false = 0
    structured_open_context = 0
    closure_or_next = 0
    parseable = 0
    token_total = 0
    samples: list[dict[str, Any]] = []

    open_keys = {
        "F_gap",
        "f_gap",
        "token_vazio",
        "uncertainty_delta",
        "uncertainty_state",
        "contract_gate",
        "r3",
        "lifecycle",
    }
    next_keys = {
        "closure_gate",
        "next_probe",
        "next_verifiable_step",
        "F_next",
        "f_next",
        "next_probes",
        "next_review_gate",
    }

    for record in records:
        token_total += int(record.get("token_vazio_occurrences", 0))
        if record.get("parse_status") != "PASS":
            continue
        parseable += 1
        obj = record["object"]
        schema = first_present(obj, ("schema", "schema_version")) or "TOKEN_VAZIO_SCHEMA"
        schema_counts[str(schema)] += 1
        if obj.get("claim_allowed") is False:
            claim_false += 1
        if has_any_key(obj, open_keys):
            structured_open_context += 1
        if has_any_key(obj, next_keys):
            closure_or_next += 1
        if len(samples) < 8:
            samples.append(
                {
                    "path": record["path"],
                    "schema": schema,
                    "claim_allowed": obj.get("claim_allowed", "TOKEN_VAZIO"),
                    "structured_open_context": has_any_key(obj, open_keys),
                    "closure_or_next_gate": has_any_key(obj, next_keys),
                    "token_vazio_occurrences": record["token_vazio_occurrences"],
                }
            )

    return {
        "selected_actions": len(records),
        "parseable_json": parseable,
        "claim_allowed_false": claim_false,
        "structured_open_context": structured_open_context,
        "closure_or_next_gate": closure_or_next,
        "token_vazio_occurrences": token_total,
        "schema_counts": dict(sorted(schema_counts.items())),
        "samples": samples,
    }


def analyze_operational_gaps(records: list[dict[str, Any]]) -> dict[str, Any]:
    parseable = 0
    claim_false = 0
    owner_present = 0
    closure_present = 0
    token_total = 0
    gap_ids: list[str] = []
    schemas: collections.Counter[str] = collections.Counter()
    states: collections.Counter[str] = collections.Counter()
    samples: list[dict[str, Any]] = []

    closure_keys = {
        "closure_gate",
        "next_probe",
        "next_verifiable_step",
        "next_review_gate",
        "falsifier",
    }

    for record in records:
        token_total += int(record.get("token_vazio_occurrences", 0))
        if record.get("parse_status") != "PASS":
            continue
        parseable += 1
        obj = record["object"]
        schema = first_present(obj, ("schema", "schema_version")) or "TOKEN_VAZIO_SCHEMA"
        schemas[str(schema)] += 1
        gap_id = obj.get("gap_id")
        if isinstance(gap_id, str) and gap_id:
            gap_ids.append(gap_id)
        if obj.get("claim_allowed") is False:
            claim_false += 1
        owner = first_present(obj, ("owner_authority", "owner", "authority"))
        if owner not in (None, "", [], {}):
            owner_present += 1
        if has_any_key(obj, closure_keys):
            closure_present += 1
        state = first_present(obj, ("status", "state", "uncertainty_state"))
        if state is not None:
            states[str(state)] += 1
        if len(samples) < 8:
            samples.append(
                {
                    "path": record["path"],
                    "schema": schema,
                    "gap_id": gap_id or "TOKEN_VAZIO_GAP_ID",
                    "claim_allowed": obj.get("claim_allowed", "TOKEN_VAZIO"),
                    "owner_present": owner not in (None, "", [], {}),
                    "closure_or_next_gate": has_any_key(obj, closure_keys),
                    "state": state or "TOKEN_VAZIO_STATE",
                    "token_vazio_occurrences": record["token_vazio_occurrences"],
                }
            )

    counts = collections.Counter(gap_ids)
    duplicate_groups = {
        gap_id: count for gap_id, count in sorted(counts.items()) if count > 1
    }
    return {
        "selected_actions": len(records),
        "parseable_json": parseable,
        "with_gap_id": len(gap_ids),
        "unique_gap_ids": len(counts),
        "duplicate_gap_id_groups": duplicate_groups,
        "claim_allowed_false": claim_false,
        "owner_present": owner_present,
        "closure_or_next_gate": closure_present,
        "token_vazio_occurrences": token_total,
        "schema_counts": dict(sorted(schemas.items())),
        "state_counts": dict(sorted(states.items())),
        "samples": samples,
    }


def build_report(action_map: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    if action_map.get("schema") != "rafaelia.systematic-pragmatic-map/v1":
        raise ValueError("unsupported action map schema")
    if action_map.get("claim_allowed") is not False:
        raise ValueError("action map claim_allowed must remain false")

    cycle_paths = selected_paths(action_map, CYCLES_PREFIX)
    gap_paths = selected_paths(action_map, GAPS_PREFIX)
    cycles = parse_records(repo_root, cycle_paths)
    gaps = parse_records(repo_root, gap_paths)

    return {
        "schema": SCHEMA,
        "claim_allowed": False,
        "scope": {
            "cycles_prefix": CYCLES_PREFIX,
            "operational_gaps_prefix": GAPS_PREFIX,
        },
        "boundary": [
            "TOKEN_VAZIO marker presence is an observation, not a defect verdict.",
            "Operational gap record identity is distinct from Gap Atlas binding.",
            "The probe never assigns G3 or G4 automatically.",
        ],
        "cycles": analyze_cycles(cycles),
        "operational_gaps": analyze_operational_gaps(gaps),
        "next_gate": (
            "Use this report as evidence for explicit G3 decisions; preserve G4 blocked "
            "until the decision semantics are recorded and validated."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--action-map", type=Path, required=True)
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    try:
        report = build_report(load_json(args.action_map), args.repo_root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"routing-semantic-probe: {exc}")
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "cycles": report["cycles"],
                "operational_gaps": report["operational_gaps"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
