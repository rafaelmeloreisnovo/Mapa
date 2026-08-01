#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_zipraf_payload_digest_u1 import validate

DATA = Path("data/control-plane/zipraf-payload-digest-u1.v1.json")


class ZiprafPayloadDigestU1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads(DATA.read_text(encoding="utf-8"))

    def assert_rejected(self, mutate) -> None:
        candidate = copy.deepcopy(self.base)
        mutate(candidate)
        with self.assertRaises(ValueError):
            validate(candidate)

    def test_canonical_passes(self) -> None:
        validate(copy.deepcopy(self.base))

    def test_provider_commit_cannot_drift(self) -> None:
        self.assert_rejected(
            lambda d: d["providers"]["blake3"].__setitem__("commit", "0" * 40)
        )

    def test_crc32_cannot_be_identity(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "crc32_is_cryptographic_identity", True
            )
        )

    def test_deflate_stored_digest_cannot_be_logical_digest(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "stored_digest_equals_deflate_logical_digest", True
            )
        )

    def test_digest_cannot_grant_execution(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "digest_grants_execution", True
            )
        )

    def test_digest_cannot_grant_dma(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "digest_grants_dma", True
            )
        )

    def test_digest_cannot_be_signature(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "digest_is_signature", True
            )
        )

    def test_digest_cannot_prove_authorship(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "digest_proves_authorship", True
            )
        )

    def test_receipt_hash_cannot_change(self) -> None:
        self.assert_rejected(
            lambda d: d["receipt"].__setitem__("sha256", "f" * 64)
        )

    def test_formula_logic_cannot_be_recorded_as_duplicated(self) -> None:
        self.assert_rejected(
            lambda d: d["formula_ci_repair"].__setitem__(
                "formula_logic_duplicated", True
            )
        )

    def test_formula_example_cannot_be_promoted_to_science(self) -> None:
        self.assert_rejected(
            lambda d: d["formula_ci_repair"].__setitem__(
                "scientific_claim", True
            )
        )

    def test_android_runtime_stays_token_vazio(self) -> None:
        self.assert_rejected(
            lambda d: d["claims"].__setitem__("android_runtime", "PROVED")
        )

    def test_u2_stays_unproven(self) -> None:
        self.assert_rejected(
            lambda d: d["next_dependency"].__setitem__("state", "PASS")
        )


if __name__ == "__main__":
    unittest.main()
