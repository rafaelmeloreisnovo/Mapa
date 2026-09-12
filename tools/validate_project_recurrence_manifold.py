#!/usr/bin/env python3
"""Fail-closed validator for RAFAELIA Project Recurrence Manifold v1.

Stdlib-only. It validates the alias-only recurrence ledger and key governance
invariants. It does not prove semantic identity, causality, scientific truth,
or complete project coverage.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/memory/project-recurrence/seed.v1.jsonl"
L9=set("LOTPC RIEA".replace(" ",""))
OMEGA7={"DIRECT","INVERSE","DERIVATIVE","ANTIDERIVATIVE","RECURSIVE","ORTHOGONAL","INTEGRATIVE"}
LENSES={"HEURISTIC","CORRELATIVE","LOGARITHMIC","RECLUSIVE","REVERSAL","EXPLORATORY","RESEARCH","ANOMALY","PARADOX","RAPPORT","ATTRACTOR_VECTORING_CANDIDATE"}
GSTAT={"PASS","FAIL","BLOCKED","TOKEN_VAZIO","NOT_APPLICABLE"}

def fail(msg:str)->None:
    raise SystemExit(f"FAIL: {msg}")

def load(path:Path):
    rows=[]
    for n,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip():
            continue
        try: rows.append(json.loads(line))
        except Exception as e: fail(f"json line {n}: {e}")
    return rows

def validate(rows):
    if not rows: fail("empty ledger")
    ids=set(); keys=set()
    for r in rows:
        if r.get("schema_version")!="rafaelia.project-recurrence-manifold/v1": fail("schema_version")
        rid=r.get("recurrence_id"); key=r.get("pattern_key")
        if rid in ids or key in keys: fail("duplicate id/key")
        ids.add(rid); keys.add(key)
        if r.get("claim_allowed") is not False: fail(f"{rid}: claim_allowed")
        pp=r.get("public_privacy",{})
        if pp!={"alias_only":True,"raw_session_ids":False,"raw_message_ids":False,"raw_content":False}: fail(f"{rid}: privacy")
        axes=[o.get("axis") for o in r.get("observations",[])]
        if len(axes)!=len(set(axes)) or not set(axes)<=L9: fail(f"{rid}: L9")
        if not set(r.get("omega7",[]))<=OMEGA7: fail(f"{rid}: omega7")
        if not set(r.get("lenses",[]))<=LENSES: fail(f"{rid}: lenses")
        for g in r.get("gates",[]):
            if g.get("status") not in GSTAT: fail(f"{rid}: gate status")
            if g.get("status")=="PASS" and g.get("gate_id")=="G-IDENTITY" and not g.get("evidence_refs"): fail(f"{rid}: identity pass without evidence")
        for rel in r.get("relations",[]):
            if rel.get("validity")=="CAUSAL_PROVEN":
                ev=[g for g in r.get("gates",[]) if g.get("gate_id")=="G-CAUSALITY" and g.get("status")=="PASS" and g.get("evidence_refs")]
                if not ev: fail(f"{rid}: causal promotion without evidence")
        gaps=r.get("token_vazio",[])
        gap_ids={g.get("gap_id") for g in gaps}
        if gap_ids != set(r.get("r3",{}).get("f_gap",[])): fail(f"{rid}: R3 gap mismatch")
        if len(r.get("r3",{}).get("f_next",[]))>3: fail(f"{rid}: too many next actions")
    return {"status":"PASS","records":len(rows),"unique_patterns":len(keys),"claim_allowed":False,"raw_private_ids":0}

def main():
    path=Path(sys.argv[1]) if len(sys.argv)>1 else DEFAULT
    print(json.dumps(validate(load(path)),sort_keys=True))

if __name__=="__main__":
    main()
