#!/usr/bin/env python3
"""Deterministic, dependency-free NOVOexport architecture-family discovery.

Evidence-first boundaries:
- recursively reads JSON/JSONL, including gzip variants;
- top-level JSON arrays are treated as independent records, not one mega-record;
- default outputs never contain source text or source paths;
- known aliases become source-bound candidates, never runtime claims;
- unknown structural contexts become TOKEN_VAZIO structural orphans;
- relations are co-occurrence observations, never causation/dependency claims;
- every run produces deterministic hashes and an auditable receipt.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULES = ROOT / "data/ontology/architectures/ARCHITECTURE_DISCOVERY_RULES_V1.json"
SUPPORTED_SUFFIXES = (".json", ".jsonl", ".json.gz", ".jsonl.gz")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize(text: str) -> str:
    folded = unicodedata.normalize("NFKD", text)
    accent_folded = "".join(ch for ch in folded if not unicodedata.combining(ch))
    return re.sub(r"[_\-.]+", " ", accent_folded.casefold())


def stable_json_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def is_supported(path: Path) -> bool:
    name = path.name.casefold()
    return any(name.endswith(suffix) for suffix in SUPPORTED_SUFFIXES)


def discover_files(inputs: list[Path]) -> list[Path]:
    files: set[Path] = set()
    for item in inputs:
        item = item.expanduser().resolve()
        if item.is_file() and is_supported(item):
            files.add(item)
        elif item.is_dir():
            for path in item.rglob("*"):
                if path.is_file() and is_supported(path):
                    files.add(path.resolve())
    return sorted(files, key=lambda p: str(p))


def open_text(path: Path):
    if path.name.casefold().endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return path.open("r", encoding="utf-8", errors="replace")


def pointer_token(value: Any) -> str:
    return str(value).replace("~", "~0").replace("/", "~1")


def iter_strings(node: Any, pointer: str = "$") -> Iterator[tuple[str, str]]:
    if isinstance(node, str):
        yield pointer, node
    elif isinstance(node, dict):
        for key in sorted(node, key=lambda x: str(x)):
            key_text = str(key)
            key_pointer = f"{pointer}/{pointer_token(key_text)}"
            yield f"{key_pointer}/@key", key_text
            yield from iter_strings(node[key], key_pointer)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from iter_strings(value, f"{pointer}/{index}")


def iter_records(path: Path) -> Iterator[tuple[str, Any]]:
    """Yield independent source records without inventing cross-record relations.

    JSONL: each non-empty line is one record.
    JSON list: each top-level item is one record (ChatGPT exports commonly use this).
    JSON object/scalar: the document is one record.
    """
    name = path.name.casefold()
    if name.endswith(".jsonl") or name.endswith(".jsonl.gz"):
        with open_text(path) as handle:
            for line_no, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                yield f"line:{line_no}", json.loads(line)
        return

    with open_text(path) as handle:
        root = json.load(handle)
    if isinstance(root, list):
        for index, record in enumerate(root):
            yield f"item:{index}", record
    else:
        yield "document", root


def compile_rules(rules_path: Path):
    raw = rules_path.read_bytes()
    data = json.loads(raw)
    if data.get("claim_allowed") is not False:
        raise ValueError("discovery rules must keep claim_allowed=false")

    named = [
        (rule, [re.compile(pattern, re.IGNORECASE) for pattern in rule["patterns"]])
        for rule in data.get("rules", [])
    ]
    signals = [
        (signal, [re.compile(pattern, re.IGNORECASE) for pattern in signal["patterns"]])
        for signal in data.get("structural_signals", [])
    ]
    return data, named, signals, sha256_bytes(raw)


def matches_any(patterns: list[re.Pattern[str]], text: str) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def location_id(source_id: str, record_pointer: str, json_pointer: str) -> str:
    payload = f"{source_id}\0{record_pointer}\0{json_pointer}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def candidate_id(location: str, rule_id: str) -> str:
    return hashlib.sha256(f"{location}\0{rule_id}".encode("utf-8")).hexdigest()[:24]


def pairs(values: set[str]) -> Iterator[tuple[str, str]]:
    ordered = sorted(values)
    for index, left in enumerate(ordered):
        for right in ordered[index + 1 :]:
            yield left, right


def make_relation_rows(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    location_groups: dict[tuple[str, str], set[str]] = defaultdict(set)
    record_groups: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in candidates:
        canonical = row.get("canonical")
        if not canonical:
            continue
        location_groups[(row["source_id"], row["location_id"])].add(canonical)
        record_groups[(row["source_id"], row["record_pointer_hash"])].add(canonical)

    counts: Counter[tuple[str, str, str]] = Counter()
    sources: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for scope, groups in (("SAME_STRING", location_groups), ("SAME_RECORD", record_groups)):
        for (source_id, _), canonicals in groups.items():
            for left, right in pairs(canonicals):
                key = (scope, left, right)
                counts[key] += 1
                sources[key].add(source_id)

    rows = []
    for (scope, left, right), count in sorted(counts.items()):
        rows.append({
            "schema": "rafaelia.architecture-discovery-relation/v1",
            "left": left,
            "right": right,
            "relation": "CO_OCCURS_IN_SOURCE_SCOPE",
            "scope": scope,
            "occurrences": count,
            "source_count": len(sources[(scope, left, right)]),
            "state": "OBSERVED_COOCCURRENCE_NOT_CAUSATION",
            "dependency_claim": False,
            "claim_allowed": False,
        })
    return rows


def scan(
    inputs: list[Path],
    rules_path: Path,
    output_dir: Path,
    fail_on_parse_error: bool = False,
    private_review_output: Path | None = None,
) -> dict[str, Any]:
    rules_data, named_rules, signal_rules, rules_sha = compile_rules(rules_path)
    files = discover_files(inputs)
    if not files:
        raise SystemExit("No supported JSON/JSONL inputs found")

    candidates: list[dict[str, Any]] = []
    private_review_rows: list[dict[str, Any]] = []
    parse_errors: list[dict[str, str]] = []
    inventory: list[dict[str, Any]] = []
    parsed_files = 0
    strings_scanned = 0

    for file_index, path in enumerate(files, 1):
        file_sha = sha256_file(path)
        source_id = file_sha[:24]
        inventory.append({
            "ordinal": file_index,
            "source_id": source_id,
            "sha256": file_sha,
            "size_bytes": path.stat().st_size,
            "format": "JSONL" if ".jsonl" in path.name.casefold() else "JSON",
            "compressed": path.name.casefold().endswith(".gz"),
        })
        file_ok = True
        try:
            for record_pointer, record in iter_records(path):
                record_hash = sha256_bytes(record_pointer.encode("utf-8"))[:24]
                for json_pointer, raw_text in iter_strings(record):
                    strings_scanned += 1
                    text = normalize(raw_text)
                    if not text.strip():
                        continue
                    location = location_id(source_id, record_pointer, json_pointer)
                    pointer_hash = sha256_bytes(json_pointer.encode("utf-8"))[:24]
                    context_digest = sha256_bytes(text.encode("utf-8"))
                    matched_signals = [
                        {"signal_id": signal["id"], "kind_hint": signal["kind_hint"]}
                        for signal, patterns in signal_rules
                        if matches_any(patterns, text)
                    ]
                    matched_here = 0
                    for rule, patterns in named_rules:
                        if not matches_any(patterns, text):
                            continue
                        matched_here += 1
                        row = {
                            "schema": "rafaelia.architecture-discovery-candidate/v1",
                            "candidate_id": candidate_id(location, rule["id"]),
                            "source_id": source_id,
                            "location_id": location,
                            "record_pointer_hash": record_hash,
                            "json_pointer_hash": pointer_hash,
                            "context_digest": context_digest,
                            "context_length": len(raw_text),
                            "rule_id": rule["id"],
                            "canonical": rule["canonical"],
                            "architecture_id": rule.get("architecture_id"),
                            "kind_hint": rule["kind_hint"],
                            "state": rule["state"],
                            "structural_signals": matched_signals,
                            "provenance_class": "NOVOEXPORT_JSON_SCAN",
                            "raw_text_emitted": False,
                            "claim_allowed": False,
                        }
                        candidates.append(row)
                        if private_review_output and rule.get("architecture_id") is None:
                            private_review_rows.append({
                                "candidate_id": row["candidate_id"],
                                "source_id": source_id,
                                "location_id": location,
                                "canonical": rule["canonical"],
                                "state": rule["state"],
                                "raw_text": raw_text[:2000],
                                "truncated": len(raw_text) > 2000,
                            })

                    if matched_here == 0 and matched_signals:
                        kinds = sorted({signal["kind_hint"] for signal in matched_signals})
                        orphan = {
                            "schema": "rafaelia.architecture-discovery-candidate/v1",
                            "candidate_id": candidate_id(location, "STRUCTURAL_ORPHAN"),
                            "source_id": source_id,
                            "location_id": location,
                            "record_pointer_hash": record_hash,
                            "json_pointer_hash": pointer_hash,
                            "context_digest": context_digest,
                            "context_length": len(raw_text),
                            "rule_id": "STRUCTURAL_ORPHAN",
                            "canonical": None,
                            "architecture_id": None,
                            "kind_hint": kinds[0] if len(kinds) == 1 else "MULTI_SIGNAL_UNRESOLVED_STRUCTURE",
                            "state": "TOKEN_VAZIO_UNRESOLVED_STRUCTURE",
                            "structural_signals": matched_signals,
                            "provenance_class": "NOVOEXPORT_JSON_SCAN",
                            "raw_text_emitted": False,
                            "claim_allowed": False,
                        }
                        candidates.append(orphan)
                        if private_review_output:
                            private_review_rows.append({
                                "candidate_id": orphan["candidate_id"],
                                "source_id": source_id,
                                "location_id": location,
                                "canonical": None,
                                "state": orphan["state"],
                                "raw_text": raw_text[:2000],
                                "truncated": len(raw_text) > 2000,
                            })
        except Exception as exc:
            file_ok = False
            parse_errors.append({
                "source_id": source_id,
                "error_type": type(exc).__name__,
                "error_digest": sha256_bytes(str(exc).encode("utf-8")),
            })
            if fail_on_parse_error:
                raise
        if file_ok:
            parsed_files += 1

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

    output_dir = output_dir.resolve()
    atomic_write_bytes(output_dir / "architecture_candidates.jsonl", candidate_bytes)
    atomic_write_bytes(output_dir / "architecture_relations.jsonl", relation_bytes)
    atomic_write_bytes(output_dir / "architecture_summary.json", summary_bytes)

    private_review_meta = {"emitted": False}
    if private_review_output:
        private_review_output = private_review_output.expanduser().resolve()
        header = {
            "schema": "rafaelia.architecture-private-review/v1",
            "visibility": "PRIVATE_LOCAL_ONLY_DO_NOT_COMMIT",
            "claim_allowed": False,
            "run_id": run_id,
        }
        private_bytes = stable_json_bytes(header) + b"".join(stable_json_bytes(row) for row in private_review_rows)
        atomic_write_bytes(private_review_output, private_bytes)
        private_review_meta = {
            "emitted": True,
            "sha256": sha256_bytes(private_bytes),
            "row_count": len(private_review_rows),
            "path_emitted_in_receipt": False,
        }

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
        "private_review": private_review_meta,
        "privacy": {
            "raw_text_emitted_in_public_outputs": False,
            "raw_source_paths_emitted": False,
            "source_content_persisted_in_public_outputs": False,
        },
        "boundary": "DISCOVERY_RECEIPT_IS_NOT_RUNTIME_OR_IMPLEMENTATION_EVIDENCE",
    }
    receipt_bytes = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    atomic_write_bytes(output_dir / "architecture_receipt.json", receipt_bytes)

    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="NOVOexport JSON/JSONL file(s) or directories")
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--fail-on-parse-error", action="store_true")
    parser.add_argument(
        "--private-review-output",
        type=Path,
        help="Optional PRIVATE_LOCAL_ONLY JSONL with bounded raw context for unresolved candidates; never commit it.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        scan(
            args.inputs,
            args.rules,
            args.output_dir,
            args.fail_on_parse_error,
            args.private_review_output,
        )
    except Exception as exc:
        print(f"FAIL architecture-discovery: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
