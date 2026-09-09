#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def die(msg):
    print(json.dumps({"status": "FAIL", "error": msg, "claim_allowed": False}, sort_keys=True))
    raise SystemExit(1)


doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
objects = doc.get("objects")
if not isinstance(objects, list):
    die("objects must be array")

ids = set()
alias_owner = {}
for row in objects:
    oid = row.get("object_id")
    if not isinstance(oid, str) or not oid:
        die("object_id required")
    if oid in ids:
        die(f"duplicate object_id {oid}")
    ids.add(oid)
    aliases = row.get("aliases", [])
    if len(set(aliases)) != len(aliases):
        die(f"duplicate alias within {oid}")
    for alias in aliases:
        if alias in alias_owner and alias_owner[alias] != oid:
            die(f"alias collision {alias}: {alias_owner[alias]} vs {oid}")
        alias_owner[alias] = oid
    if oid in aliases:
        die(f"canonical id repeated as alias {oid}")

for row in objects:
    for target in row.get("supersedes", []):
        if target not in ids:
            die(f"unresolved supersedes target {target}")

print(json.dumps({"status": "PASS", "objects": len(ids), "aliases": len(alias_owner), "claim_allowed": False}, sort_keys=True))
