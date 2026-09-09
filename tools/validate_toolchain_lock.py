#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED = ["compiler", "compiler_version", "linker", "linker_version", "target", "abi", "flags", "source_date_epoch"]


def die(msg):
    print(json.dumps({"status": "FAIL", "error": msg, "claim_allowed": False}, sort_keys=True))
    raise SystemExit(1)


doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
for key in REQUIRED:
    if key not in doc or doc[key] in (None, "", "TOKEN_VAZIO"):
        die(f"missing exact toolchain field: {key}")
flags = doc["flags"]
if not isinstance(flags, list) or not flags:
    die("flags must be non-empty array")
if len(flags) != len(set(flags)):
    die("duplicate flags")
if doc.get("claim_allowed") is not False:
    die("claim_allowed must remain false")
print(json.dumps({"status": "PASS", "target": doc["target"], "abi": doc["abi"], "flags": len(flags), "claim_allowed": False}, sort_keys=True))
