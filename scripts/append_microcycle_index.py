#!/usr/bin/env python3
"""Build a hash-chained append-only index for RAFAELIA microcycle receipts.

The index is itself an immutable GitHub Actions artifact. Each new workflow run
retrieves the latest index artifact for the same branch, verifies its self-hash
and entry chain, appends one current receipt, and uploads a new immutable index
artifact. No repository write or claim promotion is performed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

INDEX_SCHEMA = "rafaelia.microcycle-index.v1"
RECEIPT_SCHEMA = "rafaelia.adaptive-cycle-receipt.v1"


class MicrocycleIndexError(ValueError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise MicrocycleIndexError(f"{path}: root must be a JSON object")
    return value


def verify_embedded_hash(value: dict[str, Any], field: str) -> None:
    expected = value.get(field)
    if not isinstance(expected, str) or len(expected) != 64:
        raise MicrocycleIndexError(f"missing or malformed {field}")
    material = dict(value)
    material.pop(field, None)
    actual = sha256_value(material)
    if actual != expected:
        raise MicrocycleIndexError(
            f"{field} mismatch: expected {expected}, recalculated {actual}"
        )


def validate_receipt(receipt: dict[str, Any]) -> None:
    if receipt.get("schema") != RECEIPT_SCHEMA:
        raise MicrocycleIndexError("unsupported microcycle receipt schema")
    for field in (
        "claim_allowed",
        "publication_ready",
        "automatic_mutation",
        "automatic_merge",
    ):
        if receipt.get(field) is not False:
            raise MicrocycleIndexError(f"receipt must preserve {field}=false")
    if receipt.get("decision") != "EXECUTED_READ_ONLY":
        raise MicrocycleIndexError("only EXECUTED_READ_ONLY receipts may be indexed")
    cycle = receipt.get("cycle")
    if not isinstance(cycle, dict):
        raise MicrocycleIndexError("receipt cycle object is required")
    if not isinstance(cycle.get("cycle_id"), str) or not cycle["cycle_id"]:
        raise MicrocycleIndexError("cycle_id is required")
    n_mod_42 = cycle.get("n_mod_42")
    if not isinstance(n_mod_42, int) or not 0 <= n_mod_42 < 42:
        raise MicrocycleIndexError("n_mod_42 must be an integer in [0, 42)")
    if cycle.get("phase") not in {"psi", "chi", "rho", "delta", "sigma", "omega"}:
        raise MicrocycleIndexError("unknown cycle phase")
    verify_embedded_hash(receipt, "receipt_sha256")


def validate_entry(entry: dict[str, Any], previous_entry_hash: str | None) -> str:
    if entry.get("claim_allowed") is not False:
        raise MicrocycleIndexError("entry claim_allowed must remain false")
    if entry.get("previous_entry_sha256") != previous_entry_hash:
        raise MicrocycleIndexError("entry chain predecessor mismatch")
    verify_embedded_hash(entry, "entry_sha256")
    return str(entry["entry_sha256"])


def validate_index(index: dict[str, Any]) -> None:
    if index.get("schema") != INDEX_SCHEMA:
        raise MicrocycleIndexError("unsupported microcycle index schema")
    for field in ("claim_allowed", "automatic_mutation", "automatic_merge"):
        if index.get(field) is not False:
            raise MicrocycleIndexError(f"index must preserve {field}=false")
    if index.get("source_mode") != "ARTIFACT_APPEND_ONLY":
        raise MicrocycleIndexError("index source_mode must be ARTIFACT_APPEND_ONLY")
    entries = index.get("entries")
    if not isinstance(entries, list):
        raise MicrocycleIndexError("index entries must be a list")
    if index.get("entry_count") != len(entries):
        raise MicrocycleIndexError("entry_count mismatch")
    previous: str | None = None
    seen: set[str] = set()
    for raw in entries:
        if not isinstance(raw, dict):
            raise MicrocycleIndexError("each entry must be an object")
        cycle_id = raw.get("cycle_id")
        if not isinstance(cycle_id, str) or cycle_id in seen:
            raise MicrocycleIndexError("cycle ids must be present and unique")
        seen.add(cycle_id)
        previous = validate_entry(raw, previous)
    latest_four = index.get("latest_four")
    if latest_four != entries[-4:]:
        raise MicrocycleIndexError("latest_four is not derived from the final entries")
    verify_embedded_hash(index, "index_sha256")


def load_fetch_state(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {"state": "TOKEN_VAZIO_FETCH_STATE_NOT_PROVIDED"}
    state = load_object(path)
    if not isinstance(state.get("state"), str):
        raise MicrocycleIndexError("fetch state requires a state string")
    return state


def build_entry(
    receipt: dict[str, Any],
    *,
    previous_entry_sha256: str | None,
    run_id: str,
    run_attempt: str,
    run_url: str,
    repository: str,
    head_branch: str,
    head_sha: str,
    artifact_name: str,
) -> dict[str, Any]:
    cycle = receipt["cycle"]
    entry: dict[str, Any] = {
        "cycle_id": cycle["cycle_id"],
        "generated_at": receipt.get("generated_at"),
        "n_mod_42": cycle["n_mod_42"],
        "phase": cycle["phase"],
        "decision": receipt["decision"],
        "claim_allowed": False,
        "receipt_sha256": receipt["receipt_sha256"],
        "run_id": str(run_id),
        "run_attempt": str(run_attempt),
        "run_url": run_url,
        "repository": repository,
        "head_branch": head_branch,
        "head_sha": head_sha,
        "artifact_name": artifact_name,
        "previous_entry_sha256": previous_entry_sha256,
    }
    entry["entry_sha256"] = sha256_value(entry)
    return entry


def append_receipt(
    receipt: dict[str, Any],
    previous_index: dict[str, Any] | None,
    fetch_state: dict[str, Any],
    **entry_kwargs: str,
) -> tuple[dict[str, Any], str]:
    validate_receipt(receipt)
    if previous_index is not None:
        validate_index(previous_index)
        entries = [dict(item) for item in previous_index["entries"]]
        previous_index_sha256: str | None = previous_index["index_sha256"]
        segment_id = previous_index.get("segment_id")
        if not isinstance(segment_id, str) or not segment_id:
            raise MicrocycleIndexError("previous index segment_id is required")
    else:
        entries = []
        previous_index_sha256 = None
        segment_id = f"SEGMENT-{receipt['cycle']['cycle_id']}"

    cycle_id = receipt["cycle"]["cycle_id"]
    duplicates = [item for item in entries if item.get("cycle_id") == cycle_id]
    if duplicates:
        if duplicates[0].get("receipt_sha256") != receipt.get("receipt_sha256"):
            raise MicrocycleIndexError("same cycle_id observed with a different receipt hash")
        operation = "IDEMPOTENT_ALREADY_PRESENT"
    else:
        predecessor = entries[-1]["entry_sha256"] if entries else None
        entries.append(
            build_entry(
                receipt,
                previous_entry_sha256=predecessor,
                **entry_kwargs,
            )
        )
        operation = "APPENDED"

    continuity_state = str(fetch_state.get("state", "TOKEN_VAZIO_FETCH_STATE_UNKNOWN"))
    index: dict[str, Any] = {
        "schema": INDEX_SCHEMA,
        "segment_id": segment_id,
        "generated_at": receipt.get("generated_at"),
        "source_mode": "ARTIFACT_APPEND_ONLY",
        "claim_allowed": False,
        "automatic_mutation": False,
        "automatic_merge": False,
        "entry_count": len(entries),
        "entries": entries,
        "latest_four": entries[-4:],
        "previous_index_sha256": previous_index_sha256,
        "continuity": {
            "state": continuity_state,
            "previous_artifact_id": fetch_state.get("artifact_id"),
            "previous_run_id": fetch_state.get("run_id"),
            "previous_head_branch": fetch_state.get("head_branch"),
        },
        "boundaries": {
            "artifact_retention_is_not_permanent_archive": True,
            "index_is_not_scientific_evidence": True,
            "ci_is_not_physical_runtime": True,
            "hash_is_not_truth": True,
            "claim_allowed": False,
        },
    }
    index["index_sha256"] = sha256_value(index)
    validate_index(index)
    return index, operation


def render_markdown(index: dict[str, Any], operation: str) -> str:
    rows = []
    for entry in reversed(index["latest_four"]):
        rows.append(
            "| `{cycle_id}` | {n_mod_42} | `{phase}` | `{decision}` | "
            "[{run_id}]({run_url}) | `{receipt_sha256}` |".format(**entry)
        )
    if not rows:
        rows.append("| `TOKEN_VAZIO` | — | — | — | — | — |")
    return "\n".join(
        [
            "# RAFAELIA Microcycle Index",
            "",
            "Append-only, hash-chained navigation over immutable workflow artifacts.",
            "This index does not promote claims and does not substitute for physical or scientific evidence.",
            "",
            f"- Segment: `{index['segment_id']}`",
            f"- Entries: `{index['entry_count']}`",
            f"- Operation: `{operation}`",
            f"- Continuity: `{index['continuity']['state']}`",
            f"- Index SHA-256: `{index['index_sha256']}`",
            "- `claim_allowed=false`",
            "",
            "## Four most recent indexed microcycles",
            "",
            "| cycle_id | n mod 42 | phase | decision | run | receipt SHA-256 |",
            "|---|---:|---|---|---:|---|",
            *rows,
            "",
            "## Boundaries",
            "",
            "- A scheduled run is not scientific evidence.",
            "- A CI receipt is not physical Termux execution.",
            "- Artifact retention is not permanent archival storage.",
            "- Missing continuity remains `TOKEN_VAZIO`; it is never rewritten as success.",
            "",
        ]
    )


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--current-receipt", type=Path, required=True)
    parser.add_argument("--previous-index", type=Path)
    parser.add_argument("--fetch-state", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-attempt", default="1")
    parser.add_argument("--run-url", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--head-branch", required=True)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--artifact-name", default="rafaelia-adaptive-cycle")
    args = parser.parse_args()

    try:
        receipt = load_object(args.current_receipt)
        previous = (
            load_object(args.previous_index)
            if args.previous_index is not None and args.previous_index.exists()
            else None
        )
        fetch_state = load_fetch_state(args.fetch_state)
        index, operation = append_receipt(
            receipt,
            previous,
            fetch_state,
            run_id=args.run_id,
            run_attempt=args.run_attempt,
            run_url=args.run_url,
            repository=args.repository,
            head_branch=args.head_branch,
            head_sha=args.head_sha,
            artifact_name=args.artifact_name,
        )
    except (OSError, json.JSONDecodeError, MicrocycleIndexError) as error:
        print(
            json.dumps(
                {
                    "schema": INDEX_SCHEMA,
                    "decision": "BLOCKED_TOKEN_VAZIO",
                    "claim_allowed": False,
                    "error": f"{type(error).__name__}: {error}",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "microcycle_index.json", index)
    (args.output_dir / "microcycle_index.md").write_text(
        render_markdown(index, operation), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "decision": "EXECUTED_READ_ONLY",
                "operation": operation,
                "entry_count": index["entry_count"],
                "latest_four_count": len(index["latest_four"]),
                "continuity": index["continuity"]["state"],
                "index_sha256": index["index_sha256"],
                "claim_allowed": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
