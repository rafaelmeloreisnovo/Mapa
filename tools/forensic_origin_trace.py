#!/usr/bin/env python3
"""Fail-closed forensic origin overlay for RAFAELIA operational ontology."""
from __future__ import annotations
import argparse, json
from pathlib import Path

UNRESOLVED={"TOKEN_VAZIO","HIPOTESE","ESTIMATIVA","CONJECTURA","BOTH","NEITHER","SCOPE_SPLIT"}

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def incoming(records):
    inc={r["id"]:[] for r in records}
    for r in records:
        for rel in r.get("relations",[]):
            if rel.get("target") in inc:
                inc[rel["target"]].append({"source":r["id"],"operator":rel.get("operator"),"scope":rel.get("scope")})
    return inc

def trace(ontology, contract):
    records=ontology.get("records",[])
    inc=incoming(records)
    out=[]
    for r in records:
        if r.get("epistemic_state") not in UNRESOLVED:
            continue
        override=contract.get("record_overrides",{}).get(r["id"],{})
        root_kind=contract.get("gap_root_map",{}).get(r.get("gap_class"),"UNCLASSIFIED_BLOCKER")
        overlay="BLOCKED_BY_ACCESS" if r.get("gap_class")=="TV-ACCESS" else "BLOCKED_BY_GOVERNANCE" if "ethics" in (r.get("reason") or "").lower() else "FIRST_BLOCKER_IDENTIFIED"
        out.append({
            "record_id":r["id"],
            "editorial_status_preserved":r.get("status"),
            "epistemic_state_preserved":r.get("epistemic_state"),
            "source_gap_class":r.get("gap_class"),
            "source_reason":r.get("reason"),
            "source_decision_context":r.get("decision_context"),
            "source_provenance":r.get("provenance",[]),
            "incoming_relations":inc.get(r["id"],[]),
            "blocker_family":root_kind,
            "first_observed_blocker":override.get("first_blocker",r.get("reason") or "TOKEN_VAZIO"),
            "required_evidence":override.get("required_evidence",r.get("next_gate")),
            "discriminating_test":override.get("discriminating_test",(r.get("falsifiers") or ["TOKEN_VAZIO_TEST"])[0]),
            "next_gate_preserved":r.get("next_gate"),
            "overlay_state":overlay,
            "root_cause_state":"ROOT_CAUSE_NOT_PROVEN",
            "promotion_allowed":False
        })
    return {
        "schema":"rafaelia.forensic-origin-trace-report/v1",
        "claim_allowed":False,
        "source_ontology_version":ontology.get("metadata",{}).get("version"),
        "records":out,
        "summary":{
            "unresolved_traced":len(out),
            "promotion_allowed":0,
            "rule":"trace origin before editorial/scientific promotion"
        }
    }

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--ontology",required=True)
    p.add_argument("--contract",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args(argv)
    report=trace(load(a.ontology),load(a.contract))
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(report["summary"],sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
