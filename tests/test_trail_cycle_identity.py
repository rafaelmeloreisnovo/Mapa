#!/usr/bin/env python3
import copy,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/"tools/validate_trail_cycle_identity.py"
s=importlib.util.spec_from_file_location("v",P);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
BASE={"trail_id":"OPERATIONAL_DASHBOARD","trail_seq":1,"cycle_uid":"OPERATIONAL_DASHBOARD-001-20260814T015917Z-7f377447","legacy_local_cycle":"C83","claim_allowed":False}

def q(name,records,ok):
    e=v.validate_many(records);assert (not e)==ok,(name,e);print("PASS",name)

def main():
    q("valid",[copy.deepcopy(BASE)],True)
    x=copy.deepcopy(BASE);x["trail_id"]="bad trail";q("bad-trail",[x],False)
    x=copy.deepcopy(BASE);x["trail_seq"]=0;q("bad-seq",[x],False)
    x=copy.deepcopy(BASE);x["cycle_uid"]="C83";q("bare-cycle-rejected",[x],False)
    x=copy.deepcopy(BASE);x["cycle_uid"]="OTHER-001-20260814T015917Z-7f377447";q("prefix-mismatch",[x],False)
    x=copy.deepcopy(BASE);x["legacy_local_cycle"]="83";q("bad-legacy",[x],False)
    x=copy.deepcopy(BASE);x["claim_allowed"]=True;q("claim-promotion",[x],False)
    q("duplicate-cycle-uid",[copy.deepcopy(BASE),copy.deepcopy(BASE)],False)
    y=copy.deepcopy(BASE);y["trail_id"]="FG006_REPOSITORY_COVERAGE";y["trail_seq"]=84;y["cycle_uid"]="FG006_REPOSITORY_COVERAGE-084-20260814T015300Z-97ca494e";q("same-legacy-different-trail-allowed",[copy.deepcopy(BASE),y],True)
    print("PASS 9/9")
if __name__=="__main__":main()
