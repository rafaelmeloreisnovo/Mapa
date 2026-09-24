#!/usr/bin/env python3
import argparse, json, re, unicodedata
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

def tokens(s: str):
    return re.findall(r"[a-z0-9]+", norm(s))

def load_routes(path):
    rows=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def _catalog_reduction(resolved: bool, method: str):
    return {
        "before": "NP_CATALOG",
        "after": "P_CATALOG" if resolved else "NP_CATALOG",
        "method": method,
        "complexity_claim": False,
    }

def _catalog_delta(query, routes, resolved, candidate_count_after, matched_terms):
    query_tokens = tokens(query)
    matched_tokens = set()
    for term in matched_terms:
        matched_tokens.update(tokens(term))
    residual_tokens = [token for token in query_tokens if token not in matched_tokens]
    universe = len(routes)
    after = max(0, min(candidate_count_after, universe))
    return {
        "metric_version": "v1",
        "scope": "ROUTE_RESOLUTION_ONLY",
        "route_universe": universe,
        "candidate_count_after": after,
        "delta_np_catalog": universe - after,
        "delta_p_catalog": 1 if resolved else 0,
        "delta_section_noise": len(residual_tokens),
        "residual_tokens": residual_tokens,
        "units": {
            "delta_np_catalog": "route_candidates_removed",
            "delta_p_catalog": "deterministic_resolution_flag",
            "delta_section_noise": "normalized_query_tokens",
        },
        "complexity_claim": False,
        "evidence_claim": False,
    }

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
                return {
                    "status":"TOKEN_VAZIO_ROUTE_NOT_MATERIALIZED",
                    "route_id":rid,
                    "catalog_reduction":_catalog_reduction(False,"explicit command prefix points to a non-materialized route"),
                    "catalog_delta":_catalog_delta(query,routes,False,len(routes),[prefix.rstrip(":")]),
                    "claim_allowed":False,
                }
            return {
                "status":"ROUTE_RESOLVED",
                "route_id":rid,
                "reason":"explicit_command_prefix",
                "path":route["path"],
                "evidence_gate":route["evidence_gate"],
                "rollback":route["rollback"],
                "catalog_reduction":_catalog_reduction(True,"explicit command prefix plus stable route registry"),
                "catalog_delta":_catalog_delta(query,routes,True,1,[prefix.rstrip(":")]),
                "claim_allowed":False,
            }

    scored=[]
    for route in routes:
        score,hits=_score(query,route)
        if score>0:
            scored.append((score,route,hits))
    if not scored:
        return {
            "status":"TOKEN_VAZIO_NO_ROUTE",
            "candidates":[],
            "catalog_reduction":_catalog_reduction(False,"no stable trigger matched"),
            "catalog_delta":_catalog_delta(query,routes,False,len(routes),[]),
            "claim_allowed":False,
        }
    scored.sort(key=lambda x:(-x[0],x[1]["route_id"]))
    top=scored[0][0]
    tied=[x for x in scored if x[0]==top]
    if len(tied)>1:
        matched_terms=[]
        for _,_,hits in tied:
            matched_terms.extend(hits)
        return {
            "status":"TOKEN_VAZIO_AMBIGUOUS_ROUTE",
            "candidates":[x[1]["route_id"] for x in tied],
            "score":top,
            "catalog_reduction":_catalog_reduction(False,"candidate set remains ambiguous"),
            "catalog_delta":_catalog_delta(query,routes,False,len(tied),matched_terms),
            "claim_allowed":False,
        }
    _,route,hits=scored[0]
    return {
        "status":"ROUTE_RESOLVED",
        "route_id":route["route_id"],
        "reason":"trigger_match",
        "matched_triggers":hits,
        "path":route["path"],
        "evidence_gate":route["evidence_gate"],
        "rollback":route["rollback"],
        "catalog_reduction":_catalog_reduction(True,"unique best trigger under the fixed route registry"),
        "catalog_delta":_catalog_delta(query,routes,True,1,hits),
        "claim_allowed":False,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--routes",default="data/manifold/routes_omega_v1.jsonl")
    args=ap.parse_args()
    print(json.dumps(resolve(args.query,load_routes(args.routes)),ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
