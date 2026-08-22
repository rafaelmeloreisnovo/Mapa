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
    path = Path(repo_root) / "data" / "control-plane" / "lineage_authority_v1.json"
    if not path.exists():
        print(f"ERROR: lineage_authority_v1.json not found at {path}")
        return None
    with open(path) as f:
        return json.load(f)


def validate_promotion_scope(authority):
    """Fail closed if the schema promotes itself beyond the evidenced control-plane state."""
    scope = authority.get("scope")
    target_scope = authority.get("target_scope")
    if scope != "VERIFICATION_PENDING":
        print(f"ERROR: lineage scope={scope}, expected VERIFICATION_PENDING until certification receipt exists")
        return False
    if target_scope != "FEDERATION_CERTIFIED":
        print(f"ERROR: lineage target_scope={target_scope}, expected FEDERATION_CERTIFIED")
        return False
    print("✓ Promotion scope is fail-closed (VERIFICATION_PENDING → FEDERATION_CERTIFIED target)")
    return True


def validate_authority_pyramid(authority):
    required_repos = {
        "termux-packages", "termux-app-rafacodephi", "mapa",
        "rafpolimata", "rafgittools", "llamarafaelia"
    }
    pyramid = authority.get("authority_pyramid", {})
    found_repos = set(pyramid.keys())
    if found_repos != required_repos:
        print("ERROR: Authority pyramid repos mismatch")
        print(f"  Expected: {required_repos}")
        print(f"  Found: {found_repos}")
        return False
    for repo, spec in pyramid.items():
        for field in ["role", "responsibility", "scope", "immutable_id_type", "independence_claim"]:
            if field not in spec:
                print(f"ERROR: {repo} missing required field: {field}")
                return False
    print("✓ Authority pyramid valid (6 repos)")
    return True


def validate_dedup_rules(authority):
    required_classes = {
        "identical_artifact", "upstream_sync",
        "independent_derivation", "cross_repo_evidence_chain"
    }
    rules = {r["class"] for r in authority.get("dedup_rules", [])}
    if rules != required_classes:
        print("ERROR: Dedup rules mismatch")
        print(f"  Expected: {required_classes}")
        print(f"  Found: {rules}")
        return False
    for rule in authority.get("dedup_rules", []):
        if "proof_required" not in rule or "is_independent" not in rule:
            print(f"ERROR: Rule {rule['class']} missing proof_required or is_independent")
            return False
        rule_class = rule["class"]
        is_independent = rule["is_independent"]
        if rule_class in ["identical_artifact", "upstream_sync"] and is_independent:
            print(f"ERROR: {rule_class} incorrectly marked as independent")
            return False
        if rule_class in ["independent_derivation", "cross_repo_evidence_chain"] and not is_independent:
            print(f"ERROR: {rule_class} incorrectly marked as non-independent")
            return False
    print("✓ Dedup rules valid (4 classes)")
    return True


def validate_lineage_id_schema(authority):
    lineage_spec = authority.get("lineage_id_structure", {})
    for field in ["format", "example", "immutable", "uniqueness", "versioning", "authority_binding"]:
        if field not in lineage_spec:
            print(f"ERROR: lineage_id_structure missing {field}")
            return False
    expected_format = "{repo}:{branch}:{commit}:{path}:{artifact_hash}"
    if lineage_spec["format"] != expected_format:
        print("ERROR: lineage_id format incorrect")
        print(f"  Expected: {expected_format}")
        print(f"  Found: {lineage_spec['format']}")
        return False
    if not lineage_spec["immutable"]:
        print("ERROR: lineage_id_structure must be immutable=true")
        return False
    print("✓ Lineage ID schema valid")
    return True


def validate_cross_repo_validation(authority):
    validation = authority.get("cross_repo_validation", {})
    required_repos = {
        "termux-packages", "termux-app-rafacodephi", "mapa",
        "rafpolimata", "rafgittools", "llamarafaelia"
    }
    if set(validation.get("repos", [])) != required_repos:
        print("ERROR: cross_repo_validation repos mismatch")
        return False
    required_gates = {
        "lineage_chain_closure",
        "authority_non_overlap",
        "dedup_consistency",
        "independence_proof",
        "dependency_graph_acyclic",
    }
    found_gates = set(validation.get("validation_gates", []))
    if found_gates != required_gates:
        print("ERROR: cross_repo_validation gates mismatch")
        print(f"  Expected: {required_gates}")
        print(f"  Found: {found_gates}")
        return False
    print("✓ Cross-repo validation gates defined (5 gates)")
    return True


def validate_independence_closure(authority):
    closure = authority.get("tv_independence_closure", {})
    required_conditions = {
        "status": "CLOSED",
        "authority_pyramid_defined": True,
        "dedup_rules_enumerated": True,
        "lineage_id_schema_specified": True,
        "ready_for_federation_certification": True,
    }
    for key, expected in required_conditions.items():
        actual = closure.get(key)
        if actual != expected:
            print(f"ERROR: tv_independence_closure.{key} = {actual}, expected {expected}")
            return False
    print("✓ TV-INDEPENDENCE closure complete")
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate federated lineage authority")
    parser.add_argument("--check", action="store_true", help="Execute validation check")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    args = parser.parse_args()
    if not args.check:
        print("Usage: python3 validate_lineage_authority.py --check")
        return 0

    authority = load_lineage_authority(args.repo_root)
    if authority is None:
        return 1

    print("Validating lineage authority schema...\n")
    validators = [
        ("Promotion scope", lambda: validate_promotion_scope(authority)),
        ("Authority pyramid", lambda: validate_authority_pyramid(authority)),
        ("Dedup rules", lambda: validate_dedup_rules(authority)),
        ("Lineage ID schema", lambda: validate_lineage_id_schema(authority)),
        ("Cross-repo validation gates", lambda: validate_cross_repo_validation(authority)),
        ("TV-INDEPENDENCE closure", lambda: validate_independence_closure(authority)),
    ]

    all_pass = True
    for name, validator in validators:
        print(f"\n[{name}]")
        if not validator():
            all_pass = False

    print("\n" + "=" * 60)
    if all_pass:
        print("✓ LINEAGE AUTHORITY VALIDATION PASSED")
        print("  - Promotion scope: fail-closed")
        print("  - Authority pyramid: 6 repos")
        print("  - Dedup rules: 4 classes")
        print("  - Lineage ID: immutable schema")
        print("  - Cross-repo validation: 5 gates")
        print("  - TV-INDEPENDENCE: CLOSED")
        return 0

    print("✗ LINEAGE AUTHORITY VALIDATION FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
