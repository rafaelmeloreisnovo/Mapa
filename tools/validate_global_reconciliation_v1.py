#!/usr/bin/env python3
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/control-plane/omega-assurance/global-reconciliation.v1.json"

EXPECTED_MAIN = "dae0865c28ac1f32c53f60ba46608bfb6de9f01c"
EXPECTED_SEED_HEAD = "4d036f0ab8472c3688d4b4bf260ea7bacba1233d"
EXPECTED_SEED_RUN = 37340489362
EXPECTED_SEED_MERGE = EXPECTED_MAIN
REQUIRED_BOUNDARIES = {
    "SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM",
    "TOKEN_VAZIO != 0",
    "MERGED != POST_MERGE_CI_PASS",
    "DEDICATED_GATE_PASS != GLOBAL_REPO_PASS",
    "VALUE_EQUALITY != REPRESENTATION_IDENTITY",
    "FORMAL_ANALOGY != PHYSICAL_EVIDENCE",
    "STORED_HISTORY != CURRENT_STATE",
}
ABSENCE_TYPES = {"NUMERIC_ZERO", "NULL", "EMPTY_SET", "TOKEN_VAZIO", "NOT_RUN", "UNDEFINED"}


def load(path: Path = MANIFEST) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("root must be object")
    return value


def _fraction(text: str) -> Fraction:
    n, d = text.split("/", 1)
    return Fraction(int(n), int(d))


def validate_manifest(m: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if m.get("schema_version") != "rafaelia.global-reconciliation/v1":
        errors.append("schema_version_mismatch")
    if m.get("gate_id") != "GLOBAL_RECONCILIATION_V1":
        errors.append("gate_id_mismatch")
    if m.get("claim_allowed") is not False:
        errors.append("claim_allowed_must_remain_false")

    authority = m.get("authority")
    if not isinstance(authority, dict) or authority.get("base_main") != EXPECTED_MAIN:
        errors.append("base_main_mismatch")

    seed = m.get("seed_gate")
    if not isinstance(seed, dict):
        errors.append("seed_gate_missing")
    else:
        if seed.get("tested_head") != EXPECTED_SEED_HEAD:
            errors.append("seed_tested_head_mismatch")
        if seed.get("dedicated_run") != EXPECTED_SEED_RUN:
            errors.append("seed_run_mismatch")
        if seed.get("dedicated_run_state") != "PASS_EXACT_HEAD":
            errors.append("seed_exact_head_pass_missing")
        if seed.get("merge_commit") != EXPECTED_SEED_MERGE or seed.get("merge_state") != "MERGED":
            errors.append("seed_merge_mismatch")
        if seed.get("post_merge_ci") == "PASS":
            errors.append("post_merge_pass_without_evidence")
        if not str(seed.get("post_merge_ci", "")).startswith("TOKEN_VAZIO"):
            errors.append("post_merge_ci_must_remain_typed_unknown")
        if seed.get("claim_allowed") is not False:
            errors.append("seed_claim_boundary_broken")

    provider = m.get("provider_gate")
    if not isinstance(provider, dict):
        errors.append("provider_gate_missing")
    else:
        if provider.get("main_protected") is False and provider.get("global_promotion") is not False:
            errors.append("unprotected_main_cannot_global_promote")
        if provider.get("required_status_enforcement") == "OFF" and provider.get("state") != "FAIL_CLOSED_PROVIDER_ENFORCEMENT":
            errors.append("provider_fail_closed_state_mismatch")

    sup = m.get("supersession_policy")
    if not isinstance(sup, dict) or sup.get("routing_rule") != "LATEST_EVIDENCED_SUCCESSOR_WINS_FOR_CURRENT_STATE":
        errors.append("supersession_routing_rule_missing")
    elif sup.get("predecessors_preserved") is not True:
        errors.append("predecessor_history_must_be_preserved")

    typed = m.get("typed_absence")
    if not isinstance(typed, list):
        errors.append("typed_absence_missing")
    else:
        by_type = {x.get("type"): x for x in typed if isinstance(x, dict)}
        if set(by_type) != ABSENCE_TYPES:
            errors.append("typed_absence_set_mismatch")
        if by_type.get("NUMERIC_ZERO", {}).get("numeric_payload") != 0:
            errors.append("numeric_zero_payload_mismatch")
        for name in ABSENCE_TYPES - {"NUMERIC_ZERO"}:
            if by_type.get(name, {}).get("numeric_payload") is not None:
                errors.append(f"{name.lower()}_must_not_have_numeric_payload")
        if by_type.get("TOKEN_VAZIO", {}).get("numeric_payload") == 0:
            errors.append("token_vazio_collapsed_to_zero")

    reps = m.get("representation_semantics")
    if not isinstance(reps, list):
        errors.append("representation_semantics_missing")
    else:
        eq = next((x for x in reps if isinstance(x, dict) and x.get("left") == "7/3"), None)
        if not eq:
            errors.append("scaled_fraction_pair_missing")
        else:
            if eq.get("right") != "77/33":
                errors.append("scaled_fraction_pair_mismatch")
            if isinstance(eq.get("right"), str):
                if _fraction(eq["left"]) != _fraction(eq["right"]):
                    errors.append("scaled_fraction_value_equality_false")
                if eq["left"] == eq["right"]:
                    errors.append("scaled_fraction_representation_not_distinct")
            if eq.get("canonical_value") != "7/3":
                errors.append("scaled_fraction_canonical_mismatch")
        expected = {"999/969": "333/323", "777/555": "7/5"}
        for left, canonical in expected.items():
            item = next((x for x in reps if isinstance(x, dict) and x.get("left") == left), None)
            if not item or item.get("canonical_value") != canonical or str(_fraction(left)) != canonical:
                errors.append(f"canonical_reduction_mismatch:{left}")

    fb = m.get("formal_boundaries")
    if not isinstance(fb, dict):
        errors.append("formal_boundaries_missing")
    else:
        fluid = fb.get("fluid_wave_energy", {})
        if fluid.get("state") != "FORMAL_ANALOGY" or fluid.get("claim_allowed") is not False:
            errors.append("fluid_analogy_boundary_broken")
        if not str(fluid.get("physical_binding", "")).startswith("TOKEN_VAZIO"):
            errors.append("fluid_physical_binding_must_be_token_vazio")
        shannon = fb.get("shannon", {})
        if shannon.get("claim") != "NO_SHANNON_VIOLATION_CLAIM":
            errors.append("shannon_boundary_missing")

    custody = m.get("local_input_custody")
    if not isinstance(custody, list) or len(custody) != 7:
        errors.append("local_input_custody_incomplete")
    else:
        for item in custody:
            digest = item.get("sha256") if isinstance(item, dict) else None
            if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
                errors.append("invalid_local_input_sha256")

    if not REQUIRED_BOUNDARIES.issubset(set(m.get("boundaries", []))):
        errors.append("required_boundaries_missing")

    return sorted(set(errors))


def run(m: dict[str, Any] | None = None) -> dict[str, Any]:
    m = m if m is not None else load()
    errors = validate_manifest(m)
    return {
        "schema_version": "rafaelia.global-reconciliation-receipt/v1",
        "gate_id": "GLOBAL_RECONCILIATION_V1",
        "status": "PASS" if not errors else "FAIL",
        "claim_allowed": False,
        "errors": errors,
        "semantics": "PASS validates reconciliation invariants only; it does not prove scientific, physical, provider or repository-global claims.",
    }


def main() -> int:
    receipt = run()
    print(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
