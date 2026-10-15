"""Offline falsifiers for the mobile device reconstruction route.

Checks only the public routing manifest, never private Drive or device hardware.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data/devices/mobile_bitraf_w20_reconstruction_route.v1.json"
EXPECTED_DIRECTIONS = set("D1 D2 D3 D4 D5 D6 D7".split())
ACCEPTED_TYPES = {
    "PASS_SCOPED_SOURCE", "HOLD_TYPED", "PASS_SCOPED_PUBLIC_METADATA",
    "TOKEN_VAZIO_SOURCE_STALENESS", "PASS_SCOPED_EXHAUSTIVE_CI",
    "HOLD_NOT_ENFORCED", "TOKEN_VAZIO_PHYSICAL_RECEIPT",
}


def validate(x):
    errors = []
    if x.get("schema") != "rafaelia.device.mobile-bitraf-reconstruction-route/v1":
        errors.append("SCHEMA_MISMATCH")
    if x.get("claim_allowed") is not False or x.get("promotion") != "HOLD_NO_AUTOMERGE":
        errors.append("PROMOTION_CLAIM_UNSAFE")
    if not isinstance(x.get("rollback"), str) or "predecessor" not in x["rollback"]:
        errors.append("ROLLBACK_UNBOUND")
    dirs = x.get("seven_directions")
    if not isinstance(dirs, list):
        return errors + ["SEVEN_DIRECTIONS_MISSING"]
    ids = [r.get("id") for r in dirs if isinstance(r, dict)]
    if set(ids) != EXPECTED_DIRECTIONS or len(ids) != 7:
        errors.append("MISSING_OR_DUPLICATED_AXIS")
    for d in dirs:
        if not isinstance(d, dict) or d.get("status") not in ACCEPTED_TYPES:
            errors.append("UNKNOWN_OR_FALSE_PASS")
    auth = x.get("authority", [])
    if not isinstance(auth, list) or not any(r.get("domain") == "W20_BRIDGE" for r in auth):
        errors.append("SOURCE_PRODUCER_MISSING")
    else:
        w20 = next(r for r in auth if r.get("domain") == "W20_BRIDGE")
        pair = next((r for r in auth if r.get("domain") == "W20_PAIR40"), {})
        if w20.get("repo") != "rafaelmeloreisnovo/RafPolimata" or w20.get("head") != pair.get("head"):
            errors.append("CROSS_SOURCE_SHA_MISMATCH")
        if w20.get("pr") != 436 or pair.get("pr") != 436:
            errors.append("MISSING_PR_BINDING")
    for dev in x.get("unavailable_devices", []):
        if dev.get("physical_execution") != "NOT_APPLICABLE":
            errors.append("DESTROYED_HANDSET_RUNTIME_CLAIM")
    chain = x.get("physical_chain", [])
    if chain[-3:] != ["DEVICE_LAUNCH", "DEVICE_OUTPUT", "INDEPENDENT_REVIEW"]:
        errors.append("DEVICE_EVIDENCE_CHAIN_INCOMPLETE")
    for gap in x.get("gaps", []):
        if gap.get("state") not in {"TOKEN_VAZIO", "TOKEN_VAZIO_RELATIONAL",
                                    "TOKEN_VAZIO_SCIENCE", "TOKEN_VAZIO_PHYSICAL",
                                    "DESIGN_PROFILE_PENDING_RATIFICATION", "HOLD"}:
            errors.append("GAP_FALSE_CLOSED")
    return sorted(set(errors))


class TestMobileBitrafRoute(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(FILE.read_text(encoding="utf-8"))

    def test_scoped_source_contract(self):
        self.assertEqual(validate(self.base), [])

    def test_false_claim_rejected(self):
        import copy
        x = copy.deepcopy(self.base)
        x["claim_allowed"] = True
        self.assertTrue(validate(x))

    def test_physical_claim_for_lost_realme_rejected(self):
        import copy
        x = copy.deepcopy(self.base)
        x["unavailable_devices"][0]["physical_execution"] = "PASS"
        self.assertIn("DESTROYED_HANDSET_RUNTIME_CLAIM", validate(x))

    def test_bridge_same_head_as_serializer(self):
        import copy
        x = copy.deepcopy(self.base)
        next(a for a in x["authority"] if a["domain"] == "W20_PAIR40")["head"] = "0" * 40
        self.assertIn("CROSS_SOURCE_SHA_MISMATCH", validate(x))

    def test_missing_seven_direction_fails(self):
        import copy
        x = copy.deepcopy(self.base)
        x["seven_directions"].pop()
        self.assertIn("MISSING_OR_DUPLICATED_AXIS", validate(x))

    def test_unsupported_promotion_fails(self):
        import copy
        x = copy.deepcopy(self.base)
        x["promotion"] = "PASS"
        self.assertIn("PROMOTION_CLAIM_UNSAFE", validate(x))


if __name__ == "__main__":
    unittest.main()
