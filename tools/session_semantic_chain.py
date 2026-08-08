#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "data/memory/session-semantic/chain-policy.v1.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class ChainError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ChainError(f"not_object:{path}")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ChainError(f"jsonl:{path}:{lineno}:{exc}") from exc
        if not isinstance(row, dict):
            raise ChainError(f"jsonl_not_object:{path}:{lineno}")
        rows.append(row)
    return rows


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def stable_id(prefix: str, *parts: str) -> str:
    digest = sha256(list(parts))[:24]
    return f"{prefix}:{digest}"


def validate_binding(binding: dict[str, Any], accepted_basis: set[str]) -> None:
    required = {
        "session_id",
        "provider_session_id",
        "provider_message_id",
        "export_artifact_id",
        "chunk_coordinate",
        "source_sha256",
        "match_basis",
        "verified",
    }
    missing = sorted(required - set(binding))
    if missing:
        raise ChainError(f"binding_missing_fields:{binding.get('session_id')}:{','.join(missing)}")
    for key in (
        "session_id",
        "provider_session_id",
        "provider_message_id",
        "export_artifact_id",
        "chunk_coordinate",
    ):
        if not isinstance(binding.get(key), str) or not binding[key].strip():
            raise ChainError(f"binding_invalid_string:{binding.get('session_id')}:{key}")
    if binding.get("match_basis") not in accepted_basis:
        raise ChainError(f"binding_match_basis:{binding.get('session_id')}:{binding.get('match_basis')}")
    if binding.get("verified") is not True:
        raise ChainError(f"binding_not_verified:{binding.get('session_id')}")
    if not isinstance(binding.get("source_sha256"), str) or not HEX64.fullmatch(binding["source_sha256"]):
        raise ChainError(f"binding_source_sha256:{binding.get('session_id')}")


