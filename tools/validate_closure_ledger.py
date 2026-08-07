#!/usr/bin/env python3
"""Fail-closed validator for the RAFAELIA closure ledger.

Dependency-free by design: Python stdlib only.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/gaps/closure_ledger.20260807.jsonl"
EXPECTED_RECORDS = 15
REQUIRED = {"schema", "event_id", "gap_id", "state", "claim_allowed", "F_ok", "F_gap", "F_next"}


class ValidationError(ValueError):
    pass


def load() -> tuple[list[dict[str, Any]], str]:
    raw = LEDGER.read_bytes()
    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(raw.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"line {line_no}: invalid JSON: {exc}") from exc
        if not isinstance(item, dict):
            raise ValidationError(f"line {line_no}: record must be object")
        records.append(item)
    return records, hashlib.sha256(raw).hexdigest()


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(records: list[dict[str, Any]]) -> dict[str, Any]:
    if len(records) != EXPECTED_RECORDS:
        raise ValidationError(f"expected {EXPECTED_RECORDS} records, got {len(records)}")

    event_ids: set[str] = set()
    gap_ids: set[str] = set()
    allowed_true = 0

    for index, record in enumerate(records, start=1):
        missing = sorted(REQUIRED - record.keys())
        if missing:
            raise ValidationError(f"record {index}: missing {','.join(missing)}")
        if record.get("schema") != "rafaelia.closure-ledger.v1":
            raise ValidationError(f"record {index}: unsupported schema")

        event_id = record["event_id"]
        gap_id = record["gap_id"]
        if not nonempty(event_id) or event_id in event_ids:
            raise ValidationError(f"record {index}: invalid/duplicate event_id")
        if not nonempty(gap_id) or gap_id in gap_ids:
            raise ValidationError(f"record {index}: invalid/duplicate gap_id")
        event_ids.add(event_id)
        gap_ids.add(gap_id)

        for field in ("state", "F_ok", "F_gap", "F_next"):
            if not nonempty(record[field]):
                raise ValidationError(f"record {index}: empty {field}")

        allowed = record["claim_allowed"]
        if not isinstance(allowed, bool):
            raise ValidationError(f"record {index}: claim_allowed must be boolean")

        if allowed:
            allowed_true += 1
            if record["state"] != "CLOSED_PROVEN_SCOPED":
                raise ValidationError(f"record {index}: true claim requires CLOSED_PROVEN_SCOPED")
            if not nonempty(record.get("scope")):
                raise ValidationError(f"record {index}: scoped true claim requires scope")
            evidence = record.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                raise ValidationError(f"record {index}: scoped true claim requires evidence")
            if "observed_total" not in record:
                raise ValidationError(f"record {index}: scoped inventory claim requires observed_total")
        else:
            state = record["state"]
            permitted = (
                state.startswith("TOKEN_VAZIO_TYPED")
                or state.startswith("REDUCED")
                or state.startswith("OPEN_ACTIONABLE")
                or state.startswith("BLOCKED_EXTERNAL")
            )
            if not permitted:
                raise ValidationError(f"record {index}: false claim has unsupported state {state}")

    if allowed_true != 1:
        raise ValidationError(f"expected exactly one scoped claim_allowed=true record, got {allowed_true}")

    required_gaps = {f"IGC-GAP-{i:03d}" for i in range(1, 13)}
    missing_gaps = sorted(required_gaps - gap_ids)
    if missing_gaps:
        raise ValidationError(f"missing IGC gaps: {','.join(missing_gaps)}")

    return {
        "schema": "rafaelia.closure-ledger-validation.v1",
        "state": "PASS",
        "records": len(records),
        "scoped_claims_allowed": allowed_true,
        "igc_gap_coverage": "12/12",
    }


def main() -> int:
    try:
        records, sha256 = load()
        result = validate(records)
        result["ledger_sha256"] = sha256
    except (OSError, ValidationError) as exc:
        print(f"CLOSURE_LEDGER_FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
