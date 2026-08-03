#!/usr/bin/env python3
"""Fail-closed validator for the RAFAELIA IGC priority delta."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from dataclasses import dataclass
from typing import Any, Iterable

ROOT = pathlib.Path(__file__).resolve().parents[1]

DEFAULT_PATHS = {
    "gaps": ROOT / "data/gaps/igc_priority_fgap.20260802T2250-0300.jsonl",
    "geometry": ROOT / "data/geometry/geometric_invariants.delta.20260802T2250-0300.jsonl",
    "questions": ROOT / "data/questions/igc_urgent_questions.20260802T2250-0300.jsonl",
    "memory": ROOT / "data/memory/longitudinal_igc_priority.20260802T2250-0300.jsonl",
}

EXPECTED_COUNTS = {"gaps": 12, "geometry": 4, "questions": 15, "memory": 6}
ALLOWED_PRIORITIES = {"P0", "P1"}


class ValidationError(ValueError):
    pass


@dataclass(frozen=True)
class LoadedJsonl:
    path: pathlib.Path
    records: tuple[dict[str, Any], ...]
    sha256: str


def require(record: dict[str, Any], fields: Iterable[str], label: str) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise ValidationError(f"{label}: missing fields: {','.join(missing)}")


def require_false_claim(record: dict[str, Any], label: str) -> None:
    if record.get("claim_allowed") is not False:
        raise ValidationError(f"{label}: claim_allowed must be false")


def load_jsonl(path: pathlib.Path) -> LoadedJsonl:
    raw = path.read_bytes()
    records: list[dict[str, Any]] = []
    for line_no, raw_line in enumerate(raw.splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            value = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValidationError(f"{path}:{line_no}: record must be an object")
        records.append(value)
    return LoadedJsonl(path=path, records=tuple(records), sha256=hashlib.sha256(raw).hexdigest())


def ensure_unique(records: Iterable[dict[str, Any]], key: str, label: str) -> set[str]:
    seen: set[str] = set()
    for index, record in enumerate(records, start=1):
        value = record.get(key)
        if not isinstance(value, str) or not value:
            raise ValidationError(f"{label}[{index}]: invalid {key}")
        if value in seen:
            raise ValidationError(f"{label}[{index}]: duplicate {key}={value}")
        seen.add(value)
    return seen


def validate_gaps(loaded: LoadedJsonl) -> dict[str, Any]:
    records = loaded.records
    ids = ensure_unique(records, "gap_id", "gaps")
    p0 = 0
    p1 = 0
    for index, record in enumerate(records, start=1):
        label = f"gaps[{index}]"
        require(record, ["schema", "gap_id", "priority", "urgency", "importance", "domain", "state", "token", "observation", "risk", "next_gate", "acceptance", "dependencies", "claim_allowed"], label)
        require_false_claim(record, label)
        priority = record["priority"]
        if priority not in ALLOWED_PRIORITIES:
            raise ValidationError(f"{label}: unsupported priority {priority}")
        p0 += priority == "P0"
        p1 += priority == "P1"
        if not isinstance(record["dependencies"], list):
            raise ValidationError(f"{label}: dependencies must be a list")
    for index, record in enumerate(records, start=1):
        for dependency in record["dependencies"]:
            if dependency not in ids:
                raise ValidationError(f"gaps[{index}]: unknown dependency {dependency}")
    if p0 == 0:
        raise ValidationError("gaps: at least one P0 record is required")
    return {"count": len(records), "p0": p0, "p1": p1, "sha256": loaded.sha256}


def validate_geometry(loaded: LoadedJsonl) -> dict[str, Any]:
    records = loaded.records
    ensure_unique(records, "record_id", "geometry")
    for index, record in enumerate(records, start=1):
        label = f"geometry[{index}]"
        require(record, ["schema", "record_id", "object_id", "representation", "transformation_family", "invariants", "non_invariants", "tolerance", "status", "evidence_pointers", "falsifier", "next_gate", "claim_allowed"], label)
        require_false_claim(record, label)
        if not isinstance(record["representation"], dict) or not record["representation"]:
            raise ValidationError(f"{label}: representation must be a non-empty object")
        if not isinstance(record["transformation_family"], str) or not record["transformation_family"]:
            raise ValidationError(f"{label}: transformation_family is required")
        if not isinstance(record["invariants"], list) or not record["invariants"]:
            raise ValidationError(f"{label}: at least one invariant is required")
        if not isinstance(record["evidence_pointers"], list) or not record["evidence_pointers"]:
            raise ValidationError(f"{label}: evidence_pointers cannot be empty")
        if not isinstance(record["falsifier"], str) or not record["falsifier"].strip():
            raise ValidationError(f"{label}: falsifier is required")
    return {"count": len(records), "sha256": loaded.sha256}


def validate_questions(loaded: LoadedJsonl) -> dict[str, Any]:
    records = loaded.records
    ensure_unique(records, "question_id", "questions")
    p0 = 0
    for index, record in enumerate(records, start=1):
        label = f"questions[{index}]"
        require(record, ["schema", "question_id", "priority", "category", "question", "required_for", "failure_state", "next_action", "claim_allowed"], label)
        require_false_claim(record, label)
        if record["priority"] not in ALLOWED_PRIORITIES:
            raise ValidationError(f"{label}: unsupported priority")
        p0 += record["priority"] == "P0"
        if not str(record["failure_state"]).startswith(("TOKEN_VAZIO", "FAIL")):
            raise ValidationError(f"{label}: failure_state must be TOKEN_VAZIO or FAIL")
        if not isinstance(record["required_for"], list) or not record["required_for"]:
            raise ValidationError(f"{label}: required_for cannot be empty")
    if p0 < 10:
        raise ValidationError("questions: at least ten P0 questions are required")
    return {"count": len(records), "p0": p0, "sha256": loaded.sha256}


def validate_memory(loaded: LoadedJsonl) -> dict[str, Any]:
    records = loaded.records
    ensure_unique(records, "event_id", "memory")
    for index, record in enumerate(records, start=1):
        label = f"memory[{index}]"
        require(record, ["schema", "event_id", "observed_at", "event_type", "state", "claim_allowed"], label)
        require_false_claim(record, label)
    return {"count": len(records), "sha256": loaded.sha256}


def validate(paths: dict[str, pathlib.Path]) -> dict[str, Any]:
    loaded = {name: load_jsonl(path) for name, path in paths.items()}
    for name, expected in EXPECTED_COUNTS.items():
        actual = len(loaded[name].records)
        if actual != expected:
            raise ValidationError(f"{name}: expected {expected} records, got {actual}")
    summary = {
        "schema": "rafaelia.igc-priority-validation-result.v1",
        "state": "PASS",
        "claim_allowed": False,
        "gaps": validate_gaps(loaded["gaps"]),
        "geometry": validate_geometry(loaded["geometry"]),
        "questions": validate_questions(loaded["questions"]),
        "memory": validate_memory(loaded["memory"]),
    }
    return summary


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    args = parser.parse_args(argv)
    paths = {name: args.root / path.relative_to(ROOT) for name, path in DEFAULT_PATHS.items()}
    try:
        result = validate(paths)
    except (OSError, ValidationError) as exc:
        print(f"IGC_PRIORITY_VALIDATION_FAIL: {exc}", file=sys.stderr)
        return 1
    print(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
