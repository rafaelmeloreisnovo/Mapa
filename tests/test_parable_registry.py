import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ParableRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(
            (ROOT / "data/parables/traditional-parable-mechanisms.v1.json")
            .read_text(encoding="utf-8")
        )
        cls.records = []
        for relative_path in cls.manifest["shards"]:
            shard = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
            cls.records.extend(shard["records"])

    def test_registry_contains_exactly_42_unique_records(self):
        self.assertEqual(42, self.manifest["count"])
        self.assertEqual(42, len(self.records))
        ids = [record["id"] for record in self.records]
        self.assertEqual(42, len(set(ids)))
        self.assertEqual(
            [f"PAR-{number:03d}" for number in range(1, 43)],
            ids,
        )

    def test_no_reference_is_silently_marked_verified(self):
        forbidden = {"CANONICAL_REFERENCE", "VERIFIED_PRIMARY_SOURCE"}
        self.assertFalse(
            any(record["source_state"] in forbidden for record in self.records)
        )

    def test_source_required_records_keep_token_vazio(self):
        pending = [
            record for record in self.records
            if record["source_state"] == "SOURCE_REQUIRED"
        ]
        self.assertGreater(len(pending), 0)
        for record in pending:
            self.assertIn("TOKEN_VAZIO", record["source_reference"])

    def test_authorial_material_is_not_relabelled_traditional(self):
        authorial = [
            record for record in self.records
            if record["tradition_scope"] == "rafaelia_authorial"
        ]
        self.assertGreaterEqual(len(authorial), 7)
        for record in authorial:
            self.assertIn(record["source_state"], {"USER_AUTHORED", "USER_SYNTHESIS"})

    def test_policy_blocks_automatic_tradition_attribution(self):
        self.assertFalse(self.manifest["automatic_tradition_attribution"])
        self.assertFalse(self.manifest["claim_allowed"])
        self.assertTrue(self.manifest["policy"]["named_tradition_requires_source"])
        self.assertTrue(
            self.manifest["policy"]["contested_attribution_must_remain_contested"]
        )


if __name__ == "__main__":
    unittest.main()
