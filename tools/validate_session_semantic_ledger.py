#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data/memory/session-semantic/manifest.v1.json"


class LedgerError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise LedgerError(f"not_object:{path}")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LedgerError(f"jsonl:{path}:{lineno}:{exc}") from exc
        if not isinstance(row, dict):
            raise LedgerError(f"jsonl_not_object:{path}:{lineno}")
        rows.append(row)
    return rows


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(manifest_path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    errors: list[str] = []

    def require(ok: bool, msg: str) -> None:
        if not ok:
            errors.append(msg)

    require(manifest.get("schema_version") == "rafaelia.session-semantic-ledger-manifest/v1", "manifest.schema_version")
    require(manifest.get("claim_allowed") is False, "manifest.claim_allowed_must_be_false")

    shards = manifest.get("shards", {})
    required_shards = {"forests", "concepts", "sessions", "relations"}
    require(set(shards) == required_shards, "manifest.shards")
    if set(shards) != required_shards:
        raise LedgerError(";".join(errors))

    paths = {name: ROOT / rel for name, rel in shards.items()}
    for name, path in paths.items():
        require(path.is_file(), f"missing_shard:{name}:{path}")
    if errors:
        raise LedgerError(";".join(errors))

    forests_doc = load_json(paths["forests"])
    forests = forests_doc.get("forests", [])
    concepts = load_jsonl(paths["concepts"])
    sessions = load_jsonl(paths["sessions"])
    relations = load_jsonl(paths["relations"])

    forest_ids = [f.get("forest_id") for f in forests]
    concept_ids = [c.get("concept_id") for c in concepts]
    session_ids = [s.get("session_id") for s in sessions]
    relation_ids = [r.get("relation_id") for r in relations]

    require(len(forest_ids) == 7, "forest_count_must_be_7")
    require(len(set(forest_ids)) == len(forest_ids), "duplicate_forest_id")
    require(len(set(concept_ids)) == len(concept_ids), "duplicate_concept_id")
    require(len(set(session_ids)) == len(session_ids), "duplicate_session_id")
    require(len(set(relation_ids)) == len(relation_ids), "duplicate_relation_id")

    fset = set(forest_ids)
    cset = set(concept_ids)
    sset = set(session_ids)
    endpoints = cset | sset

    for idx, concept in enumerate(concepts):
        require(concept.get("claim_allowed") is False, f"concept[{idx}].claim_allowed")
        require(isinstance(concept.get("concept_id"), str) and concept["concept_id"].startswith("concept:"), f"concept[{idx}].id")

    block_count = 0
    gap_count = 0
    provider_gap_count = 0
    sequences: list[int] = []
    source_locators: set[str] = set()

    for idx, session in enumerate(sessions):
        sid = session.get("session_id")
        require(session.get("claim_allowed") is False, f"session[{idx}].claim_allowed")
        require(session.get("primary_forest") in fset, f"session[{idx}].primary_forest")
        for forest in session.get("secondary_forests", []):
            require(forest in fset, f"session[{idx}].secondary_forest:{forest}")
        for cref in session.get("concept_refs", []):
            require(cref in cset, f"session[{idx}].concept_ref:{cref}")
        blocks = session.get("semantic_blocks", [])
        require(bool(blocks), f"session[{idx}].semantic_blocks")
        block_count += len(blocks)
        for bidx, block in enumerate(blocks):
            for cref in block.get("concept_refs", []):
                require(cref in cset, f"session[{idx}].block[{bidx}].concept_ref:{cref}")
        locator = session.get("source_locator")
        require(isinstance(locator, str) and locator.startswith("gpt-project-context://"), f"session[{idx}].source_locator")
        require(locator not in source_locators, f"duplicate_source_locator:{locator}")
        source_locators.add(locator)
        precision = session.get("timestamp_precision")
        label = session.get("observed_time_label", "")
        if precision == "minute":
            require(":" in label, f"session[{idx}].minute_precision")
        if precision == "hour":
            require(":" not in label, f"session[{idx}].hour_precision")
        seq = session.get("ordinal_sequence")
        require(isinstance(seq, int) and seq > 0, f"session[{idx}].ordinal_sequence")
        if isinstance(seq, int):
            sequences.append(seq)

        gaps = session.get("gaps", [])
        gap_count += len(gaps)
        if session.get("provider_id") is None:
            require(session.get("source_state") == "OBSERVED_CONTEXT_PROVIDER_ID_UNAVAILABLE", f"session[{idx}].source_state_without_provider")
            typed = [g for g in gaps if g.get("gap_class") == "TV-SOURCE" and g.get("blocking") is True]
            require(bool(typed), f"session[{idx}].missing_blocking_TV_SOURCE")
            if typed:
                provider_gap_count += 1
        else:
            require(session.get("source_state") == "VERIFIED_PROVIDER_ID", f"session[{idx}].verified_provider_state")

    require(sorted(sequences) == list(range(1, len(sessions) + 1)), "ordinal_sequence_not_contiguous")

    allowed_predicates = {
        "DERIVES_FROM", "DEPENDS_ON", "SUPPORTS", "CONTRADICTS", "SUPERSEDES",
        "IMPLEMENTS", "VALIDATES", "BLOCKS", "PRODUCES", "MENTIONS", "CROSS_LINK",
    }
    for idx, rel in enumerate(relations):
        require(rel.get("subject") in endpoints, f"relation[{idx}].subject:{rel.get('subject')}")
        require(rel.get("object") in endpoints, f"relation[{idx}].object:{rel.get('object')}")
        require(rel.get("predicate") in allowed_predicates, f"relation[{idx}].predicate")
        conf = rel.get("confidence")
        require(isinstance(conf, (int, float)) and 0 <= conf <= 1, f"relation[{idx}].confidence")
        require(rel.get("state") in {"OBSERVED", "DERIVED_INTERPRETATION", "TOKEN_VAZIO"}, f"relation[{idx}].state")

    coverage = manifest.get("coverage", {})
    actual = {
        "sessions": len(sessions),
        "semantic_blocks": block_count,
        "concepts": len(concepts),
        "relations": len(relations),
        "typed_gaps": gap_count,
        "provider_id_gaps": provider_gap_count,
        "claim_allowed_true": sum(1 for c in concepts if c.get("claim_allowed") is True) + sum(1 for s in sessions if s.get("claim_allowed") is True),
    }
    require(coverage == actual, f"coverage_mismatch:declared={coverage}:actual={actual}")
    require(manifest.get("scope", {}).get("observed_session_count") == len(sessions), "scope.observed_session_count")
    require(manifest.get("scope", {}).get("provider_ids_resolved") == len(sessions) - provider_gap_count, "scope.provider_ids_resolved")

    if errors:
        raise LedgerError(";".join(errors))

    return {
        "schema": "rafaelia.session-semantic-ledger-validation/v1",
        "status": "PASS",
        "event_id": manifest.get("event_id"),
        "claim_allowed": False,
        "coverage": actual,
        "sha256": {name: sha256_file(path) for name, path in paths.items()},
        "gates": {
            "forest_references": "PASS",
            "concept_references": "PASS",
            "relation_endpoints": "PASS",
            "provider_identity_fail_closed": "PASS",
            "coverage_exact": "PASS",
            "ordinal_sequence_contiguous_within_snapshot": "PASS"
        },
        "boundary": "PASS validates internal consistency of the semantic projection; it does not prove provider identity, full-session completeness, scientific equivalence, or physical execution."
    }


def main() -> int:
    manifest = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MANIFEST
    if not manifest.is_absolute():
        manifest = ROOT / manifest
    try:
        report = validate(manifest)
    except (OSError, json.JSONDecodeError, LedgerError) as exc:
        report = {
            "schema": "rafaelia.session-semantic-ledger-validation/v1",
            "status": "FAIL",
            "claim_allowed": False,
            "reason": str(exc),
        }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
