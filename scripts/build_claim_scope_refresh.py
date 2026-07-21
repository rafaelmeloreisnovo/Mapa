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


class ScopeRefreshError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ScopeRefreshError(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ScopeRefreshError(f"{path}: {exc}") from exc
    require(isinstance(value, dict), f"{path}: root must be an object")
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


def _normalize_exact_rows(rows: Any) -> dict[str, dict[str, int]]:
    require(isinstance(rows, list), "exact_token_files must be an array")
    output: dict[str, dict[str, int]] = {}
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"exact_token_files[{index}] must be an object")
        path = row.get("path")
        tokens = row.get("tokens")
        require(isinstance(path, str) and path, f"exact_token_files[{index}].path invalid")
        require(path not in output, f"duplicate exact-token path: {path}")
        require(isinstance(tokens, dict) and tokens, f"{path}: exact token counts required")
        normalized: dict[str, int] = {}
        for token, count in tokens.items():
            require(token in {"ALIGNED", "CERTIFIED", "COMPLETE", "COMPLIANT"}, f"{path}: unknown strong token")
            require(isinstance(count, int) and not isinstance(count, bool) and count > 0, f"{path}: invalid exact token count")
            normalized[token] = count
        output[path] = dict(sorted(normalized.items()))
    return output


def _normalize_contradictions(rows: Any) -> dict[str, dict[str, list[str]]]:
    require(isinstance(rows, list), "warnings must be an array")
    output: dict[str, dict[str, list[str]]] = {}
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"warnings[{index}] must be an object")
        require(row.get("class") == "POTENTIAL_PROSE_CONTRADICTION", f"warnings[{index}]: unknown warning class")
        path = row.get("path")
        require(isinstance(path, str) and path, f"warnings[{index}].path invalid")
        require(path not in output, f"duplicate contradiction path: {path}")
        strong = row.get("strong_tokens")
        pending = row.get("pending_tokens")
        require(isinstance(strong, list) and strong, f"{path}: strong tokens required")
        require(isinstance(pending, list) and pending, f"{path}: pending tokens required")
        output[path] = {
            "strong_tokens": sorted(set(str(value) for value in strong)),
            "pending_tokens": sorted(set(str(value) for value in pending)),
        }
    return output


