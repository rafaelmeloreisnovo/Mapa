#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/gaps/open_work_execution_contract.delta.20260808.v2.json"

EXPECTED_TRANSITIONS = {
    "TOKEN_VAZIO_ACT_DR6_CMBONLY_MATERIALIZATION_REPRODUCTION": "TOKEN_VAZIO_ACT_DR6_LCDM_POSTERIOR_CHAIN_REPRODUCTION",
    "TOKEN_VAZIO_H0_RD_FULL_BOLTZMANN_REPRODUCTION": "TOKEN_VAZIO_H0_RD_FULL_BOLTZMANN_INFERENCE_INTEGRATION",
    "TOKEN_VAZIO_NOT_YET_CLASSIFIED_ALL_582_REFS": "TOKEN_VAZIO_DIVERGED_OR_DESCENDANT_REF_SEMANTIC_REVIEW",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def validate(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "rafaelia.open_work_execution_contract_delta.v2":
        fail("unexpected schema")
    if data.get("append_only") is not True:
        fail("delta must be append-only")
    if data.get("claim_allowed") is not False or data.get("automatic_merge") is not False:
        fail("claim/merge boundary violated")
    if data.get("predecessor") != "data/gaps/open_work_execution_contract.20260808.v1.json":
        fail("V1 predecessor must remain explicit")

    boundary = data.get("authority_boundary", {})
    if boundary.get("rll_lab_v2_observed") is not True:
        fail("lab V2 observation missing")
    if boundary.get("rll_release_v2_promoted") is not False or boundary.get("rll_main_v2_promoted") is not False:
        fail("lab evidence cannot be promoted to release/main by this delta")
    if boundary.get("release_authority_mutated_by_this_delta") is not False:
        fail("delta cannot mutate release authority")

    counts = data.get("counts", {})
    if counts.get("release_authoritative_open_tokens") != 14 or counts.get("lab_v2_open_tokens") != 14:
        fail("open-token denominator changed unexpectedly")
    frozen = counts.get("frozen_diverged_ref_cohort")
    equivalent = counts.get("patch_equivalent_refs")
    unique = counts.get("unique_patch_semantic_review_refs")
    if (frozen, equivalent, unique) != (35, 3, 32) or equivalent + unique != frozen:
        fail("ref cohort accounting mismatch")

    rows = data.get("transitions")
    if not isinstance(rows, list) or len(rows) != 3:
        fail("exactly three successor transitions required")
    observed = {}
    for row in rows:
        predecessor = row.get("predecessor_token")
        successor = row.get("successor_token")
        if predecessor in observed:
            fail("duplicate predecessor transition")
        observed[predecessor] = successor
        if row.get("successor_state") != "OPEN_INTERNAL":
            fail(f"{successor}: successor must remain OPEN_INTERNAL")
        if not isinstance(row.get("boundary"), str) or not row["boundary"].strip():
            fail(f"{predecessor}: missing epistemic boundary")
    if observed != EXPECTED_TRANSITIONS:
        fail("transition set mismatch")

    source = data.get("source", {})
    if source.get("lab_pr") != 691 or source.get("lab_merge_commit") != "512bf1f65191d4581b05918e70d0768c5955597e":
        fail("RLL lab authority mismatch")
    if source.get("ci_harness_successor_pr") != 694:
        fail("post-691 harness successor must be recorded")

    return {
        "state": "PASS",
        "claim_allowed": False,
        "release_authority_mutated": False,
        "lab_open_tokens": 14,
        "transitions": 3,
        "unique_patch_semantic_review_refs": 32,
    }


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT
    try:
        result = validate(path)
    except Exception as exc:
        print(json.dumps({"state": "FAIL", "error": f"{type(exc).__name__}: {exc}"}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
