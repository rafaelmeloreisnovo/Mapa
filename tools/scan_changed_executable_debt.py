#!/usr/bin/env python3
"""Block newly introduced high-confidence executable debt markers.

The scan is delta-scoped: historical debt is not rewritten, while new executable
TODO/stub/placeholder markers must either be implemented or explicitly justified
with `DEBT_OK:` on the same line. Test fixtures are outside this gate.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

EXECUTABLE_SUFFIXES = {
    ".py", ".sh", ".bash", ".c", ".h", ".cc", ".cpp", ".cxx", ".hpp",
    ".rs", ".go", ".java", ".kt", ".kts", ".js", ".mjs", ".cjs", ".ts",
    ".tsx", ".jsx", ".rb", ".pl", ".asm", ".s", ".S",
}
SUPPRESSION = "DEBT_OK:"
TOKEN_PARTS = [
    ("TODO", "TO" + "DO"),
    ("FIXME", "FIX" + "ME"),
    ("PLACEHOLDER", "PLACE" + "HOLDER"),
    ("STUB", "ST" + "UB"),
    ("NotImplementedError", "NotImplemented" + "Error"),
    ("todo!", "to" + "do!"),
    ("unimplemented!", "unimplemented" + "!"),
    ("UnsupportedOperationException", "UnsupportedOperation" + "Exception"),
]


def run_git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def commit_exists(ref: str) -> bool:
    proc = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}^{{commit}}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return proc.returncode == 0


def select_range(explicit_base: str | None) -> str:
    if explicit_base:
        if not commit_exists(explicit_base):
            raise RuntimeError(f"base commit/ref not found: {explicit_base}")
        return f"{explicit_base}...HEAD"

    event = os.environ.get("GITHUB_EVENT_NAME", "")
    if event == "pull_request":
        base_name = os.environ.get("GITHUB_BASE_REF") or "main"
        base = f"origin/{base_name}"
        if not commit_exists(base):
            raise RuntimeError(f"pull-request base ref not found: {base}")
        return f"{base}...HEAD"

    before = os.environ.get("GITHUB_EVENT_BEFORE", "")
    if re.fullmatch(r"[0-9a-f]{40}", before or "") and set(before) != {"0"} and commit_exists(before):
        return f"{before}..HEAD"
    if commit_exists("HEAD^"):
        return "HEAD^..HEAD"
    raise RuntimeError("unable to establish a bounded git diff range")


def is_fixture(path: Path) -> bool:
    parts = set(path.parts)
    return "fixtures" in parts and "tests" in parts


def changed_executable_files(diff_range: str) -> list[Path]:
    output = run_git("diff", "--name-only", "--diff-filter=ACMR", diff_range)
    result: list[Path] = []
    for raw in output.splitlines():
        path = Path(raw)
        if not raw or is_fixture(path):
            continue
        if path.suffix in EXECUTABLE_SUFFIXES and path.is_file():
            result.append(path)
    return sorted(result)


def scan(path: Path) -> list[str]:
    findings: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return [f"{path}:READ_ERROR:{exc}"]
    for number, line in enumerate(lines, start=1):
        if SUPPRESSION in line:
            continue
        for label, token in TOKEN_PARTS:
            if token in line:
                findings.append(f"{path}:{number}:{label}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="optional explicit base ref/commit")
    args = parser.parse_args()
    try:
        diff_range = select_range(args.base)
        files = changed_executable_files(diff_range)
    except RuntimeError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2

    findings: list[str] = []
    for path in files:
        findings.extend(scan(path))

    print(f"diff_range={diff_range}")
    print(f"changed_executable_files={len(files)}")
    if findings:
        for finding in findings:
            print(f"FAIL: unresolved executable debt marker: {finding}", file=sys.stderr)
        print(
            "Implement the code or add an explicit same-line `DEBT_OK:` justification; "
            "do not silence the gate globally.",
            file=sys.stderr,
        )
        return 1

    print("PASS: no newly introduced unresolved executable debt markers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
