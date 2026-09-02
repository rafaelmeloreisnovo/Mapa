#!/usr/bin/env python3
"""
Connector Evidence Scope Boundary Script

This script validates Circle 1, Gate RM-03: Evidence scope boundary declaration.
Ensures connector declares evidence scope (local/federated/third-party) and authority boundaries.
"""

import json
import sys
from pathlib import Path


def validate_evidence_scope(connector_name: str, strict: bool = False) -> bool:
    """
    Validate that connector declares evidence scope and authority boundaries.

    Circle 1, Gate RM-03 validation.

    Args:
        connector_name: Name or ID of connector under review
        strict: If True, fail on undeclared scope; if False, warn and continue

    Returns:
        True if validation passes; False if FAIL_CLOSED
    """
    print(f"[RM-03] Validating evidence scope boundary: {connector_name}")
    print(f"  Strict mode: {strict}")

    registry_path = Path(__file__).parent.parent / "data" / "control-plane" / "CONNECTORS_UNDER_REVISION.v1.json"
    if not registry_path.exists():
        print(f"ERROR: Registry not found at {registry_path}")
        return False

    with open(registry_path) as f:
        registry = json.load(f)

    connectors = registry.get("connectors", [])

    # Find target connector
    target_connector = None
    for conn in connectors:
        if conn["name"] == connector_name or conn["connector_id"] == connector_name:
            target_connector = conn
            break

    if not target_connector:
        print(f"ERROR: Connector '{connector_name}' not found in registry")
        return False

    print(f"  Connector ID: {target_connector['connector_id']}")
    print(f"  Producer authority: {target_connector['producer_authority']}")

    # Validation checks for evidence scope
    checks_passed = 0
    checks_total = 3

    # Check 1: Producer authority declared and clear
    if target_connector.get("producer_authority"):
        authority_parts = target_connector["producer_authority"].split("(")
        if len(authority_parts) >= 1:
            print(f"  ✓ Producer authority declared: {authority_parts[0].strip()}")
            checks_passed += 1
        else:
            print(f"  ✗ Producer authority format unclear")
    else:
        print(f"  ✗ Producer authority NOT declared")

    # Check 2: Purpose/scope declared (describes what evidence type)
    if target_connector.get("purpose"):
        print(f"  ✓ Scope purpose declared: {target_connector['purpose'][:60]}...")
        checks_passed += 1
    else:
        print(f"  ✗ Scope purpose NOT declared (TOKEN_VAZIO)")

    # Check 3: Risk assessment declared (indicates evidence type expectations)
    if target_connector.get("risk_assessment"):
        print(f"  ✓ Risk assessment declared: {target_connector['risk_assessment']}")
        checks_passed += 1
    else:
        print(f"  ✗ Risk assessment NOT declared")

    result = checks_passed == checks_total

    if result:
        print(f"\n[RM-03] PASS: Evidence scope boundary validated")
    else:
        if strict:
            print(f"\n[RM-03] FAIL_CLOSED: {checks_passed}/{checks_total} checks passed (strict mode)")
        else:
            print(f"\n[RM-03] WARNING: {checks_passed}/{checks_total} checks passed (non-strict)")

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_evidence_scope.py <connector_name> [--strict]")
        sys.exit(1)

    connector_name = sys.argv[1]
    strict = "--strict" in sys.argv

    result = validate_evidence_scope(connector_name, strict=strict)
    sys.exit(0 if result else 1)
