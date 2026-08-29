#!/usr/bin/env python3
"""Resumable, semantics-preserving runner for architecture discovery.

This wrapper removes the runtime-budget failure mode of the canonical scanner by
checkpointing after each fully processed source file, then rebuilding the exact
canonical aggregate from those checkpoints. It does not change discovery rules,
matching semantics, candidate IDs, relation semantics, privacy boundaries, or
claim gates.

Contract:
SOURCE -> TRANSFORM -> CLAIM -> TEST/EVIDENCE -> RECEIPT -> INDEX -> MEMORY
VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM

Safety properties:
- state_dir is private/local execution state and may contain local source paths;
- public outputs are produced only after every discovered source has a complete
  per-file receipt;
- final candidate/relation/summary/receipt serialization reuses the canonical
  scanner's deterministic helpers;
- claim_allowed remains false;
- a partial state can be resumed idempotently without rescanning completed files;
- --verify-against-full-run is intended for bounded fixtures, not large corpora.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

from discover_architecture_families import (
    atomic_write_bytes,
    compile_rules,
    discover_files,
    make_relation_rows,
    scan,
    sha256_bytes,
    stable_json_bytes,
)

MANIFEST_SCHEMA = "rafaelia.architecture-discovery-resumable-manifest/v1"
CHECKPOINT_SCHEMA = "rafaelia.architecture-discovery-resumable-checkpoint/v1"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    data = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    atomic_write_bytes(path, data)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def manifest_for(inputs: list[Path], rules_path: Path) -> dict[str, Any]:
    files = discover_files(inputs)
    if not files:
        raise SystemExit("No supported JSON/JSONL inputs found")
    rules_data, _, _, rules_sha = compile_rules(rules_path)
    return {
        "schema": MANIFEST_SCHEMA,
        "claim_allowed": False,
        "rules": {"schema": rules_data["schema"], "sha256": rules_sha},
        "files": [str(path) for path in files],
        "file_count": len(files),
        "cursor_next": 1,
    }


def ensure_manifest(state_dir: Path, inputs: list[Path], rules_path: Path) -> dict[str, Any]:
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_dir / "manifest.json"
    proposed = manifest_for(inputs, rules_path)
    if not path.exists():
        write_json(path, proposed)
        return proposed

    current = read_json(path)
    invariant_keys = ("schema", "rules", "files", "file_count")
    for key in invariant_keys:
        if current.get(key) != proposed.get(key):
            raise SystemExit(f"State manifest mismatch for {key}; refuse silent rebind")
    return current


def shard_dir(state_dir: Path, ordinal: int) -> Path:
    return state_dir / "shards" / f"{ordinal:05d}"


def shard_complete(path: Path) -> bool:
    required = (
        "architecture_candidates.jsonl",
        "architecture_relations.jsonl",
        "architecture_summary.json",
        "architecture_receipt.json",
        "checkpoint.json",
    )
    return all((path / name).is_file() for name in required)


def process_pending(
    manifest: dict[str, Any],
    state_dir: Path,
    rules_path: Path,
    max_seconds: float,
    fail_on_parse_error: bool,
) -> tuple[int, int]:
    started = time.monotonic()
    processed_now = 0
    files = [Path(value) for value in manifest["files"]]

    for ordinal, source in enumerate(files, 1):
        target = shard_dir(state_dir, ordinal)
        if shard_complete(target):
            continue

        # Never accept a half-written shard as a checkpoint.
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)

        scan(
            [source],
            rules_path,
            target,
            fail_on_parse_error=fail_on_parse_error,
            private_review_output=None,
        )
        receipt = read_json(target / "architecture_receipt.json")
        summary = read_json(target / "architecture_summary.json")
        checkpoint = {
            "schema": CHECKPOINT_SCHEMA,
            "claim_allowed": False,
            "ordinal": ordinal,
            "source_local_path_sha256": sha256_bytes(str(source).encode("utf-8")),
            "source_id": receipt["input_inventory"][0]["source_id"],
            "source_sha256": receipt["input_inventory"][0]["sha256"],
            "input_scope_complete": receipt["input_scope_complete"],
            "parse_error_count": len(receipt["parse_errors"]),
            "candidate_count": summary["candidate_count"],
            "relation_count_local": summary["relation_count"],
            "output_hashes": receipt["outputs"],
        }
        write_json(target / "checkpoint.json", checkpoint)
        processed_now += 1

        manifest["cursor_next"] = ordinal + 1
        write_json(state_dir / "manifest.json", manifest)

        if max_seconds > 0 and time.monotonic() - started >= max_seconds:
            break

    completed = sum(1 for i in range(1, len(files) + 1) if shard_complete(shard_dir(state_dir, i)))
    return processed_now, completed


def finalize(manifest: dict[str, Any], state_dir: Path, rules_path: Path, output_dir: Path) -> dict[str, Any]:
    files = [Path(value) for value in manifest["files"]]
    missing = [i for i in range(1, len(files) + 1) if not shard_complete(shard_dir(state_dir, i))]
    if missing:
        raise SystemExit(f"Cannot finalize; incomplete shard checkpoints: {missing[:20]}")

    rules_data, _, _, rules_sha = compile_rules(rules_path)
    if manifest["rules"]["sha256"] != rules_sha:
        raise SystemExit("Rules digest drift detected; refuse finalization")

    candidates: list[dict[str, Any]] = []
    inventory: list[dict[str, Any]] = []
    parse_errors: list[dict[str, str]] = []
    strings_scanned = 0
    parsed_files = 0

    for ordinal in range(1, len(files) + 1):
        part = shard_dir(state_dir, ordinal)
        receipt = read_json(part / "architecture_receipt.json")
        summary = read_json(part / "architecture_summary.json")
        checkpoint = read_json(part / "checkpoint.json")

        if receipt["rules"]["sha256"] != rules_sha:
            raise SystemExit(f"Rules mismatch at shard {ordinal}")
        if checkpoint["source_sha256"] != receipt["input_inventory"][0]["sha256"]:
            raise SystemExit(f"Checkpoint/receipt source mismatch at shard {ordinal}")

        entry = dict(receipt["input_inventory"][0])
        entry["ordinal"] = ordinal
        inventory.append(entry)
        parse_errors.extend(receipt["parse_errors"])
        strings_scanned += int(summary["strings_scanned"])
        if receipt["input_scope_complete"]:
            parsed_files += 1
        candidates.extend(load_jsonl(part / "architecture_candidates.jsonl"))

    candidates.sort(
        key=lambda row: (
            row.get("canonical") or "~TOKEN_VAZIO_STRUCTURAL_ORPHAN",
            row["source_id"],
            row["location_id"],
            row["rule_id"],
        )
    )
    relations = make_relation_rows(candidates)

    by_canonical = Counter((row.get("canonical") or "TOKEN_VAZIO_STRUCTURAL_ORPHAN") for row in candidates)
    by_kind = Counter(row["kind_hint"] for row in candidates)
    by_state = Counter(row["state"] for row in candidates)
    known = sum(1 for row in candidates if row.get("architecture_id"))
    unresolved = len(candidates) - known
    structural_orphans = sum(1 for row in candidates if row["rule_id"] == "STRUCTURAL_ORPHAN")

    inventory_digest = sha256_bytes(stable_json_bytes(inventory))
    run_material = stable_json_bytes({
        "rules_sha256": rules_sha,
        "inventory_digest": inventory_digest,
        "candidate_count": len(candidates),
        "relation_count": len(relations),
    })
    run_id = f"ARCHDISC-{sha256_bytes(run_material)[:20]}"

    summary = {
        "schema": "rafaelia.architecture-discovery-summary/v1",
        "run_id": run_id,
        "claim_allowed": False,
        "semantic_exhaustiveness_claim": False,
        "input_scope_complete": parsed_files == len(files),
        "files_discovered": len(files),
        "files_parsed": parsed_files,
        "parse_error_count": len(parse_errors),
        "strings_scanned": strings_scanned,
        "candidate_count": len(candidates),
        "known_registry_matches": known,
        "token_vazio_candidates": unresolved,
        "structural_orphan_count": structural_orphans,
        "relation_count": len(relations),
        "counts_by_canonical": dict(sorted(by_canonical.items())),
        "counts_by_kind_hint": dict(sorted(by_kind.items())),
        "counts_by_state": dict(sorted(by_state.items())),
        "next_gate": "REVIEW_AND_PROMOTE_ONLY_WITH_PRIMARY_PROVENANCE",
    }

    candidate_bytes = b"".join(stable_json_bytes(row) for row in candidates)
    relation_bytes = b"".join(stable_json_bytes(row) for row in relations)
    summary_bytes = json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"

    output_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_bytes(output_dir / "architecture_candidates.jsonl", candidate_bytes)
    atomic_write_bytes(output_dir / "architecture_relations.jsonl", relation_bytes)
    atomic_write_bytes(output_dir / "architecture_summary.json", summary_bytes)

    receipt = {
        "schema": "rafaelia.architecture-discovery-receipt/v1",
        "run_id": run_id,
        "claim_allowed": False,
        "semantic_exhaustiveness_claim": False,
        "input_scope_complete": summary["input_scope_complete"],
        "rules": {"schema": rules_data["schema"], "sha256": rules_sha},
        "input_inventory_digest": inventory_digest,
        "input_inventory": inventory,
        "parse_errors": parse_errors,
        "outputs": {
            "architecture_candidates.jsonl": sha256_bytes(candidate_bytes),
            "architecture_relations.jsonl": sha256_bytes(relation_bytes),
            "architecture_summary.json": sha256_bytes(summary_bytes),
        },
        "private_review": {"emitted": False},
        "privacy": {
            "raw_text_emitted_in_public_outputs": False,
            "raw_source_paths_emitted": False,
            "source_content_persisted_in_public_outputs": False,
        },
        "boundary": "DISCOVERY_RECEIPT_IS_NOT_RUNTIME_OR_IMPLEMENTATION_EVIDENCE",
    }
    receipt_bytes = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    atomic_write_bytes(output_dir / "architecture_receipt.json", receipt_bytes)
    return receipt


def verify_equivalence(inputs: list[Path], rules_path: Path, resumable_output: Path, work_dir: Path) -> None:
    reference = work_dir / "reference-full-run"
    if reference.exists():
        shutil.rmtree(reference)
    scan(inputs, rules_path, reference, fail_on_parse_error=True, private_review_output=None)
    names = (
        "architecture_candidates.jsonl",
        "architecture_relations.jsonl",
        "architecture_summary.json",
        "architecture_receipt.json",
    )
    mismatches = []
    for name in names:
        left = sha256_bytes((reference / name).read_bytes())
        right = sha256_bytes((resumable_output / name).read_bytes())
        if left != right:
            mismatches.append((name, left, right))
    if mismatches:
        raise SystemExit(f"Equivalence verification failed: {mismatches}")
    print(json.dumps({"equivalence": "PASS_EXACT", "files": list(names)}, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--rules", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=180.0,
        help="Soft budget checked between completed source files; 0 means no soft limit.",
    )
    parser.add_argument("--fail-on-parse-error", action="store_true")
    parser.add_argument("--verify-against-full-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        manifest = ensure_manifest(args.state_dir.resolve(), args.inputs, args.rules.resolve())
        processed_now, completed = process_pending(
            manifest,
            args.state_dir.resolve(),
            args.rules.resolve(),
            args.max_seconds,
            args.fail_on_parse_error,
        )
        total = int(manifest["file_count"])
        status = {
            "schema": "rafaelia.architecture-discovery-resumable-status/v1",
            "claim_allowed": False,
            "processed_now": processed_now,
            "completed": completed,
            "total": total,
            "cursor_next": manifest.get("cursor_next"),
            "state": "READY_TO_FINALIZE" if completed == total else "CHECKPOINTED_PARTIAL",
        }
        print(json.dumps(status, sort_keys=True))

        if completed == total:
            receipt = finalize(manifest, args.state_dir.resolve(), args.rules.resolve(), args.output_dir.resolve())
            print(json.dumps({"finalized": True, "run_id": receipt["run_id"], "outputs": receipt["outputs"]}, sort_keys=True))
            if args.verify_against_full_run:
                verify_equivalence(args.inputs, args.rules.resolve(), args.output_dir.resolve(), args.state_dir.resolve())
        return 0
    except Exception as exc:
        print(f"FAIL architecture-discovery-resumable: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
