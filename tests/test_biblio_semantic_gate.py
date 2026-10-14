"""Independent source-side falsifiers for semantic boundaries and arithmetic."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_biblio_semantics_v1 import analyze, arithmetic, dictionary_rows

DATA = json.loads(
    (ROOT / "data/biblioteconomia/federated_biblio_contract.v1.json")
    .read_text(encoding="utf-8")
)
ROWS = dictionary_rows(
    (ROOT / "data/semantics/semantic-dictionary.v1.jsonl")
    .read_text(encoding="utf-8")
)


class TestSevenDirections(unittest.TestCase):
    def test_current_cross_source_semantics_scoped(self):
        result = analyze(DATA, ROWS)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["offline_checks"], "PASS_SCOPED")
        self.assertIs(result["claim_allowed"], False)
        self.assertEqual(result["seven_directions"]["semantic_scope"], "HOLD_TYPED_CONTEXT_REQUIRED")
        self.assertEqual(result["seven_directions"]["android_arm32"], "TOKEN_VAZIO_PHYSICAL_RECEIPT")

    def test_integer_arithmetic_exact_no_eval(self):
        self.assertEqual(arithmetic("70*7"), 490)
        self.assertEqual(arithmetic("21*2"), 42)
        self.assertEqual(arithmetic("10*10*10"), 1000)
        self.assertEqual(arithmetic("10+8+2"), 20)
        self.assertEqual((1000 - 1).bit_length(), 10)
        with self.assertRaises(ValueError):
            arithmetic("__import__('os').system('false')")

    def test_missing_empty_set_scope_is_detected(self):
        mutated = copy.deepcopy(DATA)
        mutated["semantic_scope_collisions"] = [
            r for r in mutated["semantic_scope_collisions"] if r["literal_utf8"] != "∅"
        ]
        self.assertIn("EMPTY_SET_EPISTEMIC_COLLISION_UNBOUND", analyze(mutated, ROWS)["errors"])

    def test_dont_silently_alias_delta(self):
        mutated = copy.deepcopy(DATA)
        next(
            r for r in mutated["semantic_scope_collisions"] if r["literal_utf8"] == "∆"
        )["do_not_normalize_without_evidence"] = False
        self.assertIn("DELTA_ALIAS_UNBOUND", analyze(mutated, ROWS)["errors"])

    def test_existing_dictionary_source_mutation_is_detected(self):
        rows = copy.deepcopy(ROWS)
        next(r for r in rows if r["entry_id"] == "SEM-EMPTY-001")["aliases"] = []
        self.assertIn("EMPTY_SET_EPISTEMIC_COLLISION_UNBOUND", analyze(DATA, rows)["errors"])

    def test_math_false_claim_fails(self):
        mutated = copy.deepcopy(DATA)
        next(r for r in mutated["mathematical_checks"] if r["literal"] == "70*7=14")["expect"] = "TRUE"
        self.assertIn("MATH_FALSE_UNTYPED:70*7=14", analyze(mutated, ROWS)["errors"])

    def test_privacy_secrets_fields_fail(self):
        mutated = copy.deepcopy(DATA)
        mutated["providers"][0]["oauth_token"] = "synthetic-fixture-not-a-real-credential"
        self.assertIn("PRIVATE_LOCATOR_OR_SECRET_KEY:oauth_token", analyze(mutated, ROWS)["errors"])

    def test_promotion_and_raw_corpus_fail(self):
        mutated = copy.deepcopy(DATA)
        mutated["publishing_policy"]["raw_conversations"] = True
        mutated["promotion"]["auto_merge"] = True
        errs = analyze(mutated, ROWS)["errors"]
        self.assertIn("AUTO_MERGE_UNSAFE", errs)
        self.assertIn("RAW_CONVERSATION_PUBLICATION_UNSAFE", errs)

    def test_no_duplicate_lexical_surface(self):
        mutated = copy.deepcopy(DATA)
        mutated["lexical_types"].append(copy.deepcopy(mutated["lexical_types"][0]))
        self.assertIn("DUPLICATE_LITERAL:§", analyze(mutated, ROWS)["errors"])

    def test_missing_source_predecessor_fails(self):
        mutated = copy.deepcopy(DATA)
        mutated["predecessor"] = "TOKEN_VAZIO"
        self.assertIn("PREDECESSOR_IDENTITY_CHANGED", analyze(mutated, ROWS)["errors"])


if __name__ == "__main__":
    unittest.main()
