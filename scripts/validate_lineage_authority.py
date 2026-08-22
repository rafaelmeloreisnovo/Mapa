#!/usr/bin/env python3
"""
validate_lineage_authority.py

Validates federated lineage authority schema and deduplication rules.
Ensures cross-repository evidence is correctly classified as independent or dependent.

Execution: python3 validate_lineage_authority.py --check
Exit code: 0 = PASS, 1 = FAIL
"""

import json
import sys
from pathlib import Path

def load_lineage_authority(repo_root="."):
    """Load lineage authority schema from control plane."""
    path = Path(repo_root) / "data" / "control-plane" / "lineage_authority_v1.json"
    if not path.exists():
        print(f"ERROR: lineage_authority_v1.json not found at {path}")
        return None

    with open(path) as f:
        return json.load(f)

def validate_authority_pyramid(authority):
    """Validate 6-repo authority pyramid structure."""
    required_repos = {
        "termux-packages",
        "termux-app-rafacodephi",
        "mapa",
        "rafpolimata",
        "rafgittools",
        "llamarafaelia"
    }

    pyramid = authority.get("authority_pyramid", {})
    found_repos = set(pyramid.keys())

    if found_repos != required_repos:
        print(f"ERROR: Authority pyramid repos mismatch")
        print(f"  Expected: {required_repos}")
        print(f"  Found: {found_repos}")
        return False

    for repo, spec in pyramid.items():
        required_fields = ["role", "responsibility", "scope", "immutable_id_type", "independence_claim"]
        for field in required_fields:
            if field not in spec:
                print(f"ERROR: {repo} missing required field: {field}")
                return False

    print(f"✓ Authority pyramid valid (6 repos)")
    return True

def validate_dedup_rules(authority):
    """Validate deduplication rule classes."""
    required_classes = {
        "identical_artifact",
        "upstream_sync",
        "independent_derivation",
        "cross_repo_evidence_chain"
    }

    rules = {r["class"] for r in authority.get("dedup_rules", [])}
    if rules != required_classes:
        print(f"ERROR: Dedup rules mismatch")
        print(f"  Expected: {required_classes}")
        print(f"  Found: {rules}")
        return False

    for rule in authority.get("dedup_rules", []):
        if "proof_required" not in rule or "is_independent" not in rule:
            print(f"ERROR: Rule {rule['class']} missing proof_required or is_independent")
            return False

        # Validate independence classification
        rule_class = rule["class"]
        is_independent = rule["is_independent"]

        # By definition, identical and upstream are NOT independent
        if rule_class in ["identical_artifact", "upstream_sync"] and is_independent:
            print(f"ERROR: {rule_class} incorrectly marked as independent")
            return False

        # By definition, independent_derivation and cross_repo are independent
        if rule_class in ["independent_derivation", "cross_repo_evidence_chain"] and not is_independent:
            print(f"ERROR: {rule_class} incorrectly marked as non-independent")
            return False

    print(f"✓ Dedup rules valid (4 classes)")
    return True

def validate_lineage_id_schema(authority):
    """Validate lineage ID structure specification."""
    lineage_spec = authority.get("lineage_id_structure", {})

    required_fields = ["format", "example", "immutable", "uniqueness", "versioning", "authority_binding"]
    for field in required_fields:
        if field not in lineage_spec:
            print(f"ERROR: lineage_id_structure missing {field}")
            return False

    # Validate format pattern
    expected_format = "{repo}:{branch}:{commit}:{path}:{artifact_hash}"
    if lineage_spec["format"] != expected_format:
        print(f"ERROR: lineage_id format incorrect")
        print(f"  Expected: {expected_format}")
        print(f"  Found: {lineage_spec['format']}")
        return False

    # Validate immutability claim
    if not lineage_spec["immutable"]:
        print(f"ERROR: lineage_id_structure must be immutable=true")
        return False

    print(f"✓ Lineage ID schema valid")
    return True

def validate_cross_repo_validation(authority):
    """Validate cross-repository validation gates."""
    validation = authority.get("cross_repo_validation", {})

    required_repos = {"termux-packages", "termux-app-rafacodephi", "mapa", "rafpolimata", "rafgittools", "llamarafaelia"}
    found_repos = set(validation.get("repos", []))

    if found_repos != required_repos:
        print(f"ERROR: cross_repo_validation repos mismatch")
        return False

    required_gates = {
        "lineage_chain_closure",
        "authority_non_overlap",
        "dedup_consistency",
        "independence_proof"
    }
    found_gates = set(validation.get("validation_gates", []))

    if found_gates != required_gates:
        print(f"ERROR: cross_repo_validation gates mismatch")
        print(f"  Expected: {required_gates}")
        print(f"  Found: {found_gates}")
        return False

    print(f"✓ Cross-repo validation gates defined (4 gates)")
    return True

def validate_independence_closure(authority):
    """Validate that TV-INDEPENDENCE closure is marked complete."""
    closure = authority.get("tv_independence_closure", {})

    required_conditions = {
        "status": "CLOSED",
        "authority_pyramid_defined": True,
        "dedup_rules_enumerated": True,
        "lineage_id_schema_specified": True,
        "ready_for_federation_certification": True
    }

    for key, expected in required_conditions.items():
        actual = closure.get(key)
        if actual != expected:
            print(f"ERROR: tv_independence_closure.{key} = {actual}, expected {expected}")
            return False

    print(f"✓ TV-INDEPENDENCE closure complete")
    return True

def main():
    """Execute lineage authority validation."""
    import argparse

    parser = argparse.ArgumentParser(description="Validate federated lineage authority")
    parser.add_argument("--check", action="store_true", help="Execute validation check")
    parser.add_argument("--repo-root", default=".", help="Repository root path")

    args = parser.parse_args()

    if not args.check:
        print("Usage: python3 validate_lineage_authority.py --check")
        return 0

    # Load lineage authority
    authority = load_lineage_authority(args.repo_root)
    if authority is None:
        return 1

    print("Validating lineage authority schema...\n")

    # Run validators
    validators = [
        ("Authority pyramid", lambda: validate_authority_pyramid(authority)),
        ("Dedup rules", lambda: validate_dedup_rules(authority)),
        ("Lineage ID schema", lambda: validate_lineage_id_schema(authority)),
        ("Cross-repo validation gates", lambda: validate_cross_repo_validation(authority)),
        ("TV-INDEPENDENCE closure", lambda: validate_independence_closure(authority))
    ]

    all_pass = True
    for name, validator in validators:
        print(f"\n[{name}]")
        if not validator():
            all_pass = False

    print("\n" + "="*60)
    if all_pass:
        print("✓ LINEAGE AUTHORITY VALIDATION PASSED")
        print("  - Authority pyramid: 6 repos")
        print("  - Dedup rules: 4 classes")
        print("  - Lineage ID: immutable schema")
        print("  - Cross-repo validation: 4 gates")
        print("  - TV-INDEPENDENCE: CLOSED")
        return 0
    else:
        print("✗ LINEAGE AUTHORITY VALIDATION FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
