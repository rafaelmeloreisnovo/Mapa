#!/usr/bin/env python3
"""Fail-closed validator for Serpent-Dove conduct and gap metabolism V1.

This validates structural/governance contracts only. It does not prove producer
runtime, private-corpus exhaustiveness, scientific claims, compliance, or
repository promotion authorization.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONDUCT = ROOT / "data/control-plane/omega-assurance/serpent-dove-conduct.v1.json"
GAPS = ROOT / "data/control-plane/omega-assurance/gap-metabolism-registry.v1.json"
FIXTURES = ROOT / "data/fixtures/omega-assurance/serpent-dove-negative-cases.v1.json"
SCHEMA = ROOT / "schemas/omega-assurance/serpent-dove-transition.v1.schema.json"

EXPECTED_RULES = {f"SP{i:02d}" for i in range(1, 15)}
EXPECTED_OPERATORS = {
    "DIRECT", "INVERSE", "REVERSIVE", "DERIVATIVE", "ANTIDERIVATIVE",
    "ORTHOGONAL", "TRANSVERSE", "SCALE",
}
EXPECTED_SCANS = {
    "FORGOTTEN_TOKEN_SCAN", "ABANDONED_HYPOTHESIS_SCAN",
    "UNRESOLVED_ANOMALY_SCAN", "STALE_TOKEN_VAZIO_SCAN",
    "UNTESTED_ASSUMPTION_SCAN", "UNOWNED_RISK_SCAN",
    "NORMALIZATION_OF_DEVIANCE_WATCH",
}
VALID_URGENCY = {"P0", "P1", "P2", "P3"}
PRIVATE_LOCATORS = (
    "drive.google.com/", "docs.google.com/document/d/",
    "docs.google.com/spreadsheets/d/", "docs.google.com/presentation/d/",
)


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be object")
    return value


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def policy_decision(case: dict[str, Any]) -> tuple[str, str | None]:
    signal = case.get("signal")
    conclusion = case.get("proposed_conclusion")
    action = case.get("action")
    authority = case.get("authority")
    certainty = case.get("certainty")
    reversibility = case.get("reversibility")
    age = case.get("evidence_age")
    source_role = case.get("source_role")

    if signal == "SEARCH_MISS" and conclusion == "ABSENT":
        return "REJECT", "search miss cannot prove absence"
    if signal == "PROVIDER_NOT_FOUND" and conclusion == "DELETED":
        return "REJECT", "provider miss cannot prove deletion"
    if action == "ACT_BOUNDED" and certainty in {"AMBIGUOUS", "TOKEN_VAZIO"}:
        return "REJECT", "ambiguous evidence cannot trigger ACT_BOUNDED"
    if action == "ACT_BOUNDED" and authority in {"DENY", "HOLD", "TOKEN_VAZIO"}:
        return "REJECT", "unknown authority cannot trigger ACT_BOUNDED"
    if action == "ACT_BOUNDED" and reversibility in {"FAILED", "TOKEN_VAZIO"}:
        return "REJECT", "unknown or failed reversibility cannot trigger ACT_BOUNDED"
    if conclusion == "CURRENT_PASS" and age in {"STALE", "HISTORICAL_ONLY", "INVALIDATED"}:
        return "REJECT", "historical or stale evidence cannot promote current PASS"
    if signal == "SKIPPED" and conclusion == "EXECUTED":
        return "REJECT", "skipped is not executed"
    if source_role == "PARABLE" and conclusion == "ENGINEERING_PROOF":
        return "REJECT", "parable is not engineering evidence"
    if signal == "FAST_SEMANTIC_CROSSCHECK" and conclusion == "EXACT_PIPELINE_PASS":
        return "REJECT", "fast crosscheck is not exact pipeline execution"
    if signal in {"PR_MERGED", "CI_SUCCESS"} and conclusion == "SCIENTIFIC_CONFIRMATION":
        return "REJECT", "merge or CI cannot manufacture scientific confirmation"
    if signal == "MITIGATION_SUCCESS" and conclusion == "ROOT_CAUSE_RESOLVED":
        return "REJECT", "mitigation is not root cause"
    if signal == "PRIVATE_LOCATOR_TOKEN" and conclusion == "PUBLIC_PAYLOAD":
        return "REJECT", "private locator cannot enter public payload"
    return "ALLOW", None


def validate_schema(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    add(errors, schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    add(errors, schema.get("additionalProperties") is False, "schema must close additionalProperties")
    required = set(schema.get("required", []))
    add(errors, {"operator", "minimum_intervention", "rollback", "claim_allowed"}.issubset(required), "schema required conduct fields incomplete")
    op = schema.get("properties", {}).get("operator", {})
    op_required = set(op.get("required", []))
    expected = {"intent", "authority_state", "certainty", "blast_radius", "reversibility", "information_exposure", "escalation_path"}
    add(errors, expected == op_required, "operator audit field set mismatch")
    add(errors, bool(schema.get("allOf")), "schema must encode fail-closed conditionals")
    return errors


def validate_conduct(conduct: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    add(errors, conduct.get("schema_version") == "rafaelia.serpent-dove-conduct/v1", "conduct schema_version mismatch")
    add(errors, conduct.get("claim_allowed") is False, "conduct claim_allowed must remain false")
    add(errors, conduct.get("append_only") is True, "conduct must be append-only")
    metaphor = conduct.get("source_metaphor", {})
    add(errors, metaphor.get("epistemic_type") == "PARABLE", "Matthew source must remain PARABLE")
    add(errors, metaphor.get("engineering_evidence_weight") == 0, "parable must have zero engineering evidence weight")
    heuristic = conduct.get("architectural_heuristic", {})
    add(errors, heuristic.get("status") == "ARCHITECTURAL_HEURISTIC_NOT_VALIDATED_METRIC", "Omega_SP must remain heuristic")
    add(errors, {r.get("id") for r in conduct.get("rules", []) if isinstance(r, dict)} == EXPECTED_RULES, "SP01..SP14 rule set mismatch")
    add(errors, conduct.get("quiet_watchdog", {}).get("meta_watch_depth") == 2, "meta watchdog depth must be 2")
    add(errors, {x.get("id") for x in conduct.get("gap_operators", []) if isinstance(x, dict)} == EXPECTED_OPERATORS, "gap operator set mismatch")
    scans = set(conduct.get("attention_metabolism", {}).get("scans", []))
    add(errors, EXPECTED_SCANS.issubset(scans), "attention metabolism scan set incomplete")
    add(errors, conduct.get("urgency_contract", {}).get("no_scalar_compensation") is True, "urgency must not compensate P0")
    tests = set(conduct.get("test_families", []))
    add(errors, "TEST_DO_NOT_OVERREACT" in tests, "TEST_DO_NOT_OVERREACT missing")
    add(errors, "TEST_SKIPPED_IS_NOT_EXECUTED" in tests, "skipped!=executed test missing")
    add(errors, "TEST_PARABLE_IS_NOT_ENGINEERING_EVIDENCE" in tests, "parable boundary test missing")
    return errors


def validate_gaps(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    add(errors, registry.get("schema_version") == "rafaelia.gap-metabolism-registry/v1", "gap registry schema_version mismatch")
    add(errors, registry.get("claim_allowed") is False, "gap registry claim_allowed must remain false")
    add(errors, registry.get("append_only") is True, "gap registry must be append-only")
    add(errors, registry.get("scope_exhaustiveness_claim") is False, "gap registry cannot claim exhaustiveness")
    add(errors, set(registry.get("operator_contract", [])) == EXPECTED_OPERATORS, "registry operator contract mismatch")

    public_text = json.dumps(registry, ensure_ascii=False)
    for locator in PRIVATE_LOCATORS:
        add(errors, locator not in public_text, f"private locator leaked into public registry: {locator}")

    source_ids = {s.get("id") for s in registry.get("source_surfaces", []) if isinstance(s, dict)}
    gap_ids: set[str] = set()
    p0_count = 0
    for index, gap in enumerate(registry.get("gaps", []), 1):
        label = f"gap[{index}]"
        if not isinstance(gap, dict):
            errors.append(f"{label} must be object")
            continue
        gid = gap.get("id")
        add(errors, isinstance(gid, str) and gid not in gap_ids, f"{label} duplicate/missing id")
        if isinstance(gid, str):
            gap_ids.add(gid)
        urgency = gap.get("urgency")
        add(errors, urgency in VALID_URGENCY, f"{gid}: invalid urgency")
        if urgency == "P0":
            p0_count += 1
            add(errors, gap.get("action_mode") == "HOLD", f"{gid}: P0 must HOLD")
        add(errors, bool(gap.get("provenance")), f"{gid}: provenance required")
        unknown_sources = set(gap.get("provenance", [])) - source_ids
        add(errors, not unknown_sources, f"{gid}: unknown provenance refs {sorted(unknown_sources)}")
        add(errors, isinstance(gap.get("falsifier"), str) and bool(gap.get("falsifier")), f"{gid}: falsifier required")
        add(errors, isinstance(gap.get("next_gate"), str) and bool(gap.get("next_gate")), f"{gid}: next_gate required")
        operators = gap.get("operators", {})
        add(errors, isinstance(operators, dict) and set(operators) == EXPECTED_OPERATORS, f"{gid}: all 8 operators required")
        if isinstance(operators, dict):
            for op, text in operators.items():
                add(errors, isinstance(text, str) and bool(text.strip()), f"{gid}: empty operator {op}")
        if gap.get("evidence_age") in {"STALE", "HISTORICAL_ONLY", "INVALIDATED"}:
            add(errors, not str(gap.get("state", "")).startswith("CLOSED_CURRENT"), f"{gid}: stale evidence cannot close current state")
    add(errors, p0_count >= 2, "expected non-compensatory P0 blockers missing")

    learning_ids: set[str] = set()
    for learning in registry.get("closed_learnings", []):
        lid = learning.get("id") if isinstance(learning, dict) else None
        add(errors, isinstance(lid, str) and lid not in learning_ids, "duplicate/missing learning id")
        if isinstance(lid, str):
            learning_ids.add(lid)
        add(errors, bool(learning.get("provenance")) if isinstance(learning, dict) else False, f"{lid}: learning provenance required")
        add(errors, bool(learning.get("boundary")) if isinstance(learning, dict) else False, f"{lid}: learning boundary required")
    return errors


def validate_fixtures(fixtures: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    rejected = 0
    allowed = 0
    for case in fixtures.get("cases", []):
        cid = case.get("id")
        add(errors, isinstance(cid, str) and cid not in seen, "fixture duplicate/missing id")
        if isinstance(cid, str):
            seen.add(cid)
        decision, reason = policy_decision(case)
        expected = case.get("expected")
        add(errors, decision == expected, f"fixture {cid}: expected {expected}, got {decision} ({reason})")
        if expected == "REJECT":
            rejected += 1
            add(errors, reason == case.get("expected_reason"), f"fixture {cid}: rejection reason mismatch")
        elif expected == "ALLOW":
            allowed += 1
    add(errors, rejected >= 10, "negative intervention coverage too small")
    add(errors, allowed >= 2, "positive bounded-behavior coverage too small")
    return errors


def run() -> dict[str, Any]:
    schema = load(SCHEMA)
    conduct = load(CONDUCT)
    gaps = load(GAPS)
    fixtures = load(FIXTURES)
    errors = validate_schema(schema) + validate_conduct(conduct) + validate_gaps(gaps) + validate_fixtures(fixtures)
    return {
        "schema_version": "rafaelia.serpent-dove-gap-metabolism-validator-receipt/v1",
        "status": "PASS" if not errors else "FAIL",
        "claim_allowed": False,
        "gap_count": len(gaps.get("gaps", [])),
        "learning_count": len(gaps.get("closed_learnings", [])),
        "fixture_count": len(fixtures.get("cases", [])),
        "errors": errors,
    }


def main() -> int:
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
