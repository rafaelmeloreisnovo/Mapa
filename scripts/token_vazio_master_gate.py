#!/usr/bin/env python3
"""Fail-closed validator for bounded TOKEN_VAZIO current-state snapshots.

Stdlib only. This gate validates structural anti-regression properties; it does
not promote scientific, physical-runtime, security-remediation or provider-wide
coverage claims.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


class GateError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    require(isinstance(data, dict), "root must be a JSON object")
    return data


def validate(data: dict[str, Any]) -> None:
    require(data.get("schema") == "rafaelia.token-vazio-master-current-bounded/v1", "unexpected schema")
    require(data.get("claim_allowed") is False, "claim_allowed must remain false")

    coverage = data.get("coverage")
    require(isinstance(coverage, dict), "coverage object missing")
    require(coverage.get("status") == "BOUNDED_NOT_EXHAUSTIVE", "coverage must remain bounded/non-exhaustive")
    require(bool(coverage.get("forbidden_interpretation")), "forbidden_interpretation missing")

    items = data.get("items")
    require(isinstance(items, list) and items, "items must be a non-empty list")

    ids: set[str] = set()
    resolved = partial = open_or_missing = 0

    for index, item in enumerate(items):
        require(isinstance(item, dict), f"item[{index}] must be an object")
        item_id = item.get("id")
        state = item.get("current_state")
        require(isinstance(item_id, str) and item_id, f"item[{index}] id missing")
        require(item_id not in ids, f"duplicate item id: {item_id}")
        ids.add(item_id)
        require(isinstance(state, str) and state, f"{item_id}: current_state missing")
        require(bool(item.get("class")), f"{item_id}: class missing")
        require(bool(item.get("priority")), f"{item_id}: priority missing")
        require(state != "PASS", f"{item_id}: bare PASS is forbidden in reconciliation state")

        if state.startswith("RESOLVED"):
            resolved += 1
            evidence = item.get("evidence")
            require(isinstance(evidence, dict) and evidence, f"{item_id}: resolved state requires evidence")
            require(evidence.get("conclusion") == "success", f"{item_id}: resolved evidence must carry observed success")
            require(bool(evidence.get("head_sha")), f"{item_id}: head_sha missing")
            require(bool(evidence.get("merge_commit_sha")), f"{item_id}: merge_commit_sha missing")
            require(bool(evidence.get("workflow_run")), f"{item_id}: workflow_run missing")
        elif state.startswith("PARTIAL"):
            partial += 1
            remaining = item.get("remaining")
            require(isinstance(remaining, str) and "TOKEN_VAZIO" in remaining, f"{item_id}: partial state must expose remaining TOKEN_VAZIO")
            require(bool(item.get("next_gate")), f"{item_id}: partial state requires next_gate")
        else:
            open_or_missing += 1
            require(bool(item.get("next_gate")), f"{item_id}: unresolved state requires next_gate")

    counts = data.get("counts")
    require(isinstance(counts, dict), "counts object missing")
    require(counts.get("items_in_bounded_view") == len(items), "items_in_bounded_view mismatch")
    require(counts.get("resolved_evidenced") == resolved, "resolved_evidenced mismatch")
    require(counts.get("partial_evidenced") == partial, "partial_evidenced mismatch")
    require(counts.get("open_or_missing") == open_or_missing, "open_or_missing mismatch")
    require(counts.get("ecosystem_total") == "TOKEN_VAZIO_NOT_PROVEN", "ecosystem total must remain explicitly unproven")

    rule = data.get("promotion_rule", "")
    require("Only exact evidence closes the exact dimension" in rule, "exact-evidence promotion rule missing")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} SNAPSHOT.json", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        validate(load(path))
    except (OSError, json.JSONDecodeError, GateError) as exc:
        print(f"FAIL {path}: {exc}", file=sys.stderr)
        return 1
    print(f"PASS {path}: bounded TOKEN_VAZIO reconciliation is structurally coherent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
