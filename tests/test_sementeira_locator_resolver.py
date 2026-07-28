import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "sementeira_locator_resolver.py"
spec = importlib.util.spec_from_file_location("sementeira_locator_resolver", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def payload(locator, digest):
    return {
        "evidence": [{"id": "src", "kind": "SOURCE", "locator": locator, "sha256": digest}],
        "claims": [{"id": "c1", "evidence_refs": ["src"]}],
        "claim_allowed": False,
    }


class LocatorResolverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs").mkdir()
        self.file = self.root / "docs" / "source.txt"
        self.file.write_text("origem\nprova\n", encoding="utf-8")
        self.digest, _ = module.sha256_file(self.file)

    def tearDown(self):
        self.tmp.cleanup()

    def test_matching_hash_passes_identity_gate(self):
        receipt = module.resolve_payload(payload("docs/source.txt", self.digest), self.root)
        self.assertEqual(receipt["artifact_identity_gate"], "PASS")
        self.assertEqual(receipt["results"][0]["status"], module.MATCH)
        self.assertFalse(receipt["epistemic_promotion_allowed"])

    def test_repo_scheme_is_supported(self):
        receipt = module.resolve_payload(payload("repo://docs/source.txt", self.digest), self.root)
        self.assertEqual(receipt["results"][0]["status"], module.MATCH)

    def test_mismatch_blocks_referenced_evidence(self):
        receipt = module.resolve_payload(payload("docs/source.txt", "0" * 64), self.root)
        self.assertEqual(receipt["artifact_identity_gate"], "FAIL")
        self.assertEqual(receipt["results"][0]["status"], module.MISMATCH)

    def test_missing_file_remains_token_vazio(self):
        receipt = module.resolve_payload(payload("docs/missing.txt", self.digest), self.root)
        self.assertEqual(receipt["results"][0]["status"], module.UNRESOLVED)
        self.assertEqual(receipt["results"][0]["reason"], "FILE_NOT_FOUND")

    def test_path_traversal_is_blocked(self):
        receipt = module.resolve_payload(payload("../outside.txt", self.digest), self.root)
        self.assertEqual(receipt["results"][0]["status"], module.BLOCKED)
        self.assertEqual(receipt["results"][0]["reason"], "PATH_TRAVERSAL")

    def test_absolute_path_is_blocked(self):
        receipt = module.resolve_payload(payload(str(self.file.resolve()), self.digest), self.root)
        self.assertEqual(receipt["results"][0]["status"], module.BLOCKED)

    def test_network_scheme_is_unresolved_not_fetched(self):
        receipt = module.resolve_payload(payload("https://example.invalid/source", self.digest), self.root)
        self.assertEqual(receipt["results"][0]["status"], module.UNRESOLVED)
        self.assertEqual(receipt["results"][0]["reason"], "UNSUPPORTED_SCHEME")

    def test_invalid_expected_hash_is_blocked(self):
        receipt = module.resolve_payload(payload("docs/source.txt", "abc"), self.root)
        self.assertEqual(receipt["results"][0]["status"], module.BLOCKED)
        self.assertIn("INVALID_EXPECTED_SHA256", {x["code"] for x in receipt["blocking_findings"]})

    @unittest.skipIf(not hasattr(os, "symlink"), "symlink unavailable")
    def test_symlink_escape_is_blocked(self):
        outside = self.root.parent / f"outside-{self.root.name}.txt"
        outside.write_text("outside", encoding="utf-8")
        try:
            os.symlink(outside, self.root / "docs" / "escape.txt")
            digest, _ = module.sha256_file(outside)
            receipt = module.resolve_payload(payload("docs/escape.txt", digest), self.root)
            self.assertEqual(receipt["results"][0]["status"], module.BLOCKED)
            self.assertEqual(receipt["results"][0]["reason"], "SYMLINK_ESCAPE")
        finally:
            outside.unlink(missing_ok=True)

    def test_referenced_evidence_absent_is_blocked(self):
        data = {"evidence": [], "claims": [{"id": "c1", "evidence_refs": ["missing"]}]}
        receipt = module.resolve_payload(data, self.root)
        self.assertIn("REFERENCED_EVIDENCE_MISSING", {x["code"] for x in receipt["blocking_findings"]})

    def test_receipt_is_deterministic(self):
        data = payload("docs/source.txt", self.digest)
        first = module.resolve_payload(data, self.root)
        second = module.resolve_payload(data, self.root)
        self.assertEqual(first["receipt_sha256"], second["receipt_sha256"])

    def test_hash_identity_never_promotes_claim(self):
        receipt = module.resolve_payload(payload("docs/source.txt", self.digest), self.root)
        self.assertTrue(receipt["all_referenced_hashes_match"])
        self.assertFalse(receipt["claim_allowed"])
        self.assertFalse(receipt["epistemic_promotion_allowed"])


if __name__ == "__main__":
    unittest.main()
