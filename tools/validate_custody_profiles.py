#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED_TYPES = {
    "C0_SOURCE_ORIGIN",
    "C1_IDENTITY_AUTHORITY",
    "C2_ARTIFACT_INTEGRITY",
    "C3_TRANSFORMATION_DERIVATION",
    "C4_EXECUTION_RUNTIME",
    "C5_EVIDENCE_MEASUREMENT",
    "C6_TRANSFER_CROSS_PROVIDER",
    "C7_DECISION_CLAIM_GATE",
    "C8_RECEIPT_AUDIT",
}
REQUIRED_PROVIDERS = {"GOOGLE_DRIVE", "GITHUB", "CHATGPT_SESSION"}
REQUIRED_ACTORS = {"HUMAN_OWNER", "ASSISTANT_SERVICE", "PROVIDER_AUTOMATION", "DEVICE_RUNTIME"}
REQUIRED_BRIDGE_FIELDS = {
    "artifact_id", "from_provider", "to_provider", "source_ref",
    "destination_ref", "relation", "observed_at", "identity_rule",
}
VALID_EFFECTS = {"NO_PROMOTION", "MAY_FEED_GATE", "GATE_ONLY"}

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate(doc):
    errors = []
    if doc.get("schema_version") != "mapa.custody-profiles.v1":
        errors.append("schema_version")
    if doc.get("claim_allowed_default") is not False:
        errors.append("claim_allowed_default_must_be_false")

    providers = doc.get("providers")
    if not isinstance(providers, list):
        errors.append("providers")
        providers = []
    provider_ids = [p.get("id") for p in providers if isinstance(p, dict)]
    if set(provider_ids) != REQUIRED_PROVIDERS or len(provider_ids) != len(set(provider_ids)):
        errors.append("provider_set_or_duplicates")

    by_provider = {p.get("id"): p for p in providers if isinstance(p, dict)}
    session = by_provider.get("CHATGPT_SESSION", {})
    if session.get("durable") is not False:
        errors.append("chatgpt_session_must_not_be_durable")
    if "CLAIM_PROMOTION" not in set(session.get("not_authority", [])):
        errors.append("chatgpt_session_claim_promotion_boundary")

    actors = doc.get("actors")
    if not isinstance(actors, list):
        errors.append("actors")
        actors = []
    actor_ids = [a.get("id") for a in actors if isinstance(a, dict)]
    if set(actor_ids) != REQUIRED_ACTORS or len(actor_ids) != len(set(actor_ids)):
        errors.append("actor_set_or_duplicates")
    by_actor = {a.get("id"): a for a in actors if isinstance(a, dict)}

    human = by_actor.get("HUMAN_OWNER", {})
    assistant = by_actor.get("ASSISTANT_SERVICE", {})
    if human.get("may_define_objective") is not True:
        errors.append("human_owner_objective_authority")
    if human.get("may_authorize_claim_promotion") is not True:
        errors.append("human_owner_promotion_authority")
    for key in ("may_define_objective", "may_authorize_claim_promotion", "may_authorize_merge_or_destructive_change"):
        if assistant.get(key) is not False:
            errors.append("assistant_boundary_" + key)

    types = doc.get("custody_types")
    if not isinstance(types, list):
        errors.append("custody_types")
        types = []
    ids = [t.get("id") for t in types if isinstance(t, dict)]
    if set(ids) != REQUIRED_TYPES or len(ids) != len(set(ids)):
        errors.append("custody_type_set_or_duplicates")

    for item in types:
        if not isinstance(item, dict):
            errors.append("custody_type_not_object")
            continue
        tid = item.get("id")
        if not item.get("object_of_custody"):
            errors.append(f"{tid}:object_of_custody")
        if not item.get("authority_rule"):
            errors.append(f"{tid}:authority_rule")
        evidence = item.get("minimum_evidence")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(x, str) and x for x in evidence):
            errors.append(f"{tid}:minimum_evidence")
        allowed = item.get("allowed_primary_providers")
        if not isinstance(allowed, list) or not allowed or not set(allowed) <= REQUIRED_PROVIDERS:
            errors.append(f"{tid}:allowed_primary_providers")
        effect = item.get("claim_effect")
        if effect not in VALID_EFFECTS:
            errors.append(f"{tid}:claim_effect")
        if tid == "C7_DECISION_CLAIM_GATE":
            if effect != "GATE_ONLY":
                errors.append("C7_must_be_gate_only")
        elif effect == "GATE_ONLY":
            errors.append(f"{tid}:gate_only_forbidden")

    transitions = doc.get("transition_rules")
    if not isinstance(transitions, list) or not transitions:
        errors.append("transition_rules")
    else:
        for i, rule in enumerate(transitions):
            if not isinstance(rule, dict):
                errors.append(f"transition_{i}_not_object")
                continue
            req = rule.get("requires")
            if not rule.get("from") or not rule.get("to") or not isinstance(req, list) or not req:
                errors.append(f"transition_{i}_incomplete")
            if rule.get("to") == "C7_DECISION_CLAIM_GATE" and rule.get("automatic_promotion") is not False:
                errors.append("decision_transition_must_not_auto_promote")

    bridge = doc.get("cross_provider_bridge")
    if not isinstance(bridge, dict):
        errors.append("cross_provider_bridge")
    else:
        fields = set(bridge.get("required_fields", []))
        if not REQUIRED_BRIDGE_FIELDS <= fields:
            errors.append("cross_provider_bridge_required_fields")
        if not bridge.get("native_document_rule"):
            errors.append("native_document_rule")
        if not bridge.get("session_rule"):
            errors.append("session_rule")

    invariants = set(doc.get("invariants", []))
    for inv in (
        "SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM",
        "TOKEN_VAZIO != 0",
        "IMPLEMENTED_UNTESTED != PASS",
    ):
        if inv not in invariants:
            errors.append("missing_invariant:" + inv)
    return errors

def main(argv):
    if len(argv) != 2:
        print("usage: validate_custody_profiles.py <registry.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        doc = load(path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID io_or_json: {exc}", file=sys.stderr)
        return 2
    errors = validate(doc)
    if errors:
        print("FAIL")
        for err in errors:
            print(err)
        return 1
    print("PASS custody profiles registry")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
