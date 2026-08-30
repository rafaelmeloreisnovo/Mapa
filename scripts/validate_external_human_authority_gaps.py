#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAPS = ROOT / "data/control-plane/EXTERNAL_HUMAN_AUTHORITY_GAPS_V1.json"


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def main():
    g = json.loads(GAPS.read_text(encoding="utf-8"))
    require(g["schema"] == "rafaelia.external-human-authority-gaps.v1", "schema drift")
    require(g["claim_allowed"] is False, "external gap registry self-promoted")
    require(g["automation_may_close_external_gap"] is False, "automation allowed to close external gap")
    require(g["repository_owner_alone_counts_as_independent_review"] is False, "owner self-review promoted to independence")
    require(g["bot_or_ci_counts_as_affected_group_voice"] is False, "bot/CI promoted to affected-group voice")
    require(g["absence_of_objection_counts_as_approval"] is False, "silence promoted to approval")

    entries = g["gaps"]
    ids = {e["id"] for e in entries}
    required = {
        "TOKEN_VAZIO_INDEPENDENT_HUMAN_RIGHTS_REVIEW",
        "TOKEN_VAZIO_CHILD_SAFETY_DOMAIN_REVIEW_FOR_APPLICABLE_PRODUCTS",
        "TOKEN_VAZIO_JURISDICTION_SPECIFIC_LEGAL_REVIEW_WHEN_REQUIRED",
        "TOKEN_VAZIO_AFFECTED_COMMUNITY_REPRESENTATION_FOR_HIGH_IMPACT_DEPLOYMENT",
        "TOKEN_VAZIO_ENVIRONMENTAL_EXTERNALITY_MEASUREMENT_WHEN_MATERIAL",
        "TOKEN_VAZIO_GITHUB_ADMIN_OR_PROVIDER_CAPABLE_SURFACE",
    }
    require(required.issubset(ids), "required external authority gap removed")
    require(len(ids) == len(entries), "duplicate gap id")

    for entry in entries:
        require(entry.get("state") == "TOKEN_VAZIO", f"external gap fabricated closed: {entry.get('id')}")
        require(entry.get("self_closure_allowed") is False, f"self closure enabled: {entry.get('id')}")
        require(entry.get("authority_type"), f"authority type missing: {entry.get('id')}")
        require(entry.get("minimum_evidence"), f"minimum evidence missing: {entry.get('id')}")
        require(entry.get("required_when"), f"applicability missing: {entry.get('id')}")

    rules = set(g["closure_rules"])
    for rule in (
        "TOKEN_VAZIO != PASS",
        "SELF_REVIEW != INDEPENDENT_REVIEW",
        "BOT_REVIEW != AFFECTED_GROUP_VOICE",
        "NO_OBJECTION != CONSENT",
        "CI_PASS != ETHICAL_CERTIFICATION",
    ):
        require(rule in rules, f"closure rule missing: {rule}")

    print("PASS: external human authority gaps remain typed and fail-closed")


if __name__ == "__main__":
    main()
