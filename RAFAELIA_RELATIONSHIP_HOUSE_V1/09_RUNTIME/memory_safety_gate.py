#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOUSE = ROOT / "RAFAELIA_RELATIONSHIP_HOUSE_V1"
CONTRACT = HOUSE / "00_AUTHORITY" / "MEMORY_SAFETY_GATE_V1.json"
BASELINE = HOUSE / "10_AUDIT" / "FROZEN_BASELINE_V1.json"

TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".yaml", ".yml", ".py", ".txt", ".tsv", ".csv"}


def fail(message: str) -> None:
    print(f"MEMORY_SAFETY_GATE=FAIL reason={message}")
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid_json:{path.relative_to(ROOT)}:{exc}")


def validate_contract() -> None:
    contract = load_json(CONTRACT)
    baseline = load_json(BASELINE)

    if contract.get("policy") != "FAIL_CLOSED":
        fail("contract_not_fail_closed")
    if contract.get("claim_allowed") is not False:
        fail("contract_claim_allowed_must_be_false")
    if baseline.get("status") != "FROZEN_BASELINE":
        fail("baseline_not_frozen")
    if baseline.get("immutable") is not True:
        fail("baseline_not_immutable")
    if baseline.get("claim_allowed") is not False:
        fail("baseline_claim_allowed_must_be_false")
    if baseline.get("private_location_persisted") is not False:
        fail("private_location_flag_must_be_false")
    if baseline.get("raw_private_content_persisted") is not False:
        fail("raw_private_content_flag_must_be_false")

    checks = baseline.get("checksum_set", {})
    for field in ("checksum_manifest_sha256", "index_manifest_sha256"):
        value = checks.get(field, "")
        if not re.fullmatch(r"[0-9a-f]{64}", value):
            fail(f"bad_sha256:{field}")

    rule = baseline.get("optimization_rule", {})
    if rule.get("v1_mutation_allowed") is not False:
        fail("v1_mutation_must_be_denied")
    if rule.get("promotion_method") != "POINTER_SWITCH_ONLY":
        fail("promotion_must_be_pointer_switch")
    if rule.get("rollback_target") != "V1":
        fail("rollback_target_must_be_v1")


def scan_public_boundary() -> None:
    # Patterns are assembled so the scanner source does not contain a real locator/secret literal.
    locator = re.compile(r"(?:drive|docs)" + r"\." + r"google" + r"\.com/(?:file/d|document/d|spreadsheets/d)/[A-Za-z0-9_-]{20,}")
    id_assignment = re.compile(r"(?:document_id|drive_id|file_id)\s*[:=]\s*[\"']?[A-Za-z0-9_-]{20,}", re.IGNORECASE)
    secret_markers = ["ghp" + "_", "github" + "_pat_", "sk" + "-", "AIza"[:2] + "Iza"]

    findings: list[str] = []
    for path in HOUSE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(ROOT)
        if locator.search(text):
            findings.append(f"private_locator:{rel}")
        if id_assignment.search(text):
            findings.append(f"private_id_assignment:{rel}")
        for marker in secret_markers:
            if marker in text:
                findings.append(f"secret_marker:{rel}")
                break

    if findings:
        fail("public_boundary:" + ",".join(sorted(set(findings))))


def assert_immutable_against(base_ref: str | None) -> None:
    if not base_ref:
        return
    rel = str(BASELINE.relative_to(ROOT))
    exists = subprocess.run(
        ["git", "cat-file", "-e", f"{base_ref}:{rel}"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0
    if not exists:
        return
    changed = subprocess.run(
        ["git", "diff", "--quiet", base_ref, "HEAD", "--", rel],
        cwd=ROOT,
        check=False,
    ).returncode != 0
    if changed:
        fail("frozen_baseline_modified_create_v2_instead")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", default=None)
    args = parser.parse_args()

    validate_contract()
    scan_public_boundary()
    assert_immutable_against(args.base_ref)
    print("MEMORY_SAFETY_GATE=PASS")
    print("baseline=V1 immutable=true promotion=POINTER_SWITCH_ONLY claim_allowed=false")


if __name__ == "__main__":
    main()
