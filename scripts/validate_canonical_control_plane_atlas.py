#!/usr/bin/env python3
"""Validate RAFAELIA canonical control-plane invariants without external deps."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXPECTED_SCHEMA = "rafaelia.canonical_control_plane_atlas.v1"
EXPECTED_TRANSVERSAL = {
    "PROVENANCE",
    "CUSTODY_CHAIN",
    "RECEIPTS",
    "CONTRACTS",
    "URGENCIES_GATES",
    "CLAIMS",
    "RISKS",
    "ATLAS_ROUTES",
    "VALIDATIONS",
    "SUPERSESSION",
    "CLOSURE_LEDGER",
}
EXPECTED_DIMENSIONS = {
    "identity",
    "authority",
    "source",
    "provenance",
    "custody",
    "epistemic_state",
    "evidence",
    "relations",
    "contracts",
    "risk",
    "urgency",
    "TOKEN_VAZIO",
    "falsifier",
    "rollback",
    "receipt",
    "ATLAS_routes",
    "closure",
}
EXPECTED_CONTRACTS = {
    "C-EVIDENCE-001",
    "C-TOKEN-001",
    "C-SEARCH-001",
    "C-RUNTIME-001",
    "C-REGRESSION-001",
}
EXPECTED_ATLAS_PLANES = {"ATLAS", "NOVO", "L", "O", "T", "REL", "SCALE", "EVID", "GAP", "LEARN"}
EXPECTED_INGESTION_ORDER = [
    "ENUMERATE",
    "IDENTIFY",
    "HASH_REVISION",
    "PROVENANCE",
    "RELATIONS",
    "CONTRACTS",
    "EVIDENCE",
    "GAPS_TOKEN_VAZIO",
    "URGENCY",
    "VALIDATION",
    "RECEIPT",
    "ATLAS_EDGES",
    "LEARN_APPEND",
    "CLOSURE",
]
EXPECTED_TERMINALS = {
    "RESOLVED_EVIDENCED",
    "ACCEPTED_BOUNDARY",
    "FALSIFIED",
    "SUPERSEDED",
    "DEFERRED_WITH_TRIGGER",
}
REQUIRED_GUARDS = {
    "SEARCH_MISS_NE_GLOBAL_ABSENCE",
    "DERIVED_NE_OBSERVED",
    "FIXTURE_NE_LIVE",
    "CODE_PRESENT_NE_RUNTIME_VERIFIED",
    "TOKEN_VAZIO_NE_ZERO",
    "FROZEN_HISTORY_NE_DESTRUCTIVE_REWRITE",
    "SUPERSESSION_REQUIRES_RECEIPT",
    "CLAIM_ALLOWED_FALSE_BY_DEFAULT",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def validate(data: dict) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(data.get("schema") == EXPECTED_SCHEMA, "schema mismatch")
    require(data.get("state") in {"VERIFIED_LIMITED_APPEND_ONLY", "CLOSED_VERIFIED"}, "invalid state")
    require(data.get("source_mutation_allowed") is False, "source_mutation_allowed must be false")
    require(isinstance(data.get("predecessors"), list) and len(data["predecessors"]) >= 1, "predecessor required")

    master = data.get("master_index", {})
    require(isinstance(master, dict), "master_index must be object")
    require(master.get("append_only") is True, "MASTER_INDEX must be append_only")
    legacy = set(master.get("legacy_planes_preserved", []))
    transversal = set(master.get("transversal_planes_added", []))
    require(bool(legacy), "legacy planes must be preserved")
    require(EXPECTED_TRANSVERSAL <= transversal, "missing transversal registry")
    require(not (legacy & EXPECTED_TRANSVERSAL), "transversal registry must not masquerade as legacy plane")

    node_contract = data.get("canonical_node_contract", {})
    dims = set(node_contract.get("required_dimensions", [])) if isinstance(node_contract, dict) else set()
    require(EXPECTED_DIMENSIONS <= dims, "canonical node dimensions incomplete")
    require(node_contract.get("identity_pattern") == "RAF:<provider>:<authority>:<object-id>:<revision>", "stable identity pattern mismatch")

    contracts = data.get("contracts", [])
    contract_ids = {c.get("id") for c in contracts if isinstance(c, dict)}
    require(EXPECTED_CONTRACTS <= contract_ids, "required contracts missing")
    for contract in contracts:
        if not isinstance(contract, dict):
            errors.append("contract entry must be object")
            continue
        invariant = str(contract.get("invariant", ""))
        require("TOKEN_VAZIO=0" not in invariant.replace(" ", ""), f"contract {contract.get('id')} collapses TOKEN_VAZIO to zero")
        require(contract.get("blocks_claim") is True, f"contract {contract.get('id')} must block claim on failure")

    lifecycle = data.get("token_vazio_lifecycle", {})
    require(lifecycle.get("open") == "TOKEN_VAZIO", "TOKEN_VAZIO lifecycle open state mismatch")
    require(EXPECTED_TERMINALS <= set(lifecycle.get("allowed_terminal_states", [])), "TOKEN_VAZIO terminal states incomplete")
    forbidden = str(lifecycle.get("forbidden_transition", ""))
    require("ASSUMED_VALUE_WITHOUT_EVIDENCE" in forbidden, "missing no-assumption TOKEN_VAZIO guard")

    atlas = data.get("atlas_planes", {})
    require(EXPECTED_ATLAS_PLANES <= set(atlas.keys()) if isinstance(atlas, dict) else False, "ATLAS routing planes incomplete")
    require(data.get("ingestion_order") == EXPECTED_INGESTION_ORDER, "ingestion order regression")

    closure = data.get("closure_contract", {})
    formula = str(closure.get("formula", "")) if isinstance(closure, dict) else ""
    for term in ("C_objects", "C_identity", "C_provenance", "C_relations", "C_contracts", "C_evidence", "C_gaps", "C_receipts"):
        require(term in formula, f"closure formula missing {term}")

    guards = set(data.get("guards", []))
    require(REQUIRED_GUARDS <= guards, "anti-regression guards incomplete")

    open_priority = data.get("open_priority_gaps", [])
    if open_priority:
        require(data.get("claim_allowed") is False, "global claim must remain false while priority gaps are open")
        require(data.get("state") != "CLOSED_VERIFIED", "cannot be CLOSED_VERIFIED with open priority gaps")

    for route in data.get("seed_routes", []):
        if not isinstance(route, dict):
            errors.append("seed route must be object")
            continue
        relations = route.get("relations", [])
        if any(str(rel).startswith("GAP:") for rel in relations):
            require(route.get("claim_allowed") is False, f"route {route.get('object')} has GAP but claim_allowed is not false")

    require(isinstance(data.get("F_next"), list) and bool(data.get("F_next")), "F_next must remain explicit")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="data/control-plane/CANONICAL_CONTROL_PLANE_ATLAS_V1_20260829.json",
    )
    args = parser.parse_args()
    path = Path(args.path)

    try:
        data = load_json(path)
    except Exception as exc:  # fail closed
        print(f"FAIL: cannot load {path}: {exc}", file=sys.stderr)
        return 2

    errors = validate(data)
    if errors:
        print(f"FAIL: {path}")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"PASS: {path}")
    print(" - canonical node dimensions preserved")
    print(" - TOKEN_VAZIO cannot collapse to zero/assumption")
    print(" - ATLAS planes and ingestion order preserved")
    print(" - open gaps keep global claim fail-closed")
    print(" - anti-regression guards preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
