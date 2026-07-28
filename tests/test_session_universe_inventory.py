#!/usr/bin/env python3
"""Testes stdlib-only para o inventário da sessão."""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_session_universe_inventory.py"
INVENTORY_PATH = ROOT / "data" / "sementeira" / "inventories" / "session-universe-456.v1.json"

spec = importlib.util.spec_from_file_location("session_inventory_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class SessionUniverseInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))

    def test_baseline_passes(self) -> None:
        checks = validator.validate(copy.deepcopy(self.data))
        self.assertEqual(len(checks), 8)

    def test_all_416_atom_ids_are_contiguous(self) -> None:
        ids = [item["id"] for item in self.data["atomic_entities"]]
        self.assertEqual(ids[0], "ATOM-001")
        self.assertEqual(ids[-1], "ATOM-416")
        self.assertEqual(len(set(ids)), 416)

    def test_missing_atom_names_are_not_invented(self) -> None:
        self.assertTrue(all(item["name"] is None for item in self.data["atomic_entities"]))

    def test_alleged_closures_remain_blocked(self) -> None:
        for result in self.data["results"][:8]:
            self.assertFalse(result["claim_allowed"])
            self.assertEqual(result["state"], "TOKEN_VAZIO_FORMAL_PROOF")

    def test_sixteen_roadmaps_remain_itemization_vacancies(self) -> None:
        roadmaps = self.data["results"][8:]
        self.assertEqual(len(roadmaps), 16)
        self.assertTrue(all(item["name"] is None for item in roadmaps))
        self.assertTrue(all(item["state"] == "TOKEN_VAZIO_MISSING_ITEMIZATION" for item in roadmaps))

    def test_456_versus_457_convention_is_explicit(self) -> None:
        counts = self.data["declared_counts"]
        self.assertEqual(counts["grand_total_excluding_meta"], 456)
        self.assertEqual(counts["grand_total_including_meta"], 457)
        self.assertEqual(self.data["counting_convention"]["state"], "TOKEN_VAZIO_COUNTING_CONVENTION")

    def test_pairwise_and_powerset_are_exact(self) -> None:
        combinatorics = self.data["combinatorics"]
        self.assertEqual(combinatorics["pairwise_combinations"], 86320)
        self.assertEqual(int(combinatorics["powerset_exact"]), 2**416)

    def test_fail_closed_catches_promoted_closure(self) -> None:
        corrupted = copy.deepcopy(self.data)
        corrupted["results"][0]["claim_allowed"] = True
        with self.assertRaises(ValueError):
            validator.validate(corrupted)


if __name__ == "__main__":
    unittest.main()
