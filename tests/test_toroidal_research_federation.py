from __future__ import annotations
import importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('validator',ROOT/'scripts/validate_toroidal_research_federation.py'); assert SPEC and SPEC.loader
validator=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(validator)

def base(): return json.loads((ROOT/'indices/TOROIDAL_RESEARCH_FEDERATION.json').read_text(encoding='utf-8'))
def reseal(d): d['integrity']['digest']=validator.digest(d); return d
class Tests(unittest.TestCase):
    def invalid(self,d,text):
        with self.assertRaises(validator.ValidationError) as c: validator.validate(d)
        self.assertIn(text,str(c.exception))
    def test_valid(self): self.assertEqual('PASS',validator.validate(base())['status'])
    def test_duplicate_role(self):
        d=base(); d['repositories'][1]['role']='GOVERNANCE'; reseal(d); self.invalid(d,'duplicate role')
    def test_active_requires_evidence(self):
        d=base(); d['repositories'][0]['evidence_locator']='TOKEN_VAZIO'; reseal(d); self.invalid(d,'required for ACTIVE')
    def test_planned_requires_exit_criteria(self):
        d=base(); d['repositories'][2]['exit_criteria']=[]; reseal(d); self.invalid(d,'exit_criteria required')
    def test_unknown_dependency(self):
        d=base(); d['repositories'][2]['depends_on']=['R-NOPE']; reseal(d); self.invalid(d,'unknown id')
    def test_cycle_rejected(self):
        d=base(); d['edges'].append({'from':'R-MAP','to':'R-GOV','relation':'bad-cycle'}); d['derived']['edge_count']+=1; d['derived']['cycle_count']=1; reseal(d); self.invalid(d,'must be acyclic')
    def test_claim_allowed_blocked(self):
        d=base(); d['governance']['claim_allowed']=True; reseal(d); self.invalid(d,'claim_allowed=false')
    def test_digest_tamper(self):
        d=base(); d['repositories'][0]['artifact_path']='tampered'; self.invalid(d,'digest mismatch')
if __name__=='__main__': unittest.main()