def build_refresh(
    *,
    ledger: dict[str, Any],
    head: dict[str, Any],
    claim_scan: dict[str, Any],
    precision: dict[str, Any],
    current_commit: str,
) -> dict[str, Any]:
    require(HEX40.fullmatch(current_commit) is not None, "current commit must be 40 lowercase hex")
    require(ledger.get("schema") == "mapa.claim-contradiction-ledger.v1", "ledger schema mismatch")
    require(head.get("schema") == "mapa.claim-contradiction-head.v1", "head schema mismatch")
    require(claim_scan.get("schema") == "mapa.claim-vocabulary-scan.v1", "claim scan schema mismatch")
    require(precision.get("schema") == "mapa.claim-discovery-precision.v1", "precision schema mismatch")
    require(claim_scan.get("status") == "PASS", "claim scan must pass structurally")
    require(precision.get("status") == "PASS", "precision scan must pass structurally")
    require(claim_scan.get("claim_allowed") is False, "claim scan boundary mismatch")
    require(precision.get("claim_allowed") is False, "precision boundary mismatch")
    require(head.get("derived", {}).get("claim_allowed") is False, "head boundary mismatch")
    require(head.get("derived", {}).get("reviewed_safe_count") == 36, "baseline head must contain 36 reviewed-safe candidates")
    require(head.get("derived", {}).get("token_vazio_count") == 0, "baseline head has unresolved candidate")
    require(precision.get("exact_token_files_truncated") is False, "exact-token file list is truncated")
    require(claim_scan.get("warnings_truncated") is False, "claim warning list is truncated")
    require(precision.get("unreadable_file_count") == 0, "precision scan contains unreadable files")
    require(claim_scan.get("explicit_claim_error_count") == 0, "explicit claim errors block refresh")

    entries = ledger.get("entries")
    require(isinstance(entries, list) and entries, "ledger entries required")
    baseline_by_path: dict[str, str] = {}
    for index, entry in enumerate(entries):
        require(isinstance(entry, dict), f"ledger entries[{index}] must be an object")
        entry_id = entry.get("id")
        path = entry.get("path")
        require(isinstance(entry_id, str) and entry_id, f"ledger entries[{index}].id invalid")
        require(isinstance(path, str) and path, f"ledger entries[{index}].path invalid")
        require(path not in baseline_by_path, f"duplicate baseline path: {path}")
        baseline_by_path[path] = entry_id
    require(len(baseline_by_path) == 36, "baseline candidate count mismatch")

    exact_by_path = _normalize_exact_rows(precision.get("exact_token_files"))
    contradiction_by_path = _normalize_contradictions(claim_scan.get("warnings"))
    current_paths = sorted(set(exact_by_path) | set(contradiction_by_path))
    baseline_paths = set(baseline_by_path)
    current_path_set = set(current_paths)
    known_paths = sorted(current_path_set & baseline_paths)
    new_paths = sorted(current_path_set - baseline_paths)
    baseline_without_current_signal = sorted(baseline_paths - current_path_set)

    new_candidates: list[dict[str, Any]] = []
    for path in new_paths:
        new_candidates.append(
            {
                "id": stable_candidate_id(path),
                "path": path,
                "state": "TOKEN_VAZIO",
                "owner_role": "R12",
                "claim_allowed": False,
                "exact_tokens": exact_by_path.get(path, {}),
                "contradiction": contradiction_by_path.get(path),
                "reason": "NEW_PATH_AFTER_PINNED_BASELINE_REQUIRES_CONTIGUOUS_REVIEW",
                "exit_criteria": [
                    "read the complete file at the current pinned commit",
                    "classify every exact strong-token occurrence in context",
                    "preserve implementation, execution and evidence boundaries",
                    "append a review batch without rewriting the baseline ledger",
                ],
            }
        )

    baseline_signal_rows = [
        {
            "entry_id": baseline_by_path[path],
            "path": path,
            "exact_tokens": exact_by_path.get(path, {}),
            "contradiction": contradiction_by_path.get(path),
        }
        for path in known_paths
    ]

    policy_excluded_paths = precision.get("policy_excluded_paths")
    if policy_excluded_paths is None:
        policy_excluded_paths = "NOT_EXPOSED_BY_PRECISION_REPORT"

    report = {
        "schema": SCHEMA,
        "status": "PASS",
        "gap_id": "G006",
        "authority_repository": "rafaelmeloreisnovo/Mapa",
        "baseline": {
            "source_commit": ledger.get("source_snapshot", {}).get("commit"),
            "candidate_count": len(baseline_by_path),
            "reviewed_safe_count": head.get("derived", {}).get("reviewed_safe_count"),
            "reviewed_blocking_count": head.get("derived", {}).get("reviewed_blocking_count"),
            "token_vazio_count": head.get("derived", {}).get("token_vazio_count"),
            "ledger_digest": ledger.get("integrity", {}).get("digest"),
            "head_digest": head.get("integrity", {}).get("digest"),
        },
        "current_scan": {
            "commit": current_commit,
            "scope": "POLICY_FILTERED_CURRENT_TREE",
            "files_scanned": precision.get("files_scanned"),
            "files_skipped_by_size": precision.get("files_skipped_by_size"),
            "exact_token_file_count": len(exact_by_path),
            "contradiction_file_count": len(contradiction_by_path),
            "candidate_path_count": len(current_paths),
            "policy_excluded_paths": policy_excluded_paths,
        },
        "derived": {
            "known_baseline_signal_count": len(known_paths),
            "new_candidate_count": len(new_candidates),
            "baseline_without_current_signal_count": len(baseline_without_current_signal),
            "review_required": bool(new_candidates),
            "filtered_scope_refresh_complete": False,
            "full_byte_repository_scan_proven": False,
            "portfolio_exit_criteria_met": False,
            "claim_allowed": False,
            "certification_claim": False,
            "next_gate": (
                "REVIEW_NEW_SCOPE_CANDIDATES_AND_PRODUCE_FULL_BYTE_RECEIPT"
                if new_candidates
                else "PRODUCE_FULL_BYTE_REPOSITORY_RECEIPT"
            ),
        },
        "known_baseline_signals": baseline_signal_rows,
        "new_candidates": new_candidates,
        "baseline_without_current_signal": [
            {"entry_id": baseline_by_path[path], "path": path}
            for path in baseline_without_current_signal
        ],
        "boundaries": {
            "missing_current_signal_means_resolved": False,
            "new_control_file_is_automatically_safe": False,
            "filtered_scan_equals_full_scan": False,
            "automatic_claim_promotion": False,
            "automatic_portfolio_closure": False,
            "claim_allowed": False,
            "certification_claim": False,
        },
        "integrity": {
            "algorithm": "blake2b-256",
            "canonicalization": "json-sort-keys-utf8; integrity.digest blanked",
            "digest": "",
        },
    }
    report["integrity"]["digest"] = canonical_digest(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=Path("indices/CLAIM_CONTRADICTION_LEDGER.json"))
    parser.add_argument("--head", type=Path, default=Path("indices/CLAIM_CONTRADICTION_HEAD.json"))
    parser.add_argument("--claim-scan", type=Path, required=True)
    parser.add_argument("--precision", type=Path, required=True)
    parser.add_argument("--current-commit", required=True)
    parser.add_argument("--write-report", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = build_refresh(
            ledger=load(args.ledger),
            head=load(args.head),
            claim_scan=load(args.claim_scan),
            precision=load(args.precision),
            current_commit=args.current_commit,
        )
    except ScopeRefreshError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    text = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    args.write_report.parent.mkdir(parents=True, exist_ok=True)
    args.write_report.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
