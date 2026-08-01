#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_zipraf_content_page_graph import validate

FIXTURE = Path("data/control-plane/zipraf-content-page-graph.v1.json")


class ZiprafContentPageGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def rejects(self, mutate) -> None:
        data = copy.deepcopy(self.base)
        mutate(data)
        with self.assertRaises(ValueError):
            validate(data)

    def test_valid(self) -> None:
        validate(copy.deepcopy(self.base))

    def test_deflate_direct_map(self) -> None:
        self.rejects(lambda d: d["blocks"][1].update(direct_map_candidate=True))

    def test_magic_self_authorization(self) -> None:
        self.rejects(lambda d: d["blocks"][0].update(platform_loader_authorized=True))

    def test_45_percent_observe_only(self) -> None:
        self.rejects(lambda d: d["blocks"][0]["redundancy"].update(recovery_claim_ppm=450000))

    def test_hash_is_not_clock(self) -> None:
        self.rejects(lambda d: d["invariants"].update(hash_is_clock_measurement=True))

    def test_absolute_pointer_across_epoch(self) -> None:
        self.rejects(lambda d: d["invariants"].update(absolute_pointer_reuse_across_epoch=True))

    def test_write_conflict(self) -> None:
        def mutate(data) -> None:
            data["blocks"][1]["immutable"] = False
            data["edges"][2]["access"] = ["WRITE"]
            other = copy.deepcopy(data["edges"][2])
            other["module_id"] = "M-WRITER-2"
            other["core_mask"] = 8
            data["edges"].append(other)

        self.rejects(mutate)

    def test_irq_epoch_gate_required(self) -> None:
        self.rejects(lambda d: d["dma_irq_policy"].update(irq_accept_requires=["IN_FLIGHT"]))

    def test_blockchain_not_assumed(self) -> None:
        self.rejects(lambda d: d["ledger"].update(blockchain_consensus="PROVED"))

    def test_claim_allowed_stays_false(self) -> None:
        self.rejects(lambda d: d.update(claim_allowed=True))


if __name__ == "__main__":
    unittest.main()
