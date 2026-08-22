#!/usr/bin/env python3
"""Validate RAFAELIA semantic-support contract and bounded semantic packets.

Stdlib-only. Checks semantic governance invariants; it does not decide
scientific truth, algebraic equivalence, novelty, or implementation correctness.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
from typing import Any

SHA40 = re.compile(r"^[0-9a-f]{40}$")
PACKET_ID = re.compile(r"^SEM:[A-Z0-9:_-]+$")
PROOF_CAP_ZERO = {"FORMAL_ANALOGY","METHOD_SHARED","CO_OCCURS"}
FORMAL_WITNESS = {"DEFINITIONAL_EQUIV","FORMAL_REWRITE","CHANGE_OF_VARIABLES"}
EVIDENCE_EDGES = {"EVIDENCES","REFUTES","CORRECTS","SUPERSEDES"}
KNOWN_RELATIONS = {"EXACT_ALIAS","DEFINITIONAL_EQUIV","FORMAL_REWRITE","CHANGE_OF_VARIABLES","IMPLEMENTS","EXECUTES","EVIDENCES","REFUTES","CORRECTS","SUPERSEDES","DERIVED_FROM","DEPENDS_ON","PRECONDITION","METHOD_SHARED","FORMAL_ANALOGY","CO_OCCURS"}
NON_FORMULA = {"PIPELINE","PROTOCOL","LABEL"}

class ValidationError(Exception): pass
def fail(msg: str): raise ValidationError(msg)
def load_json(path: Path) -> Any:
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: fail(f"{path}: unreadable JSON: {exc}")

def validate_packet(p: dict[str,Any]) -> None:
    required={"schema","packet_id","source","surface","semantic","grounding","relations","operational","epistemic"}
    if required-set(p): fail(f"{p.get('packet_id','<unknown>')}: missing {sorted(required-set(p))}")
    if p["schema"]!="rafaelia.semantic-support-packet/v1" or not PACKET_ID.fullmatch(p["packet_id"]): fail(f"{p.get('packet_id')}: invalid identity/schema")
    src=p["source"]
    for k in ("repository","path","ref","blob_sha","span"):
        if not src.get(k): fail(f"{p['packet_id']}: missing source.{k}")
    if not SHA40.fullmatch(str(src["blob_sha"])): fail(f"{p['packet_id']}: blob_sha must be 40-hex")
    surf=p["surface"]
    if not str(surf.get("text","")).strip(): fail(f"{p['packet_id']}: empty surface")
    if surf.get("normalization") not in {"PRESERVE_SOURCE","NFC_TRIM","DERIVED_CANONICAL"}: fail(f"{p['packet_id']}: bad normalization")
    sem=p["semantic"]
    if not sem.get("domain_candidates"): fail(f"{p['packet_id']}: no domain candidates")
    amb=sem.get("ambiguity",{}); state=amb.get("state"); alts=amb.get("alternatives",[])
    if state in {"UNRESOLVED_TYPED","BLOCKED"} and len(alts)<2: fail(f"{p['packet_id']}: unresolved ambiguity needs >=2 readings")
    selected=amb.get("selected_reading")
    if selected is not None and selected not in {a.get("reading_id") for a in alts}: fail(f"{p['packet_id']}: selected reading missing")
    grd=p["grounding"]
    if grd.get("state") in {"SOURCE_EXPLICIT","REVERSIBLE_LIFT","DERIVED_TYPED"} and not grd.get("canonical_form"): fail(f"{p['packet_id']}: grounded state needs canonical form")
    if grd.get("state")=="DERIVED_TYPED" and not grd.get("witnesses"): fail(f"{p['packet_id']}: derived grounding needs witness")
    epi=p["epistemic"]
    if epi.get("claim_allowed") is not False: fail(f"{p['packet_id']}: claim_allowed must be false")
    if not epi.get("proof_boundary"): fail(f"{p['packet_id']}: proof boundary missing")
    op=p["operational"]
    if not op.get("route") or not op.get("next_gate"): fail(f"{p['packet_id']}: route/next gate missing")
    if epi.get("state")=="EXECUTED" and not op.get("execution_refs"): fail(f"{p['packet_id']}: EXECUTED without receipt")
    if epi.get("state")=="EVIDENCED" and not op.get("evidence_refs"): fail(f"{p['packet_id']}: EVIDENCED without evidence")
    if sem.get("object_class") in NON_FORMULA and any("E2_" in r or "ALGEBRA" in r for r in op["route"]): fail(f"{p['packet_id']}: non-formula routed to algebra")
    if state in {"UNRESOLVED_TYPED","BLOCKED"} and any(r.startswith("E2_") for r in op["route"]): fail(f"{p['packet_id']}: unresolved ambiguity routed to E2")
    for rel in p["relations"]:
        operator=rel.get("operator"); effect=rel.get("evidence_effect"); cap=rel.get("promotion_cap")
        if operator not in KNOWN_RELATIONS: fail(f"{p['packet_id']}: unknown relation {operator}")
        if operator in PROOF_CAP_ZERO and (effect not in {"NONE","STRUCTURAL_ONLY"} or cap not in {"NEVER","FORMAL_ONLY"}): fail(f"{p['packet_id']}: analogy/method edge promoted as proof")
        if operator in FORMAL_WITNESS and not grd.get("witnesses"): fail(f"{p['packet_id']}: {operator} lacks witness")
        if operator=="IMPLEMENTS" and not op.get("implementation_refs"): fail(f"{p['packet_id']}: IMPLEMENTS without binding")
        if operator=="EXECUTES" and not op.get("execution_refs"): fail(f"{p['packet_id']}: EXECUTES without receipt")
        if operator in EVIDENCE_EDGES and not op.get("evidence_refs"): fail(f"{p['packet_id']}: {operator} without evidence")

def validate(contract: dict[str,Any], packets: list[dict[str,Any]]) -> dict[str,Any]:
    if contract.get("schema")!="rafaelia.semantic-support-contract/v1" or contract.get("claim_allowed") is not False: fail("invalid semantic support contract")
    arms=contract.get("support_arms",[])
    expected=[f"S{i}_{n}" for i,n in enumerate(["SOURCE_IDENTITY","SURFACE_PRESERVATION","SYMBOL_TABLE","SCOPE_MODALITY","AMBIGUITY","GROUNDING","RELATION_GRAPH","DOMAIN_ENGINE","IMPLEMENTATION_BINDING","EXECUTION_EVIDENCE","FALSIFICATION","MEMORY_CUSTODY","CLAIM_PROMOTION"])]
    if [a.get("id") for a in arms]!=expected: fail("support arms must be exactly S0..S12")
    ids=[p.get("packet_id") for p in packets]
    if len(ids)!=len(set(ids)): fail("duplicate packet ids")
    cc={}; ac={}; gc={}
    for p in packets:
        validate_packet(p)
        for d,k in ((cc,p["semantic"]["object_class"]),(ac,p["semantic"]["ambiguity"]["state"]),(gc,p["grounding"]["state"])): d[k]=d.get(k,0)+1
    return {"schema":"rafaelia.semantic-support-validation/v1","status":"PASS","claim_allowed":False,"packets":len(packets),"support_arms":len(arms),"class_counts":dict(sorted(cc.items())),"ambiguity_counts":dict(sorted(ac.items())),"grounding_counts":dict(sorted(gc.items())),"packet_ids":sorted(ids),"boundary":"Contract consistency only; not semantic/scientific truth, E2 equivalence, implementation correctness or novelty."}

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--contract",default="data/semantics/semantic-support-contract.v1.json")
    ap.add_argument("--packets-dir",default="data/semantics/e1b")
    ap.add_argument("--output",default="")
    a=ap.parse_args()
    try:
        cp=Path(a.contract); packet_paths=sorted(Path(a.packets_dir).glob("*.json"))
        if not packet_paths: fail("no semantic packets found")
        report=validate(load_json(cp),[load_json(p) for p in packet_paths])
        report["contract_sha256"]=hashlib.sha256(cp.read_bytes()).hexdigest()
        report["packet_set_sha256"]=hashlib.sha256("".join(hashlib.sha256(p.read_bytes()).hexdigest() for p in packet_paths).encode()).hexdigest()
        text=json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n"
        if a.output:
            out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        sys.stdout.write(text); return 0
    except ValidationError as exc:
        sys.stderr.write(f"SEMANTIC_SUPPORT_FAIL: {exc}\n"); return 2
if __name__=="__main__": raise SystemExit(main())
