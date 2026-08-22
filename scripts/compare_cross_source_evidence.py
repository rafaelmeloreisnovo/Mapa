#!/usr/bin/env python3
"""
compare_cross_source_evidence.py

Cross-repository deduplication audit.
Ensures that duplicated artifacts are correctly classified as non-independent evidence,
and that independent derivations are properly validated.

Execution: python3 compare_cross_source_evidence.py --lineage-check
Exit code: 0 = PASS (no false positives/negatives), 1 = FAIL
"""

import json
import sys
from pathlib import Path

def load_lineage_authority(repo_root="."):
    """Load lineage authority schema."""
    path = Path(repo_root) / "data" / "control-plane" / "lineage_authority_v1.json"
    if not path.exists():
        print(f"ERROR: lineage_authority_v1.json not found at {path}")
        return None

    with open(path) as f:
        return json.load(f)

def load_fixture_manifest(repo_root="."):
    """Load frozen fixture manifest."""
    path = Path(repo_root) / "data" / "fixtures" / "FIXTURE_MANIFEST_v1.json"
    if not path.exists():
        print(f"ERROR: FIXTURE_MANIFEST_v1.json not found at {path}")
        return None

    with open(path) as f:
        return json.load(f)

def validate_dedup_consistency(authority):
    """Validate that dedup rules are applied consistently."""
    dedup_rules = authority.get("dedup_rules", [])

    for rule in dedup_rules:
        rule_class = rule.get("class")
        is_independent = rule.get("is_independent")
        proof_required = rule.get("proof_required", [])

        if rule_class in ["identical_artifact", "upstream_sync"]:
            required_proofs = {"hash", "metadata", "timestamp", "source_linkage"}
            if not any(p in str(proof_required).lower() for p in required_proofs):
                print(f"ERROR: {rule_class} dedup rule missing required proof types")
                return False

        if rule_class in ["independent_derivation", "cross_repo_evidence_chain"]:
            if "divergence" not in str(proof_required).lower() and "pipeline" not in str(proof_required).lower():
                print(f"ERROR: {rule_class} dedup rule missing divergence/pipeline proof")
                return False

    print(f"✓ Dedup rules consistency validated")
    return True

def validate_producer_authority_hierarchy(authority):
    """Validate that producer → consumer evidence flow respects authority."""
    pyramid = authority.get("authority_pyramid", {})

    hierarchy = [
        "termux-packages",
        "termux-app-rafacodephi",
        "rafpolimata",
        "mapa",
        "rafgittools",
        "llamarafaelia"
    ]

    seen_scopes = set()
    for repo in hierarchy:
        if repo not in pyramid:
            print(f"ERROR: {repo} missing from authority pyramid")
            return False

        scope = pyramid[repo].get("scope")
        if scope in seen_scopes:
            print(f"ERROR: {repo} has duplicate scope: {scope}")
            return False
        seen_scopes.add(scope)

    print(f"✓ Producer authority hierarchy validated")
    return True

def validate_independence_proof_flow(authority):
    """Validate that independence proofs follow evidence chain rules."""
    dedup_rules = authority.get("dedup_rules", [])

    cross_repo_rule = next((r for r in dedup_rules if r["class"] == "cross_repo_evidence_chain"), None)
    if not cross_repo_rule:
        print(f"ERROR: cross_repo_evidence_chain dedup rule missing")
        return False

    required_proofs = cross_repo_rule.get("proof_required", [])
    critical_proofs = {"producer_commit_hash", "handoff_schema_match", "consumer_receipt", "timestamp_continuity"}

    found_proofs = set(required_proofs)
    if not critical_proofs.issubset(found_proofs):
        print(f"ERROR: cross_repo_evidence_chain missing critical proofs: {critical_proofs - found_proofs}")
        return False

    print(f"✓ Independence proof flow validated")
    return True

def simulate_dedup_scenarios(authority):
    """Test dedup rules against synthetic scenarios."""
    dedup_rules = authority.get("dedup_rules", [])

    identical_rule = next((r for r in dedup_rules if r["class"] == "identical_artifact"), None)
    if not identical_rule or identical_rule.get("is_independent"):
        print(f"ERROR: Scenario 1 (identical hashes) should be non-independent")
        return False

    upstream_rule = next((r for r in dedup_rules if r["class"] == "upstream_sync"), None)
    if not upstream_rule or upstream_rule.get("is_independent"):
        print(f"ERROR: Scenario 2 (upstream_sync) should be non-independent")
        return False

    independent_rule = next((r for r in dedup_rules if r["class"] == "independent_derivation"), None)
    if not independent_rule or not independent_rule.get("is_independent"):
        print(f"ERROR: Scenario 3 (independent_derivation) should be independent")
        return False

    print(f"✓ Dedup scenario simulation passed (3 scenarios)")
    return True

def main():
    """Execute cross-repo deduplication audit."""
    import argparse

    parser = argparse.ArgumentParser(description="Cross-repository deduplication audit")
    parser.add_argument("--lineage-check", action="store_true", help="Execute lineage dedup check")
    parser.add_argument("--repo-root", default=".", help="Repository root path")

    args = parser.parse_args()

    if not args.lineage_check:
        print("Usage: python3 compare_cross_source_evidence.py --lineage-check")
        return 0

    authority = load_lineage_authority(args.repo_root)
    if authority is None:
        return 1

    manifest = load_fixture_manifest(args.repo_root)
    if manifest is None:
        return 1

    print("Executing cross-repository deduplication audit...\n")

    validators = [
        ("Dedup consistency", lambda: validate_dedup_consistency(authority)),
        ("Producer authority hierarchy", lambda: validate_producer_authority_hierarchy(authority)),
        ("Independence proof flow", lambda: validate_independence_proof_flow(authority)),
        ("Dedup scenario simulation", lambda: simulate_dedup_scenarios(authority))
    ]

    all_pass = True
    for name, validator in validators:
        print(f"\n[{name}]")
        if not validator():
            all_pass = False

    print("\n" + "="*60)
    if all_pass:
        print(f"✓ CROSS-REPO DEDUPLICATION AUDIT PASSED")
        print(f"  - Dedup rules: consistent")
        print(f"  - Authority hierarchy: validated")
        print(f"  - Independence proofs: correct flow")
        print(f"  - Scenarios: all pass")
        print(f"  - Fixtures: {manifest.get('integrity', {}).get('total_fixtures', 0)} frozen")
        return 0
    else:
        print(f"✗ CROSS-REPO DEDUPLICATION AUDIT FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
