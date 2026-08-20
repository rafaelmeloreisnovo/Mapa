#!/usr/bin/env python3
"""Fail-closed record gate for RAFAELIA operational-gap records.

Canonical v1 records are validated by operational_gap_assurance.py.
Legacy records are never silently upgraded to canonical PASS. They are accepted
only as historical evidence when claim_allowed is false, and are reported as
TOKEN_VAZIO_REVALIDATION_REQUIRED until a superseding canonical record/receipt
exists.

A very small explicit quarantine set handles records that used the canonical
schema label before all current subcontracts were enforced. This is intentionally
allowlist-only: new malformed canonical records still fail.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from operational_gap_assurance import build_report

CANONICAL = "rafaelia.operational-gap-assurance/v1"
LEGACY_SCHEMAS = {
    "RAFAELIA_OPERATIONAL_GAP_V1",
    "rafaelia.operational-gap.v1",
}
HISTORICAL_CANONICAL_QUARANTINE = {
    "gap:mapa:federated-broker:hmac-provenance:20260819",
}


def emit_historical(record: dict, source_profile: str) -> int:
    claim_allowed = record.get("claim_allowed")
    if claim_allowed is not False:
        print(json.dumps({
            "schema_version": "rafaelia.operational-gap-legacy-gate/v1",
            "source_profile": source_profile,
            "gap_id": record.get("gap_id"),
            "valid": False,
            "legacy_accepted": False,
            "errors": ["historical records require claim_allowed=false"],
            "closure_result": "BLOCKED",
        }, indent=2, sort_keys=True, ensure_ascii=False))
        return 2

    print(json.dumps({
        "schema_version": "rafaelia.operational-gap-legacy-gate/v1",
        "source_profile": source_profile,
        "gap_id": record.get("gap_id"),
        "valid": True,
        "legacy_accepted": True,
        "claim_allowed": False,
        "status": record.get("status", record.get("state", "TOKEN_VAZIO")),
        "closure_result": "TOKEN_VAZIO_REVALIDATION_REQUIRED",
        "next_probe": record.get("next_probe"),
        "anti_promotion_invariant": "HISTORICAL_ACCEPTED_NE_CANONICAL_VALIDATED_NE_CLOSED_BY_EVIDENCE",
    }, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: operational_gap_record_gate.py RECORD.json", file=sys.stderr)
        return 64

    path = Path(sys.argv[1])
    record = json.loads(path.read_text(encoding="utf-8"))

    if record.get("schema_version") == CANONICAL:
        report = build_report(record)
        if report["valid"]:
            print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
            return 0
        if record.get("gap_id") in HISTORICAL_CANONICAL_QUARANTINE:
            return emit_historical(record, "CANONICAL_LABEL_PRE_CURRENT_SUBCONTRACTS")
        print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
        return 2

    legacy_schema = record.get("schema")
    if legacy_schema in LEGACY_SCHEMAS:
        return emit_historical(record, legacy_schema)

    print(json.dumps({
        "schema_version": "rafaelia.operational-gap-legacy-gate/v1",
        "gap_id": record.get("gap_id"),
        "valid": False,
        "errors": ["unknown operational-gap schema"],
        "observed_schema_version": record.get("schema_version"),
        "observed_schema": record.get("schema"),
    }, indent=2, sort_keys=True, ensure_ascii=False))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
