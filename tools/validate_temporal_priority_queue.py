#!/usr/bin/env python3
"""Fail-closed validator for the current RAFAELIA uncertainty/gap routing layer.

This validator does not close external gates. It prevents stale, untyped, duplicate,
or under-specified gaps from becoming current routing authority.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

HEX40 = re.compile(r"^[0-9a-f]{40}$")
PRIORITIES = {"P0", "P1", "P2", "P3"}
REQUIRED_OPEN_FIELDS = {
    "priority",
    "id",
    "state",
    "scope",
    "authority",
    "evidence",
    "uncertainty",
    "falsifier",
    "closure_gate",
    "next_action",
}
FORBIDDEN_ACTIVE_IDS = {
    "TV-ROOT-PNG-STRUCTURAL-CI-BLOCKER",
    "TV-GENESIS-SEAL-EXACT-SHA256",
    "TV-RAW018-CURRENT-BYTE-CUSTODY",
    "TV-RAW018-PID-COMMITMENT-ALGORITHM-PROVENANCE",
    "TV-RAW018-CHRONOLOGICAL-COMMITMENT-CURRENT-REPRODUCTION",
    "TOKEN_VAZIO_RUNNER",
}
MANDATORY_ACTIVE_IDS = {
    "P0-MAIN-SERVER-ENFORCEMENT",
    "P0-INDEPENDENT-APPROVAL",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, str) and item.strip() for item in value
    )


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if data.get("schema") != "rafaelia.token-vazio-priority-queue.v3":
        fail(errors, "SCHEMA_MISMATCH")
    if data.get("claim_allowed") is not False:
        fail(errors, "CLAIM_ALLOWED_MUST_BE_FALSE")
    if data.get("release_allowed") is not False:
        fail(errors, "RELEASE_ALLOWED_MUST_BE_FALSE")
    if data.get("promotion_allowed") is not False:
        fail(errors, "PROMOTION_ALLOWED_MUST_BE_FALSE")
    if data.get("history_policy") != "APPEND_ONLY_PRESERVE_PREDECESSOR":
        fail(errors, "APPEND_ONLY_HISTORY_POLICY_REQUIRED")
    if data.get("latest_evidence_wins_for_routing") is not True:
        fail(errors, "LATEST_EVIDENCE_ROUTING_REQUIRED")
    if data.get("unresolved_untyped_gaps") != 0:
        fail(errors, "UNTYPED_GAPS_MUST_BE_ZERO")

    source_sha = data.get("source_main_sha")
    if not isinstance(source_sha, str) or not HEX40.fullmatch(source_sha):
        fail(errors, "SOURCE_MAIN_SHA_INVALID")

    active = data.get("active_items")
    resolved = data.get("resolved_or_superseded")
    if not isinstance(active, list):
        fail(errors, "ACTIVE_ITEMS_NOT_LIST")
        active = []
    if not isinstance(resolved, list):
        fail(errors, "RESOLVED_ITEMS_NOT_LIST")
        resolved = []

    ids: set[str] = set()
    active_ids: set[str] = set()
    for index, item in enumerate(active):
        prefix = f"active_items[{index}]"
        if not isinstance(item, dict):
            fail(errors, f"{prefix}:NOT_OBJECT")
            continue
        missing = REQUIRED_OPEN_FIELDS - item.keys()
        if missing:
            fail(errors, f"{prefix}:MISSING_FIELDS:{','.join(sorted(missing))}")
        gap_id = item.get("id")
        if not isinstance(gap_id, str) or not gap_id.strip():
            fail(errors, f"{prefix}:INVALID_ID")
            continue
        if gap_id in ids:
            fail(errors, f"DUPLICATE_ID:{gap_id}")
        ids.add(gap_id)
        active_ids.add(gap_id)
        if item.get("priority") not in PRIORITIES:
            fail(errors, f"{gap_id}:INVALID_PRIORITY")
        state = item.get("state")
        if not isinstance(state, str) or not state.strip():
            fail(errors, f"{gap_id}:INVALID_STATE")
        for field in ("scope", "evidence", "closure_gate"):
            if not nonempty_list(item.get(field)):
                fail(errors, f"{gap_id}:{field.upper()}_EMPTY")
        for field in ("authority", "uncertainty", "falsifier", "next_action"):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                fail(errors, f"{gap_id}:{field.upper()}_EMPTY")

    stale = sorted(active_ids & FORBIDDEN_ACTIVE_IDS)
    for gap_id in stale:
        fail(errors, f"STALE_RESOLVED_GAP_REACTIVATED:{gap_id}")
    missing_mandatory = sorted(MANDATORY_ACTIVE_IDS - active_ids)
    for gap_id in missing_mandatory:
        fail(errors, f"MANDATORY_P0_MISSING:{gap_id}")

    resolved_ids: set[str] = set()
    for index, item in enumerate(resolved):
        prefix = f"resolved_or_superseded[{index}]"
        if not isinstance(item, dict):
            fail(errors, f"{prefix}:NOT_OBJECT")
            continue
        gap_id = item.get("id")
        state = item.get("state")
        evidence = item.get("evidence")
        if not isinstance(gap_id, str) or not gap_id.strip():
            fail(errors, f"{prefix}:INVALID_ID")
            continue
        if gap_id in ids:
            fail(errors, f"ID_ACTIVE_AND_RESOLVED:{gap_id}")
        if gap_id in resolved_ids:
            fail(errors, f"DUPLICATE_RESOLVED_ID:{gap_id}")
        resolved_ids.add(gap_id)
        ids.add(gap_id)
        if not isinstance(state, str) or not state.strip():
            fail(errors, f"{gap_id}:INVALID_RESOLVED_STATE")
        if not nonempty_list(evidence):
            fail(errors, f"{gap_id}:RESOLUTION_EVIDENCE_EMPTY")

    absent_resolution_rows = sorted(FORBIDDEN_ACTIVE_IDS - resolved_ids)
    for gap_id in absent_resolution_rows:
        fail(errors, f"EXPECTED_RESOLUTION_ROW_MISSING:{gap_id}")

    invariants = data.get("invariants")
    if not nonempty_list(invariants):
        fail(errors, "INVARIANTS_EMPTY")
    else:
        required_invariants = {
            "TOKEN_VAZIO != 0",
            "resolved != deleted_history",
            "latest_evidence_wins_for_current_routing",
        }
        missing = sorted(required_invariants - set(invariants))
        for invariant in missing:
            fail(errors, f"REQUIRED_INVARIANT_MISSING:{invariant}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="data/control-plane/TOKEN_VAZIO_PRIORITY_QUEUE.v3.json",
    )
    args = parser.parse_args()
    path = Path(args.path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: unable to read/parse {path}: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("FAIL: queue root must be an object", file=sys.stderr)
        return 2

    errors = validate(data)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        print(f"RESULT: FAIL ({len(errors)} finding(s))", file=sys.stderr)
        return 1

    print(f"PASS: {path}")
    print(f"active_items={len(data['active_items'])}")
    print(f"resolved_or_superseded={len(data['resolved_or_superseded'])}")
    print("claim_allowed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
