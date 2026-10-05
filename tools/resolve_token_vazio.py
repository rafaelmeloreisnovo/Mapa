#!/usr/bin/env python3
"""TOKEN_VAZIO legacy decision tool, hardened fail-closed.

This tool may list/show gaps and append PRESERVED or
REJECTED_INSUFFICIENT_EVIDENCE decisions. Direct APPROVED_CLOSED is blocked:
closure now requires a dedicated falsifiable readiness/evidence path and an
explicit independent approval boundary.

The block is intentional. CONTRACT_READY != EXECUTED != CLOSED.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


DIRECT_CLOSE_BLOCK_REASON = (
    "APPROVED_CLOSED is disabled in this legacy tool. "
    "Use the TOKEN_VAZIO closure-readiness/evidence gate; preserve the gap "
    "until source, authority, execution, evidence, uncertainty and independent "
    "approval are explicitly bound."
)


def load_registry(registry_path: Path) -> List[Dict]:
    """Load TOKEN_VAZIO_REGISTRY.jsonl."""
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
    """Load append-only decisions, keyed by TOKEN_VAZIO id."""
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
    """List documented TOKEN_VAZIO entries."""
    print("\n" + "=" * 80)
    print("TOKEN_VAZIO REGISTRY - All Documented Gaps")
    print("=" * 80)

    by_priority = {}
    for entry in registry:
        priority = entry.get("priority", "UNKNOWN")
        by_priority.setdefault(priority, []).append(entry)

    for priority in ["P0", "P1", "P2"]:
        if priority in by_priority:
            print(f"\n{priority} Entries:")
            for entry in by_priority[priority]:
                gap_id = entry.get("id", "UNKNOWN")
                status = entry.get("current_status", "UNKNOWN")
                severity = entry.get("severity", "unknown")
                print(f"  - {gap_id}")
                print(f"    Status: {status}")
                print(f"    Severity: {severity}")


def show_gap(gap_id: str, registry: List[Dict], decisions: Dict[str, Dict]) -> None:
    """Show detailed information about a specific gap."""
    gap = next((entry for entry in registry if entry.get("id") == gap_id), None)
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
    print("\nAffected Components:")
    for component in gap.get("affected_components", []):
        print(f"  - {component}")

    if gap_id in decisions:
        decision = decisions[gap_id]
        print("\n** APPROVAL DECISION RECORDED **")
        print(f"Decision: {decision.get('decision', 'UNKNOWN')}")
        print(f"Approved by: {decision.get('approved_by', 'N/A')}")
        print(f"Timestamp: {decision.get('timestamp', 'N/A')}")
        print(f"Phase: {decision.get('phase', 'N/A')}")
    else:
        print("\n** NO APPROVAL DECISION YET **")
        print("This gap requires:")
        print("  1. explicit closure-readiness contract")
        print("  2. source-bound evidence and falsifier execution")
        print("  3. uncertainty/reproducibility boundary")
        print("  4. independent authorized approval")
        print("Direct closure through this legacy tool is disabled.")


def record_decision(
    gap_id: str,
    decision: str,
    decisions_path: Path,
    approved_by: str,
    evidence_package: Optional[Dict] = None,
    notes: Optional[str] = None,
) -> bool:
    """Append a non-closing governance decision.

    APPROVED_CLOSED is deliberately rejected here so a legacy convenience path
    cannot bypass the closure-readiness and evidence boundaries.
    """
    valid_decisions = [
        "APPROVED_CLOSED",
        "APPROVED_PRESERVED",
        "REJECTED_INSUFFICIENT_EVIDENCE",
    ]
    if decision not in valid_decisions:
        print(f"ERROR: Invalid decision. Must be one of: {valid_decisions}", file=sys.stderr)
        return False
    if decision == "APPROVED_CLOSED":
        print(f"ERROR: {DIRECT_CLOSE_BLOCK_REASON}", file=sys.stderr)
        return False
    if not approved_by or not approved_by.strip():
        print("ERROR: --approved-by must be explicit; no automated default approver is allowed", file=sys.stderr)
        return False
    if notes and len(notes) > 500:
        print("ERROR: --notes exceeds 500 characters", file=sys.stderr)
        return False

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "token_vazio_id": gap_id,
        "decision": decision,
        "approved_by": approved_by.strip(),
        "evidence_package": evidence_package or {},
        "resolution_notes": notes or "",
        "phase": "TOKEN_VAZIO_LEGACY_FAIL_CLOSED_V1",
        "claim_allowed": False,
    }

    decisions_path.parent.mkdir(parents=True, exist_ok=True)
    with open(decisions_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")

    print(f"Decision recorded for {gap_id}: {decision}")
    return True


def main(argv=None):
    p = argparse.ArgumentParser(
        description="TOKEN_VAZIO legacy decision tool - fail-closed for direct closure"
    )
    p.add_argument(
        "--action", required=True, choices=["list", "show", "approve"], help="Action to perform"
    )
    p.add_argument("--gap-id", help="TOKEN_VAZIO gap identifier (for show/approve actions)")
    p.add_argument(
        "--decision",
        help="Decision (APPROVED_PRESERVED or REJECTED_INSUFFICIENT_EVIDENCE; direct APPROVED_CLOSED is blocked)",
    )
    p.add_argument(
        "--approved-by",
        help="Explicit identity/authority recording the non-closing decision",
        default=None,
    )
    p.add_argument("--notes", help="Decision notes (max 500 chars)")
    p.add_argument(
        "--repo-root", default="/home/user/Mapa", help="Repository root directory"
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

    if ns.action == "show":
        if not ns.gap_id:
            print("ERROR: --gap-id required for show action", file=sys.stderr)
            return 1
        show_gap(ns.gap_id, registry, decisions)
        return 0

    if ns.action == "approve":
        if not ns.gap_id or not ns.decision:
            print("ERROR: --gap-id and --decision required for approve action", file=sys.stderr)
            return 1
        if not ns.approved_by:
            print("ERROR: --approved-by is required; automated default approval is forbidden", file=sys.stderr)
            return 1

        evidence_package = {"notes": ns.notes} if ns.notes else None
        ok = record_decision(
            ns.gap_id,
            ns.decision,
            decisions_path,
            ns.approved_by,
            evidence_package,
            ns.notes,
        )
        return 0 if ok else 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
