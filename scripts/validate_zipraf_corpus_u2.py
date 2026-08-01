#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

MANIFEST_SHA256 = "a92f5e288a596972289a6cff843d2fd5d9bff326964daa71902c56d5ad1635f5"
BLAKE3_PROVIDER = "rafaelmeloreisnovo/BLAKE3@ff6991d8b13f5b4b16dc311b5acc9c63ae835152"
FALSE_INVARIANTS = {
    "fixture_is_external_independent_corpus",
    "apk_extension_proves_apk_validity",
    "apk_markers_prove_signature",
    "apk_markers_grant_installation",
    "manifest_grants_execution",
    "manifest_grants_dma",
    "stored_deflate_digest_is_logical_digest",
    "scanner_extracts_entries",
    "scanner_executes_entries",
    "private_corpus_may_be_published_by_default",
}


def fail(message: str) -> None:
    raise ValueError(message)


def validate(data: dict[str, Any]) -> None:
    if data.get("schema_version") != "zipraf-corpus-u2.v1":
        fail("schema_version")
    if data.get("claim_allowed") is not False:
        fail("claim_allowed")

    producer = data.get("producer", {})
    if producer.get("repository") != "rafaelmeloreisnovo/Vectras-VM-Android":
        fail("producer repository")
    if producer.get("pull_request") != 1079:
        fail("producer pull request")
    if producer.get("base_branch") != "main_01_zipraf-real-archive-v2":
        fail("stacked base branch")
    if producer.get("merged") is not False:
        fail("open producer recorded as merged")
    if producer.get("gate_run") != 30722482763 or producer.get("gate_result") != "PASS":
        fail("producer gate")
    head = producer.get("head_sha")
    if not isinstance(head, str) or len(head) != 40:
        fail("producer head")
    int(head, 16)

    dependency = data.get("dependency", {})
    if dependency.get("u0_real_zip_spans") != "REMOTE_GATE_PASS":
        fail("U0 dependency")
    if dependency.get("u1_payload_identity") != "REMOTE_GATE_PASS":
        fail("U1 dependency")
    if dependency.get("stacked_on_pull_request") != 1078:
        fail("stacked PR dependency")

    harness = data.get("harness", {})
    expected_counts = {
        "archive_total": 3,
        "parsed_archives": 2,
        "parse_failures": 1,
        "entry_total": 6,
        "entry_rejected": 0,
    }
    if harness.get("gate") != "ZIPRAF_CORPUS_U2_HARNESS_V1":
        fail("harness gate")
    for key, expected in expected_counts.items():
        if harness.get(key) != expected:
            fail(f"harness {key}")
    if harness.get("extraction_performed") is not False:
        fail("extraction boundary")
    if harness.get("execution_authorized") is not False:
        fail("execution boundary")
    if harness.get("manifest_sha256") != MANIFEST_SHA256:
        fail("manifest receipt")
    if harness.get("artifact_storage") != "QUOTA_BLOCKED_RECEIPT_VALIDATED_HASHED_IN_LOG":
        fail("artifact quota state")

    fixtures = data.get("fixtures")
    if not isinstance(fixtures, list) or len(fixtures) != 3:
        fail("fixture count")
    by_name = {item.get("name"): item for item in fixtures if isinstance(item, dict)}
    if set(by_name) != {"sample.zip", "sample.apk", "malformed.zip"}:
        fail("fixture identities")
    if by_name["malformed.zip"].get("expected_state") != "PARSE_REJECTED":
        fail("negative fixture")
    if by_name["sample.apk"].get("signed_production_apk") is not False:
        fail("synthetic APK signing claim")

    contract = data.get("manifest_contract", {})
    if contract.get("blake3_provider") != BLAKE3_PROVIDER:
        fail("BLAKE3 provider")
    if contract.get("max_archive_bytes") != 268435456:
        fail("archive limit")
    if contract.get("max_entries_v2") != 64:
        fail("entry limit")
    archive_fields = contract.get("archive_fields")
    entry_fields = contract.get("entry_fields")
    if not isinstance(archive_fields, list) or "archive_sha256" not in archive_fields or "archive_blake3" not in archive_fields:
        fail("archive fields")
    if not isinstance(entry_fields, list) or "stored_sha256" not in entry_fields or "stored_blake3" not in entry_fields:
        fail("entry fields")
    if "execution_authorized" not in entry_fields or "dma_authorized" not in entry_fields:
        fail("entry authorization fields")

    invariants = data.get("promotion_invariants", {})
    for key in FALSE_INVARIANTS:
        if invariants.get(key) is not False:
            fail(f"unsafe promotion invariant: {key}")

    privacy = data.get("privacy", {})
    required_public = {
        "SOURCE_URI_OR_REPOSITORY",
        "SOURCE_COMMIT_OR_RELEASE",
        "FILE_SHA256",
        "LICENSE_OR_PROVENANCE",
        "SIZE_LIMIT",
        "EXPECTED_PARSER_STATE",
    }
    if set(privacy.get("public_corpus_requires", [])) != required_public:
        fail("public corpus provenance")
    if privacy.get("private_corpus_policy") != "RUN_LOCAL_AND_FEDERATE_SANITIZED_RECEIPTS_ONLY":
        fail("private corpus policy")

    dependency = data.get("next_dependency", {})
    if dependency.get("order") != "U2_REAL_CORPUS" or dependency.get("state") != "TOKEN_VAZIO":
        fail("real corpus boundary")

    claims = data.get("claims", {})
    if claims.get("u2_harness") != "REMOTE_GATE_PASS":
        fail("harness claim")
    if claims.get("deterministic_manifest") != "REMOTE_GATE_PASS":
        fail("manifest determinism claim")
    if claims.get("real_external_zip_apk_corpus") != "TOKEN_VAZIO":
        fail("external corpus overclaim")
    if claims.get("signed_production_apk") != "TOKEN_VAZIO":
        fail("production APK overclaim")
    if claims.get("android_installation") != "TOKEN_VAZIO":
        fail("Android installation overclaim")
    if claims.get("entry_execution") is not False:
        fail("entry execution overclaim")
    if claims.get("claim_allowed") is not False:
        fail("nested claim_allowed")


def main() -> int:
    path = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else "data/control-plane/zipraf-corpus-u2.v1.json"
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("root")
    validate(data)
    print("ZIPRAF_CORPUS_U2_FEDERATION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
