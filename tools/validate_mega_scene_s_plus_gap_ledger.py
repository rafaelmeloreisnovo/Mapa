#!/usr/bin/env python3
"""Fail-closed validator for the Mega Scene S+ gap ledger."""

from __future__ import annotations
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/control-plane/MEGA_SCENE_S_PLUS_GAP_LEDGER_20260824.v1.json"
DELTA = ROOT / "data/audits/TOKEN_VAZIO_REGISTRY_DELTA_20260824_MEGA_SCENE_S_PLUS.jsonl"
ALLOWED_PRIORITIES = {"P0", "P1", "P2"}
REQUIRED_ITEM_FIELDS = {
    "id", "class", "priority", "state", "known", "uncertainty", "evidence_anchor", "next_gate"
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot parse {path}: {exc}")


def main() -> int:
    data = load_json(LEDGER)
    if data.get("claim_allowed") is not False:
        fail("claim_allowed must be false")
    if data.get("coverage", {}).get("status") != "BOUNDED_CURRENT_NOT_EXHAUSTIVE":
        fail("coverage must remain bounded/non-exhaustive")
    if data.get("status") != "MATERIALIZED_BOUNDED_CURRENT_NOT_EXHAUSTIVE":
        fail("unexpected ledger status")

    items = data.get("items")
    if not isinstance(items, list) or not items:
        fail("items must be a non-empty list")

    seen: set[str] = set()
    for pos, item in enumerate(items):
        missing = REQUIRED_ITEM_FIELDS - item.keys()
        if missing:
            fail(f"item {pos} missing fields: {sorted(missing)}")
        gap_id = item["id"]
        if not isinstance(gap_id, str) or not gap_id.strip():
            fail(f"item {pos} has invalid id")
        if gap_id in seen:
            fail(f"duplicate id: {gap_id}")
        seen.add(gap_id)
        if item["priority"] not in ALLOWED_PRIORITIES:
            fail(f"invalid priority for {gap_id}: {item['priority']}")
        for field in ("class", "state", "known", "uncertainty", "evidence_anchor", "next_gate"):
            if not isinstance(item[field], str) or not item[field].strip():
                fail(f"{gap_id}: empty {field}")
        if item["class"] == "SEMANTIC_SEED":
            if item["state"] != "TOKEN_VAZIO_DEFINITION":
                fail(f"semantic seed promoted beyond TOKEN_VAZIO: {gap_id}")
            if not item.get("parable_role"):
                fail(f"semantic seed missing parable_role: {gap_id}")

    text = LEDGER.read_text(encoding="utf-8")
    if "docs.google.com/" in text or "drive.google.com/" in text:
        fail("public ledger contains a Drive locator")

    delta_ids: set[str] = set()
    for line_no, line in enumerate(DELTA.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"delta line {line_no} invalid JSON: {exc}")
        gap_id = row.get("id")
        if not gap_id or gap_id in delta_ids:
            fail(f"delta duplicate/invalid id at line {line_no}: {gap_id}")
        delta_ids.add(gap_id)
        if gap_id not in seen:
            fail(f"delta id absent from ledger: {gap_id}")
        if row.get("priority") not in ALLOWED_PRIORITIES:
            fail(f"delta invalid priority: {gap_id}")
        if not row.get("evidence_anchor") or not row.get("approval_gate"):
            fail(f"delta missing evidence/gate: {gap_id}")

    if not delta_ids:
        fail("delta registry is empty")

    print(json.dumps({
        "status": "PASS",
        "ledger_items": len(items),
        "delta_items": len(delta_ids),
        "semantic_seeds": sum(1 for item in items if item["class"] == "SEMANTIC_SEED"),
        "claim_allowed": False,
        "coverage": data["coverage"]["status"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
