#!/usr/bin/env python3
"""Fail-closed validator for the RAFAELIA Operational Core 94 registry."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^OC94-(\d{3})$")
REQUIRED_AXES = ("source", "test", "environment", "receipt", "ecosystem_function")


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/core/operational-core-94.v1.json")
    data = json.loads(path.read_text(encoding="utf-8"))

    if data.get("schema") != "rafaelia.operational-core-94.v1":
        fail("unexpected schema")
    if data.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")
    if data.get("expected_total") != 94:
        fail("expected_total must be 94")

    items = data.get("items")
    if not isinstance(items, list):
        fail("items must be a list")
    if data.get("identified_count") != len(items):
        fail("identified_count does not match items length")
    if data.get("unitemized_count") != 94 - len(items):
        fail("unitemized_count does not close expected_total")

    seen_ids: set[str] = set()
    seen_titles: set[str] = set()
    numeric_ids: list[int] = []
    for item in items:
        item_id = item.get("id")
        match = ID_RE.fullmatch(item_id or "")
        if not match:
            fail(f"invalid item id: {item_id!r}")
        if item_id in seen_ids:
            fail(f"duplicate item id: {item_id}")
        seen_ids.add(item_id)
        numeric_ids.append(int(match.group(1)))

        title = item.get("title")
        if not isinstance(title, str) or not title.strip():
            fail(f"missing title for {item_id}")
        if title in seen_titles:
            fail(f"duplicate title: {title}")
        seen_titles.add(title)

        if item.get("priority") not in {"P0", "P1", "P2", "TV"}:
            fail(f"invalid priority for {item_id}")
        if item.get("claim_allowed") is not False:
            fail(f"item {item_id} promoted claim")
        for axis in REQUIRED_AXES:
            value = item.get(axis)
            if not isinstance(value, dict) or not value:
                fail(f"item {item_id} missing axis {axis}")

    if numeric_ids != list(range(1, len(items) + 1)):
        fail("identified IDs must be contiguous from OC94-001")

    gap = data.get("unitemized_range", {})
    if gap.get("count") != data.get("unitemized_count"):
        fail("unitemized_range count mismatch")
    if gap.get("state") != "TOKEN_VAZIO_ITEMIZATION_PENDING":
        fail("unitemized range must remain TOKEN_VAZIO_ITEMIZATION_PENDING")
    expected_first = f"OC94-{len(items)+1:03d}"
    if gap.get("first_id") != expected_first or gap.get("last_id") != "OC94-094":
        fail("unitemized range boundaries mismatch")

    print(json.dumps({
        "status": "PASS",
        "expected_total": 94,
        "identified_count": len(items),
        "unitemized_count": 94 - len(items),
        "required_axes": list(REQUIRED_AXES),
        "claim_allowed": False
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
