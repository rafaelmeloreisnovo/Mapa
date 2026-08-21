import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "shared_data_validator", ROOT / "tools" / "validate_shared_data_release.py"
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

ALLOWED = json.loads(
    (ROOT / "examples" / "shared_data" / "manifest.synthetic.allowed.v1.json").read_text(encoding="utf-8")
)
BLOCKED = json.loads(
    (ROOT / "examples" / "shared_data" / "manifest.synthetic.blocked.v1.json").read_text(encoding="utf-8")
)


class SharedDataReleaseTests(unittest.TestCase):
    def test_synthetic_allowed_passes(self):
        self.assertEqual(validator.validate_manifest(ALLOWED), [])

    def test_restricted_token_vazio_blocks(self):
        errors = validator.validate_manifest(BLOCKED)
        self.assertIn("C2plus_redaction_required", errors)
        self.assertIn("C2plus_reidentification_TOKEN_VAZIO", errors)
        self.assertIn("C2plus_semantic_TOKEN_VAZIO", errors)
        self.assertIn("human_approval_required", errors)
        self.assertIn("approval_not_releaseable", errors)

    def test_c4_never_raw_automated(self):
        manifest = dict(ALLOWED)
        manifest["source_criticality"] = "C4_CRITICAL"
        manifest["human_approval"] = True
        self.assertIn("C4_raw_automation_prohibited", validator.validate_manifest(manifest))

    def test_secret_or_credential_detection_blocks(self):
        manifest = dict(ALLOWED)
        manifest["credential_or_secret_presence"] = True
        self.assertIn("credential_or_secret_presence", validator.validate_manifest(manifest))

    def test_claim_promotion_is_forbidden(self):
        manifest = dict(ALLOWED)
        manifest["claim_allowed"] = True
        self.assertIn("claim_allowed_must_be_false", validator.validate_manifest(manifest))

    def test_revoked_release_blocks(self):
        manifest = dict(ALLOWED)
        manifest["revoked"] = True
        manifest["approval_state"] = "REVOKED"
        errors = validator.validate_manifest(manifest)
        self.assertIn("revoked", errors)
        self.assertIn("approval_not_releaseable", errors)

    def test_unknown_field_fails_closed(self):
        manifest = dict(ALLOWED)
        manifest["surprise_field"] = "not allowed"
        self.assertTrue(any(e.startswith("additional_properties:") for e in validator.validate_manifest(manifest)))


if __name__ == "__main__":
    unittest.main()
