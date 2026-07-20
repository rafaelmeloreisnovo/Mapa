from __future__ import annotations
import importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('pointer',ROOT/'scripts/validate_platform_assurance_pointer.py'); assert SPEC and SPEC.loader
v=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(v)
def base(): return json.loads((ROOT/'indices/PLATFORM_ASSURANCE_CONTROL_PLANE.json').read_text(encoding='utf-8'))
def reseal(d): d['integrity']['digest']=v.digest(d); return d
class Tests(unittest.TestCase):
 def invalid(self,d,text):
  with self.assertRaises(v.ValidationError) as c: v.validate(d)
  self.assertIn(text,str(c.exception))
 def test_valid(self):
  r=v.validate(base()); self.assertEqual('PASS',r['status']); self.assertEqual(5,r['p0_routes'])
 def test_claim_blocked(self):
  d=base(); d['claim_allowed']=True; reseal(d); self.invalid(d,'claim_allowed')
 def test_scope_drift(self):
  d=base(); d['scope']['work_item_count']=13; reseal(d); self.invalid(d,'work_item_count')
 def test_duplicate_route(self):
  d=base(); d['p0_routes'][1]['id']=d['p0_routes'][0]['id']; reseal(d); self.invalid(d,'duplicate')
 def test_unknown_route(self):
  d=base(); d['p0_routes'][0]['id']='WI-NOPE'; reseal(d); self.invalid(d,'unknown')
 def test_boundary_promotion_rejected(self):
  d=base(); d['boundaries']['security_blocker_is_compensable']=True; reseal(d); self.invalid(d,'must be false')
 def test_integrity_tamper(self):
  d=base(); d['state']='STALE_POINTER'; self.invalid(d,'digest mismatch')
 def test_observed_head_marks_stale(self):
  r=v.validate(base(),'1'*40); self.assertEqual('STALE_POINTER',r['pointer_state']); self.assertTrue(r['reasons'])
 def test_matching_head_remains_active(self):
  d=base(); r=v.validate(d,d['producer']['merge_commit']); self.assertEqual('ACTIVE_CONTROL_PLANE_WITH_OPEN_BLOCKERS',r['pointer_state'])
if __name__=='__main__': unittest.main()
