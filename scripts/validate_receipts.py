#!/usr/bin/env python3
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple

REQUIRED_FIELDS = {
    'cycle_id': str,
    'n_mod_42': int,
    'phase': str,
    'decision': str,
    'previous_entry_sha256': str,
    'latest_four_count': int,
    'claim_allowed': bool,
}

VALID_PHASES = {'psi', 'chi', 'rho', 'delta', 'sigma', 'omega'}

def validate_entry(entry: Dict[str, Any], index: int, previous_sha: str = None) -> Tuple[bool, List[str]]:
    """Validate a single receipt entry."""
    issues = []

    # Check all required fields exist
    for field, field_type in REQUIRED_FIELDS.items():
        if field not in entry:
            issues.append(f"Entry {index}: Missing field '{field}'")
        elif not isinstance(entry[field], field_type):
            issues.append(f"Entry {index}: Field '{field}' has wrong type (expected {field_type.__name__}, got {type(entry[field]).__name__})")

    # Validate specific fields
    if 'cycle_id' in entry:
        cycle_id = entry['cycle_id']
        if not isinstance(cycle_id, str) or not cycle_id.startswith('RAF-CYCLE-'):
            issues.append(f"Entry {index}: Invalid cycle_id format: {cycle_id}")

    if 'n_mod_42' in entry:
        n_mod = entry['n_mod_42']
        if not (0 <= n_mod < 42):
            issues.append(f"Entry {index}: n_mod_42 out of range [0, 42): {n_mod}")

    if 'phase' in entry:
        phase = entry['phase']
        if phase not in VALID_PHASES:
            issues.append(f"Entry {index}: Invalid phase '{phase}'. Must be one of {VALID_PHASES}")

    if 'decision' in entry:
        decision = entry['decision']
        if decision != 'EXECUTED_READ_ONLY':
            issues.append(f"Entry {index}: Decision is '{decision}', expected 'EXECUTED_READ_ONLY'")

    if 'latest_four_count' in entry:
        count = entry['latest_four_count']
        if count != 4:
            issues.append(f"Entry {index}: latest_four_count is {count}, expected 4")

    if 'claim_allowed' in entry:
        if entry['claim_allowed'] != False:
            issues.append(f"Entry {index}: claim_allowed is {entry['claim_allowed']}, must be false")

    # Validate hash chain continuity
    if previous_sha and 'previous_entry_sha256' in entry:
        if entry['previous_entry_sha256'] != previous_sha:
            issues.append(f"Entry {index}: Hash chain broken. Expected previous_entry_sha256={previous_sha}, got {entry['previous_entry_sha256']}")

    return len(issues) == 0, issues

def validate_receipt(receipt_path: str) -> Dict[str, Any]:
    """Validate a complete receipt file."""
    result = {
        'file': receipt_path,
        'exists': os.path.exists(receipt_path),
        'valid': False,
        'issues': [],
        'entries_count': 0,
        'entries_valid': True,
        'claim_allowed': None,
        'latest_four_count': None,
        'hash_chain_valid': True,
    }

    if not result['exists']:
        result['issues'].append(f"File not found: {receipt_path}")
        return result

    try:
        with open(receipt_path, 'r') as f:
            receipt = json.load(f)
    except json.JSONDecodeError as e:
        result['issues'].append(f"Invalid JSON: {e}")
        return result
    except Exception as e:
        result['issues'].append(f"Error reading file: {e}")
        return result

    # Validate top-level fields
    if 'claim_allowed' in receipt:
        result['claim_allowed'] = receipt['claim_allowed']
        if receipt['claim_allowed'] != False:
            result['issues'].append(f"Top-level claim_allowed is {receipt['claim_allowed']}, must be false")
    else:
        result['issues'].append("Missing top-level claim_allowed field")

    if 'latest_four_count' in receipt:
        result['latest_four_count'] = receipt['latest_four_count']
        if receipt['latest_four_count'] != 4:
            result['issues'].append(f"Top-level latest_four_count is {receipt['latest_four_count']}, expected 4")
    else:
        result['issues'].append("Missing top-level latest_four_count field")

    # Validate entries
    if 'entries' not in receipt:
        result['issues'].append("Missing 'entries' array in receipt")
        return result

    entries = receipt['entries']
    if not isinstance(entries, list):
        result['issues'].append(f"'entries' is not a list, got {type(entries)}")
        return result

    result['entries_count'] = len(entries)

    previous_sha = None
    for i, entry in enumerate(entries):
        valid, issues = validate_entry(entry, i, previous_sha)
        if not valid:
            result['entries_valid'] = False
            result['issues'].extend(issues)

        # Track hash for chain validation
        if 'entry_sha256' in entry:
            previous_sha = entry['entry_sha256']

    # Check continuity assertions if present
    if 'continuity_assertions' in receipt:
        assertions = receipt['continuity_assertions']
        for key, value in assertions.items():
            if not value:
                result['issues'].append(f"Continuity assertion failed: {key}={value}")
                result['hash_chain_valid'] = False

    # Final validation
    result['valid'] = len(result['issues']) == 0 and result['entries_valid'] and result['hash_chain_valid']

    return result

