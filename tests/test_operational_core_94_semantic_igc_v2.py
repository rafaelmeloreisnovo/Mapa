import json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REG=ROOT/"data/core/operational-core-94.semantic-igc.v2.json"; VAL=ROOT/"scripts/validate_operational_core_94_semantic_igc_v2.py"
class T(unittest.TestCase):
 def bundle(self):
  td=tempfile.TemporaryDirectory(); r=Path(td.name); shutil.copytree(ROOT/'data',r/'data'); return td,r
 def runv(self,reg=REG): return subprocess.run([sys.executable,str(VAL),str(reg)],text=True,capture_output=True)
 def failhas(self,r,s): self.assertNotEqual(r.returncode,0); self.assertIn(s,r.stdout+r.stderr)
 def test_01_pass(self):
  r=self.runv(); self.assertEqual(r.returncode,0,r.stdout+r.stderr); self.assertEqual(json.loads(r.stdout)['paths'],37)
 def test_02_claim(self):
  td,r=self.bundle(); p=r/'data/core/shards/operational-core-94.nodes-001-008.v2.json'; d=json.loads(p.read_text()); d['items'][0]['claim_allowed']=True; p.write_text(json.dumps(d)); self.failhas(self.runv(r/'data/core/operational-core-94.semantic-igc.v2.json'),'promoted claim'); td.cleanup()
 def test_03_gate(self):
  td,r=self.bundle(); p=r/'data/core/operational-core-94.semantic-igc.v2.json'; d=json.loads(p.read_text()); d['semantic_method']['gate_profiles']['IGC-STATIC-LIMITED-V1']['cohesion_gates']['G_F']='TOKEN_VAZIO'; p.write_text(json.dumps(d)); self.failhas(self.runv(p),'missing gate G_F'); td.cleanup()
 def test_04_endpoint(self):
  td,r=self.bundle(); p=r/'data/core/shards/operational-core-94.paths-001-019.v2.json'; d=json.loads(p.read_text()); d['items'][0]['target']='UNKNOWN'; p.write_text(json.dumps(d)); self.failhas(self.runv(r/'data/core/operational-core-94.semantic-igc.v2.json'),'unknown endpoint'); td.cleanup()
 def test_05_duplicate_path(self):
  td,r=self.bundle(); p=r/'data/core/shards/operational-core-94.paths-001-019.v2.json'; d=json.loads(p.read_text()); d['items'][1]['path_id']='SP-001'; p.write_text(json.dumps(d)); self.failhas(self.runv(r/'data/core/operational-core-94.semantic-igc.v2.json'),'path IDs must be contiguous'); td.cleanup()
 def test_06_physical(self):
  td,r=self.bundle(); p=r/'data/core/operational-core-94.semantic-igc.v2.json'; d=json.loads(p.read_text()); d['path_metrics']['physical_execution_verified']=1; p.write_text(json.dumps(d)); self.failhas(self.runv(p),'physical execution cannot be promoted'); td.cleanup()
 def test_07_provider_collapse(self):
  td,r=self.bundle(); a=r/'data/core/shards/operational-core-94.nodes-009-016.v2.json'; d=json.loads(a.read_text()); d['items'][6]['source']['provider_id']=d['items'][5]['source']['provider_id']; a.write_text(json.dumps(d)); self.failhas(self.runv(r/'data/core/operational-core-94.semantic-igc.v2.json'),'distinct provider identities collapsed'); td.cleanup()
 def test_08_boundary(self):
  td,r=self.bundle(); p=r/'data/core/operational-core-94.semantic-igc.v2.json'; d=json.loads(p.read_text()); d['boundary']['unitemized_count']=77; p.write_text(json.dumps(d)); self.failhas(self.runv(p),'boundary does not close'); td.cleanup()
 def test_09_zone53(self):
  td,r=self.bundle(); a=r/'data/core/shards/operational-core-94.nodes-009-016.v2.json'; d=json.loads(a.read_text()); d['items'][7]['generator']['lineage_state']='VERIFIED'; a.write_text(json.dumps(d)); self.failhas(self.runv(r/'data/core/operational-core-94.semantic-igc.v2.json'),'zone53 generator must remain TOKEN_VAZIO'); td.cleanup()
if __name__=='__main__': unittest.main()
