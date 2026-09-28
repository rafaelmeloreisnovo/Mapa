#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQ_ROUTE = {
    "route_id","source_ref","target_ref","relation_type","owner","authority",
    "predecessor","successor","dependency_edges","evidence_ref","receipt_ref",
    "rollback_ref","replay_recipe","reproduction_state","privacy_class",
    "retention_class","claim_allowed"
}
REQ_AGENT = {
    "id","token","workstream","alpha_intent","omega_delivery","locality",
    "dimensions","claim_allowed"
}

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def lines(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def fail(msg):
    raise SystemExit(msg)

def validate(root):
    root=Path(root)
    atlas=load(root/"atlas.v1.json")
    orders=load(root/"agent_work_orders.v1.json")
    routes=lines(root/"routes.v1.jsonl")

    if atlas.get("claim_allowed") is not False or orders.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")
    if len(atlas.get("workstreams",[])) != 11:
        fail("expected WS00..WS10")
    ws={x["id"] for x in atlas["workstreams"]}
    if ws != {f"WS{i:02d}" for i in range(11)}:
        fail("workstream id set mismatch")

    agents=orders.get("agents",[])
    if len(agents) != 11:
        fail("expected 11 agent work orders")
    for a in agents:
        miss=REQ_AGENT-set(a)
        if miss:
            fail(f"agent {a.get('id')}: missing {sorted(miss)}")
        if a["workstream"] not in ws:
            fail(f"agent {a['id']}: unknown workstream")
        if a["claim_allowed"] is not False:
            fail(f"agent {a['id']}: claim_allowed must be false")
        dims=a["dimensions"]
        for k,v in dims.items():
            if not isinstance(v,int) or not 0 <= v <= 3:
                fail(f"agent {a['id']}: invalid routing dimension {k}={v}")

    if not routes:
        fail("routes missing")
    for r in routes:
        miss=REQ_ROUTE-set(r)
        if miss:
            fail(f"route {r.get('route_id')}: missing {sorted(miss)}")
        if r["claim_allowed"] is not False:
            fail(f"route {r['route_id']}: claim_allowed must be false")
        if not r["rollback_ref"] or not r["replay_recipe"]:
            fail(f"route {r['route_id']}: rollback/replay missing")

    inv=set(atlas.get("invariants",[]))
    for must in [
        "SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM",
        "TOKEN_VAZIO != 0",
        "IMPLEMENTED_UNTESTED != PASS"
    ]:
        if must not in inv:
            fail(f"missing invariant: {must}")

    return {
        "status":"PASS",
        "workstreams":len(ws),
        "agents":len(agents),
        "routes":len(routes),
        "claim_allowed":False
    }

if __name__=="__main__":
    if len(sys.argv)!=2:
        fail("usage: validate_session_full_dispatch.py ROOT")
    print(json.dumps(validate(sys.argv[1]),sort_keys=True))
