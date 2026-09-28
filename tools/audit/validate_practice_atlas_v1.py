#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ALLOWED_STATES = {
    "REFERENCE", "IMPLEMENTED", "IMPLEMENTED_UNTESTED", "PASS", "FAIL",
    "NOT_RUN", "PENDING", "AUDIT", "TOKEN_VAZIO"
}

def fail(msg):
    print(json.dumps({"state": "FAIL", "error": msg}, ensure_ascii=False))
    raise SystemExit(1)

def main():
    if len(sys.argv) != 2:
        fail("usage: validate_practice_atlas_v1.py <atlas.json>")
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "RAFAELIA_PRACTICE_ATLAS_V1":
        fail("unexpected schema")
    if data.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")
    state = data.get("state")
    if state not in ALLOWED_STATES:
        fail("invalid state")
    areas = data.get("areas")
    if not isinstance(areas, list) or not areas:
        fail("areas must be a non-empty list")
    ids = set()
    required = {"id","intent","authority","source_min","implementation_refs","evidence_rule","gap","next"}
    for idx, area in enumerate(areas):
        missing = sorted(required - set(area))
        if missing:
            fail(f"area[{idx}] missing {missing}")
        if area["id"] in ids:
            fail(f"duplicate area id: {area['id']}")
        ids.add(area["id"])
        if not area["authority"]:
            fail(f"{area['id']}: empty authority; use typed TOKEN_VAZIO")
        src = area["source_min"]
        if not isinstance(src, list) or not (1 <= len(src) <= 3):
            fail(f"{area['id']}: source_min must contain 1..3 entries")
        for key in ("intent","evidence_rule","gap","next"):
            if not isinstance(area[key], str) or not area[key].strip():
                fail(f"{area['id']}: {key} must be non-empty")
    print(json.dumps({
        "state": "PASS",
        "schema": data["schema"],
        "areas": len(areas),
        "unique_ids": len(ids),
        "claim_allowed": data["claim_allowed"]
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
