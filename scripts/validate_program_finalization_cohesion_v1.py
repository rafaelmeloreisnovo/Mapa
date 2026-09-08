#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "indices" / "ATLAS_X_PROGRAM_FINALIZATION_CURRENT_V1.json"

EXPECTED_GATES = {
    "physical_android_termux_execution",
    "exact_multi_repository_runtime_execution",
    "remote_network_identity",
    "provider_or_legal_authorization",
    "live_default_branch_ruleset",
    "server_merge_enforcement",
    "manual_promotion_decision",
    "codescan_credentialed_analysis",
}

FORBIDDEN_PASS_VALUES = {"TOKEN_VAZIO", "UNKNOWN", "UNVERIFIED", "PENDING"}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    contract = data.get("program_contract", {})
    completion = data.get("completion", {})
    gates = data.get("external_evidence_gates", {})
    invariants = set(data.get("invariants", []))

    if data.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")
    if data.get("weight_training_authorized") is not False:
        fail("weight training must remain unauthorized")
    if data.get("autonomous_goal_creation") is not False:
        fail("autonomous goal creation must remain false")

    if contract.get("dataset_creates_mission_authority") is not False:
        fail("dataset must not create mission authority")
    if contract.get("model_output_grants_execution") is not False:
        fail("model output must not grant execution")
    if contract.get("model_can_create_independent_goal") is not False:
        fail("model must not create independent goals")
    if contract.get("learn_updates_model_weights") is not False:
        fail("LEARN:X must not update model weights")
    if contract.get("retrieval_updates_model_weights") is not False:
        fail("retrieval must not update model weights")
    if contract.get("training_or_finetune_authorized") is not False:
        fail("training/finetune must not be authorized")

    required_invariants = {
        "DATASET_CONTEXT!=PROGRAM_MISSION_AUTHORITY",
        "MODEL_PROPOSAL!=EXECUTION_PERMISSION",
        "RETRIEVAL_CONTEXT!=WEIGHT_UPDATE",
        "LEARN_APPEND_ONLY!=ONLINE_SELF_TRAINING",
        "CONTINUE_APPROVED_SCOPE!=AUTONOMOUS_GOAL_CREATION",
        "TOKEN_VAZIO!=EVIDENCE",
        "CI_SUCCESS!=PHYSICAL_RUNTIME_PROOF",
        "SOURCE_CHECK!=SCIENTIFIC_CLAIM",
    }
    missing = required_invariants - invariants
    if missing:
        fail(f"missing invariants: {sorted(missing)}")

    if set(gates) != EXPECTED_GATES:
        fail(f"external gate set drifted: {sorted(set(gates) ^ EXPECTED_GATES)}")

    unresolved = []
    for name, value in gates.items():
        if not isinstance(value, str) or not value:
            fail(f"gate {name} has invalid state")
        upper = value.upper()
        if upper != "PASS":
            unresolved.append(name)
        if any(token in upper for token in FORBIDDEN_PASS_VALUES) and upper == "PASS":
            fail(f"gate {name} promoted unsupported state to PASS")

    if completion.get("source_side_program_closure") is not True:
        fail("source-side program closure must be true")
    if completion.get("source_side_cohesion_closure") is not True:
        fail("source-side cohesion closure must be true")

    if unresolved:
        if completion.get("external_execution_closure") is not False:
            fail("external execution closure cannot be true while gates are unresolved")
        if completion.get("terminal_allowed_now") is not False:
            fail("terminal state cannot be allowed while gates are unresolved")
    else:
        if completion.get("terminal_allowed_now") is not True:
            fail("all gates PASS but terminal_allowed_now is not true")

    if completion.get("terminal_state_promotes_scientific_claim") is not False:
        fail("terminal state must not promote scientific claims")
    if completion.get("terminal_state_authorizes_weight_training") is not False:
        fail("terminal state must not authorize weight training")

    print("PASS: RAFAELIA program finalization cohesion V1 is fail-closed and internally coherent")
    print(f"unresolved_external_gates={len(unresolved)}")
    for gate in unresolved:
        print(f"OPEN {gate}={gates[gate]}")


if __name__ == "__main__":
    main()
