#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ALLOWED_EVIDENCE={"PROVADO","EVIDENCIADO","HIPÓTESE","MODELO_ANALÓGICO","PARÁBOLA","REFUTADO","TOKEN_VAZIO"}
ALLOWED_REL={"GOVERNS","INDEXES","PRODUCES","CONSUMES","VALIDATES","CUSTODIES","REFERENCES","DEPENDS_ON","MIRRORS","REPLICATES"}

def fail(msg:str)->None:
    print(json.dumps({"ok":False,"state":"TOKEN_VAZIO","error":msg},ensure_ascii=False)); raise SystemExit(1)

def main(path:str)->None:
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("claim_allowed") is not False: fail("claim_allowed must be false")
    nodes=data.get("nodes",[]); edges=data.get("edges",[]); contexts=data.get("contexts",[])
    node_ids=[n.get("id") for n in nodes]
    if not nodes or len(node_ids)!=len(set(node_ids)): fail("nodes missing or duplicated")
    edge_ids=[e.get("id") for e in edges]
    if len(edge_ids)!=len(set(edge_ids)): fail("edge ids duplicated")
    known=set(node_ids)
    for e in edges:
        if e.get("from") not in known or e.get("to") not in known: fail(f"dangling edge {e.get('id')}")
        if e.get("relation") not in ALLOWED_REL: fail(f"invalid relation {e.get('id')}")
        if e.get("evidence_state") not in ALLOWED_EVIDENCE: fail(f"invalid evidence state {e.get('id')}")
        if e.get("evidence_state") in {"PROVADO","EVIDENCIADO"} and not e.get("receipt_locator"): fail(f"evidenced edge without receipt {e.get('id')}")
    ctx_ids=[c.get("context_id") for c in contexts]
    if not contexts or len(ctx_ids)!=len(set(ctx_ids)): fail("contexts missing or duplicated")
    for c in contexts:
        if not set(c.get("entry_nodes",[])).issubset(known): fail(f"context references unknown node {c.get('context_id')}")
    print(json.dumps({"ok":True,"state":"PASS_LOCAL_LIMITED","nodes":len(nodes),"edges":len(edges),"contexts":len(contexts),"claim_allowed":False},ensure_ascii=False))

if __name__=="__main__":
    if len(sys.argv)!=2: fail("usage: validate_federated_reference_matrix.py MATRIX.json")
    main(sys.argv[1])
