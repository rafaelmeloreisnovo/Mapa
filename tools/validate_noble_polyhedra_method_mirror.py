#!/usr/bin/env python3
"""Fail-closed validator for the 2026-08-24 noble-polyhedra method mirror.

This validator checks epistemic/custody boundaries only. It does not validate
Connor Hill's mathematics and does not turn a structural analogy into a claim.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data/geometry/noble_polyhedra_method_mirror_20260824.v1.json"
PROBE = ROOT / "data/evidence/termux_geometry_probe_20260824.v1.json"
RECEIPT = ROOT / "data/receipts/research/noble_polyhedra_method_mirror_20260824.v1.json"
EXPECTED_ARXIV = "2607.28711"

REQUIRED_INVARIANTS = {
    "VISION_NE_ARTIFACT",
    "ARTIFACT_NE_EXECUTION",
    "EXECUTION_NE_EVIDENCE",
    "EVIDENCE_NE_CLAIM",
    "METHOD_MIRROR_NE_MATHEMATICAL_EQUIVALENCE",
    "SEARCH_MISS_NE_ABSENCE",
    "TOKEN_VAZIO_NE_ZERO",
}

FORBIDDEN_PROMOTIONS = {
    "RAFAELIA_ALREADY_CLASSIFIED_NOBLE_POLYHEDRA",
    "HILL_RESULT_VALIDATES_RAFAELIA_THEORIES",
    "RAFAELIA_HAS_146_ANALOGOUS_OBJECTS",
    "RAFAELIA_42_ORBITS_PROVED",
    "INTERNAL_PRIOR_ART_ABSENT",
    "NOVELTY_PROVED",
}


def load(path: Path) -> dict:
    if not path.is_file():
        raise AssertionError(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    try:
        mirror = load(MIRROR)
        probe = load(PROBE)
        receipt = load(RECEIPT)

        require(mirror.get("claim_allowed") is False, "mirror must remain claim_allowed=false")
        require(probe.get("claim_allowed") is False, "probe must remain claim_allowed=false")
        require(receipt.get("claim_allowed") is False, "receipt must remain claim_allowed=false")
        require(mirror.get("relation_scope") == "METHOD_MIRROR_ONLY", "relation scope widened")
        require(mirror.get("external_reference", {}).get("arxiv") == EXPECTED_ARXIV,
                "primary-source arXiv identifier drifted")
        require(f"arXiv:{EXPECTED_ARXIV}" in set(receipt.get("source_boundary", {}).get("primary_external_authorities", [])),
                "custody receipt does not pin corrected arXiv identifier")

        invariants = set(mirror.get("invariants", []))
        require(REQUIRED_INVARIANTS <= invariants, "required anti-regression invariants missing")

        forbidden = set(mirror.get("forbidden_promotions", []))
        require(FORBIDDEN_PROMOTIONS <= forbidden, "forbidden promotion guard weakened")

        archive_a = mirror["internal_sources"]["attached_snapshot"]["sha256"]
        archive_b = probe["source"]["archive_sha256"]
        require(archive_a == archive_b, "archive custody hash mismatch")

        require(probe.get("scoped_verdict") == "PASS_LOCAL_DISCRETE_ROTATION_SELFTEST",
                "runtime receipt verdict changed")
        blocked = set(probe.get("does_not_evidence", []))
        require("noble_polyhedra_classification" in blocked, "classifier non-claim boundary missing")
        require("42_stable_orbits" in blocked, "42-orbit non-claim boundary missing")

        gates = receipt.get("gates", {})
        require(gates.get("method_mirror_only") is True, "method mirror gate not asserted")
        require(gates.get("mathematical_equivalence") is False, "equivalence improperly promoted")
        require(gates.get("novelty") is False, "novelty improperly promoted")
        require(gates.get("noble_polyhedra_classifier_implemented") is False,
                "classifier implementation improperly promoted")

        anomalies = receipt.get("operational_anomalies", [])
        require(any(a.get("id") == "ANOM-API-PROBE-20260824-01" and
                    a.get("postcondition") == "__probe__ ABSENT_ON_MAIN"
                    for a in anomalies), "custody anomaly closure not recorded")
        require(any(a.get("id") == "ANOM-PROVENANCE-ARXIV-ID-20260824-02" and
                    a.get("correct_value") == EXPECTED_ARXIV
                    for a in anomalies), "provenance correction receipt missing")

        gaps = {g.get("id"): g.get("state") for g in mirror.get("gaps", [])}
        require(gaps.get("TV-RAW-CROSS-CORPUS-EXHAUSTIVENESS") == "TOKEN_VAZIO",
                "raw corpus uncertainty must remain TOKEN_VAZIO")
        require(gaps.get("TV-INTERNAL-NOBLE-POLYHEDRA-PRIOR-ART") == "TOKEN_VAZIO",
                "internal prior-art uncertainty must remain TOKEN_VAZIO")
        require(gaps.get("MIRROR-VALIDATOR-EXECUTION-ENV") == "TOKEN_VAZIO_EXECUTION_ENV",
                "validator execution-environment gap must remain explicit until rerun")

    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        return 1

    print("PASS: noble-polyhedra method mirror boundaries intact")
    print(f"primary_arxiv={EXPECTED_ARXIV}")
    print("claim_allowed=false")
    print("scope=METHOD_MIRROR_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
