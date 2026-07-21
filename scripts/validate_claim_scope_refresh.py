#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = "mapa.claim-scope-refresh.v1"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^NCC-[0-9A-F]{12}$")


class ScopeRefreshValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ScopeRefreshValidationError(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ScopeRefreshValidationError(f"{path}: {exc}") from exc
    require(isinstance(value, dict), "scope refresh root must be an object")
    return value


def canonical_digest(data: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(data))
    clone.setdefault("integrity", {})["digest"] = ""
    raw = json.dumps(
        clone,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.blake2b(raw, digest_size=32).hexdigest()


def stable_candidate_id(path: str) -> str:
    return "NCC-" + hashlib.sha256(path.encode("utf-8")).hexdigest()[:12].upper()


def _unique_paths(rows: Any, label: str) -> dict[str, dict[str, Any]]:
    require(isinstance(rows, list), f"{label} must be an array")
    output: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"{label}[{index}] must be an object")
        path = row.get("path")
        require(isinstance(path, str) and path, f"{label}[{index}].path invalid")
        require(path not in output, f"duplicate path in {label}: {path}")
        output[path] = row
    return output


def validate(report: dict[str, Any]) -> dict[str, Any]:
    require(report.get("schema") == SCHEMA, "invalid scope refresh schema")
    require(report.get("status") == "PASS", "scope refresh status must be PASS")
    require(report.get("gap_id") == "G006", "G006 scope required")
    require(report.get("authority_repository") == "rafaelmeloreisnovo/Mapa", "authority mismatch")

    baseline = report.get("baseline")
    require(isinstance(baseline, dict), "baseline required")
    require(HEX40.fullmatch(str(baseline.get("source_commit", ""))) is not None, "baseline source commit invalid")
    require(baseline.get("candidate_count") == 36, "baseline candidate count mismatch")
    require(baseline.get("reviewed_safe_count") == 36, "baseline reviewed safe count mismatch")
    require(baseline.get("reviewed_blocking_count") == 0, "baseline blocking count mismatch")
    require(baseline.get("token_vazio_count") == 0, "baseline TOKEN_VAZIO count mismatch")
    require(HEX64.fullmatch(str(baseline.get("ledger_digest", ""))) is not None, "baseline ledger digest invalid")
    require(HEX64.fullmatch(str(baseline.get("head_digest", ""))) is not None, "baseline head digest invalid")

    current = report.get("current_scan")
    require(isinstance(current, dict), "current_scan required")
    require(HEX40.fullmatch(str(current.get("commit", ""))) is not None, "current scan commit invalid")
    require(current.get("scope") == "POLICY_FILTERED_CURRENT_TREE", "current scan scope mismatch")
    for key in (
        "files_scanned",
        "files_skipped_by_size",
        "exact_token_file_count",
        "contradiction_file_count",
        "candidate_path_count",
    ):
        value = current.get(key)
        require(isinstance(value, int) and not isinstance(value, bool) and value >= 0, f"current_scan.{key} invalid")

    known = _unique_paths(report.get("known_baseline_signals"), "known_baseline_signals")
    new = _unique_paths(report.get("new_candidates"), "new_candidates")
    missing = _unique_paths(report.get("baseline_without_current_signal"), "baseline_without_current_signal")
    require(not (set(known) & set(new)), "known and new paths overlap")
    require(not (set(known) & set(missing)), "known and missing paths overlap")
    require(not (set(new) & set(missing)), "new and missing paths overlap")
    require(len(known) + len(missing) == 36, "baseline path partition mismatch")
    require(current.get("candidate_path_count") == len(known) + len(new), "current candidate path arithmetic mismatch")

    known_ids: set[str] = set()
    for path, row in known.items():
        entry_id = row.get("entry_id")
        require(isinstance(entry_id, str) and re.fullmatch(r"^CC[0-9]{3}$", entry_id), f"{path}: baseline entry id invalid")
        require(entry_id not in known_ids, f"duplicate baseline entry id: {entry_id}")
        known_ids.add(entry_id)
        exact_tokens = row.get("exact_tokens")
        require(isinstance(exact_tokens, dict), f"{path}: exact_tokens must be an object")

    missing_ids: set[str] = set()
    for path, row in missing.items():
        entry_id = row.get("entry_id")
        require(isinstance(entry_id, str) and re.fullmatch(r"^CC[0-9]{3}$", entry_id), f"{path}: missing entry id invalid")
        require(entry_id not in missing_ids, f"duplicate missing entry id: {entry_id}")
        missing_ids.add(entry_id)
    require(not (known_ids & missing_ids), "baseline entry ids overlap between known and missing")
    require(len(known_ids | missing_ids) == 36, "baseline entry id coverage mismatch")

    new_ids: set[str] = set()
    for path, row in new.items():
        candidate_id = row.get("id")
        require(isinstance(candidate_id, str) and ID_RE.fullmatch(candidate_id), f"{path}: candidate id invalid")
        require(candidate_id == stable_candidate_id(path), f"{path}: candidate id is not deterministic")
        require(candidate_id not in new_ids, f"duplicate new candidate id: {candidate_id}")
        new_ids.add(candidate_id)
        require(row.get("state") == "TOKEN_VAZIO", f"{path}: new candidate state must be TOKEN_VAZIO")
        require(row.get("owner_role") == "R12", f"{path}: owner role mismatch")
        require(row.get("claim_allowed") is False, f"{path}: new candidate claim boundary mismatch")
        require(row.get("reason") == "NEW_PATH_AFTER_PINNED_BASELINE_REQUIRES_CONTIGUOUS_REVIEW", f"{path}: reason mismatch")
        criteria = row.get("exit_criteria")
        require(isinstance(criteria, list) and len(criteria) >= 4, f"{path}: exit criteria incomplete")
        exact_tokens = row.get("exact_tokens")
        contradiction = row.get("contradiction")
        require(isinstance(exact_tokens, dict), f"{path}: exact_tokens must be an object")
        require(exact_tokens or isinstance(contradiction, dict), f"{path}: no discovery evidence")

    derived = report.get("derived")
    require(isinstance(derived, dict), "derived required")
    require(derived.get("known_baseline_signal_count") == len(known), "known baseline count mismatch")
    require(derived.get("new_candidate_count") == len(new), "new candidate count mismatch")
    require(derived.get("baseline_without_current_signal_count") == len(missing), "missing baseline count mismatch")
    require(derived.get("review_required") is bool(new), "review_required mismatch")
    require(derived.get("filtered_scope_refresh_complete") is False, "filtered refresh cannot be complete")
    require(derived.get("full_byte_repository_scan_proven") is False, "full-byte scan cannot be inferred")
    require(derived.get("portfolio_exit_criteria_met") is False, "scope refresh cannot close portfolio")
    require(derived.get("claim_allowed") is False, "scope refresh claim boundary mismatch")
    require(derived.get("certification_claim") is False, "scope refresh certification boundary mismatch")
    expected_next = (
        "REVIEW_NEW_SCOPE_CANDIDATES_AND_PRODUCE_FULL_BYTE_RECEIPT"
        if new
        else "PRODUCE_FULL_BYTE_REPOSITORY_RECEIPT"
    )
    require(derived.get("next_gate") == expected_next, "scope refresh next gate mismatch")

    boundaries = report.get("boundaries")
    require(isinstance(boundaries, dict), "boundaries required")
    expected_boundary_keys = {
        "missing_current_signal_means_resolved",
        "new_control_file_is_automatically_safe",
        "filtered_scan_equals_full_scan",
        "automatic_claim_promotion",
        "automatic_portfolio_closure",
        "claim_allowed",
        "certification_claim",
    }
    require(set(boundaries) == expected_boundary_keys, "scope refresh boundary coverage mismatch")
    for key in sorted(expected_boundary_keys):
        require(boundaries.get(key) is False, f"boundary {key} must remain false")

    integrity = report.get("integrity")
    require(isinstance(integrity, dict), "integrity required")
    require(integrity.get("algorithm") == "blake2b-256", "integrity algorithm mismatch")
    observed = integrity.get("digest")
    require(isinstance(observed, str) and HEX64.fullmatch(observed) is not None, "integrity digest format mismatch")
    expected_digest = canonical_digest(report)
    require(observed == expected_digest, "scope refresh integrity mismatch")

    return {
        "status": "PASS",
        "schema": SCHEMA,
        "baseline_candidate_count": 36,
        "known_baseline_signal_count": len(known),
        "new_candidate_count": len(new),
        "baseline_without_current_signal_count": len(missing),
        "new_candidate_ids_deterministic": True,
        "all_new_candidates_token_vazio": True,
        "review_required": bool(new),
        "next_gate": expected_next,
        "filtered_scope_refresh_complete": False,
        "full_byte_repository_scan_proven": False,
        "portfolio_exit_criteria_met": False,
        "claim_allowed": False,
        "certification_claim": False,
        "integrity_digest": expected_digest,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args(argv)
    try:
        result = validate(load(args.path))
    except ScopeRefreshValidationError as exc:
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
