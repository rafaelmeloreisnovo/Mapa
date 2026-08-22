import json, unittest
from pathlib import Path
from tools.semantic_support.validate_semantic_support_v1 import ValidationError, validate

def contract(): return json.loads(Path("data/semantics/semantic-support-contract.v1.json").read_text(encoding="utf-8"))
def packets(): return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(Path("data/semantics/e1b").glob("*.json"))]

class SemanticSupportTests(unittest.TestCase):
    def test_canonical_packets_pass(self):
        r=validate(contract(),packets()); self.assertEqual(r["status"],"PASS"); self.assertEqual(r["packets"],6); self.assertEqual(r["support_arms"],13)
    def test_claim_true_fails_closed(self):
        ps=packets(); ps[0]["epistemic"]["claim_allowed"]=True
        with self.assertRaises(ValidationError): validate(contract(),ps)
    def test_unresolved_requires_two_readings(self):
        ps=packets(); p=next(x for x in ps if x["packet_id"]=="SEM:E1B:F01"); p["semantic"]["ambiguity"]["alternatives"]=[]
        with self.assertRaises(ValidationError): validate(contract(),ps)
    def test_analogy_cannot_support_proof(self):
        ps=packets(); p=next(x for x in ps if x["packet_id"]=="SEM:E1B:F08"); p["relations"][0]["evidence_effect"]="SUPPORTS"
        with self.assertRaises(ValidationError): validate(contract(),ps)
    def test_executed_requires_receipt(self):
        ps=packets(); ps[0]["epistemic"]["state"]="EXECUTED"; ps[0]["operational"]["execution_refs"]=[]
        with self.assertRaises(ValidationError): validate(contract(),ps)
if __name__=="__main__": unittest.main()
