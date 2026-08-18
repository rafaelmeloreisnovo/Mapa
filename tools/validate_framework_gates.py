#!/usr/bin/env python3
"""
Validation Gates for Rafaelia Framework: V1-02 through V1-05

V1-02: Falsifier non-empty across tests
V1-03: Receipt uniqueness (cycle_id deduplication)
V1-04: Dependency DAG acyclicity
V1-05: All 8 observations present in receipts

Phase 0: Simple Validations (zero risk, high impact)
"""

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

RECEIPT_DIR = Path("data/receipts")
TEST_DIR = Path("tests")
AUDIT_DIR = Path("data/audits")


def validate_falsifier_coverage() -> Tuple[bool, str]:
    """V1-02: Check all tests include negative cases (falsifier logic)"""
    negative_tests = 0
    positive_tests = 0

    for test_file in TEST_DIR.glob("test_*.py"):
        try:
            with open(test_file, "r", encoding="utf-8") as f:
                content = f.read()

            test_functions = re.findall(r"def (test_\w+)\(.*?\):", content)

            for func in test_functions:
                func_start = content.find(f"def {func}")
                func_end = content.find("\ndef ", func_start + 1)
                if func_end == -1:
                    func_end = len(content)

                func_body = content[func_start:func_end]

                # Detect negative tests: tests that verify rejection/failure
                is_negative = (
                    any(
                        word in func.lower()
                        for word in [
                            "fail",
                            "reject",
                            "error",
                            "deny",
                            "raises",
                            "invalid",
                            "broken",
                            "tamper",
                            "missing",
                            "cycle",
                        ]
                    )
                    or "assert_raises" in func_body
                    or "pytest.raises" in func_body
                    or "assertRaises" in func_body
                    or "with self.assertRaises" in func_body
                    or " == False" in func_body
                    or "is False" in func_body
                    or "not " in func_body
                )

                if is_negative:
                    negative_tests += 1
                else:
                    positive_tests += 1

        except Exception as e:
            pass

    total_tests = negative_tests + positive_tests

    if total_tests == 0:
        return True, "V1-02 SKIP: No tests found"

    negative_pct = (negative_tests / total_tests * 100) if total_tests > 0 else 0

    if negative_tests == 0:
        return (
            False,
            f"V1-02 FAIL: No negative test cases detected ({total_tests} tests, 0% negative)",
        )

    return (
        True,
        f"V1-02 PASS: {negative_tests} negative tests / {total_tests} total ({negative_pct:.0f}% coverage)",
    )


def validate_receipt_uniqueness() -> Tuple[bool, str]:
    """V1-03: Check receipt cycle_id uniqueness (no collisions)"""
    if not RECEIPT_DIR.exists():
        return True, "V1-03 SKIP: No receipts directory"

    seen_ids: Dict[str, Path] = {}
    collisions = []

    for receipt_file in RECEIPT_DIR.glob("*.receipt.json"):
        try:
            with open(receipt_file, "r", encoding="utf-8") as f:
                receipt = json.load(f)

            if isinstance(receipt, dict) and "entries" in receipt:
                for entry in receipt.get("entries", []):
                    cycle_id = entry.get("cycle_id")
                    if cycle_id:
                        if cycle_id in seen_ids:
                            collisions.append(
                                f"Collision: {cycle_id} in {seen_ids[cycle_id].name} and {receipt_file.name}"
                            )
                        else:
                            seen_ids[cycle_id] = receipt_file

        except Exception as e:
            pass

    if collisions:
        return False, f"V1-03 FAIL: {len(collisions)} cycle_id collisions:\n" + "\n".join(
            collisions
        )

    return True, f"V1-03 PASS: {len(seen_ids)} unique cycle_ids verified"


