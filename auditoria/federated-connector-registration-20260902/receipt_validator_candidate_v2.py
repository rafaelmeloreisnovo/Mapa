#!/usr/bin/env python3
"""RAFAELIA receipt validator candidate v2.

AUDIT-BRANCH CANDIDATE ONLY.
This file is not schema authority and does not promote historical receipts.
It exists to make the unresolved canonicalization rules executable/falsifiable.

Candidate rules (must remain proposal until custody authority accepts/supersedes them):
- receipt digest algorithm: SHA-256
- canonical bytes: UTF-8(JSON with sorted keys, no insignificant whitespace)
- `immutable_hash` is excluded from the material it authenticates (avoids self-reference)
- Git object identity is validated separately from evidence/content digest
- historical mismatch is reported; nothing is rewritten
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

HEX40_OR_64 = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


def canonical_payload(receipt: dict) -> bytes:
    payload = dict(receipt)
    payload.pop("immutable_hash", None)
    text = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return text.encode("utf-8")


def candidate_digest(receipt: dict) -> str:
    return hashlib.sha256(canonical_payload(receipt)).hexdigest()


def validate(receipt: dict) -> dict:
    observed_digest = receipt.get("immutable_hash")
    source_commit = receipt.get("source_commit")
    computed = candidate_digest(receipt)

    digest_shape_ok = isinstance(observed_digest, str) and bool(SHA256_HEX.fullmatch(observed_digest))
    git_object_id_shape_ok = isinstance(source_commit, str) and bool(HEX40_OR_64.fullmatch(source_commit))
    digest_matches_candidate = digest_shape_ok and observed_digest == computed

    problems = []
    if not digest_shape_ok:
        problems.append("immutable_hash_not_full_sha256_hex")
    if not git_object_id_shape_ok:
        problems.append("source_commit_not_supported_git_object_id_shape")
    if digest_shape_ok and not digest_matches_candidate:
        problems.append("immutable_hash_does_not_match_candidate_canonicalization")

    # Fail closed: this candidate can falsify a receipt under the candidate rules,
    # but cannot declare the historical schema authoritative or promote a claim.
    return {
        "validator": "RAFAELIA_RECEIPT_VALIDATOR_CANDIDATE_V2",
        "authority": "PROPOSED_NOT_CANONICAL",
        "claim_allowed": False,
        "canonicalization_candidate": {
            "digest": "sha256",
            "encoding": "utf-8",
            "json_keys": "sorted",
            "json_separators": [",", ":"],
            "ensure_ascii": False,
            "excluded_fields": ["immutable_hash"],
        },
        "source_commit": source_commit,
        "git_object_id_shape_ok": git_object_id_shape_ok,
        "observed_immutable_hash": observed_digest,
        "observed_digest_shape_ok": digest_shape_ok,
        "candidate_digest": computed,
        "digest_matches_candidate": digest_matches_candidate,
        "classification": "CANDIDATE_PASS" if not problems else "CANDIDATE_FAIL_CLOSED",
        "problems": problems,
        "closure_gate": "custody authority accepts/version-controls semantics + independent execution receipt + fixtures + deterministic reproduction",
    }


def self_test() -> None:
    base = {
        "receipt_id": "fixture-positive",
        "source_commit": "0" * 40,
        "evidence_scope": "local",
        "custody_status": "APPENDED",
    }
    positive = dict(base)
    positive["immutable_hash"] = candidate_digest(positive)
    assert validate(positive)["classification"] == "CANDIDATE_PASS"

    malformed = dict(base)
    malformed["immutable_hash"] = "a" * 62
    result = validate(malformed)
    assert result["classification"] == "CANDIDATE_FAIL_CLOSED"
    assert "immutable_hash_not_full_sha256_hex" in result["problems"]

    mutated = dict(positive)
    mutated["evidence_scope"] = "federated"
    result = validate(mutated)
    assert result["classification"] == "CANDIDATE_FAIL_CLOSED"
    assert "immutable_hash_does_not_match_candidate_canonicalization" in result["problems"]


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        self_test()
        print(json.dumps({"self_test": "PASS", "claim_allowed": False}, sort_keys=True))
        raise SystemExit(0)

    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} RECEIPT_JSON_OR_JSONL", file=sys.stderr)
        raise SystemExit(2)

    raw = Path(sys.argv[1]).read_text(encoding="utf-8")
    receipt = json.loads(raw)
    print(json.dumps(validate(receipt), indent=2, sort_keys=True, ensure_ascii=False))
