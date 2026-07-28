from __future__ import annotations
import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("router", ROOT/"scripts"/"route_longitudinal_vector_domain.py")
router=importlib.util.module_from_spec(SPEC); assert SPEC.loader; SPEC.loader.exec_module(router)
ENV=json.loads((ROOT/"examples"/"domain-routing-envelope.v1.json").read_text(encoding="utf-8"))
REG=json.loads((ROOT/"config"/"domain-authority-registry.v1.json").read_text(encoding="utf-8"))

class RouterTests(unittest.TestCase):
    def run_route(self,p=None,r=None):
        return router.route(copy.deepcopy(p or ENV),copy.deepcopy(r or REG),ROOT)
    def test_valid_routes(self):
        out=self.run_route(); self.assertEqual(out["state"],"PASS"); self.assertEqual(out["route_count"],2)
    def test_no_claim_promotion(self):
        self.assertFalse(self.run_route()["claim_allowed"])
    def test_unknown_domain_blocked(self):
        p=copy.deepcopy(ENV); p["claims"][0]["declared_domain"]="METAPHYSICAL"
        with self.assertRaises(router.RoutingError): self.run_route(p)
    def test_domain_list_blocked(self):
        p=copy.deepcopy(ENV); p["claims"][0]["declared_domain"]=["COMPUTATIONAL","SCIENTIFIC"]
        with self.assertRaises(router.RoutingError): self.run_route(p)
    def test_cross_domain_promotion_blocked(self):
        p=copy.deepcopy(ENV); p["cross_domain_promotion_allowed"]=True
        with self.assertRaises(router.RoutingError): self.run_route(p)
    def test_semantic_inference_blocked(self):
        p=copy.deepcopy(ENV); p["semantic_domain_inference_allowed"]=True
        with self.assertRaises(router.RoutingError): self.run_route(p)
    def test_claim_type_domain_mismatch(self):
        p=copy.deepcopy(ENV); p["claims"][0]["declared_domain"]="LEGAL"
        with self.assertRaises(router.RoutingError): self.run_route(p)
    def test_input_state_domain_mismatch(self):
        p=copy.deepcopy(ENV); p["claims"][0]["input_state"]="POLICY_LINKED"
        with self.assertRaises(router.RoutingError): self.run_route(p)
    def test_forbidden_transition(self):
        p=copy.deepcopy(ENV); p["claims"][0]["requested_transition"]="PROVED"
        with self.assertRaises(router.RoutingError): self.run_route(p)
    def test_missing_source_ref(self):
        p=copy.deepcopy(ENV); p["claims"][0]["source_refs"]=[]
        with self.assertRaises(router.RoutingError): self.run_route(p)
    def test_hash_mismatch(self):
        p=copy.deepcopy(ENV); p["vector"]["canonical_sha256"]="0"*64
        with self.assertRaises(router.RoutingError): self.run_route(p)
    def test_vector_id_mismatch(self):
        p=copy.deepcopy(ENV); p["vector"]["vector_id"]="wrong"
        with self.assertRaises(router.RoutingError): self.run_route(p)
    def test_vector_revision_mismatch(self):
        p=copy.deepcopy(ENV); p["vector"]["revision"]=2
        with self.assertRaises(router.RoutingError): self.run_route(p)
    def test_duplicate_claim_id(self):
        p=copy.deepcopy(ENV); p["claims"].append(copy.deepcopy(p["claims"][0]))
        with self.assertRaises(router.RoutingError): self.run_route(p)
    def test_registry_must_have_four_authorities(self):
        r=copy.deepcopy(REG); del r["domains"]["ETHICAL"]
        with self.assertRaises(router.RoutingError): self.run_route(r=r)
    def test_domain_results_are_separate_batches(self):
        out=self.run_route(); self.assertEqual(set(out["gate_batches"]),{"gate.computational.v1","gate.ethical.v1"})
    def test_parable_route_does_not_become_evidence(self):
        out=self.run_route(); ethical=[x for x in out["routes"] if x["declared_domain"]=="ETHICAL"][0]
        self.assertFalse(ethical["epistemic_promotion_allowed"])
if __name__=="__main__": unittest.main()
