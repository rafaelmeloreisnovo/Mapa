"""Synthetic negative tests for RAFAELIA lexical witnesses; no personal corpus."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_typed_void_lexemes import classify, validate

DATA = json.loads((ROOT / "data/semantics/typed-void-lexical-fixtures.v1.json").read_text(encoding="utf-8"))


class LexemeTests(unittest.TestCase):
    def test_complete_contract(self):
        self.assertEqual(validate(DATA), [])

    def test_glyph_requires_set_context(self):
        a = classify({"raw": "∅", "syntax": "set_theory", "domain": "set"})
        b = classify({"raw": "∅", "syntax": "free_text", "domain": "unbound"})
        self.assertEqual(a["kind"], "EMPTY_SET")
        self.assertEqual(b["kind"], "TOKEN_VAZIO")
        self.assertEqual(a["codepoints"], b["codepoints"])

    def test_empty_value_versus_quotes(self):
        a = classify({"raw": "", "syntax": "observed_string", "domain": "text"})
        b = classify({"raw": '""', "syntax": "json_string", "domain": "text"})
        self.assertEqual((a["kind"], b["kind"]), ("EMPTY_STRING", "EMPTY_STRING"))
        self.assertNotEqual(a["codepoints"], b["codepoints"])

    def test_quoted_quotes_are_nonempty(self):
        a = classify({"raw": "'\"\"'", "syntax": "python_string", "domain": "text"})
        self.assertEqual((a["kind"], a["parsed_length"], a["parsed_value"]), ("PRESENT", 2, '""'))

    def test_space_is_not_empty(self):
        for raw, syntax in [("' '", "python_string"), ('" "', "json_string")]:
            with self.subTest(raw=raw):
                a = classify({"raw": raw, "syntax": syntax, "domain": "text"})
                self.assertEqual((a["kind"], a["parsed_length"]), ("PRESENT", 1))

    def test_double_delimiter_is_not_missing_object_key(self):
        a = classify({"raw": "a;;b", "syntax": "semicolon_fields", "domain": "delimited_text"})
        b = classify({"syntax": "object_key", "domain": "object"})
        self.assertEqual(a["parsed_value"], ["a", "", "b"])
        self.assertEqual(a["kind"], "PRESENT")
        self.assertEqual(b["kind"], "MISSING_FIELD")

    def test_missing_and_explicit_null_differ(self):
        a = classify({"syntax": "object_key", "domain": "object"})
        b = classify({"raw": "null", "syntax": "json_null", "domain": "json"})
        self.assertNotEqual(a["kind"], b["kind"])
        self.assertFalse(a["source_present"])
        self.assertTrue(b["source_present"])

    def test_unbound_null_is_not_json_null(self):
        self.assertEqual(classify({"raw": "Null", "syntax": "free_text", "domain": "unbound"})["kind"], "TOKEN_VAZIO")
        self.assertEqual(classify({"raw": "null", "syntax": "free_text", "domain": "unbound"})["kind"], "TOKEN_VAZIO")

    def test_zero_vs_superscript(self):
        zero = classify({"raw": "0", "syntax": "json_number", "domain": "number"})
        sup = classify({"raw": "⁰", "syntax": "symbolic", "domain": "symbolic"})
        self.assertEqual((zero["kind"], zero["parsed_value"]), ("NUMERIC_ZERO", 0))
        self.assertEqual(sup["kind"], "TOKEN_VAZIO")
        self.assertEqual(sup["codepoints"], ["U+2070"])
        self.assertNotEqual(zero["codepoints"], sup["codepoints"])

    def test_false_json_single_quotes(self):
        self.assertEqual(classify({"raw": "''", "syntax": "json_string", "domain": "text"})["kind"], "TOKEN_VAZIO")

    def test_unicode_normalization_not_applied(self):
        a = classify({"raw": "0", "syntax": "free_text", "domain": "unbound"})
        b = classify({"raw": "⁰", "syntax": "free_text", "domain": "unbound"})
        self.assertNotEqual(a["codepoints"], b["codepoints"])

    def test_duplicate_ids_fail(self):
        d = copy.deepcopy(DATA)
        d["cases"][1]["id"] = d["cases"][0]["id"]
        self.assertTrue(validate(d))

    def test_wrong_expected_kind_fails(self):
        d = copy.deepcopy(DATA)
        d["cases"][0]["expected_kind"] = "NUMERIC_ZERO"
        self.assertTrue(validate(d))

    def test_claim_promotion_fails(self):
        d = copy.deepcopy(DATA)
        d["claim_allowed"] = True
        self.assertIn("INVALID_FIXTURE_SCOPE_OR_CLAIM", validate(d))

    def test_missing_raw_is_not_empty_string(self):
        a = classify({"syntax": "object_key", "domain": "object"})
        b = classify({"raw": "", "syntax": "observed_string", "domain": "text"})
        self.assertEqual(a["kind"], "MISSING_FIELD")
        self.assertEqual(b["kind"], "EMPTY_STRING")


if __name__ == "__main__":
    unittest.main()
