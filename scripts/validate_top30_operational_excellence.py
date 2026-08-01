#!/usr/bin/env python3
"""Validate and evaluate the RAFAELIA Top-30 operational excellence registry.

This evaluator is read-only and fail-closed. Scores rank implementation work;
they never certify compliance, truth, production readiness or scientific merit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "rafaelia.operational-excellence-top30.v1"
RECEIPT_SCHEMA = "rafaelia.operational-excellence-receipt.v1"
ALLOWED_STATES = {"EVIDENCED", "PARTIAL", "TOKEN_VAZIO", "BLOCKED_EXTERNAL", "NOT_APPLICABLE"}
ALLOWED_MODES = {"AUTOMATABLE", "HYBRID", "HUMAN_REQUIRED"}
REQUIRED_CATEGORIES = {
    "Governance", "Security", "Evidence", "Reliability", "Quality",
    "Operations", "Data", "Resilience", "Privacy", "Delivery",
    "Performance", "Efficiency", "Human Factors", "Knowledge", "Lifecycle", "Learning",
}


class RegistryError(ValueError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RegistryError("root must be an object")
    return value


def validate(registry: dict[str, Any]) -> None:
    if registry.get("schema") != SCHEMA:
        raise RegistryError("wrong schema")
    for flag in ("claim_allowed", "publication_ready", "automatic_mutation", "automatic_merge"):
        if registry.get(flag) is not False:
            raise RegistryError(f"{flag} must remain false")
    if registry.get("source_mode") != "READ_ONLY":
        raise RegistryError("source_mode must be READ_ONLY")

    state_weights = registry.get("state_weights")
    gap_weights = registry.get("priority_gap_weights")
    if not isinstance(state_weights, dict) or set(state_weights) != ALLOWED_STATES:
        raise RegistryError("state_weights must cover all allowed states")
    if not isinstance(gap_weights, dict) or set(gap_weights) != ALLOWED_STATES:
        raise RegistryError("priority_gap_weights must cover all allowed states")
    if state_weights["EVIDENCED"] != 1.0 or state_weights["TOKEN_VAZIO"] != 0.0:
        raise RegistryError("state weight boundary drift")
    if gap_weights["TOKEN_VAZIO"] != 1.0 or gap_weights["EVIDENCED"] >= gap_weights["PARTIAL"]:
        raise RegistryError("priority gap weights are incoherent")

    boundary = registry.get("scoring_boundary")
    if not isinstance(boundary, dict) or boundary.get("maximum_automatic_decision") != "READY_FOR_HUMAN_REVIEW":
        raise RegistryError("automatic decision boundary drift")

    practices = registry.get("practices")
    if not isinstance(practices, list) or len(practices) != 30:
        raise RegistryError("exactly 30 practices are required")
    ranks = [item.get("rank") for item in practices if isinstance(item, dict)]
    ids = [item.get("id") for item in practices if isinstance(item, dict)]
    if ranks != list(range(1, 31)):
        raise RegistryError("ranks must be exactly 1..30")
    if len(ids) != 30 or len(set(ids)) != 30 or any(not isinstance(value, str) or not value for value in ids):
        raise RegistryError("practice ids must be present and unique")

    values = []
    categories = set()
    for item in practices:
        if item.get("claim_allowed") is not False:
            raise RegistryError(f"{item.get('id')}: claim_allowed must be false")
        state = item.get("state")
        mode = item.get("execution_mode")
        if state not in ALLOWED_STATES:
            raise RegistryError(f"{item.get('id')}: invalid state")
        if mode not in ALLOWED_MODES:
            raise RegistryError(f"{item.get('id')}: invalid execution mode")
        value = item.get("value_score")
        live = item.get("live_potential_score")
        if not isinstance(value, int) or not 0 <= value <= 100:
            raise RegistryError(f"{item.get('id')}: invalid value_score")
        if not isinstance(live, int) or not 0 <= live <= 100:
            raise RegistryError(f"{item.get('id')}: invalid live_potential_score")
        values.append(value)
        categories.add(item.get("category"))
        for field in ("control_objective", "falsifier", "next_step"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise RegistryError(f"{item.get('id')}: {field} required")

    if values != sorted(values, reverse=True):
        raise RegistryError("value_score must be non-increasing by rank")
    if not REQUIRED_CATEGORIES.issubset(categories):
        raise RegistryError(f"category coverage incomplete: {sorted(REQUIRED_CATEGORIES - categories)}")


def evaluate(registry: dict[str, Any], generated_at: datetime) -> dict[str, Any]:
    validate(registry)
    practices = registry["practices"]
    state_weights = registry["state_weights"]
    gap_weights = registry["priority_gap_weights"]
    total_value = 0.0
    earned_value = 0.0
    applicable = 0
    state_counts = Counter()
    category_value: dict[str, dict[str, float | int]] = {}
    ranked_actions = []

    for item in practices:
        state = item["state"]
        state_counts[state] += 1
        raw_weight = state_weights[state]
        weight = None if raw_weight is None else float(raw_weight)
        value = float(item["value_score"])
        live = float(item["live_potential_score"])
        if weight is not None:
            applicable += 1
            total_value += value
            earned_value += value * weight
        bucket = category_value.setdefault(item["category"], {"total": 0.0, "earned": 0.0, "count": 0})
        if weight is not None:
            bucket["total"] = float(bucket["total"]) + value
            bucket["earned"] = float(bucket["earned"]) + value * weight
        bucket["count"] = int(bucket["count"]) + 1
        priority = value * (live / 100.0) * float(gap_weights[state])
        ranked_actions.append({
            "rank": item["rank"], "id": item["id"], "category": item["category"],
            "state": state, "execution_mode": item["execution_mode"],
            "priority_score": round(priority, 6), "next_step": item["next_step"],
            "falsifier": item["falsifier"],
        })

    ranked_actions.sort(key=lambda value: (-value["priority_score"], value["rank"], value["id"]))
    maturity = earned_value / total_value if total_value else 0.0
    category_summary = {}
    for category, values in sorted(category_value.items()):
        total = float(values["total"])
        category_summary[category] = {
            "count": int(values["count"]),
            "weighted_maturity": round(float(values["earned"]) / total, 6) if total else None,
        }

    receipt: dict[str, Any] = {
        "schema": RECEIPT_SCHEMA,
        "generated_at": generated_at.isoformat(),
        "decision": "EXECUTED_READ_ONLY",
        "claim_allowed": False,
        "publication_ready": False,
        "automatic_mutation": False,
        "automatic_merge": False,
        "registry_sha256": sha256_value(registry),
        "summary": {
            "practice_count": 30,
            "applicable_count": applicable,
            "weighted_maturity": round(maturity, 6),
            "unrealized_weighted_potential": round(1.0 - maturity, 6),
            "state_counts": dict(sorted(state_counts.items())),
            "top10_open_actions": ranked_actions[:10],
            "category_summary": category_summary,
        },
        "boundaries": {
            "score_is_not_certification": True,
            "score_is_not_truth": True,
            "score_is_not_scientific_validation": True,
            "external_settings_require_external_evidence": True,
            "human_review_required_for_promotion": True,
        },
        "token_vazio": [item["id"] for item in practices if item["state"] in {"TOKEN_VAZIO", "BLOCKED_EXTERNAL"}],
    }
    receipt["receipt_sha256"] = sha256_value(receipt)
    return receipt


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def render_summary(receipt: dict[str, Any]) -> str:
    summary = receipt["summary"]
    lines = [
        "# RAFAELIA Top-30 Operational Excellence Receipt", "",
        f"- Decision: `{receipt['decision']}`",
        f"- Practices: `{summary['practice_count']}`",
        f"- Weighted maturity: `{summary['weighted_maturity']:.6f}`",
        f"- Unrealized weighted potential: `{summary['unrealized_weighted_potential']:.6f}`",
        f"- Claim allowed: `{str(receipt['claim_allowed']).lower()}`",
        f"- Registry SHA-256: `{receipt['registry_sha256']}`",
        f"- Receipt SHA-256: `{receipt['receipt_sha256']}`", "", "## Top 10 next actions", "",
    ]
    for action in summary["top10_open_actions"]:
        lines.append(f"{action['rank']}. `{action['id']}` — `{action['state']}` — priority `{action['priority_score']:.6f}`")
        lines.append(f"   - Next: {action['next_step']}")
        lines.append(f"   - Falsifier: {action['falsifier']}")
    lines.extend(["", "## Boundary", "", "The score orders engineering work. It does not certify compliance, production readiness, truth, or scientific validity."])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=Path("data/control-plane/RAFAELIA_TOP30_OPERATIONAL_EXCELLENCE.v1.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/rafaelia-top30"))
    parser.add_argument("--timestamp")
    args = parser.parse_args()
    generated_at = datetime.fromisoformat(args.timestamp.replace("Z", "+00:00")) if args.timestamp else datetime.now(timezone.utc)
    if generated_at.tzinfo is None:
        generated_at = generated_at.replace(tzinfo=timezone.utc)
    generated_at = generated_at.astimezone(timezone.utc)
    try:
        receipt = evaluate(load_object(args.registry), generated_at)
    except (OSError, json.JSONDecodeError, RegistryError) as error:
        failure = {"schema": RECEIPT_SCHEMA, "decision": "BLOCKED_TOKEN_VAZIO", "claim_allowed": False, "publication_ready": False, "error": f"{type(error).__name__}: {error}"}
        write_json(args.output_dir / "top30_receipt.json", failure)
        print(json.dumps(failure, ensure_ascii=False, indent=2))
        return 2
    write_json(args.output_dir / "top30_receipt.json", receipt)
    write_json(args.output_dir / "top30_next_actions.json", receipt["summary"]["top10_open_actions"])
    (args.output_dir / "top30_summary.md").write_text(render_summary(receipt), encoding="utf-8")
    print(json.dumps({
        "decision": receipt["decision"],
        "weighted_maturity": receipt["summary"]["weighted_maturity"],
        "unrealized_weighted_potential": receipt["summary"]["unrealized_weighted_potential"],
        "next_action": receipt["summary"]["top10_open_actions"][0]["id"],
        "receipt_sha256": receipt["receipt_sha256"],
        "claim_allowed": receipt["claim_allowed"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
