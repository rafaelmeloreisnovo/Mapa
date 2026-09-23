#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

EDGE_RELATIONS = {"ROUTES_TO","INDEXES","RECONSTRUCTS_FROM","POINTS_TO","DEPENDS_ON","EVIDENCES","GATES","RECEIPTS","SUPERSEDES","ROLLBACK_TO","CONTEXTUALIZES","RELATES_TO","EXPANDS_TO","SOURCE_OF","CROSS_PROVIDER_BRIDGE","RESOLVES_TO","VALIDATED_BY"}
EDGE_STATES = {"OBSERVED_SOURCE","OBSERVED_SOURCE_ROLE","OBSERVED_CONCEPTUAL_ROUTE","MATERIALIZED","OPERATIONAL_ROUTE_DEFINED","VALIDATED_BOUNDED","TOKEN_VAZIO","SUPERSEDED"}
ROUTE_STATES = {"ROUTE_DEFINED","VALIDATED_BOUNDED","SUPERSEDED"}

def read_jsonl(path):
    out=[]
    for n,line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try: out.append(json.loads(line))
        except json.JSONDecodeError as e: raise SystemExit(f"{path}:{n}: invalid JSON: {e}")
    return out

def require(obj, keys, ctx):
    miss=[k for k in keys if k not in obj]
    if miss: raise SystemExit(f"{ctx}: missing {miss}")

def validate_edges(path):
    rows=read_jsonl(path); seen=set()
    for i,o in enumerate(rows,1):
        require(o,["edge_id","source_id","relation_type","target_id","scope","evidence_ref","state","contradiction","gap"],f"edge[{i}]")
        if not re.fullmatch(r"E\d{4,}",o["edge_id"]): raise SystemExit(f"edge[{i}]: bad edge_id")
        if o["edge_id"] in seen: raise SystemExit(f"edge[{i}]: duplicate edge_id")
        seen.add(o["edge_id"])
        if o["relation_type"] not in EDGE_RELATIONS: raise SystemExit(f"edge[{i}]: bad relation_type")
        if o["state"] not in EDGE_STATES: raise SystemExit(f"edge[{i}]: bad state")
        for k in ("source_id","target_id","scope","evidence_ref"):
            if not isinstance(o[k],str) or not o[k]: raise SystemExit(f"edge[{i}]: empty {k}")
    return len(rows)

def validate_routes(path):
    rows=read_jsonl(path); seen=set()
    for i,o in enumerate(rows,1):
        require(o,["route_id","trigger","path","minimum_sources","expansion_condition","evidence_gate","rollback","state"],f"route[{i}]")
        if not re.fullmatch(r"R\d{4,}",o["route_id"]): raise SystemExit(f"route[{i}]: bad route_id")
        if o["route_id"] in seen: raise SystemExit(f"route[{i}]: duplicate route_id")
        seen.add(o["route_id"])
        if o["state"] not in ROUTE_STATES: raise SystemExit(f"route[{i}]: bad state")
        for k in ("trigger","path","minimum_sources","evidence_gate","rollback"):
            if not isinstance(o[k],list) or not o[k] or not all(isinstance(v,str) and v for v in o[k]):
                raise SystemExit(f"route[{i}]: bad {k}")
    return len(rows)

def main(argv):
    if len(argv)!=3: raise SystemExit("usage: validate_manifold_registry.py EDGES.jsonl ROUTES.jsonl")
    e=validate_edges(argv[1]); r=validate_routes(argv[2])
    print(json.dumps({"status":"PASS","edges":e,"routes":r,"claim_allowed":False},sort_keys=True))
if __name__=="__main__": main(sys.argv)
