#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_claim_review_chain import (
    ChainValidationError,
    canonical_digest,
    load_json,
    validate_chain,
    validate_resolution,
)

SCHEMA = "mapa.claim-review-residual.v1"
NEXT_GATE = "OBSERVABLE_SCANNER_RECEIPT_AND_SCOPE_REFRESH"
HISTORICAL_NEXT_GATE = "MATERIALIZE_FULL_CC028_AND_OBSERVABLE_SCANNER_RECEIPT"
HEX40 = re.compile(r"^[0-9a-f]{40}$")


class ResidualValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ResidualValidationError(message)


def _derive_historical_states(root: Path, head: dict[str, Any]) -> tuple[dict[str, str], dict[str, str]]:
    ledger = load_json(root / head["base_ledger"]["path"])
    states = {entry["id"]: entry["review_state"] for entry in ledger["entries"]}
    paths = {entry["id"]: entry["path"] for entry in ledger["entries"]}
    for ref in head["review_batches"][:2]:
        batch = load_json(root / ref["path"])
        for decision in batch["decisions"]:
            states[decision["entry_id"]] = decision["to_state"]
    return states, paths


def validate_historical_residual(
    root: Path,
    residual: dict[str, Any],
    head: dict[str, Any],
) -> dict[str, Any]:
    require(residual.get("schema") == SCHEMA, "invalid historical residual schema")
    require(residual.get("authority_repository") == "rafaelmeloreisnovo/Mapa", "Mapa authority required")
    require(residual.get("gap_id") == "G006", "G006 scope required")
    require(residual.get("claim_allowed") is False, "historical claim_allowed must remain false")
    require(residual.get("certification_claim") is False, "historical certification claim is forbidden")
    require(residual.get("portfolio_exit_criteria_met") is False, "historical portfolio boundary mismatch")
    source_commit = residual.get("source_commit")
    require(isinstance(source_commit, str) and HEX40.fullmatch(source_commit), "historical source commit invalid")

    states, paths = _derive_historical_states(root, head)
    expected_ids = sorted(entry_id for entry_id, state in states.items() if state == "TOKEN_VAZIO")
    require(expected_ids == ["CC028"], "historical chain must contain only CC028 as TOKEN_VAZIO")
    entries = residual.get("residuals")
    require(isinstance(entries, list) and len(entries) == 1, "one historical residual required")
    entry = entries[0]
    require(isinstance(entry, dict) and entry.get("id") == "CC028", "historical residual id mismatch")
    require(entry.get("path") == paths["CC028"], "historical residual path mismatch")
    require(entry.get("state") == "TOKEN_VAZIO", "historical residual state mismatch")
    require(entry.get("owner_role") == "R12", "historical owner role mismatch")
    require(entry.get("claim_allowed") is False, "historical entry claim boundary mismatch")
    require(entry.get("reason") == "CONNECTOR_RESPONSE_TRUNCATED_AT_LINE_BOUNDARY", "historical reason mismatch")

    attempts = entry.get("attempts")
    require(isinstance(attempts, list) and len(attempts) == 2, "exactly two historical attempts required")
    require(
        [attempt.get("method") for attempt in attempts]
        == ["GitHub.fetch_file", "GitHub.fetch_blob"],
        "historical methods changed",
    )
    require(all(attempt.get("result") == "TRUNCATED_RESPONSE" for attempt in attempts), "historical attempt result changed")
    blob_shas = {attempt.get("blob_sha") for attempt in attempts}
    require(blob_shas == {"b43554096f00c0918997dd9f9b11787cec4d4e52"}, "historical blob identity changed")

    boundary = entry.get("observed_boundary")
    require(isinstance(boundary, dict), "historical observed boundary required")
    require(boundary.get("partial_state_observed") is True, "historical PARTIAL observation missing")
    require(boundary.get("claim_allowed_false_observed") is True, "historical claim boundary observation missing")
    require(boundary.get("full_content_observed") is False, "historical full-content state changed")
    require(boundary.get("semantic_disposition_allowed") is False, "historical semantic boundary changed")

    derived = residual.get("derived")
    require(isinstance(derived, dict), "historical derived required")
    require(derived.get("residual_count") == 1, "historical residual count mismatch")
    require(derived.get("token_vazio_ids") == ["CC028"], "historical TOKEN_VAZIO ids mismatch")
    require(derived.get("next_gate") == HISTORICAL_NEXT_GATE, "historical next gate changed")
    require(derived.get("claim_allowed") is False, "historical derived claim boundary changed")
    require(derived.get("certification_claim") is False, "historical derived certification boundary changed")
    require(derived.get("portfolio_exit_criteria_met") is False, "historical derived portfolio boundary changed")

    integrity = residual.get("integrity")
    require(isinstance(integrity, dict), "historical integrity required")
    require(integrity.get("algorithm") == "blake2b-256", "historical integrity algorithm mismatch")
    expected_digest = canonical_digest(residual)
    require(integrity.get("digest") == expected_digest, "historical residual integrity mismatch")
    return {
        "historical_residual_count": 1,
        "historical_token_vazio_ids": ["CC028"],
        "historical_attempt_count": 2,
        "historical_integrity_digest": expected_digest,
        "historical_full_content_observed": False,
        "historical_semantic_disposition_allowed": False,
    }


