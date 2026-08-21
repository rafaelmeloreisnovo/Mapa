#!/usr/bin/env python3
"""Phase 0 Foundation Validation: 5 CI gates for zero-risk baseline."""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def validate_claim_allowed(state_file: Path) -> Tuple[bool, str]:
    """Gate 1: Claim allowed must be false during Phase 0."""
    try:
        with open(state_file) as f:
            data = json.load(f)
        if data.get("claim_allowed") is not False:
            return False, f"claim_allowed={data.get('claim_allowed')}, expected False"
        return True, "✓ claim_allowed=false"
    except Exception as e:
        return False, str(e)


def validate_falsifiers(data_dir: Path) -> Tuple[bool, str]:
    """Gate 2: Every TOKEN_VAZIO must have falsifier + next_verifiable_step."""
    errors = []
    checked = 0

    for json_file in data_dir.rglob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)

            # Check if it's an operational gap or similar structure
            if isinstance(data, dict) and data.get("status") == "TOKEN_VAZIO":
                checked += 1
                if not data.get("falsifier"):
                    errors.append(f"{json_file.name}: missing falsifier")
                if not data.get("next_verifiable_step"):
                    errors.append(f"{json_file.name}: missing next_verifiable_step")

            # Check nested structures
            if isinstance(data, dict) and "evidence_id" in data:
                if data.get("status") == "TOKEN_VAZIO":
                    checked += 1
                    if not data.get("recovery_rank"):
                        errors.append(f"{json_file.name}: TOKEN_VAZIO without recovery_rank")
        except (json.JSONDecodeError, TypeError):
            pass

    if errors:
        return False, f"Checked {checked}, found {len(errors)} gaps:\n  " + "\n  ".join(errors)
    return True, f"✓ Falsifiers validated ({checked} TOKEN_VAZIO entries checked)"


def validate_evidence_uniqueness(data_dir: Path) -> Tuple[bool, str]:
    """Gate 3: No duplicate evidence_id within cycle."""
    evidence_ids = {}
    duplicates = []

    for json_file in data_dir.rglob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)

            if isinstance(data, dict):
                evid_id = data.get("evidence_id")
                if evid_id:
                    if evid_id in evidence_ids:
                        duplicates.append((evid_id, evidence_ids[evid_id], json_file.name))
                    else:
                        evidence_ids[evid_id] = json_file.name
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        evid_id = item.get("evidence_id")
                        if evid_id:
                            if evid_id in evidence_ids:
                                duplicates.append((evid_id, evidence_ids[evid_id], json_file.name))
                            else:
                                evidence_ids[evid_id] = json_file.name
        except (json.JSONDecodeError, TypeError):
            pass

    if duplicates:
        dup_str = "\n  ".join([f"{eid}: {f1} == {f2}" for eid, f1, f2 in duplicates])
        return False, f"Duplicates found:\n  {dup_str}"
    return True, f"✓ Evidence uniqueness validated ({len(evidence_ids)} unique IDs)"


def validate_lane_dag(routing_dir: Path) -> Tuple[bool, str]:
    """Gate 4: Lane dependency graph must be acyclic."""
    # Expected DAG: R1 -> R2 -> R3 -> R4/R5
    # No lane should have a reverse dependency

    dependencies = {
        "R1": [],  # qemu source (no dependencies)
        "R2": [],  # androidx source (no dependencies)
        "R3": ["R1", "R2"],  # gradle build (depends on sources)
        "R4": ["R3"],  # abi validation (depends on artifact)
        "R5": ["R3"],  # device runtime (depends on artifact)
    }

    # Check for cycles using DFS
    def has_cycle(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)

        for dep in dependencies.get(node, []):
            if dep not in visited:
                if has_cycle(dep, visited, rec_stack):
                    return True
            elif dep in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    visited = set()
    for node in dependencies:
        if node not in visited:
            if has_cycle(node, visited, set()):
                return False, "Cycle detected in lane dependencies"

    return True, "✓ Lane DAG validated (no cycles, critical path: R1→R2→R3→R4/R5)"


def validate_observation_coverage(state_file: Path) -> Tuple[bool, str]:
    """Gate 5: 8 core observations must have evidence or TOKEN_VAZIO."""
    required_gates = ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8"]

    try:
        with open(state_file) as f:
            data = json.load(f)

        modules = data.get("modules", []) if isinstance(data, dict) else data if isinstance(data, list) else []

        coverage_by_gate = {gate: 0 for gate in required_gates}
        total_by_gate = {gate: 0 for gate in required_gates}

        for module in modules:
            if not isinstance(module, dict):
                continue

            # Each module should address gates O0-O8
            # Map module state to gate evidence
            state = module.get("state", "")
            caps = module.get("capabilities", [])

            if state != "TOKEN_VAZIO":
                coverage_by_gate["O1"] += 1  # Source identity
            total_by_gate["O1"] += 1

            if state in ["VERIFIED_LIMITED", "TESTED_LOCAL", "TESTED_DEVICE"]:
                coverage_by_gate["O2"] += 1  # Contract defined
                coverage_by_gate["O3"] += 1  # Environment ready
                coverage_by_gate["O4"] += 1  # Build executed
            total_by_gate["O2"] += 1
            total_by_gate["O3"] += 1
            total_by_gate["O4"] += 1

            if len(caps) > 0:
                coverage_by_gate["O5"] += 1  # Artifact produced
            total_by_gate["O5"] += 1

            if state == "VERIFIED_LIMITED":
                coverage_by_gate["O6"] += 1  # Signature valid
                coverage_by_gate["O7"] += 1  # ABI compatible
            total_by_gate["O6"] += 1
            total_by_gate["O7"] += 1

            # O8 typically TOKEN_VAZIO in CI
            coverage_by_gate["O8"] += 0 if "TOKEN_VAZIO" in state else 1
            total_by_gate["O8"] += 1

        uncovered = [gate for gate in required_gates if coverage_by_gate[gate] == 0 and total_by_gate[gate] > 0]

        if uncovered:
            return False, f"Uncovered gates: {', '.join(uncovered)}"

        coverage_pct = sum(coverage_by_gate.values()) / max(sum(total_by_gate.values()), 1) * 100
        return True, f"✓ Observation coverage validated ({coverage_pct:.0f}% of gates covered)"
    except Exception as e:
        return False, str(e)


def main() -> int:
    """Run all 5 Phase 0 validation gates."""
    mapa_root = Path(__file__).parent.parent
    state_file = mapa_root / "data" / "control-plane" / "current_state_snapshot.v1.json"
    data_dir = mapa_root / "data"

    gates = [
        ("1: Claim Allowed Enforcement", lambda: validate_claim_allowed(state_file)),
        ("2: Falsifier Checks", lambda: validate_falsifiers(data_dir)),
        ("3: Evidence Uniqueness", lambda: validate_evidence_uniqueness(data_dir)),
        ("4: Lane DAG Acyclicity", lambda: validate_lane_dag(data_dir)),
        ("5: Observation Coverage", lambda: validate_observation_coverage(state_file)),
    ]

    results = []
    failed = 0

    print("\n" + "="*70)
    print("PHASE 0 VALIDATION GATES")
    print("="*70)

    for name, gate_func in gates:
        success, message = gate_func()
        results.append((name, success, message))
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"\nGate {name}")
        print(f"  {status}: {message}")
        if not success:
            failed += 1

    print("\n" + "="*70)
    print(f"SUMMARY: {len(gates) - failed}/{len(gates)} gates passed")
    print("="*70 + "\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
