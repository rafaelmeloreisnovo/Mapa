#!/usr/bin/env python3
"""Validate the Mapa control-plane registry for the four-inks session ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "indices/SESSION_VECTOR_FOUR_INKS_REGISTRY.v1.jsonl"

EXPECTED_COUNTS = {
    "PARABLE": 8,
    "CONVENTION": 6,
    "DEMONSTRATION": 3,
    "HYPOTHESIS": 2,
    "TOKEN_VAZIO": 3,
}
EXPECTED_POINTERS = {
    "PARABLE": "MAP-SV-PARABLE",
    "CONVENTION": "MAP-SV-CONVENTION",
    "DEMONSTRATION": "MAP-SV-DEMONSTRATION",
    "HYPOTHESIS": "MAP-SV-HYPOTHESIS",
    "TOKEN_VAZIO": "MAP-SV-TOKEN-VAZIO",
}
REQUIRED = {
    "schema_version", "pointer_id", "producer", "source_path", "source_ref",
    "source_blob_sha", "source_digest", "selector", "authority", "state",
    "scope", "not_claimed", "next_action", "drift_policy", "claim_allowed",
}


def load_records(path: Path) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_no}: invalid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"line {line_no}: record must be an object")
        record["_line"] = line_no
        result.append(record)
    if not result:
        raise ValueError("registry is empty")
    return result


def validate(records: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    pointer_ids: set[str] = set()
    inks: set[str] = set()
    refs: set[str] = set()
    blobs: set[str] = set()
    paths: set[str] = set()
    total_count = 0

    for record in records:
        line = record.get("_line", "?")
        keys = set(record) - {"_line"}
        missing = REQUIRED - keys
        extra = keys - REQUIRED
        if missing:
            errors.append(f"line {line}: missing keys {sorted(missing)}")
        if extra:
            errors.append(f"line {line}: unexpected keys {sorted(extra)}")

        if record.get("schema_version") != "session-vector-pointer.v1":
            errors.append(f"line {line}: invalid schema_version")
        if record.get("producer") != "rafaelmeloreisnovo/papers":
            errors.append(f"line {line}: producer must be papers")
        if record.get("source_path") != "data/memory/session_vectors_four_inks.v1.jsonl":
            errors.append(f"line {line}: invalid source_path")
        if record.get("claim_allowed") is not False:
            errors.append(f"line {line}: claim_allowed must remain false")
        if record.get("drift_policy") != "ref_or_blob_change_requires_resynchronization":
            errors.append(f"line {line}: invalid drift policy")

        pointer_id = record.get("pointer_id")
        if pointer_id in pointer_ids:
            errors.append(f"line {line}: duplicate pointer_id {pointer_id}")
        pointer_ids.add(pointer_id)

        ref = record.get("source_ref")
        blob = record.get("source_blob_sha")
        path = record.get("source_path")
        if not isinstance(ref, str) or len(ref) != 40 or any(c not in "0123456789abcdef" for c in ref):
            errors.append(f"line {line}: source_ref must be a 40-char lowercase hex SHA")
        if not isinstance(blob, str) or len(blob) != 40 or any(c not in "0123456789abcdef" for c in blob):
            errors.append(f"line {line}: source_blob_sha must be a 40-char lowercase hex SHA")
        refs.add(str(ref))
        blobs.add(str(blob))
        paths.add(str(path))

        digest = record.get("source_digest")
        if digest != "TOKEN_VAZIO" and (
            not isinstance(digest, str)
            or len(digest) != 64
            or any(c not in "0123456789abcdef" for c in digest)
        ):
            errors.append(f"line {line}: source_digest must be SHA-256 or TOKEN_VAZIO")

        selector = record.get("selector")
        if not isinstance(selector, dict) or set(selector) != {"ink", "expected_count"}:
            errors.append(f"line {line}: malformed selector")
            continue
        ink = selector.get("ink")
        count = selector.get("expected_count")
        if ink not in EXPECTED_COUNTS:
            errors.append(f"line {line}: invalid ink selector {ink}")
        else:
            if ink in inks:
                errors.append(f"line {line}: duplicate ink selector {ink}")
            inks.add(ink)
            if pointer_id != EXPECTED_POINTERS[ink]:
                errors.append(f"line {line}: pointer_id does not match ink {ink}")
            if count != EXPECTED_COUNTS[ink]:
                errors.append(f"line {line}: expected_count for {ink} must be {EXPECTED_COUNTS[ink]}")
            total_count += int(count) if isinstance(count, int) else 0

        authority = record.get("authority")
        expected_authority = {
            "source_owner": "rafaelmeloreisnovo/papers",
            "scientific_owner": "rafaelmeloreisnovo/papers",
            "control_plane": "rafaelmeloreisnovo/Mapa",
            "execution_owner": "receipt-producing environment",
        }
        if authority != expected_authority:
            errors.append(f"line {line}: authority split is invalid")

        if record.get("state") not in {
            "SYNCHRONIZED_PRIVATE", "STALE_CONSUMER", "CONTRADICTION", "BLOCKED_BEFORE_STEPS"
        }:
            errors.append(f"line {line}: invalid state")
        if not isinstance(record.get("not_claimed"), list) or not record["not_claimed"]:
            errors.append(f"line {line}: not_claimed is required")
        if not isinstance(record.get("scope"), str) or len(record["scope"]) < 12:
            errors.append(f"line {line}: scope is too short")
        if not isinstance(record.get("next_action"), str) or len(record["next_action"]) < 8:
            errors.append(f"line {line}: next_action is required")

    if inks != set(EXPECTED_COUNTS):
        errors.append(f"registry must contain all five regimes, got {sorted(inks)}")
    if pointer_ids != set(EXPECTED_POINTERS.values()):
        errors.append(f"registry pointer set mismatch: {sorted(pointer_ids)}")
    if total_count != 22:
        errors.append(f"selector counts must total 22, got {total_count}")
    if len(refs) != 1:
        errors.append(f"all pointers must pin one producer ref, got {sorted(refs)}")
    if len(blobs) != 1:
        errors.append(f"all pointers must pin one producer blob, got {sorted(blobs)}")
    if len(paths) != 1:
        errors.append(f"all pointers must pin one producer path, got {sorted(paths)}")

    return {
        "schema_version": "four-inks-session-registry-validation.v1",
        "status": "PASS" if not errors else "FAIL",
        "claim_allowed": False,
        "pointer_count": len(records),
        "selected_vector_count": total_count,
        "source_ref": next(iter(refs)) if len(refs) == 1 else "TOKEN_VAZIO",
        "source_blob_sha": next(iter(blobs)) if len(blobs) == 1 else "TOKEN_VAZIO",
        "source_digest": "TOKEN_VAZIO",
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    try:
        report = validate(load_records(args.registry))
    except (OSError, ValueError) as exc:
        report = {
            "schema_version": "four-inks-session-registry-validation.v1",
            "status": "FAIL",
            "claim_allowed": False,
            "pointer_count": 0,
            "selected_vector_count": 0,
            "source_ref": "TOKEN_VAZIO",
            "source_blob_sha": "TOKEN_VAZIO",
            "source_digest": "TOKEN_VAZIO",
            "errors": [str(exc)],
        }

    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
