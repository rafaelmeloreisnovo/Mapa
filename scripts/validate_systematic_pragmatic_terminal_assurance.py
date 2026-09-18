#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ASSURANCE_SCHEMA = "rafaelia.systematic-pragmatic-terminal-assurance/v1"
RECEIPT_SCHEMA = "rafaelia.systematic-pragmatic-terminal-receipt/v1"


def load(path: Path):
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path}: root must be object"
    return value


def validate_assurance(d):
    assert d["schema"] == ASSURANCE_SCHEMA
    assert d["claim_allowed"] is False
    assert d["publication_ready"] is False
    assert d["autonomous_objective_creation"] is False
    s = d["structural_routing"]
    assert s["state"] == "COMPLETE_STRUCTURAL_ROUTING"
    assert s["source_gap_bindings"] == 35
    assert s["schema_families_structurally_resolved"] == 25
    assert s["remaining_internal_review_required"] == 0
    assert s["remaining_internal_binding_token_vazio_count"] == 0
    assert len(d["internal_regressions"]) == 2
    assert all(x["local_code_change_authorized"] is True for x in d["internal_regressions"])
    assert all(x.get("remediation_state") == "FIXED_CONFIRMED" for x in d["internal_regressions"])
    assert len(d["external_gates"]) == 4
    assert all(x["local_code_change_authorized"] is False for x in d["external_gates"])
    local = d["local_assurance"]
    assert local["state"] == "PASS"
    assert local["ci"]["conclusion"] == "success"
    assert local["gap_atlas"]["conclusion"] == "success"
    assert local["main_hardening"]["conclusion"] == "success"
    assert local["live_control_plane"]["conclusion"] == "success"
    temporal = d["temporal_routing"]
    assert temporal["state"] == "FRESH_FAIL_CLOSED"
    assert temporal["provider_enforcement_closed"] is False
    assert temporal["independent_approval_closed"] is False
    t = d["terminal_semantics"]
    assert t["structural_routing_complete"] is True
    assert t["repository_local_assurance"] == "PASS"
    assert t["repository_operational_readiness"] == "BLOCKED_BY_EXTERNAL_GATES"
    assert t["external_gate_failure_does_not_reopen_structural_routing"] is True
    assert t["external_gate_failure_remains_explicit"] is True
    assert t["source_record_binding_is_subject_closure"] is False
    return d


def validate_receipt(r, assurance):
    assert r["schema"] == RECEIPT_SCHEMA
    assert r["claim_allowed"] is False
    terminal = r["terminal_assurance"]
    assert terminal["state"] == "COMPLETE_STRUCTURAL_ROUTING_LOCAL_ASSURANCE_PASS_EXTERNAL_GATES_OPEN"
    assert terminal["claim_allowed"] is False
    assert terminal["publication_ready"] is False
    assert terminal["autonomous_objective_creation"] is False
    assert terminal["tested_head"] == assurance["local_assurance"]["tested_head"]
    closure = r["structural_closure"]
    assert closure["source_gap_bindings"] == "35/35"
    assert closure["schema_families_structurally_resolved"] == "25/25"
    assert closure["remaining_internal_review_required"] == 0
    assert closure["remaining_internal_binding_debt"] == 0
    assert closure["canonical_completion_candidates"] == 0
    assert closure["field_review_work_items"] == 0
    assert closure["subject_level_closure"] is False
    local = r["local_assurance"]
    for key in (
        "ci",
        "gap_atlas",
        "main_hardening",
        "live_control_plane",
        "security_codescan",
        "codeql",
        "branch_topology",
        "workflow_graph",
        "workflow_supply_chain_ratchet",
        "human_dignity_ethics",
    ):
        assert local[key]["conclusion"] == "success", f"local assurance not green: {key}"
    debt = local["ci"]["historical_markdown_debt"]
    assert debt["issues"] <= debt["issue_ceiling"]
    assert debt["files_with_issues"] <= debt["file_ceiling"]
    assert len(r["external_gates"]) == 4
    assert all(x["state"] == "BLOCKED_EXTERNAL" for x in r["external_gates"])
    assert all(x.get("authority") and x.get("next") for x in r["external_gates"])
    assert r["temporal_routing"]["state"] == "FRESH_FAIL_CLOSED"
    inv = set(r["invariants"])
    required = {
        "SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM",
        "TOKEN_VAZIO != 0",
        "STRUCTURAL_ROUTING_COMPLETE != EXTERNAL_PROVIDER_READY",
        "LOCAL_ASSURANCE_PASS != PUBLICATION_READY",
        "SOURCE_RECORD_BINDING != SUBJECT_LEVEL_CLOSURE",
        "NO_AUTONOMOUS_GOAL_CREATION",
        "NO_FAKE_APPROVAL",
        "NO_FAKE_CREDENTIAL",
        "NO_FAKE_RULESET",
    }
    assert required <= inv
    return r



def validate_cross_store(x):
    assert x["schema"] == "rafaelia.systematic-pragmatic-terminal-cross-store-receipt/v1"
    assert x["claim_allowed"] is False
    assert x["publication_ready"] is False
    assert x["terminal_state"] == "COMPLETE_STRUCTURAL_ROUTING_LOCAL_ASSURANCE_PASS_EXTERNAL_GATES_OPEN"
    github = x["github"]
    assert github["repository"] == "rafaelmeloreisnovo/Mapa"
    assert github["pr"] == 651
    assert github["state"] == "READY_FOR_INDEPENDENT_REVIEW_NOT_MERGED"
    drive = x["drive"]
    assert drive["start_here"]["document_id"]
    assert drive["start_here"]["revision_id"]
    assert drive["canonical_predecessor"]["append_result"] == "FAILED_PRECONDITION"
    assert drive["canonical_predecessor"]["disposition"] == "PRESERVED_NO_OVERWRITE"
    assert drive["canonical_predecessor"]["cause"].startswith("TOKEN_VAZIO")
    assert drive["canonical_successor"]["document_id"]
    assert drive["canonical_successor"]["revision_id"]
    assert drive["canonical_successor"]["state"] == "WRITTEN"
    custody = x["custody"]
    assert custody["predecessor_preserved"] is True
    assert custody["overwrite_performed"] is False
    assert custody["destructive_edit_performed"] is False
    assert custody["bidirectional_route_materialized"] is True
    assert len(x["external_gates_remain_open"]) == 4
    return x

def main():
    assurance_path = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else "data/governance/SYSTEMATIC_PRAGMATIC_TERMINAL_ASSURANCE_V1.json"
    )
    receipt_path = Path(
        sys.argv[2]
        if len(sys.argv) > 2
        else "data/receipts/pragmatic-map/RECEIPT_SYSTEMATIC_PRAGMATIC_TERMINAL_20260918.json"
    )
    cross_store_path = Path(
        sys.argv[3]
        if len(sys.argv) > 3
        else "data/receipts/pragmatic-map/RECEIPT_SYSTEMATIC_PRAGMATIC_TERMINAL_CROSS_STORE_20260918.json"
    )
    assurance = validate_assurance(load(assurance_path))
    receipt = validate_receipt(load(receipt_path), assurance)
    cross_store = validate_cross_store(load(cross_store_path))
    print(json.dumps({
        "status": "PASS",
        "structural_routing": "COMPLETE",
        "local_assurance": "PASS",
        "external_gates": len(receipt["external_gates"]),
        "external_state": "BLOCKED_EXTERNAL",
        "cross_store": "PASS" if cross_store else "FAIL",
        "claim_allowed": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
