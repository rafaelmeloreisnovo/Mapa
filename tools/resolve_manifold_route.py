#!/usr/bin/env python3
import argparse, json, unicodedata
from pathlib import Path

COMMAND_PREFIX = {
    "atlas:": "R0007",
    "novo:": "R0006",
    "gap:": "R0008",
    "evid:": "R0009",
    "learn:": "R0010",
}

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode("ascii")
    return " ".join(s.lower().replace("_"," ").split())

def load_routes(path):
    rows=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def _score(query, route):
    q=norm(query)
    score=0
    hits=[]
    for raw in route["trigger"]:
        t=norm(raw)
        if not t:
            continue
        if t in q:
            score=max(score,100+len(t))
            hits.append(raw)
        elif " " not in t and t in q.split():
            score=max(score,50+len(t))
            hits.append(raw)
    return score,hits

def resolve(query, routes):
    q=norm(query)
    for prefix,rid in COMMAND_PREFIX.items():
        if q.startswith(prefix):
            route=next((r for r in routes if r["route_id"]==rid),None)
            if route is None:
                return {"status":"TOKEN_VAZIO_ROUTE_NOT_MATERIALIZED","route_id":rid,"claim_allowed":False}
            return {"status":"ROUTE_RESOLVED","route_id":rid,"reason":"explicit_command_prefix","path":route["path"],"evidence_gate":route["evidence_gate"],"rollback":route["rollback"],"claim_allowed":False}

    scored=[]
    for route in routes:
        score,hits=_score(query,route)
        if score>0:
            scored.append((score,route,hits))
    if not scored:
        return {"status":"TOKEN_VAZIO_NO_ROUTE","candidates":[],"claim_allowed":False}
    scored.sort(key=lambda x:(-x[0],x[1]["route_id"]))
    top=scored[0][0]
    tied=[x for x in scored if x[0]==top]
    if len(tied)>1:
        return {"status":"TOKEN_VAZIO_AMBIGUOUS_ROUTE","candidates":[x[1]["route_id"] for x in tied],"score":top,"claim_allowed":False}
    _,route,hits=scored[0]
    return {"status":"ROUTE_RESOLVED","route_id":route["route_id"],"reason":"trigger_match","matched_triggers":hits,"path":route["path"],"evidence_gate":route["evidence_gate"],"rollback":route["rollback"],"claim_allowed":False}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--routes",default="data/manifold/routes_omega_v1.jsonl")
    args=ap.parse_args()
    print(json.dumps(resolve(args.query,load_routes(args.routes)),ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
