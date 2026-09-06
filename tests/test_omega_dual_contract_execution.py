from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data/governance/OMEGA_DUAL_CONTRACT_EXECUTION_20260906.v1.json"
VALIDATOR = ROOT / "tools/validate_omega_dual_contract_execution.py"

spec = importlib.util.spec_from_file_location("omega_dual_contract_validator", VALIDATOR)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class OmegaDualContractExecutionTests(unittest.TestCase):
    def load(self) -> dict:
        return json.loads(RECORD.read_text(encoding="utf-8"))

    def validate_candidate(self, candidate: dict) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            return module.validate(path)

    def test_record_passes_fail_closed_validation(self) -> None:
        result = module.validate(RECORD)
        self.assertEqual(result["state"], "PASS")
        self.assertEqual(result["nodes"], 11)
        self.assertEqual(result["edges"], 13)
        self.assertEqual(result["isolated_nodes"], [])

    def test_claim_cannot_be_promoted(self) -> None:
        candidate = self.load()
        candidate["claim_allowed"] = True
        result = self.validate_candidate(candidate)
        self.assertEqual(result["state"], "FAIL")
        self.assertIn("claim_allowed must remain false", result["errors"])

    def test_graph_cannot_reference_missing_node(self) -> None:
        candidate = self.load()
        candidate["graph"]["edges"][0]["target"] = "MISSING:NODE"
        result = self.validate_candidate(candidate)
        self.assertEqual(result["state"], "FAIL")
        self.assertTrue(any("undefined endpoint" in error for error in result["errors"]))

    def test_branch_write_is_not_merge(self) -> None:
        data = self.load()
        self.assertFalse(data["automatic_merge"])
        self.assertEqual(data["publication_effect"], "NONE")
        self.assertIn("branch write != merge != main", data["boundaries"])


if __name__ == "__main__":
    unittest.main()
