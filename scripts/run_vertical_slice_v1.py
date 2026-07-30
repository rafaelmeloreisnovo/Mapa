#!/usr/bin/env python3
"""Execute the bounded RAFAELIA SRC->CLAIM->RUN->RECEIPT->DECISION->MAPA slice.

Standard library only. Fail-closed. No semantic or scientific promotion is made.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import struct
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as stream:
        if stream.read(8) != b"\x89PNG\r\n\x1a\n":
            raise ValueError("invalid PNG signature")
        length = struct.unpack(">I", stream.read(4))[0]
        kind = stream.read(4)
        if kind != b"IHDR" or length < 8:
            raise ValueError("missing or invalid IHDR")
        return struct.unpack(">II", stream.read(8))


def load_registry(repository_root: Path) -> dict:
    path = repository_root / "data/vertical_slice_v1/registry.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    if registry.get("claim_allowed") is not False:
        raise ValueError("registry must be fail-closed: claim_allowed=false")
    for claim in registry.get("claims", []):
        if not claim.get("falsifier"):
            raise ValueError(f"claim without falsifier: {claim.get('id')}")
    return registry


def execute(source_root: Path, repository_root: Path, runtime_class: str) -> dict:
    registry = load_registry(repository_root)
    observations: list[dict] = []
    by_kind: dict[str, list[tuple[dict, Path, dict]]] = {}
    missing_sources: list[str] = []
    hash_failures: list[str] = []

    for source in registry["sources"]:
        path = source_root / source["filename"]
        if not path.is_file():
            missing_sources.append(source["id"])
            continue
        actual_hash = sha256_file(path)
        hash_match = actual_hash == source["sha256"]
        if not hash_match:
            hash_failures.append(source["id"])
        observation = {
            "source_id": source["id"],
            "filename": source["filename"],
            "kind": source["kind"],
            "size_bytes": path.stat().st_size,
            "sha256": actual_hash,
            "hash_match": hash_match,
        }
        observations.append(observation)
        by_kind.setdefault(source["kind"], []).append((source, path, observation))

    claim_results: dict[str, dict] = {}

    apk_items = by_kind.get("APK", [])
    if apk_items:
        _, path, observation = apk_items[0]
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
        expected = set(registry["expected"]["apk_entries"])
        missing_entries = sorted(expected - names)
        claim_results["CLAIM-APK-ABI-001"] = {
            "pass": not missing_entries and observation["hash_match"],
            "entry_count": len(names),
            "missing_entries": missing_entries,
            "observed_expected_entries": sorted(expected & names),
        }
    else:
        claim_results["CLAIM-APK-ABI-001"] = {
            "pass": False,
            "state": "TOKEN_VAZIO_SOURCE_UNAVAILABLE",
        }

    export_items = by_kind.get("CHAT_EXPORT_ZIP", [])
    if export_items:
        _, path, observation = export_items[0]
        with zipfile.ZipFile(path) as archive:
            first_bad_entry = archive.testzip()
            root_entries = sorted(
                name for name in archive.namelist() if "/" not in name.rstrip("/")
            )
        expected = sorted(registry["expected"]["chat_export_root_entries"])
        claim_results["CLAIM-EXPORT-ROOT-001"] = {
            "pass": first_bad_entry is None
            and root_entries == expected
            and observation["hash_match"],
            "root_entries": root_entries,
            "expected_entries": expected,
            "first_bad_entry": first_bad_entry,
        }
    else:
        claim_results["CLAIM-EXPORT-ROOT-001"] = {
            "pass": False,
            "state": "TOKEN_VAZIO_SOURCE_UNAVAILABLE",
        }

    image_results: list[dict] = []
    for source, path, observation in by_kind.get("PNG", []):
        try:
            width, height = png_dimensions(path)
            image_results.append(
                {
                    "source_id": source["id"],
                    "filename": source["filename"],
                    "width": width,
                    "height": height,
                    "pass": observation["hash_match"] and width > 0 and height > 0,
                }
            )
        except Exception as error:  # fail-closed; error preserved in receipt
            image_results.append(
                {
                    "source_id": source["id"],
                    "filename": source["filename"],
                    "pass": False,
                    "error": str(error),
                }
            )
    claim_results["CLAIM-PNG-CORPUS-001"] = {
        "pass": len(image_results) == 7 and all(item["pass"] for item in image_results),
        "images": image_results,
    }

    overall_pass = (
        not missing_sources
        and not hash_failures
        and all(result.get("pass") for result in claim_results.values())
    )
    result = {
        "event_id": registry["event_id"],
        "run_id": "RUN-VSLICE-001",
        "overall_pass": overall_pass,
        "missing_sources": missing_sources,
        "hash_failures": hash_failures,
        "observations": observations,
        "claim_results": claim_results,
    }
    stdout_text = (
        ("PASS" if overall_pass else "FAIL")
        + f" {registry['event_id']} sources={len(observations)} claims={len(claim_results)}\n"
    )
    receipt = {
        "schema": "rafaelia_operational_record_v1",
        "id": "RECEIPT-VSLICE-001",
        "record_type": "RECEIPT",
        "state": "EVIDENCIADO" if overall_pass else "REFUTADO",
        "claim_allowed": False,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "event_id": registry["event_id"],
        "run_id": "RUN-VSLICE-001",
        "runtime_class": runtime_class,
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "machine": platform.machine(),
            "implementation": platform.python_implementation(),
        },
        "commit": "TOKEN_VAZIO_GIT_COMMIT_NOT_BOUND",
        "device": platform.node() or "TOKEN_VAZIO_DEVICE_NAME",
        "architecture": platform.machine() or "TOKEN_VAZIO_ARCH",
        "compiler": platform.python_compiler(),
        "flags": [],
        "input_hash": canonical_hash(registry["sources"]),
        "command": f"python3 scripts/run_vertical_slice_v1.py --source-root {source_root}",
        "exit_code": 0 if overall_pass else 1,
        "stdout_hash": hashlib.sha256(stdout_text.encode("utf-8")).hexdigest(),
        "stderr_hash": hashlib.sha256(b"").hexdigest(),
        "output_hash": canonical_hash(result),
        "provenance": {
            "origin": "local_vertical_slice_execution",
            "sha256": canonical_hash(result),
        },
        "falsifier": "hash mismatch, missing expected entry, corrupt ZIP, invalid PNG signature or unreadable IHDR",
        "next_verifiable_step": "replicate in Android Termux, bind to exact commit and obtain independent human review",
        "result": result,
    }
    return {"stdout": stdout_text, "receipt": receipt}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--repository-root", default=Path(__file__).resolve().parents[1], type=Path)
    parser.add_argument("--runtime-class", default="UNKNOWN_RUNTIME")
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    execution = execute(args.source_root, args.repository_root, args.runtime_class)
    receipt = execution["receipt"]
    output = args.receipt_out or args.repository_root / "receipts/vertical_slice/RECEIPT-VSLICE-001.runtime.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(execution["stdout"], end="")
    return int(receipt["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
