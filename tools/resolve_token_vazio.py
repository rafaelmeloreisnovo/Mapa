#!/usr/bin/env python3
"""
TOKEN_VAZIO Approval Decision Tool

Manages the 3-gate approval workflow for closing documented gaps (TOKEN_VAZIO entries).

Phases:
  GATE 1: Evidence Gathering (Lane 04 prepares artifacts)
  GATE 2: Validation (Lane 04 confirms falsifiers pass)
  GATE 3: Approval (Lane 00 authorizes closure or preservation)

Usage:
  python tools/resolve_token_vazio.py --action list
  python tools/resolve_token_vazio.py --action show --gap-id TOKEN_VAZIO_ID
  python tools/resolve_token_vazio.py --action approve --gap-id TOKEN_VAZIO_ID --decision APPROVED_CLOSED
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


def load_registry(registry_path: Path) -> List[Dict]:
    """Load TOKEN_VAZIO_REGISTRY.jsonl"""
    entries = []
    if not registry_path.exists():
        print(f"ERROR: Registry not found: {registry_path}", file=sys.stderr)
        return entries

    with open(registry_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    return entries


def load_decisions(decisions_path: Path) -> Dict[str, Dict]:
    """Load TOKEN_VAZIO_APPROVAL_DECISIONS.jsonl into dict keyed by gap_id"""
    decisions = {}
    if not decisions_path.exists():
        return decisions

    with open(decisions_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                try:
                    entry = json.loads(line)
                    gap_id = entry.get("token_vazio_id")
                    if gap_id:
                        decisions[gap_id] = entry
                except json.JSONDecodeError:
                    pass

    return decisions


def list_gaps(registry: List[Dict]) -> None:
    """List all TOKEN_VAZIO entries with status"""
    print("\n" + "=" * 80)
    print("TOKEN_VAZIO REGISTRY - All Documented Gaps")
    print("=" * 80)

    by_priority = {}
    for entry in registry:
        priority = entry.get("priority", "UNKNOWN")
        if priority not in by_priority:
            by_priority[priority] = []
        by_priority[priority].append(entry)

    for priority in ["P0", "P1", "P2"]:
        if priority in by_priority:
            print(f"\n{priority} Entries:")
            for entry in by_priority[priority]:
                gap_id = entry.get("id", "UNKNOWN")
                status = entry.get("current_status", "UNKNOWN")
                severity = entry.get("severity", "unknown")
                print(f"  ✓ {gap_id}")
                print(f"    Status: {status}")
                print(f"    Severity: {severity}")


def show_gap(gap_id: str, registry: List[Dict], decisions: Dict[str, Dict]) -> None:
    """Show detailed information about a specific gap"""
    gap = None
    for entry in registry:
        if entry.get("id") == gap_id:
            gap = entry
            break

    if not gap:
        print(f"ERROR: Gap not found: {gap_id}", file=sys.stderr)
        return

    print("\n" + "=" * 80)
    print(f"TOKEN_VAZIO: {gap_id}")
    print("=" * 80)
    print(f"Priority: {gap.get('priority', 'UNKNOWN')}")
    print(f"Severity: {gap.get('severity', 'unknown')}")
    print(f"Description: {gap.get('description', 'N/A')}")
    print(f"Current Status: {gap.get('current_status', 'UNKNOWN')}")
    print(f"Approval Gate: {gap.get('approval_gate', 'N/A')}")
    print(f"Resolution Date Estimate: {gap.get('resolution_date_estimate', 'N/A')}")
    print(f"\nAffected Components:")
    for component in gap.get("affected_components", []):
        print(f"  - {component}")

    # Show approval decision if exists
    if gap_id in decisions:
        decision = decisions[gap_id]
        print(f"\n** APPROVAL DECISION RECORDED **")
        print(f"Decision: {decision.get('decision', 'UNKNOWN')}")
        print(f"Approved by: {decision.get('approved_by', 'N/A')}")
        print(f"Timestamp: {decision.get('timestamp', 'N/A')}")
        print(f"Phase: {decision.get('phase', 'N/A')}")
    else:
        print(f"\n** NO APPROVAL DECISION YET **")
        print("This gap requires:")
        print("  1. GATE 1: Evidence gathering (Lane 04 prepares artifacts)")
        print("  2. GATE 2: Validation (Lane 04 confirms falsifiers pass)")
        print("  3. GATE 3: Approval (Lane 00 authorizes closure)")


def record_decision(
    gap_id: str,
    decision: str,
    decisions_path: Path,
    approved_by: str,
    evidence_package: Optional[Dict] = None,
    notes: Optional[str] = None,
) -> bool:
    """Record approval decision (append-only)"""

    valid_decisions = [
        "APPROVED_CLOSED",
        "APPROVED_PRESERVED",
        "REJECTED_INSUFFICIENT_EVIDENCE",
    ]

    if decision not in valid_decisions:
        print(f"ERROR: Invalid decision. Must be one of: {valid_decisions}", file=sys.stderr)
        return False

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "token_vazio_id": gap_id,
        "decision": decision,
        "approved_by": approved_by,
        "evidence_package": evidence_package or {},
        "resolution_notes": notes or "",
        "phase": "Phase 2-P1-03",
    }

    # Append to JSONL (append-only)
    decisions_path.parent.mkdir(parents=True, exist_ok=True)
    with open(decisions_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")

    print(f"✓ Decision recorded for {gap_id}: {decision}")
    return True


def main(argv=None):
    p = argparse.ArgumentParser(
        description="TOKEN_VAZIO Approval Decision Tool - Manage documented gaps"
    )
    p.add_argument(
        "--action",
        required=True,
        choices=["list", "show", "approve"],
        help="Action to perform",
    )
    p.add_argument(
        "--gap-id",
        help="TOKEN_VAZIO gap identifier (for show/approve actions)",
    )
    p.add_argument(
        "--decision",
        help="Approval decision (APPROVED_CLOSED, APPROVED_PRESERVED, REJECTED_INSUFFICIENT_EVIDENCE)",
    )
    p.add_argument(
        "--approved-by",
        help="Identity of approver (e.g., Lane 00 / Governance)",
        default="Claude Code (Rafaelia Framework Validator)",
    )
    p.add_argument(
        "--notes",
        help="Decision notes (max 500 chars)",
    )
    p.add_argument(
        "--repo-root",
        default="/home/user/Mapa",
        help="Repository root directory",
    )

    ns = p.parse_args(argv)
    repo_root = Path(ns.repo_root)
    registry_path = repo_root / "data" / "audits" / "TOKEN_VAZIO_REGISTRY.jsonl"
    decisions_path = repo_root / "data" / "audits" / "TOKEN_VAZIO_APPROVAL_DECISIONS.jsonl"

    registry = load_registry(registry_path)
    decisions = load_decisions(decisions_path)

    if ns.action == "list":
        if not registry:
            print("ERROR: No gaps found in registry")
            return 2
        list_gaps(registry)
        return 0

    elif ns.action == "show":
        if not ns.gap_id:
            print("ERROR: --gap-id required for show action", file=sys.stderr)
            return 1
        show_gap(ns.gap_id, registry, decisions)
        return 0

    elif ns.action == "approve":
        if not ns.gap_id or not ns.decision:
            print("ERROR: --gap-id and --decision required for approve action", file=sys.stderr)
            return 1

        evidence_package = None
        if ns.notes:
            evidence_package = {"notes": ns.notes}

        if record_decision(
            ns.gap_id,
            ns.decision,
            decisions_path,
            ns.approved_by,
            evidence_package,
            ns.notes,
        ):
            return 0
        else:
            return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
