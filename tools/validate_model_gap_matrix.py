#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

ALLOWED_STATES = {
    "PARTIAL_BOUNDED","OBSERVED_UNPROMOTED","SPEC_IMPLEMENTED_UNTESTED_GLOBAL",
    "SPEC_ONLY_PARTIAL_VALIDATION","SPEC_PARTIAL","METHOD_ONLY","SPEC_ONLY","NORMATIVE"
}

def fail(msg):
    raise SystemExit(msg)

def validate(path):
    obj=json.loads(Path(path).read_text(encoding="utf-8"))
    if obj.get("schema_version")!="1.0": fail("unsupported schema_version")
    if obj.get("registry_id")!="RAFAELIA_MODEL_GAP_MATRIX_V1": fail("registry_id mismatch")
    if obj.get("claim_allowed") is not False: fail("claim_allowed must remain false")
    models=obj.get("models")
    if not isinstance(models,list) or not models: fail("models missing")
    ids=set()
    for row in models:
        mid=row.get("model_id","")
        if not re.fullmatch(r"M[0-9]{2}",mid): fail(f"bad model_id: {mid}")
        if mid in ids: fail(f"duplicate model_id: {mid}")
        ids.add(mid)
        if row.get("state") not in ALLOWED_STATES: fail(f"unsupported state {mid}: {row.get('state')}")
        tv=row.get("token_vazio")
        if not isinstance(tv,list) or not tv or any(not isinstance(x,str) or not x.startswith("TOKEN_VAZIO") for x in tv):
            fail(f"invalid token_vazio: {mid}")
        if not row.get("gap") or not row.get("gap_kind"): fail(f"missing gap: {mid}")
        if not row.get("evidence_needed") or not row.get("closure_criterion") or not row.get("next"):
            fail(f"incomplete closure contract: {mid}")
        for ref in row.get("linked_gap_refs",[]):
            if not re.fullmatch(r"G[0-9]{4}",ref): fail(f"bad linked gap ref {mid}: {ref}")
    expected={f"M{i:02d}" for i in range(15)}
    if ids != expected: fail(f"model coverage mismatch: missing={sorted(expected-ids)} extra={sorted(ids-expected)}")
    return {"status":"PASS","models":len(models),"token_vazio":sum(len(x["token_vazio"]) for x in models),"claim_allowed":False}

if __name__=="__main__":
    if len(sys.argv)!=2: fail("usage: validate_model_gap_matrix.py MATRIX.json")
    print(json.dumps(validate(sys.argv[1]),sort_keys=True))
