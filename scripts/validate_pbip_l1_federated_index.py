"""Validate the PBIP-L1 federated formula index.

This validator accepts controlled lifecycle advancement when concrete evidence is
pinned. It never promotes Android runtime, device, reproduction or scientific
claim state from a unit-test receipt.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_NODES = {
    "FORMAL_MATH",
    "GEOMETRY_REFERENCE",
    "ACADEMIC_LEDGER",
    "RLL_BINDING",
    "VECTRAS_BINDING",
    "PRIVATE_BINDING",
    "EVIDENCE_ROUTE",
}
BASE_REQUIRED_GATES = {
    "TOKEN_VAZIO_POLY3_CANONICAL",
    "TOKEN_VAZIO_PHYSICAL_VORTEX_MODEL",
}
CI_PENDING_GATE = "TOKEN_VAZIO_CI_BINDING_PBIP_L1"


def _node(nodes: list[dict], node_id: str) -> dict:
    return next((n for n in nodes if n.get("id") == node_id), {})


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

    # Unit-level evidence is allowed to advance independently of broader runtime.
    implemented = evidence.get("implemented_pbip_consumer") is True
    unit_build = evidence.get("pbip_unit_build_proven") is True
    unit_exec = evidence.get("unit_test_execution_proven") is True
    provider_receipt = evidence.get("provider_receipt_observed") is True
    artifact_hash = evidence.get("artifact_hash_observed") is True

    unit_flags = (unit_build, unit_exec, provider_receipt, artifact_hash)
    if any(unit_flags) and not implemented:
        errors.append("unit evidence cannot exist without implemented_pbip_consumer")
    if any(unit_flags) and not all(unit_flags):
        errors.append("partial PBIP unit receipt state is not allowed")

    # These broader states remain closed in PBIP-L1 V1.
    for field in ("build_proven", "runtime_proven", "device_proven", "reproduced"):
        if evidence.get(field) is not False:
            errors.append(f"{field} must remain false in PBIP-L1 V1")

    gates = set(index.get("gates", []))
    if not BASE_REQUIRED_GATES.issubset(gates):
        errors.append("base TOKEN_VAZIO gates missing")

    vectras = _node(nodes, "VECTRAS_BINDING")
    route = _node(nodes, "EVIDENCE_ROUTE")

    if unit_exec:
        # The CI-binding gap must close only when a concrete provider receipt is pinned.
        if CI_PENDING_GATE in gates:
            errors.append("CI pending gate must be closed after observed receipt")
        for key in ("implementation_path", "test_path"):
            if not vectras.get(key):
                errors.append(f"VECTRAS_BINDING missing {key}")
        for key in ("implementation_sha256", "test_sha256"):
            if not SHA256.fullmatch(str(vectras.get(key, ""))):
                errors.append(f"VECTRAS_BINDING invalid {key}")
        if not isinstance(vectras.get("workflow_run_id"), int):
            errors.append("VECTRAS_BINDING missing workflow_run_id")
        if not isinstance(vectras.get("workflow_job_id"), int):
            errors.append("VECTRAS_BINDING missing workflow_job_id")
        if not route.get("receipt_path"):
            errors.append("EVIDENCE_ROUTE missing receipt_path")
        if not SHA256.fullmatch(str(route.get("receipt_sha256", ""))):
            errors.append("EVIDENCE_ROUTE invalid receipt_sha256")
        if not isinstance(route.get("artifact_id"), int):
            errors.append("EVIDENCE_ROUTE missing artifact_id")
        if not SHA256.fullmatch(str(route.get("artifact_zip_sha256", ""))):
            errors.append("EVIDENCE_ROUTE invalid artifact_zip_sha256")
    else:
        if implemented and any(unit_flags):
            errors.append("incoherent pending unit evidence state")
        if CI_PENDING_GATE not in gates:
            errors.append("CI pending gate missing before unit receipt")

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

    if unit_exec and "PBIP_UNIT_BUILD_PROVEN != ANDROID_RUNTIME_PROVEN" not in invariants:
        errors.append("missing unit/runtime separation invariant")

    rll = _node(nodes, "RLL_BINDING")
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
