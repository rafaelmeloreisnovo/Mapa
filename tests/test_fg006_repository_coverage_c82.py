#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=R/"data/governance/fg006-repository-coverage-c82-delta.v1.json"
P=R/"tools/validate_fg006_repository_coverage_c82.py"
s=importlib.util.spec_from_file_location("v",P); v=importlib.util.module_from_spec(s); s.loader.exec_module(v)
c=lambda x:json.loads(json.dumps(x))
def q(n,d,ok):
    e=v.validate(d); assert (not e)==ok,(n,e); print("PASS",n)
def main():
    b=json.loads(L.read_text(encoding="utf-8")); q("valid",b,1)
    x=c(b); x["claim_allowed"]=True; q("claim",x,0)
    x=c(b); x["repository_wide_closed"]=True; q("premature-close",x,0)
    x=c(b); x["new_candidates"].append(c(x["new_candidates"][0])); x["summary"]["new_unique_candidate_count"]+=1; x["summary"]["known_candidate_lower_bound"]+=1; q("duplicate-new",x,0)
    x=c(b); x["new_candidates"][0]["path"]=x["predecessor"]["candidate_paths"][0]; q("already-predecessor",x,0)
    x=c(b); x["new_candidates"][0]["path"]="auditoria/cadeia_custodia/not-json.txt"; q("non-json",x,0)
    x=c(b); x["new_candidates"][0]["path"]="data/random/object.json"; q("semantic-mismatch",x,0)
    x=c(b); x["new_candidates"][0]["absent"].remove("receipt"); q("missing-field-bucket",x,0)
    x=c(b); x["new_candidates"][0]["present"].append("timestamp"); q("duplicate-field-bucket",x,0)
    x=c(b); x["summary"]["known_candidate_lower_bound"]=999; q("lower-bound",x,0)
    x=c(b); x["enumeration"]["recursive_tree_attempt"]["exhaustive"]=True; q("fake-exhaustive",x,0)
    x=c(b); x["summary"]["remaining_predecessor_unfetched_count"]=1; q("remaining-tv",x,0)
    x=c(b); x["summary"]["full_fg006_original_contract_count"]=1; q("fake-full",x,0)
    x=c(b); x["summary"]["blocking_token_vazio"]=[]; q("missing-blocking-tv",x,0)
    x=c(b); x["predecessor_token_vazio_resolutions"][0]["path"]="missing/from/predecessor.json"; q("resolution-not-predecessor",x,0)
    print("PASS 15/15")
if __name__=="__main__": main()
