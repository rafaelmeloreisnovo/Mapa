#!/usr/bin/env python3
import copy,importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];L=R/"data/governance/fg006-repository-coverage-c84-reconciliation.v1.json";P=R/"tools/validate_fg006_repository_coverage_c84.py"
s=importlib.util.spec_from_file_location("v",P);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);B=json.loads(L.read_text())
def q(n,f,ok):
 d=copy.deepcopy(B);f(d);e=v.validate(d);assert(not e)==ok,(n,e);print("PASS",n)
def main():
 q("valid",lambda d:None,1)
 q("claim",lambda d:d.__setitem__("claim_allowed",True),0)
 q("close",lambda d:d.__setitem__("repository_wide_closed",True),0)
 q("wrong-cycle",lambda d:d.__setitem__("cycle_id","OMEGA-ANTI-REGRESSION-C83"),0)
 q("missing-trail",lambda d:d.__setitem__("trail_id",""),0)
 q("bad-cycle-uid",lambda d:d.__setitem__("cycle_uid","C84"),0)
 q("collision-uncontained",lambda d:d["cycle_identity"].__setitem__("collision_state","OPEN"),0)
 q("allocation-nonzero",lambda d:d["cycle_identity"]["allocation_probe"].__setitem__("drive_results",1),0)
 q("parent-head",lambda d:d["parent_c82"].__setitem__("head","0"*40),0)
 q("parent-count",lambda d:d["parent_c82"].__setitem__("minimum_candidate_count",29),0)
 q("tree-overclaim",lambda d:d["parent_c82"].__setitem__("machine_extracted_full_pathset",True),0)
 q("merge-authorized",lambda d:d["concurrency_containment"].__setitem__("merge_authorized",True),0)
 q("resolution-count",lambda d:d["c81_unfetched_resolution"].__setitem__("remaining",1),0)
 q("duplicate-record",lambda d:d["c81_unfetched_resolution"]["records"].__setitem__(1,copy.deepcopy(d["c81_unfetched_resolution"]["records"][0])),0)
 q("field-partition",lambda d:d["c81_unfetched_resolution"]["records"][0]["not_applicable"].pop(),0)
 q("custody-window",lambda d:d["inspection_upgrades"][0].__setitem__("observed_event_count",14),0)
 q("source-window",lambda d:d["inspection_upgrades"][1].__setitem__("observed_record_count",22),0)
 q("candidate-overclaim",lambda d:d["candidate_accounting"].__setitem__("current_lower_bound",31),0)
 q("missing-tree-tv",lambda d:d["token_vazio"].__setitem__("open",["TOKEN_VAZIO_GLOBAL_CYCLE_ID_ATOMIC_ALLOCATION"]),0)
 q("missing-allocator-tv",lambda d:d["token_vazio"].__setitem__("open",["TOKEN_VAZIO_FG006_TREE_PAYLOAD_MACHINE_EXTRACTION_C82"]),0)
 print("PASS 20/20")
if __name__=="__main__":main()
