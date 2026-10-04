#!/usr/bin/env python3
"""Validate the repository exposure/freestanding decision matrix.

Stdlib-only. This validates inventory coherence and gate invariants. It does not
change repository visibility and does not prove authorship or freestanding status.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "control-plane" / "repository_exposure_freestanding.v1.json"

ALLOWED_GROUPS = {
    "KEEP_PUBLIC",
    "KEEP_PUBLIC_REVIEW_PROVENANCE",
    "KEEP_PUBLIC_LOW_RISK",
    "REVIEW_PUBLIC",
    "CLOSE_PENDING_SANITIZED_EXPORT",
    "KEEP_PRIVATE",
    "SPLIT_PUBLIC_CORE_PRIVATE_CONTROL",
    "PUBLIC_AFTER_GATE",
}

REQUIRED_INVARIANTS = {
    "SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM",
    "TOKEN_VAZIO != 0",
    "IMPLEMENTED_UNTESTED != PASS",
    "PUBLIC != AUTHORIAL",
    "AUTHORIAL != FREESTANDING",
    "FREESTANDING_PASS requires evidence, not naming or intent",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def duplicates(items: list[str]) -> list[str]:
    seen: set[str] = set()
    dup: set[str] = set()
    for item in items:
        if item in seen:
            dup.add(item)
        seen.add(item)
    return sorted(dup)


def main() -> int:
    try:
        data = json.loads(MATRIX.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse matrix: {exc}")

    if data.get("schema") != "rafaelia.repository-exposure-freestanding/v1":
        fail("unexpected schema")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        fail("authority must be an object")
    for key in ("human_policy", "machine_matrix", "authorship_invariant"):
        raw = authority.get(key)
        if not isinstance(raw, str) or not raw:
            fail(f"authority.{key} missing")
        if not (ROOT / raw).exists():
            fail(f"authority path missing: {raw}")

    invariants = set(data.get("invariants", []))
    missing = sorted(REQUIRED_INVARIANTS - invariants)
    if missing:
        fail(f"missing invariants: {missing}")

    gate = data.get("freestanding_gate")
    if not isinstance(gate, dict):
        fail("freestanding_gate must be an object")
    required = gate.get("required")
    if not isinstance(required, list) or len(required) < 8:
        fail("freestanding_gate.required is incomplete")
    if gate.get("inventory_result") != "NO_REPOSITORY_PROMOTED_TO_FREESTANDING_PASS_BY_METADATA_ONLY":
        fail("inventory result must fail closed")

    groups = data.get("groups")
    if not isinstance(groups, dict):
        fail("groups must be an object")
    if set(groups) != ALLOWED_GROUPS:
        fail(f"unexpected group set: {sorted(set(groups) ^ ALLOWED_GROUPS)}")

    grouped: list[str] = []
    for name, values in groups.items():
        if not isinstance(values, list) or not all(isinstance(v, str) and v for v in values):
            fail(f"group {name} must contain non-empty repository names")
        grouped.extend(values)
    dup_grouped = duplicates(grouped)
    if dup_grouped:
        fail(f"repository appears in multiple recommendation groups: {dup_grouped}")

    visibility = data.get("current_visibility")
    if not isinstance(visibility, dict):
        fail("current_visibility must be an object")
    public = visibility.get("public")
    private = visibility.get("private")
    if not isinstance(public, list) or not isinstance(private, list):
        fail("visibility lists missing")
    if duplicates(public) or duplicates(private):
        fail("duplicates inside visibility lists")
    overlap = sorted(set(public) & set(private))
    if overlap:
        fail(f"repository cannot be both public and private: {overlap}")

    visible = public + private
    if sorted(grouped) != sorted(visible):
        missing_from_groups = sorted(set(visible) - set(grouped))
        missing_from_visibility = sorted(set(grouped) - set(visible))
        fail(
            "group/visibility inventory mismatch: "
            f"missing_from_groups={missing_from_groups}; "
            f"missing_from_visibility={missing_from_visibility}"
        )

    scope = data.get("scope", {})
    if scope.get("repositories_observed") != len(visible):
        fail("scope.repositories_observed mismatch")
    if scope.get("public") != len(public):
        fail("scope.public mismatch")
    if scope.get("private") != len(private):
        fail("scope.private mismatch")
    if len(visible) != 90 or len(public) != 30 or len(private) != 60:
        fail(f"unexpected V1 inventory size: total={len(visible)} public={len(public)} private={len(private)}")

    if groups["CLOSE_PENDING_SANITIZED_EXPORT"] != [
        "TRABALHO_ROADMAP_AUDIT_GOV_DATA_ROTA_MAPwithCHAIN_security"
    ]:
        fail("P0 close lane changed without matrix version update")
    if groups["SPLIT_PUBLIC_CORE_PRIVATE_CONTROL"] != ["RafNet-Core"]:
        fail("P0 split lane changed without matrix version update")

    print(
        "PASS: repository exposure matrix coherent; "
        f"repos={len(visible)} public={len(public)} private={len(private)} "
        f"groups={len(groups)} schema={data['schema']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
