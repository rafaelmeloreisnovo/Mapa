#!/usr/bin/env python3
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "data/quality/MARKDOWN_DEBT_BASELINE_20260829.v1.json"


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def emit_debt_diagnostics(output: str) -> None:
    """Emit deterministic per-file/per-rule counts without changing gate semantics."""
    file_counts: Counter[str] = Counter()
    rule_counts: Counter[str] = Counter()
    issue_line = re.compile(
        r"^(?P<path>.+?):(?P<line>\d+)(?::(?P<column>\d+))?\s+"
        r"(?P<rule>MD\d{3}(?:/[^\s]+)?)\b"
    )
    for raw_line in output.splitlines():
        line = re.sub(r"\x1b\[[0-9;]*m", "", raw_line)
        match = issue_line.match(line)
        if not match:
            continue
        file_counts[match.group("path")] += 1
        rule_counts[match.group("rule").split("/", 1)[0]] += 1

    print(
        "MARKDOWN_DEBT_DIAGNOSTICS "
        f"parsed_issues={sum(file_counts.values())} files={len(file_counts)} rules={len(rule_counts)}"
    )
    for path, count in sorted(file_counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"MARKDOWN_DEBT_FILE count={count} path={path}")
    for rule, count in sorted(rule_counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"MARKDOWN_DEBT_RULE count={count} rule={rule}")


def main() -> None:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    expected_version = baseline["tool"]["version"]

    version = subprocess.run(
        ["npm", "list", "-g", "markdownlint-cli2", "--depth=0", "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if version.returncode != 0:
        fail("npm could not resolve installed markdownlint-cli2: " + (version.stderr or version.stdout).strip())
    try:
        version_data = json.loads(version.stdout)
        actual_version = version_data["dependencies"]["markdownlint-cli2"]["version"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        fail(f"cannot parse installed markdownlint-cli2 version: {exc}")
    if actual_version != expected_version:
        fail(f"tool drift: expected markdownlint-cli2 {expected_version}; got {actual_version}")

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
        f"tool={actual_version} files_linted={files_linted if files_linted is not None else 'UNKNOWN'} "
        f"issues={issues}/{ceiling_issues} files_with_issues={files_with_issues}/{ceiling_files}"
    )

    if issues > ceiling_issues or files_with_issues > ceiling_files:
        emit_debt_diagnostics(output)

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
