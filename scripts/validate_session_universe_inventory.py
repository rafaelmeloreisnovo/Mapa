#!/usr/bin/env python3
"""Validador stdlib-only do inventário SESSION-UNIVERSE-456."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


BLOCKED_CLOSURE_STATE = "TOKEN_VAZIO_FORMAL_PROOF"


def load_inventory(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("inventory root must be an object")
    return data


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(data: dict[str, Any]) -> list[str]:
    checks: list[str] = []
    require(data.get("event_id") == "SESSION-UNIVERSE-456-20260728", "wrong event_id")
    require(data["governance"]["claim_allowed"] is False, "global claim gate must be false")
    require(data["governance"]["review_policy"] == "ONE_BY_ONE", "review policy must be ONE_BY_ONE")
    require(data["governance"]["missing_data_policy"] == "TOKEN_VAZIO", "missing data policy must be TOKEN_VAZIO")
    checks.append("governance")

    registry = data["atomic_registry"]
    atom_ids = registry["ids"]
    default = registry["default"]
    expected_ids = [f"ATOM-{i:03d}" for i in range(1, 417)]
    require(len(atom_ids) == 416, "atomic entity count must be 416")
    require(atom_ids == expected_ids, "atomic IDs not contiguous")
    require(len(set(atom_ids)) == 416, "atomic IDs must be unique")
    require(default["name"] is None, "missing atom names must stay null")
    require(default["reviewed"] is False, "atoms cannot be pre-reviewed")
    require(default["state"] == "TOKEN_VAZIO_SOURCE_ENUMERATION_PENDING", "wrong atom state")
    require(default["claim_allowed"] is False, "atom claim gate opened")
    checks.append("416_atomic_slots")

    require(len(data["clusters"]) == 8, "cluster count must be 8")
    require(len(data["results"]) == 24, "result count must be 24")
    require(len(data["operators"]) == 3, "operator count must be 3")
    require(len(data["transformer_seeds"]) == 5, "seed count must be 5")
    require(len(data["meta_syntheses"]) == 1, "meta count must be 1")
    checks.append("category_counts")

    closures = data["results"][:8]
    require(all(item["state"] == BLOCKED_CLOSURE_STATE for item in closures), "an alleged closure was promoted")
    require(all(item["claim_allowed"] is False for item in closures), "closure claim gate opened")
    roadmaps = data["results"][8:]
    require(all(item["name"] is None for item in roadmaps), "missing roadmap names must not be invented")
    require(all(item["state"] == "TOKEN_VAZIO_MISSING_ITEMIZATION" for item in roadmaps), "wrong roadmap state")
    checks.append("epistemic_gates")

    counts = data["declared_counts"]
    require(counts["atomic_initial"] + counts["atomic_extended"] == counts["atomic_total"] == 416, "atomic arithmetic mismatch")
    derived = (
        counts["clusters"]
        + counts["alleged_complete_closures"]
        + counts["proof_roadmaps"]
        + counts["operators"]
        + counts["transformer_seeds"]
    )
    require(derived == counts["derived_subtotal_excluding_meta"] == 40, "derived subtotal mismatch")
    require(counts["atomic_total"] + derived == counts["grand_total_excluding_meta"] == 456, "source total mismatch")
    require(counts["grand_total_excluding_meta"] + counts["meta_syntheses"] == counts["grand_total_including_meta"] == 457, "meta-inclusive total mismatch")
    require(data["counting_convention"]["state"] == "TOKEN_VAZIO_COUNTING_CONVENTION", "count ambiguity not preserved")
    checks.append("count_reconciliation")

    combinatorics = data["combinatorics"]
    require(combinatorics["pairwise_combinations"] == math.comb(416, 2) == 86320, "pairwise count mismatch")
    require(int(combinatorics["powerset_exact"]) == 2**416, "powerset mismatch")
    checks.append("combinatorics")

    queue_expected = (
        len(atom_ids)
        + len(data["results"])
        + len(data["operators"])
        + len(data["transformer_seeds"])
        + len(data["meta_syntheses"])
    )
    require(queue_expected == 449, "review queue arithmetic mismatch")
    require(data["review_queue"]["pending"] == queue_expected, "review queue pending mismatch")
    require(data["review_queue"]["completed"] == 0, "review queue must start at zero")
    require(data["review_queue"]["current_cursor"] == "ATOM-001", "review cursor must start at ATOM-001")
    checks.append("review_queue")

    for family in ("results", "operators", "transformer_seeds", "meta_syntheses"):
        require(all(item["claim_allowed"] is False for item in data[family]), f"{family} claim gate opened")
    require(data["exhaustiveness_claim"]["claim_allowed"] is False, "exhaustiveness claim gate opened")
    checks.append("global_fail_closed")
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "inventory",
        nargs="?",
        type=Path,
        default=Path("data/sementeira/inventories/session-universe-456.v1.json"),
    )
    args = parser.parse_args()
    try:
        checks = validate(load_inventory(args.inventory))
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"PASS: {len(checks)}/{len(checks)} checks")
    for check in checks:
        print(f"PASS {check}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
