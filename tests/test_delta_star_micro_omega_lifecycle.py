#!/usr/bin/env python3
import copy, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/governance/RAFAELIA_DELTA_STAR_MICRO_OMEGA_LIFECYCLE_V1.json"
VAL=ROOT/"tools/validate_delta_star_micro_omega_lifecycle.py"
spec=importlib.util.spec_from_file_location("lifeval",VAL)
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
BASE=json.loads(DATA.read_text(encoding="utf-8"))

def check(name, mutate, expected_ok):
    d=copy.deepcopy(BASE); mutate(d)
    errors=v.validate(d)
    assert (not errors)==expected_ok,(name,errors)
    print("PASS",name)

def main():
    check("valid",lambda d:None,True)
    check("claim-promotion",lambda d:d.__setitem__("claim_allowed",True),False)
    check("cycle-broken",lambda d:d.__setitem__("cycle",["DELTA","OMEGA"]),False)
    check("token-vazio-missing",lambda d:d.__setitem__("discovery_labels",[x for x in d["discovery_labels"] if x!="TOKEN_VAZIO"]),False)
    check("omega-absolute",lambda d:d["phase_contracts"]["OMEGA"].__setitem__("forbidden",[]),False)
    check("sigma-unbounded",lambda d:d.__setitem__("six_sigma_boundary","sigma 6 achieved"),False)
    check("metric-missing",lambda d:d["phase_contracts"]["MICRO_PER_MILLE"]["metrics"].pop("regression_rate"),False)
    check("priority-urgency-only",lambda d:d["priority_function"].__setitem__("dimensions",["urgency"]),False)
    check("allow-history-overwrite",lambda d:d["anti_regression"].__setitem__("historical_state_never_silently_overwritten",False),False)
    check("coerce-empty-to-zero",lambda d:d["anti_regression"].__setitem__("token_vazio_never_coerced_to_zero",False),False)
    check("parallel-architecture",lambda d:d["current_integration"].__setitem__("status","NEW_PARALLEL_SYSTEM"),False)
    check("missing-fnext",lambda d:d.__setitem__("F_next",""),False)
    print("PASS 12/12")

if __name__=="__main__":
    main()
