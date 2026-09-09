#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED = [
    "ROOT_MANIFEST",
    "CANONICAL_OBJECT_REGISTRY",
    "SOURCE_SET",
    "TOOLCHAIN_LOCK",
    "SCHEMAS",
    "GOLDEN_VECTORS",
    "BUILD_RECIPES",
    "RUNTIME_RECIPES",
    "EVIDENCE_INDEX",
    "MEMORY_INDEX",
]


def die(msg, missing=None):
    print(json.dumps({"status": "FAIL", "error": msg, "missing": missing or [], "claim_allowed": False}, sort_keys=True))
    raise SystemExit(1)


doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
classes = doc.get("classes", {})
missing = [key for key in REQUIRED if key not in classes]
if missing:
    die("missing rebuild classes", missing)

not_pass = [key for key in REQUIRED if classes[key].get("state") != "PASS"]
if not_pass:
    print(json.dumps({"status": "INCOMPLETE", "not_pass": not_pass, "clean_room_rebuild_closed": False, "claim_allowed": False}, sort_keys=True))
    raise SystemExit(2)

print(json.dumps({"status": "PASS", "clean_room_rebuild_closed": True, "required_classes": len(REQUIRED), "claim_allowed": False}, sort_keys=True))
