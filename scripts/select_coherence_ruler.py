#!/usr/bin/env python3
"""Select the first governed invariant that safely restricts calculation scope."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def load(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def eligible(candidate: Dict[str, Any], control: Dict[str, Any]) -> bool:
    if candidate.get("evidence_class") not in control["evidence_classes"]:
        return False
    if len(candidate.get("support_axes", [])) < int(control["minimum_support_axes"]):
        return False
    if not candidate.get("identity_bound", False):
        return False
    if not candidate.get("scope_declared", False):
        return False
    if not candidate.get("falsifier_defined", False):
        return False
    if not candidate.get("privacy_safe", False):
        return False
    if int(candidate.get("unresolved_contradictions", 0)) != 0:
        return False
    if candidate.get("region") not in control["regions"]:
        return False
    return True


def select_ruler(control: Dict[str, Any], fixture: Dict[str, Any]) -> Dict[str, Any]:
    limits = control["limits"]
    candidates: List[Dict[str, Any]] = list(fixture.get("candidates", []))
    budget = {
        "candidate_evaluations": len(candidates),
        "relation_edges": int(fixture.get("relation_edges", 0)),
        "requested_regions": int(fixture.get("requested_regions", 0)),
    }
    if fixture.get("raw_content_included") is not False:
        return hold(control, budget, "PUBLIC_SAFE_BOUNDARY_FAILED")
    if budget["candidate_evaluations"] > int(limits["candidates"]):
        return hold(control, budget, "CANDIDATE_BUDGET_EXCEEDED")
    if budget["relation_edges"] > int(limits["relations"]):
        return hold(control, budget, "RELATION_BUDGET_EXCEEDED")
    if budget["requested_regions"] > int(limits["regions"]):
        return hold(control, budget, "REGION_BUDGET_EXCEEDED")

    ordered = sorted(candidates, key=lambda c: (int(c.get("priority", 10**9)), str(c.get("id", ""))))
    rejected: List[str] = []
    for candidate in ordered:
        if eligible(candidate, control):
            return {
                "schema": "rafaelia.coherence_ruler_receipt.v1",
                "status": "RULER_FOUND_REGION_RESTRICTED",
                "claim_allowed": False,
                "selected_ruler": candidate["id"],
                "selected_region": candidate["region"],
                "random_total_permutation_sweep_required": False,
                "decision_path": rejected + [candidate["id"]],
                "watchdog_budget": budget,
                "rollback": "OUTPUT_ONLY_NO_AUTONOMOUS_MUTATION",
                "failover": "CONSERVATIVE_HOLD_WITH_TYPED_GAP",
            }
        rejected.append(candidate.get("id", "TOKEN_VAZIO_ID"))
    return hold(control, budget, "NO_GOVERNED_RULER")


def hold(control: Dict[str, Any], budget: Dict[str, int], reason: str) -> Dict[str, Any]:
    return {
        "schema": "rafaelia.coherence_ruler_receipt.v1",
        "status": control.get("fallback", "FAILSAFE_HOLD"),
        "claim_allowed": False,
        "selected_ruler": "TOKEN_VAZIO",
        "selected_region": "TOKEN_VAZIO",
        "random_total_permutation_sweep_required": False,
        "hold_reason": reason,
        "watchdog_budget": budget,
        "rollback": "OUTPUT_ONLY_NO_AUTONOMOUS_MUTATION",
        "failover": "CONSERVATIVE_HOLD_WITH_TYPED_GAP",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--control", default="data/control-plane/coherence-ruler-selector.v1.json")
    parser.add_argument("--input", default="fixtures/coherence_ruler/session_aggregate.v1.json")
    parser.add_argument("--output")
    args = parser.parse_args()

    receipt = select_ruler(load(Path(args.control)), load(Path(args.input)))
    rendered = json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if receipt["status"] == "RULER_FOUND_REGION_RESTRICTED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
