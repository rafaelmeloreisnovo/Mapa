#!/usr/bin/env python3
"""
Connector Namespace Collision Detection Script

This script validates Circle 1, Gate RM-02: Namespace collision detection.
Ensures no duplicate identifiers, aliases, or source repositories across connectors.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set


def validate_namespace_collisions(connector_name: str, strict: bool = False) -> bool:
    """
    Validate that connector has no namespace collisions with existing connectors.

    Circle 1, Gate RM-02 validation.

    Args:
        connector_name: Name or ID of connector under review
        strict: If True, fail on any collision; if False, warn and continue

    Returns:
        True if validation passes; False if FAIL_CLOSED
    """
    print(f"[RM-02] Validating namespace collisions: {connector_name}")
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

    # Build namespace indices from all OTHER connectors
    existing_ids: Set[str] = set()
    existing_names: Set[str] = set()
    existing_aliases: Set[str] = set()
    existing_repos: Set[str] = set()

    for conn in connectors:
        if conn["connector_id"] == target_connector["connector_id"]:
            continue  # Skip self
        existing_ids.add(conn["connector_id"])
        existing_names.add(conn["name"])
        existing_aliases.add(conn.get("alias", ""))
        existing_repos.add(conn["source_repository"])

    # Check for collisions
    collisions = []

    if target_connector["connector_id"] in existing_ids:
        collisions.append(f"Connector ID conflict: {target_connector['connector_id']}")

    if target_connector["name"] in existing_names:
        collisions.append(f"Connector name conflict: {target_connector['name']}")

    if target_connector.get("alias") and target_connector["alias"] in existing_aliases:
        collisions.append(f"Connector alias conflict: {target_connector['alias']}")

    if target_connector["source_repository"] in existing_repos:
        collisions.append(f"Source repository conflict: {target_connector['source_repository']}")

    if collisions:
        for collision in collisions:
            print(f"  ✗ {collision}")
        if strict:
            print(f"\n[RM-02] FAIL_CLOSED: Namespace collision detected (strict mode)")
        else:
            print(f"\n[RM-02] WARNING: Namespace collision detected (non-strict)")
        return False
    else:
        print(f"  ✓ Connector ID unique")
        print(f"  ✓ Connector name unique")
        print(f"  ✓ Connector alias unique")
        print(f"  ✓ Source repository unique")
        print(f"\n[RM-02] PASS: No namespace collisions detected")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_namespace_collisions.py <connector_name> [--strict]")
        sys.exit(1)

    connector_name = sys.argv[1]
    strict = "--strict" in sys.argv

    result = validate_namespace_collisions(connector_name, strict=strict)
    sys.exit(0 if result else 1)
