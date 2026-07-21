#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = "mapa.claim-contradiction-ledger.v1"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^CC[0-9]{3}$")


class LedgerValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise LedgerValidationError(message)


def load(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LedgerValidationError(f"{path}: {exc}") from exc
    require(isinstance(data, dict), "ledger root must be an object")
    return data


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
    require(data.get("schema") == SCHEMA, "invalid ledger schema")
    require(data.get("authority_repository") == "rafaelmeloreisnovo/Mapa", "Mapa authority required")
    require(data.get("gap_id") == "G006", "G006 scope required")
    require(
        data.get("assessment_type")
        == "BOUNDED_GITHUB_CODE_SEARCH_SNAPSHOT_NOT_FULL_REPOSITORY_SCAN",
        "assessment must remain bounded",
    )
    require(data.get("claim_allowed") is False, "claim_allowed must remain false")
    require(data.get("certification_claim") is False, "certification claim is forbidden")

    snapshot = data.get("source_snapshot")
    require(isinstance(snapshot, dict), "source_snapshot required")
    require(snapshot.get("repository") == "rafaelmeloreisnovo/Mapa", "snapshot repository mismatch")
    require(isinstance(snapshot.get("commit"), str) and HEX40.fullmatch(snapshot["commit"]), "snapshot commit must be SHA-1")
    require(isinstance(snapshot.get("query"), str) and snapshot["query"], "snapshot query required")
    require(snapshot.get("exhaustive") is False, "code-search snapshot must not be called exhaustive")
    require(isinstance(snapshot.get("limitations"), list) and snapshot["limitations"], "snapshot limitations required")

    policy = data.get("review_policy")
    require(isinstance(policy, dict), "review_policy required")
    allowed_states = set(policy.get("allowed_review_states", []))
    safe_dispositions = set(policy.get("safe_dispositions", []))
    blocking_dispositions = set(policy.get("blocking_dispositions", []))
    require(allowed_states == {"REVIEWED_SAFE", "REVIEWED_BLOCKING", "TOKEN_VAZIO"}, "review state set mismatch")
    require(bool(safe_dispositions), "safe dispositions required")
    require(bool(blocking_dispositions), "blocking dispositions required")
    require(policy.get("token_vazio_is_zero") is False, "TOKEN_VAZIO cannot be zero")
    require(policy.get("automatic_dismissal") is False, "automatic dismissal forbidden")
    require(policy.get("automatic_rewrite") is False, "automatic rewrite forbidden")

    entries = data.get("entries")
    require(isinstance(entries, list) and entries, "entries required")
    ids: set[str] = set()
    paths: set[str] = set()
    counts = {"REVIEWED_SAFE": 0, "REVIEWED_BLOCKING": 0, "TOKEN_VAZIO": 0}

    for index, entry in enumerate(entries):
        require(isinstance(entry, dict), f"entries[{index}] must be an object")
        entry_id = entry.get("id")
        path = entry.get("path")
        state = entry.get("review_state")
        disposition = entry.get("disposition")
        require(isinstance(entry_id, str) and ID_RE.fullmatch(entry_id), f"entries[{index}].id invalid")
        require(entry_id not in ids, f"duplicate entry id: {entry_id}")
        ids.add(entry_id)
        require(isinstance(path, str) and path and not path.startswith("/"), f"{entry_id}.path invalid")
        require(path not in paths, f"duplicate candidate path: {path}")
        paths.add(path)
        require(state in allowed_states, f"{entry_id}.review_state invalid")
        require(isinstance(disposition, str) and disposition, f"{entry_id}.disposition required")
        require(isinstance(entry.get("rationale"), str) and entry["rationale"], f"{entry_id}.rationale required")
        require(entry.get("owner_role") == "R12", f"{entry_id}.owner_role must remain R12")
        require(entry.get("claim_allowed") is False, f"{entry_id}.claim_allowed must be false")
        counts[state] += 1

        if state == "REVIEWED_SAFE":
            require(disposition in safe_dispositions, f"{entry_id}: unknown safe disposition")
            pointer = entry.get("evidence_pointer")
            require(isinstance(pointer, str) and "@" in pointer, f"{entry_id}: evidence pointer required")
            pinned_path, pinned_commit = pointer.rsplit("@", 1)
            require(pinned_path == path, f"{entry_id}: evidence path mismatch")
            require(pinned_commit == snapshot["commit"], f"{entry_id}: evidence commit mismatch")
        elif state == "REVIEWED_BLOCKING":
            require(disposition in blocking_dispositions, f"{entry_id}: unknown blocking disposition")
            require(isinstance(entry.get("exit_criteria"), list) and entry["exit_criteria"], f"{entry_id}: blocking exit criteria required")
        else:
            require(disposition == "UNREVIEWED_INDEX_CANDIDATE", f"{entry_id}: TOKEN_VAZIO disposition mismatch")
            criteria = entry.get("exit_criteria")
            require(isinstance(criteria, list) and len(criteria) >= 3, f"{entry_id}: review exit criteria required")
            require("evidence_pointer" not in entry, f"{entry_id}: unreviewed candidate cannot claim evidence pointer")

    candidate_count = snapshot.get("candidate_count")
    require(candidate_count == len(entries), "snapshot candidate count mismatch")

    derived = data.get("derived")
    require(isinstance(derived, dict), "derived required")
    require(derived.get("candidate_count") == len(entries), "derived candidate count mismatch")
    require(derived.get("reviewed_safe_count") == counts["REVIEWED_SAFE"], "derived safe count mismatch")
    require(derived.get("reviewed_blocking_count") == counts["REVIEWED_BLOCKING"], "derived blocking count mismatch")
    require(derived.get("token_vazio_count") == counts["TOKEN_VAZIO"], "derived TOKEN_VAZIO count mismatch")
    require(sum(counts.values()) == len(entries), "review arithmetic mismatch")
    require(derived.get("portfolio_exit_criteria_met") is False, "portfolio exit criteria must remain false")
    require(derived.get("claim_allowed") is False, "derived claim boundary mismatch")
    require(derived.get("certification_claim") is False, "derived certification boundary mismatch")
    require(derived.get("next_gate") == "CONTIGUOUS_REVIEW_AND_SCANNER_RECEIPT", "next gate mismatch")

    integrity = data.get("integrity")
    require(isinstance(integrity, dict), "integrity required")
    require(integrity.get("algorithm") == "blake2b-256", "integrity algorithm mismatch")
    observed = integrity.get("digest")
    require(isinstance(observed, str) and HEX64.fullmatch(observed), "integrity digest invalid")
    expected = canonical_digest(data)
    require(observed == expected, "integrity digest mismatch")

    return {
        "status": "PASS",
        "schema": SCHEMA,
        "candidate_count": len(entries),
        "reviewed_safe_count": counts["REVIEWED_SAFE"],
        "reviewed_blocking_count": counts["REVIEWED_BLOCKING"],
        "token_vazio_count": counts["TOKEN_VAZIO"],
        "snapshot_exhaustive": False,
        "portfolio_exit_criteria_met": False,
        "claim_allowed": False,
        "certification_claim": False,
        "integrity_digest": expected,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, default=Path("indices/CLAIM_CONTRADICTION_LEDGER.json"))
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args(argv)
    try:
        result = validate(load(args.path))
    except LedgerValidationError as exc:
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
