#!/usr/bin/env python3
import json, sys
from pathlib import Path

EXPECTED_CYCLE=["DELTA","STAR","MICRO_PER_MILLE","OMEGA","DELTA"]
PHASES={"DELTA","STAR","MICRO_PER_MILLE","OMEGA"}
REQ_LABELS={"TOKEN_VAZIO","absence","urgent","provenance","contract","necessary","important","forgotten","ignored","obvious","censored","left_behind","suggested","should","good_candidate","aborted","uncertain"}
REQ_METRICS={"regression_rate","closure_rate","evidence_coverage","token_vazio_resolution_rate","defect_density","dpmo_optional"}
REQ_PRIORITY={"impact","urgency","dependency_blocking","evidence_deficit","provenance_risk","regression_risk","reversibility"}

def validate(d):
    e=[]
    if d.get("schema")!="rafaelia.delta-star-micro-omega-lifecycle/v1": e.append("schema")
    if d.get("claim_allowed") is not False: e.append("claim_allowed")
    if d.get("append_only") is not True: e.append("append_only")
    if d.get("cycle")!=EXPECTED_CYCLE: e.append("cycle")
    pc=d.get("phase_contracts",{})
    if set(pc)!=PHASES: e.append("phase_contracts")
    for p in PHASES:
        x=pc.get(p,{})
        if not x.get("purpose"): e.append(f"{p}.purpose")
        if not x.get("required"): e.append(f"{p}.required")
        if not x.get("forbidden"): e.append(f"{p}.forbidden")
        if not x.get("exit_gate"): e.append(f"{p}.exit_gate")
    labels=set(d.get("discovery_labels",[]))
    if not REQ_LABELS.issubset(labels): e.append("discovery_labels")
    rule=str(d.get("label_rule","")).lower()
    if "never constitute evidence" not in rule: e.append("label_rule")
    metrics=set(pc.get("MICRO_PER_MILLE",{}).get("metrics",{}))
    if metrics!=REQ_METRICS: e.append("metrics")
    pd=set(d.get("priority_function",{}).get("dimensions",[]))
    if pd!=REQ_PRIORITY: e.append("priority_dimensions")
    ss=str(d.get("six_sigma_boundary","")).lower()
    for term in ("measured defects","opportunities","sampling plan","receipt"):
        if term not in ss: e.append("six_sigma_boundary"); break
    ar=d.get("anti_regression",{})
    for k in ("closed_state_requires_evidence","negative_results_append_only","new_conflict_reopens_delta","historical_state_never_silently_overwritten","token_vazio_never_coerced_to_zero"):
        if ar.get(k) is not True: e.append(f"anti_regression.{k}")
    integ=d.get("current_integration",{})
    if integ.get("parent_pr")!=223: e.append("parent_pr")
    if integ.get("status")!="EXTENDS_EXISTING_WINDOWS_NOT_PARALLEL_ARCHITECTURE": e.append("integration_status")
    if not d.get("F_next"): e.append("F_next")
    return sorted(set(e))

def main():
    if len(sys.argv)!=2:
        print("usage: validate_delta_star_micro_omega_lifecycle.py <json>")
        return 2
    d=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    e=validate(d)
    if e:
        for x in e: print("REJECT",x)
        return 1
    print("PASS delta-star-micro-omega lifecycle fail-closed contract")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
