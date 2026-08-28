#!/usr/bin/env python3
"""Phase 0 security observations with explicit open-finding states.

The audit is read-only. It never prints secret values; secret findings retain
only detector rule, path, line, and a fingerprint from the existing scanner.
Unpinned actions are reported as PASS_WITH_OPEN_FINDINGS rather than silently
being reported as a clean PASS.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ACTION_RE = re.compile(r"^\s*uses:\s*([^\s#]+)@([^\s#]+)")
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
DEPENDENCY_RE = re.compile(
    r"(?:git\+https?://|git://|ssh://|github\.com/.+\.git|@(?:main|master|latest)\b)"
)


def load_secret_scanner(root: Path):
    scanner_path = root / "tools" / "scan_secret_hygiene.py"
    spec = importlib.util.spec_from_file_location("phase_0_secret_scanner", scanner_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("secret scanner could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit_secret_exposure(root: Path) -> dict[str, Any]:
    scanner = load_secret_scanner(root)
    excluded_fixture_paths = {"tests/test_secret_hygiene.py"}
    findings: list[dict[str, Any]] = []
    skipped_binary = 0
    skipped_oversize_text = 0
    unreadable = 0
    files_scanned = 0
    excluded = []
    for path in scanner.iter_files(root):
        relative = path.relative_to(root).as_posix()
        if relative in excluded_fixture_paths:
            excluded.append(relative)
            continue
        try:
            size = path.stat().st_size
            if size > scanner.MAX_FILE_BYTES:
                if scanner._looks_binary(path):
                    skipped_binary += 1
                else:
                    skipped_oversize_text += 1
                continue
            raw = path.read_bytes()
        except OSError:
            unreadable += 1
            continue
        if b"\x00" in raw[: scanner.SNIFF_BYTES]:
            skipped_binary += 1
            continue
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            skipped_binary += 1
            continue
        files_scanned += 1
        findings.extend(scanner.scan_text(path, content, root))
    coverage_complete = unreadable == 0 and skipped_oversize_text == 0
    return {
        "id": "S1-01",
        "name": "secret-exposure",
        "status": "PASS" if not findings and coverage_complete else "FAIL",
        "files_scanned": files_scanned,
        "skipped_binary": skipped_binary,
        "skipped_oversize_text": skipped_oversize_text,
        "unreadable": unreadable,
        "coverage_complete": coverage_complete,
        "excluded_fixture_paths": excluded,
        "findings_count": len(findings),
        "findings": findings,
    }


def tracked_files(root: Path) -> list[Path]:
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    names = [name for name in completed.stdout.decode("utf-8").split("\0") if name]
    return [root / name for name in names]


def audit_file_permissions(root: Path) -> dict[str, Any]:
    issues: list[str] = []
    checked = 0
    for path in tracked_files(root):
        if not path.exists():
            continue
        checked += 1
        mode = path.stat().st_mode & 0o777
        if mode & 0o002:
            issues.append(path.relative_to(root).as_posix())
    return {
        "id": "S1-02",
        "name": "file-permissions",
        "status": "PASS" if not issues else "FAIL",
        "tracked_files_checked": checked,
        "world_writable_paths": issues,
    }


def audit_action_pinning(root: Path) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    workflow_count = 0
    action_count = 0
    workflows_root = root / ".github" / "workflows"
    for path in sorted(workflows_root.rglob("*")):
        if path.suffix not in {".yml", ".yaml"} or not path.is_file():
            continue
        workflow_count += 1
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = ACTION_RE.match(line)
            if not match:
                continue
            action, reference = match.groups()
            if action.startswith("./"):
                continue
            action_count += 1
            if not SHA_RE.fullmatch(reference):
                findings.append(
                    {
                        "path": path.relative_to(root).as_posix(),
                        "line": str(line_number),
                        "action": action,
                        "reference": reference,
                    }
                )
    status = "PASS" if not findings else "PASS_WITH_OPEN_FINDINGS"
    return {
        "id": "S1-03",
        "name": "action-pinning",
        "status": status,
        "workflow_files_checked": workflow_count,
        "remote_actions_checked": action_count,
        "unpinned_action_count": len(findings),
        "findings": findings,
        "closure_boundary": "all remote action references use immutable 40-hex commit SHAs",
    }


def audit_dependency_surface(root: Path) -> dict[str, Any]:
    names = {
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "package.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "Cargo.toml",
        "go.mod",
    }
    findings: list[dict[str, str]] = []
    files_checked = 0
    for path in tracked_files(root):
        if path.name not in names or not path.is_file():
            continue
        files_checked += 1
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if DEPENDENCY_RE.search(line):
                findings.append(
                    {
                        "path": path.relative_to(root).as_posix(),
                        "line": str(line_number),
                        "reason": "dynamic-or-git dependency reference",
                    }
                )
    return {
        "id": "S1-04",
        "name": "dependency-surface",
        "status": "PASS" if not findings else "FAIL",
        "dependency_files_checked": files_checked,
        "findings": findings,
    }


def run_audits(root: Path) -> dict[str, Any]:
    checks = [
        audit_secret_exposure(root),
        audit_file_permissions(root),
        audit_action_pinning(root),
        audit_dependency_surface(root),
    ]
    hard_failures = [item["id"] for item in checks if item["status"] == "FAIL"]
    open_findings = [item["id"] for item in checks if item["status"] == "PASS_WITH_OPEN_FINDINGS"]
    if hard_failures:
        overall = "FAIL"
    elif open_findings:
        overall = "PASS_WITH_OPEN_FINDINGS"
    else:
        overall = "PASS"
    return {
        "schema": "rafaelia.phase-0-security-audit-receipt/v2",
        "observed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repository": "rafaelmeloreisnovo/Mapa",
        "claim_allowed": False,
        "status": overall,
        "checks": checks,
        "summary": {
            "checks_total": len(checks),
            "hard_failures": hard_failures,
            "open_findings": open_findings,
        },
        "f_ok": "secret, permission, action-reference, and dependency surfaces were scanned read-only",
        "f_gap": (
            ["remote GitHub Actions are not all immutable SHA-pinned"]
            if open_findings
            else []
        ),
        "f_next": "pin each reported action to a reviewed immutable commit SHA and append a new audit receipt",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        receipt = run_audits(root)
    except (OSError, RuntimeError, subprocess.CalledProcessError, UnicodeDecodeError) as exc:
        print(f"PHASE_0_SECURITY_FAIL: {exc}", file=sys.stderr)
        return 2
    if args.output:
        output = args.output if args.output.is_absolute() else root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    if receipt["status"] == "FAIL":
        return 1
    if args.strict and receipt["status"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
