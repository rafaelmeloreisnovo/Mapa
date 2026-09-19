#!/usr/bin/env python3
"""Fail-closed structural validator for the RAFAELIA Humanity policy.

This checks governance invariants only. PASS is not a legal opinion.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/legal/humanity-protection-access.v1.json"

def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")

def load() -> dict:
    try:
        return json.loads(POLICY.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"load: {exc}")

def validate(p: dict) -> dict:
    if p.get("schema_version") != "rafaelia.humanity-protection-access/v1":
        fail("schema_version")
    if p.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")
    protection = p.get("protection") or {}
    for key in (
        "preserve_human_authorship",
        "preserve_upstream_notices",
        "preserve_provenance",
        "forbid_false_authorship",
        "nationality_neutral",
    ):
        if protection.get(key) is not True:
            fail(f"protection.{key}")
    access = p.get("access") or {}
    if access.get("blanket_relicense") is not False:
        fail("blanket_relicense must be false")
    if access.get("existing_grants_preserved") is not True:
        fail("existing_grants_preserved")
    gate = p.get("release_gate") or []
    required = {
        "RIGHTS_AUDIT",
        "MATERIAL_CLASS",
        "THIRD_PARTY_BOUNDARY",
        "PRIVACY_SECURITY_GATE",
        "LICENSE_COMPATIBILITY",
        "EXPLICIT_LICENSE_NOTICE",
        "EFFECTIVE_REF",
        "RECEIPT",
    }
    if set(gate) != required:
        fail("release_gate mismatch")
    blocked = set(p.get("blocked_by_default") or [])
    if "THIRD_PARTY_RIGHTS_UNRESOLVED" not in blocked:
        fail("third-party fail-closed boundary missing")
    if "PERSONAL_OR_SENSITIVE_DATA_UNCLEARED" not in blocked:
        fail("privacy fail-closed boundary missing")
    source_ids = {x.get("id") for x in p.get("sources") or []}
    for required_source in {"WIPO-BERNE-SUMMARY","BR-L9610-1998","BR-L9609-1998","CC-FAQ-SOFTWARE-BOUNDARY"}:
        if required_source not in source_ids:
            fail(f"missing source {required_source}")
    return {
        "status": "PASS",
        "schema_version": p["schema_version"],
        "claim_allowed": False,
        "blanket_relicense": False,
        "release_gate_count": len(gate),
    }

if __name__ == "__main__":
    print(json.dumps(validate(load()), sort_keys=True))
