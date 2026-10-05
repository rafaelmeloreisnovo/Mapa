#!/usr/bin/env python3
"""Fail-closed TOKEN_VAZIO closure-readiness gate V1.

Stdlib-only and non-mutating. The gate does not fill a TOKEN_VAZIO, execute a
provider change, approve closure, or validate a scientific claim. It checks
whether a documented gap has an explicit closure contract and reports exactly
which dimensions remain unknown.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/control-plane/omega-assurance/token-vazio-closure-readiness.v1.json"
GAPS = ROOT / "data/control-plane/omega-assurance/gap-metabolism-registry.v1.json"

URGENCY = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
FAN_OUT = {"GLOBAL": 0, "CROSS_REPO": 1, "REPO": 2, "LOCAL": 3, "TOKEN_VAZIO": 4}
BENEFIT = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "TOKEN_VAZIO": 3}
EFFORT = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "TOKEN_VAZIO": 3}


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be object")
    return value


def token_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        text = value.strip()
        return not text or text == "TOKEN_VAZIO" or text.startswith("TOKEN_VAZIO_")
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) == 0
    return False


def is_token_vazio_gap(gap: dict[str, Any]) -> bool:
    state = str(gap.get("state", ""))
    gap_class = str(gap.get("gap_class", ""))
    gid = str(gap.get("id", ""))
    return "TOKEN_VAZIO" in state or gap_class.startswith("TV-") or "TOKEN_VAZIO" in gid


def assess_profile(
    contract: dict[str, Any], profile: dict[str, Any], source_gap: dict[str, Any] | None
) -> dict[str, Any]:
    missing: list[str] = []
    errors: list[str] = []

    for field in contract.get("required_dimensions", []):
        if token_empty(profile.get(field)):
            missing.append(field)

    gid = profile.get("gap_id")
    if source_gap is None:
        errors.append("gap_id_not_found_in_source_registry")
    else:
        source_refs = set(profile.get("source_refs", []))
        provenance = set(source_gap.get("provenance", []))
        if not source_refs:
            errors.append("source_refs_required")
        elif not source_refs.issubset(provenance):
            errors.append("source_refs_not_bound_to_gap_provenance")
        if profile.get("falsifier") != source_gap.get("falsifier"):
            errors.append("falsifier_drift_from_source_registry")

    if profile.get("claim_allowed") is not False:
        errors.append("claim_allowed_must_remain_false")

    policy = profile.get("dependency_policy")
    if not isinstance(policy, dict):
        errors.append("dependency_policy_must_be_object")
    else:
        ext = policy.get("external_runtime_dependencies")
        bump = policy.get("version_bumps")
        if not isinstance(ext, bool) or not isinstance(bump, bool):
            errors.append("dependency_policy_boolean_contract_invalid")
        if (ext is True or bump is True) and token_empty(policy.get("exception_ref")):
            errors.append("dependency_or_bump_requires_exception_ref")

    state = "CONTRACT_READY_NOT_EXECUTED"
    if missing:
        state = "TOKEN_VAZIO_BLOCKED"
    if errors:
        state = "INVALID_CONTRACT"

    return {
        "gap_id": gid,
        "urgency": source_gap.get("urgency", "TOKEN_VAZIO") if source_gap else "TOKEN_VAZIO",
        "state": state,
        "missing_dimensions": sorted(missing),
        "errors": sorted(errors),
        "next_gate": profile.get("next_gate", "TOKEN_VAZIO"),
        "claim_allowed": False,
    }


def priority_key(profile: dict[str, Any], source_gap: dict[str, Any] | None) -> tuple[Any, ...]:
    urgency = source_gap.get("urgency", "P3") if source_gap else "P3"
    return (
        URGENCY.get(str(urgency), 9),
        FAN_OUT.get(str(profile.get("fan_out_class", "TOKEN_VAZIO")), 9),
        BENEFIT.get(str(profile.get("uncertainty_reduction_class", "TOKEN_VAZIO")), 9),
        BENEFIT.get(str(profile.get("information_gain_class", "TOKEN_VAZIO")), 9),
        EFFORT.get(str(profile.get("effort_class", "TOKEN_VAZIO")), 9),
        str(profile.get("gap_id", "")),
    )


def validate_contract(contract: dict[str, Any], gaps: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if contract.get("schema_version") != "rafaelia.token-vazio-closure-readiness/v1":
        errors.append("schema_version_mismatch")
    if contract.get("claim_allowed") is not False:
        errors.append("gate_claim_allowed_must_be_false")
    if contract.get("closure_is_automatic") is not False:
        errors.append("automatic_closure_forbidden")
    if contract.get("append_only_evidence_required") is not True:
        errors.append("append_only_evidence_required")
    if contract.get("priority_contract", {}).get("no_scalar_score") is not True:
        errors.append("priority_must_not_fake_scalar_precision")

    invariants = set(contract.get("invariants", []))
    required_invariants = {
        "TOKEN_VAZIO != NUMERIC_ZERO",
        "MISSING_FIELD != INFERRED_VALUE",
        "SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM",
        "CI_PASS != SCIENTIFIC_VALIDATION",
        "P0_BLOCKER_IS_NON_COMPENSATORY",
        "DEPENDENCY_OR_VERSION_BUMP_REQUIRES_EXPLICIT_NECESSITY_EVIDENCE",
    }
    if not required_invariants.issubset(invariants):
        errors.append("required_invariants_missing")

    defaults = contract.get("dependency_default", {})
    if defaults.get("external_runtime_dependencies") is not False:
        errors.append("external_dependencies_must_default_false")
    if defaults.get("version_bumps") is not False:
        errors.append("version_bumps_must_default_false")

    gap_by_id = {
        g.get("id"): g for g in gaps.get("gaps", []) if isinstance(g, dict) and isinstance(g.get("id"), str)
    }
    seen: set[str] = set()
    for profile in contract.get("profiles", []):
        if not isinstance(profile, dict):
            errors.append("profile_must_be_object")
            continue
        gid = profile.get("gap_id")
        if not isinstance(gid, str) or gid in seen:
            errors.append("profile_gap_id_missing_or_duplicate")
            continue
        seen.add(gid)
        assessment = assess_profile(contract, profile, gap_by_id.get(gid))
        errors.extend(f"{gid}:{err}" for err in assessment["errors"])
    return sorted(set(errors))


def run(contract: dict[str, Any] | None = None, gaps: dict[str, Any] | None = None) -> dict[str, Any]:
    contract = contract if contract is not None else load(CONTRACT)
    gaps = gaps if gaps is not None else load(GAPS)
    structural_errors = validate_contract(contract, gaps)
    gap_by_id = {
        g.get("id"): g for g in gaps.get("gaps", []) if isinstance(g, dict) and isinstance(g.get("id"), str)
    }
    profiles = [p for p in contract.get("profiles", []) if isinstance(p, dict)]
    assessments = [
        assess_profile(contract, profile, gap_by_id.get(profile.get("gap_id"))) for profile in profiles
    ]

    ranked = sorted(profiles, key=lambda p: priority_key(p, gap_by_id.get(p.get("gap_id"))))
    selected = ranked[0] if ranked else None
    selected_assessment = None
    if selected is not None:
        selected_assessment = assess_profile(contract, selected, gap_by_id.get(selected.get("gap_id")))

    profiled = {p.get("gap_id") for p in profiles}
    token_candidates = [
        g for g in gaps.get("gaps", []) if isinstance(g, dict) and is_token_vazio_gap(g)
    ]
    unprofiled = sorted(
        str(g.get("id")) for g in token_candidates if g.get("id") not in profiled
    )

    return {
        "schema_version": "rafaelia.token-vazio-closure-readiness-receipt/v1",
        "status": "PASS" if not structural_errors else "FAIL",
        "gate_semantics": "PASS means the readiness mechanism is structurally valid; it does not mean any gap is closed.",
        "claim_allowed": False,
        "closure_is_automatic": False,
        "profile_count": len(profiles),
        "token_vazio_candidate_count": len(token_candidates),
        "unprofiled_token_vazio_count": len(unprofiled),
        "unprofiled_token_vazio": unprofiled,
        "assessments": assessments,
        "selected_next": selected_assessment,
        "structural_errors": structural_errors,
    }


def main() -> int:
    receipt = run()
    print(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
