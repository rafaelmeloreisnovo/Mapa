#!/usr/bin/env python3
"""Deterministic stdlib checker for RAFAELIA μ Semantic Event v2 fixtures.

This is intentionally narrower than a full JSON Schema engine. It validates the
critical authority/privacy/provenance invariants and emits a canonical SHA-256 so a
replay can compare structure without retaining raw content.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ACTORS = {"USER", "ASSISTANT", "TOOL", "SYSTEM", "UNKNOWN"}
AUTHORSHIP_STATES = {"VERIFIED_LIMITED", "DECLARED_BY_AUTHOR", "THIRD_PARTY_BOUND", "TOKEN_VAZIO"}
SENSE_STATES = {"BOUND", "DECLARED_BY_AUTHOR", "PROVISIONAL", "TOKEN_VAZIO"}
CLAIM_STATES = {"BLOCKED", "VERIFIED_LIMITED", "TOKEN_VAZIO"}
PRIVACY = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "SENSITIVE", "TOKEN_VAZIO"}
MINOR = {"YES", "NO", "TOKEN_VAZIO"}


def canonical_bytes(obj: dict) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_sha256(obj: dict) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def validate_event(e: dict) -> list[str]:
    errors: list[str] = []
    if e.get("schema_version") != "rafaelia.mu-semantic-event/v2":
        errors.append("bad schema_version")
    if e.get("actor") not in ACTORS:
        errors.append("invalid actor")
    if e.get("claim_allowed") is not False:
        errors.append("claim_allowed must remain false")

    source = e.get("source") or {}
    if source.get("raw_content_embedded") is not False:
        errors.append("raw_content_embedded must be false")
    sha = source.get("content_sha256", "")
    if len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
        errors.append("source content_sha256 invalid")

    auth = e.get("authority") or {}
    aa = auth.get("authorship_authority") or {}
    sa = auth.get("sense_authority") or {}
    ca = auth.get("claim_authority") or {}
    if aa.get("state") not in AUTHORSHIP_STATES:
        errors.append("invalid authorship_authority state")
    if sa.get("state") not in SENSE_STATES:
        errors.append("invalid sense_authority state")
    if ca.get("state") not in CLAIM_STATES:
        errors.append("invalid claim_authority state")
    if auth.get("privacy_class") not in PRIVACY:
        errors.append("invalid privacy_class")
    if auth.get("minor_related") not in MINOR:
        errors.append("invalid minor_related")

    # No actor -> authorship coercion.
    if e.get("actor") == "USER" and aa.get("state") == "VERIFIED_LIMITED" and not aa.get("evidence_refs"):
        errors.append("USER actor does not prove VERIFIED_LIMITED authorship without evidence")

    # Child-related records cannot silently omit privacy/authorization.
    if auth.get("minor_related") == "YES":
        if auth.get("privacy_class") in {"PUBLIC", "TOKEN_VAZIO"}:
            errors.append("minor-related event must fail closed on privacy")
        if not auth.get("authorization_ref"):
            errors.append("minor-related event requires authorization_ref")

    # Claim authority must never be inferred from authorship/sense authority.
    if ca.get("state") == "VERIFIED_LIMITED" and not ca.get("gate_refs"):
        errors.append("VERIFIED_LIMITED claim authority requires gate_refs")
    if ca.get("state") == "VERIFIED_LIMITED" and not ca.get("evidence_refs"):
        errors.append("VERIFIED_LIMITED claim authority requires evidence_refs")

    if not e.get("provenance"):
        errors.append("provenance required")
    if not e.get("lexemes"):
        errors.append("lexemes required")
    return errors


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("event")
    args = p.parse_args()
    try:
        event = json.loads(Path(args.event).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2
    errors = validate_event(event)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS sha256={canonical_sha256(event)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
