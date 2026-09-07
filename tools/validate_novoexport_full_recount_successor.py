#!/usr/bin/env python3
"""Fail-closed validator for the NOVOexport structural recount successor."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/evidence/novoexport_full_recount_successor_20260907.v1.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_INVARIANTS = {
    "DATASET_INFORMS != MISSION_AUTHORITY",
    "MODEL_PROPOSAL != EXECUTION_AUTHORITY",
    "LEARN_APPEND_ONLY != ONLINE_SELF_TRAINING",
    "STRUCTURAL_CARDINALITY != SEMANTIC_EXHAUSTIVITY",
    "STRUCTURAL_REUSE_CLASS != PROVIDER_ORIGIN_CAUSE",
    "SOURCE != DERIVED_INDEX != EXECUTION != EVIDENCE != CLAIM",
    "TOKEN_VAZIO != PASS",
}


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "rafaelia.novoexport-full-recount-successor.v1":
        errors.append("schema")
    if data.get("claim_allowed") is not False:
        errors.append("claim_allowed")

    scope = data.get("source_scope", {})
    expected_counts = {
        "range": "conversations-000..050",
        "source_shards": 51,
        "source_bytes": 1107289897,
        "root_conversations_observed": 5054,
        "unique_conversation_ids": 5054,
        "mapping_nodes_observed": 307043,
        "message_bearing_nodes_observed": 301991,
        "unique_effective_message_ids": 296794,
        "distinct_duplicated_effective_message_ids": 2988,
        "duplicate_effective_message_id_observations": 5197,
        "duplicates_same_conversation_excess": 0,
        "duplicates_cross_conversation_excess": 5197,
        "parse_errors": 0,
    }
    for key, expected in expected_counts.items():
        if scope.get(key) != expected:
            errors.append(f"source_scope.{key}")
    if not HEX64.fullmatch(str(scope.get("source_set_digest_sha256", ""))):
        errors.append("source_set_digest_sha256")

    reuse = data.get("structural_reuse", {})
    if reuse.get("classification") != "SHARED_MESSAGE_SUBGRAPH_ACROSS_DISTINCT_CONVERSATION_IDS":
        errors.append("structural_reuse.classification")
    for key in ("same_node_id", "same_role"):
        if reuse.get(key) != {"observed": 2988, "total": 2988}:
            errors.append(f"structural_reuse.{key}")
    if reuse.get("same_content") != {"observed": 2986, "total": 2988}:
        errors.append("structural_reuse.same_content")
    if reuse.get("same_full_message_object") != {"observed": 2859, "total": 2988}:
        errors.append("structural_reuse.same_full_message_object")
    if reuse.get("provider_origin_state") != "TOKEN_VAZIO":
        errors.append("provider_origin_must_remain_token_vazio")
    if reuse.get("provider_origin_gap") != "TV-MESSAGE-ID-PROVIDER-ORIGIN-CAUSE-20260907":
        errors.append("provider_origin_gap")

    ext = data.get("external_evidence", {})
    for key in (
        "full_recount_receipt_sha256",
        "duplicate_relation_receipt_sha256",
        "topology_private_receipt_sha256",
        "topology_safe_receipt_sha256",
    ):
        if not HEX64.fullmatch(str(ext.get(key, ""))):
            errors.append(f"external_evidence.{key}")

    binding = data.get("rafgittools_binding", {})
    if binding.get("repository") != "rafaelmeloreisnovo/RafGitTools":
        errors.append("rafgittools_binding.repository")
    if binding.get("pull_request") != 430:
        errors.append("rafgittools_binding.pull_request")
    if not HEX40.fullmatch(str(binding.get("head_sha", ""))):
        errors.append("rafgittools_binding.head_sha")
    state = binding.get("state")
    merge_commit = str(binding.get("merge_commit", ""))
    if state == "VALIDATED_PENDING_MERGE":
        if merge_commit != "TOKEN_VAZIO":
            errors.append("pending_binding_must_not_have_merge_commit")
    elif state == "MERGED_VALIDATED":
        if not HEX40.fullmatch(merge_commit):
            errors.append("merged_binding_requires_merge_commit")
    else:
        errors.append("rafgittools_binding.state")
    for key in ("canonical_coherence_gate", "federation_audit", "navigator_selftest"):
        if binding.get(key) != "PASS":
            errors.append(f"rafgittools_binding.{key}")

    semantic = data.get("semantic_ingest", {})
    if semantic.get("structural_cardinality_proven") is not True:
        errors.append("structural_cardinality_proven")
    if semantic.get("semantic_exhaustivity_proven") is not False:
        errors.append("semantic_exhaustivity_proven_must_be_false")
    if not str(semantic.get("state", "")).startswith("TOKEN_VAZIO"):
        errors.append("semantic_state")
    required_gaps = {
        "TV-INDEX-INGEST-000-050",
        "TV-MESSAGES-FULL-COVERAGE-SEMANTIC",
        "TV-MESSAGE-ID-PROVIDER-ORIGIN-CAUSE-20260907",
    }
    if not required_gaps <= set(semantic.get("open_gaps", [])):
        errors.append("semantic_open_gaps")

    authority = data.get("authority", {})
    if authority != {
        "dataset_informs": True,
        "dataset_is_mission_authority": False,
        "model_self_authority": False,
        "training_executed": False,
        "weight_update_executed": False,
        "learn_append_only": True,
    }:
        errors.append("authority_boundary")

    missing = REQUIRED_INVARIANTS - set(data.get("invariants", []))
    if missing:
        errors.append("missing_invariants:" + ",".join(sorted(missing)))
    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read {path}: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        print("FAIL: " + "; ".join(errors), file=sys.stderr)
        return 1
    binding = data["rafgittools_binding"]
    print(
        "PASS "
        f"structural_messages={data['source_scope']['message_bearing_nodes_observed']} "
        f"unique_ids={data['source_scope']['unique_effective_message_ids']} "
        f"rafgittools={binding['state']} semantic=OPEN claim_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
