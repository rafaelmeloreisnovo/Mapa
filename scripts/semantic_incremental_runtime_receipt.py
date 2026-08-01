#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "rafaelia.semantic-runtime-receipt.v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan(root: Path) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        stat = path.stat()
        index[rel] = {
            "sha256": sha256_file(path),
            "bytes": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
            "etag": f'"sha256:{sha256_file(path)}"',
        }
    return index


def incremental(previous: dict[str, Any], root: Path) -> tuple[dict[str, Any], list[str], list[str]]:
    current_paths = {p.relative_to(root).as_posix(): p for p in root.rglob("*") if p.is_file()}
    result: dict[str, Any] = {}
    changed: list[str] = []
    reused: list[str] = []
    for rel, path in sorted(current_paths.items()):
        stat = path.stat()
        old = previous.get(rel)
        if isinstance(old, dict) and old.get("bytes") == stat.st_size and old.get("mtime_ns") == stat.st_mtime_ns:
            result[rel] = old
            reused.append(rel)
        else:
            digest = sha256_file(path)
            result[rel] = {
                "sha256": digest,
                "bytes": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
                "etag": f'"sha256:{digest}"',
            }
            changed.append(rel)
    deleted = sorted(set(previous) - set(current_paths))
    changed.extend(f"DELETE:{item}" for item in deleted)
    return result, changed, reused


def canonical_sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--previous-index", type=Path)
    parser.add_argument("--out-index", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    previous: dict[str, Any] = {}
    if args.previous_index and args.previous_index.is_file():
        previous = json.loads(args.previous_index.read_text(encoding="utf-8"))

    t0 = time.perf_counter_ns()
    inc, changed, reused = incremental(previous, root)
    incremental_ns = time.perf_counter_ns() - t0

    t1 = time.perf_counter_ns()
    full = scan(root)
    full_scan_ns = time.perf_counter_ns() - t1

    equivalent = inc == full
    coverage = 1.0 if not full else len(set(inc) & set(full)) / len(full)
    state = "PASS_OPERATIONAL" if equivalent and coverage == 1.0 else "BLOCKED"

    receipt = {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "NON_DESTRUCTIVE_INCREMENTAL_APPEND_ONLY",
        "state": state,
        "claim_allowed": False,
        "root": root.as_posix(),
        "files": len(full),
        "changed": changed,
        "reused_count": len(reused),
        "coverage": coverage,
        "incremental_ns": incremental_ns,
        "full_scan_ns": full_scan_ns,
        "speedup_ratio": (full_scan_ns / incremental_ns) if incremental_ns else None,
        "equivalent_to_full_scan": equivalent,
        "incremental_index_sha256": canonical_sha(inc),
        "full_scan_index_sha256": canonical_sha(full),
        "token_vazio": [] if equivalent else ["TOKEN_VAZIO_INDEX_DIVERGENCE"],
    }

    args.out_index.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.out_index.write_text(json.dumps(inc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if state == "PASS_OPERATIONAL" else 3


if __name__ == "__main__":
    raise SystemExit(main())
