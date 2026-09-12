#!/usr/bin/env python3
"""Validate RAFAELIA license scope registry fail-closed.

This validator checks structural licensing boundaries. It does not determine
copyright ownership, legal enforceability, or compatibility beyond the
explicit states in the registry.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"data/legal/license-scope-registry.v1.jsonl"
ALLOWED_CURRENT={"PERMITTED_BY_CURRENT_LICENSE","REQUIRES_SEPARATE_LICENSE","TOKEN_VAZIO"}
ALLOWED_RNC={"YES_AFTER_FILE_SCOPE_AUDIT","NO_INCOMPATIBLE","TOKEN_VAZIO"}

def fail(msg): raise SystemExit(f"FAIL: {msg}")

def load():
    rows=[]
    for n,line in enumerate(REG.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try: rows.append(json.loads(line))
        except Exception as e: fail(f"json line {n}: {e}")
    return rows

def validate(rows):
    if not rows: fail("empty registry")
    ids=set()
    for r in rows:
        if r.get("schema_version")!="rafaelia.license-scope-record/v1": fail("schema_version")
        if r.get("scope_id") in ids: fail("duplicate scope_id")
        ids.add(r["scope_id"])
        if r.get("claim_allowed") is not False: fail(f"{r['scope_id']}: claim_allowed")
        if r.get("commercial_rights_current") not in ALLOWED_CURRENT: fail(f"{r['scope_id']}: commercial state")
        if r.get("custom_rnc_allowed") not in ALLOWED_RNC: fail(f"{r['scope_id']}: rnc state")
        lic=(r.get("observed_license") or "").upper()
        if "GPL" in lic and r.get("custom_rnc_allowed")=="YES_AFTER_FILE_SCOPE_AUDIT":
            fail(f"{r['scope_id']}: blanket GPL noncommercial conflict")
        if r.get("state")=="TOKEN_VAZIO" and not r.get("gaps"):
            fail(f"{r['scope_id']}: unresolved state without gap")
    return {"status":"PASS","records":len(rows),"claim_allowed":False}

if __name__=="__main__":
    print(json.dumps(validate(load()),sort_keys=True))
