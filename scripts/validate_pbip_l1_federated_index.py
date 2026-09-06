"""Validate the PBIP-L1 federated formula index.

This validates federation structure and evidence gating only. It does not prove
PBIP runtime execution or any physical/cosmological equivalence.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

SHA40 = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_NODES = {
    "FORMAL_MATH",
    "GEOMETRY_REFERENCE",
    "ACADEMIC_LEDGER",
    "RLL_BINDING",
    "VECTRAS_BINDING",
    "PRIVATE_BINDING",
    "EVIDENCE_ROUTE",
}
REQUIRED_GATES = {
    "TOKEN_VAZIO_CI_BINDING_PBIP_L1",
    "TOKEN_VAZIO_POLY3_CANONICAL",
    "TOKEN_VAZIO_PHYSICAL_VORTEX_MODEL",
}


def validate(index: dict) -> list[str]:
    errors: list[str] = []

    if index.get("schema_version") != "1.0":
        errors.append("bad schema_version")
    if index.get("federation_id") != "PBIP-L1-FED-V1":
        errors.append("bad federation_id")
    if index.get("formula_id") != "PBIP-L1":
        errors.append("bad formula_id")
    if index.get("claim_allowed") is not False:
        errors.append("claim_allowed must be false")

    formula = index.get("formula", {})
    if formula.get("pythagorean_form") != "q^2 = r^2 - d_perp^2":
        errors.append("unexpected Pythagorean form")
    if formula.get("quadratic_form") != "Delta_B = 4(r^2 - d_perp^2) = 4q^2":
        errors.append("unexpected quadratic form")

    nodes = index.get("nodes", [])
    ids = [node.get("id") for node in nodes]
    if len(ids) != len(set(ids)):
        errors.append("duplicate node ids")
    if set(ids) != REQUIRED_NODES:
        errors.append("node set incomplete")

    known = set(ids)
    for node in nodes:
        if not node.get("repo") or not node.get("path") or not node.get("role"):
            errors.append(f"{node.get('id')}: incomplete node")
        if not SHA40.fullmatch(str(node.get("ref", ""))):
            errors.append(f"{node.get('id')}: unpinned ref")

    for edge in index.get("edges", []):
        if not isinstance(edge, list) or len(edge) != 3:
            errors.append("malformed edge")
            continue
        source, target, relation = edge
        if source not in known or target not in known:
            errors.append("dangling edge")
        if source == target:
            errors.append("self edge")
        if not relation:
            errors.append("empty relation")

    evidence = index.get("evidence_state", {})
    if evidence.get("source_observed") is not True:
        errors.append("source_observed must be true")
    if evidence.get("wired_documentally") is not True:
        errors.append("wired_documentally must be true")
    for field in (
        "implemented_pbip_consumer",
        "build_proven",
        "runtime_proven",
        "device_proven",
        "reproduced",
    ):
        if evidence.get(field) is not False:
            errors.append(f"{field} must remain false until evidence exists")

    gates = set(index.get("gates", []))
    if not REQUIRED_GATES.issubset(gates):
        errors.append("required TOKEN_VAZIO gates missing")

    invariants = set(index.get("invariants", []))
    for required in (
        "TOKEN_VAZIO != 0",
        "FORMULA != IMPLEMENTATION",
        "EVIDENCE != CLAIM",
        "Poincare_return_map != Poincare_conjecture",
        "H_RADIAL_30 != H_MAX_EQUILATERAL_MERIDIAN",
    ):
        if required not in invariants:
            errors.append(f"missing invariant: {required}")

    rll = next((n for n in nodes if n.get("id") == "RLL_BINDING"), {})
    if rll.get("physical_equivalence") is not False:
        errors.append("RLL physical_equivalence must be false")

    return errors


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="data/control-plane/PBIP_L1_FEDERATED_INDEX.v1.json",
    )
    args = parser.parse_args()
    errors = validate(load(args.path))
    if errors:
        raise SystemExit("INVALID: " + "; ".join(errors))
    print("PASS: PBIP-L1-FED-V1 structural federation valid")
