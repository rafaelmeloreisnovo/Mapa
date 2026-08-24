#!/usr/bin/env python3
"""Validate the bounded NOVOexport RAW 048-050 historical-byte evidence packet."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/evidence/novoexport_raw048_050_wave3_20260824.v1.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
EXPECTED = {
    "conversations-048.json": (36771626, 100, 6543, "ed19ea07f8763a8a4d87204d80c817694ce4d6c339c71b1d2a1b955a8c125256"),
    "conversations-049.json": (47806754, 100, 7196, "608e45449809a47f5931f86328b96dab2b2b86a5abf21a8dfe1c7da6834a2f1a"),
    "conversations-050.json": (17115060, 54, 3647, "c5058bf25f682de12de68b54029d13b07e836cd519416752fbc5e4fa320b4979"),
}


def main() -> int:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    assert data["schema"] == "rafaelia.novoexport-raw048-050-wave3/v1"
    assert data["claim_allowed"] is False
    assert data["state"] == "PARTIAL_EVIDENCED_HISTORICAL_BYTES_CURRENT_PROVIDER_UNBOUND"
    assert data["authority"]["private_provider_locators_persisted_publicly"] is False

    objects = data["objects"]
    assert len(objects) == 3
    seen = set()
    for obj in objects:
        name = obj["file"]
        assert name in EXPECTED and name not in seen
        seen.add(name)
        size, conversations, messages, digest = EXPECTED[name]
        assert obj["bytes"] == size
        assert obj["physical_inventory_bytes"] == size
        assert obj["size_matches"] is True
        assert obj["conversations"] == conversations
        assert obj["messages"] == messages
        assert obj["historical_download_sha256"] == digest
        assert HEX64.fullmatch(obj["historical_download_sha256"])
        assert obj["historical_bytes_parse"] == "EVIDENCED"
        assert obj["current_provider_object"].startswith("TOKEN_VAZIO_")
        assert obj["current_byte_stream"].startswith("TOKEN_VAZIO_")
        assert obj["current_sha256"].startswith("TOKEN_VAZIO_")
        assert obj["exact_pid_set"].startswith("TOKEN_VAZIO_")
    assert seen == set(EXPECTED)

    remaining = set(data["gap_transition"]["remaining"])
    assert "directly addressable current provider objects" in remaining
    assert "current SHA-256 rehash" in remaining
    assert "exact conversation_id/PID sets" in remaining
    assert "HISTORICAL_DOWNLOADED_BYTES != CURRENT_PROVIDER_CUSTODY" in data["invariants"]
    print("PASS: RAW048-050 historical byte evidence narrowed without promoting current provider custody")
    return 0


if __name__ == "__main__":
    sys.exit(main())
