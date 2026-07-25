import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('v',ROOT/'scripts/validate_operational_triage.py'); v=importlib.util.module_from_spec(s); s.loader.exec_module(v)
def load(): return json.loads((ROOT/'data/triage/rafaelia-operational-triage.v1.json').read_text())
class T(unittest.TestCase):
 def fail_has(self,d,n):
  r=v.validate(d); self.assertEqual('FAIL',r['status']); self.assertTrue(any(n in x for x in r['errors']),r)
 def test_valid(self):
  r=v.validate(load()); self.assertEqual('PASS',r['status'],r); self.assertEqual(8,r['metrics']['items']); self.assertEqual('ITM-001',r['execution_queue'][0]['item_id'])
 def test_duplicate(self): d=load(); d['items'].append(copy.deepcopy(d['items'][0])); self.fail_has(d,'duplicate item_id')
 def test_priority(self): d=load(); d['items'][0]['declared_priority']='P4_BACKLOG'; self.fail_has(d,'declared_priority')
 def test_privacy(self): d=load(); d['items'][0]['score_vector']['privacy_integrity']=1; self.fail_has(d,'privacy_integrity >= 4')
 def test_evidence(self): d=load(); d['items'][0]['invariants'][0]['evidence_refs']=[]; self.fail_has(d,'SATISFIED requires evidence_refs')
 def test_vazio_closed(self): d=load(); d['items'][2]['status']='CLOSED'; self.fail_has(d,'TOKEN_VAZIO cannot be VERIFIED or CLOSED')
 def test_missing_dep(self): d=load(); d['items'][2]['dependencies']=['ITM-999']; self.fail_has(d,'dependency ITM-999 does not exist')
 def test_cycle(self): d=load(); d['items'][0]['dependencies']=['ITM-004']; self.fail_has(d,'dependency cycle')
 def test_group_member(self): d=load(); d['groups'][0]['members'].append('ITM-999'); self.fail_has(d,'member ITM-999 does not exist')
 def test_same_mismatch(self):
  d=load(); d['relations'].append({'relation_id':'REL-999','left':'ITM-005','right':'ITM-006','relation_type':'SAME_SITUATION','evidence_refs':['ev:x'],'reason':'x','claim_allowed':False}); self.fail_has(d,'SAME_SITUATION mismatch')
 def test_same_needs_evidence(self):
  d=load(); x=copy.deepcopy(d['items'][0]); x['item_id']='ITM-009'; d['items'].append(x); d['groups'][0]['members'].append('ITM-009'); d['relations'].append({'relation_id':'REL-999','left':'ITM-001','right':'ITM-009','relation_type':'SAME_SITUATION','evidence_refs':[],'reason':'x','claim_allowed':False}); self.fail_has(d,'SAME_SITUATION requires evidence_refs')
 def test_same_distinct_conflict(self):
  d=load(); x=copy.deepcopy(d['items'][0]); x['item_id']='ITM-009'; d['items'].append(x); d['groups'][0]['members'].append('ITM-009'); d['relations'] += [{'relation_id':'REL-998','left':'ITM-001','right':'ITM-009','relation_type':'SAME_SITUATION','evidence_refs':['ev:x'],'reason':'x','claim_allowed':False},{'relation_id':'REL-999','left':'ITM-001','right':'ITM-009','relation_type':'DISTINCT','evidence_refs':[],'reason':'x','claim_allowed':False}]; self.fail_has(d,'cannot be SAME_SITUATION and DISTINCT')
 def test_claim(self): d=load(); d['claim_allowed']=True; self.fail_has(d,'claim_allowed must remain false')
 def test_endpoint(self): d=load(); d['relations'][0]['right']='ITM-999'; self.fail_has(d,'endpoints must exist')
 def test_order(self):
  p=[x['priority'] for x in v.validate(load())['execution_queue']]; self.assertEqual('P0_CRITICAL',p[0]); self.assertLess(p.index('P1_URGENT'),p.index('P2_NECESSARY'))
 def test_analogy(self): self.assertEqual('PASS',v.validate(load())['status'])
if __name__=='__main__': unittest.main()
