#!/usr/bin/env python3
"""Fail-closed typed intake for observer/observed networks. Stdlib only."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "governance" / "observer_observed_network_v1.json"

class ContractError(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise ContractError(message)

def validate(data):
    require(isinstance(data, dict), "root must be an object")
    require(data.get("schema") == "rafaelia.observer-observed-network.v1", "schema drift")
    require(data.get("authority") == "rafaelmeloreisnovo/Mapa", "authority drift")
    for key in ("claim_allowed", "automatic_promotion", "automatic_merge", "direct_main_mutation"):
        require(data.get(key) is False, key + " must be false")
    rules = data.get("rules")
    require(isinstance(rules, dict) and rules and all(x is True for x in rules.values()), "rules must remain enabled")
    for key in ("epistemic_states", "novelty_states", "science_tracks", "conduct",
                "semantic_flags", "relation_kinds", "evidence_effects"):
        values = data.get(key)
        require(isinstance(values, list) and values and len(values) == len(set(values)), key + " invalid")
    require({"OBSERVED", "TOKEN_VAZIO", "HYPOTHESIS", "DERIVED"} <= set(data["epistemic_states"]), "missing epistemic states")
    require("NUMERIC_ZERO" in data["semantic_flags"] and "NO_EVENT_OBSERVED" in data["semantic_flags"], "zero/absence conflated")
    required = {"id", "recorded_date", "observer", "observed", "event_time", "description",
                "epistemic_state", "novelty_state", "science_tracks", "conduct",
                "semantic_flags", "relation_kind", "evidence_effect", "evidence_refs",
                "gaps", "falsifier", "next_gate", "claim_allowed", "promotion_state", "causal_claim"}
    records = data.get("records")
    require(isinstance(records, list) and records, "nonempty records required")
    seen = set()
    for record in records:
        require(isinstance(record, dict) and required <= record.keys(), "record missing required fields")
        rid = record["id"]
        require(isinstance(rid, str) and rid and rid not in seen, "invalid/duplicate id")
        seen.add(rid)
        require(record["claim_allowed"] is False and record["promotion_state"] == "BLOCKED", rid + ": promotion bypass")
        require(record["causal_claim"] is False, rid + ": unverified causal claim")
        require(record["epistemic_state"] in data["epistemic_states"], rid + ": unknown epistemic state")
        require(record["novelty_state"] in data["novelty_states"], rid + ": unknown novelty state")
        for name in ("science_tracks", "conduct", "semantic_flags"):
            value = record[name]
            require(isinstance(value, list) and value and set(value) <= set(data[name]), rid + ": invalid " + name)
        require(record["relation_kind"] in data["relation_kinds"], rid + ": invalid relation")
        require(record["evidence_effect"] in data["evidence_effects"], rid + ": invalid evidence effect")
        require(record["relation_kind"] not in ("HYPOTHESIZES", "SEMANTIC_SIMILARITY", "CAUSAL_CANDIDATE")
                or record["evidence_effect"] in ("NONE", "ROUTING_ONLY"), rid + ": semantic edge promoted to evidence")
        require(isinstance(record["observer"], dict)
                and record["observer"].get("kind") in ("HUMAN", "HUMAN_INTENT", "SENSOR", "PROCESS", "TOOL_READBACK", "DOCUMENT")
                and isinstance(record["observer"].get("ref"), str)
                and record["observer"]["ref"].strip(), rid + ": unidentified observer")
        observed = record["observed"]
        require(isinstance(observed, dict) and isinstance(observed.get("ref"), str) and observed["ref"].strip(), rid + ": observed target missing")
        require(record["observer"] != record["observed"], rid + ": observer conflated with observed")
        require(isinstance(record["recorded_date"], str) and len(record["recorded_date"]) == 10, rid + ": missing date precision")
        for name in ("description", "falsifier", "next_gate"):
            require(isinstance(record[name], str) and record[name].strip(), rid + ": empty " + name)
        gaps = record["gaps"]
        require(isinstance(gaps, list) and all(isinstance(g, str) and g.startswith("TOKEN_VAZIO_") for g in gaps), rid + ": invalid gap typing")
        refs = record["evidence_refs"]
        require(isinstance(refs, list) and all(isinstance(ref, str) and ref.strip() for ref in refs), rid + ": invalid evidence refs")
        if record["epistemic_state"] == "OBSERVED":
            require(bool(refs) and isinstance(observed.get("revision"), str) and len(observed["revision"]) == 40,
                    rid + ": observed fact requires exact source revision and evidence")
        elif record["epistemic_state"] in ("TOKEN_VAZIO", "HYPOTHESIS"):
            require(bool(gaps) and record["evidence_effect"] in ("NONE", "ROUTING_ONLY"),
                    rid + ": unknown/hypothesis cannot be evidence")
            require("NUMERIC_ZERO" not in record["semantic_flags"] or record["epistemic_state"] != "TOKEN_VAZIO",
                    rid + ": missing is not numeric zero")
        if "ATEMPORAL" in record["semantic_flags"]:
            require(record["recorded_date"], rid + ": atemporal semantics do not erase recording clock")
    return {"records": len(records), "typed_gaps": sum(len(x["gaps"]) for x in records)}

def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    result = validate(data)
    print("PASS observer_observed_network_v1 " + json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
