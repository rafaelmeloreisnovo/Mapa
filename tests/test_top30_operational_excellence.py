from __future__ import annotations

import importlib.util
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_top30_operational_excellence.py"
spec = importlib.util.spec_from_file_location("top30", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class Top30OperationalExcellenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.path = ROOT / "data" / "control-plane" / "RAFAELIA_TOP30_OPERATIONAL_EXCELLENCE.v1.json"
        self.registry = module.load_object(self.path)

    def test_registry_has_exact_ranked_thirty(self) -> None:
        module.validate(self.registry)
        self.assertEqual([item["rank"] for item in self.registry["practices"]], list(range(1, 31)))
        self.assertEqual(len({item["id"] for item in self.registry["practices"]}), 30)

    def test_fail_closed_boundaries(self) -> None:
        self.assertFalse(self.registry["claim_allowed"])
        self.assertFalse(self.registry["automatic_mutation"])
        self.assertFalse(self.registry["automatic_merge"])
        self.assertEqual(self.registry["source_mode"], "READ_ONLY")

    def test_value_scores_are_non_increasing(self) -> None:
        values = [item["value_score"] for item in self.registry["practices"]]
        self.assertEqual(values, sorted(values, reverse=True))

    def test_unresolved_items_have_falsifier_and_next_step(self) -> None:
        for item in self.registry["practices"]:
            if item["state"] != "EVIDENCED":
                self.assertTrue(item["falsifier"])
                self.assertTrue(item["next_step"])

    def test_evaluation_is_hash_bound_and_read_only(self) -> None:
        receipt = module.evaluate(self.registry, datetime(2026, 8, 1, 18, 57, tzinfo=timezone.utc))
        self.assertEqual(receipt["decision"], "EXECUTED_READ_ONLY")
        self.assertFalse(receipt["claim_allowed"])
        self.assertEqual(receipt["summary"]["practice_count"], 30)
        stored = json.loads(json.dumps(receipt))
        digest = stored.pop("receipt_sha256")
        self.assertEqual(digest, module.sha256_value(stored))

    def test_priority_prefers_high_value_open_control(self) -> None:
        receipt = module.evaluate(self.registry, datetime.now(timezone.utc))
        first = receipt["summary"]["top10_open_actions"][0]
        self.assertEqual(first["id"], "REPRODUCIBLE_BUILD_AND_RUNTIME")
        self.assertIn(first["state"], {"TOKEN_VAZIO", "PARTIAL", "BLOCKED_EXTERNAL"})

    def test_claim_promotion_is_rejected(self) -> None:
        broken = json.loads(json.dumps(self.registry))
        broken["claim_allowed"] = True
        with self.assertRaises(module.RegistryError):
            module.validate(broken)

    def test_missing_practice_is_rejected(self) -> None:
        broken = json.loads(json.dumps(self.registry))
        broken["practices"].pop()
        with self.assertRaises(module.RegistryError):
            module.validate(broken)

    def test_invalid_rank_order_is_rejected(self) -> None:
        broken = json.loads(json.dumps(self.registry))
        broken["practices"][0]["rank"] = 2
        with self.assertRaises(module.RegistryError):
            module.validate(broken)


if __name__ == "__main__":
    unittest.main()
