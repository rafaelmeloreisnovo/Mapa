#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_claim_vocabulary import ClaimValidationError, load_json, validate_policy

SCHEMA = "mapa.claim-discovery-precision.v1"
BOUNDARY_TEMPLATE = r"(?<![A-Z0-9_]){token}(?![A-Z0-9_])"


class DiscoveryPrecisionError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DiscoveryPrecisionError(message)


def _is_excluded(relative: Path, excluded_paths: list[str]) -> bool:
    posix = relative.as_posix()
    return any(
        posix == prefix or posix.startswith(prefix.rstrip("/") + "/")
        for prefix in excluded_paths
    )


def token_counts(text: str, token: str) -> dict[str, int]:
    upper = text.upper()
    substring = upper.count(token)
    exact = len(
        re.findall(
            BOUNDARY_TEMPLATE.format(token=re.escape(token)),
            upper,
        )
    )
    return {
        "substring_count": substring,
        "exact_count": exact,
        "lexical_false_positive_count": max(substring - exact, 0),
    }


def validate_known_resolution(root: Path) -> dict[str, Any]:
    path = root / "indices/CLAIM_REVIEW_RESOLUTION_CC028.json"
    resolution = load_json(path)
    require(resolution.get("schema") == "mapa.claim-review-resolution.v1", "CC028 resolution schema mismatch")
    require(resolution.get("entry_id") == "CC028", "CC028 resolution id mismatch")
    require(resolution.get("path") == "indices/REPOSITORY_INVENTORY.json", "CC028 source path mismatch")
    scan = resolution.get("token_scan")
    require(isinstance(scan, dict), "CC028 token scan required")
    require(scan.get("false_positive_source") == "completeness_ratio", "CC028 false-positive source mismatch")
    require(scan.get("substring_occurrences") == {"COMPLETE": 1}, "CC028 substring count mismatch")
    require(
        scan.get("strong_token_counts")
        == {"ALIGNED": 0, "CERTIFIED": 0, "COMPLETE": 0, "COMPLIANT": 0},
        "CC028 exact token counts mismatch",
    )
    require(scan.get("exact_claim_token_absent") is True, "CC028 exact-token absence not sealed")
    materialization = resolution.get("materialization")
    require(isinstance(materialization, dict), "CC028 materialization required")
    require(materialization.get("identity_verified") is True, "CC028 identity not verified")
    require(materialization.get("json_parse_status") == "PASS", "CC028 JSON parse not proven")
    require(materialization.get("canonical_digest_match") is True, "CC028 canonical digest mismatch")
    return {
        "status": "PASS",
        "entry_id": "CC028",
        "source_path": "indices/REPOSITORY_INVENTORY.json",
        "false_positive_source": "completeness_ratio",
        "substring_complete_count": 1,
        "exact_complete_count": 0,
        "resolution_digest": resolution["integrity"]["digest"],
    }


def scan_discovery_precision(
    root: Path,
    policy: dict[str, Any],
    *,
    max_bytes: int = 2_000_000,
) -> dict[str, Any]:
    policy_result = validate_policy(policy)
    extensions = {str(value).lower() for value in policy["scan_extensions"]}
    excluded_paths = [str(value) for value in policy["excluded_paths"]]
    tokens = sorted(str(value).upper() for value in policy["strong_states"])

    files_scanned = 0
    files_skipped_by_size = 0
    unreadable_files: list[dict[str, str]] = []
    lexical_rows: list[dict[str, Any]] = []
    exact_file_count = 0
    token_totals = {
        token: {
            "substring_count": 0,
            "exact_count": 0,
            "lexical_false_positive_count": 0,
        }
        for token in tokens
    }

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if _is_excluded(relative, excluded_paths):
            continue
        if path.suffix.lower() not in extensions:
            continue
        try:
            size = path.stat().st_size
        except OSError as exc:
            unreadable_files.append({"path": relative.as_posix(), "error": str(exc)})
            continue
        if size > max_bytes:
            files_skipped_by_size += 1
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            unreadable_files.append({"path": relative.as_posix(), "error": str(exc)})
            continue

        files_scanned += 1
        file_exact = False
        false_tokens: dict[str, dict[str, int]] = {}
        for token in tokens:
            counts = token_counts(text, token)
            for key, value in counts.items():
                token_totals[token][key] += value
            if counts["exact_count"]:
                file_exact = True
            if counts["lexical_false_positive_count"]:
                false_tokens[token] = counts
        if file_exact:
            exact_file_count += 1
        if false_tokens:
            lexical_rows.append(
                {
                    "path": relative.as_posix(),
                    "tokens": false_tokens,
                }
            )

    known = validate_known_resolution(root)
    false_positive_total = sum(
        values["lexical_false_positive_count"] for values in token_totals.values()
    )
    return {
        "status": "PASS" if not unreadable_files else "FAIL",
        "schema": SCHEMA,
        "gap_id": policy["gap_id"],
        "scope_repository": policy["authority_repository"],
        "policy_status": policy_result["status"],
        "files_scanned": files_scanned,
        "files_skipped_by_size": files_skipped_by_size,
        "unreadable_file_count": len(unreadable_files),
        "unreadable_files": unreadable_files[:100],
        "strong_tokens": tokens,
        "token_totals": token_totals,
        "files_with_exact_strong_token": exact_file_count,
        "files_with_lexical_false_positive": len(lexical_rows),
        "lexical_false_positive_count": false_positive_total,
        "lexical_false_positives": lexical_rows[:100],
        "lexical_false_positives_truncated": len(lexical_rows) > 100,
        "known_resolution": known,
        "discovery_rule": "substring discovery is triage only; exact boundary token controls semantic review",
        "portfolio_exit_criteria_met": False,
        "claim_allowed": False,
        "certification_claim": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--policy",
        type=Path,
        default=Path("indices/CLAIM_VOCABULARY_POLICY.json"),
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--max-bytes", type=int, default=2_000_000)
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args(argv)
    try:
        result = scan_discovery_precision(
            args.root,
            load_json(args.policy),
            max_bytes=args.max_bytes,
        )
    except (ClaimValidationError, DiscoveryPrecisionError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    text = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
