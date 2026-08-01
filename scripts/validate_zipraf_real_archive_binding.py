#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

EXPECTED_ACTIONS = {"DIRECT_MAP_LAYOUT", "COPY_STORE", "DECOMPRESS", "REJECT"}
FALSE_INVARIANTS = {
    "layout_mappable_grants_digest",
    "layout_mappable_grants_execution",
    "layout_mappable_grants_dma",
    "magic_grants_execution",
    "crc32_is_content_identity",
    "hash_is_clock_measurement",
    "deflate_is_direct_map",
    "unsafe_name_can_bind",
}
REQUIRED_URGENCY = {f"U{i}" for i in range(9)}


def fail(message: str) -> None:
    raise ValueError(message)


def validate(data: dict[str, Any]) -> None:
    if data.get("schema_version") != "zipraf-real-archive-binding.v2":
        fail("schema_version")
    if data.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")

    producer = data.get("producer", {})
    if producer.get("repository") != "rafaelmeloreisnovo/Vectras-VM-Android":
        fail("producer repository")
    if producer.get("pull_request") != 1078:
        fail("producer pull request")
    if not isinstance(producer.get("head_sha"), str) or len(producer["head_sha"]) != 40:
        fail("producer head_sha")
    int(producer["head_sha"], 16)
    if producer.get("merged") is not False:
        fail("open producer cannot be recorded as merged")

    compatibility = data.get("compatibility", {})
    if compatibility.get("envelope") != "ZIP_CLASSIC":
        fail("compatibility envelope")
    if compatibility.get("zip64") != "EXPLICITLY_UNSUPPORTED_V2":
        fail("ZIP64 scope")
    if compatibility.get("multidisk") != "REJECTED":
        fail("multidisk policy")
    if compatibility.get("central_local_binding") is not True:
        fail("central/local binding")

    actions = data.get("entry_actions")
    if not isinstance(actions, list) or set(actions) != EXPECTED_ACTIONS or len(actions) != 4:
        fail("entry action algebra")

    invariants = data.get("promotion_invariants", {})
    for key in FALSE_INVARIANTS:
        if invariants.get(key) is not False:
            fail(f"unsafe promotion invariant: {key}")

    kat = data.get("host_kat", {})
    if not isinstance(kat.get("verification_count"), int) or kat["verification_count"] < 37:
        fail("host KAT count")
    if kat.get("local_result") != "PASS":
        fail("host KAT local result")

    receipt = data.get("mmap_receipt_contract", {})
    if receipt.get("gate") != "ZIPRAF_HOST_MMAP_V1":
        fail("mmap gate")
    if receipt.get("explicit_user_copy_bytes") != 0:
        fail("explicit user copy contract")
    if receipt.get("scope") != "HOST_MMAP_LAYOUT_NOT_ANDROID_DMA_OR_EXECUTION":
        fail("mmap scope")
    if receipt.get("kernel_or_hardware_zero_copy_claim") is not False:
        fail("kernel/hardware zero-copy overclaim")

    scheduling = data.get("scheduling", {})
    if scheduling.get("physical_clock_harmonic") != "TOKEN_VAZIO":
        fail("clock harmonic claim")
    if scheduling.get("octa_core_runtime") != "TOKEN_VAZIO":
        fail("octa-core runtime claim")

    security = data.get("security_policy", {})
    required_security = {
        "reject_absolute_paths",
        "reject_parent_traversal",
        "reject_empty_segments",
        "reject_trailing_dot_or_space",
        "reject_reserved_devices",
        "reject_portable_name_collisions",
        "reject_symlink_binding",
        "reject_encrypted_binding",
    }
    if any(security.get(key) is not True for key in required_security):
        fail("security policy weakened")

    urgency = data.get("urgency")
    if not isinstance(urgency, list) or {item.get("order") for item in urgency} != REQUIRED_URGENCY:
        fail("urgency matrix")
    if [item.get("order") for item in urgency] != [f"U{i}" for i in range(9)]:
        fail("urgency order")
    by_order = {item["order"]: item for item in urgency}
    if by_order["U6"].get("state") != "NOT_AUTHORIZED":
        fail("BitRafa 35-45 boundary")

    claims = data.get("claims", {})
    if claims.get("compressed_zero_copy") is not False:
        fail("compressed zero-copy")
    if claims.get("android_mmap") != "TOKEN_VAZIO":
        fail("Android mmap claim")
    if claims.get("dma_iommu_irq_hardware") != "TOKEN_VAZIO":
        fail("DMA hardware claim")
    if claims.get("bitflip_35_45_recovery") != "NOT_AUTHORIZED":
        fail("35-45 recovery claim")
    if claims.get("blockchain_consensus") != "TOKEN_VAZIO":
        fail("blockchain consensus claim")


def main() -> int:
    path = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else "data/control-plane/zipraf-real-archive-binding.v2.json"
    )
    validate(json.loads(path.read_text(encoding="utf-8")))
    print("ZIPRAF_REAL_ARCHIVE_BINDING_V2 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
