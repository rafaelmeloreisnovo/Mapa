#!/usr/bin/env python3
"""Fail-closed structural gate for RAFAELIA authority pyramid V1.

This validator proves schema/contract structure only. It does not prove legal compliance,
security effectiveness, physical runtime, cultural meaning, or producer execution.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

EXPECTED_SCHEMA = "rafaelia.authority-pyramid-fail-closed.v1"
REQUIRED_LAYERS = {
    "L0_OBSERVABLE_REALITY",
    "L1_PROTECTED_SUBJECT_CONTEXT",
    "L2_BINDING_EXTERNAL_AUTHORITY",
    "L3_TECHNICAL_NORMATIVE_REFERENCE",
    "L4_FEDERATED_GOVERNANCE",
    "L5_PRODUCER_AUTHORITY",
    "L6_EXECUTION_EVIDENCE",
    "L7_CLAIM_PROMOTION",
}
REQUIRED_EVIDENCE_STATES = {
    "TOKEN_VAZIO",
    "OBSERVED",
    "PARTIAL",
    "EVIDENCED_SCOPED",
    "FAILURE",
    "BUG_CONFIRMED",
    "REGRESSION",
    "SECURITY_WEAKNESS",
    "VULNERABILITY_SUSPECTED",
    "VULNERABILITY_CONFIRMED",
    "PRIVACY_RISK",
    "COMPLIANCE_GAP",
    "GOVERNANCE_GAP",
    "DEBUG_BLOCKER",
    "NEAR_MISS",
    "INCIDENT",
    "SUPERSEDED",
    "NOT_APPLICABLE_WITH_EVIDENCE",
}
REQUIRED_ATTENTION_STATES = {
    "ACTIVE",
    "URGENT",
    "IGNORED_DISCOVERED",
    "FORGOTTEN_REDISCOVERED",
    "UNDERPRIORITIZED",
    "DEFERRED_WITH_OWNER",
    "ABORTED_WITH_REASON",
    "BLOCKED_EXTERNAL",
}
REQUIRED_NON_COMPENSATORY = {"governance", "privacy", "security", "protected_subject"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_contract(doc: dict) -> list[str]:
    errors: list[str] = []

    if doc.get("schema") != EXPECTED_SCHEMA:
        fail(errors, f"schema must be {EXPECTED_SCHEMA}")
    if doc.get("claim_allowed") is not False:
        fail(errors, "claim_allowed must be false for the policy artifact")
    if doc.get("automatic_merge") is not False:
        fail(errors, "automatic_merge must be false")

    layers = doc.get("authority_layers")
    if not isinstance(layers, list):
        fail(errors, "authority_layers must be a list")
        layers = []
    observed_layers = {x.get("level") for x in layers if isinstance(x, dict)}
    missing_layers = sorted(REQUIRED_LAYERS - observed_layers)
    if missing_layers:
        fail(errors, f"missing authority layers: {missing_layers}")
    for idx, layer in enumerate(layers):
        if not isinstance(layer, dict):
            fail(errors, f"authority_layers[{idx}] must be object")
            continue
        for key in ("level", "authority", "requires", "rule"):
            if key not in layer:
                fail(errors, f"authority layer {idx} missing {key}")

    evidence_states = set(doc.get("evidence_states", []))
    if not REQUIRED_EVIDENCE_STATES.issubset(evidence_states):
        fail(errors, f"evidence_states missing: {sorted(REQUIRED_EVIDENCE_STATES - evidence_states)}")

    attention_states = set(doc.get("attention_states", []))
    if not REQUIRED_ATTENTION_STATES.issubset(attention_states):
        fail(errors, f"attention_states missing: {sorted(REQUIRED_ATTENTION_STATES - attention_states)}")

    non_comp = set(doc.get("non_compensatory_dimensions", []))
    if not REQUIRED_NON_COMPENSATORY.issubset(non_comp):
        fail(errors, f"non_compensatory_dimensions missing: {sorted(REQUIRED_NON_COMPENSATORY - non_comp)}")

    invariants = set(doc.get("core_invariants", []))
    for required in (
        "TOKEN_VAZIO != 0 != false != PASS",
        "group_label != cultural_meaning",
        "child_status_unknown != adult",
        "cultural_reference_missing -> TOKEN_VAZIO_CONTEXT",
        "standard_reference != certification",
    ):
        if required not in invariants:
            fail(errors, f"missing invariant: {required}")

    p0 = doc.get("p0_triggers")
    if not isinstance(p0, list) or not p0:
        fail(errors, "p0_triggers must be non-empty")

    protected = doc.get("protected_subject_gate")
    if not isinstance(protected, dict):
        fail(errors, "protected_subject_gate must be object")
    else:
        if protected.get("default") != "TOKEN_VAZIO_NOT_ESTABLISHED":
            fail(errors, "protected-subject default must be TOKEN_VAZIO_NOT_ESTABLISHED")
        if protected.get("promotion_rule") != "missing_required_field -> HOLD":
            fail(errors, "protected-subject promotion must fail closed")
        no_inference = set(protected.get("no_inference_fields", []))
        required_no_inference = {"age", "ethnicity", "culture", "religion", "guardian_status", "vulnerability"}
        if not required_no_inference.issubset(no_inference):
            fail(errors, "protected-subject no-inference fields incomplete")
        required_fields = set(protected.get("required_if_established_or_potential", []))
        for key in ("purpose", "data_flow", "retention", "minimization", "authority_or_legal_basis", "best_interest_review", "receipt"):
            if key not in required_fields:
                fail(errors, f"protected-subject required field missing: {key}")

    producer_adapters = doc.get("producer_adapters")
    if not isinstance(producer_adapters, list) or not producer_adapters:
        fail(errors, "producer_adapters must be non-empty list")
    else:
        seen_repos: set[str] = set()
        for idx, adapter in enumerate(producer_adapters):
            if not isinstance(adapter, dict):
                fail(errors, f"producer_adapters[{idx}] must be object")
                continue
            for key in ("repo", "role", "base_authority_sha", "adapter_pr", "adapter_head_sha", "adapter_path", "state", "claim_allowed"):
                if key not in adapter:
                    fail(errors, f"producer adapter {idx} missing {key}")
            repo = adapter.get("repo")
            if repo in seen_repos:
                fail(errors, f"duplicate producer adapter: {repo}")
            if isinstance(repo, str):
                seen_repos.add(repo)
            if adapter.get("claim_allowed") is not False:
                fail(errors, f"producer adapter {repo} must keep claim_allowed=false")
            for hash_key in ("base_authority_sha", "adapter_head_sha"):
                value = adapter.get(hash_key)
                if not isinstance(value, str) or len(value) != 40:
                    fail(errors, f"producer adapter {repo} invalid {hash_key}")

    assurance = doc.get("assurance")
    if not isinstance(assurance, dict):
        fail(errors, "assurance must be object")
    else:
        if assurance.get("required_behavior") != "fail_closed":
            fail(errors, "assurance required_behavior must be fail_closed")
        if assurance.get("unknown_is_pass") is not False:
            fail(errors, "unknown_is_pass must be false")

    promotion_rule = doc.get("promotion_rule", "")
    if "HOLD" not in promotion_rule or "TOKEN_VAZIO" not in promotion_rule:
        fail(errors, "promotion_rule must explicitly hold unresolved TOKEN_VAZIO")

    if not doc.get("falsifier"):
        fail(errors, "falsifier is required")

    return errors


def self_test(base: dict) -> list[str]:
    failures: list[str] = []

    positive_errors = validate_contract(base)
    if positive_errors:
        failures.append(f"positive fixture rejected: {positive_errors}")

    fixtures: list[tuple[str, dict]] = []

    unknown_as_pass = copy.deepcopy(base)
    unknown_as_pass["assurance"]["unknown_is_pass"] = True
    fixtures.append(("unknown_must_not_pass", unknown_as_pass))

    missing_protected_gate = copy.deepcopy(base)
    missing_protected_gate["protected_subject_gate"]["required_if_established_or_potential"].remove("best_interest_review")
    fixtures.append(("protected_subject_missing_best_interest", missing_protected_gate))

    inferred_culture = copy.deepcopy(base)
    inferred_culture["protected_subject_gate"]["no_inference_fields"].remove("culture")
    fixtures.append(("culture_must_not_be_inferred", inferred_culture))

    promotion_leak = copy.deepcopy(base)
    promotion_leak["producer_adapters"][0]["claim_allowed"] = True
    fixtures.append(("producer_claim_must_remain_closed", promotion_leak))

    for name, fixture in fixtures:
        errs = validate_contract(fixture)
        if not errs:
            failures.append(f"negative fixture unexpectedly passed: {name}")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="data/control-plane/RAFAELIA_AUTHORITY_PYRAMID_FAIL_CLOSED_V1.json",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    path = Path(args.path)
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # fail closed on missing/invalid input
        print(f"FAIL: cannot load {path}: {exc}")
        return 1

    errors = validate_contract(doc)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"authority-pyramid: failures={len(errors)}")
        return 1

    if args.self_test:
        test_failures = self_test(doc)
        if test_failures:
            for error in test_failures:
                print(f"FAIL SELF-TEST: {error}")
            print(f"authority-pyramid-self-test: failures={len(test_failures)}")
            return 1
        print("authority-pyramid-self-test: negative-fixtures=4 failures=0")

    print(
        "authority-pyramid: PASS "
        f"layers={len(doc['authority_layers'])} "
        f"producers={len(doc['producer_adapters'])} "
        "claim_allowed=false unknown_is_pass=false"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
