#!/usr/bin/env python3
"""Validate the RAFAELIA federated custody-chain type registry.

This validator is intentionally dependency-free and does not replace the
historical mapa.custody-event.v1 validator. It validates the federation layer
that differentiates custody by surface, evidence type and actor authority.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "data/control-plane/CUSTODY_CHAIN_TYPE_REGISTRY.v1.json"

ALLOWED_SURFACES = {"GITHUB", "GOOGLE_DRIVE", "RUNTIME", "CROSS_SURFACE"}
REQUIRED_ACTORS = {
    "HUMAN_AUTHORITY",
    "ASSISTANT_ORCHESTRATOR",
    "CONNECTOR_PROVIDER",
    "RUNTIME_EXECUTOR",
    "INDEPENDENT_REVIEWER",
    "TOKEN_VAZIO_ACTOR",
}
REQUIRED_PROFILES = {
    "GITHUB_SOURCE_CODE_CUSTODY",
    "GITHUB_REVIEW_PROMOTION_CUSTODY",
    "GITHUB_ACTIONS_EXECUTION_CUSTODY",
    "DRIVE_DOCUMENT_REVISION_CUSTODY",
    "DRIVE_CONTENT_MATERIALIZATION_CUSTODY",
    "DRIVE_MOVE_RENAME_CUSTODY",
    "TRANSFORMATION_LINEAGE_CUSTODY",
    "EVIDENCE_CUSTODY",
    "AGENT_ACTION_CUSTODY",
    "CREDENTIAL_PERMISSION_CUSTODY",
    "CROSS_SURFACE_BINDING_CUSTODY",
    "RECEIPT_CHAIN_CUSTODY",
}
MISSING_BEHAVIOR = "TOKEN_VAZIO_OR_ROUTE_STATE_BLOCKED"


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _unique_ids(items: Any, key: str, label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    if not isinstance(items, list):
        errors.append(f"{label} must be an array")
        return {}
    out: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{label}[{index}] must be an object")
            continue
        ident = item.get(key)
        if not _nonempty(ident):
            errors.append(f"{label}[{index}].{key} must be non-empty")
            continue
        if ident in out:
            errors.append(f"duplicate {label} id: {ident}")
            continue
        out[ident] = item
    return out


def validate_registry(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if data.get("schema_version") != "rafaelia.custody-chain-type-registry.v1":
        errors.append("unexpected schema_version")
    if data.get("claim_allowed") is not False:
        errors.append("registry claim_allowed must remain false")

    actors = _unique_ids(data.get("actor_classes"), "actor_class", "actor_classes", errors)
    missing_actors = sorted(REQUIRED_ACTORS - actors.keys())
    if missing_actors:
        errors.append(f"missing required actor classes: {missing_actors}")

    for actor_id, actor in actors.items():
        for field in (
            "can_authorize_scope",
            "can_execute_mutation",
            "can_satisfy_independent_review",
            "can_self_authorize_promotion",
        ):
            if not isinstance(actor.get(field), bool):
                errors.append(f"{actor_id}.{field} must be boolean")
        evidence = actor.get("evidence_required")
        if not isinstance(evidence, list) or not evidence or not all(_nonempty(x) for x in evidence):
            errors.append(f"{actor_id}.evidence_required must be a non-empty string array")

    assistant = actors.get("ASSISTANT_ORCHESTRATOR", {})
    if assistant.get("can_authorize_scope") is not False:
        errors.append("ASSISTANT_ORCHESTRATOR cannot authorize scope")
    if assistant.get("can_satisfy_independent_review") is not False:
        errors.append("ASSISTANT_ORCHESTRATOR cannot satisfy independent review")
    if assistant.get("can_self_authorize_promotion") is not False:
        errors.append("ASSISTANT_ORCHESTRATOR cannot self-authorize promotion")

    for actor_id in ("CONNECTOR_PROVIDER", "RUNTIME_EXECUTOR"):
        actor = actors.get(actor_id, {})
        if actor.get("can_authorize_scope") is not False:
            errors.append(f"{actor_id} cannot authorize scope")
        if actor.get("can_self_authorize_promotion") is not False:
            errors.append(f"{actor_id} cannot self-authorize promotion")

    profiles = _unique_ids(data.get("custody_profiles"), "profile_id", "custody_profiles", errors)
    missing_profiles = sorted(REQUIRED_PROFILES - profiles.keys())
    if missing_profiles:
        errors.append(f"missing required custody profiles: {missing_profiles}")

    for profile_id, profile in profiles.items():
        if profile.get("surface") not in ALLOWED_SURFACES:
            errors.append(f"{profile_id}.surface is invalid")
        if profile.get("missing_behavior") != MISSING_BEHAVIOR:
            errors.append(f"{profile_id}.missing_behavior must be fail-closed")
        anchors = profile.get("required_anchors")
        if not isinstance(anchors, list) or not anchors or not all(_nonempty(x) for x in anchors):
            errors.append(f"{profile_id}.required_anchors must be a non-empty string array")
        if isinstance(anchors, list) and len(anchors) != len(set(anchors)):
            errors.append(f"{profile_id}.required_anchors must be unique")
        for field in ("purpose", "authority", "evidence_rule", "claim_boundary"):
            if not _nonempty(profile.get(field)):
                errors.append(f"{profile_id}.{field} must be non-empty")

    agent = profiles.get("AGENT_ACTION_CUSTODY", {})
    anchors = set(agent.get("required_anchors", [])) if isinstance(agent.get("required_anchors"), list) else set()
    for required in ("human_authority_ref", "assistant_orchestrator_ref", "connector_provider", "provider_result_ref"):
        if required not in anchors:
            errors.append(f"AGENT_ACTION_CUSTODY missing anchor: {required}")

    credential = profiles.get("CREDENTIAL_PERMISSION_CUSTODY", {})
    credential_anchors = set(credential.get("required_anchors", [])) if isinstance(credential.get("required_anchors"), list) else set()
    for required in ("provider", "principal_or_subject_ref", "target_resource", "permission_scope", "credential_locator_or_secret_name_without_value", "observed_state", "provider_result_or_readback_ref"):
        if required not in credential_anchors:
            errors.append(f"CREDENTIAL_PERMISSION_CUSTODY missing anchor: {required}")
    boundary = credential.get("claim_boundary", "")
    if isinstance(boundary, str) and "secret value" not in boundary.lower():
        errors.append("CREDENTIAL_PERMISSION_CUSTODY must distinguish configured names from secret-value evidence")

    binding = data.get("cross_surface_binding")
    if not isinstance(binding, dict):
        errors.append("cross_surface_binding must be an object")
    else:
        if binding.get("relation_required") is not True:
            errors.append("cross_surface_binding.relation_required must be true")
        for field in ("identity_fields", "byte_equivalence_requires"):
            values = binding.get(field)
            if not isinstance(values, list) or not values or not all(_nonempty(x) for x in values):
                errors.append(f"cross_surface_binding.{field} must be a non-empty string array")
        if not _nonempty(binding.get("duplication_rule")):
            errors.append("cross_surface_binding.duplication_rule must be non-empty")

    authority = data.get("surface_authority")
    if not isinstance(authority, dict):
        errors.append("surface_authority must be an object")
    else:
        for field in ("github", "drive", "runtime", "cross_surface"):
            if not _nonempty(authority.get(field)):
                errors.append(f"surface_authority.{field} must be non-empty")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", nargs="?", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args()
    try:
        data = json.loads(args.registry.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"state": "FAIL", "errors": [str(exc)]}, indent=2))
        return 2
    if not isinstance(data, dict):
        print(json.dumps({"state": "FAIL", "errors": ["registry root must be an object"]}, indent=2))
        return 2

    errors = validate_registry(data)
    print(json.dumps({
        "state": "PASS" if not errors else "FAIL",
        "registry": str(args.registry),
        "actor_classes": len(data.get("actor_classes", [])) if isinstance(data.get("actor_classes"), list) else 0,
        "custody_profiles": len(data.get("custody_profiles", [])) if isinstance(data.get("custody_profiles"), list) else 0,
        "errors": errors,
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
