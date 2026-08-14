#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "tools" / "validate_metric_observation_v1.py"
spec = importlib.util.spec_from_file_location("metric_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class MetricObservationV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.examples = json.loads((ROOT / "data" / "benchmarks" / "metric-observation-v1.examples.json").read_text(encoding="utf-8"))

    def test_examples_pass(self):
        for obj in self.examples:
            self.assertEqual([], validator.validate(obj), obj["observation_id"])

    def test_mb_and_mib_are_not_equal(self):
        mb = validator.expected_normalization(1.0, "MB/s")
        mib = validator.expected_normalization(1.0, "MiB/s")
        self.assertEqual(1_000_000.0, mb["canonical_value"])
        self.assertEqual(1_048_576.0, mib["canonical_value"])
        self.assertNotEqual(mb["canonical_value"], mib["canonical_value"])

    def test_iops_semantics_are_preserved(self):
        norm = validator.expected_normalization(4096, "IOPS")
        self.assertEqual("PRESERVED_SEMANTIC", norm["status"])
        self.assertEqual("IOPS", norm["canonical_unit"])
        self.assertEqual("io_operation_rate", norm["dimension"])

    def test_estimate_cannot_promote_claim(self):
        obj = dict(self.examples[0])
        obj["epistemic_class"] = "ESTIMATE_CODE_ANALYSIS"
        obj["value_state"] = "ESTIMATE"
        obj["claim_allowed"] = True
        errors = validator.validate(obj)
        self.assertTrue(any("fail-closed" in e for e in errors))

    def test_token_vazio_cannot_have_numeric_value(self):
        obj = json.loads(json.dumps(self.examples[2]))
        obj["observed_value"] = 123
        errors = validator.validate(obj)
        self.assertTrue(any("observed_value=null" in e for e in errors))

    def test_measured_requires_evidence_environment_workload(self):
        obj = json.loads(json.dumps(self.examples[0]))
        obj["evidence"] = {"artifact_sha256": None, "receipt_refs": [], "raw_result_refs": [], "digest_verified": None}
        obj["environment"] = {}
        obj["workload"] = {}
        errors = validator.validate(obj)
        self.assertTrue(any("requires artifact hash" in e for e in errors))
        self.assertTrue(any("requires non-empty environment" in e for e in errors))
        self.assertTrue(any("requires non-empty workload" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
