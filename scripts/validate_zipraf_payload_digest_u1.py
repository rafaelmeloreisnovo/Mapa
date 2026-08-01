#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

BLAKE3_COMMIT = "ff6991d8b13f5b4b16dc311b5acc9c63ae835152"
RECEIPT_SHA256 = "5c02f528713539e33d0cfabf6c99fa6d03b619c16d645b6c3ef099b0c93b2cb4"
FALSE_INVARIANTS = {
    "crc32_is_cryptographic_identity",
    "stored_digest_equals_deflate_logical_digest",
    "digest_grants_execution",
    "digest_grants_dma",
    "digest_proves_authorship",
    "digest_is_signature",
    "digest_is_clock_measurement",
    "unpinned_provider_is_authorized",
}


def fail(message: str) -> None:
    raise ValueError(message)


def validate(data: dict[str, Any]) -> None:
    if data.get("schema_version") != "zipraf-payload-digest-u1.v1":
        fail("schema_version")
    if data.get("claim_allowed") is not False:
        fail("claim_allowed")

    producer = data.get("producer", {})
    if producer.get("repository") != "rafaelmeloreisnovo/Vectras-VM-Android":
        fail("producer repository")
    if producer.get("pull_request") != 1078 or producer.get("merged") is not False:
        fail("producer PR state")
    if producer.get("gate_name") != "ZIPRAF Payload Digest U1":
        fail("gate name")
    if producer.get("gate_run") != 30721856193 or producer.get("gate_result") != "PASS":
        fail("remote gate")
    head = producer.get("head_sha")
    if not isinstance(head, str) or len(head) != 40:
        fail("producer head")
    int(head, 16)

    providers = data.get("providers", {})
    sha = providers.get("sha256", {})
    if sha.get("implementation") != "RMR_PORTABLE_C" or sha.get("digest_bytes") != 32:
        fail("SHA-256 provider")
    if set(sha.get("known_answer_vectors", [])) != {"EMPTY", "ABC"}:
        fail("SHA-256 KATs")

    blake3 = providers.get("blake3", {})
    if blake3.get("repository") != "rafaelmeloreisnovo/BLAKE3":
        fail("BLAKE3 repository")
    if blake3.get("commit") != BLAKE3_COMMIT:
        fail("BLAKE3 immutable commit")
    if blake3.get("c_api_version") != "1.8.2":
        fail("BLAKE3 API version")
    if blake3.get("backend") != "PORTABLE_C_SIMD_DISABLED":
        fail("BLAKE3 backend")
    if blake3.get("digest_bytes") != 32:
        fail("BLAKE3 digest length")
    if set(blake3.get("known_answer_vectors", [])) != {"EMPTY", "ABC"}:
        fail("BLAKE3 KATs")

    scopes = data.get("digest_scopes", {})
    if scopes.get("STORED_BYTES") != "EXACT_ARCHIVE_PAYLOAD_SPAN":
        fail("stored scope")
    if scopes.get("LOGICAL_BYTES_STORE") != "STORED_EQUALS_LOGICAL":
        fail("STORE logical scope")
    if scopes.get("LOGICAL_BYTES_DEFLATE") != "MATERIALIZATION_REQUIRED":
        fail("DEFLATE logical scope")

    receipt = data.get("receipt", {})
    if receipt.get("gate") != "ZIPRAF_PAYLOAD_DIGEST_U1_V1":
        fail("receipt gate")
    if receipt.get("status") != "PASS" or receipt.get("checks") != 17:
        fail("receipt result")
    if receipt.get("sha256") != RECEIPT_SHA256:
        fail("receipt SHA-256")
    if receipt.get("scope") != "STORED_BYTES_AND_STORE_LOGICAL_BYTES_NO_DEFLATE_MATERIALIZATION":
        fail("receipt scope")
    if receipt.get("artifact_storage") != "QUOTA_BLOCKED_RECEIPT_VALIDATED_HASHED_IN_LOG":
        fail("artifact quota boundary")

    invariants = data.get("promotion_invariants", {})
    for key in FALSE_INVARIANTS:
        if invariants.get(key) is not False:
            fail(f"unsafe promotion: {key}")

    formula = data.get("formula_ci_repair", {})
    if formula.get("state") != "PASS" or formula.get("run") != 30721856200:
        fail("formula CI repair")
    if formula.get("canonical_source") != "engine/model.py":
        fail("formula canonical source")
    if formula.get("compatibility_bridge") != "formula_ci/model.py":
        fail("formula compatibility bridge")
    if formula.get("formula_logic_duplicated") is not False:
        fail("formula logic duplicated")
    if formula.get("scientific_claim") is not False:
        fail("formula scientific overclaim")

    dependency = data.get("next_dependency", {})
    if dependency.get("order") != "U2" or dependency.get("state") != "TOKEN_VAZIO":
        fail("next dependency")

    claims = data.get("claims", {})
    if claims.get("deflate_logical_digest") != "MATERIALIZATION_REQUIRED":
        fail("DEFLATE claim")
    if claims.get("signature_or_authorship") != "NOT_PROVIDED_BY_DIGEST":
        fail("authorship boundary")
    if claims.get("android_runtime") != "TOKEN_VAZIO":
        fail("Android runtime claim")
    if claims.get("claim_allowed") is not False:
        fail("nested claim_allowed")


def main() -> int:
    path = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else "data/control-plane/zipraf-payload-digest-u1.v1.json"
    )
    validate(json.loads(path.read_text(encoding="utf-8")))
    print("ZIPRAF_PAYLOAD_DIGEST_U1_FEDERATION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
