import json
import math
import unittest
from pathlib import Path

from scripts.semantic_tensor_parable_engine import (
    SemanticTensorError,
    analyze_record,
    build_receipt,
    normalized_entropy,
    tokenize,
    validate_control,
)

ROOT = Path(__file__).resolve().parents[1]


class SemanticTensorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.control = json.loads(
            (ROOT / "data/control-plane/rafaelia-semantic-tensor.v1.json")
            .read_text(encoding="utf-8")
        )
        cls.records = json.loads(
            (ROOT / "tests/fixtures/semantic_tensor_inputs.json")
            .read_text(encoding="utf-8")
        )

    def test_control_weights_and_model_boundary(self):
        validate_control(self.control)
        total = sum(item["weight"] for item in self.control["tensor_dimensions"])
        self.assertTrue(math.isclose(total, 1.0))
        self.assertFalse(self.control["model_boundary"]["changes_model_weights"])
        self.assertFalse(self.control["model_boundary"]["changes_tokenizer"])
        self.assertFalse(self.control["model_boundary"]["changes_training_data"])

    def test_tokenization_is_deterministic(self):
        text = "Entropia → coerência; TOKEN_VAZIO."
        self.assertEqual(tokenize(text), tokenize(text))
        self.assertIn("entropia", tokenize(text))
        self.assertIn("coerência", tokenize(text))

    def test_entropy_is_bounded(self):
        self.assertEqual(0.0, normalized_entropy([]))
        self.assertEqual(0.0, normalized_entropy(["um"]))
        value = normalized_entropy(["a", "b", "a", "c"])
        self.assertGreaterEqual(value, 0.0)
        self.assertLessEqual(value, 1.0)

    def test_unsupported_scientific_claim_fails_closed(self):
        result = analyze_record(self.control, self.records[1])
        self.assertEqual("BLOCKED_TOKEN_VAZIO", result["decision"])
        self.assertGreater(result["contradiction_penalty"], 0.0)

    def test_authorial_parable_is_not_promoted_as_fact(self):
        result = analyze_record(self.control, self.records[0])
        self.assertEqual("PARABLE_ANALOGY_NO_FACT_PROMOTION", result["decision"])
        self.assertFalse(result["unsupported_cultural_attribution"])

    def test_unsourced_named_tradition_is_blocked(self):
        result = analyze_record(self.control, self.records[3])
        self.assertEqual(
            "BLOCKED_UNSOURCED_CULTURAL_ATTRIBUTION",
            result["decision"],
        )

    def test_spiritual_confession_is_preserved_without_domain_claim(self):
        result = analyze_record(self.control, self.records[4])
        self.assertEqual(
            "PRESERVED_AS_CONFESSION_NOT_DOMAIN_CLAIM",
            result["decision"],
        )

    def test_verified_technical_record_reaches_human_review(self):
        result = analyze_record(self.control, self.records[2])
        self.assertEqual("READY_FOR_HUMAN_REVIEW", result["decision"])
        self.assertGreaterEqual(result["quality_score"], 0.72)

    def test_receipt_never_promotes_claim_automatically(self):
        receipt = build_receipt(self.control, self.records)
        self.assertFalse(receipt["model_mutation"])
        self.assertFalse(receipt["claim_allowed"])
        self.assertFalse(receipt["automatic_promotion"])
        self.assertEqual(len(self.records), receipt["record_count"])

    def test_invalid_weight_sum_is_rejected(self):
        broken = json.loads(json.dumps(self.control))
        broken["tensor_dimensions"][0]["weight"] = 0.99
        with self.assertRaises(SemanticTensorError):
            validate_control(broken)


if __name__ == "__main__":
    unittest.main()
