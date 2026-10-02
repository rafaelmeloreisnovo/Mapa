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
    def test_scoped_authority_split_and_runtime_chain(self):
        d=json.loads(MATRIX.read_text())
        nodes={n['id']:n for n in d['nodes']}
        edges={e['id']:e for e in d['edges']}
        self.assertEqual(nodes['N-MAPA']['authority_role'],'ONTOLOGY')
        self.assertEqual(nodes['N-RAFGITTOOLS']['authority_role'],'CONTROL_PLANE')
        self.assertEqual(nodes['N-TERMUX-PACKAGES']['locator'],'rafaelmeloreisnovo/termux-packages')
        self.assertEqual(edges['E-MAPA-RGT']['relation'],'REFERENCES')
        self.assertEqual(edges['E-RGT-MAPA']['relation'],'GOVERNS')
        self.assertEqual(edges['E-PKG-TERMUX']['relation'],'PRODUCES')
        self.assertEqual(edges['E-TERMUX-PKG']['relation'],'CONSUMES')
    def test_current_drive_custody_replaces_dead_locators(self):
        d=json.loads(MATRIX.read_text())
        locators={n['locator'] for n in d['nodes']}
        self.assertIn('drive:1NIv_E2NdtdLaKi3dWTwqPVl7B9zIKrRk',locators)
        self.assertIn('drive:1n7ZiUL8gpVr0cZe1NDXCxXdyXK5lgoEk2jk9uHWWQ0o',locators)
        self.assertNotIn('drive:1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88',locators)
        self.assertNotIn('drive:1HlBedJvhjj1WO4yQszwcSRRlHY7lhSgt',locators)

if __name__=='__main__': unittest.main()
