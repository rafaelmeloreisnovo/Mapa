#!/usr/bin/env python3
"""Dependency-free validator for RAFAELIA Empty State Ontology V1."""

from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "semantics" / "empty-state-ontology.v1.json"

EXPECTED_IDS = [
    "TOKEN_VAZIO", "VOID", "NOTHING_ABSOLUTE", "INVISIBLE", "ABSENCE",
    "SILENCE", "ZERO", "EMPTY_SET", "NULL", "UNKNOWN", "UNOBSERVED",
    "SHADOW", "LIMIT",
]
EXPECTED_DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
REQUIRED_DISTINCTIONS = {
    frozenset(("TOKEN_VAZIO", "ZERO")),
    frozenset(("TOKEN_VAZIO", "NULL")),
    frozenset(("TOKEN_VAZIO", "EMPTY_SET")),
    frozenset(("VOID", "NOTHING_ABSOLUTE")),
    frozenset(("ZERO", "EMPTY_SET")),
    frozenset(("NULL", "EMPTY_SET")),
    frozenset(("UNKNOWN", "UNOBSERVED")),
    frozenset(("UNOBSERVED", "ABSENCE")),
    frozenset(("SILENCE", "ABSENCE")),
    frozenset(("INVISIBLE", "ABSENCE")),
    frozenset(("SHADOW", "INVISIBLE")),
    frozenset(("LIMIT", "ABSENCE")),
}


class OntologyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise OntologyError(message)


def by_id(data: dict) -> dict[str, dict]:
    return {row["id"]: row for row in data["states"]}


def validate_data(data: dict) -> dict:
    require(data.get("schema") == "rafaelia.empty-state-ontology.v1", "unexpected schema")
    require(data.get("claim_allowed") is False, "registry cannot promote domain claims")

    states = data.get("states")
    require(isinstance(states, list) and len(states) == 13, "exactly 13 states required")
    ids = [row.get("id") for row in states]
    require(ids == EXPECTED_IDS, f"state order/id mismatch: {ids!r}")
    require(len(set(ids)) == 13, "state ids must be unique")

    rows = by_id(data)
    for sid, row in rows.items():
        require(bool(row.get("definition")), f"{sid}: definition missing")
        require(bool(row.get("requires_context")), f"{sid}: context requirements missing")
        require(bool(row.get("evidence_rule")), f"{sid}: evidence rule missing")
        require(isinstance(row.get("forbidden_inferences"), list) and row["forbidden_inferences"],
                f"{sid}: forbidden inference boundary missing")

    require(rows["TOKEN_VAZIO"]["promotable"] is False, "TOKEN_VAZIO cannot be promoted as a value")
    require(rows["NOTHING_ABSOLUTE"]["promotable"] is False, "NOTHING_ABSOLUTE cannot be empirically promoted")
    require("No empirical promotion" in rows["NOTHING_ABSOLUTE"]["evidence_rule"],
            "NOTHING_ABSOLUTE must remain outside empirical promotion")

    center = data.get("center_binding", {})
    require(center.get("legacy_expression") == "CENTER=TOKEN_VAZIO", "legacy center marker must be preserved")
    require(center.get("refined_semantic_type") == "VOID", "center semantic refinement must be VOID")
    require(center.get("representation_marker") == "TOKEN_VAZIO", "center representation marker must remain TOKEN_VAZIO")

    coercion = data.get("coercion_policy", {})
    require(coercion.get("mode") == "EXPLICIT_ONLY", "coercion must be explicit-only")
    require(coercion.get("default") == "DENY", "default coercion must deny")

    distinctions = data.get("hard_distinctions", [])
    actual = []
    for pair in distinctions:
        require(isinstance(pair, list) and len(pair) == 2, "distinction must be a pair")
        require(pair[0] in rows and pair[1] in rows and pair[0] != pair[1], "invalid distinction endpoints")
        actual.append(frozenset(pair))
    require(len(actual) == len(set(actual)), "duplicate hard distinction")
    require(REQUIRED_DISTINCTIONS <= set(actual), "required hard distinctions missing")

    projection = data.get("omega8_projection", [])
    require(len(projection) == 8, "Omega8 projection must contain eight directions")
    require([row.get("direction") for row in projection] == EXPECTED_DIRECTIONS,
            "Omega8 direction order mismatch")
    require(len({row.get("operator") for row in projection}) == 8,
            "Omega8 operators must remain distinct")
    require(all(bool(row.get("rule")) for row in projection), "Omega8 rule missing")

    transitions = data.get("transitions", [])
    require(transitions, "transition policy missing")
    for tr in transitions:
        require(tr.get("from") in rows and tr.get("to") in rows, "transition endpoint unknown")
        require(tr.get("allowed") in {"CONDITIONAL", "REPRESENTATION_ONLY", "DENY"},
                "invalid transition policy")
        if tr.get("allowed") == "CONDITIONAL":
            require(bool(tr.get("requires")), "conditional transition requires evidence conditions")

    deny = next((tr for tr in transitions
                 if tr.get("from") == "NOTHING_ABSOLUTE" and tr.get("to") == "ABSENCE"), None)
    require(deny is not None and deny.get("allowed") == "DENY",
            "NOTHING_ABSOLUTE -> ABSENCE must be denied")

    invisible = rows["INVISIBLE"]
    shadow = rows["SHADOW"]
    absence = rows["ABSENCE"]
    silence = rows["SILENCE"]
    unobserved = rows["UNOBSERVED"]
    limit = rows["LIMIT"]

    require("unique cause" in " ".join(invisible["forbidden_inferences"]).lower(),
            "INVISIBLE must reject unique-cause inference")
    require("unique cause" in " ".join(shadow["forbidden_inferences"]).lower(),
            "SHADOW must reject unique-cause inference")
    require("scope" in absence["requires_context"], "ABSENCE requires scope")
    require("method" in absence["requires_context"], "ABSENCE requires method")
    require("window" in silence["requires_context"], "SILENCE requires window")
    require("observation_method" in unobserved["requires_context"], "UNOBSERVED requires observation method")
    require("boundary_definition" in limit["requires_context"], "LIMIT requires a boundary definition")

    gaps = data.get("gaps", [])
    require(any(g.get("id") == "ONTO-GAP-001" and g.get("state") == "TOKEN_VAZIO" for g in gaps),
            "metaphysical-to-empirical gap must remain explicit")

    return {
        "status": "PASS",
        "schema": data["schema"],
        "states": len(states),
        "hard_distinctions": len(actual),
        "omega8_directions": len(projection),
        "transitions": len(transitions),
        "claim_allowed": data["claim_allowed"],
        "center_semantic_type": center["refined_semantic_type"],
        "center_marker": center["representation_marker"],
    }


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    print(json.dumps(validate_data(data), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
