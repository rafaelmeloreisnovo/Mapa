#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/control-plane/HUMAN_DIGNITY_ETHICS_RATCHET_V1.json"
NORMATIVE = ROOT / "data/control-plane/NORMATIVE_ROUTING_REGISTRY_V1.json"
DOC = ROOT / "docs/governance/CAMINHOS_DA_LUZ_HUMAN_DIGNITY_ETHICS_BY_DESIGN_V1.md"


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def main():
    p = json.loads(POLICY.read_text(encoding="utf-8"))
    n = json.loads(NORMATIVE.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    require(p["claim_allowed"] is False, "policy must not self-promote to claim")
    require(p["promotion_allowed"] is False, "policy must not self-promote")
    require(p["release_allowed_from_this_artifact_alone"] is False, "policy cannot release by itself")
    require(p["autonomous_human_value_decision_allowed"] is False, "autonomous human-value decision enabled")
    require(p["single_actor_final_authority_for_high_impact"] is False, "single-actor high-impact authority enabled")

    invariants = set(p["core_invariants"])
    required_invariants = {
        "PERSON != RESOURCE != TOKEN != DATASET != COST_FUNCTION",
        "HUMAN_DIGNITY > EFFICIENCY",
        "TOKEN_VAZIO != PASS",
        "UNKNOWN_RISK != SAFE",
        "NO_AUDITOR_FINDING != PROVEN_ABSENCE",
        "MODEL_RECOMMENDATION != HUMAN_VALUE_DECISION",
        "AVERAGE_WELFARE != PROTECTION_OF_EACH_GROUP",
        "VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM",
    }
    require(required_invariants.issubset(invariants), "core human-protection invariant drift")

    domains = set(p["protected_domains"])
    required_domains = {
        "children_and_adolescents",
        "health_and_mental_health",
        "education",
        "privacy_and_personal_data",
        "civil_and_human_rights",
        "culture_and_belief",
        "accessibility_and_disability",
        "environment_and_ecosystem",
        "humanitarian_contexts",
    }
    require(required_domains.issubset(domains), "protected domain removed")

    child = p["hard_gates"]["child_best_interest"]
    require(child["required"] is True, "child best-interest gate disabled")
    require(child["optimization_weight_allowed"] is False, "child protection converted to tunable weight")
    require(child["final_exclusively_algorithmic_decision_allowed"] is False, "exclusive algorithmic child decision enabled")

    impact = p["hard_gates"]["high_impact_decision"]
    for key in (
        "plural_human_review_required",
        "appeal_required",
        "rollback_or_mitigation_required",
        "consequence_radius_required",
        "affected_group_voice_required",
    ):
        require(impact[key] is True, f"high-impact protection weakened: {key}")

    privacy = p["hard_gates"]["privacy"]
    for key in (
        "data_minimization_required",
        "purpose_limitation_required",
        "sensitive_data_default_hold",
        "retention_must_be_justified",
    ):
        require(privacy[key] is True, f"privacy protection weakened: {key}")

    uncertainty = p["hard_gates"]["uncertainty"]
    require(uncertainty["unknown_must_remain_typed"] is True, "unknowns may be erased")
    require(uncertainty["unknown_may_not_be_coerced_to_zero_false_or_safe"] is True, "unknown coercion enabled")
    require(uncertainty["higher_uncertainty_and_higher_impact_reduces_automation_authority"] is True, "uncertainty no longer reduces automation authority")

    culture = p["hard_gates"]["culture_and_belief"]
    require(culture["identity_ranking_allowed"] is False, "identity ranking enabled")
    require(culture["belief_truth_scoring_for_personal_worth_allowed"] is False, "belief/personal-worth scoring enabled")

    ratchet = p["risk_ratcheting"]
    require(ratchet["latest_wins"] is False, "latest-wins regression")
    require(ratchet["silent_default_to_safe"] is False, "unknown silently defaults to safe")
    needed = {
        "durable_provenance_pointer",
        "evidence_not_weaker_than_predecessor_or_direct_falsification",
        "declared_falsifier_or_test",
        "human_impact_assessment_when_scope_expands",
        "consequence_radius_is_explicit",
        "rollback_or_mitigation_path",
        "no_loss_of_child_privacy_dignity_or_appeal_protection",
    }
    require(needed.issubset(set(ratchet["supersession_requires_all"])), "supersession contract weakened")

    cross = p["cross_repo_rule"]
    require(cross["local_pass_implies_human_impact_pass"] is False, "local technical PASS promoted to ethics PASS")
    require(cross["technical_correctness_implies_ethics"] is False, "technical correctness promoted to ethics")
    require(cross["scientific_novelty_implies_social_permission"] is False, "novelty promoted to social permission")
    require(cross["performance_gain_may_override_hard_rights"] is False, "performance allowed to override hard rights")

    open_gaps = set(p["open_gaps"])
    require("TOKEN_VAZIO_INDEPENDENT_HUMAN_RIGHTS_REVIEW" in open_gaps, "independent human-rights review gap fabricated closed")
    require("TOKEN_VAZIO_CHILD_SAFETY_DOMAIN_REVIEW_FOR_APPLICABLE_PRODUCTS" in open_gaps, "child-safety domain review gap fabricated closed")

    # Normative routing is versioned, authoritative-source based, and never self-certifying.
    require(n["schema"] == "rafaelia.normative_routing_registry.v1", "normative registry schema drift")
    require(n["claim_allowed"] is False, "normative registry self-promoted to claim")
    require(n["certification_claimed"] is False, "normative registry claims certification")
    require(n["legal_opinion_claimed"] is False, "normative registry claims legal opinion")
    require(n["rule"] == "NORMATIVE_ALIGNMENT != CERTIFICATION", "normative alignment/certification boundary weakened")

    entries = n["entries"]
    ids = {entry["id"] for entry in entries}
    required_normative_ids = {
        "NORM-UDHR-1948",
        "NORM-UNESCO-AI-ETHICS-2021",
        "NORM-UNICEF-AI-CHILDREN-V3-2025",
        "NORM-WHO-AI-HEALTH-2021-2025",
        "NORM-NIST-AI-RMF-1-0",
        "NORM-ISO-IEC-42001-2023",
        "NORM-BR-LGPD-COMPILED",
        "NORM-ANPD-CHILDREN-ENUNCIADO-1-2023",
    }
    require(required_normative_ids.issubset(ids), "required normative routing anchor removed")
    require(len(ids) == len(entries), "duplicate normative registry id")
    for entry in entries:
        require(entry.get("authority"), f"missing normative authority: {entry.get('id')}")
        require(entry.get("instrument"), f"missing normative instrument: {entry.get('id')}")
        require(entry.get("scope"), f"missing normative scope: {entry.get('id')}")
        require(entry.get("source", "").startswith("https://"), f"non-https normative source: {entry.get('id')}")

    triggers = set(n["review_triggers"])
    require("source_reports_revision_or_supersession" in triggers, "normative supersession review trigger removed")
    require("scope_expands_to_new_jurisdiction" in triggers, "jurisdiction expansion review trigger removed")
    normative_gaps = set(n["open_gaps"])
    require("TOKEN_VAZIO_INDEPENDENT_LEGAL_REVIEW_WHEN_REQUIRED" in normative_gaps, "independent legal review gap fabricated closed")

    for phrase in (
        "PERSON != RESOURCE != TOKEN != DATASET != COST_FUNCTION",
        "MODEL_RECOMMENDATION != HUMAN_VALUE_DECISION",
        "UNKNOWN_RISK != SAFE",
        "BEST_INTEREST_OF_CHILD = HARD_CONSTRAINT",
        "LATEST != STRONGER",
    ):
        require(phrase in doc, f"documentation invariant missing: {phrase}")

    print("PASS: human dignity ethics-by-design ratchet v1 + normative routing registry v1")


if __name__ == "__main__":
    main()
