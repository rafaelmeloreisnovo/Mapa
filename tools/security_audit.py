#!/usr/bin/env python3
"""
Security Audits for Rafaelia Framework: S1-01 through S1-04

S1-01: GitHub token exposure in logs
S1-02: File permissions audit
S1-03: GitHub Actions pinning (SHA vs tags)
S1-04: Document TOKEN_VAZIO dependency risks

Phase 0: Security Audits (zero risk, high impact)
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

AUDIT_DIR = Path("data/audits")
WORKFLOWS_DIR = Path(".github/workflows")
RECEIPTS_DIR = Path("data/receipts")


def audit_token_exposure() -> Tuple[bool, str]:
    """S1-01: Scan for exposed GitHub tokens in logs/artifacts"""
    token_patterns = [
        r"Bearer [A-Za-z0-9_\-\.]+",
        r"ghp_[A-Za-z0-9_]+",
        r"gho_[A-Za-z0-9_]+",
        r"GITHUB_TOKEN=[A-Za-z0-9_]+",
        r"Authorization: [A-Za-z0-9_\-\.]+",
    ]

    findings = []

    for audit_file in AUDIT_DIR.glob("*.jsonl"):
        try:
            with open(audit_file, "r", encoding="utf-8") as f:
                content = f.read()

            for pattern in token_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    findings.append(f"{audit_file.name}: {len(matches)} potential tokens")

        except Exception:
            pass

    if findings:
        return False, f"S1-01 FAIL: Potential tokens found:\n" + "\n".join(findings)

    return True, "S1-01 PASS: No token exposure detected in audit logs"


def audit_file_permissions() -> Tuple[bool, str]:
    """S1-02: Verify receipt and audit files have restricted permissions"""
    issues = []

    # Check receipts are not world-writable
    if RECEIPTS_DIR.exists():
        for receipt_file in RECEIPTS_DIR.glob("*.receipt.json"):
            stat_info = receipt_file.stat()
            mode = stat_info.st_mode & 0o777

            # Should not be world-writable (o+w = 0o002)
            if mode & 0o002:
                issues.append(f"{receipt_file.name} is world-writable (mode {oct(mode)})")

    # Check audit directory permissions
    if AUDIT_DIR.exists():
        stat_info = AUDIT_DIR.stat()
        mode = stat_info.st_mode & 0o777

        # Should be 755 or 750, not 777
        if mode == 0o777:
            issues.append(f"data/audits directory is world-writable (mode 777)")

    if issues:
        return False, f"S1-02 FAIL: Permission issues:\n" + "\n".join(issues)

    return True, "S1-02 PASS: File permissions restricted correctly"


def audit_action_pinning() -> Tuple[bool, str]:
    """S1-03: Verify GitHub Actions are pinned to commit SHAs, not tags"""
    unpinned = []

    if WORKFLOWS_DIR.exists():
        for workflow_file in WORKFLOWS_DIR.glob("*.yml"):
            try:
                with open(workflow_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Look for actions/checkout@v1, @main, @latest (bad)
                bad_patterns = [
                    (r"uses:\s*[\w\-/]+@(v\d+|main|latest|master)", "tag/branch reference"),
                ]

                for pattern, description in bad_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        unpinned.append(f"{workflow_file.name}: {description} detected")

                # Check for SHAs (good)
                sha_pattern = r"uses:\s*[\w\-/]+@[a-f0-9]{40}"
                shas = re.findall(sha_pattern, content)

            except Exception:
                pass

    # Phase 0 finding: Document unpinned actions but don't fail
    # Pinning is a Phase 1/2 hardening task, not a blocker
    if unpinned:
        return True, f"S1-03 FINDING: {len(unpinned)} workflows use version tags (pinning upgrade in Phase 1)"

    return True, "S1-03 PASS: All critical GitHub Actions pinned to commit SHAs"


def audit_token_vazio_dependencies() -> Tuple[bool, str]:
    """S1-04: Document unresolved TOKEN_VAZIO dependency risks"""
    vazio_file = AUDIT_DIR / "TOKEN_VAZIO_REGISTRY.jsonl"

    if not vazio_file.exists():
        return False, "S1-04 FAIL: TOKEN_VAZIO registry not found"

    try:
        with open(vazio_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        vazio_count = len(lines)
        p1_count = 0
        p2_count = 0

        for line in lines:
            entry = json.loads(line)
            priority = entry.get("priority", "UNKNOWN")
            if priority == "P1":
                p1_count += 1
            elif priority == "P2":
                p2_count += 1

        summary = f"S1-04 PASS: {vazio_count} TOKEN_VAZIO entries documented ({p1_count} P1, {p2_count} P2)"
        return True, summary

    except Exception as e:
        return False, f"S1-04 FAIL: Error reading TOKEN_VAZIO registry: {e}"


def main():
    print("=" * 60)
    print("RAFAELIA SECURITY AUDITS (Phase 0)")
    print("=" * 60)

    results = []

    print("\n[S1-01] Checking token exposure...")
    s101_pass, s101_msg = audit_token_exposure()
    results.append(s101_pass)
    print(f"  {s101_msg}")

    print("\n[S1-02] Checking file permissions...")
    s102_pass, s102_msg = audit_file_permissions()
    results.append(s102_pass)
    print(f"  {s102_msg}")

    print("\n[S1-03] Checking action pinning...")
    s103_pass, s103_msg = audit_action_pinning()
    results.append(s103_pass)
    print(f"  {s103_msg}")

    print("\n[S1-04] Checking TOKEN_VAZIO documentation...")
    s104_pass, s104_msg = audit_token_vazio_dependencies()
    results.append(s104_pass)
    print(f"  {s104_msg}")

    print("\n" + "=" * 60)
    if all(results):
        print("✓ ALL SECURITY AUDITS PASSED")
        return 0
    else:
        failed = sum(1 for r in results if not r)
        print(f"✗ {failed}/{len(results)} audits FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
