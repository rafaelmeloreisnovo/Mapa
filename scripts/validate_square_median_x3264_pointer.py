#!/usr/bin/env python3
"""Validate the cross-repository square-median x32/x64 evidence packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED = {
    "EVID-SMR-PAPERS-PR28": ("rafaelmeloreisnovo/papers", 28),
    "EVID-SMR-QEMU-PR65": ("rafaelmeloreisnovo/qemu_rafaelia", 65),
    "EVID-SMR-QEMU-LOCAL-RECEIPT": ("rafaelmeloreisnovo/qemu_rafaelia", None),
    "EVID-SMR-VECTRAS-PR1072": ("rafaelmeloreisnovo/Vectras-VM-Android", 1072),
}


def validate(repo_root: Path):
    packet_path = repo_root / "data/control-plane/evidence_pointer_square_median_x3264.v1.json"
    index_path = repo_root / "indices/SQUARE_MEDIAN_X3264_AUTHORITY_MAP.md"
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    errors = []

    if packet.get("schema_version") != "rafaelia.cross-repo-evidence-packet/v1":
        errors.append("unexpected schema_version")
    if packet.get("claim_allowed") is not False:
        errors.append("packet must remain claim_allowed=false")
    if not index_path.is_file():
        errors.append("authority index missing")

    pointers = {item.get("evidence_id"): item for item in packet.get("pointers", [])}
    if set(pointers) != set(EXPECTED):
        errors.append("pointer identity set differs from canonical V1")

    for evidence_id, (repository, pr_number) in EXPECTED.items():
        item = pointers.get(evidence_id, {})
        if item.get("repository") != repository:
            errors.append(f"{evidence_id}: wrong repository")
        if pr_number is not None and item.get("pr_number") != pr_number:
            errors.append(f"{evidence_id}: wrong PR number")
        if item.get("claim_allowed") is not False:
            errors.append(f"{evidence_id}: claim must be blocked")
        if not item.get("limitations"):
            errors.append(f"{evidence_id}: limitations required")
        if not item.get("ref"):
            errors.append(f"{evidence_id}: immutable observed ref required")

    gates = packet.get("gates", {})
    required_gates = {
        "exact_mathematics": "VERIFIED_LOCAL",
        "elf32_build": "VERIFIED_LOCAL",
        "elf64_native_execution": "VERIFIED_LOCAL",
        "source_built_qemu_i386": "TOKEN_VAZIO_PENDING_WORKFLOW",
        "source_built_qemu_x86_64": "TOKEN_VAZIO_PENDING_WORKFLOW",
        "vectras_linux_user_profile": "TOKEN_VAZIO_NOT_IMPLEMENTED",
        "android_dispatch": "TOKEN_VAZIO",
        "full_system_guest_boot": "NOT_IN_SCOPE",
    }
    for key, value in required_gates.items():
        if gates.get(key) != value:
            errors.append(f"gate {key}: expected {value!r}, got {gates.get(key)!r}")

    relation_nodes = set(pointers)
    for relation in packet.get("relations", []):
        if relation.get("from") not in relation_nodes or relation.get("to") not in relation_nodes:
            errors.append(f"orphan relation: {relation}")

    passed = not errors
    return {
        "schema": "rafaelia.square-median-x3264-pointer-validation.v1",
        "state": "PASS_POINTER_BOUNDARY" if passed else "FAIL_CLOSED",
        "pointer_count": len(pointers),
        "errors": errors,
        "claim_allowed": False,
        "pass": passed,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = validate(args.repo_root.resolve())
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