def build(policy_path: Path = POLICY_PATH) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    policy = load_json(policy_path)
    if policy.get("schema_version") != "rafaelia.session-semantic-chain-policy/v1":
        raise ChainError("policy.schema_version")

    sessions_path = ROOT / policy["source_sessions"]
    bindings_path = ROOT / policy["identity_bindings"]
    sessions = load_jsonl(sessions_path)
    bindings_doc = load_json(bindings_path)
    if bindings_doc.get("schema_version") != "rafaelia.session-identity-bindings/v1":
        raise ChainError("bindings.schema_version")

    accepted_basis = set(policy["identity_contract"]["accepted_match_basis"])
    bindings: dict[str, dict[str, Any]] = {}
    for binding in bindings_doc.get("bindings", []):
        if not isinstance(binding, dict):
            raise ChainError("binding_not_object")
        validate_binding(binding, accepted_basis)
        sid = binding["session_id"]
        if sid in bindings:
            raise ChainError(f"duplicate_binding:{sid}")
        bindings[sid] = binding

    session_ids = {s.get("session_id") for s in sessions}
    orphan_bindings = sorted(set(bindings) - session_ids)
    if orphan_bindings:
        raise ChainError(f"orphan_bindings:{','.join(orphan_bindings)}")

    rows: list[dict[str, Any]] = []
    expected_pairs: set[tuple[str, str, str]] = set()
    observed_pairs: set[tuple[str, str, str]] = set()
    occurrence_ids: set[str] = set()
    fingerprints: dict[str, str] = {}

    for session in sessions:
        sid = session.get("session_id")
        if not isinstance(sid, str) or not sid:
            raise ChainError("session_missing_id")
        locator = session.get("source_locator")
        if not isinstance(locator, str) or not locator:
            raise ChainError(f"session_missing_source_locator:{sid}")

        identity_material = {
            "session_id": sid,
            "observed_time_label": session.get("observed_time_label"),
            "observed_title": session.get("observed_title"),
            "source_locator": locator,
        }
        fingerprint = sha256(identity_material)
        if fingerprint in fingerprints and fingerprints[fingerprint] != sid:
            raise ChainError(f"observation_fingerprint_collision:{sid}:{fingerprints[fingerprint]}")
        fingerprints[fingerprint] = sid

        binding = bindings.get(sid)
        exact_identity = binding is not None
        blocks = session.get("semantic_blocks", [])
        if not isinstance(blocks, list) or not blocks:
            raise ChainError(f"session_without_blocks:{sid}")

        for block in blocks:
            if not isinstance(block, dict):
                raise ChainError(f"block_not_object:{sid}")
            block_id = block.get("block_id")
            if not isinstance(block_id, str) or not block_id:
                raise ChainError(f"block_missing_id:{sid}")
            concept_refs = block.get("concept_refs", [])
            if not isinstance(concept_refs, list) or not concept_refs:
                raise ChainError(f"block_without_concepts:{block_id}")
            if len(concept_refs) != len(set(concept_refs)):
                raise ChainError(f"duplicate_concept_in_block:{block_id}")

            for concept_id in concept_refs:
                if not isinstance(concept_id, str) or not concept_id.startswith("concept:"):
                    raise ChainError(f"invalid_concept_ref:{block_id}:{concept_id}")
                pair = (sid, block_id, concept_id)
                expected_pairs.add(pair)
                if pair in observed_pairs:
                    raise ChainError(f"duplicate_chain_pair:{sid}:{block_id}:{concept_id}")
                observed_pairs.add(pair)

                occurrence_id = stable_id("occurrence", sid, block_id, concept_id)
                if occurrence_id in occurrence_ids:
                    raise ChainError(f"occurrence_id_collision:{occurrence_id}")
                occurrence_ids.add(occurrence_id)

                relation_id = stable_id("chain-relation", occurrence_id, concept_id)
                claim_id = stable_id("trace-claim", occurrence_id, "TRACEABILITY_CLAIM")
                evidence_id = stable_id("chain-evidence", claim_id, fingerprint)
                state_id = stable_id("chain-state", evidence_id, sid)
                artifact_id = stable_id("chain-artifact", state_id, block_id)

                block_is_token_vazio = block.get("state") == "TOKEN_VAZIO"
                evidence_state = "BOUND_EXACT" if exact_identity else "PROJECTED_CONTEXT_ONLY"
                trace_claim_allowed = exact_identity and not block_is_token_vazio
                promotion_allowed = trace_claim_allowed and evidence_state == "BOUND_EXACT"
                if promotion_allowed:
                    promotion_state = "PROMOTABLE"
                elif exact_identity:
                    promotion_state = "EVIDENCE_BOUND"
                else:
                    promotion_state = "IDENTITY_PENDING"

                row: dict[str, Any] = {
                    "schema_version": "rafaelia.session-semantic-chain-row/v1",
                    "session_id": sid,
                    "block_id": block_id,
                    "concept_id": concept_id,
                    "occurrence_id": occurrence_id,
                    "relation_id": relation_id,
                    "claim_id": claim_id,
                    "evidence_id": evidence_id,
                    "state_id": state_id,
                    "artifact_id": artifact_id,
                    "observation_fingerprint": fingerprint,
                    "identity_status": "EXACT_PROVIDER_BOUND" if exact_identity else "UNRESOLVED_PROVIDER_ID",
                    "provider_session_id": binding["provider_session_id"] if binding else None,
                    "provider_message_id": binding["provider_message_id"] if binding else None,
                    "export_artifact_id": binding["export_artifact_id"] if binding else None,
                    "chunk_coordinate": binding["chunk_coordinate"] if binding else None,
                    "source_sha256": binding["source_sha256"] if binding else None,
                    "source_locator": locator,
                    "claim_kind": "TRACEABILITY_CLAIM",
                    "claim_allowed": trace_claim_allowed,
                    "evidence_state": evidence_state,
                    "promotion_state": promotion_state,
                    "promotion_allowed": promotion_allowed,
                }
                rows.append(row)

    if expected_pairs != observed_pairs:
        missing = sorted(expected_pairs - observed_pairs)
        extra = sorted(observed_pairs - expected_pairs)
        raise ChainError(f"coverage_not_1to1:missing={missing}:extra={extra}")

    unresolved_sessions = sorted({r["session_id"] for r in rows if r["identity_status"] == "UNRESOLVED_PROVIDER_ID"})
    promotable_sessions = sorted({r["session_id"] for r in rows if r["promotion_allowed"]})
    report = {
        "schema": "rafaelia.session-semantic-chain-validation/v1",
        "status": "PASS",
        "sessions": len(sessions),
        "semantic_pairs_expected": len(expected_pairs),
        "chain_rows": len(rows),
        "projected_semantic_coverage": 1.0 if expected_pairs == observed_pairs else 0.0,
        "identity_bindings_exact": len(bindings),
        "identity_pending_sessions": len(unresolved_sessions),
        "promotable_sessions": len(promotable_sessions),
        "raw_export_coverage": "TOKEN_VAZIO" if unresolved_sessions else "BOUND_FOR_PROJECTED_SESSIONS",
        "promotion_default": "DENY",
        "boundary": "1:1 coverage applies to the current semantic projection only. Provider/export byte coverage is not inferred from titles, summaries or local fingerprints.",
    }
    return rows, report


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for row in rows)
    path.write_text(payload, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build/validate the deterministic Session Semantic Ledger 1:1 chain view.")
    parser.add_argument("--policy", default=str(POLICY_PATH))
    parser.add_argument("--emit", help="Write the derived chain JSONL to this path.")
    parser.add_argument("--lookup", help="Return rows whose IDs/locator contain this substring.")
    args = parser.parse_args()

    policy_path = Path(args.policy)
    if not policy_path.is_absolute():
        policy_path = ROOT / policy_path
    try:
        rows, report = build(policy_path)
        if args.emit:
            emit = Path(args.emit)
            if not emit.is_absolute():
                emit = ROOT / emit
            write_jsonl(emit, rows)
            report["emitted"] = str(emit.relative_to(ROOT)) if emit.is_relative_to(ROOT) else str(emit)
        if args.lookup:
            needle = args.lookup.casefold()
            matches = [
                row for row in rows
                if needle in " ".join(str(v) for v in row.values() if v is not None).casefold()
            ]
            print(json.dumps({"report": report, "matches": matches}, ensure_ascii=False, sort_keys=True, indent=2))
        else:
            print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (OSError, json.JSONDecodeError, ChainError, KeyError, TypeError) as exc:
        print(json.dumps({
            "schema": "rafaelia.session-semantic-chain-validation/v1",
            "status": "FAIL",
            "promotion_default": "DENY",
            "reason": str(exc),
        }, ensure_ascii=False, sort_keys=True, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
