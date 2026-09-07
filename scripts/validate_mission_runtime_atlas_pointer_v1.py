#!/usr/bin/env python3
"""Validate the Mapa MissionExecution runtime-evidence pointer fail-closed."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POINTER = ROOT / "indices/ATLAS_X_MISSION_RUNTIME_CURRENT_V1.json"
RECEIPT = ROOT / "receipts/2026-09-07_ATLAS_MISSION_RUNTIME_EVIDENCE_CLOSURE_V1.json"
SHA1 = re.compile(r"^[0-9a-f]{40}$")

EXPECTED_GATES = {
    "physical_android_termux_execution": "TOKEN_VAZIO_DEVICE",
    "exact_multi_repository_runtime_execution": "TOKEN_VAZIO_EXECUTION",
    "remote_network_identity": "TOKEN_VAZIO_RUNTIME",
    "provider_or_legal_authorization": "TOKEN_VAZIO_EXTERNAL_AUTHORITY",
    "live_default_branch_ruleset": "FAIL_PROVIDER_OBSERVED_DISABLED",
    "server_merge_enforcement": "TOKEN_VAZIO_EXTERNAL_AUTHORITY",
    "manual_promotion_decision": "TOKEN_VAZIO_MANUAL_AUTHORITY",
    "codescan_credentialed_analysis": "TOKEN_VAZIO_SECRET",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    try:
        p = load(POINTER)
        r = load(RECEIPT)

        require(p["schema"] == "rafaelia.atlas_mission_runtime_evidence_pointer/v1", "pointer schema")
        require(p["route_id"] == "ATLAS:X-MISSION-RUNTIME-EVIDENCE-CLOSURE-20260907", "route id")
        require(p["state"] == "SOURCE_READY_EXTERNAL_GATES_ONLY", "state")
        require(p["claim_allowed"] is False, "claim_allowed")
        require(p["scientific_claim_promotion"] is False, "scientific claim")
        require(p["weight_training_authorized"] is False, "weight training")
        require(p["authority"]["Mapa"] == "FEDERATED_ROUTING_STATE_ONLY", "Mapa authority")
        require(p["authority"]["producer_implementation_claims_stay_with_producers"] is True, "producer authority")

        producer = p["producer_evidence"]
        require(producer["repository"] == "rafaelmeloreisnovo/termux-app-rafacodephi", "producer repo")
        require(producer["pull_request"] == 431, "producer PR")
        require(SHA1.fullmatch(producer["merge_commit"]) is not None, "producer merge sha")
        require(SHA1.fullmatch(producer["contract"]["git_blob_sha1"]) is not None, "contract blob")
        require(SHA1.fullmatch(producer["validator"]["git_blob_sha1"]) is not None, "validator blob")
        require(producer["source_gate"]["run_id"] == 34100074268, "source run")
        require(producer["source_gate"]["conclusion"] == "SUCCESS", "source run result")
        require(producer["source_gate"]["proves_physical_or_external_execution"] is False, "scope promotion")

        require(p["open_evidence_gates"] == EXPECTED_GATES, "gate set/state mismatch")
        require(sum(str(v).startswith("TOKEN_VAZIO") for v in EXPECTED_GATES.values()) == 7, "expected TOKEN_VAZIO count")
        require(sum(str(v).startswith("FAIL_") for v in EXPECTED_GATES.values()) == 1, "expected FAIL count")

        provider = p["external_provider_observations"]
        ruleset = provider["live_default_branch_ruleset"]
        require(ruleset["provider"] == "GitHub", "ruleset provider")
        require(ruleset["repository"] == "rafaelmeloreisnovo/Mapa", "ruleset repository")
        require(ruleset["ruleset_id"] == 21909304, "ruleset id")
        require(ruleset["condition"] == "~DEFAULT_BRANCH", "ruleset condition")
        require(ruleset["enforcement"] == "disabled", "ruleset must remain observed disabled")
        require(ruleset["observed_state"] == "FAIL_PROVIDER_OBSERVED_DISABLED", "ruleset observed state")
        require(ruleset["promotion"] == "DENIED", "ruleset promotion")
        protection = provider["branch_protection_detail"]
        require(protection["provider_result"] == "403_RESOURCE_NOT_ACCESSIBLE_BY_INTEGRATION", "branch protection provider result")
        require(protection["observed_state"] == "TOKEN_VAZIO_EXTERNAL_AUTHORITY", "branch protection detail state")
        require(protection["promotion"] == "DENIED", "branch protection promotion")

        require(p["non_gates"]["model_weight_training"] == "NOT_AUTHORIZED", "training non-gate")
        require(p["non_gates"]["scientific_claim_promotion"] == "BLOCKED", "science non-gate")
        require(len(p["q01_q12"]) == 12, "Q01-Q12 count")
        require(p["completion"]["source_side_program_closure"] is True, "source closure")
        require(p["completion"]["external_execution_closure"] is False, "external closure must remain false")
        require(p["completion"]["terminal_state_promotes_scientific_claim"] is False, "terminal scientific promotion")
        require(p["completion"]["terminal_state_authorizes_weight_training"] is False, "terminal training promotion")

        require(r["schema"] == "rafaelia.atlas_mission_runtime_evidence_receipt/v1", "receipt schema")
        require(r["claim_allowed"] is False, "receipt claim_allowed")
        require(r["scientific_claim_promotion"] is False, "receipt scientific claim")
        require(r["weight_training_authorized"] is False, "receipt weight training")
        require(r["pointer"]["route_id"] == p["route_id"], "receipt pointer route")
        require(r["pointer"]["git_blob_sha1"] == "5d44e53827009c0033bb44123033f496786d5bcc", "receipt pointer blob")
        require(r["producer"]["merge_commit"] == producer["merge_commit"], "receipt producer merge")
        require(r["producer"]["workflow_run_id"] == producer["source_gate"]["run_id"], "receipt workflow run")
        require(r["producer"]["workflow_result"] == "SUCCESS", "receipt workflow result")
        require(r["producer"]["physical_or_external_execution_proven"] is False, "receipt scope promotion")

        rr = r["provider_observations"]["live_default_branch_ruleset"]
        require(rr["ruleset_id"] == ruleset["ruleset_id"], "receipt ruleset id")
        require(rr["enforcement"] == "disabled", "receipt ruleset enforcement")
        require(rr["state"] == "FAIL_PROVIDER_OBSERVED_DISABLED", "receipt ruleset state")
        require(r["provider_observations"]["branch_protection_detail"]["state"] == "TOKEN_VAZIO_EXTERNAL_AUTHORITY", "receipt branch protection detail")

        decision = r["federation_decision"]
        require(decision["required_gate_count"] == 8, "receipt required gate count")
        require(decision["token_vazio_gate_count"] == 7, "receipt TOKEN_VAZIO count")
        require(decision["observed_failing_gate_count"] == 1, "receipt FAIL count")
        require(decision["gate_states"] == EXPECTED_GATES, "receipt gate state map")
        require(decision["model_weight_training"] == "NOT_AUTHORIZED", "receipt training")
        require(decision["scientific_claim_promotion"] == "BLOCKED", "receipt science")

        raw = POINTER.read_text(encoding="utf-8") + RECEIPT.read_text(encoding="utf-8")
        for forbidden in ('"credential":', '"token":', '"secret":', '"password":'):
            require(forbidden not in raw.lower(), f"forbidden secret field persisted: {forbidden}")

        print("PASS Atlas MissionExecution runtime pointer/receipt fail-closed")
        print("state=SOURCE_READY_EXTERNAL_GATES_ONLY required_gates=8 token_vazio=7 observed_fail=1 claim_allowed=false")
        return 0
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL_CLOSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
