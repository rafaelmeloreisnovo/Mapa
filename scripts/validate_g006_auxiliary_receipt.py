#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SCHEMA = "mapa.g006-auxiliary-local-validation.v1"
EXPECTED_FILES = {
    "scripts/run_g006_local_gate.py",
    "tests/test_g006_local_gate.py",
    "tests/test_github_blob_materializer.py",
    "tools/materialize_github_blob.py",
}


class AuxiliaryReceiptError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuxiliaryReceiptError(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AuxiliaryReceiptError(f"{path}: {exc}") from exc
    require(isinstance(value, dict), "receipt root must be an object")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def canonical_digest(data: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(data))
    clone.setdefault("integrity", {})["digest"] = ""
    raw = json.dumps(
        clone,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.blake2b(raw, digest_size=32).hexdigest()


def validate(root: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    require(receipt.get("schema") == SCHEMA, "invalid auxiliary receipt schema")
    require(
        receipt.get("scope") == "auxiliary_materializer_and_local_gate_runner_only",
        "auxiliary receipt scope mismatch",
    )
    require(receipt.get("environment") == "assistant_local_python_runtime", "environment mismatch")

    commands = receipt.get("commands")
    require(isinstance(commands, list) and len(commands) == 2, "two command receipts required")
    by_name = {command.get("name"): command for command in commands if isinstance(command, dict)}
    require(set(by_name) == {"py_compile", "unittest"}, "command coverage mismatch")
    require(by_name["py_compile"].get("status") == "PASS", "py_compile did not pass")
    require(by_name["py_compile"].get("returncode") == 0, "py_compile return code mismatch")
    require(by_name["py_compile"].get("file_count") == 4, "compiled file count mismatch")
    require(by_name["unittest"].get("status") == "PASS", "unittest did not pass")
    require(by_name["unittest"].get("returncode") == 0, "unittest return code mismatch")
    require(by_name["unittest"].get("test_count") == 15, "unittest count mismatch")

    results = receipt.get("results")
    require(
        results
        == {
            "compile_status": "PASS",
            "tests_errored": 0,
            "tests_failed": 0,
            "tests_passed": 15,
            "tests_run": 15,
        },
        "auxiliary result summary mismatch",
    )

    noise = receipt.get("environment_noise")
    require(isinstance(noise, dict), "environment noise record required")
    require(noise.get("observed") is True, "observed environment noise must be preserved")
    require(noise.get("affected_test_result") is False, "noise/test boundary mismatch")
    require(noise.get("process_returncodes_remained_zero") is True, "noise return-code boundary mismatch")

    boundaries = receipt.get("boundaries")
    require(isinstance(boundaries, dict), "boundaries required")
    for key in (
        "full_repository_suite_executed",
        "claim_control_plane_suite_executed",
        "git_commit_bound_receipt",
        "remote_runner_receipt",
        "portfolio_exit_criteria_met",
        "claim_allowed",
        "certification_claim",
    ):
        require(boundaries.get(key) is False, f"boundary {key} must remain false")

    declared = receipt.get("files_sha256")
    require(isinstance(declared, dict), "files_sha256 required")
    require(set(declared) == EXPECTED_FILES, "receipt file coverage mismatch")
    observed: dict[str, str] = {}
    for relative in sorted(EXPECTED_FILES):
        path = root / relative
        require(path.is_file(), f"receipt-bound file missing: {relative}")
        observed[relative] = sha256_file(path)
        require(observed[relative] == declared[relative], f"receipt-bound file drift: {relative}")

    integrity = receipt.get("integrity")
    require(isinstance(integrity, dict), "integrity required")
    require(integrity.get("algorithm") == "blake2b-256", "integrity algorithm mismatch")
    expected_digest = canonical_digest(receipt)
    require(integrity.get("digest") == expected_digest, "auxiliary receipt integrity mismatch")

    return {
        "status": "PASS",
        "schema": SCHEMA,
        "compiled_file_count": 4,
        "tests_run": 15,
        "tests_passed": 15,
        "environment_noise_preserved": True,
        "bound_file_count": len(observed),
        "file_hashes_match": True,
        "full_repository_suite_executed": False,
        "claim_control_plane_suite_executed": False,
        "git_commit_bound_receipt": False,
        "remote_runner_receipt": False,
        "portfolio_exit_criteria_met": False,
        "claim_allowed": False,
        "certification_claim": False,
        "integrity_digest": expected_digest,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--receipt",
        type=Path,
        default=Path("resultados/G006_AUXILIARY_LOCAL_VALIDATION_2026-07-21.json"),
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args(argv)
    try:
        result = validate(args.root.resolve(), load(args.receipt))
    except AuxiliaryReceiptError as exc:
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
