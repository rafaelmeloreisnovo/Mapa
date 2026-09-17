#!/usr/bin/env python3
"""Deterministic, privacy-preserving identity and commitment index for JSON/JSONL.

This layer does not copy raw payloads and does not infer semantic meaning.
It binds source occurrence, exact bytes, canonical record content, ordered
record commitments, file roots, and a corpus root.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Iterator, Sequence

BUFFER = 1024 * 1024
VERSION = "1.0.0"

D_OCC = b"RAFAELIA:JSON:OCCURRENCE:V1\0"
D_LEAF = b"RAFAELIA:JSON:LEAF:V1\0"
D_NODE = b"RAFAELIA:JSON:NODE:V1\0"
D_ODD = b"RAFAELIA:JSON:ODD:V1\0"
D_EMPTY = b"RAFAELIA:JSON:EMPTY:V1\0"
D_CHAIN = b"RAFAELIA:JSON:CHAIN:V1\0"
D_SEQUENCE = b"RAFAELIA:JSON:SEQUENCE:V1\0"
D_FILE = b"RAFAELIA:JSON:FILE:V1\0"
D_MANIFEST = b"RAFAELIA:JSON:MANIFEST:V1\0"


class IndexErrorV1(ValueError):
    """Fail-closed indexing error."""


def h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise IndexErrorV1(f"non-canonicalizable JSON value: {exc}") from exc


def json_line(value: Any) -> bytes:
    return canonical(value) + b"\n"


def digest_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(BUFFER):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def _reject_constant(value: str) -> None:
    raise IndexErrorV1(f"non-standard JSON constant: {value}")


def json_load_bytes(raw: bytes) -> Any:
    try:
        text = raw.decode("utf-8")
        return json.loads(text, parse_constant=_reject_constant)
    except UnicodeDecodeError as exc:
        raise IndexErrorV1(f"invalid UTF-8: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise IndexErrorV1(f"malformed JSON: {exc.msg} at {exc.lineno}:{exc.colno}") from exc


def value_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, str):
        return "string"
    if isinstance(value, (int, float)):
        return "number"
    raise IndexErrorV1(f"unsupported JSON value type: {type(value).__name__}")


def normalize_rel(path: Path, root: Path) -> str:
    try:
        return path.resolve(strict=True).relative_to(root.resolve(strict=True)).as_posix()
    except ValueError as exc:
        raise IndexErrorV1(f"path escapes source root: {path}") from exc


def occurrence_id(source_id: str, rel: str, ordinal: int | None = None) -> str:
    payload = source_id.encode("utf-8") + b"\0" + rel.encode("utf-8")
    if ordinal is not None:
        payload += b"\0" + str(ordinal).encode("ascii")
    return "occ:v1:sha256:" + h(D_OCC + payload)


def content_id(canonical_sha256: str) -> str:
    return "cid:json-c14n-v1:sha256:" + canonical_sha256


def merkle_root(hex_hashes: Sequence[str]) -> str:
    if not hex_hashes:
        return h(D_EMPTY)
    level = [bytes.fromhex(item) for item in hex_hashes]
    while len(level) > 1:
        nxt: list[bytes] = []
        idx = 0
        while idx < len(level):
            left = level[idx]
            if idx + 1 < len(level):
                right = level[idx + 1]
                nxt.append(bytes.fromhex(h(D_NODE + left + right)))
            else:
                nxt.append(bytes.fromhex(h(D_ODD + left)))
            idx += 2
        level = nxt
    return level[0].hex()


def chain_next(previous: str | None, commitment: str) -> str:
    prev = b"" if previous is None else bytes.fromhex(previous)
    return h(D_CHAIN + prev + bytes.fromhex(commitment))


def sequence_next(state: Any, canonical_record: bytes) -> None:
    state.update(len(canonical_record).to_bytes(8, "big"))
    state.update(canonical_record)


def discover(inputs: Sequence[Path]) -> tuple[Path, list[Path]]:
    if not inputs:
        raise IndexErrorV1("at least one input is required")
    resolved = [path.resolve(strict=True) for path in inputs]
    roots = [path if path.is_dir() else path.parent for path in resolved]
    common = Path(os.path.commonpath([str(root) for root in roots]))
    files: set[Path] = set()
    for path in resolved:
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_symlink():
                    continue
                if child.is_file() and child.suffix.lower() in {".json", ".jsonl"}:
                    files.add(child.resolve(strict=True))
        elif path.is_file() and path.suffix.lower() in {".json", ".jsonl"}:
            files.add(path)
        else:
            raise IndexErrorV1(f"unsupported input (expected .json/.jsonl or directory): {path}")
    ordered = sorted(files, key=lambda p: normalize_rel(p, common))
    if not ordered:
        raise IndexErrorV1("no .json or .jsonl files discovered")
    return common, ordered


def iter_jsonl(path: Path) -> Iterator[Any]:
    with path.open("rb") as stream:
        for lineno, raw in enumerate(stream, 1):
            if not raw.strip():
                continue
            try:
                yield json_load_bytes(raw)
            except IndexErrorV1 as exc:
                raise IndexErrorV1(f"{path.name}: line {lineno}: {exc}") from exc


def iter_json(path: Path, max_document_bytes: int) -> Iterator[Any]:
    size = path.stat().st_size
    if size > max_document_bytes:
        raise IndexErrorV1(
            f"{path.name}: {size} bytes exceeds --max-document-bytes={max_document_bytes}; "
            "use the specialized streaming custody indexer for very large top-level arrays"
        )
    value = json_load_bytes(path.read_bytes())
    if isinstance(value, list):
        yield from value
    else:
        yield value


def iter_records(path: Path, max_document_bytes: int) -> Iterator[Any]:
    if path.suffix.lower() == ".jsonl":
        yield from iter_jsonl(path)
    else:
        yield from iter_json(path, max_document_bytes)


def file_record(
    *,
    source_id: str,
    rel: str,
    path: Path,
    records_fp: Any,
    max_document_bytes: int,
) -> tuple[dict[str, Any], int]:
    raw_sha256, size_bytes = digest_file(path)
    file_occ = occurrence_id(source_id, rel)
    sequence = hashlib.sha256(D_SEQUENCE)
    record_hashes: list[str] = []
    previous_chain: str | None = None
    count = 0

    for count, value in enumerate(iter_records(path, max_document_bytes), 1):
        cbytes = canonical(value)
        csha = h(cbytes)
        rec_occ = occurrence_id(source_id, rel, count)
        leaf_payload = {
            "schema": "rafaelia.json-identity-record.v1",
            "source_id": source_id,
            "relative_path": rel,
            "file_occurrence_id": file_occ,
            "record_ordinal": count,
            "record_occurrence_id": rec_occ,
            "record_content_id": content_id(csha),
            "canonical_sha256": csha,
            "canonical_bytes": len(cbytes),
            "value_type": value_type(value),
            "claim_allowed": False,
        }
        leaf_commitment = h(D_LEAF + canonical(leaf_payload))
        current_chain = chain_next(previous_chain, leaf_commitment)
        record = {
            **leaf_payload,
            "leaf_commitment_sha256": leaf_commitment,
            "previous_chain_sha256": previous_chain,
            "chain_sha256": current_chain,
        }
        records_fp.write(json_line(record))
        record_hashes.append(leaf_commitment)
        sequence_next(sequence, cbytes)
        previous_chain = current_chain

    if count == 0:
        raise IndexErrorV1(f"{rel}: JSON/JSONL contains no indexable records")

    merkle = merkle_root(record_hashes)
    seq_sha = sequence.hexdigest()
    file_payload = {
        "schema": "rafaelia.json-identity-file.v1",
        "source_id": source_id,
        "relative_path": rel,
        "file_occurrence_id": file_occ,
        "file_content_id": "bid:sha256:" + raw_sha256,
        "size_bytes": size_bytes,
        "raw_sha256": raw_sha256,
        "record_count": count,
        "record_sequence_sha256": seq_sha,
        "record_merkle_root_sha256": merkle,
        "terminal_chain_sha256": previous_chain,
        "claim_allowed": False,
    }
    file_commitment = h(D_FILE + canonical(file_payload))
    return {**file_payload, "file_commitment_sha256": file_commitment}, count


def artifact_sums(out: Path) -> None:
    names = [
        "records.index.jsonl",
        "files.index.jsonl",
        "manifest.json",
        "receipt.json",
    ]
    lines = []
    for name in names:
        path = out / name
        digest, _ = digest_file(path)
        lines.append(f"{digest}  {name}")
    (out / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    inputs: Sequence[Path],
    out: Path,
    *,
    source_id: str,
    max_document_bytes: int = 128 * 1024 * 1024,
) -> dict[str, Any]:
    if not source_id.strip():
        raise IndexErrorV1("source_id must be non-empty")
    if max_document_bytes < 1:
        raise IndexErrorV1("max_document_bytes must be positive")

    root, files = discover(inputs)
    if out.exists() and any(out.iterdir()):
        raise IndexErrorV1("out directory must be absent or empty to preserve prior receipts")
    out.mkdir(parents=True, exist_ok=True)

    staging = Path(tempfile.mkdtemp(prefix=".json-identity-v1-", dir=str(out)))
    files_tmp = staging / "files.index.jsonl"
    records_tmp = staging / "records.index.jsonl"

    file_commitments: list[str] = []
    total_records = 0
    corpus_chain: str | None = None

    try:
        with files_tmp.open("wb") as f_files, records_tmp.open("wb") as f_records:
            for path in files:
                rel = normalize_rel(path, root)
                item, count = file_record(
                    source_id=source_id,
                    rel=rel,
                    path=path,
                    records_fp=f_records,
                    max_document_bytes=max_document_bytes,
                )
                f_files.write(json_line(item))
                total_records += count
                commitment = item["file_commitment_sha256"]
                file_commitments.append(commitment)
                corpus_chain = chain_next(corpus_chain, commitment)

        corpus_merkle = merkle_root(file_commitments)
        manifest_core = {
            "schema": "rafaelia.json-identity-manifest.v1",
            "schema_version": VERSION,
            "source_id": source_id,
            "source_root_label": root.name or ".",
            "file_count": len(files),
            "record_count": total_records,
            "file_order": "LEXICOGRAPHIC_RELATIVE_PATH",
            "record_order": "TOP_LEVEL_ARRAY_OR_JSONL_ORDER",
            "identity_model": {
                "occurrence_id": "SHA256(domain,source_id,relative_path,ordinal?)",
                "content_id": "SHA256(canonical JSON record)",
                "byte_id": "SHA256(exact file bytes)",
                "semantic_equivalence": "NOT_CLAIMED",
            },
            "commitment_model": {
                "leaf": "SHA256(domain,canonical record metadata)",
                "merkle": "DOMAIN_SEPARATED_ORDERED_BINARY_TREE",
                "chain": "SHA256(domain,previous_commitment,current_commitment)",
                "hash_of_hashes": True,
            },
            "corpus_merkle_root_sha256": corpus_merkle,
            "corpus_terminal_chain_sha256": corpus_chain,
            "privacy": {
                "raw_values_copied": False,
                "raw_payloads_copied": False,
                "paths_expose_only_relative_names": True,
            },
            "source_modified": False,
            "claim_allowed": False,
        }
        manifest_commitment = h(D_MANIFEST + canonical(manifest_core))
        manifest = {**manifest_core, "manifest_commitment_sha256": manifest_commitment}
        receipt = {
            "schema": "rafaelia.json-identity-receipt.v1",
            "state": "INDEXED_IDENTITY_COMMITMENTS",
            "source_id": source_id,
            "file_count": len(files),
            "record_count": total_records,
            "corpus_merkle_root_sha256": corpus_merkle,
            "manifest_commitment_sha256": manifest_commitment,
            "raw_payloads_copied": False,
            "source_modified": False,
            "falsifiers": [
                "same bytes produce different byte_id",
                "same canonical record produces different content_id",
                "record reorder leaves Merkle/chain unchanged",
                "source mutation does not change affected commitments",
            ],
            "claim_allowed": False,
        }

        shutil.move(str(records_tmp), str(out / "records.index.jsonl"))
        shutil.move(str(files_tmp), str(out / "files.index.jsonl"))
        (out / "manifest.json").write_bytes(json_line(manifest))
        (out / "receipt.json").write_bytes(json_line(receipt))
        artifact_sums(out)
        return receipt
    except Exception:
        for name in ("records.index.jsonl", "files.index.jsonl", "manifest.json", "receipt.json", "SHA256SUMS"):
            (out / name).unlink(missing_ok=True)
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--max-document-bytes", type=int, default=128 * 1024 * 1024)
    args = parser.parse_args()
    try:
        receipt = run(
            args.inputs,
            args.out_dir,
            source_id=args.source_id,
            max_document_bytes=args.max_document_bytes,
        )
    except (OSError, IndexErrorV1) as exc:
        print(f"HOLD_FAIL_CLOSED: {type(exc).__name__}: {exc}")
        return 2
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
