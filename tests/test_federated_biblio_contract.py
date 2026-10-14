"""Source-bound regression checks for the public federated library contract.

Does not inspect Drive private corpus, OAuth, alphaXiv private notes, or physical APK.
"""
import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "biblioteconomia" / "federated_biblio_contract.v1.json"
REQUIRED_SURFACES = {"GITHUB_PUBLIC", "GITHUB_PRIVATE", "GOOGLE_DRIVE_PUBLIC", "GOOGLE_DRIVE_PRIVATE", "ALPHAXIV", "ANDROID_ARM32"}
PUBLIC_NO_PRIVATE_FIELDS = {"private_file_id", "private_folder_id", "oauth_token", "refresh_token", "raw_conversation", "conversation_id", "message_id"}


def inspect(data):
    errors = []
    if not isinstance(data, dict):
        return ["object required"]
    if data.get("claim_allowed") is not False or data.get("promotion", {}).get("auto_merge") is not False:
        errors.append("promotion not allowed")
    ps = data.get("providers")
    if not isinstance(ps, list):
        return errors + ["providers required"]
    ids = [p.get("surface") for p in ps if isinstance(p, dict)]
    if len(ids) != len(ps) or set(ids) != REQUIRED_SURFACES:
        errors.append("providers inconsistent")
    for p in ps:
        if not isinstance(p, dict):
            errors.append("provider object required")
            continue
        if p.get("surface") in {"GITHUB_PUBLIC", "GOOGLE_DRIVE_PUBLIC"} and p.get("private_payload_allowed") is not False:
            errors.append("public private-payload leak")
        if p.get("surface") == "GOOGLE_DRIVE_PRIVATE" and p.get("access") != "private":
            errors.append("Drive classification regression")
    literals = data.get("lexical_types")
    if not isinstance(literals, list):
        return errors + ["lexical types missing"]
    for t in literals:
        lit = t.get("literal_utf8")
        points = t.get("unicode_codepoints")
        if points is not None and points != ["U+%04X" % ord(ch) for ch in lit]:
            errors.append("unicode codepoint mismatch")
    ent = next((t for t in literals if t.get("literal_utf8") == "∅"), {})
    if "TOKEN_VAZIO" not in ent.get("not_equal_to", []):
        errors.append("empty set must not equal unknown")
    if "NO_RAW_PRIVATE_DATA_IN_PUBLIC_REPOSITORY" not in data.get("invariants", []):
        errors.append("public leakage invariant missing")
    checks = {c.get("literal"): c.get("expect") for c in data.get("mathematical_checks", [])}
    if checks.get("70*7=14") != "CONTRADICTION_490_NOT_14":
        errors.append("math contradiction incorrectly promoted")
    if checks.get("10+8+2=20") != "TRUE_ARITHMETIC_ONLY":
        errors.append("format hypothesis incorrectly promoted")
    def walk(obj):
        if isinstance(obj, dict):
            if PUBLIC_NO_PRIVATE_FIELDS & set(obj):
                errors.append("private locator in public record")
            for v in obj.values(): walk(v)
        elif isinstance(obj, list):
            for v in obj: walk(v)
    walk(data)
    return errors


class TestFederatedLibraryContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_positive_scoped_static_structure(self):
        self.assertEqual(inspect(self.data), [])

    def test_guard_against_promotion(self):
        d = copy.deepcopy(self.data); d["claim_allowed"] = True
        self.assertTrue(inspect(d))

    def test_guard_private_public_provider(self):
        d = copy.deepcopy(self.data)
        next(p for p in d["providers"] if p["surface"] == "GITHUB_PUBLIC")["private_payload_allowed"] = True
        self.assertTrue(inspect(d))

    def test_guard_unicode_wrong_codepoint(self):
        d = copy.deepcopy(self.data)
        next(t for t in d["lexical_types"] if t["literal_utf8"] == "∆")["unicode_codepoints"] = ["U+0394"]
        self.assertTrue(inspect(d))

    def test_guard_mathematical_inconsistency(self):
        d = copy.deepcopy(self.data)
        next(c for c in d["mathematical_checks"] if c["literal"] == "70*7=14")["expect"] = "TRUE"
        self.assertTrue(inspect(d))

    def test_guard_missing_provider(self):
        d = copy.deepcopy(self.data); d["providers"].pop()
        self.assertTrue(inspect(d))

    def test_guard_private_locator_field(self):
        d = copy.deepcopy(self.data); d["private_folder_id"] = "fake"
        self.assertTrue(inspect(d))


if __name__ == "__main__":
    unittest.main()