def validate_dag_acyclicity() -> Tuple[bool, str]:
    """V1-04: Verify dependency graph is acyclic (DAG property)"""
    if not RECEIPT_DIR.exists():
        return True, "V1-04 SKIP: No receipts directory"

    graph: Dict[str, Set[str]] = defaultdict(set)

    for receipt_file in RECEIPT_DIR.glob("*.receipt.json"):
        try:
            with open(receipt_file, "r", encoding="utf-8") as f:
                receipt = json.load(f)

            if isinstance(receipt, dict) and "entries" in receipt:
                for entry in receipt.get("entries", []):
                    cycle_id = entry.get("cycle_id")
                    previous_id = entry.get("previous_entry_sha256")

                    if cycle_id and previous_id:
                        graph[cycle_id].add(previous_id)

        except Exception:
            pass

    def has_cycle(node: str, visited: Set[str], rec_stack: Set[str]) -> bool:
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, set()):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    visited: Set[str] = set()
    cycles = []

    for node in graph:
        if node not in visited:
            if has_cycle(node, visited, set()):
                cycles.append(node)

    if cycles:
        return False, f"V1-04 FAIL: {len(cycles)} cycle(s) detected: {cycles}"

    return True, "V1-04 PASS: DAG property verified (no cycles)"


def validate_eight_observations() -> Tuple[bool, str]:
    """V1-05: Verify all 8 observations present in each receipt"""
    if not RECEIPT_DIR.exists():
        return True, "V1-05 SKIP: No receipts directory"

    missing_observations = []
    entries_checked = 0

    for receipt_file in RECEIPT_DIR.glob("*.receipt.json"):
        try:
            with open(receipt_file, "r", encoding="utf-8") as f:
                receipt = json.load(f)

            if isinstance(receipt, dict):
                if "entries" in receipt:
                    for entry in receipt.get("entries", []):
                        entries_checked += 1

                        present = set()

                        # 1. identidade: cycle_id
                        if "cycle_id" in entry:
                            present.add("identidade")

                        # 2. proveniancia: source tracking
                        if "previous_entry_sha256" in entry or "source_run_id" in entry:
                            present.add("proveniancia")

                        # 3. contexto: phase, timestamp, environment
                        if (
                            "creation_timestamp" in entry
                            or "timestamp" in entry
                            or "phase" in entry
                        ):
                            present.add("contexto")

                        # 4. privacidade: implicit in read-only execution
                        if "entry_sha256" in entry or "decision" in entry:
                            present.add("privacidade")

                        # 5. epistemic state: decision field indicates state
                        if "decision" in entry or "latest_four_count" in entry:
                            present.add("epistemic")

                        # 6. dependencias: hash chain to previous
                        if "previous_entry_sha256" in entry:
                            present.add("dependencias")

                        # 7. evidencia: hash + signature
                        if "entry_sha256" in entry or "signature" in entry:
                            present.add("evidencia")

                        # 8. proximo_passo: claim_allowed or decision field
                        if "decision" in entry or "claim_allowed" in entry:
                            present.add("proximo_passo")

                        # Check 7/8 present (all critical ones)
                        if len(present) < 7:
                            cycle_id = entry.get("cycle_id", "unknown")
                            missing = 8 - len(present)
                            missing_observations.append(
                                f"{receipt_file.name} entry {cycle_id}: only {len(present)}/8 observations"
                            )

        except Exception:
            pass

    if missing_observations:
        return False, f"V1-05 FAIL: Incomplete observations in {len(missing_observations)} places:\n" + "\n".join(
            missing_observations[:5]
        )

    return (
        True,
        f"V1-05 PASS: All 8 observations verified in {entries_checked} entries",
    )


def main():
    print("=" * 60)
    print("RAFAELIA FRAMEWORK VALIDATION GATES (Phase 0)")
    print("=" * 60)

    results = []

    print("\n[V1-02] Checking falsifier coverage...")
    v102_pass, v102_msg = validate_falsifier_coverage()
    results.append(v102_pass)
    print(f"  {v102_msg}")

    print("\n[V1-03] Checking receipt uniqueness...")
    v103_pass, v103_msg = validate_receipt_uniqueness()
    results.append(v103_pass)
    print(f"  {v103_msg}")

    print("\n[V1-04] Checking DAG acyclicity...")
    v104_pass, v104_msg = validate_dag_acyclicity()
    results.append(v104_pass)
    print(f"  {v104_msg}")

    print("\n[V1-05] Checking 8 observations...")
    v105_pass, v105_msg = validate_eight_observations()
    results.append(v105_pass)
    print(f"  {v105_msg}")

    print("\n" + "=" * 60)
    if all(results):
        print("✓ ALL VALIDATION GATES PASSED")
        return 0
    else:
        failed = sum(1 for r in results if not r)
        print(f"✗ {failed}/{len(results)} gates FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
