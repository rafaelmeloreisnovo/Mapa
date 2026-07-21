#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_claim_review_chain import (
    ChainValidationError,
    load_json,
    validate_chain,
)

SCHEMA = "mapa.claim-review-residual.v1"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
NEXT_GATE = "MATERIALIZE_FULL_CC028_AND_OBSERVABLE_SCANNER_RECEIPT"


class ResidualValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ResidualValidationError(message)


def canonical_digest(data: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(data))
    clone.setdefault("integrity", {})["digest"] = ""
    payload = json.dumps(
        clone,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.blake2b(payload, digest_size=32).hexdigest()


def _derive_states(root: Path, head: dict[str, Any]) -> tuple[dict[str, str], dict[str, str]]:
    ledger = load_json(root / head["base_ledger"]["path"])
    states = {entry["id"]: entry["review_state"] for entry in ledger["entries"]}
    paths = {entry["id"]: entry["path"] for entry in ledger["entries"]}
    for ref in head["review_batches"]:
        batch = load_json(root / ref["path"])
        for decision in batch["decisions"]:
            states[decision["entry_id"]] = decision["to_state"]
    return states, paths


def validate_residual(root: Path, residual: dict[str, Any], head: dict[str, Any]) -> dict[str, Any]:
    try:
        chain = validate_chain(root, head)
    except ChainValidationError as exc:
        raise ResidualValidationError(f"claim review chain invalid: {exc}") from exc

    require(residual.get("schema") == SCHEMA, "invalid residual schema")
    require(residual.get("authority_repository") == "rafaelmeloreisnovo/Mapa", "Mapa authority required")
    require(residual.get("gap_id") == "G006", "G006 scope required")
    require(residual.get("claim_allowed") is False, "claim_allowed must remain false")
    require(residual.get("certification_claim") is False, "certification claim is forbidden")
    require(residual.get("portfolio_exit_criteria_met") is False, "portfolio exit criteria must remain false")
    source_commit = residual.get("source_commit")
    require(isinstance(source_commit, str) and HEX40.fullmatch(source_commit), "source commit invalid")

    states, paths = _derive_states(root, head)
    expected_ids = sorted(entry_id for entry_id, state in states.items() if state == "TOKEN_VAZIO")
    entries = residual.get("residuals")
    require(isinstance(entries, list) and entries, "residual entries required")
    ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
    require(len(ids) == len(entries), "every residual must be an object with an id")
    require(len(ids) == len(set(ids)), "duplicate residual id")
    require(sorted(ids) == expected_ids, "residual coverage differs from review-chain TOKEN_VAZIO state")

    for entry in entries:
        entry_id = entry["id"]
        require(entry.get("path") == paths[entry_id], f"{entry_id}: path mismatch")
        require(entry.get("state") == "TOKEN_VAZIO", f"{entry_id}: residual state must be TOKEN_VAZIO")
        require(entry.get("owner_role") == "R12", f"{entry_id}: owner role mismatch")
        require(entry.get("claim_allowed") is False, f"{entry_id}: claim_allowed must remain false")
        require(entry.get("reason") == "CONNECTOR_RESPONSE_TRUNCATED_AT_LINE_BOUNDARY", f"{entry_id}: reason mismatch")
        criteria = entry.get("exit_criteria")
        require(isinstance(criteria, list) and len(criteria) >= 5, f"{entry_id}: exit criteria incomplete")

        attempts = entry.get("attempts")
        require(isinstance(attempts, list) and len(attempts) >= 2, f"{entry_id}: at least two materialization attempts required")
        methods = {attempt.get("method") for attempt in attempts if isinstance(attempt, dict)}
        require({"GitHub.fetch_file", "GitHub.fetch_blob"}.issubset(methods), f"{entry_id}: materialization methods incomplete")
        blob_shas = {attempt.get("blob_sha") for attempt in attempts if isinstance(attempt, dict)}
        require(len(blob_shas) == 1 and all(isinstance(value, str) and HEX40.fullmatch(value) for value in blob_shas), f"{entry_id}: blob identity mismatch")
        require(all(attempt.get("result") == "TRUNCATED_RESPONSE" for attempt in attempts), f"{entry_id}: attempt result mismatch")

        boundary = entry.get("observed_boundary")
        require(isinstance(boundary, dict), f"{entry_id}: observed boundary required")
        require(boundary.get("partial_state_observed") is True, f"{entry_id}: PARTIAL observation required")
        require(boundary.get("claim_allowed_false_observed") is True, f"{entry_id}: false claim boundary observation required")
        require(boundary.get("full_content_observed") is False, f"{entry_id}: full content must remain unobserved")
        require(boundary.get("semantic_disposition_allowed") is False, f"{entry_id}: semantic disposition must remain forbidden")
        fields = boundary.get("root_fields_observed")
        require(isinstance(fields, list) and {"scope", "repositories"}.issubset(set(fields)), f"{entry_id}: observed root fields incomplete")

    derived = residual.get("derived")
    require(isinstance(derived, dict), "derived required")
    require(derived.get("residual_count") == len(entries), "derived residual count mismatch")
    require(derived.get("token_vazio_ids") == expected_ids, "derived TOKEN_VAZIO ids mismatch")
    require(derived.get("next_gate") == NEXT_GATE, "derived next gate mismatch")
    require(derived.get("claim_allowed") is False, "derived claim boundary mismatch")
    require(derived.get("certification_claim") is False, "derived certification boundary mismatch")
    require(derived.get("portfolio_exit_criteria_met") is False, "derived portfolio boundary mismatch")
    require(chain["token_vazio_count"] == len(entries), "chain residual count mismatch")
    require(chain["next_gate"] == NEXT_GATE, "chain and residual next gates differ")

    integrity = residual.get("integrity")
    require(isinstance(integrity, dict), "integrity required")
    require(integrity.get("algorithm") == "blake2b-256", "integrity algorithm mismatch")
    expected_digest = canonical_digest(residual)
    require(integrity.get("digest") == expected_digest, "integrity digest mismatch")

    return {
        "status": "PASS",
        "schema": SCHEMA,
        "residual_count": len(entries),
        "token_vazio_ids": expected_ids,
        "materialization_attempt_count": sum(len(entry["attempts"]) for entry in entries),
        "full_content_observed": False,
        "semantic_disposition_allowed": False,
        "next_gate": NEXT_GATE,
        "portfolio_exit_criteria_met": False,
        "claim_allowed": False,
        "certification_claim": False,
        "integrity_digest": expected_digest,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, default=Path("indices/CLAIM_REVIEW_RESIDUAL.json"))
    parser.add_argument("--head", type=Path, default=Path("indices/CLAIM_CONTRADICTION_HEAD.json"))
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args(argv)
    try:
        result = validate_residual(Path.cwd(), load_json(args.residual), load_json(args.head))
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
