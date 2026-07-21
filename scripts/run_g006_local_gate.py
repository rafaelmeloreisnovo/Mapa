#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HEX40 = re.compile(r"^[0-9a-f]{40}$")
NEXT_GATE = "OBSERVABLE_SCANNER_RECEIPT_AND_SCOPE_REFRESH"

G006_SCRIPTS = [
    "scripts/validate_claim_vocabulary.py",
    "scripts/validate_claim_contradiction_ledger.py",
    "scripts/validate_claim_review_chain.py",
    "scripts/validate_claim_review_residual.py",
    "scripts/validate_claim_discovery_precision.py",
    "scripts/run_g006_local_gate.py",
]
G006_TESTS = [
    "tests/test_claim_vocabulary.py",
    "tests/test_claim_contradiction_ledger.py",
    "tests/test_claim_review_chain.py",
    "tests/test_claim_review_residual.py",
    "tests/test_claim_discovery_precision.py",
    "tests/test_g006_local_gate.py",
]
CONTROL_FILES = [
    "indices/CLAIM_VOCABULARY_POLICY.json",
    "indices/CLAIM_CONTRADICTION_LEDGER.json",
    "indices/CLAIM_CONTRADICTION_HEAD.json",
    "indices/CLAIM_REVIEW_RESIDUAL.json",
    "indices/CLAIM_REVIEW_RESOLUTION_CC028.json",
    "indices/claim_review_batches/CLAIM_REVIEW_BATCH_001_2026-07-20.json",
    "indices/claim_review_batches/CLAIM_REVIEW_BATCH_002_2026-07-20.json",
    "indices/claim_review_batches/CLAIM_REVIEW_BATCH_003_2026-07-21.json",
    "schemas/claim-contradiction-ledger.schema.json",
    *G006_SCRIPTS,
    *G006_TESTS,
]


