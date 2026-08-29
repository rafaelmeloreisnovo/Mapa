#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "data/quality/MARKDOWN_DEBT_BASELINE_20260829.v1.json"


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def main() -> None:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    expected_version = baseline["tool"]["version"]

    version = subprocess.run(
        ["markdownlint-cli2", "--version"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    version_text = (version.stdout + "\n" + version.stderr).strip()
    if version.returncode != 0:
        fail(f"markdownlint-cli2 --version failed: {version_text}")
    if expected_version not in version_text:
        fail(f"tool drift: expected markdownlint-cli2 {expected_version}; got {version_text!r}")

    proc = subprocess.run(
        ["markdownlint-cli2", "**/*.md", "#node_modules"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (proc.stdout or "") + (proc.stderr or "")

    linting = re.findall(r"^Linting:\s+(\d+)\s+files\s*$", output, flags=re.MULTILINE)
    summaries = re.findall(
        r"^Summary:\s+(\d+)\s+issues?\s+in\s+(\d+)\s+files?\s*$",
        output,
        flags=re.MULTILINE,
    )

    files_linted = int(linting[-1]) if linting else None
    if summaries:
        issues, files_with_issues = map(int, summaries[-1])
    elif proc.returncode == 0:
        issues, files_with_issues = 0, 0
    else:
        tail = "\n".join(output.splitlines()[-20:])
        fail("linter failed without parseable debt summary:\n" + tail)

    ceiling_issues = int(baseline["scope"]["issues"])
    ceiling_files = int(baseline["scope"]["files_with_issues"])

    print(
        "MARKDOWN_DEBT "
        f"tool={expected_version} files_linted={files_linted if files_linted is not None else 'UNKNOWN'} "
        f"issues={issues}/{ceiling_issues} files_with_issues={files_with_issues}/{ceiling_files}"
    )

    if issues > ceiling_issues:
        fail(f"historical Markdown debt increased: {issues} > {ceiling_issues}")
    if files_with_issues > ceiling_files:
        fail(
            "Markdown debt spread to more files: "
            f"{files_with_issues} > {ceiling_files}"
        )

    if issues < ceiling_issues or files_with_issues < ceiling_files:
        print("PASS: Markdown historical debt decreased; baseline remains a ceiling, not a target")
    else:
        print("PASS: Markdown historical debt did not increase")


if __name__ == "__main__":
    main()
