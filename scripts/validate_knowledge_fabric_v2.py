#!/usr/bin/env python3
"""Dependency-free validator for the RAFAELIA Knowledge Fabric V2 contract."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

OPERATIONS = {"DISCOVER", "READ", "EXECUTE", "WRITE", "PUBLISH"}
PROMOTION_CAPS = {"catalog_only", "tested_scope", "claim_review_required"}
EVIDENCE_EFFECTS = {"none", "supports", "contradicts"}
ACCESS_CLASSES = {"public", "private", "restricted", "TOKEN_VAZIO"}


def _iso(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return "T" in value
    except ValueError:
        return False


def validate(bundle: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(bundle, dict):
        return ["bundle_must_be_object"]
    if bundle.get("schema") != "rafaelia.knowledge-fabric/v2":
        errors.append("schema_version")
    if bundle.get("claim_allowed") is not False:
        errors.append("claim_allowed_must_remain_false")

    collections = ("objects", "relations", "events", "evidence", "receipts", "authorities", "actions", "states", "deltas", "gaps")
    for name in collections:
        if not isinstance(bundle.get(name), list):
            errors.append(f"{name}_must_be_array")
    if errors:
        return errors

    objects = bundle["objects"]
    object_ids = [x.get("id") for x in objects if isinstance(x, dict)]
    if len(object_ids) != len(objects) or any(not isinstance(x, str) or not x for x in object_ids):
        errors.append("object_identity_required")
    if len(set(object_ids)) != len(object_ids):
        errors.append("duplicate_object_id")
    object_by_id = {x["id"]: x for x in objects if isinstance(x, dict) and isinstance(x.get("id"), str)}

    # Globally disjoint typed IDs prevent an artifact, execution, evidence, receipt, or claim
    # from being silently treated as the same entity.
    typed_ids: dict[str, str] = {}
    for collection in ("objects", "relations", "events", "evidence", "receipts", "authorities", "actions", "states", "deltas", "gaps"):
        for item in bundle[collection]:
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                item_id = item["id"]
                if item_id in typed_ids:
                    errors.append(f"typed_id_collision:{item_id}:{typed_ids[item_id]}:{collection}")
                else:
                    typed_ids[item_id] = collection

    for obj in objects:
        if not isinstance(obj, dict):
            continue
        if not obj.get("object_type"):
            errors.append(f"object_type_required:{obj.get('id')}")
        ident = obj.get("source_identity")
        if not isinstance(ident, dict) or any(not isinstance(ident.get(k), str) or not ident[k] for k in ("surface", "provider_id", "ref")):
            errors.append(f"source_identity_incomplete:{obj.get('id')}")
        elif ident.get("hash") and not ident.get("hash_scope"):
            errors.append(f"hash_scope_required:{obj.get('id')}")
        if obj.get("access_class") not in ACCESS_CLASSES:
            errors.append(f"invalid_access_class:{obj.get('id')}")
        if obj.get("object_type") == "token" and obj.get("semantic_state") == "TOKEN_VAZIO":
            if obj.get("literal_surface") is None:
                errors.append(f"unresolved_token_literal_required:{obj.get('id')}")

    relation_ids = set()
    for rel in bundle["relations"]:
        if not isinstance(rel, dict):
            errors.append("relation_must_be_object")
            continue
        rid = rel.get("id")
        if not rid or rid in relation_ids:
            errors.append("relation_id_missing_or_duplicate")
        relation_ids.add(rid)
        for endpoint in ("source_id", "target_id"):
            if rel.get(endpoint) not in object_by_id:
                errors.append(f"relation_endpoint_missing:{rid}:{endpoint}")
        required = ("direction", "scope", "source_ref", "evidence_effect", "promotion_cap", "guard", "supersession_ref")
        for field in required:
            if field not in rel or rel[field] is None or rel[field] == "":
                errors.append(f"relation_field_missing:{rid}:{field}")
        if rel.get("evidence_effect") not in EVIDENCE_EFFECTS:
            errors.append(f"relation_evidence_effect:{rid}")
        if rel.get("promotion_cap") not in PROMOTION_CAPS:
            errors.append(f"relation_promotion_cap:{rid}")

    event_ids = set()
    events_by_target: dict[str, list[dict]] = {}
    for event in bundle["events"]:
        if not isinstance(event, dict):
            errors.append("event_must_be_object")
            continue
        eid = event.get("id")
        if not eid or eid in event_ids:
            errors.append("event_id_missing_or_duplicate")
        event_ids.add(eid)
        target = event.get("target_id")
        if target not in object_by_id:
            errors.append(f"event_target_missing:{eid}")
        events_by_target.setdefault(target, []).append(event)
        if not _iso(event.get("observed_at")):
            errors.append(f"event_observed_at_invalid:{eid}")
        if not event.get("source_ref"):
            errors.append(f"event_source_ref_missing:{eid}")
    for oid, obj in object_by_id.items():
        if obj.get("object_type") == "pull_request" and not events_by_target.get(oid):
            errors.append(f"mutable_pull_request_requires_event:{oid}")

    state_ids = set()
    for state in bundle["states"]:
        if not isinstance(state, dict):
            errors.append("state_must_be_object")
            continue
        sid = state.get("id")
        if not sid or sid in state_ids:
            errors.append("state_id_missing_or_duplicate")
        state_ids.add(sid)
        if state.get("target_id") not in object_by_id:
            errors.append(f"state_target_missing:{sid}")
        if not _iso(state.get("observed_at")):
            errors.append(f"state_observed_at_invalid:{sid}")
        if not state.get("source_ref") or not isinstance(state.get("value"), str):
            errors.append(f"state_source_or_value_missing:{sid}")

    delta_ids = set()
    for delta in bundle["deltas"]:
        if not isinstance(delta, dict):
            errors.append("delta_must_be_object")
            continue
        did = delta.get("id")
        if not did or did in delta_ids:
            errors.append("delta_id_missing_or_duplicate")
        delta_ids.add(did)
        parent, successor = delta.get("parent_state_id"), delta.get("successor_state_id")
        if parent not in state_ids or successor not in state_ids:
            errors.append(f"delta_state_reference_missing:{did}")
        if parent == successor:
            errors.append(f"delta_must_create_successor_state:{did}")
        if delta.get("append_only") is not True:
            errors.append(f"delta_must_be_append_only:{did}")
        if not delta.get("summary") or not delta.get("source_ref"):
            errors.append(f"delta_provenance_required:{did}")

    gap_ids = set()
    for gap in bundle["gaps"]:
        if not isinstance(gap, dict):
            errors.append("gap_must_be_object")
            continue
        gid = gap.get("id")
        if not gid or gid in gap_ids:
            errors.append("gap_id_missing_or_duplicate")
        gap_ids.add(gid)
        if gap.get("target_id") not in object_by_id:
            errors.append(f"gap_target_missing:{gid}")
        if not gap.get("reason") or not gap.get("next_probe"):
            errors.append(f"gap_reason_and_next_probe_required:{gid}")
        if gap.get("status") not in {"TOKEN_VAZIO", "PENDING", "FAIL"}:
            errors.append(f"gap_status_invalid:{gid}")

    evidence = bundle["evidence"]
    evidence_ids = set()
    for item in evidence:
        if not isinstance(item, dict):
            errors.append("evidence_must_be_object")
            continue
        eid = item.get("id")
        if not eid or eid in evidence_ids:
            errors.append("evidence_id_missing_or_duplicate")
        evidence_ids.add(eid)
        if not all(item.get(k) for k in ("evidence_type", "scope", "source_ref", "result")):
            errors.append(f"evidence_fields_required:{eid}")
    receipt_ids = set()
    for receipt in bundle["receipts"]:
        if not isinstance(receipt, dict):
            errors.append("receipt_must_be_object")
            continue
        rid = receipt.get("id")
        if not rid or rid in receipt_ids or rid in evidence_ids:
            errors.append("receipt_id_missing_duplicate_or_collides_with_evidence")
        receipt_ids.add(rid)
        if not _iso(receipt.get("timestamp")):
            errors.append(f"receipt_timestamp_invalid:{rid}")
        refs = receipt.get("evidence_refs")
        if not isinstance(refs, list) or not refs:
            errors.append(f"receipt_evidence_refs_required:{rid}")
        elif any(ref not in evidence_ids for ref in refs):
            errors.append(f"receipt_must_reference_evidence:{rid}")

    for obj in objects:
        if isinstance(obj, dict) and obj.get("object_type") == "claim":
            refs = obj.get("evidence_refs")
            if not isinstance(refs, list) or not refs:
                errors.append(f"claim_evidence_refs_required:{obj.get('id')}")
            elif any(ref not in evidence_ids for ref in refs):
                errors.append(f"claim_must_reference_evidence:{obj.get('id')}")

    grants: dict[tuple[str, str, str], str] = {}
    for authority in bundle["authorities"]:
        if not isinstance(authority, dict):
            errors.append("authority_must_be_object")
            continue
        if not authority.get("source_ref"):
            errors.append(f"authority_source_ref_required:{authority.get('id')}")
        for grant in authority.get("grants", []):
            if not isinstance(grant, dict):
                errors.append("grant_must_be_object")
                continue
            key = (grant.get("actor"), grant.get("target_id"), grant.get("operation"))
            if grant.get("operation") not in OPERATIONS or grant.get("decision") not in {"ALLOW", "DENY"}:
                errors.append(f"grant_invalid:{authority.get('id')}")
            if key in grants:
                errors.append(f"grant_ambiguous:{key}")
            grants[key] = grant.get("decision")

    action_ids = set()
    for action in bundle["actions"]:
        if not isinstance(action, dict):
            errors.append("action_must_be_object")
            continue
        aid = action.get("id")
        if not aid or aid in action_ids:
            errors.append("action_id_missing_or_duplicate")
        action_ids.add(aid)
        target = object_by_id.get(action.get("target_id"))
        if target is None:
            errors.append(f"action_target_missing:{aid}")
            continue
        operation = action.get("operation")
        if operation not in OPERATIONS:
            errors.append(f"action_operation_invalid:{aid}")
            continue
        actual = grants.get((action.get("actor"), action.get("target_id"), operation), "DENY")
        if target.get("access_class") == "TOKEN_VAZIO" and operation in {"READ", "EXECUTE", "WRITE", "PUBLISH"}:
            actual = "DENY"
        if actual != action.get("expected_decision"):
            errors.append(f"authority_decision_mismatch:{aid}:expected_{action.get('expected_decision')}_got_{actual}")
    return sorted(errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    bundle = json.loads(args.input.read_text(encoding="utf-8"))
    defects = validate(bundle)
    report = {"schema": "rafaelia.knowledge-fabric-validation/v2", "status": "FAIL" if defects else "PASS", "defects": defects, "claim_allowed": False}
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    print(output, end="")
    return 1 if defects else 0


if __name__ == "__main__":
    raise SystemExit(main())