def main():
    receipts_dir = Path('/home/user/Mapa/data/receipts')
    audits_dir = Path('/home/user/Mapa/data/audits')

    print("=" * 80)
    print("WORKFLOW RUNS RECEIPTS VALIDATION REPORT")
    print("=" * 80)

    # Find and validate receipt files
    receipt_files = list(receipts_dir.glob('rafaelia_adaptive_cycle_latest4*.receipt.json'))

    if not receipt_files:
        print("\nNo receipt files found matching pattern 'rafaelia_adaptive_cycle_latest4*.receipt.json'")
    else:
        print(f"\nFound {len(receipt_files)} receipt file(s):")
        for receipt_file in sorted(receipt_files, reverse=True):
            print(f"\n{'-' * 80}")
            print(f"Receipt File: {receipt_file.name}")
            print(f"{'-' * 80}")

            result = validate_receipt(str(receipt_file))

            print(f"Status: {'✓ VALID' if result['valid'] else '✗ INVALID'}")
            print(f"Entries: {result['entries_count']}")
            print(f"claim_allowed: {result['claim_allowed']}")
            print(f"latest_four_count: {result['latest_four_count']}")

            if result['issues']:
                print(f"\nIssues found ({len(result['issues'])}):")
                for issue in result['issues']:
                    print(f"  - {issue}")
            else:
                print("\nNo issues found - all validations passed!")

    # Check audit files
    audit_files = list(audits_dir.glob('RAFAELIA_ADAPTIVE_CYCLE_LATEST4*.json'))

    if audit_files:
        print(f"\n{'=' * 80}")
        print(f"AUDIT FILES FOUND ({len(audit_files)})")
        print(f"{'=' * 80}")

        for audit_file in sorted(audit_files, reverse=True):
            print(f"\n{'-' * 80}")
            print(f"Audit File: {audit_file.name}")
            print(f"{'-' * 80}")

            try:
                with open(audit_file, 'r') as f:
                    audit = json.load(f)

                print(f"Schema: {audit.get('schema', 'N/A')}")
                print(f"claim_allowed: {audit.get('claim_allowed', 'N/A')}")
                print(f"latest_four_count: {audit.get('latest_four_count', 'N/A')}")

                if 'runs' in audit:
                    print(f"Runs in audit: {len(audit['runs'])}")
                    for run in audit['runs']:
                        print(f"\n  Run {run.get('run_number')} (ID: {run.get('run_id')})")
                        print(f"    cycle_id: {run.get('cycle_id')}")
                        print(f"    n_mod_42: {run.get('n_mod_42')}")
                        print(f"    phase: {run.get('phase')}")
                        print(f"    decision: {run.get('decision')}")
                        print(f"    claim_allowed: {run.get('claim_allowed')}")
                        print(f"    latest_four_count: {run.get('latest_four_count')}")

                        # Validate individual run
                        valid = (
                            run.get('claim_allowed') == False and
                            run.get('latest_four_count') == 4 and
                            run.get('decision') == 'EXECUTED_READ_ONLY' and
                            run.get('phase') in VALID_PHASES and
                            0 <= run.get('n_mod_42', -1) < 42
                        )
                        print(f"    Status: {'✓ VALID' if valid else '✗ INVALID'}")

                if 'observed_relations' in audit:
                    print(f"\nObserved Relations:")
                    relations = audit['observed_relations']
                    print(f"  entry_count_monotonic: {relations.get('entry_count_monotonic')}")
                    print(f"  all_decisions_read_only: {relations.get('all_decisions_read_only')}")
                    print(f"  all_claim_allowed_false: {relations.get('all_claim_allowed_false')}")

            except Exception as e:
                print(f"Error reading audit file: {e}")

    print(f"\n{'=' * 80}")
    print("VALIDATION COMPLETE")
    print(f"{'=' * 80}\n")

if __name__ == '__main__':
    main()
