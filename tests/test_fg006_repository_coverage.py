#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]; L=R/"data/governance/fg006-repository-coverage-c81.v1.json"; P=R/"tools/validate_fg006_repository_coverage.py"
s=importlib.util.spec_from_file_location("v",P);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
c=lambda x:json.loads(json.dumps(x))
def q(n,d,ok):
 e=v.validate(d);assert (not e)==ok,(n,e);print("PASS",n)
def main():
 b=json.loads(L.read_text());q("valid",b,1)
 x=c(b);x["claim_allowed"]=True;q("claim",x,0)
 x=c(b);x["repository_wide_closed"]=True;q("close",x,0)
 x=c(b);x["records"].append(c(x["records"][0]));x["summary"]["candidate_count"]+=1;x["summary"]["content_inspected_count"]+=1;q("duplicate",x,0)
 x=c(b);x["records"][0]["present"].append("magic");q("unknown-field",x,0)
 x=c(b);x["summary"]["candidate_count"]=99;q("count",x,0)
 print("PASS 6/6")
if __name__=="__main__":main()
