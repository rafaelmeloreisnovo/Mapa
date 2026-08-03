#!/usr/bin/env python3
"""Fail-closed integral evidence gate for RAFAELIA.

The gate validates evidence shape and computes a promotion decision.  A
structurally valid blocked receipt is a successful audit result: uncertainty is
preserved as TOKEN_VAZIO instead of being converted into PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SHA1 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SPDX = re.compile(r"^[A-Za-z0-9.+-]+$")
ALLOWED_STATUS = {"PASS", "FAIL", "TOKEN_VAZIO"}
ALLOWED_CLAIM_CLASSES = {
    "PROVADO",
    "EVIDENCIADO",
    "HIPOTESE",
    "MODELO",
    "PARABOLA",
    "REFUTADO",
    "TOKEN_VAZIO",
}
SHELLS = {"sh", "bash", "dash", "zsh", "fish", "cmd", "powershell", "pwsh"}

REQUIRED_CRITERIA = (
    "hash_valid",
    "authorship_identified",
    "license_known",
    "build_reproducible",
    "tests_executed",
    "receipt_stored",
    "claim_compatible",
    "source_commit_bound",
    "dependency_provenance",
    "falsifiers_exercised",
    "privacy_secret_scan",
    "promotion_control",
    "physical_runtime_receipt",
    "independent_reproduction",
)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_sha1(value: Any) -> bool:
    return isinstance(value, str) and SHA1.fullmatch(value) is not None


def valid_sha256(value: Any) -> bool:
    return isinstance(value, str) and SHA256.fullmatch(value) is not None


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def argv_safe(value: Any) -> bool:
    if not isinstance(value, list) or not value:
        return False
    for command in value:
        if not isinstance(command, list) or not command:
            return False
        if not all(nonempty(item) and "\x00" not in item and "\n" not in item for item in command):
            return False
        executable = Path(command[0]).name.lower()
        if executable in SHELLS:
            return False
    return True


def evidence_list(value: Any) -> bool:
    return isinstance(value, list) and all(nonempty(item) for item in value)


def validate_artifacts(receipt: dict[str, Any], errors: list[str]) -> bool:
    artifacts = receipt.get("artifacts")
    add(errors, isinstance(artifacts, list) and len(artifacts) > 0,
        "artifacts must be a non-empty array")
    if not isinstance(artifacts, list) or not artifacts:
        return False

    seen: set[str] = set()
    ok = True
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            errors.append(f"artifact[{index}] must be an object")
            ok = False
            continue
        path = artifact.get("path")
        add(errors, nonempty(path), f"artifact[{index}].path is required")
        if nonempty(path):
            add(errors, path not in seen, f"duplicate artifact path: {path}")
            seen.add(path)
        digest_ok = valid_sha1(artifact.get("git_blob_sha1")) or valid_sha256(artifact.get("sha256"))
        add(errors, digest_ok, f"artifact[{index}] requires git_blob_sha1 or sha256")
        add(errors, artifact.get("verified") in {True, False},
            f"artifact[{index}].verified must be boolean")
        ok = ok and nonempty(path) and digest_ok and artifact.get("verified") in {True, False}
    return ok


def validate_criterion(name: str, criterion: Any, receipt: dict[str, Any], errors: list[str]) -> None:
    add(errors, isinstance(criterion, dict), f"criteria.{name} must be an object")
    if not isinstance(criterion, dict):
        return
    status = criterion.get("status")
    add(errors, status in ALLOWED_STATUS, f"criteria.{name}.status is invalid")
    add(errors, evidence_list(criterion.get("evidence")),
        f"criteria.{name}.evidence must be an array of strings")
    if status != "PASS":
        add(errors, nonempty(criterion.get("next_verifiable_step")),
            f"criteria.{name}.next_verifiable_step is required when not PASS")

    if name == "hash_valid" and status == "PASS":
        artifacts = receipt.get("artifacts", [])
        add(errors, isinstance(artifacts, list) and bool(artifacts) and
            all(isinstance(a, dict) and a.get("verified") is True for a in artifacts),
            "hash_valid PASS requires every artifact to be verified")

    elif name == "authorship_identified" and status == "PASS":
        authors = criterion.get("authors")
        add(errors, isinstance(authors, list) and bool(authors),
            "authorship_identified PASS requires authors")
        if isinstance(authors, list):
            for i, author in enumerate(authors):
                add(errors, isinstance(author, dict), f"authors[{i}] must be an object")
                if isinstance(author, dict):
                    add(errors, nonempty(author.get("identity")), f"authors[{i}].identity is required")
                    add(errors, nonempty(author.get("role")), f"authors[{i}].role is required")
                    add(errors, valid_sha1(author.get("commit_sha")),
                        f"authors[{i}].commit_sha must bind authorship to a commit")

    elif name == "license_known" and status == "PASS":
        license_data = criterion.get("license")
        add(errors, isinstance(license_data, dict), "license_known PASS requires license object")
        if isinstance(license_data, dict):
            add(errors, nonempty(license_data.get("spdx")) and
                SPDX.fullmatch(license_data["spdx"]) is not None,
                "license.spdx is invalid")
            add(errors, nonempty(license_data.get("path")), "license.path is required")
            add(errors, valid_sha1(license_data.get("git_blob_sha1")) or
                valid_sha256(license_data.get("sha256")),
                "license requires a content digest")

    elif name == "build_reproducible" and status == "PASS":
        build = criterion.get("build")
        add(errors, isinstance(build, dict), "build_reproducible PASS requires build object")
        if isinstance(build, dict):
            add(errors, build.get("executed") is True, "build.executed must be true")
            add(errors, build.get("exit_code") == 0, "build.exit_code must be 0")
            add(errors, nonempty(build.get("toolchain")) and nonempty(build.get("toolchain_digest")),
                "build requires pinned toolchain and digest")
            add(errors, argv_safe(build.get("commands")), "build.commands must be safe argv arrays")
            add(errors, valid_sha256(build.get("output_sha256")), "build.output_sha256 is invalid")
            add(errors, isinstance(build.get("replay_count"), int) and build["replay_count"] >= 2,
                "build.replay_count must be at least 2")
            add(errors, build.get("outputs_match") is True, "build.outputs_match must be true")
            add(errors, nonempty(build.get("receipt")), "build.receipt is required")

    elif name == "tests_executed" and status == "PASS":
        tests = criterion.get("tests")
        add(errors, isinstance(tests, dict), "tests_executed PASS requires tests object")
        if isinstance(tests, dict):
            counts = tests.get("counts")
            add(errors, isinstance(counts, dict), "tests.counts is required")
            if isinstance(counts, dict):
                required = ("discovered", "executed", "passed", "failed", "skipped")
                add(errors, all(isinstance(counts.get(k), int) and counts[k] >= 0 for k in required),
                    "test counts must be non-negative integers")
                if all(isinstance(counts.get(k), int) for k in required):
                    add(errors, counts["discovered"] > 0 and
                        counts["discovered"] == counts["executed"] == counts["passed"] and
                        counts["failed"] == 0 and counts["skipped"] == 0,
                        "all discovered tests must execute and pass with no failures or skips")
            add(errors, nonempty(tests.get("receipt")), "tests.receipt is required")

    elif name == "receipt_stored" and status == "PASS":
        stored = criterion.get("receipt")
        add(errors, isinstance(stored, dict), "receipt_stored PASS requires receipt object")
        if isinstance(stored, dict):
            path = stored.get("path")
            add(errors, nonempty(path) and
                (path.startswith("data/receipts/") or path.startswith("evidence/")),
                "stored receipt path must be append-only evidence")
            add(errors, valid_sha256(stored.get("sha256")), "stored receipt sha256 is invalid")
            add(errors, stored.get("append_only") is True, "stored receipt must be append-only")
            add(errors, stored.get("commit_bound") is True, "stored receipt must be commit-bound")

    elif name == "claim_compatible" and status == "PASS":
        claim = criterion.get("claim")
        add(errors, isinstance(claim, dict), "claim_compatible PASS requires claim object")
        if isinstance(claim, dict):
            add(errors, claim.get("classification") in ALLOWED_CLAIM_CLASSES,
                "claim classification is invalid")
            add(errors, claim.get("claim_allowed") in {True, False},
                "claim_allowed must be boolean")
            if claim.get("classification") in {"HIPOTESE", "MODELO", "PARABOLA", "TOKEN_VAZIO", "REFUTADO"}:
                add(errors, claim.get("claim_allowed") is False,
                    "non-promotable claim classes require claim_allowed=false")

    elif name == "source_commit_bound" and status == "PASS":
        source = receipt.get("source", {})
        add(errors, isinstance(source, dict) and valid_sha1(source.get("commit_sha")),
            "source_commit_bound PASS requires a valid source commit")
        add(errors, isinstance(source, dict) and source.get("worktree_clean") is True,
            "source_commit_bound PASS requires clean worktree")

    elif name == "dependency_provenance" and status == "PASS":
        deps = criterion.get("dependencies")
        add(errors, isinstance(deps, list) and bool(deps),
            "dependency_provenance PASS requires dependencies")
        if isinstance(deps, list):
            for i, dep in enumerate(deps):
                add(errors, isinstance(dep, dict), f"dependencies[{i}] must be an object")
                if isinstance(dep, dict):
                    add(errors, nonempty(dep.get("name")), f"dependencies[{i}].name is required")
                    add(errors, nonempty(dep.get("version_or_ref")),
                        f"dependencies[{i}].version_or_ref is required")
                    add(errors, valid_sha256(dep.get("digest")) or valid_sha1(dep.get("commit_sha")),
                        f"dependencies[{i}] requires digest or commit_sha")

    elif name == "falsifiers_exercised" and status == "PASS":
        falsifiers = criterion.get("falsifiers")
        add(errors, isinstance(falsifiers, list) and bool(falsifiers),
            "falsifiers_exercised PASS requires falsifiers")
        if isinstance(falsifiers, list):
            for i, falsifier in enumerate(falsifiers):
                add(errors, isinstance(falsifier, dict), f"falsifiers[{i}] must be an object")
                if isinstance(falsifier, dict):
                    add(errors, nonempty(falsifier.get("id")), f"falsifiers[{i}].id is required")
                    add(errors, falsifier.get("status") == "EXERCISED",
                        f"falsifiers[{i}] must be EXERCISED")

    elif name == "privacy_secret_scan" and status == "PASS":
        scan = criterion.get("scan")
        add(errors, isinstance(scan, dict), "privacy_secret_scan PASS requires scan object")
        if isinstance(scan, dict):
            add(errors, scan.get("executed") is True, "scan.executed must be true")
            add(errors, scan.get("findings") == 0, "scan.findings must be zero")
            add(errors, nonempty(scan.get("receipt")), "scan.receipt is required")

    elif name == "promotion_control" and status == "PASS":
        control = criterion.get("control")
        add(errors, isinstance(control, dict), "promotion_control PASS requires control object")
        if isinstance(control, dict):
            add(errors, control.get("automatic_merge") is False,
                "automatic_merge must be false")
            add(errors, control.get("human_review_required") is True,
                "human_review_required must be true")
            add(errors, isinstance(control.get("required_checks"), list) and
                bool(control.get("required_checks")) and
                all(nonempty(x) for x in control["required_checks"]),
                "required_checks must be named")
            add(errors, control.get("negative_test_executed") is True,
                "promotion control requires a negative test")

    elif name == "physical_runtime_receipt" and status == "PASS":
        runtime = criterion.get("runtime")
        add(errors, isinstance(runtime, dict), "physical_runtime_receipt PASS requires runtime object")
        if isinstance(runtime, dict):
            add(errors, runtime.get("physical_device") is True, "physical_device must be true")
            add(errors, nonempty(runtime.get("device_class")), "device_class is required")
            add(errors, nonempty(runtime.get("receipt")), "runtime receipt is required")
            add(errors, valid_sha256(runtime.get("receipt_sha256")),
                "runtime receipt_sha256 is invalid")

    elif name == "independent_reproduction" and status == "PASS":
        reproduction = criterion.get("reproduction")
        add(errors, isinstance(reproduction, dict),
            "independent_reproduction PASS requires reproduction object")
        if isinstance(reproduction, dict):
            add(errors, reproduction.get("independent_environment") is True,
                "independent_environment must be true")
            add(errors, reproduction.get("outputs_match") is True,
                "independent outputs must match")
            add(errors, nonempty(reproduction.get("receipt")),
                "independent reproduction receipt is required")


def compute_decision(criteria: dict[str, Any], policy: dict[str, Any]) -> tuple[str, list[str]]:
    blockers = policy.get("promotion_blockers", list(REQUIRED_CRITERIA))
    blocking: list[str] = []
    has_fail = False
    for name in blockers:
        criterion = criteria.get(name, {})
        status = criterion.get("status") if isinstance(criterion, dict) else None
        if status != "PASS":
            blocking.append(name)
        if status == "FAIL":
            has_fail = True
    if has_fail:
        return "BLOCKED_FAIL", blocking
    if blocking:
        return "BLOCKED_TOKEN_VAZIO", blocking
    return "READY_FOR_DOMAIN_REVIEW", []


def validate(receipt: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    add(errors, receipt.get("schema") == "rafaelia.integral-gate-receipt/v1",
        "unexpected receipt schema")
    add(errors, policy.get("schema") == "rafaelia.integral-gate-policy/v1",
        "unexpected policy schema")
    add(errors, nonempty(receipt.get("receipt_id")), "receipt_id is required")
    add(errors, nonempty(receipt.get("observed_at")), "observed_at is required")

    source = receipt.get("source")
    add(errors, isinstance(source, dict), "source must be an object")
    if isinstance(source, dict):
        add(errors, nonempty(source.get("repository")), "source.repository is required")
        add(errors, valid_sha1(source.get("commit_sha")), "source.commit_sha is invalid")
        add(errors, nonempty(source.get("branch")), "source.branch is required")

    artifacts_ok = validate_artifacts(receipt, errors)

    criteria = receipt.get("criteria")
    add(errors, isinstance(criteria, dict), "criteria must be an object")
    if not isinstance(criteria, dict):
        criteria = {}
    required = policy.get("required_criteria", list(REQUIRED_CRITERIA))
    add(errors, isinstance(required, list) and required == list(REQUIRED_CRITERIA),
        "policy.required_criteria must match the canonical integral gate order")
    for name in REQUIRED_CRITERIA:
        add(errors, name in criteria, f"missing criterion: {name}")
        validate_criterion(name, criteria.get(name), receipt, errors)

    decision = receipt.get("decision")
    add(errors, isinstance(decision, dict), "decision must be an object")
    computed, blocking = compute_decision(criteria, policy)
    if isinstance(decision, dict):
        add(errors, decision.get("result") == computed,
            f"decision.result must equal computed result {computed}")
        add(errors, decision.get("blocking_criteria") == blocking,
            "decision.blocking_criteria does not match computed blockers")
        add(errors, decision.get("claim_allowed") is False,
            "integral gate v1 never promotes claims directly")
        add(errors, decision.get("automatic_merge") is False,
            "integral gate v1 requires automatic_merge=false")

    return {
        "receipt_valid": not errors and artifacts_ok,
        "computed_result": computed,
        "blocking_criteria": blocking,
        "claim_allowed": False,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument(
        "--policy",
        type=Path,
        default=Path("data/control-plane/integral-gate.v1.json"),
    )
    args = parser.parse_args()
    try:
        receipt_bytes = args.receipt.read_bytes()
        receipt = load_json(args.receipt)
        policy = load_json(args.policy)
        result = validate(receipt, policy)
        result["receipt_file_sha256"] = hashlib.sha256(receipt_bytes).hexdigest()
    except (OSError, ValueError) as exc:
        print(json.dumps({"receipt_valid": False, "errors": [str(exc)]}, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["receipt_valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
