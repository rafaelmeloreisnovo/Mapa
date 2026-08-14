#!/usr/bin/env python3
import json, sys
from pathlib import Path

REQ_LEX = {"provenance","proveniência","proveniencia","custody","custódia","custodia"}
REQ_EXT = {".json",".jsonl"}
EXCLUDED = ("docs/","tests/","tools/","schema/","schemas/")

def validate(d):
    e=[]
    if d.get("schema")!="RAFAELIA_FG006_REPOSITORY_COVERAGE_DELTA_V2": e.append("schema")
    if d.get("claim_allowed") is not False: e.append("claim_allowed")
    if d.get("repository_wide_closed") is not False: e.append("repository_wide_closed")
    snap=d.get("snapshot",{})
    if len(str(snap.get("commit","")))!=40 or len(str(snap.get("tree_sha","")))!=40: e.append("snapshot")
    t=d.get("tree_evidence",{})
    if t.get("recursive") is not True: e.append("tree_recursive")
    if t.get("truncated") is not False: e.append("tree_truncated")
    if t.get("machine_extracted_full_pathset") is not False: e.append("machine_extraction_claim")
    lex=d.get("lexical_contract",{})
    if not REQ_LEX.issubset(set(lex.get("semantic_lexemes",[]))): e.append("lexemes")
    if set(lex.get("extensions",[])) != REQ_EXT: e.append("extensions")
    base=d.get("baseline_candidates",[])
    delta=d.get("discovered_delta",[])
    paths=base+[x.get("path") for x in delta]
    if len(base)!=d.get("parent_ledger",{}).get("candidate_count"): e.append("parent_count")
    if len(delta)!=d.get("discovered_delta_count"): e.append("delta_count")
    if len(paths)!=len(set(paths)): e.append("duplicate_path")
    if d.get("minimum_candidate_count")!=len(paths): e.append("minimum_count")
    if not isinstance(d.get("exhaustive_candidate_count"),str) or not d["exhaustive_candidate_count"].startswith("TOKEN_VAZIO"): e.append("exhaustive_count")
    for i,x in enumerate(delta):
        p=x.get("path","")
        if not any(p.endswith(ext) for ext in REQ_EXT): e.append(f"delta[{i}].extension")
        if p.startswith(EXCLUDED): e.append(f"delta[{i}].excluded")
        sha=x.get("blob_sha1","")
        if len(sha)!=40 or any(c not in "0123456789abcdef" for c in sha): e.append(f"delta[{i}].blob_sha1")
        if not x.get("discovery"): e.append(f"delta[{i}].discovery")
        if not x.get("inspection"): e.append(f"delta[{i}].inspection")
        if not x.get("classification"): e.append(f"delta[{i}].classification")
    open_tv=set(d.get("token_vazio",{}).get("open",[]))
    if "TOKEN_VAZIO_FG006_TREE_PAYLOAD_MACHINE_EXTRACTION_C82" not in open_tv: e.append("machine_tv_missing")
    return e

def main():
    d=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors=validate(d)
    if errors:
        for x in errors: print("REJECT",x)
        return 1
    print(f"PASS fg006-c82 lower_bound={d['minimum_candidate_count']} delta={d['discovered_delta_count']} closed=false")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
