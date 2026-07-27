#!/usr/bin/env python3
"""Validate and rank defensive strategies for Sementeira.

This module intentionally stores defensive intent, controls, detection and mitigation.
It does not operationalize high-risk behavior or transferable harmful capability.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HEX64 = re.compile(r"^[0-9a-f]{64}$")

ALLOWED_TIERS = {
    "K0_PUBLIC_CONCEPT",
    "K1_DETECTION_MITIGATION",
    "K2_SAFE_SIMULATION",
    "K3_RESTRICTED_AUTHORIZED_LAB",
    "K4_PROHIBITED_HIGH_RISK_DETAIL",
}
ALLOWED_STATES = {
    "P0_MANDATORY_GUARDRAIL",
    "P1_DEFENSIVE_PILOT",
    "P2_OBSERVE_AND_RESEARCH",
    "P3_QUARANTINE",
    "P4_PROHIBITED",
}
ALLOWED_ORIGINS = {
    "OBSERVED",
    "LATENT",
    "LATERAL",
    "FORGOTTEN",
    "DISREGARDED",
    "OBVIOUS_MISSED",
    "MODEL_INHIBITION_CANDIDATE",
}
FORBIDDEN_OUTPUTS_REQUIRED = {
    "CAT-HR-01",
    "CAT-HR-02",
    "CAT-HR-03",
    "CAT-HR-04",
    "CAT-HR-05",
    "CAT-HR-06",
}

@dataclass(frozen=True)
class RankedStrategy:
    strategy_id: str
    state: str
    priority_key: tuple[int, ...]
    reasons: tuple[str, ...]


def _score(value: Any, name: str, errors: list[str]) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 5:
        errors.append(f"{name} must be an integer between 0 and 5")
        return 0
    return value


def validate_strategy(item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "strategy_id", "title", "origin_vectors", "security_posture",
        "knowledge_tier", "adoption_risk", "omission_risk", "defensive_value",
        "evidence_strength", "observability", "reversibility", "dignity_risk",
        "abuse_transferability", "authorization_required", "human_oversight_required",
        "allowed_outputs", "forbidden_outputs", "controls", "normative_conflicts",
        "falsifier", "next_gate", "claim_allowed",
    }
    missing = sorted(required - item.keys())
    if missing:
        return [f"missing required fields: {', '.join(missing)}"]

    if not isinstance(item["strategy_id"], str) or not item["strategy_id"].strip():
        errors.append("strategy_id must be a non-empty string")
    if not isinstance(item["title"], str) or not item["title"].strip():
        errors.append("title must be a non-empty string")

    origins = item["origin_vectors"]
    if not isinstance(origins, list) or not origins:
        errors.append("origin_vectors must be a non-empty array")
    elif any(origin not in ALLOWED_ORIGINS for origin in origins):
        errors.append("origin_vectors contains a non-canonical value")

    if item["security_posture"] != "WHITE_HAT_DEFENSIVE":
        errors.append("security_posture must remain WHITE_HAT_DEFENSIVE")
    if item["knowledge_tier"] not in ALLOWED_TIERS:
        errors.append("knowledge_tier is invalid")

    for field in (
        "adoption_risk", "omission_risk", "defensive_value", "evidence_strength",
        "observability", "reversibility", "dignity_risk", "abuse_transferability",
    ):
        _score(item[field], field, errors)

    if item["authorization_required"] is not True:
        errors.append("authorization_required must be true")
    if item["human_oversight_required"] is not True:
        errors.append("human_oversight_required must be true")
    if item["claim_allowed"] is not False:
        errors.append("claim_allowed must remain false")

    for field in ("allowed_outputs", "forbidden_outputs", "controls", "normative_conflicts"):
        if not isinstance(item[field], list):
            errors.append(f"{field} must be an array")
    forbidden = set(item["forbidden_outputs"]) if isinstance(item["forbidden_outputs"], list) else set()
    absent = sorted(FORBIDDEN_OUTPUTS_REQUIRED - forbidden)
    if absent:
        errors.append(f"forbidden_outputs missing: {', '.join(absent)}")

    if item["knowledge_tier"] == "K4_PROHIBITED_HIGH_RISK_DETAIL":
        if item.get("high_risk_detail_present") is True:
            errors.append("K4 entries must not preserve high-risk operational detail")

    if not isinstance(item["falsifier"], str) or not item["falsifier"].strip():
        errors.append("falsifier must be a non-empty string")
    if not isinstance(item["next_gate"], str) or not item["next_gate"].strip():
        errors.append("next_gate must be a non-empty string")
    return errors


def classify(item: dict[str, Any]) -> RankedStrategy:
    errors = validate_strategy(item)
    if errors:
        return RankedStrategy(item.get("strategy_id", "INVALID"), "P4_PROHIBITED", (4,), tuple(errors))

    tier = item["knowledge_tier"]
    dignity = item["dignity_risk"]
    abuse = item["abuse_transferability"]
    adoption = item["adoption_risk"]
    omission = item["omission_risk"]
    value = item["defensive_value"]
    evidence = item["evidence_strength"]
    observability = item["observability"]
    reversibility = item["reversibility"]

    if tier == "K4_PROHIBITED_HIGH_RISK_DETAIL" or dignity >= 5:
        state = "P4_PROHIBITED"
        reasons = ("high-risk transfer or dignity hard gate",)
    elif tier == "K3_RESTRICTED_AUTHORIZED_LAB" or abuse >= 4 or dignity >= 4:
        state = "P3_QUARANTINE"
        reasons = ("restricted laboratory or high abuse/dignity risk",)
    elif omission >= 4 and value >= 4 and adoption <= 2 and dignity <= 2:
        state = "P0_MANDATORY_GUARDRAIL"
        reasons = ("high omission risk with strong defensive value and acceptable adoption risk",)
    elif value >= 3 and evidence >= 2 and reversibility >= 2:
        state = "P1_DEFENSIVE_PILOT"
        reasons = ("defensive value supported enough for a reversible pilot",)
    else:
        state = "P2_OBSERVE_AND_RESEARCH"
        reasons = ("insufficient evidence or readiness; preserve as research",)

    state_order = {
        "P0_MANDATORY_GUARDRAIL": 0,
        "P1_DEFENSIVE_PILOT": 1,
        "P2_OBSERVE_AND_RESEARCH": 2,
        "P3_QUARANTINE": 3,
        "P4_PROHIBITED": 4,
    }
    # Lexicographic ordering avoids pretending that uncalibrated weights are scientific.
    priority_key = (
        state_order[state],
        -omission,
        -value,
        -evidence,
        -observability,
        -reversibility,
        adoption,
        dignity,
        abuse,
    )
    return RankedStrategy(item["strategy_id"], state, priority_key, reasons)


def evaluate_registry(payload: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if payload.get("schema") != "sementeira.defensive-strategy-registry/v1":
        errors.append("invalid registry schema")
    if payload.get("claim_allowed") is not False:
        errors.append("registry claim_allowed must remain false")
    strategies = payload.get("strategies")
    if not isinstance(strategies, list):
        return {"status": "FAIL", "errors": errors + ["strategies must be an array"]}

    ranked = [classify(item) for item in strategies if isinstance(item, dict)]
    ranked.sort(key=lambda item: item.priority_key)
    invalid = [r for r in ranked if r.strategy_id == "INVALID" or (r.state == "P4_PROHIBITED" and len(r.reasons) > 1)]
    counts: dict[str, int] = {state: 0 for state in ALLOWED_STATES}
    for result in ranked:
        counts[result.state] += 1

    return {
        "status": "FAIL" if errors or invalid else "PASS",
        "errors": errors + [reason for item in invalid for reason in item.reasons],
        "ranking": [
            {"strategy_id": r.strategy_id, "state": r.state, "reasons": list(r.reasons)}
            for r in ranked
        ],
        "state_counts": counts,
        "claim_allowed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.registry.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2
    result = evaluate_registry(payload)
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
