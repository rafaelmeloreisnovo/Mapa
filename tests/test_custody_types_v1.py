import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("cv",ROOT/"tools"/"validate_custody_types_v1.py")
M=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

class CustodyTypesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tax=M.load(ROOT/"data/governance/custody/00_INDEX/custody_types_v1.json")
        cls.can=M.load(ROOT/"data/control-plane/CUSTODY_CHAIN_TYPE_REGISTRY.v1.json")
        cls.map=M.load(ROOT/"data/governance/custody/01_ATLAS/CUSTODY_TYPES_V1_CANONICAL_MAPPING.json")
        cls.ev=M.load(ROOT/"data/governance/custody/07_EVIDENCE/custody_refactor_v1.sample_event.json")

    def test_taxonomy(self):
        self.assertEqual(M.validate_taxonomy(self.tax),[])

    def test_projection(self):
        self.assertEqual(M.validate_projection(self.tax,self.can,self.map),[])

    def test_event(self):
        self.assertEqual(M.validate_event(self.ev,self.tax),[])

    def test_projection_rejects_unknown_canonical_profile(self):
        m=json.loads(json.dumps(self.map))
        m["class_mapping"][0]["canonical_profiles"].append("INVENTED_PROFILE")
        self.assertTrue(any("unknown canonical profiles" in x for x in M.validate_projection(self.tax,self.can,m)))

    def test_c09_maps_to_explicit_canonical_credential_profile(self):
        row=next(x for x in self.map["class_mapping"] if x["local_class"]=="C09_CREDENTIAL_AUTHORITY")
        self.assertEqual(row["canonical_profiles"],["CREDENTIAL_PERMISSION_CUSTODY"])
        self.assertEqual(row["mapping_state"],"DIRECT")
        self.assertEqual(M.validate_projection(self.tax,self.can,self.map),[])

    def test_c09_rejects_wrong_canonical_profile(self):
        m=json.loads(json.dumps(self.map))
        row=next(x for x in m["class_mapping"] if x["local_class"]=="C09_CREDENTIAL_AUTHORITY")
        row["canonical_profiles"]=["AGENT_ACTION_CUSTODY"]
        self.assertTrue(any("C09 must map only" in x for x in M.validate_projection(self.tax,self.can,m)))

    def test_git_oid_not_sha256_label(self):
        e=json.loads(json.dumps(self.ev))
        e["integrity"]["algorithm"]="SHA256"
        self.assertTrue(any("provider identity" in x for x in M.validate_event(e,self.tax)))

    def test_receipt_digest_requires_canonicalization(self):
        e=json.loads(json.dumps(self.ev))
        e["integrity"]={"identity_kind":"receipt_digest","value":"aa"*32,"algorithm":"SHA256","canonicalization":None}
        self.assertTrue(any("canonicalization" in x for x in M.validate_event(e,self.tax)))

    def test_assistant_cannot_self_authorize(self):
        e=json.loads(json.dumps(self.ev))
        e["actors"]["authorized_by"]={"type":"assistant_session","ref":"CURRENT_CONVERSATION"}
        self.assertTrue(any("self-authorize" in x for x in M.validate_event(e,self.tax)))

    def test_open_gap_blocks_claim(self):
        e=json.loads(json.dumps(self.ev))
        e["claim_allowed"]=True
        self.assertTrue(any("open gap" in x for x in M.validate_event(e,self.tax)))

if __name__=="__main__":
    unittest.main()