class LocalGateError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise LocalGateError(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def atomic_write(path: Path, data: bytes, *, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def build_command_plan(root: Path, output_dir: Path) -> list[dict[str, Any]]:
    python = sys.executable
    return [
        {
            "name": "py_compile",
            "argv": [python, "-m", "py_compile", *G006_SCRIPTS, *G006_TESTS],
        },
        {
            "name": "unittest",
            "argv": [python, "-m", "unittest", "-v", *G006_TESTS],
        },
        {
            "name": "claim_vocabulary",
            "argv": [
                python,
                "scripts/validate_claim_vocabulary.py",
                "--root",
                ".",
                "--policy",
                "indices/CLAIM_VOCABULARY_POLICY.json",
                "--write-report",
                str(output_dir / "claim-vocabulary-validation.json"),
            ],
        },
        {
            "name": "claim_ledger",
            "argv": [
                python,
                "scripts/validate_claim_contradiction_ledger.py",
                "--path",
                "indices/CLAIM_CONTRADICTION_LEDGER.json",
                "--write-report",
                str(output_dir / "claim-contradiction-ledger-validation.json"),
            ],
        },
        {
            "name": "claim_chain",
            "argv": [
                python,
                "scripts/validate_claim_review_chain.py",
                "--head",
                "indices/CLAIM_CONTRADICTION_HEAD.json",
                "--write-report",
                str(output_dir / "claim-review-chain-validation.json"),
            ],
        },
        {
            "name": "claim_residual_resolution",
            "argv": [
                python,
                "scripts/validate_claim_review_residual.py",
                "--residual",
                "indices/CLAIM_REVIEW_RESIDUAL.json",
                "--resolution",
                "indices/CLAIM_REVIEW_RESOLUTION_CC028.json",
                "--head",
                "indices/CLAIM_CONTRADICTION_HEAD.json",
                "--write-report",
                str(output_dir / "claim-review-residual-validation.json"),
            ],
        },
        {
            "name": "claim_discovery_precision",
            "argv": [
                python,
                "scripts/validate_claim_discovery_precision.py",
                "--root",
                ".",
                "--policy",
                "indices/CLAIM_VOCABULARY_POLICY.json",
                "--write-report",
                str(output_dir / "claim-discovery-precision-validation.json"),
            ],
        },
    ]


def run_command(
    *,
    root: Path,
    output_dir: Path,
    name: str,
    argv: list[str],
    timeout_seconds: int,
) -> dict[str, Any]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            argv,
            cwd=root,
            text=False,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        returncode = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        returncode = 124
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        timed_out = True
    duration = round(time.monotonic() - started, 6)
    stdout_path = output_dir / "logs" / f"{name}.stdout.log"
    stderr_path = output_dir / "logs" / f"{name}.stderr.log"
    atomic_write(stdout_path, stdout)
    atomic_write(stderr_path, stderr)
    return {
        "name": name,
        "argv": argv,
        "returncode": returncode,
        "timed_out": timed_out,
        "duration_seconds": duration,
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "stdout_bytes": len(stdout),
        "stderr_bytes": len(stderr),
        "stdout_sha256": sha256_bytes(stdout),
        "stderr_sha256": sha256_bytes(stderr),
        "status": "PASS" if returncode == 0 else "FAIL",
    }


def observe_git(root: Path, expected_commit: str, allow_dirty: bool) -> dict[str, Any]:
    require(HEX40.fullmatch(expected_commit) is not None, "expected commit must be 40 lowercase hex")
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
            timeout=30,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
            timeout=30,
        ).stdout
    except (OSError, subprocess.SubprocessError) as exc:
        raise LocalGateError(f"Git observation failed: {exc}") from exc
    require(head == expected_commit, "observed Git commit differs from expected commit")
    dirty = bool(status.strip())
    require(allow_dirty or not dirty, "working tree is dirty")
    return {
        "head_commit": head,
        "expected_commit": expected_commit,
        "commit_match": True,
        "working_tree_dirty": dirty,
        "dirty_allowed": allow_dirty,
    }


def load_report(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LocalGateError(f"{path}: {exc}") from exc
    require(isinstance(value, dict), f"{path}: report must be an object")
    return value


def validate_report_bundle(output_dir: Path) -> dict[str, Any]:
    reports = {
        "claim_scan": load_report(output_dir / "claim-vocabulary-validation.json"),
        "claim_ledger": load_report(output_dir / "claim-contradiction-ledger-validation.json"),
        "claim_chain": load_report(output_dir / "claim-review-chain-validation.json"),
        "claim_residual": load_report(output_dir / "claim-review-residual-validation.json"),
        "claim_precision": load_report(output_dir / "claim-discovery-precision-validation.json"),
    }
    require(all(report.get("status") == "PASS" for report in reports.values()), "one or more G006 reports failed")

    scan = reports["claim_scan"]
    require(scan.get("explicit_claim_error_count") == 0, "explicit claim errors remain")
    require(scan.get("portfolio_exit_criteria_met") is False, "scanner cannot close portfolio")
    require(scan.get("claim_allowed") is False, "scanner claim boundary mismatch")

    ledger = reports["claim_ledger"]
    require(ledger.get("candidate_count") == 36, "ledger candidate count mismatch")
    require(ledger.get("reviewed_safe_count") == 6, "base ledger safe count mismatch")
    require(ledger.get("token_vazio_count") == 30, "base ledger TOKEN_VAZIO count mismatch")

    chain = reports["claim_chain"]
    require(chain.get("review_batch_count") == 3, "review batch count mismatch")
    require(chain.get("review_decision_count") == 30, "review decision count mismatch")
    require(chain.get("reviewed_safe_count") == 36, "reviewed safe count mismatch")
    require(chain.get("reviewed_blocking_count") == 0, "reviewed blockers remain")
    require(chain.get("token_vazio_count") == 0, "current indexed residual remains")
    require(chain.get("review_completion_ratio") == 1.0, "indexed review is incomplete")
    require(chain.get("exact_absence_resolution_count") == 1, "CC028 resolution count mismatch")
    require(chain.get("next_gate") == NEXT_GATE, "chain next gate mismatch")
    require(chain.get("claim_allowed") is False, "chain claim boundary mismatch")

    residual = reports["claim_residual"]
    require(residual.get("historical_residual_count") == 1, "historical residual missing")
    require(residual.get("current_residual_count") == 0, "current residual count mismatch")
    require(residual.get("full_content_observed") is True, "CC028 full content not observed")
    require(residual.get("decoded_size_bytes") == 19542, "CC028 decoded size mismatch")
    require(residual.get("exact_strong_token_count") == 0, "CC028 exact strong token remains")
    require(residual.get("false_positive_source") == "completeness_ratio", "CC028 cause mismatch")
    require(residual.get("claim_allowed") is False, "residual claim boundary mismatch")

    precision = reports["claim_precision"]
    known = precision.get("known_resolution", {})
    require(known.get("entry_id") == "CC028", "precision resolution id mismatch")
    require(known.get("substring_complete_count") == 1, "precision substring count mismatch")
    require(known.get("exact_complete_count") == 0, "precision exact count mismatch")
    require(precision.get("claim_allowed") is False, "precision claim boundary mismatch")

    return {
        "status": "PASS",
        "report_count": len(reports),
        "candidate_count": 36,
        "reviewed_safe_count": 36,
        "reviewed_blocking_count": 0,
        "current_residual_count": 0,
        "next_gate": NEXT_GATE,
        "claim_allowed": False,
        "certification_claim": False,
        "reports": reports,
    }


def build_checksums(root: Path, output_dir: Path) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for relative in sorted(CONTROL_FILES):
        path = root / relative
        require(path.is_file(), f"control file missing: {relative}")
        checksums[relative] = sha256_file(path)
    target = output_dir / "G006_CHECKSUMS.sha256"
    rendered = "".join(f"{digest}  {path}\n" for path, digest in checksums.items())
    atomic_write(target, rendered.encode("utf-8"))
    return checksums


def build_receipt(
    *,
    root: Path,
    output_dir: Path,
    git: dict[str, Any],
    commands: list[dict[str, Any]],
    bundle: dict[str, Any] | None,
    checksums: dict[str, str],
    started_at: str,
    finished_at: str,
    status: str,
    error: str | None,
) -> dict[str, Any]:
    receipt = {
        "schema": "mapa.g006-local-gate-receipt.v1",
        "status": status,
        "started_at": started_at,
        "finished_at": finished_at,
        "root": str(root),
        "output_dir": str(output_dir),
        "runtime": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
        "git": git,
        "commands": commands,
        "report_bundle": bundle,
        "control_file_count": len(checksums),
        "control_checksums": checksums,
        "error": error,
        "boundaries": {
            "remote_runner_receipt": False,
            "portfolio_exit_criteria_met": False,
            "claim_allowed": False,
            "certification_claim": False,
        },
        "integrity": {
            "algorithm": "blake2b-256",
            "canonicalization": "json-sort-keys-utf8; integrity.digest blanked",
            "digest": "",
        },
    }
    receipt["integrity"]["digest"] = canonical_digest(receipt)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    args = parser.parse_args(argv)

    root = args.root.resolve()
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = (root / output_dir).resolve()
    started_at = utc_now()
    commands: list[dict[str, Any]] = []
    checksums: dict[str, str] = {}
    bundle: dict[str, Any] | None = None
    git: dict[str, Any] = {}
    error: str | None = None
    status = "FAIL"

    try:
        require(root.is_dir(), "root directory does not exist")
        git = observe_git(root, args.expected_commit, args.allow_dirty)
        output_dir.mkdir(parents=True, exist_ok=True)
        for spec in build_command_plan(root, output_dir):
            result = run_command(
                root=root,
                output_dir=output_dir,
                name=spec["name"],
                argv=spec["argv"],
                timeout_seconds=args.timeout_seconds,
            )
            commands.append(result)
            require(result["status"] == "PASS", f"command failed: {spec['name']}")
        bundle = validate_report_bundle(output_dir)
        checksums = build_checksums(root, output_dir)
        status = "PASS"
    except (LocalGateError, OSError) as exc:
        error = str(exc)

    receipt = build_receipt(
        root=root,
        output_dir=output_dir,
        git=git,
        commands=commands,
        bundle=bundle,
        checksums=checksums,
        started_at=started_at,
        finished_at=utc_now(),
        status=status,
        error=error,
    )
    atomic_write(
        output_dir / "g006-local-gate-receipt.json",
        (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"),
    )
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
