#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_zipraf_corpus_u2 import validate

DATA = Path("data/control-plane/zipraf-corpus-u2.v1.json")


class ZiprafCorpusU2Test(unittest.TestCase):
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

    def test_fixture_cannot_be_external_corpus(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "fixture_is_external_independent_corpus", True
            )
        )

    def test_apk_extension_cannot_prove_validity(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "apk_extension_proves_apk_validity", True
            )
        )

    def test_markers_cannot_prove_signature(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "apk_markers_prove_signature", True
            )
        )

    def test_manifest_cannot_grant_execution(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "manifest_grants_execution", True
            )
        )

    def test_manifest_cannot_grant_dma(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "manifest_grants_dma", True
            )
        )

    def test_deflate_stored_digest_cannot_be_logical_digest(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "stored_deflate_digest_is_logical_digest", True
            )
        )

    def test_scanner_cannot_extract(self) -> None:
        self.assert_rejected(
            lambda d: d["harness"].__setitem__("extraction_performed", True)
        )

    def test_scanner_cannot_execute(self) -> None:
        self.assert_rejected(
            lambda d: d["harness"].__setitem__("execution_authorized", True)
        )

    def test_manifest_hash_cannot_change(self) -> None:
        self.assert_rejected(
            lambda d: d["harness"].__setitem__("manifest_sha256", "0" * 64)
        )

    def test_private_corpus_cannot_publish_by_default(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "private_corpus_may_be_published_by_default", True
            )
        )

    def test_external_corpus_stays_token_vazio(self) -> None:
        self.assert_rejected(
            lambda d: d["claims"].__setitem__(
                "real_external_zip_apk_corpus", "PROVED"
            )
        )

    def test_signed_apk_stays_token_vazio(self) -> None:
        self.assert_rejected(
            lambda d: d["claims"].__setitem__("signed_production_apk", "PROVED")
        )

    def test_producer_must_remain_stacked(self) -> None:
        self.assert_rejected(
            lambda d: d["producer"].__setitem__("base_branch", "master")
        )


if __name__ == "__main__":
    unittest.main()
