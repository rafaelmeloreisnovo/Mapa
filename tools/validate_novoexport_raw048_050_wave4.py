#!/usr/bin/env python3
"""Validate the public-safe RAW 048-050 current-custody successor receipt."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/evidence/novoexport_raw048_050_wave4_current_custody_20260825.v1.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
EXPECTED = {
    "conversations-048.json": (36771626, 100, 6543, "ed19ea07f8763a8a4d87204d80c817694ce4d6c339c71b1d2a1b955a8c125256"),
    "conversations-049.json": (47806754, 100, 7196, "608e45449809a47f5931f86328b96dab2b2b86a5abf21a8dfe1c7da6834a2f1a"),
    "conversations-050.json": (17115060, 54, 3647, "c5058bf25f682de12de68b54029d13b07e836cd519416752fbc5e4fa320b4979"),
}


def validate(path: Path = PATH) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["schema"] == "rafaelia.novoexport-raw048-050-current-custody/v1"
    assert data["state"] == "PARTIAL_EVIDENCED_CURRENT_CUSTODY_PID_SET_OPEN"
    assert data["claim_allowed"] is False
    assert data["append_only"] is True
    authority = data["authority"]
    assert authority["current_provider_locators_verified"] is True
    assert authority["current_provider_locators_persisted_publicly"] is False
    assert authority["raw_bytes_persisted_publicly"] is False
    assert authority["raw_ids_persisted_publicly"] is False

    objects = data["objects"]
    assert len(objects) == 3
    assert {obj["file"] for obj in objects} == set(EXPECTED)
    for obj in objects:
        size, conversations, messages, digest = EXPECTED[obj["file"]]
        assert obj["bytes"] == size
        assert obj["historical_root_conversations"] == conversations
        assert obj["historical_messages"] == messages
        assert obj["provider_locator_state"] == "VERIFIED_PRIVATE_NOT_PUBLISHED"
        assert obj["current_sha256"] == digest
        assert obj["historical_download_sha256"] == digest
        assert HEX64.fullmatch(digest)
        assert obj["exact_byte_identity"] is True
        assert obj["current_parse_binding"] == "EVIDENCED_BY_EXACT_BYTE_IDENTITY_TO_HISTORICAL_PARSE"
        assert obj["exact_pid_set"] == "TOKEN_VAZIO_PID_SET"

    remaining = set(data["gap_transition"]["remaining"])
    assert remaining == {"RAW048_EXACT_PID_SET", "RAW049_EXACT_PID_SET", "RAW050_EXACT_PID_SET"}
    serialized = path.read_text(encoding="utf-8")
    assert "drive.google.com" not in serialized
    assert "docs.google.com" not in serialized
    assert "provider_id" not in serialized
    return data


def main() -> int:
    validate()
    print("PASS: RAW048-050 current custody is byte-bound; PID sets remain fail-closed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
