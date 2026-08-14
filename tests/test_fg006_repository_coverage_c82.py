#!/usr/bin/env python3
import copy, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LP=ROOT/"data/governance/fg006-repository-coverage-c82.v2.json"
VP=ROOT/"tools/validate_fg006_repository_coverage_c82.py"
spec=importlib.util.spec_from_file_location("v",VP)
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
base=json.loads(LP.read_text(encoding="utf-8"))

def chk(name,mut,ok):
    d=copy.deepcopy(base); mut(d)
    errs=v.validate(d)
    assert (not errs)==ok,(name,errs)
    print("PASS",name)

def main():
    chk("valid",lambda d:None,True)
    chk("claim-true",lambda d:d.__setitem__("claim_allowed",True),False)
    chk("closed-true",lambda d:d.__setitem__("repository_wide_closed",True),False)
    chk("truncated-true",lambda d:d["tree_evidence"].__setitem__("truncated",True),False)
    chk("recursive-false",lambda d:d["tree_evidence"].__setitem__("recursive",False),False)
    chk("machine-extraction-overclaim",lambda d:d["tree_evidence"].__setitem__("machine_extracted_full_pathset",True),False)
    chk("missing-localized-lexeme",lambda d:d["lexical_contract"].__setitem__("semantic_lexemes",["provenance","custody"]),False)
    chk("duplicate-path",lambda d:d["discovered_delta"].__setitem__(0,dict(d["discovered_delta"][0],path=d["baseline_candidates"][0])),False)
    chk("excluded-delta",lambda d:d["discovered_delta"].__setitem__(0,dict(d["discovered_delta"][0],path="schemas/custodia.json")),False)
    chk("bad-blob",lambda d:d["discovered_delta"][0].__setitem__("blob_sha1","abc"),False)
    chk("count-overclaim",lambda d:d.__setitem__("minimum_candidate_count",31),False)
    chk("remove-machine-tv",lambda d:d["token_vazio"].__setitem__("open",[x for x in d["token_vazio"]["open"] if "TREE_PAYLOAD_MACHINE_EXTRACTION" not in x]),False)
    print("PASS 12/12")

if __name__=="__main__":
    main()
