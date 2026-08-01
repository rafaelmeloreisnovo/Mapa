#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_zipraf_real_archive_binding import validate

DATA = Path("data/control-plane/zipraf-real-archive-binding.v2.json")


class ZiprafRealArchiveBindingTest(unittest.TestCase):
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

    def test_claim_allowed_cannot_promote(self) -> None:
        self.assert_rejected(lambda d: d.__setitem__("claim_allowed", True))

    def test_mmap_layout_cannot_grant_execution(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "layout_mappable_grants_execution", True
            )
        )

    def test_crc32_cannot_become_identity(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "crc32_is_content_identity", True
            )
        )

    def test_deflate_cannot_become_direct_map(self) -> None:
        self.assert_rejected(
            lambda d: d["promotion_invariants"].__setitem__(
                "deflate_is_direct_map", True
            )
        )

    def test_host_receipt_cannot_claim_kernel_zero_copy(self) -> None:
        self.assert_rejected(
            lambda d: d["mmap_receipt_contract"].__setitem__(
                "kernel_or_hardware_zero_copy_claim", True
            )
        )

    def test_android_mmap_stays_token_vazio(self) -> None:
        self.assert_rejected(
            lambda d: d["claims"].__setitem__("android_mmap", "PROVED")
        )

    def test_octa_core_stays_token_vazio(self) -> None:
        self.assert_rejected(
            lambda d: d["scheduling"].__setitem__("octa_core_runtime", "PROVED")
        )

    def test_bitraf_35_45_stays_not_authorized(self) -> None:
        self.assert_rejected(
            lambda d: d["claims"].__setitem__(
                "bitflip_35_45_recovery", "VERIFIED"
            )
        )

    def test_dma_stays_token_vazio(self) -> None:
        self.assert_rejected(
            lambda d: d["claims"].__setitem__(
                "dma_iommu_irq_hardware", "PROVED"
            )
        )

    def test_security_policy_cannot_weaken(self) -> None:
        self.assert_rejected(
            lambda d: d["security_policy"].__setitem__(
                "reject_parent_traversal", False
            )
        )

    def test_urgency_order_cannot_shuffle(self) -> None:
        def mutate(data):
            data["urgency"][0], data["urgency"][1] = (
                data["urgency"][1],
                data["urgency"][0],
            )
        self.assert_rejected(mutate)

    def test_open_pr_cannot_be_recorded_as_merged(self) -> None:
        self.assert_rejected(
            lambda d: d["producer"].__setitem__("merged", True)
        )


if __name__ == "__main__":
    unittest.main()
