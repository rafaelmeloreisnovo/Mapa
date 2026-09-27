import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("cv",ROOT/"tools"/"validate_custody_types_v1.py")
M=importlib.util.module_from_spec(S); S.loader.exec_module(M)
class CustodyTypesTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.tax=M.load(ROOT/"data/governance/custody/00_INDEX/custody_types_v1.json")
  c.ev=M.load(ROOT/"data/governance/custody/07_EVIDENCE/custody_refactor_v1.sample_event.json")
 def test_taxonomy(c): c.assertEqual(M.validate_taxonomy(c.tax),[])
 def test_event(c): c.assertEqual(M.validate_event(c.ev,c.tax),[])
 def test_git_oid_not_sha256_label(c):
  e=json.loads(json.dumps(c.ev)); e["integrity"]["algorithm"]="SHA256"
  c.assertTrue(any("provider identity" in x for x in M.validate_event(e,c.tax)))
 def test_receipt_digest_requires_canonicalization(c):
  e=json.loads(json.dumps(c.ev)); e["integrity"]={"identity_kind":"receipt_digest","value":"aa"*32,"algorithm":"SHA256","canonicalization":None}
  c.assertTrue(any("canonicalization" in x for x in M.validate_event(e,c.tax)))
 def test_assistant_cannot_self_authorize(c):
  e=json.loads(json.dumps(c.ev)); e["actors"]["authorized_by"]={"type":"assistant_session","ref":"CURRENT_CONVERSATION"}
  c.assertTrue(any("self-authorize" in x for x in M.validate_event(e,c.tax)))
 def test_open_gap_blocks_claim(c):
  e=json.loads(json.dumps(c.ev)); e["claim_allowed"]=True
  c.assertTrue(any("open gap" in x for x in M.validate_event(e,c.tax)))
if __name__=="__main__": unittest.main()
