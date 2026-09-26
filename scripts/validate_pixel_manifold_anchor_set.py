#!/usr/bin/env python3
from __future__ import annotations
import argparse,copy,hashlib,json,math,statistics
from pathlib import Path

SCHEMA="rafaelia.pixel-manifold-anchor-set/v1"
ARTIFACT="PIXEL_MANIFOLD_ANCHOR_SET_V1_20260926"
GAPS={f"TV-PET-{i:03d}" for i in range(1,11)}
INV={"SOURCE_ART != FORMAL_MODEL != EXECUTION != EVIDENCE != CLAIM","VISUAL_KEY_MATCH != SEMANTIC_IDENTITY","MANUAL_VISUAL_REVIEW != EXTERNAL_GROUND_TRUTH","TOKEN_VAZIO != 0"}
class V(ValueError): pass
def req(x,m):
    if not x: raise V(m)
def digest(p):
    q=dict(p);q.pop("artifact_sha256",None)
    return hashlib.sha256(json.dumps(q,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def auc(P,N):
    return sum(1 if p>n else .5 if p==n else 0 for p in P for n in N)/(len(P)*len(N))
def validate(p):
    req(p.get("schema")==SCHEMA,"schema");req(p.get("artifact_id")==ARTIFACT,"artifact")
    req(p.get("claim_allowed") is False,"claim_allowed");req(p.get("artifact_sha256")==digest(p),"digest")
    req(INV<=set(p.get("invariants",[])),"invariants")
    a=p["authority"];req(a["repository_role"]=="Mapa federation + validation authority","authority")
    req(a["runtime_producer"]=="TOKEN_VAZIO","runtime producer");req(a["source_bytes_in_repository"] is False,"source bytes")
    req(a["public_private_locator_forbidden"] is True,"private locator")
    d=p["descriptor"];req(d["descriptor_version"]=="PIXEL_DESC_V1" and d["tile_size_px"]==16,"descriptor")
    req(d["determinism_session_repetitions"]>=2 and d["reproduction_scope"]=="session_local_only","scope")
    S=p["sources"];req(len(S)==10,"sources");sids=set();shas=set()
    for s in S:
        sid=s["source_id"];sha=s["sha256"];req(sid not in sids,"source id");req(sha not in shas and len(sha)==64,"source hash")
        req(s["bytes"]>0 and s["width"]>0 and s["height"]>0,"source size");req(s["color_space"]=="RGB" and s["bit_depth"]==24,"pixel format")
        sids.add(sid);shas.add(sha)
    R={}
    for r in p["regions"]:
        rid=r["region_id"];req(rid not in R and r["source_id"] in sids,"region")
        b=r["bounds_normalized"];x0,y0,x1,y1=[float(b[k]) for k in ("x0","y0","x1","y1")]
        req(all(math.isfinite(x) for x in (x0,y0,x1,y1)) and 0<=x0<x1<=1 and 0<=y0<y1<=1,"bounds")
        req(r["annotation_scope"]=="VISUAL_MOTIF_CANDIDATE","region scope");R[rid]=r
    ids=set();links=set();P=[];N=[]
    for z in p["pairs"]:
        pid=z["pair_id"];l=z["left_region_id"];r=z["right_region_id"];rel=z["expected_relation"];score=float(z["descriptor_jaccard_v1"])
        req(pid not in ids and l in R and r in R and l!=r,"pair");req(R[l]["source_id"]!=R[r]["source_id"],"cross-image")
        k=tuple(sorted((l,r)));req(k not in links,"duplicate pair");req(0<=score<=1,"score")
        req(z["annotation_confidence"]=="MANUAL_VISUAL_REVIEW" and z["ground_truth"] is False,"annotation provenance")
        if rel=="POSITIVE_VISUAL_MOTIF": req(isinstance(z["motif"],str) and z["motif"],"positive motif");P.append(score)
        elif rel=="NEGATIVE_VISUAL_MOTIF": req(z["motif"] is None,"negative motif");N.append(score)
        else: raise V("relation")
        ids.add(pid);links.add(k)
    req(len(P)>=10 and len(N)>=10,"anchor count")
    b=p["baseline"];req(b["metric"]=="region_descriptor_keyset_jaccard" and b["acceptance_threshold"]=="TOKEN_VAZIO_NOT_TUNED","baseline")
    req(b["interpretation"]=="diagnostic_only_not_accuracy","interpretation")
    vals={"positive_count":len(P),"negative_count":len(N),"positive_mean":statistics.mean(P),"positive_median":statistics.median(P),"positive_min":min(P),"positive_max":max(P),"negative_mean":statistics.mean(N),"negative_median":statistics.median(N),"negative_min":min(N),"negative_max":max(N),"pairwise_rank_auc":auc(P,N)}
    for k,v in vals.items(): req(abs(float(b[k])-float(v))<=1e-9,"baseline "+k)
    req(GAPS<={g["gap_id"] for g in p["semantic_gaps"]},"gaps")
    req(all(g["state"] in {"SEMANTIC_UNBOUND","PARTIAL_INTERPRETATION","AUTHORITY_MISSING"} for g in p["semantic_gaps"]),"gap closed")
    G={g["gate_id"]:g["state"] for g in p["gate_matrix"]};req(set(G)=={"T1","T2","T3","T4","T5","T6"},"gates")
    req(G["T1"]=="TOKEN_VAZIO_SOURCE_BYTES_NOT_IN_REPOSITORY","T1");req(G["T2"]=="READY_FOR_STATIC_VALIDATION","T2")
    req(all(G[x]=="READY_FOR_STRUCTURAL_VALIDATION" for x in ("T3","T4","T5","T6")),"T3-T6")
    return {"state":"PASS_BOUNDED","sources":len(S),"regions":len(R),"positive_pairs":len(P),"negative_pairs":len(N),"pairwise_rank_auc":round(auc(P,N),12),"T1":G["T1"],"T2":"PASS_STATIC","T3_T6":"PASS_STRUCTURAL","threshold":"TOKEN_VAZIO_NOT_TUNED","claim_allowed":False}
def selftest(base):
    cases=[]
    def bad(name,fn):
        q=copy.deepcopy(base);fn(q);q["artifact_sha256"]=digest(q)
        try: validate(q);cases.append((name,False))
        except V: cases.append((name,True))
    bad("claim",lambda q:q.__setitem__("claim_allowed",True))
    bad("gap",lambda q:q["semantic_gaps"][0].__setitem__("state","PASS"))
    bad("threshold",lambda q:q["baseline"].__setitem__("acceptance_threshold",0.08))
    bad("ground_truth",lambda q:q["pairs"][0].__setitem__("ground_truth",True))
    req(all(ok for _,ok in cases),"selftest")
    return {"state":"PASS","adversarial_cases":len(cases)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--artifact",default="data/multimodal/pixel_manifold_anchor_set.v1.json");ap.add_argument("--self-test",action="store_true");a=ap.parse_args()
    try:
        p=json.loads(Path(a.artifact).read_text());out=validate(p);out["self_test"]=selftest(p) if a.self_test else "NOT_RUN"
        print(json.dumps(out,indent=2,sort_keys=True));return 0
    except (OSError,json.JSONDecodeError,V,KeyError,TypeError,ValueError) as e:
        print(json.dumps({"state":"FAIL","error":str(e),"claim_allowed":False},indent=2));return 1
if __name__=="__main__": raise SystemExit(main())
