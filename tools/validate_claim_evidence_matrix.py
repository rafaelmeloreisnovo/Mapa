#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def die(msg):
    print(json.dumps({"status": "FAIL", "error": msg, "claim_allowed": False}, sort_keys=True))
    raise SystemExit(1)


doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
claims = doc.get("claims")
if not isinstance(claims, list):
    die("claims must be array")

ids = set()
for row in claims:
    claim_id = row.get("claim_id")
    if not isinstance(claim_id, str) or not claim_id:
        die("claim_id required")
    if claim_id in ids:
        die(f"duplicate claim_id {claim_id}")
    ids.add(claim_id)

    promotion = row.get("promotion_state")
    source_refs = row.get("source_refs", [])
    artifact_refs = row.get("artifact_refs", [])
    execution_refs = row.get("execution_refs", [])
    evidence_refs = row.get("evidence_refs", [])
    review = row.get("review_state")

    if promotion in ("BOUNDED", "ALLOWED_SCOPED"):
        if not source_refs or not artifact_refs or not evidence_refs:
            die(f"promoted claim missing source/artifact/evidence: {claim_id}")
    if promotion == "ALLOWED_SCOPED":
        if not execution_refs:
            die(f"ALLOWED_SCOPED claim missing execution: {claim_id}")
        if review != "INDEPENDENT_REVIEWED":
            die(f"ALLOWED_SCOPED requires independent review: {claim_id}")
        if not row.get("scope"):
            die(f"ALLOWED_SCOPED requires scope: {claim_id}")

print(json.dumps({"status": "PASS", "claims": len(ids), "claim_allowed": False}, sort_keys=True))
