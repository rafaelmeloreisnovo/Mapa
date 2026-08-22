import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_invariant_of_invariants_omega.py"
ARCHITECTURE = ROOT / "data" / "control-plane" / "invariant-of-invariants-omega.v1.json"


class TestInvariantOfInvariantsOmega(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canonical = json.loads(ARCHITECTURE.read_text(encoding="utf-8"))

    def run_case(self, data):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "architecture.json"
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_canonical_architecture(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(ARCHITECTURE)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["state"], "PASS_LOCAL_LIMITED")
        self.assertGreaterEqual(receipt["topologies"], 30)
        self.assertGreaterEqual(receipt["methodologies"], 56)

    def test_reject_claim_promotion(self):
        data = copy.deepcopy(self.canonical)
        data["claim_allowed"] = True
        self.assertNotEqual(self.run_case(data).returncode, 0)

    def test_reject_dangling_relation(self):
        data = copy.deepcopy(self.canonical)
        data["relations"][0]["to"] = "S-MISSING"
        self.assertNotEqual(self.run_case(data).returncode, 0)

    def test_reject_evidence_without_receipt(self):
        data = copy.deepcopy(self.canonical)
        relation = next(
            item for item in data["relations"] if item["evidence_state"] == "EVIDENCIADO"
        )
        relation["receipt_locator"] = None
        self.assertNotEqual(self.run_case(data).returncode, 0)

    def test_reject_symbol_as_evidence(self):
        data = copy.deepcopy(self.canonical)
        data["symbols"][0]["evidence_weight"] = 1
        self.assertNotEqual(self.run_case(data).returncode, 0)

    def test_reject_insufficient_topologies(self):
        data = copy.deepcopy(self.canonical)
        data["topologies"] = data["topologies"][:29]
        self.assertNotEqual(self.run_case(data).returncode, 0)

    def test_reject_insufficient_methodologies(self):
        data = copy.deepcopy(self.canonical)
        data["methodologies"] = data["methodologies"][:55]
        self.assertNotEqual(self.run_case(data).returncode, 0)

    def test_reject_timestamp_only_freshness(self):
        data = copy.deepcopy(self.canonical)
        data["freshness_contract"]["timestamp_only_forbidden"] = False
        self.assertNotEqual(self.run_case(data).returncode, 0)

    def test_reject_unbounded_query(self):
        data = copy.deepcopy(self.canonical)
        data["query_contract"]["max_limit"] = 1001
        self.assertNotEqual(self.run_case(data).returncode, 0)

    def test_reject_confounded_throughput_claim(self):
        data = copy.deepcopy(self.canonical)
        data["latency_receipts"][0]["throughput"] = 1000
        self.assertNotEqual(self.run_case(data).returncode, 0)

    def test_reject_gap_promotion(self):
        data = copy.deepcopy(self.canonical)
        data["gaps"][0]["state"] = "VERIFIED"
        self.assertNotEqual(self.run_case(data).returncode, 0)


if __name__ == "__main__":
    unittest.main()
