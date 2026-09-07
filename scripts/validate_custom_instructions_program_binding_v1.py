#!/usr/bin/env python3
"""Fail-closed validator for the RAFAELIA custom-instructions program binding.

This validator checks static source/governance semantics only. It does not prove
physical device execution, external provider authority, model training, or a
scientific claim.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "indices" / "ATLAS_X_CUSTOM_INSTRUCTIONS_PROGRAM_BINDING_CURRENT_V1.json"
EXPECTED_SCHEMA = "rafaelia.atlas.custom-instructions-program-binding.v1"
EXPECTED_ID = "ATLAS-X-CUSTOM-INSTRUCTIONS-PROGRAM-BINDING-20260907-V1"
EXPECTED_MISSION_COMMIT = "e7fe94f1394df54b0c62a1bf0bf7bb753c7e78d4"
EXPECTED_EXECUTION_COMMIT = "f29a675ad190c5f68ee77e4b2b044ebc69d438a2"

REQUIRED_FALSE = {
    "dataset_creates_mission_authority",
    "retrieval_context_updates_model_weights",
    "model_output_grants_execution",
    "learn_updates_model_weights",
    "training_or_finetune_authorized",
    "continue_approved_scope_creates_new_goal",
}

REQUIRED_TRUE = {
    "dataset_informs_mission",
    "model_output_is_proposal",
    "learn_is_append_only_program_memory",
    "continue_approved_scope_iterates_f_next",
}

REQUIRED_FORBIDDEN = {
    "DATASET_CONTEXT->PROGRAM_MISSION_AUTHORITY",
    "MODEL_PROPOSAL->EXECUTION_PERMISSION",
    "RETRIEVAL_CONTEXT->WEIGHT_UPDATE",
    "LEARN_APPEND_ONLY->ONLINE_SELF_TRAINING",
    "CONTINUE_APPROVED_SCOPE->AUTONOMOUS_GOAL_CREATION",
    "TOKEN_VAZIO->EVIDENCE",
    "SOURCE_CHECK->SCIENTIFIC_CLAIM",
}

REQUIRED_ROUTE = [
    "PROGRAM_MISSION",
    "ATLAS:X",
    "NOVO:X",
    "L:X",
    "O:X",
    "T:X",
    "REL:X",
    "EVID:X",
    "GAP:X",
    "ContextBundle",
    "IntentIR",
    "Governance",
    "ExecutionPlan",
    "AuthorizedAction",
    "ExecutionResult",
    "ProvenanceReceipt",
    "LEARN:X",
    "F_next",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing binding: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    require(isinstance(data, dict), "binding root must be an object")
    return data


def main() -> int:
    data = load_json(BINDING)

    require(data.get("schema") == EXPECTED_SCHEMA, "unexpected schema")
    require(data.get("binding_id") == EXPECTED_ID, "unexpected binding_id")
    require(data.get("append_only") is True, "append_only must be true")
    require(data.get("claim_allowed") is False, "claim_allowed must remain false")
    require(data.get("result") == "BOUND_FAIL_CLOSED", "binding must remain fail-closed")

    operator = data.get("operator_intent", {})
    require(operator.get("can_refine_execution_route") is True, "operator route refinement must remain enabled")
    require(operator.get("can_create_program_mission_authority") is False, "operator intent must not mint mission authority")
    require(operator.get("can_authorize_model_weight_training") is False, "operator intent binding must not authorize training")

    mission = data.get("program_mission_authority", {})
    require(mission.get("repository") == "rafaelmeloreisnovo/Rafaelia_Private", "mission authority repository drift")
    require(mission.get("branch") == "main", "mission authority branch drift")
    require(mission.get("merge_commit") == EXPECTED_MISSION_COMMIT, "mission authority commit drift")
    require(mission.get("receipt_id") == "MISSION-COHESION-SUCCESSOR-20260907-V1", "mission receipt drift")

    current = data.get("current_execution_receipt", {})
    require(current.get("repository") == "rafaelmeloreisnovo/Mapa", "execution receipt repository drift")
    require(current.get("commit") == EXPECTED_EXECUTION_COMMIT, "execution receipt commit drift")

    semantics = data.get("semantics", {})
    for key in REQUIRED_FALSE:
        require(semantics.get(key) is False, f"{key} must remain false")
    for key in REQUIRED_TRUE:
        require(semantics.get(key) is True, f"{key} must remain true")

    forbidden = set(data.get("forbidden_promotions", []))
    require(REQUIRED_FORBIDDEN <= forbidden, "one or more forbidden promotions disappeared")

    route = data.get("route")
    require(route == REQUIRED_ROUTE, "canonical execution route drift")

    boundary = data.get("execution_boundary", {})
    require(boundary.get("background_execution_asserted") is False, "background execution must not be asserted")
    require(boundary.get("execution_must_be_tool_backed_or_receipted") is True, "execution evidence boundary weakened")
    require(str(boundary.get("physical_android_termux_execution", "")).startswith("TOKEN_VAZIO"), "device execution gap must stay explicit")
    require(str(boundary.get("external_provider_authority", "")).startswith("TOKEN_VAZIO"), "external authority gap must stay explicit")
    require(str(boundary.get("model_weight_training", "")).startswith("TOKEN_VAZIO"), "training gap must stay explicit")

    federation = data.get("observed_federation_scope", {})
    bound = set(federation.get("bound", []))
    required_bound = {
        "rafaelmeloreisnovo/Mapa",
        "rafaelmeloreisnovo/termux-app-rafacodephi",
        "rafaelmeloreisnovo/llamaRafaelia",
        "rafaelmeloreisnovo/GAIA_phi",
        "rafaelmeloreisnovo/Rafaelia_Private",
        "rafaelmeloreisnovo/RafNet-Core",
        "rafaelmeloreisnovo/Cosmos",
        "rafaelmeloreisnovo/Rafaelia_Core",
    }
    require(required_bound <= bound, "observed federation scope regressed")
    require(str(federation.get("all_other_repositories", "")).startswith("TOKEN_VAZIO"), "unobserved repository scope must remain TOKEN_VAZIO")

    print("PASS: custom-instructions program binding invariants preserved")
    print("scope=STATIC_SOURCE_GOVERNANCE_ONLY claim_allowed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
