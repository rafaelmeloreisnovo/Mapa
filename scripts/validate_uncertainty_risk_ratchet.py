#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data/reconciliation/OMEGA_UNCERTAINTY_RISK_RATCHET_20260829.v1.json"
BASELINE = ROOT / "data/quality/MARKDOWN_DEBT_BASELINE_20260829.v1.json"
CI = ROOT / ".github/workflows/ci.yml"
CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
LEGACY_CHECKOUT_SHA = "11d5960a326750d5838078e36cf38b85af677262"
GOVERNANCE_WORKFLOWS = [
    ROOT / ".github/workflows/main-hardening-gate.yml",
    ROOT / ".github/workflows/promotion-control-v1.yml",
    ROOT / ".github/workflows/server-merge-enforcement-assurance.yml",
]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL: " + message)


def find_front(receipt, front_id):
    return next(x for x in receipt["fronts"] if x["id"] == front_id)


def main() -> None:
    r = load(RECEIPT)
    b = load(BASELINE)
    ci = CI.read_text(encoding="utf-8")

    require(r["claim_allowed"] is False, "claim gate must remain closed")
    require(r["release_allowed"] is False, "release gate must remain closed")
    require(r["promotion_allowed"] is False, "promotion gate must remain closed")

    required_invariants = {
        "VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM",
        "RECENCY != RELEVANCE != AUTHORITY != EVIDENCE",
        "ACADEMIC_STYLE != PEER_REVIEW != REPLICATION != PROOF",
        "TOKEN_VAZIO != 0",
        "FIXTURE != LIVE",
        "HEURISTIC != PROOF",
        "LISTING_MISS != GLOBAL_ABSENCE",
    }
    require(required_invariants.issubset(set(r["core_invariants"])), "core invariant drift")

    successor = r["successor_contract"]
    require(successor["latest_wins"] is False, "recency must never be authority by itself")
    needed = {
        "durable_provenance_pointer",
        "evidence_not_weaker_than_predecessor_or_direct_falsification",
        "declared_falsifier_or_test",
        "relevance_to_the_claim_being_changed",
        "consequence_radius_is_explicit_and_justified",
    }
    require(needed.issubset(set(successor["supersession_requires_all"])), "supersession contract weakened")

    pid = find_front(r, "RAW018_PID_SET_COMMITMENT")
    require(pid["state"] == "REPRODUCED_COMMITMENT", "RAW018 PID commitment state drift")
    require(pid["evidence"]["pid_count"] == 100, "RAW018 PID count drift")
    require(
        pid["evidence"]["set_commitment_sha256"]
        == "766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e",
        "RAW018 PID commitment hash drift",
    )

    chrono = find_front(r, "RAW018_CHRONOLOGICAL_COMMITMENT")
    require(chrono["state"] == "REPRODUCED_COMMITMENT", "RAW018 chronological commitment state drift")
    require(
        chrono["evidence"]["candidate_chronological_commitment_sha256"]
        == "c29cbc493b2401d0d875a49a71999f4b32f8b3faab8a86cd2c1d9a4e4ca83706",
        "RAW018 chronological commitment hash drift",
    )
    require(len(chrono["open_gaps"]) >= 2, "RAW018 hard-custody gaps were silently erased")

    genesis = find_front(r, "GENESIS_SEAL_ROOT_CUSTODY")
    require(genesis["state"] == "CUSTODY_GUARDED", "Genesis Seal custody state drift")
    require(
        genesis["evidence"]["git_blob"] == "b9d3af394b3f32601c51debf285ee1f627343f14",
        "Genesis Seal blob drift",
    )
    require(genesis["evidence"]["size_bytes"] == 3160622, "Genesis Seal size drift")

    debt = find_front(r, "MARKDOWN_HISTORICAL_DEBT")
    require(debt["state"] == "LEGACY_NONBLOCKING_DEBT_RATCHET", "Markdown debt state drift")
    require(b["tool"]["version"] == "0.23.2", "Markdown tool baseline drift")
    require(b["scope"]["issues"] == 890, "Markdown issue ceiling drift")
    require(b["scope"]["files_with_issues"] == 95, "Markdown affected-file ceiling drift")
    require(b["policy"]["mode"] == "RATCHET_NO_INCREASE", "Markdown debt policy drift")

    protected = set(r["protected_unknowns"])
    require("TOKEN_VAZIO_EXACT_CANONICAL_EXECUTABLE_FULL_SCOPE_BINDING" in protected, "MESSAGES exact binding gap erased")
    require("TOKEN_VAZIO_MATRIX_C_IDENTITY" in protected, "Matrix C identity fabricated")
    require("TOKEN_VAZIO_MATRIX_C_FORMULA" in protected, "Matrix C formula fabricated")
    require("TOKEN_VAZIO_ANDROID_PHYSICAL_RUNTIME_RECEIPT" in protected, "physical Android receipt fabricated")

    academic = r["academic_evidence_contract"]
    require(academic["citation_presence_is_proof"] is False, "citation incorrectly promoted to proof")
    require(academic["academic_tone_is_validation"] is False, "academic style incorrectly promoted")
    require(academic["fraud_label_without_specific_evidence_allowed"] is False, "unsupported fraud labeling permitted")

    serialized = json.dumps(r, ensure_ascii=False)
    require("FRAUD_CONFIRMED" not in serialized, "fraud status cannot be asserted without specific adjudicated evidence")
    require("latest_wins\": true" not in serialized, "latest-wins regression")

    require("markdownlint-cli2@0.23.2" in ci, "markdownlint dependency is not pinned")
    require("python3 scripts/check_markdown_debt_ratchet.py" in ci, "Markdown debt ratchet is not wired into general CI")
    require("b9d3af394b3f32601c51debf285ee1f627343f14" in ci, "Genesis Seal guard lost")
    require(CHECKOUT_SHA in ci, "general CI checkout runtime pin drift")

    for workflow in GOVERNANCE_WORKFLOWS:
        text = workflow.read_text(encoding="utf-8")
        require(CHECKOUT_SHA in text, f"{workflow.name}: checkout v7.0.1 exact pin missing")
        require(LEGACY_CHECKOUT_SHA not in text, f"{workflow.name}: legacy Node-20 checkout pin reintroduced")
        require("actions/checkout@v4" not in text, f"{workflow.name}: floating checkout v4 reintroduced")

    print("PASS: uncertainty/risk/evidence authority ratchet v1")


if __name__ == "__main__":
    main()