def validate_residual_resolution(
    root: Path,
    residual: dict[str, Any],
    resolution: dict[str, Any],
    head: dict[str, Any],
) -> dict[str, Any]:
    try:
        chain = validate_chain(root, head)
    except ChainValidationError as exc:
        raise ResidualValidationError(f"claim review chain invalid: {exc}") from exc

    history = validate_historical_residual(root, residual, head)
    resolution_path = "indices/CLAIM_REVIEW_RESOLUTION_CC028.json"
    resolution_report = validate_resolution(
        root,
        resolution_path,
        entry_id="CC028",
        source_commit="4016c51e024573a3875457fceb6d05926e07a07b",
        source_path="indices/REPOSITORY_INVENTORY.json",
    )
    require(resolution == load_json(root / resolution_path), "resolution argument differs from canonical file")

    historical_ref = resolution.get("historical_residual")
    require(isinstance(historical_ref, dict), "resolution historical reference required")
    require(historical_ref.get("path") == "indices/CLAIM_REVIEW_RESIDUAL.json", "historical residual path mismatch")
    require(
        historical_ref.get("digest_blake2b_256") == history["historical_integrity_digest"],
        "historical residual digest mismatch",
    )
    require(historical_ref.get("state") == "HISTORICAL_RESIDUAL_PRESERVED", "historical preservation state mismatch")

    require(chain["candidate_count"] == 36, "candidate count mismatch")
    require(chain["review_batch_count"] == 3, "review batch count mismatch")
    require(chain["review_decision_count"] == 30, "review decision count mismatch")
    require(chain["reviewed_safe_count"] == 36, "reviewed safe count mismatch")
    require(chain["reviewed_blocking_count"] == 0, "reviewed blocking count mismatch")
    require(chain["token_vazio_count"] == 0, "current residual must be empty")
    require(chain["review_completion_ratio"] == 1.0, "indexed review must be complete")
    require(chain["exact_absence_resolution_count"] == 1, "exact-absence resolution count mismatch")
    require(chain["next_gate"] == NEXT_GATE, "chain next gate mismatch")
    require(chain["portfolio_exit_criteria_met"] is False, "portfolio cannot close automatically")
    require(chain["claim_allowed"] is False, "chain claim boundary mismatch")
    require(chain["certification_claim"] is False, "chain certification boundary mismatch")

    return {
        "status": "PASS",
        "schema": "mapa.claim-review-residual-resolution-validation.v1",
        **history,
        "resolved_count": 1,
        "resolved_ids": ["CC028"],
        "current_residual_count": 0,
        "current_token_vazio_ids": [],
        "full_content_observed": True,
        "semantic_disposition_allowed": True,
        "decoded_size_bytes": resolution_report["decoded_size_bytes"],
        "git_blob_sha1": resolution_report["git_blob_sha1"],
        "sha256": resolution_report["sha256"],
        "exact_strong_token_count": resolution_report["exact_strong_token_count"],
        "false_positive_source": resolution_report["false_positive_source"],
        "resolution_integrity_digest": resolution_report["integrity_digest"],
        "next_gate": NEXT_GATE,
        "portfolio_exit_criteria_met": False,
        "claim_allowed": False,
        "certification_claim": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, default=Path("indices/CLAIM_REVIEW_RESIDUAL.json"))
    parser.add_argument("--resolution", type=Path, default=Path("indices/CLAIM_REVIEW_RESOLUTION_CC028.json"))
    parser.add_argument("--head", type=Path, default=Path("indices/CLAIM_CONTRADICTION_HEAD.json"))
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args(argv)
    try:
        result = validate_residual_resolution(
            Path.cwd(),
            load_json(args.residual),
            load_json(args.resolution),
            load_json(args.head),
        )
    except (ResidualValidationError, ChainValidationError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    text = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
