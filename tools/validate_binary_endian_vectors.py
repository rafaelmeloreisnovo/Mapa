#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def unsigned_le(data):
    return sum(byte << (8 * index) for index, byte in enumerate(data))


doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
failures = []
for row in doc.get("vectors", []):
    data = bytes.fromhex(row["hex_le"])
    got = unsigned_le(data)
    if got != row["unsigned_value"]:
        failures.append(row["id"])
    if row.get("width_bits") and len(data) * 8 != row["width_bits"]:
        failures.append(row["id"] + ":width")
print(json.dumps({"status": "PASS" if not failures else "FAIL", "vectors": len(doc.get("vectors", [])), "failures": failures, "claim_allowed": False}, sort_keys=True))
raise SystemExit(0 if not failures else 1)
