#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/gaps/open_work_execution_contract.20260808.v1.json"
ALLOWED_AUTHORITY = {"OPEN_INTERNAL", "OPEN_EXTERNAL", "OPEN_HUMAN", "OPEN_GOVERNANCE", "OPEN_MIXED"}
ALLOWED_PRIORITY = {"P0", "P1", "P2"}
REQUIRED_ITEM_FIELDS = {
    "token", "priority", "authority_state", "execution_state", "risk", "contract",
    "dependencies", "authority_required", "minimal_evidence", "promotion_condition",
    "falsifier", "next_producer"
}


def fail(message: str) -> None:
    raise AssertionError(message)


def validate(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "rafaelia.open_work_execution_contract.v1":
        fail("unexpected schema")
    if data.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")
    if data.get("automatic_merge") is not False:
        fail("automatic_merge must remain false")
    items = data.get("items")
    if not isinstance(items, list) or len(items) != 14:
        fail("contract must materialize exactly the 14 authoritative open residuals")
    tokens = [row.get("token") for row in items]
    if len(tokens) != len(set(tokens)):
        fail("duplicate token")
    if any(not isinstance(token, str) or not token.startswith("TOKEN_VAZIO_") for token in tokens):
        fail("invalid token id")

    priority = Counter()
    authority = Counter()
    in_flight = 0
    for row in items:
        missing = REQUIRED_ITEM_FIELDS - set(row)
        if missing:
            fail(f"{row.get('token')}: missing fields {sorted(missing)}")
        if row["priority"] not in ALLOWED_PRIORITY:
            fail(f"{row['token']}: invalid priority")
        if row["authority_state"] not in ALLOWED_AUTHORITY:
            fail(f"{row['token']}: invalid authority_state")
        if not isinstance(row["dependencies"], list):
            fail(f"{row['token']}: dependencies must be a list")
        for field in ("contract", "authority_required", "minimal_evidence", "promotion_condition", "falsifier", "next_producer"):
            if not isinstance(row[field], str) or not row[field].strip():
                fail(f"{row['token']}: empty {field}")
        priority[row["priority"]] += 1
        authority[row["authority_state"]] += 1

        if row["execution_state"] == "IN_FLIGHT_PASS_DRAFT":
            in_flight += 1
            flight = row.get("in_flight")
            if not isinstance(flight, dict):
                fail(f"{row['token']}: in_flight metadata required")
            if not isinstance(flight.get("pr"), int) or not isinstance(flight.get("head"), str):
                fail(f"{row['token']}: PR/head required")
            if flight.get("conclusion") != "success":
                fail(f"{row['token']}: in-flight PASS must carry success conclusion")
            if row["authority_state"] not in {"OPEN_INTERNAL", "OPEN_MIXED"}:
                fail(f"{row['token']}: in-flight CI cannot satisfy external/human authority")

        if row["authority_state"] in {"OPEN_EXTERNAL", "OPEN_HUMAN"} and row["execution_state"] == "IN_FLIGHT_PASS_DRAFT":
            fail(f"{row['token']}: external/human token cannot be closed by internal draft CI")

    expected_priority = {"P0": 4, "P1": 7, "P2": 3}
    if dict(priority) != expected_priority:
        fail(f"priority counts mismatch: {dict(priority)}")
    if in_flight != 2:
        fail(f"expected 2 in-flight draft PASS items, got {in_flight}")

    counts = data.get("counts", {})
    if counts.get("authoritative_open_tokens") != 14:
        fail("count.authoritative_open_tokens mismatch")
    if counts.get("IN_FLIGHT_PASS_DRAFT") != 2:
        fail("count.IN_FLIGHT_PASS_DRAFT mismatch")

    # Dependency ordering: only declared open tokens or explicitly successor tokens are accepted.
    known = set(tokens)
    allowed_external_successors = {"TOKEN_VAZIO_ACT_DR6_LCDM_POSTERIOR_CHAIN_REPRODUCTION"}
    for row in items:
        for dep in row["dependencies"]:
            if dep not in known and dep not in allowed_external_successors:
                fail(f"{row['token']}: undeclared dependency {dep}")

    return {
        "state": "PASS",
        "claim_allowed": False,
        "tokens": len(items),
        "priority": dict(priority),
        "authority": dict(authority),
        "in_flight_pass_draft": in_flight,
    }


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT
    try:
        result = validate(path)
    except Exception as exc:
        print(json.dumps({"state": "FAIL", "error": f"{type(exc).__name__}: {exc}"}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
