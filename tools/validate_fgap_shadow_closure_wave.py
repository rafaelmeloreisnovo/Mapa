#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ALLOWED_STATES = {"TOKEN_VAZIO", "OBSERVED", "TESTED", "EVIDENCED", "RELEASED", "BLOCKED"}
ALLOWED_URGENCY = {"P0", "P1", "P2"}
REQUIRED_ITEM = {"gap_id", "edge", "urgency", "state", "risk", "evidence_required", "next_action"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/gaps/fgap_shadow_closure_wave.20260811.v1.json")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot parse {path}: {exc}")

    if data.get("schema") != "RAFAELIA_FGAP_SHADOW_CLOSURE_WAVE_V1":
        fail("schema mismatch")
    if data.get("mode") != "APPEND_ONLY_DELTA":
        fail("mode must be APPEND_ONLY_DELTA")
    if data.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")
    if not data.get("base_commit") or len(data["base_commit"]) != 40:
        fail("base_commit must be a 40-char commit SHA")

    groups = data.get("groups")
    if not isinstance(groups, list) or len(groups) != 7:
        fail("exactly seven shadow groups are required")

    group_ids = set()
    gap_ids = set()
    p0_count = 0
    token_vazio_count = 0

    for group in groups:
        gid = group.get("id")
        if not gid or gid in group_ids:
            fail(f"invalid/duplicate group id: {gid}")
        group_ids.add(gid)
        if group.get("governance_gap") != "CLOSED_BY_THIS_DELTA":
            fail(f"{gid}: governance gap must be structurally closed by delta")
        items = group.get("items")
        if not isinstance(items, list) or not items:
            fail(f"{gid}: items must be a non-empty list")

        for item in items:
            missing = REQUIRED_ITEM - item.keys()
            if missing:
                fail(f"{gid}: item missing fields {sorted(missing)}")
            gap_id = item["gap_id"]
            if gap_id in gap_ids:
                fail(f"duplicate gap_id: {gap_id}")
            gap_ids.add(gap_id)
            if item["state"] not in ALLOWED_STATES:
                fail(f"{gap_id}: invalid state {item['state']}")
            if item["urgency"] not in ALLOWED_URGENCY:
                fail(f"{gap_id}: invalid urgency {item['urgency']}")
            if item["urgency"] == "P0":
                p0_count += 1
            if item["state"] == "TOKEN_VAZIO":
                token_vazio_count += 1
            evidence = item["evidence_required"]
            if not isinstance(evidence, list) or not evidence or any(not isinstance(x, str) or not x for x in evidence):
                fail(f"{gap_id}: evidence_required must be a non-empty string list")
            if not isinstance(item["next_action"], str) or not item["next_action"].strip():
                fail(f"{gap_id}: next_action required")

    invariants = set(data.get("invariants", []))
    mandatory = {
        "absence_of_evidence_is_not_evidence_of_absence",
        "no_token_vazio_promotion_without_evidence",
        "append_only_history_no_rewrite",
    }
    if not mandatory.issubset(invariants):
        fail("mandatory fail-closed invariants missing")

    print("PASS: RAFAELIA_FGAP_SHADOW_CLOSURE_WAVE_V1")
    print(f"groups={len(groups)} gaps={len(gap_ids)} P0={p0_count} TOKEN_VAZIO={token_vazio_count}")


if __name__ == "__main__":
    main()
