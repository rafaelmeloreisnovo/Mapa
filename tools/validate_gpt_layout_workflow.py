#!/usr/bin/env python3
"""Fail-closed validator for RAFAELIA GPT Layout Workflow V1."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "governance" / "GPT_LAYOUT_WORKFLOW_V1.json"

REQUIRED_LAYERS = [
    "L0_HUMAN_INTERFACE",
    "L1_BOOTSTRAP",
    "L2_AUTHORITY",
    "L3_NAVIGATION",
    "L4_ACTIVATION",
    "L5_EXECUTION_EVIDENCE",
    "L6_RETROFEEDBACK",
]

REQUIRED_INVARIANTS = {
    "SESSION != LONGITUDINAL_MEMORY != EVIDENCE",
    "MASCOTE != AGENTE != AUTORIDADE != EXECUTOR",
    "VISAO != ARTEFATO != EXECUCAO != EVIDENCIA != CLAIM",
    "TOKEN_VAZIO != PASS",
    "no competing master registry",
}

REQUIRED_PROFILES = {
    "new_session",
    "research_or_paper",
    "code_or_repository",
    "memory_or_session",
    "current_status",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    if not SPEC.is_file():
        fail(f"missing spec: {SPEC.relative_to(ROOT)}")

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("schema") != "rafaelia.gpt-layout-workflow/v1":
        fail("unexpected schema")

    if data.get("claim_state") != "REFERENCE":
        fail("claim_state must remain REFERENCE")

    bootstrap = data.get("bootstrap")
    if bootstrap != "bootstrap/RAFAELIA_CHATGPT_BOOTSTRAP_V1.md":
        fail("bootstrap pointer drift")
    if not (ROOT / bootstrap).is_file():
        fail("bootstrap pointer does not resolve")

    authority = data.get("authority_matrix")
    if authority != "governance/AUTHORITY_MATRIX_V1.yaml":
        fail("authority pointer drift")
    if not (ROOT / authority).is_file():
        fail("authority pointer does not resolve")

    activation = data.get("activation_registry")
    if activation != "governance/ACTIVATION_REGISTRY_V1.json":
        fail("activation pointer drift")
    if not (ROOT / activation).is_file():
        fail("activation pointer does not resolve")

    layers = [item.get("id") for item in data.get("layers", [])]
    if layers != REQUIRED_LAYERS:
        fail(f"layer order mismatch: {layers}")

    invariants = set(data.get("invariants", []))
    missing_invariants = REQUIRED_INVARIANTS - invariants
    if missing_invariants:
        fail(f"missing invariants: {sorted(missing_invariants)}")

    profiles = set(data.get("workflow_profiles", {}))
    missing_profiles = REQUIRED_PROFILES - profiles
    if missing_profiles:
        fail(f"missing workflow profiles: {sorted(missing_profiles)}")

    custom = data.get("custom_instruction_contract", {})
    if "bootstrap pointer" not in custom.get("keep", []):
        fail("custom instructions must preserve bootstrap pointer")
    if "mutable PR states" not in custom.get("exclude", []):
        fail("mutable PR state must stay outside custom instructions")

    fallback = data.get("fallback", {})
    for key, value in fallback.items():
        if not value.startswith("TOKEN_VAZIO"):
            fail(f"fallback {key} is not fail-closed: {value}")

    outputs = data.get("layers", [])[-1].get("output", [])
    if outputs != ["F_ok", "F_gap", "F_next", "DELTA"]:
        fail("R3 output contract mismatch")

    print("PASS: GPT Layout Workflow V1")
    print(f"layers={len(layers)}")
    print(f"profiles={len(profiles)}")
    print(f"invariants={len(invariants)}")
    print("claim_state=REFERENCE")


if __name__ == "__main__":
    main()
