#!/usr/bin/env python3
"""Validate CGEN Assurance Hardening 10x10 V1.

Stdlib-only fail-closed validator. It validates structure, hard invariants,
gate/lens/depth cardinality, TOKEN_VAZIO semantics, normative snapshot,
P0 preservation, anti-false-equivalence and dimensional formula transfer.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "data" / "governance" / "cgen-assurance-10x10.v1.json"

REQUIRED_POLICY_TRUE = {
    "append_only",
    "fail_closed",
    "token_vazio_first_class",
    "non_compensatory_p0",
    "promotion_requires_human_authority",
}

REQUIRED_INVARIANTS = {
    "ATTENTION != TRUTH",
    "CENSORSHIP != VALIDATION",
    "ABANDONMENT != FALSIFICATION",
    "TOKEN_VAZIO != FALSE",
    "TOKEN_VAZIO != PASS",
    "TOKEN_VAZIO != FAIL",
    "UNKNOWN_CRITICAL -> HOLD",
    "P0_CANNOT_BE_AVERAGED_AWAY",
    "STALE_NORM_CANNOT_AUTHORIZE_CURRENT_PROMOTION",
    "IRREVERSIBLE_ACTION_WITH_UNKNOWN_ROLLBACK -> BLOCK",
    "FORMULA_SIMILARITY != DOMAIN_VALIDITY",
    "DIMENSIONAL_CONSISTENCY != EMPIRICAL_VALIDATION",
    "PURE_MATH_VALIDITY != PHYSICAL_APPLICABILITY",
    "PHYSICAL_APPLICABILITY != EMPIRICAL_SUPPORT",
    "EMPIRICAL_SUPPORT != CAUSAL_EXPLANATION",
    "CAUSAL_EXPLANATION != LEGAL_OR_NORMATIVE_AUTHORITY",
}

REQUIRED_EXTERNAL_P0 = {
    "SERVER_SIDE_MAIN_BRANCH_ENFORCEMENT_UNPROVEN",
    "INDEPENDENT_PROMOTION_APPROVAL_MISSING",
}

REQUIRED_HISTORY_SEPARATORS = {
    "HISTORICALLY_CENSORED",
    "ABANDONED_PRE_CONCLUSION",
    "RETRACTED",
    "SUPERSEDED",
    "TOKEN_VAZIO_HISTORY",
}

REQUIRED_EVENT_TYPES = {
    "ANOMALY",
    "PARADOX",
    "CONTRADICTION",
    "COUNTEREXAMPLE",
    "NEGATIVE_RESULT",
    "REPLICATION_FAILURE",
    "FALSIFIED",
    "TOKEN_VAZIO",
}

REQUIRED_DRIFTS = {
    "AUTHORITY_DRIFT",
    "NORMATIVE_DRIFT",
    "PROVENANCE_DRIFT",
    "DEPENDENCY_DRIFT",
    "SECURITY_DRIFT",
    "PRIVACY_DRIFT",
    "EVIDENCE_AGING",
    "WATCHDOG_HEARTBEAT_STALE",
    "FORMULA_DOMAIN_DRIFT",
    "UNIT_SCALE_DRIFT",
}

REQUIRED_TRANSFER_FIELDS = {
    "domain",
    "codomain",
    "units",
    "scale",
    "coordinates",
    "invariants",
    "boundary_conditions",
    "transform",
    "assumptions",
    "error",
    "falsifier",
    "evidence",
}

REQUIRED_TRANSFER_DIMENSIONS = {
    "MATHEMATICAL",
    "PHYSICAL",
    "MEASUREMENT_UNIT",
    "TENSOR_ARRAY",
    "STATISTICAL",
    "SEMANTIC",
    "OPERATIONAL",
    "NORMATIVE",
}

REQUIRED_TRANSFER_STATES = {
    "PROVED_IDENTITY_SAME_DOMAIN",
    "PROVED_ISOMORPHIC_REWRITE",
    "VALID_DIMENSIONAL_TRANSFORM",
    "MODEL_TRANSFER_BOUNDED",
    "HYPOTHESIS_TRANSFER",
    "ANALOGY_ONLY",
    "INVALID_DIMENSIONAL_MISMATCH",
    "OUT_OF_SCOPE",
    "TOKEN_VAZIO_TRANSFER",
}

REQUIRED_TRANSFER_FORBIDDEN = {
    "ANALOGY_ONLY_TO_EMPIRICAL_FACT",
    "DIMENSIONAL_CONSISTENCY_TO_EMPIRICAL_VALIDATION",
    "PURE_MATH_VALIDITY_TO_PHYSICAL_APPLICABILITY",
    "PHYSICAL_APPLICABILITY_TO_CAUSAL_EXPLANATION",
    "SCIENTIFIC_MODEL_TO_NORMATIVE_AUTHORITY",
}


class ValidationError(Exception):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_https_or_http(url: str) -> None:
    parsed = urlparse(url)
    require(parsed.scheme in {"https", "http"} and bool(parsed.netloc), f"invalid source url: {url!r}")


def validate_contract(data: dict) -> list[str]:
    messages: list[str] = []

    require(data.get("schema_version") == "1.0.0", "unexpected schema_version")
    require(data.get("contract_id") == "CGEN-ASSURANCE-10X10-V1", "unexpected contract_id")

    policy = data.get("policy")
    require(isinstance(policy, dict), "policy must be object")
    for key in REQUIRED_POLICY_TRUE:
        require(policy.get(key) is True, f"policy.{key} must be true")
    require(policy.get("claim_allowed") is False, "claim_allowed must remain false")

    invariants = set(data.get("invariants") or [])
    missing_invariants = REQUIRED_INVARIANTS - invariants
    require(not missing_invariants, f"missing invariants: {sorted(missing_invariants)}")

    levels = data.get("depth_levels")
    require(isinstance(levels, list) and len(levels) == 10, "must define exactly 10 depth levels")
    require([x.get("id") for x in levels] == [f"L{i}" for i in range(10)], "depth level ids must be L0..L9")
    for level in levels:
        require(str(level.get("hard_unknown", "")).startswith("TOKEN_VAZIO_"), f"{level.get('id')} lacks typed TOKEN_VAZIO")

    lenses = data.get("correlated_lenses")
    require(isinstance(lenses, list) and len(lenses) == 10, "must define exactly 10 correlated lenses")
    require(len(set(lenses)) == 10, "correlated lenses must be unique")

    gates = data.get("gates")
    require(isinstance(gates, list) and len(gates) == 10, "must define exactly 10 gates")
    require([x.get("id") for x in gates] == [f"G{i}" for i in range(10)], "gate ids must be G0..G9")
    require(all(isinstance(x.get("blockers"), list) and x["blockers"] for x in gates), "every gate must have blockers")

    urgency = data.get("urgency")
    require(isinstance(urgency, dict), "urgency must be object")
    require(urgency.get("P0", {}).get("effect") == "HOLD", "P0 must HOLD")
    require(urgency.get("P0", {}).get("cannot_be_compensated") is True, "P0 must be non-compensatory")

    token_fields = set(data.get("token_vazio_required_fields") or [])
    for required in {"id", "blocked_gate", "missing_evidence", "owner", "f_next", "staleness_trigger", "dependencies"}:
        require(required in token_fields, f"missing TOKEN_VAZIO field: {required}")

    history = set(data.get("attention_history_states") or [])
    require(REQUIRED_HISTORY_SEPARATORS <= history, "history-state separation incomplete")

    events = set(data.get("epistemic_event_types") or [])
    require(REQUIRED_EVENT_TYPES <= events, "epistemic event types incomplete")

    transfer = data.get("formula_transfer")
    require(isinstance(transfer, dict), "formula_transfer must be object")
    require(REQUIRED_TRANSFER_FIELDS <= set(transfer.get("required_signature_fields") or []),
            "formula transfer signature incomplete")
    require(REQUIRED_TRANSFER_DIMENSIONS <= set(transfer.get("dimension_classes") or []),
            "formula transfer dimensions incomplete")
    require(REQUIRED_TRANSFER_STATES <= set(transfer.get("states") or []),
            "formula transfer states incomplete")
    require(REQUIRED_TRANSFER_FORBIDDEN <= set(transfer.get("forbidden_promotions") or []),
            "formula transfer forbidden promotions incomplete")
    require("EVIDENCE" in set(transfer.get("promotion_requires") or []),
            "formula transfer promotion must require evidence")
    require("FALSIFIER" in set(transfer.get("promotion_requires") or []),
            "formula transfer promotion must require a falsifier")

    drifts = set(data.get("monitoring_drifts") or [])
    require(REQUIRED_DRIFTS <= drifts, "monitoring drift set incomplete")

    suites = data.get("non_regression_suites")
    require(isinstance(suites, list) and len(suites) == 10 and len(set(suites)) == 10, "must define 10 unique non-regression suites")

    snapshot = data.get("normative_snapshot_extension")
    require(isinstance(snapshot, dict), "normative_snapshot_extension must be object")
    require(snapshot.get("bounded_not_universal") is True, "normative snapshot must remain bounded")
    sources = snapshot.get("sources")
    require(isinstance(sources, list) and sources, "normative source list cannot be empty")
    ids = [s.get("id") for s in sources]
    require(all(ids) and len(ids) == len(set(ids)), "normative source ids must be nonempty and unique")
    for source in sources:
        require(source.get("type"), f"source {source.get('id')} missing type")
        require(source.get("state"), f"source {source.get('id')} missing state")
        validate_https_or_http(source.get("url", ""))

    by_id = {s["id"]: s for s in sources}
    require(by_id.get("NIST-AI-RMF-1.0", {}).get("state") == "PUBLISHED_UNDER_REVISION",
            "NIST AI RMF 1.0 revision state must be explicit")
    require(by_id.get("NIST-PRIVACY-FRAMEWORK-1.0", {}).get("state") == "PUBLISHED_CURRENT_WITH_1.1_IPD_PENDING",
            "NIST Privacy Framework 1.1 pending state must be explicit")
    require(by_id.get("EU-AI-ACT-2024-1689-AMENDED-2026-1744", {}).get("state") == "PHASED_APPLICATION",
            "EU AI Act phased application must be explicit")

    external_p0 = set(data.get("external_p0_preserved") or [])
    require(REQUIRED_EXTERNAL_P0 <= external_p0, "external P0 blockers were weakened or removed")

    open_tokens = data.get("open_tokens")
    require(isinstance(open_tokens, list) and open_tokens, "open_tokens required")
    for token in open_tokens:
        require(token.get("state") == "TOKEN_VAZIO", f"open token {token.get('id')} must remain TOKEN_VAZIO")
        require(token.get("blocked_gate") in {f"G{i}" for i in range(10)}, f"open token {token.get('id')} has invalid blocked_gate")
        require(bool(token.get("f_next")), f"open token {token.get('id')} missing f_next")

    falsification = data.get("falsification_tests")
    require(isinstance(falsification, list) and len(falsification) >= 12, "at least 12 falsification tests required")
    require("FORMULA_ANALOGY_IS_PROMOTED_WITHOUT_DOMAIN_TRANSFER_EVIDENCE" in falsification,
            "formula-transfer falsifier missing")
    require("DIMENSIONAL_CONSISTENCY_IS_TREATED_AS_EMPIRICAL_VALIDATION" in falsification,
            "dimensional-consistency falsifier missing")

    messages.append("PASS: CGEN 10x10 contract structurally valid")
    messages.append("PASS: 10 depth levels × 10 correlated lenses × 10 gates")
    messages.append("PASS: TOKEN_VAZIO, P0, archive and normative-drift guards preserved")
    messages.append("PASS: dimensional formula-transfer boundary machine-enforced")
    messages.append("PASS: claim_allowed=false and external promotion blockers preserved")
    return messages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", nargs="?", default=str(DEFAULT_CONTRACT))
    args = parser.parse_args()

    path = Path(args.contract)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        for message in validate_contract(data):
            print(message)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
