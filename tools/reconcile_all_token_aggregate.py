#!/usr/bin/env python3
"""Reconcile ALL_TOKEN aggregate metadata against detailed stores.

The tool is intentionally source-agnostic: private files are supplied at runtime
and are never embedded in the repository.  It distinguishes three states:

- CONSISTENT: detailed stores and manifest aggregate agree;
- MANIFEST_AGGREGATE_DRIFT: detailed stores agree with each other, while the
  manifest's scalar aggregate differs;
- STORE_DIVERGENCE: detailed stores disagree and no aggregate should be trusted.

TOKEN_VAZIO is preserved for the generator/root-cause path unless the caller
can independently bind the code that produced the drifting scalar field.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, TextIO


def _open_text(path: Path) -> TextIO:
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", newline="")
    return path.open("rt", encoding="utf-8", newline="")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_literal_store(path: Path) -> tuple[int, int, Counter[str]]:
    rows = 0
    total = 0
    per_literal: Counter[str] = Counter()
    with _open_text(path) as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        required = {"literal", "count_total"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"{path}: missing columns {sorted(required)}")
        for row in reader:
            count = int(row["count_total"])
            rows += 1
            total += count
            per_literal[row["literal"]] += count
    return rows, total, per_literal


def _read_token_source_store(
    path: Path,
) -> tuple[int, int, Counter[str], Counter[str]]:
    rows = 0
    total = 0
    per_literal: Counter[str] = Counter()
    per_source: Counter[str] = Counter()
    with _open_text(path) as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        required = {"literal", "source", "count"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"{path}: missing columns {sorted(required)}")
        for row in reader:
            count = int(row["count"])
            rows += 1
            total += count
            per_literal[row["literal"]] += count
            per_source[row["source"]] += count
    return rows, total, per_literal, per_source


def _read_source_manifest(path: Path) -> tuple[int, int, Dict[str, int]]:
    rows = 0
    total = 0
    per_source: Dict[str, int] = {}
    with _open_text(path) as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        required = {"source", "token_occurrences"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"{path}: missing columns {sorted(required)}")
        for row in reader:
            source = row["source"]
            count = int(row["token_occurrences"])
            if source in per_source:
                raise ValueError(f"{path}: duplicate source {source!r}")
            rows += 1
            total += count
            per_source[source] = count
    return rows, total, per_source


def _mismatch_count(left: Dict[str, int], right: Dict[str, int]) -> int:
    keys = set(left) | set(right)
    return sum(1 for key in keys if left.get(key, 0) != right.get(key, 0))


def analyze(
    tokens_literal: str | Path,
    token_source_counts: str | Path,
    source_manifest: str | Path,
    manifest_json: str | Path,
) -> dict:
    literal_path = Path(tokens_literal)
    token_source_path = Path(token_source_counts)
    source_manifest_path = Path(source_manifest)
    manifest_path = Path(manifest_json)

    literal_rows, literal_total, literal_counts = _read_literal_store(literal_path)
    (
        token_source_rows,
        token_source_total,
        token_source_literals,
        token_source_sources,
    ) = _read_token_source_store(token_source_path)
    source_rows, source_total, source_counts = _read_source_manifest(source_manifest_path)

    with manifest_path.open("rt", encoding="utf-8") as fh:
        manifest = json.load(fh)

    embedded = manifest.get("source_manifest", [])
    embedded_total = sum(int(row["token_occurrences"]) for row in embedded)
    embedded_sources = {
        str(row["source"]): int(row["token_occurrences"]) for row in embedded
    }
    manifest_total = int(manifest["token_occurrences_total_raw"])

    per_literal_mismatches = _mismatch_count(literal_counts, token_source_literals)
    per_source_mismatches = _mismatch_count(source_counts, token_source_sources)
    embedded_source_mismatches = _mismatch_count(source_counts, embedded_sources)

    detailed_totals = {
        literal_total,
        token_source_total,
        source_total,
        embedded_total,
    }
    detailed_consistent = (
        len(detailed_totals) == 1
        and per_literal_mismatches == 0
        and per_source_mismatches == 0
        and embedded_source_mismatches == 0
    )

    canonical_detailed_total = literal_total if detailed_consistent else None
    manifest_delta = (
        manifest_total - canonical_detailed_total
        if canonical_detailed_total is not None
        else None
    )

    if not detailed_consistent:
        state = "STORE_DIVERGENCE"
    elif manifest_delta != 0:
        state = "MANIFEST_AGGREGATE_DRIFT"
    else:
        state = "CONSISTENT"

    return {
        "schema": "rafaelia.all-token-aggregate-reconciliation/v1",
        "state": state,
        "claim_allowed": False,
        "detailed_stores_consistent": detailed_consistent,
        "canonical_detailed_total": canonical_detailed_total,
        "manifest_token_occurrences_total_raw": manifest_total,
        "manifest_delta_vs_detailed": manifest_delta,
        "generator_root_cause": (
            "TOKEN_VAZIO_NOT_LOCATED" if state == "MANIFEST_AGGREGATE_DRIFT" else None
        ),
        "stores": {
            "tokens_literal": {
                "rows": literal_rows,
                "sum_count_total": literal_total,
                "sha256": _sha256(literal_path),
            },
            "token_source_counts": {
                "rows": token_source_rows,
                "sum_count": token_source_total,
                "distinct_sources": len(token_source_sources),
                "distinct_literals": len(token_source_literals),
                "sha256": _sha256(token_source_path),
            },
            "source_manifest": {
                "rows": source_rows,
                "sum_token_occurrences": source_total,
                "sha256": _sha256(source_manifest_path),
            },
            "manifest_json": {
                "embedded_source_manifest_rows": len(embedded),
                "embedded_source_manifest_sum": embedded_total,
                "sha256": _sha256(manifest_path),
            },
        },
        "mismatches": {
            "per_literal": per_literal_mismatches,
            "per_source": per_source_mismatches,
            "embedded_vs_source_manifest": embedded_source_mismatches,
        },
        "boundary": {
            "manifest_field_location": "EVIDENCED" if state == "MANIFEST_AGGREGATE_DRIFT" else None,
            "generator_code_location": "TOKEN_VAZIO" if state == "MANIFEST_AGGREGATE_DRIFT" else None,
            "rule": "Do not mutate detailed stores to make a historical aggregate match.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tokens-literal", required=True)
    parser.add_argument("--token-source-counts", required=True)
    parser.add_argument("--source-manifest", required=True)
    parser.add_argument("--manifest-json", required=True)
    parser.add_argument("--output")
    parser.add_argument(
        "--allow-manifest-drift",
        action="store_true",
        help="Return success for a localized manifest-only drift; STORE_DIVERGENCE still fails.",
    )
    args = parser.parse_args()

    result = analyze(
        args.tokens_literal,
        args.token_source_counts,
        args.source_manifest,
        args.manifest_json,
    )
    rendered = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")

    if result["state"] == "STORE_DIVERGENCE":
        return 2
    if result["state"] == "MANIFEST_AGGREGATE_DRIFT" and not args.allow_manifest_drift:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
