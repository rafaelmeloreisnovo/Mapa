#!/usr/bin/env python3
"""Fail-closed validator for the sparse RAFAELIA Omega7 coordinate contract."""

from __future__ import annotations

import json
import pathlib
import sys
from typing import Any


AXES = ("direction", "vertent", "line", "condition")
TERMINAL_OUTCOMES = {"COERENTE", "PARADOXO", "ANOMALIA", "TOKEN_VAZIO"}
SURFACES = {"GITHUB", "GOOGLE_DRIVE", "SITES", "TEMPLATE", "PETS", "WEB"}


class ContractError(ValueError):
    """Raised when a contract would permit an unsupported promotion."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def require_seven_unique(labels: Any, label: str) -> None:
    require(isinstance(labels, list), f"{label} must be a list")
    require(len(labels) == 7, f"{label} must have exactly 7 labels")
    require(all(isinstance(item, str) and item for item in labels), f"{label} labels must be non-empty strings")
    require(len(set(labels)) == 7, f"{label} labels must be unique")


def validate(contract: dict[str, Any]) -> dict[str, int | str]:
    require(contract.get("schema") == "rafaelia.omega7-relational-amplifier.v1", "unsupported schema")
    require(contract.get("claim_allowed") is False, "claim_allowed must remain false")
    require(contract.get("status") in {"CANONICAL_DRAFT", "VERIFIED_LIMITED", "BLOCKED", "TOKEN_VAZIO"}, "invalid status")

    axes = contract.get("axes")
    require(isinstance(axes, dict) and set(axes) == set(AXES), "axes must be exactly direction, vertent, line, condition")
    for axis in AXES:
        require_seven_unique(axes[axis], axis)

    require_seven_unique(contract.get("semantic_top"), "semantic_top")

    coordinate_space = contract.get("coordinate_space")
    require(isinstance(coordinate_space, dict), "coordinate_space must be an object")
    require(coordinate_space.get("arity") == 7, "arity must equal 7")
    require(coordinate_space.get("dimensions") == 4, "dimensions must equal 4")
    expected = 7 ** 4
    require(coordinate_space.get("addressable_cells") == expected, "addressable_cells must equal 7^4")
    materialized = coordinate_space.get("materialized_cells")
    require(isinstance(materialized, int) and 0 <= materialized <= expected, "invalid materialized_cells")
    require(isinstance(coordinate_space.get("runtime_status"), str) and coordinate_space["runtime_status"], "runtime_status is required")
    require(isinstance(coordinate_space.get("promotion_gate"), str) and coordinate_space["promotion_gate"], "promotion_gate is required")

    policy = contract.get("relation_policy")
    require(isinstance(policy, dict), "relation_policy must be an object")
    require_seven_unique(policy.get("edge_types"), "edge_types")
    outcomes = policy.get("terminal_outcomes")
    require(isinstance(outcomes, list) and set(outcomes) == TERMINAL_OUTCOMES and len(outcomes) == 4, "terminal outcomes must be the canonical four")
    causality = policy.get("causality")
    require(isinstance(causality, dict) and causality.get("default_state") == "TOKEN_VAZIO_CAUSALITY", "causality must fail closed")
    requirements = causality.get("promotion_requirements")
    require(isinstance(requirements, list) and len(requirements) >= 1, "causal promotion requirements are required")
    sparsity = policy.get("sparsity")
    require(isinstance(sparsity, dict) and sparsity.get("semantic_edges_materialized") == 0, "semantic edges must remain unmaterialized without evidence")

    sources = contract.get("source_registry")
    require(isinstance(sources, list) and sources, "source_registry is required")
    source_ids: set[str] = set()
    for source in sources:
        require(isinstance(source, dict), "source must be an object")
        source_id = source.get("source_id")
        require(isinstance(source_id, str) and source_id.startswith("SRC-"), "invalid source_id")
        require(source_id not in source_ids, "source_id must be unique")
        source_ids.add(source_id)
        require(source.get("surface") in SURFACES, "unsupported surface")
        require(source.get("claim_allowed") is False, "sources cannot promote claims")

    gaps = contract.get("token_vazio")
    require(isinstance(gaps, list) and gaps, "token_vazio is required")
    gap_ids: set[str] = set()
    for gap in gaps:
        require(isinstance(gap, dict), "gap must be an object")
        gap_id = gap.get("gap_id")
        require(isinstance(gap_id, str) and gap_id.startswith("TV-OMEGA7-"), "invalid gap_id")
        require(gap_id not in gap_ids, "gap_id must be unique")
        gap_ids.add(gap_id)
        state = gap.get("state")
        require(isinstance(state, str) and (state.startswith("TOKEN_VAZIO_") or state.startswith("BLOCKED_")), "gap state must remain explicit")
        require(isinstance(gap.get("next_gate"), str) and gap["next_gate"], "gap next_gate is required")
        require(gap.get("claim_allowed") is False, "gaps cannot promote claims")

    r3 = contract.get("r3")
    require(isinstance(r3, dict) and set(r3) == {"f_ok", "f_gap", "f_next"}, "r3 must contain f_ok, f_gap and f_next")
    for key in ("f_ok", "f_gap", "f_next"):
        require(isinstance(r3[key], list) and r3[key], f"r3.{key} must be a non-empty list")

    return {
        "status": "PASS_LIMITED_SCHEMA_AND_CONTRACT",
        "addressable_cells": expected,
        "materialized_cells": materialized,
        "sources": len(sources),
        "gaps": len(gaps),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_omega7_relational_amplifier.py CONTRACT.json", file=sys.stderr)
        return 2
    path = pathlib.Path(argv[1])
    try:
        contract = json.loads(path.read_text(encoding="utf-8"))
        report = validate(contract)
    except (OSError, json.JSONDecodeError, ContractError) as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
