#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

PREFIX = b"RAFAELIA_GLOBAL_CORPUS_ROOT_V1\0"


def die(msg):
    print(json.dumps({"status": "FAIL", "error": msg, "claim_allowed": False}, sort_keys=True))
    raise SystemExit(1)


doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
objects = doc.get("objects")
if not isinstance(objects, list) or not objects:
    die("objects must be non-empty array")

seen = set()
records = []
for row in objects:
    oid = row.get("object_id")
    sha = row.get("sha256")
    size = row.get("size")
    provider = row.get("provider")
    locator = row.get("locator")
    role = row.get("role")
    if not isinstance(oid, str) or not oid:
        die("object_id required")
    if oid in seen:
        die(f"duplicate object_id {oid}")
    seen.add(oid)
    if sha == "TOKEN_VAZIO":
        die(f"unobserved bytes cannot enter finalized root: {oid}")
    if not isinstance(sha, str) or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
        die(f"invalid sha256 {oid}")
    if not isinstance(size, int) or size < 0:
        die(f"invalid size {oid}")
    if not all(isinstance(x, str) and x for x in (provider, locator, role)):
        die(f"incomplete locator/role {oid}")
    records.append(f"{oid}\t{sha}\t{size}\t{provider}\t{locator}\t{role}\n")

payload = "".join(sorted(records, key=lambda s: s.encode("utf-8"))).encode("utf-8")
root = hashlib.sha256(PREFIX + payload).hexdigest()
print(json.dumps({"status": "PASS", "root_sha256": root, "object_count": len(records), "claim_allowed": False}, sort_keys=True))
