#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = "mapa.claim-review-resolution.v1"
AUTHORITY = "rafaelmeloreisnovo/Mapa"
ENTRY_ID = "CC028"
SOURCE_PATH = "indices/REPOSITORY_INVENTORY.json"
SOURCE_COMMIT = "4016c51e024573a3875457fceb6d05926e07a07b"
GIT_BLOB_SHA1 = "b43554096f00c0918997dd9f9b11787cec4d4e52"
SHA256 = "b19d27084e5be35a2597f07346450745abfd7084c0a831b48e0eef4c57058e02"
CANONICAL_BLAKE2B = "204b310de7ecbfc0e4df316d126748b03cb4ed624a3e0eff8914a3a1e8018d48"
HISTORICAL_RESIDUAL_DIGEST = "e345bf4687e0553d5da0589d73a86cfc75e08215bbc26be4ac82f07e5aead9bf"
NEXT_GATE = "OBSERVABLE_SCANNER_RECEIPT_AND_SCOPE_REFRESH"
LINE_RANGES = [[1, 80], [81, 160], [161, 240], [241, 320], [321, 400], [401, 437]]
TOP_LEVEL_KEYS = [
    "schema",
    "schema_version",
    "generated_at",
    "inventory_source",
    "collection_method",
    "scope",
    "statistics",
    "repositories",
    "absence_ledger",
    "integrity",
]
STRONG_TOKEN_COUNTS = {
    "ALIGNED": 0,
    "CERTIFIED": 0,
    "COMPLETE": 0,
    "COMPLIANT": 0,
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class ResolutionContractError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ResolutionContractError(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ResolutionContractError(f"{path}: {exc}") from exc
    require(isinstance(value, dict), "resolution root must be an object")
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


def validate(data: dict[str, Any]) -> dict[str, Any]:
    require(data.get("schema") == SCHEMA, "invalid resolution schema")
    require(data.get("authority_repository") == AUTHORITY, "authority mismatch")
    require(data.get("gap_id") == "G006", "G006 scope required")
    require(data.get("entry_id") == ENTRY_ID, "entry id mismatch")
    require(data.get("path") == SOURCE_PATH, "source path mismatch")
    require(data.get("source_commit") == SOURCE_COMMIT, "source commit mismatch")
    require(data.get("generated_on") == "2026-07-21", "resolution date mismatch")

    boundaries = data.get("boundaries")
    require(isinstance(boundaries, dict), "boundaries required")
    expected_boundary_keys = {
        "automatic_claim_promotion",
        "automatic_portfolio_closure",
        "certification_claim",
        "claim_allowed",
        "portfolio_exit_criteria_met",
        "remote_runner_pass_inferred",
    }
    require(set(boundaries) == expected_boundary_keys, "resolution boundary coverage mismatch")
    for key in sorted(expected_boundary_keys):
        require(boundaries.get(key) is False, f"boundary {key} must remain false")

    decision = data.get("decision")
    require(isinstance(decision, dict), "decision required")
    require(decision.get("from_state") == "TOKEN_VAZIO", "decision source state mismatch")
    require(decision.get("to_state") == "REVIEWED_SAFE", "decision target state mismatch")
    require(decision.get("disposition") == "SAFE_EXACT_TOKEN_ABSENCE", "decision disposition mismatch")
    require(decision.get("claim_allowed") is False, "decision claim boundary mismatch")
    require(decision.get("certification_claim") is False, "decision certification boundary mismatch")
    rationale = decision.get("rationale")
    require(isinstance(rationale, str) and len(rationale.strip()) >= 120, "decision rationale is insufficient")
    require("completeness_ratio" in rationale, "decision rationale lacks false-positive cause")

    historical = data.get("historical_residual")
    require(isinstance(historical, dict), "historical residual reference required")
    require(historical.get("path") == "indices/CLAIM_REVIEW_RESIDUAL.json", "historical residual path mismatch")
    require(historical.get("digest_blake2b_256") == HISTORICAL_RESIDUAL_DIGEST, "historical residual digest mismatch")
    require(historical.get("state") == "HISTORICAL_RESIDUAL_PRESERVED", "historical preservation state mismatch")

    materialization = data.get("materialization")
    require(isinstance(materialization, dict), "materialization required")
    require(materialization.get("method") == "GITHUB_CONTENT_BASE64_RANGED_RECONSTRUCTION", "materialization method mismatch")
    require(materialization.get("encoding") == "base64", "materialization encoding mismatch")
    require(materialization.get("encoded_line_count") == 437, "encoded line count mismatch")
    require(materialization.get("line_ranges") == LINE_RANGES, "Base64 line ranges mismatch")
    require(materialization.get("decoded_size_bytes") == 19542, "decoded size mismatch")
    require(materialization.get("git_blob_sha1") == GIT_BLOB_SHA1, "Git blob SHA-1 mismatch")
    require(materialization.get("sha256") == SHA256, "SHA-256 mismatch")
    require(materialization.get("identity_verified") is True, "Git identity not verified")
    require(materialization.get("json_parse_status") == "PASS", "JSON parse not proven")
    require(materialization.get("repository_count") == 41, "repository count mismatch")
    require(materialization.get("scope_state") == "PARTIAL", "scope state mismatch")
    require(materialization.get("claim_allowed") is False, "materialization claim boundary mismatch")
    require(materialization.get("absence_state") == "TOKEN_VAZIO", "absence state mismatch")
    require(materialization.get("top_level_keys") == TOP_LEVEL_KEYS, "top-level key coverage mismatch")
    require(materialization.get("declared_canonical_blake2b_256") == CANONICAL_BLAKE2B, "declared canonical digest mismatch")
    require(materialization.get("calculated_canonical_blake2b_256") == CANONICAL_BLAKE2B, "calculated canonical digest mismatch")
    require(materialization.get("canonical_digest_match") is True, "canonical digest match must be true")

    scan = data.get("token_scan")
    require(isinstance(scan, dict), "token scan required")
    require(scan.get("boundary_regex") == "(?<![A-Z0-9_])TOKEN(?![A-Z0-9_])", "boundary regex mismatch")
    require(scan.get("normalization") == "unicode text decoded as UTF-8 then uppercased", "normalization mismatch")
    require(scan.get("strong_token_counts") == STRONG_TOKEN_COUNTS, "strong token counts mismatch")
    require(scan.get("pending_token_counts") == {"TOKEN_VAZIO": 1}, "pending token count mismatch")
    require(scan.get("substring_occurrences") == {"COMPLETE": 1}, "substring occurrence mismatch")
    require(scan.get("false_positive_source") == "completeness_ratio", "false-positive source mismatch")
    require(scan.get("exact_claim_token_absent") is True, "exact claim-token absence not proven")

    derived = data.get("derived")
    require(isinstance(derived, dict), "derived state required")
    require(derived == {
        "certification_claim": False,
        "claim_allowed": False,
        "current_token_vazio_count": 0,
        "next_gate": NEXT_GATE,
        "portfolio_exit_criteria_met": False,
        "resolved_count": 1,
    }, "derived state mismatch")

    integrity = data.get("integrity")
    require(isinstance(integrity, dict), "integrity required")
    require(integrity.get("algorithm") == "blake2b-256", "integrity algorithm mismatch")
    observed = integrity.get("digest")
    require(isinstance(observed, str) and HEX64.fullmatch(observed) is not None, "integrity digest format mismatch")
    expected = canonical_digest(data)
    require(observed == expected, "resolution integrity mismatch")

    return {
        "status": "PASS",
        "schema": SCHEMA,
        "entry_id": ENTRY_ID,
        "source_commit": SOURCE_COMMIT,
        "source_path": SOURCE_PATH,
        "boundary_count": len(boundaries),
        "all_boundaries_false": True,
        "decoded_size_bytes": 19542,
        "encoded_line_count": 437,
        "git_blob_sha1": GIT_BLOB_SHA1,
        "sha256": SHA256,
        "canonical_blake2b_256": CANONICAL_BLAKE2B,
        "exact_strong_token_count": 0,
        "complete_substring_count": 1,
        "false_positive_source": "completeness_ratio",
        "historical_residual_preserved": True,
        "current_token_vazio_count": 0,
        "next_gate": NEXT_GATE,
        "portfolio_exit_criteria_met": False,
        "claim_allowed": False,
        "certification_claim": False,
        "integrity_digest": expected,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("indices/CLAIM_REVIEW_RESOLUTION_CC028.json"),
    )
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args(argv)
    try:
        result = validate(load(args.path))
    except ResolutionContractError as exc:
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
