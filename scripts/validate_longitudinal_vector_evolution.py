#!/usr/bin/env python3
"""Stdlib-only, fail-closed validator for longitudinal vector evolution."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

TOKEN = re.compile(r"^TOKEN_VAZIO_[A-Z0-9_]+$")
HEX64 = re.compile(r"^[a-f0-9]{64}$")
GATES = ("provenance", "delta_identity", "semantic_consistency", "evidence_or_typed_gap", "reversibility")
INVARIANTS = {
    "source_is_not_interpretation", "parable_is_not_physical_proof",
    "token_vazio_is_not_zero", "new_dimension_requires_semantics_type_source_and_state",
    "weights_require_calibration_and_evidence", "no_hidden_model_state_claim",
    "append_never_silently_overwrites_ancestor", "relation_requires_type_and_source",
}

class ValidationError(ValueError): pass

def require(ok, msg):
    if not ok: raise ValidationError(msg)

def hash_or_token(v):
    return isinstance(v, str) and bool(HEX64.fullmatch(v) or TOKEN.fullmatch(v))

def canonical_sha256(p):
    raw=json.dumps(p, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()

def validate(p):
    require(p.get("schema")=="rafaelia.longitudinal-vector-evolution/v1", "invalid schema")
    require(p.get("claim_allowed") is False, "claim_allowed must remain false")
    rev=p.get("revision"); prev=p.get("previous_revision")
    require(isinstance(rev,int) and rev>=1, "invalid revision")
    if rev==1: require(prev is None, "revision 1 has no parent")
    else:
        require(prev==rev-1, "invalid previous_revision")
        require(hash_or_token(p.get("previous_event_hash")), "parent hash required")

    src=p.get("source",{})
    require(src.get("hidden_model_access") is False, "unavailable internal state cannot be claimed")
    require(hash_or_token(src.get("source_sha256")), "source hash or typed gap required")

    layers=p.get("layers",{}); hx=layers.get("hexagonal",{})
    require(set(hx)=={"origin","readability","semantics","dynamics","synergy","custody"}, "invalid hexagonal layer")

    views=layers.get("polysemic",[]); require(bool(views), "views required")
    ids=set(); literal=False
    for v in views:
        vid=v.get("view_id"); require(vid and vid not in ids, "view ids must be unique"); ids.add(vid)
        require(bool(v.get("source_ref")), "view source required")
        literal |= v.get("view_type")=="LITERAL"
        if v.get("view_type") in {"PARABLE","SYMBOLIC"}:
            blocked=set(v.get("forbidden_promotions",[]))
            require(bool(blocked & {"PARABLE_AS_EVIDENCE","SYMBOLIC_AS_PHYSICAL"}), "symbolic promotion must be blocked")
    require(literal, "literal view required")

    rels=layers.get("relational",[])
    for r in rels: require(all(r.get(k) for k in ("from","type","to","source_ref")), "typed sourced relation required")

    delta=p.get("delta",{}); added=delta.get("added_dimensions",[]); names=set()
    for d in added:
        n=d.get("name"); require(n and n not in names, "dimension names must be unique"); names.add(n)
        require(bool(d.get("data_type")), "dimension type required")
        require(isinstance(d.get("semantics"),str) and len(d["semantics"].strip())>=8, "dimension semantics required")
        require(bool(d.get("source_ref")) and bool(d.get("initial_state")), "dimension source and state required")
    removed=delta.get("removed_dimensions",[])
    if removed: require(bool(delta.get("supersession_receipt")), "removal requires receipt")

    require(not (INVARIANTS-set(p.get("invariants",[]))), "mandatory invariants missing")
    gate_pass=all(p.get("gates",{}).get(g) is True for g in GATES)
    state=p.get("state")
    if state=="EVOLVED_LOCAL": require(gate_pass, "all gates required")
    else: require(state in {"BLOCKED","TOKEN_VAZIO_VECTOR_DELTA"}, "invalid state")

    for w in p.get("weights",[]):
        status=w.get("status"); value=w.get("value"); refs=w.get("evidence_refs",[])
        require(status in {"CALIBRATED","TOKEN_VAZIO_CALIBRATION"}, "invalid weight status")
        if status=="CALIBRATED":
            require(isinstance(value,(int,float)) and not isinstance(value,bool) and bool(refs), "calibrated weight needs value and evidence")
        else: require(value is None and not refs, "uncalibrated weight must remain empty")

    epi=layers.get("epistemic",{}); gaps=epi.get("typed_gaps",[])
    require(all(isinstance(g,str) and TOKEN.fullmatch(g) for g in gaps), "typed gaps required")
    require(bool(epi.get("falsifier")), "falsifier required")
    return {"schema":"rafaelia.longitudinal-vector-evolution-validation/v1","state":"PASS",
            "vector_id":p.get("vector_id"),"revision":rev,"gate_pass":gate_pass,
            "added_dimension_count":len(added),"relation_count":len(rels),"view_count":len(views),
            "claim_allowed":False,"canonical_payload_sha256":canonical_sha256(p)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("input",type=Path); ap.add_argument("--receipt",type=Path); a=ap.parse_args()
    try: receipt=validate(json.loads(a.input.read_text(encoding="utf-8")))
    except (OSError,json.JSONDecodeError,ValidationError) as e:
        print(json.dumps({"state":"FAIL","error":str(e)},ensure_ascii=False,indent=2)); return 1
    text=json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.receipt: a.receipt.parent.mkdir(parents=True,exist_ok=True); a.receipt.write_text(text,encoding="utf-8")
    print(text,end=""); return 0
if __name__=="__main__": raise SystemExit(main())
