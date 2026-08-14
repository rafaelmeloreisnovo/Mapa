#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path

from tools.ingest_vectra_benchmark_v1 import load_binding, make_obs, parse_formatted

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "data" / "benchmarks" / "vectra-79-metric-binding.v2.json"


class VectraIngestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bindings, cls.producer = load_binding(BINDING)

    def test_binding_is_complete_0_to_78(self):
        self.assertEqual(sorted(self.bindings), list(range(79)))

    def test_iops_semantics_survive_generic_formatter(self):
        run = {"timestamp_ms": 123, "cpu_model": "test", "cpu_arch": "armv7l", "cpu_cores": 8,
               "ram_bytes": 1024, "seed": 1, "warmup": 7, "samples": 21,
               "min_test_duration_ns": 500000000}
        metric = {"metric_id": 47, "raw_ns": 1000, "formatted": "1.50 Mops/s", "unit": "IOPS"}
        obs = make_obs(metric, self.bindings[47], self.producer, run, "fixture.jsonl")
        self.assertEqual(obs["normalization"]["canonical_unit"], "IOPS")
        self.assertEqual(obs["normalization"]["canonical_value"], 1_500_000.0)
        self.assertIn("TOKEN_VAZIO_UNIT_CONFLICT_REVIEW", obs["token_vazio"])
        self.assertFalse(obs["claim_allowed"])

    def test_proxy_flags_are_preserved(self):
        run = {"timestamp_ms": 124}
        metric = {"metric_id": 76, "raw_ns": 1000, "formatted": "1.0 μs/op", "unit": "μs"}
        obs = make_obs(metric, self.bindings[76], self.producer, run, "fixture.jsonl")
        self.assertIn("SIMULATION_PROXY_THREAD_YIELD_NOT_HARDWARE_IRQ", obs["config"]["binding_flags"])
        self.assertFalse(obs["claim_allowed"])

    def test_formatted_parser_rejects_non_numeric(self):
        with self.assertRaises(ValueError):
            parse_formatted("N/A")


if __name__ == "__main__":
    unittest.main()
