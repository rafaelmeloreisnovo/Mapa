#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_claim_contradiction_ledger import (
    LedgerValidationError,
    load as load_ledger,
    validate as validate_ledger,
)

HEAD_SCHEMA = "mapa.claim-contradiction-head.v1"
BATCH_SCHEMA = "mapa.claim-review-batch.v1"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
SAFE_DISPOSITIONS = {
    "SAFE_NEGATION",
    "SAFE_BOUNDED_CONTEXT",
    "SAFE_VALIDATOR_LITERAL",
    "SAFE_POLICY_REFERENCE",
    "SAFE_SEMANTIC_DEFINITION",
    "SAFE_MACHINE_BOUNDARY",
    "SAFE_NEGATIVE_CONTROL",
    "SAFE_ORGANIZATIONAL_LABEL",
    "SAFE_SCHEMA_LITERAL",
    "SAFE_TEST_FIXTURE",
}
BLOCKING_DISPOSITIONS = {
    "EXPLICIT_CLAIM_MISSING_CHAIN",
    "AMBIGUOUS_PROMOTIONAL_LANGUAGE",
    "CONTRADICTS_PENDING_STATE",
}
NEXT_GATE = "MATERIALIZE_FULL_CC028_AND_OBSERVABLE_SCANNER_RECEIPT"


class ChainValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ChainValidationError(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ChainValidationError(f"{path}: {exc}") from exc
    require(isinstance(value, dict), f"{path}: root must be an object")
    return value


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


def _validate_boundaries(boundaries: Any, *, head: bool) -> None:
    require(isinstance(boundaries, dict), "boundaries required")
    false_keys = {
        "automatic_dismissal",
        "automatic_rewrite",
        "token_vazio_is_zero",
        "portfolio_exit_criteria_met",
        "claim_allowed",
        "certification_claim",
    }
    if not head:
        false_keys.add("unread_file_can_be_reviewed_safe")
    for key in false_keys:
        require(boundaries.get(key) is False, f"boundary {key} must be false")
    if head:
        require(boundaries.get("base_ledger_is_immutable") is True, "base ledger must be immutable")
        require(boundaries.get("batches_are_append_only") is True, "review batches must be append-only")


def _state_counts(states: dict[str, str]) -> dict[str, int]:
    return {
        "reviewed_safe_count": sum(state == "REVIEWED_SAFE" for state in states.values()),
        "reviewed_blocking_count": sum(state == "REVIEWED_BLOCKING" for state in states.values()),
        "token_vazio_count": sum(state == "TOKEN_VAZIO" for state in states.values()),
    }


def validate_batch(
    batch: dict[str, Any],
    *,
    ledger: dict[str, Any],
    states: dict[str, str],
    paths: dict[str, str],
    seen_decisions: set[str],
) -> dict[str, Any]:
    require(batch.get("schema") == BATCH_SCHEMA, "invalid review batch schema")
    require(batch.get("authority_repository") == "rafaelmeloreisnovo/Mapa", "batch authority mismatch")
    require(batch.get("gap_id") == "G006", "batch G006 scope required")
    require(batch.get("review_method") == "CONTIGUOUS_FILE_REVIEW_AT_PINNED_GIT_COMMIT", "review method mismatch")
    require(batch.get("reviewer_role") == "R12", "batch reviewer role mismatch")
    source_commit = batch.get("source_commit")
    require(isinstance(source_commit, str) and HEX40.fullmatch(source_commit), "batch source commit invalid")
    require(source_commit == ledger["source_snapshot"]["commit"], "batch source commit differs from ledger snapshot")
    _validate_boundaries(batch.get("boundaries"), head=False)

    source = batch.get("source_ledger")
    require(isinstance(source, dict), "source_ledger required")
    require(source.get("path") == "indices/CLAIM_CONTRADICTION_LEDGER.json", "source ledger path mismatch")
    require(source.get("digest_blake2b_256") == ledger["integrity"]["digest"], "source ledger digest mismatch")
    require(source.get("candidate_count") == len(ledger["entries"]), "source candidate count mismatch")

    decisions = batch.get("decisions")
    require(isinstance(decisions, list) and decisions, "review decisions required")
    safe = 0
    blocking = 0
    for index, decision in enumerate(decisions):
        require(isinstance(decision, dict), f"decisions[{index}] must be an object")
        entry_id = decision.get("entry_id")
        require(entry_id in states, f"unknown ledger entry: {entry_id}")
        require(entry_id not in seen_decisions, f"duplicate review transition: {entry_id}")
        seen_decisions.add(entry_id)
        require(decision.get("path") == paths[entry_id], f"{entry_id}: path mismatch")
        require(decision.get("from_state") == states[entry_id], f"{entry_id}: from_state mismatch")
        require(states[entry_id] == "TOKEN_VAZIO", f"{entry_id}: only TOKEN_VAZIO may transition")
        require(decision.get("reviewer_role") == "R12", f"{entry_id}: reviewer role mismatch")
        require(decision.get("claim_allowed") is False, f"{entry_id}: claim_allowed must remain false")
        rationale = decision.get("rationale")
        require(isinstance(rationale, str) and len(rationale.strip()) >= 24, f"{entry_id}: rationale too weak")
        pointer = decision.get("evidence_pointer")
        require(isinstance(pointer, str) and "@" in pointer, f"{entry_id}: evidence pointer required")
        pointer_path, pointer_commit = pointer.rsplit("@", 1)
        require(pointer_path == paths[entry_id], f"{entry_id}: evidence path mismatch")
        require(pointer_commit == source_commit, f"{entry_id}: evidence commit mismatch")

        to_state = decision.get("to_state")
        disposition = decision.get("disposition")
        if to_state == "REVIEWED_SAFE":
            require(disposition in SAFE_DISPOSITIONS, f"{entry_id}: invalid safe disposition")
            safe += 1
        elif to_state == "REVIEWED_BLOCKING":
            require(disposition in BLOCKING_DISPOSITIONS, f"{entry_id}: invalid blocking disposition")
            criteria = decision.get("exit_criteria")
            require(isinstance(criteria, list) and criteria, f"{entry_id}: blocking exit criteria required")
            blocking += 1
        else:
            raise ChainValidationError(f"{entry_id}: invalid transition target")
        states[entry_id] = to_state

    counts = _state_counts(states)
    derived = batch.get("derived")
    require(isinstance(derived, dict), "batch derived required")
    require(derived.get("decision_count") == len(decisions), "batch decision count mismatch")
    require(derived.get("safe_transitions") == safe, "batch safe transition count mismatch")
    require(derived.get("blocking_transitions") == blocking, "batch blocking transition count mismatch")
    require(derived.get("result_reviewed_safe_count") == counts["reviewed_safe_count"], "batch resulting safe count mismatch")
    require(derived.get("result_reviewed_blocking_count") == counts["reviewed_blocking_count"], "batch resulting blocking count mismatch")
    require(derived.get("result_token_vazio_count") == counts["token_vazio_count"], "batch resulting TOKEN_VAZIO count mismatch")
    require(isinstance(derived.get("next_gate"), str) and derived["next_gate"], "batch next gate required")
    require(derived.get("portfolio_exit_criteria_met") is False, "batch cannot close portfolio")
    require(derived.get("claim_allowed") is False, "batch derived claim boundary mismatch")
    require(derived.get("certification_claim") is False, "batch derived certification boundary mismatch")

    expected = canonical_digest(batch)
    integrity = batch.get("integrity")
    require(isinstance(integrity, dict), "batch integrity required")
    require(integrity.get("algorithm") == "blake2b-256", "batch integrity algorithm mismatch")
    require(integrity.get("digest") == expected, "batch integrity digest mismatch")
    return {
        "batch_id": batch.get("batch_id"),
        "decision_count": len(decisions),
        "safe_transitions": safe,
        "blocking_transitions": blocking,
        **counts,
        "integrity_digest": expected,
    }


def validate_chain(root: Path, head: dict[str, Any]) -> dict[str, Any]:
    require(head.get("schema") == HEAD_SCHEMA, "invalid claim contradiction head schema")
    require(head.get("authority_repository") == "rafaelmeloreisnovo/Mapa", "head authority mismatch")
    require(head.get("gap_id") == "G006", "head G006 scope required")
    _validate_boundaries(head.get("boundaries"), head=True)

    base_ref = head.get("base_ledger")
    require(isinstance(base_ref, dict), "base_ledger reference required")
    base_path = root / str(base_ref.get("path", ""))
    ledger = load_ledger(base_path)
    try:
        ledger_result = validate_ledger(ledger)
    except LedgerValidationError as exc:
        raise ChainValidationError(f"base ledger invalid: {exc}") from exc
    require(base_ref.get("digest_blake2b_256") == ledger["integrity"]["digest"], "head base ledger digest mismatch")
    require(base_ref.get("candidate_count") == len(ledger["entries"]), "head base candidate count mismatch")

    states = {entry["id"]: entry["review_state"] for entry in ledger["entries"]}
    paths = {entry["id"]: entry["path"] for entry in ledger["entries"]}
    seen_decisions: set[str] = set()
    batch_reports: list[dict[str, Any]] = []
    refs = head.get("review_batches")
    require(isinstance(refs, list), "review_batches must be an array")
    seen_batch_ids: set[str] = set()

    for index, ref in enumerate(refs):
        require(isinstance(ref, dict), f"review_batches[{index}] must be an object")
        batch_id = ref.get("batch_id")
        require(isinstance(batch_id, str) and batch_id, f"review_batches[{index}].batch_id required")
        require(batch_id not in seen_batch_ids, f"duplicate batch id: {batch_id}")
        seen_batch_ids.add(batch_id)
        batch = load_json(root / str(ref.get("path", "")))
        require(batch.get("batch_id") == batch_id, f"{batch_id}: reference id mismatch")
        report = validate_batch(
            batch,
            ledger=ledger,
            states=states,
            paths=paths,
            seen_decisions=seen_decisions,
        )
        require(ref.get("digest_blake2b_256") == report["integrity_digest"], f"{batch_id}: reference digest mismatch")
        require(ref.get("decision_count") == report["decision_count"], f"{batch_id}: reference decision count mismatch")
        batch_reports.append(report)

    counts = _state_counts(states)
    candidate_count = len(states)
    require(sum(counts.values()) == candidate_count, "head state arithmetic mismatch")

    derived = head.get("derived")
    require(isinstance(derived, dict), "head derived required")
    expected_derived = {
        "candidate_count": candidate_count,
        "review_batch_count": len(refs),
        "review_decision_count": len(seen_decisions),
        **counts,
        "review_completion_ratio": round(
            (counts["reviewed_safe_count"] + counts["reviewed_blocking_count"]) / candidate_count,
            12,
        ),
        "portfolio_exit_criteria_met": False,
        "claim_allowed": False,
        "certification_claim": False,
        "next_gate": NEXT_GATE,
    }
    require(derived == expected_derived, "head derived state mismatch")

    integrity = head.get("integrity")
    require(isinstance(integrity, dict), "head integrity required")
    require(integrity.get("algorithm") == "blake2b-256", "head integrity algorithm mismatch")
    expected_head_digest = canonical_digest(head)
    require(integrity.get("digest") == expected_head_digest, "head integrity digest mismatch")

    return {
        "status": "PASS",
        "schema": HEAD_SCHEMA,
        "base_ledger_status": ledger_result["status"],
        "candidate_count": candidate_count,
        "review_batch_count": len(refs),
        "review_decision_count": len(seen_decisions),
        **counts,
        "review_completion_ratio": expected_derived["review_completion_ratio"],
        "batch_reports": batch_reports,
        "next_gate": NEXT_GATE,
        "portfolio_exit_criteria_met": False,
        "claim_allowed": False,
        "certification_claim": False,
        "head_integrity_digest": expected_head_digest,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--head", type=Path, default=Path("indices/CLAIM_CONTRADICTION_HEAD.json"))
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args(argv)
    try:
        result = validate_chain(Path.cwd(), load_json(args.head))
    except (ChainValidationError, LedgerValidationError) as exc:
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
