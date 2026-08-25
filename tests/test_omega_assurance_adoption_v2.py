#!/usr/bin/env python3

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_omega_assurance_adoption_v2.py"
SPEC = importlib.util.spec_from_file_location("omega_adoption_validator", VALIDATOR)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MOD)


class OmegaAssuranceAdoptionV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(
            (ROOT / "data" / "control-plane" / "omega-assurance-adoption.v2.json").read_text(encoding="utf-8")
        )
        cls.events, cls.parse_errors = MOD.load_ledger()
        cls.receipt = json.loads(
            (ROOT / "data" / "receipts" / "OMEGA_ASSURANCE_ADOPTION_V2_20260824.v1.json").read_text(
                encoding="utf-8"
            )
        )

    def errors(self, data):
        return MOD.validate_manifest(data)

    def test_real_manifest_and_ledger_pass(self):
        self.assertEqual(self.errors(self.manifest), [])
        self.assertEqual(self.parse_errors, [])
        self.assertEqual(MOD.validate_ledger(self.events), [])
        self.assertEqual(MOD.validate_receipt(self.receipt, self.manifest), [])

    def test_claim_promotion_fails(self):
        data = copy.deepcopy(self.manifest)
        data["claim_allowed"] = True
        self.assertTrue(any("claim_allowed" in e for e in self.errors(data)))

    def test_missing_axis_fails(self):
        data = copy.deepcopy(self.manifest)
        data["omega7_axes"] = data["omega7_axes"][:-1]
        self.assertTrue(any("omega7_axes" in e for e in self.errors(data)))

    def test_p0_compensation_fails(self):
        data = copy.deepcopy(self.manifest)
        data["risk_vector"]["compensation_allowed"] = True
        self.assertTrue(any("non-compensatory" in e for e in self.errors(data)))

    def test_meta_watch_depth_is_bounded(self):
        data = copy.deepcopy(self.manifest)
        data["quiet_watchdog"]["meta_watch_depth"] = 3
        self.assertTrue(any("meta_watch_depth" in e for e in self.errors(data)))

    def test_crossfail_cannot_manufacture_pass(self):
        data = copy.deepcopy(self.manifest)
        data["crossfail_cases"][0]["expected"] = "PASS"
        self.assertTrue(any("manufacture PASS" in e for e in self.errors(data)))

    def test_crossfail_seed_cannot_claim_execution(self):
        data = copy.deepcopy(self.manifest)
        data["crossfail_cases"][0]["execution_state"] = "EXECUTED_PASS"
        self.assertTrue(any("SPECIFIED_NOT_EXECUTED" in e for e in self.errors(data)))

    def test_unknown_producer_cannot_claim_execution(self):
        data = copy.deepcopy(self.manifest)
        for track in data["producer_tracks"]:
            if track["authority"] == "TOKEN_VAZIO_PRODUCER":
                track["state"] = "EXECUTED_EVIDENCED"
                break
        self.assertTrue(any("unresolved authority" in e for e in self.errors(data)))

    def test_secondary_source_fails(self):
        data = copy.deepcopy(self.manifest)
        data["primary_sources"][0]["source_kind"] = "SECONDARY_SUMMARY"
        self.assertTrue(any("official or primary" in e for e in self.errors(data)))

    def test_non_https_source_fails(self):
        data = copy.deepcopy(self.manifest)
        data["primary_sources"][0]["url"] = "http://example.invalid/spec"
        self.assertTrue(any("must be HTTPS" in e for e in self.errors(data)))

    def test_private_drive_locator_fails(self):
        data = copy.deepcopy(self.manifest)
        data["session_surface"]["drive_matrix_ref"] = "drive:1THISISAPRIVATELOCATOR12345"
        self.assertTrue(any("private Drive-style locator" in e for e in self.errors(data)))

    def test_pet_cannot_gain_authority(self):
        data = copy.deepcopy(self.manifest)
        data["session_surface"]["pet"]["authority"] = "PROMOTE"
        self.assertTrue(any("mascot" in e for e in self.errors(data)))

    def test_broken_ledger_chain_fails(self):
        events = copy.deepcopy(self.events)
        events[1]["prior_event_id"] = "OAE-UNKNOWN"
        self.assertTrue(any("prior_event_id" in e for e in MOD.validate_ledger(events)))

    def test_receipt_cannot_hide_governance_failure(self):
        receipt = copy.deepcopy(self.receipt)
        receipt["independent_governance"]["promotion_control"]["conclusion"] = "success"
        self.assertTrue(any("promotion control" in e for e in MOD.validate_receipt(receipt, self.manifest)))

    def test_receipt_cannot_hide_server_enforcement_gap(self):
        receipt = copy.deepcopy(self.receipt)
        receipt["independent_governance"]["server_merge_enforcement"]["failure_modes"] = []
        self.assertTrue(any("failure modes" in e for e in MOD.validate_receipt(receipt, self.manifest)))


if __name__ == "__main__":
    unittest.main()
