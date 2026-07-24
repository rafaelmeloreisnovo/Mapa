#!/usr/bin/env python3
"""Validate the append-only RAFAELIA cross-source registry.

The record schema validates one node. This gate validates the graph formed by all
JSONL nodes: unique identity, local relation resolution, custody identity,
provider counts, and the explicit protection of TOKEN_VAZIO records.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECORD_VALIDATOR_PATH = ROOT / "scripts" / "validate_cross_source_records.py"
SPEC = importlib.util.spec_from_file_location(
    "cross_source_record_validator",
    RECORD_VALIDATOR_PATH,
)
assert SPEC and SPEC.loader
record_validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(record_validator)

DEFAULT_REGISTRY = ROOT / "indices" / "CROSS_SOURCE_REGISTRY.jsonl"


def canonical_report_path(path: Path) -> str:
    """Return a host-independent path label suitable for sealed evidence.

    Files inside the repository are represented relative to the repository root.
    External fixtures retain only their basename so temporary directory names,
    usernames and checkout locations cannot change report hashes or leak local
    paths into artifacts.
    """

    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return f"external://{path.name}"


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []

    if not path.is_file():
        return [], [f"registry not found: {canonical_report_path(path)}"]

    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(
                f"line {line_number}: invalid JSON at column {exc.colno}: {exc.msg}"
            )
            continue
        if not isinstance(value, dict):
            errors.append(f"line {line_number}: registry entry must be an object")
            continue
        records.append(value)

    if not records:
        errors.append("registry must contain at least one record")

    return records, errors


def validate_registry_records(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    record_ids: dict[str, int] = {}
    event_ids: dict[str, int] = {}
    drive_file_ids: dict[str, int] = {}

    for index, record in enumerate(records, 1):
        prefix = f"record {index}"
        defects = record_validator.validate_record(record)
        errors.extend(f"{prefix}: {defect}" for defect in defects)

        record_id = record.get("record_id")
        if isinstance(record_id, str):
            if record_id in record_ids:
                errors.append(
                    f"{prefix}: duplicate record_id {record_id}; "
                    f"first seen at record {record_ids[record_id]}"
                )
            else:
                record_ids[record_id] = index

        source = record.get("source")
        if isinstance(source, dict) and source.get("provider") == "google_drive":
            drive_file_id = source.get("drive_file_id")
            if isinstance(drive_file_id, str):
                if drive_file_id in drive_file_ids:
                    errors.append(
                        f"{prefix}: duplicate Drive file ID {drive_file_id}; "
                        f"first seen at record {drive_file_ids[drive_file_id]}"
                    )
                else:
                    drive_file_ids[drive_file_id] = index

        custody = record.get("custody")
        if isinstance(custody, dict):
            event_id = custody.get("event_id")
            if isinstance(event_id, str) and event_id != "TOKEN_VAZIO":
                if event_id in event_ids:
                    errors.append(
                        f"{prefix}: duplicate custody event_id {event_id}; "
                        f"first seen at record {event_ids[event_id]}"
                    )
                else:
                    event_ids[event_id] = index

    known_records = set(record_ids)
    known_events = set(event_ids)

    for index, record in enumerate(records, 1):
        prefix = f"record {index}"
        relations = record.get("relations")
        if isinstance(relations, list):
            for relation_index, relation in enumerate(relations):
                if not isinstance(relation, dict):
                    continue
                target_id = relation.get("target_id")
                if isinstance(target_id, str) and target_id not in known_records:
                    errors.append(
                        f"{prefix} relation {relation_index}: dangling target_id {target_id}"
                    )

        custody = record.get("custody")
        if isinstance(custody, dict):
            previous_event_id = custody.get("previous_event_id")
            if (
                isinstance(previous_event_id, str)
                and previous_event_id != "TOKEN_VAZIO"
                and previous_event_id not in known_events
            ):
                errors.append(
                    f"{prefix}: previous_event_id {previous_event_id} "
                    "does not resolve in this registry"
                )

        classification = record.get("classification")
        metadata = record.get("metadata")
        if (
            isinstance(classification, dict)
            and classification.get("epistemic_state") == "TOKEN_VAZIO"
        ):
            if not isinstance(metadata, dict):
                errors.append(f"{prefix}: TOKEN_VAZIO requires metadata")
            elif metadata.get("deletion_allowed") is True:
                errors.append(f"{prefix}: TOKEN_VAZIO cannot authorize deletion")

    return errors


def build_report(path: Path) -> dict[str, Any]:
    records, parse_errors = load_jsonl(path)
    errors = parse_errors + validate_registry_records(records)

    providers = Counter()
    epistemic_states = Counter()
    relation_predicates = Counter()
    token_vazio_count = 0

    for record in records:
        source = record.get("source")
        if isinstance(source, dict) and isinstance(source.get("provider"), str):
            providers[source["provider"]] += 1

        classification = record.get("classification")
        if isinstance(classification, dict):
            state = classification.get("epistemic_state")
            if isinstance(state, str):
                epistemic_states[state] += 1
                if state == "TOKEN_VAZIO":
                    token_vazio_count += 1

        relations = record.get("relations")
        if isinstance(relations, list):
            for relation in relations:
                if isinstance(relation, dict):
                    predicate = relation.get("predicate")
                    if isinstance(predicate, str):
                        relation_predicates[predicate] += 1

    status = "PASS" if not errors else "FAIL"
    return {
        "schema_version": "rafaelia.cross-source-registry-report/v1",
        "registry": canonical_report_path(path),
        "status": status,
        "record_count": len(records),
        "provider_counts": dict(sorted(providers.items())),
        "epistemic_state_counts": dict(sorted(epistemic_states.items())),
        "relation_predicate_counts": dict(sorted(relation_predicates.items())),
        "token_vazio_count": token_vazio_count,
        "defect_count": len(errors),
        "defects": errors,
        "claim_allowed": False,
        "next_verifiable_step": (
            "Persist content hashes and append custody events for authorized records."
            if status == "PASS"
            else "Correct registry defects before any claim promotion or synchronization."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--write-report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(args.registry)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    if args.write_report:
        args.write_report.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
