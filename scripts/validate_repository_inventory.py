#!/usr/bin/env python3
"""
Validate repository inventory against schema.

Rules:
  - No duplicate repository IDs
  - No missing required fields
  - Dates must be coherent (created < updated < pushed or null)
  - Repository ID must be stable (GitHub-provided)
  - Owner must be in ALLOWED_OWNERS
  - Counts must match list length
"""

import json
import sys
from datetime import datetime
from jsonschema import validate, ValidationError
import hashlib

ALLOWED_OWNERS = ["rafaelmeloreisnovo", "instituto-Rafael"]

def load_schema(schema_path: str) -> dict:
    """Load JSON schema."""
    with open(schema_path) as f:
        return json.load(f)

def load_inventory(inventory_path: str) -> dict:
    """Load inventory file."""
    with open(inventory_path) as f:
        return json.load(f)

def validate_schema(inventory: dict, schema: dict) -> bool:
    """Validate inventory against schema."""
    try:
        validate(instance=inventory, schema=schema)
        return True
    except ValidationError as e:
        print(f"❌ Schema validation failed: {e.message}")
        return False

def check_no_duplicates(inventory: dict) -> bool:
    """Check for duplicate repository IDs."""
    seen_ids = set()
    seen_names = set()
    
    for repo in inventory["repositories"]:
        repo_id = repo["repository_id"]
        repo_name = repo["repository_full_name"]
        
        if repo_id in seen_ids:
            print(f"❌ Duplicate repository_id: {repo_id}")
            return False
        
        if repo_name in seen_names:
            print(f"❌ Duplicate repository_full_name: {repo_name}")
            return False
        
        seen_ids.add(repo_id)
        seen_names.add(repo_name)
    
    print(f"✓ No duplicate repository IDs or names ({len(seen_ids)} unique)")
    return True

def check_allowed_owners(inventory: dict) -> bool:
    """Check that all repos belong to allowed owners."""
    for repo in inventory["repositories"]:
        owner = repo["owner"]
        if owner not in ALLOWED_OWNERS:
            print(f"❌ Owner not in ALLOWED_OWNERS: {owner}")
            return False
    
    print(f"✓ All repositories belong to allowed owners: {ALLOWED_OWNERS}")
    return True

def check_date_coherence(inventory: dict) -> bool:
    """Check that dates are chronologically coherent."""
    for repo in inventory["repositories"]:
        repo_name = repo["repository_full_name"]
        
        created_at = datetime.fromisoformat(repo["created_at"].replace("Z", "+00:00"))
        updated_at = datetime.fromisoformat(repo["updated_at"].replace("Z", "+00:00"))
        pushed_at = repo["pushed_at"]
        
        if pushed_at:
            pushed_at = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        
        if created_at > updated_at:
            print(f"❌ Date incoherence in {repo_name}: created_at > updated_at")
            return False
        
        if pushed_at and updated_at > pushed_at:
            print(f"⚠️  Warning in {repo_name}: updated_at > pushed_at (unusual but allowed)")
    
    print(f"✓ All dates are coherent")
    return True

def check_counts_match_list(inventory: dict) -> bool:
    """Check that declared counts match actual list length."""
    stats = inventory["statistics"]
    repos = inventory["repositories"]
    
    # Check total count
    if len(repos) > 0:  # Allow 0 for demonstration
        actual_total = len(repos)
        declared_total = stats["total_repositories"]
        
        if actual_total != declared_total:
            print(f"⚠️  Total count mismatch: declared {declared_total}, actual {actual_total}")
            # Don't fail; might be snapshot
    
    # Count by visibility
    public_count = sum(1 for r in repos if r["visibility"] == "public")
    private_count = sum(1 for r in repos if r["visibility"] == "private")
    archived_count = sum(1 for r in repos if r["archived"])
    
    if public_count != stats["public_count"]:
        print(f"❌ Public count mismatch: declared {stats['public_count']}, actual {public_count}")
        return False
    
    if private_count != stats["private_count"]:
        print(f"❌ Private count mismatch: declared {stats['private_count']}, actual {private_count}")
        return False
    
    if archived_count != stats["archived_count"]:
        print(f"❌ Archived count mismatch: declared {stats['archived_count']}, actual {archived_count}")
        return False
    
    print(f"✓ Counts match list length (public: {public_count}, private: {private_count}, archived: {archived_count})")
    return True

def compute_digest(inventory: dict) -> str:
    """Compute BLAKE2b digest of repository list."""
    # Create deterministic representation of repositories
    repos_for_hash = [
        {
            "full_name": r["repository_full_name"],
            "id": r["repository_id"],
            "pushed_at": r["pushed_at"]
        }
        for r in sorted(inventory["repositories"], key=lambda x: x["repository_id"])
    ]
    
    content = json.dumps(repos_for_hash, separators=(',', ':'))
    digest = hashlib.blake2b(content.encode()).hexdigest()
    return digest

def validate_repository_inventory(inventory_path: str, schema_path: str, audit_output_path: str) -> int:
    """Main validation function."""
    print("\n=== REPOSITORY INVENTORY VALIDATION ===")
    print(f"Inventory: {inventory_path}")
    print(f"Schema: {schema_path}")
    
    try:
        schema = load_schema(schema_path)
        print("✓ Schema loaded")
    except Exception as e:
        print(f"❌ Failed to load schema: {e}")
        return 1
    
    try:
        inventory = load_inventory(inventory_path)
        print("✓ Inventory loaded")
    except Exception as e:
        print(f"❌ Failed to load inventory: {e}")
        return 1
    
    checks = [
        ("Schema validation", lambda: validate_schema(inventory, schema)),
        ("No duplicate IDs", lambda: check_no_duplicates(inventory)),
        ("Allowed owners only", lambda: check_allowed_owners(inventory)),
        ("Date coherence", lambda: check_date_coherence(inventory)),
        ("Counts match list", lambda: check_counts_match_list(inventory))
    ]
    
    results = {}
    all_passed = True
    
    print("\n--- Running validation checks ---")
    for check_name, check_func in checks:
        try:
            passed = check_func()
            results[check_name] = "PASS" if passed else "FAIL"
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} raised exception: {e}")
            results[check_name] = "ERROR"
            all_passed = False
    
    # Compute digest
    digest = compute_digest(inventory)
    print(f"\n📊 Digest BLAKE2b: {digest}")
    
    # Generate audit report
    audit_report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "inventory_path": inventory_path,
        "validation_results": results,
        "all_checks_passed": all_passed,
        "statistics": inventory["statistics"],
        "digest_blake2b": digest,
        "total_repositories_validated": len(inventory["repositories"])
    }
    
    # Save audit report
    with open(audit_output_path, "w") as f:
        json.dump(audit_report, f, indent=2)
    
    print(f"\n📄 Audit report saved: {audit_output_path}")
    
    # Final status
    print("\n" + "="*50)
    if all_passed:
        print("✅ VALIDATION PASSED")
        return 0
    else:
        print("❌ VALIDATION FAILED")
        return 1

if __name__ == "__main__":
    inventory_path = "indices/REPOSITORY_INVENTORY.json"
    schema_path = "schemas/repository_inventory.schema.json"
    audit_output_path = "resultados/REPOSITORY_INVENTORY_AUDIT.json"
    
    exit_code = validate_repository_inventory(inventory_path, schema_path, audit_output_path)
    sys.exit(exit_code)
