import json, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VALIDATOR=ROOT/'tools/validate_federated_reference_matrix.py'
MATRIX=ROOT/'data/control-plane/federated-reference-matrix.v1.json'

class TestFederatedReferenceMatrix(unittest.TestCase):
    def run_case(self,data):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'m.json'; p.write_text(json.dumps(data),encoding='utf-8')
            return subprocess.run([sys.executable,str(VALIDATOR),str(p)],capture_output=True,text=True)
    def test_canonical_matrix(self):
        r=subprocess.run([sys.executable,str(VALIDATOR),str(MATRIX)],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertIn('PASS_LOCAL_LIMITED',r.stdout)
    def test_reject_claim_promotion(self):
        d=json.loads(MATRIX.read_text()); d['claim_allowed']=True
        self.assertNotEqual(self.run_case(d).returncode,0)
    def test_reject_dangling_edge(self):
        d=json.loads(MATRIX.read_text()); d['edges'][0]['to']='N-MISSING'
        self.assertNotEqual(self.run_case(d).returncode,0)
    def test_reject_duplicate_node(self):
        d=json.loads(MATRIX.read_text()); d['nodes'].append(dict(d['nodes'][0]))
        self.assertNotEqual(self.run_case(d).returncode,0)
    def test_reject_evidence_without_receipt(self):
        d=json.loads(MATRIX.read_text()); d['edges'][0]['receipt_locator']=None
        self.assertNotEqual(self.run_case(d).returncode,0)

if __name__=='__main__': unittest.main()
