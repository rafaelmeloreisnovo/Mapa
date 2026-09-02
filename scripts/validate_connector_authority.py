#!/usr/bin/env python3
"""
Connector Authority Validation Script (REFERENCE)

This script validates Circle 1, Gate RM-01: Authority boundary validation
Status: REFERENCE (documented; not yet implemented/executed)

Do NOT run this until explicitly authorized; currently TOKEN_VAZIO on execution.
"""

import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any


def validate_connector_authority(connector_name: str, strict: bool = False) -> bool:
    """
    Validate that connector ownership is unambiguous within federated authority pyramid.

    Circle 1, Gate RM-01 validation.

    Args:
        connector_name: Name of connector under review
        strict: If True, fail on any ambiguity; if False, warn and continue

    Returns:
        True if validation passes; False if FAIL_CLOSED
    """
    print(f"[RM-01] Validating connector authority: {connector_name}")
    print(f"  Strict mode: {strict}")

    # Load connectors under review
    registry_path = Path(__file__).parent.parent / "data" / "control-plane" / "CONNECTORS_UNDER_REVISION.v1.json"
    if not registry_path.exists():
        print(f"ERROR: Registry not found at {registry_path}")
        return False

    with open(registry_path) as f:
        registry = json.load(f)

    # Find connector
    connector = None
    for conn in registry.get("connectors", []):
        if conn["name"] == connector_name or conn["connector_id"] == connector_name:
            connector = conn
            break

    if not connector:
        print(f"ERROR: Connector '{connector_name}' not found in registry")
        return False

    print(f"  Connector ID: {connector['connector_id']}")
    print(f"  Source repository: {connector['source_repository']}")
    print(f"  Producer authority: {connector['producer_authority']}")

    # Validation checks (REFERENCE level; not fully implemented)
    checks_passed = 0
    checks_total = 3

    # Check 1: Producer authority is declared
    if connector.get("producer_authority"):
        print(f"  ✓ Producer authority declared")
        checks_passed += 1
    else:
        print(f"  ✗ Producer authority NOT declared (TOKEN_VAZIO)")

    # Check 2: Source repository is accessible (REFERENCE only; not checking actual git)
    if connector.get("source_repository"):
        print(f"  ✓ Source repository declared")
        checks_passed += 1
    else:
        print(f"  ✗ Source repository NOT declared")

    # Check 3: Connector status is UNDER_REVIEW
    if connector.get("status") == "UNDER_REVIEW":
        print(f"  ✓ Connector status is UNDER_REVIEW (ready for registration)")
        checks_passed += 1
    else:
        print(f"  ✗ Connector status is not UNDER_REVIEW: {connector.get('status')}")

    result = checks_passed == checks_total

    if result:
        print(f"\n[RM-01] PASS: Authority boundary validated")
    else:
        if strict:
            print(f"\n[RM-01] FAIL_CLOSED: {checks_passed}/{checks_total} checks passed (strict mode)")
        else:
            print(f"\n[RM-01] WARNING: {checks_passed}/{checks_total} checks passed (non-strict)")

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_connector_authority.py <connector_name> [--strict]")
        sys.exit(1)

    connector_name = sys.argv[1]
    strict = "--strict" in sys.argv

    result = validate_connector_authority(connector_name, strict=strict)
    sys.exit(0 if result else 1)
