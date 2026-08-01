#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

OBSERVE_ONLY = {"NONE", "PARITY2_OBSERVE", "ECC32_MASKED_OBSERVE"}
DIGEST_LENGTH = {"SHA256": 64, "BLAKE3": 64}


def fail(message: str) -> None:
    raise ValueError(message)


def is_power_of_two(value: int) -> bool:
    return value > 0 and value & (value - 1) == 0


def ranges_overlap(a0: int, alen: int, b0: int, blen: int) -> bool:
    return a0 < b0 + blen and b0 < a0 + alen


def validate(data: dict[str, Any]) -> None:
    if data.get("schema_version") != "zipraf-content-page-graph.v1":
        fail("schema_version")
    if data.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")

    shell = data.get("compatibility_shell", {})
    if shell.get("format") != "ZIP":
        fail("ZIP compatibility shell required")
    if shell.get("direct_map_rule") != "STORE_ALIGNED_IMMUTABLE_DIGEST_VERIFIED":
        fail("direct_map_rule")

    invariants = data.get("invariants", {})
    for key in (
        "absolute_pointer_reuse_across_epoch",
        "magic_grants_execution",
        "hash_is_clock_measurement",
        "system_attribute_is_pinning",
    ):
        if invariants.get(key) is not False:
            fail(f"unsafe invariant: {key}")

    blocks = data.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        fail("blocks")
    block_map: dict[str, dict[str, Any]] = {}
    spans: list[tuple[int, int, str, str]] = []

    for block in blocks:
        block_id = block.get("block_id")
        if not isinstance(block_id, str) or not block_id or block_id in block_map:
            fail("duplicate/invalid block_id")
        block_map[block_id] = block
        offset = block.get("archive_offset")
        stored = block.get("stored_size")
        logical = block.get("logical_size")
        alignment = block.get("alignment")
        if not all(isinstance(x, int) and x > 0 for x in (stored, logical, alignment)):
            fail(f"invalid sizes {block_id}")
        if not isinstance(offset, int) or offset < 0 or not is_power_of_two(alignment):
            fail(f"invalid offset/alignment {block_id}")

        digest_kind = block.get("digest_kind")
        digest = block.get("digest")
        if digest_kind not in DIGEST_LENGTH or not isinstance(digest, str) or len(digest) != DIGEST_LENGTH[digest_kind]:
            fail(f"digest {block_id}")
        int(digest, 16)

        if block.get("direct_map_candidate"):
            if block.get("compression_method") != "STORE" or stored != logical:
                fail(f"compressed/size-mismatch direct map {block_id}")
            if offset % alignment or block.get("immutable") is not True:
                fail(f"unaligned/mutable direct map {block_id}")

        if block.get("execution_candidate") and not block.get("direct_map_candidate"):
            fail(f"execution candidate must first be direct-map candidate {block_id}")
        if block.get("magic_kind") in {"PE_MZ", "ELF"} and block.get("platform_loader_authorized") is True:
            fail(f"fixture cannot self-authorize loader {block_id}")

        redundancy = block.get("redundancy", {})
        profile = redundancy.get("profile")
        claim = redundancy.get("recovery_claim_ppm")
        if not isinstance(claim, int) or not 0 <= claim <= 1_000_000:
            fail(f"recovery claim {block_id}")
        if profile in OBSERVE_ONLY and claim != 0:
            fail(f"observe-only redundancy cannot recover {block_id}")
        if claim > 0 and not redundancy.get("erasure_positions_known"):
            fail(f"positive recovery requires known erasures {block_id}")
        if profile == "MDS_EXTERNAL_PROOF" and not redundancy.get("external_proof"):
            fail(f"MDS proof absent {block_id}")

        for o0, olen, odigest, oid in spans:
            if ranges_overlap(offset, stored, o0, olen):
                exact_alias = offset == o0 and stored == olen and digest == odigest
                if not exact_alias:
                    fail(f"overlapping archive spans {block_id}/{oid}")
        spans.append((offset, stored, digest, block_id))

    edges = data.get("edges")
    if not isinstance(edges, list):
        fail("edges")
    for i, edge in enumerate(edges):
        block = block_map.get(edge.get("block_id"))
        if block is None:
            fail("edge references unknown block")
        offset, length = edge.get("offset"), edge.get("length")
        if not isinstance(offset, int) or not isinstance(length, int) or offset < 0 or length <= 0:
            fail("edge range")
        if offset + length > block["logical_size"]:
            fail("edge outside block")
        if not isinstance(edge.get("core_mask"), int) or edge["core_mask"] <= 0:
            fail("core_mask")
        access = edge.get("access")
        if not isinstance(access, list) or not access:
            fail("access")
        if "WRITE" in access and block.get("immutable"):
            fail("write to immutable")
        if "EXEC_CANDIDATE" in access and not block.get("execution_candidate"):
            fail("exec edge on non-candidate")
        for other in edges[i + 1 :]:
            if edge.get("block_id") == other.get("block_id") and edge.get("phase") == other.get("phase"):
                if "WRITE" in access or "WRITE" in other.get("access", []):
                    if ranges_overlap(offset, length, other.get("offset", -1), other.get("length", 0)):
                        fail("same-phase write conflict")

    policy = data.get("dma_irq_policy", {})
    required_irq = {"IN_FLIGHT", "TRANSACTION_MATCH", "EPOCH_MATCH", "TTL_VALID"}
    if set(policy.get("irq_accept_requires", [])) != required_irq:
        fail("IRQ gate")
    if policy.get("remap_sequence") != ["QUIESCE", "VERIFY", "REMAP", "EPOCH_INCREMENT", "RESUME"]:
        fail("remap sequence")

    scheduling = data.get("scheduling", {})
    if scheduling.get("clock_harmonic_claim") != "TOKEN_VAZIO":
        fail("clock harmonic claim")
    ledger = data.get("ledger", {})
    if ledger.get("blockchain_consensus") != "TOKEN_VAZIO":
        fail("blockchain consensus claim")
    if ledger.get("hash_scope") != "CONTENT_AND_MANIFEST_IDENTITY_NOT_CLOCK":
        fail("hash scope")

    claims = data.get("claims", {})
    if claims.get("compressed_zero_copy") is not False:
        fail("compressed zero-copy")
    if claims.get("bitflip_35_45_recovery") != "NOT_AUTHORIZED":
        fail("35-45% claim")


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/control-plane/zipraf-content-page-graph.v1.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    validate(data)
    print("ZIPRAF_CONTENT_PAGE_GRAPH PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
