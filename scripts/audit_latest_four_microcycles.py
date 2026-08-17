#!/usr/bin/env python3
"""Emit a fail-closed audit projection for the four newest RAFAELIA microcycles."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.append_microcycle_index import MicrocycleIndexError, load_object, validate_index

AUDIT_SCHEMA = "rafaelia.adaptive-cycle-latest4-audit.v1"
REQUIRED_ENTRY_FIELDS = (
    "run_id",
    "cycle_id",
    "n_mod_42",
    "phase",
    "decision",
    "previous_entry_sha256",
    "entry_sha256",
    "receipt_sha256",
    "claim_allowed",
)


def build_audit(index: dict[str, Any]) -> dict[str, Any]:
    """Validate the complete index, then expose a stable latest-four projection."""
    validate_index(index)
    latest = index["latest_four"]
    if len(latest) != 4:
        raise MicrocycleIndexError(
            f"latest_four_count must be 4 after established history; observed {len(latest)}"
        )

    projected: list[dict[str, Any]] = []
    for position, entry in enumerate(latest):
        missing = [field for field in REQUIRED_ENTRY_FIELDS if field not in entry]
        if missing:
            raise MicrocycleIndexError(
                f"latest_four[{position}] missing required fields: {', '.join(missing)}"
            )
        if entry["claim_allowed"] is not False:
            raise MicrocycleIndexError("latest-four entry attempted claim promotion")
        if entry["decision"] != "EXECUTED_READ_ONLY":
            raise MicrocycleIndexError("latest-four entry is not EXECUTED_READ_ONLY")
        if not isinstance(entry["n_mod_42"], int) or not 0 <= entry["n_mod_42"] < 42:
            raise MicrocycleIndexError("latest-four n_mod_42 outside [0, 42)")

        projected.append(
            {
                "run_id": str(entry["run_id"]),
                "cycle_id": entry["cycle_id"],
                "n_mod_42": entry["n_mod_42"],
                "phase": entry["phase"],
                "decision": entry["decision"],
                "previous_entry_sha256": entry["previous_entry_sha256"],
                "entry_sha256": entry["entry_sha256"],
                "receipt_sha256": entry["receipt_sha256"],
                "latest_four_count": 4,
                "claim_allowed": False,
            }
        )

    for previous, current in zip(projected, projected[1:]):
        if current["previous_entry_sha256"] != previous["entry_sha256"]:
            raise MicrocycleIndexError("latest-four predecessor relation is broken")

    return {
        "schema": AUDIT_SCHEMA,
        "decision": "VERIFIED_LATEST_FOUR_READ_ONLY",
        "latest_four_count": 4,
        "entry_count": index["entry_count"],
        "index_sha256": index["index_sha256"],
        "chain_continuity": "VERIFIED_COMPLETE_INDEX_AND_LATEST_FOUR",
        "claim_allowed": False,
        "automatic_mutation": False,
        "automatic_merge": False,
        "entries": projected,
        "boundaries": {
            "hash_is_not_truth": True,
            "schedule_is_not_evidence": True,
            "ci_is_not_physical_runtime": True,
            "index_is_not_scientific_evidence": True,
            "parabola_is_not_mechanism": True,
            "semantic_pattern_is_not_physical_law": True,
        },
        "token_vazio": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        audit = build_audit(load_object(args.index))
    except (OSError, json.JSONDecodeError, MicrocycleIndexError) as error:
        blocked = {
            "schema": AUDIT_SCHEMA,
            "decision": "BLOCKED_TOKEN_VAZIO",
            "claim_allowed": False,
            "token_vazio": ["LATEST_FOUR_ANTI_REGRESSION_EVIDENCE"],
            "error": f"{type(error).__name__}: {error}",
        }
        print(json.dumps(blocked, ensure_ascii=False, indent=2))
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
