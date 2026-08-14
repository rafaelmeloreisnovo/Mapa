#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys, unicodedata
from pathlib import Path

REQ={"provider","path_or_id","hash","timestamp","generator","parent","execution","receipt"}
BUCKETS=("present","partial","absent","not_applicable")
HEX40=re.compile(r"^[0-9a-f]{40}$")

def norm(s):
    s=unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+","_",s).strip("_")

def field_partition(x,prefix,errors):
    used=set()
    for b in BUCKETS:
        vals=x.get(b)
        if not isinstance(vals,list):
            errors.append(f"{prefix}.{b}")
            continue
        sv=set(vals)
        if len(sv)!=len(vals):
            errors.append(f"{prefix}.{b}_duplicate")
        if used & sv:
            errors.append(f"{prefix}.overlap")
        used |= sv
    if used != REQ:
        errors.append(f"{prefix}.field_partition")
    return used

def validate(d):
    e=[]
    if d.get("schema")!="RAFAELIA_FG006_REPOSITORY_COVERAGE_DELTA_V1": e.append("schema")
    if d.get("claim_allowed") is not False: e.append("claim_allowed")
    enum=d.get("enumeration",{})
    tree=enum.get("recursive_tree_attempt",{})
    exhaustive=tree.get("exhaustive")
    if d.get("repository_wide_closed") is not False: e.append("premature_close")
    if exhaustive is True:
        if tree.get("github_truncated_flag_observed") is not False or tree.get("connector_output_clipped_before_truncated_flag") is not False:
            e.append("invalid_exhaustive_proof")
    aliases={norm(x) for x in enum.get("semantic_aliases",[])}
    if not {"provenance","custody","custodia","cadeia_custodia"} <= aliases:
        e.append("semantic_aliases")

    pred=d.get("predecessor",{})
    paths=pred.get("candidate_paths")
    if not isinstance(paths,list) or len(paths)!=pred.get("candidate_count"):
        e.append("predecessor_count")
        paths=[]
    if len(set(paths))!=len(paths): e.append("predecessor_duplicate")
    predset=set(paths)

    new=d.get("new_candidates")
    if not isinstance(new,list): return e+["new_candidates"]
    seen=set()
    for i,x in enumerate(new):
        p=x.get("path")
        q=f"new[{i}]"
        if not isinstance(p,str) or not p: e.append(f"{q}.path"); continue
        if p in seen: e.append(f"{q}.duplicate")
        seen.add(p)
        if p in predset: e.append(f"{q}.already_predecessor")
        if not (p.endswith(".json") or p.endswith(".jsonl")): e.append(f"{q}.extension")
        np=norm(p)
        if not any(a in np for a in aliases): e.append(f"{q}.semantic_match")
        if not HEX40.fullmatch(str(x.get("source_git_blob_sha1",""))): e.append(f"{q}.blob")
        if not str(x.get("inspection","")).startswith("CONTENT_FETCHED_C82"): e.append(f"{q}.inspection")
        field_partition(x,q,e)

    res=d.get("predecessor_token_vazio_resolutions")
    if not isinstance(res,list): return e+["resolutions"]
    rseen=set()
    for i,x in enumerate(res):
        p=x.get("path"); q=f"resolution[{i}]"
        if p not in predset: e.append(f"{q}.not_predecessor")
        if p in rseen: e.append(f"{q}.duplicate")
        rseen.add(p)
        if not HEX40.fullmatch(str(x.get("source_git_blob_sha1",""))): e.append(f"{q}.blob")
        if not str(x.get("inspection","")).startswith("CONTENT_FETCHED_C82"): e.append(f"{q}.inspection")
        field_partition(x,q,e)

    s=d.get("summary",{})
    if s.get("predecessor_candidate_count")!=pred.get("candidate_count"): e.append("summary_predecessor")
    if s.get("new_unique_candidate_count")!=len(new): e.append("summary_new")
    if s.get("known_candidate_lower_bound")!=pred.get("candidate_count",0)+len(new): e.append("lower_bound")
    if s.get("predecessor_content_fetched_count_c82")!=len(res): e.append("resolution_count")
    if s.get("predecessor_unfetched_or_applicability_count_before")!=len(res): e.append("resolution_baseline")
    if s.get("remaining_predecessor_unfetched_count")!=0: e.append("remaining_predecessor_tv")
    if s.get("full_fg006_original_contract_count")!=0: e.append("unexpected_full")
    if s.get("exhaustive_tree_proof") is not False: e.append("summary_exhaustive")
    blocking=s.get("blocking_token_vazio")
    if not isinstance(blocking,list) or "TOKEN_VAZIO_FG006_EXHAUSTIVE_TRACKED_TREE_ENUMERATION_C82" not in blocking:
        e.append("blocking_tv")
    return e

def main():
    d=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    e=validate(d)
    if e:
        for x in e: print("REJECT",x)
        return 1
    print(f"PASS fg006-coverage-c82 lower_bound={d['summary']['known_candidate_lower_bound']} new={len(d['new_candidates'])} resolved={len(d['predecessor_token_vazio_resolutions'])} closed=false")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
