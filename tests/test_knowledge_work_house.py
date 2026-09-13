import unittest
from scripts.validate_knowledge_work_house import validate_unit

def base_unit():
    return {
        "id":"KW-001",
        "intent":"reproduce one bounded knowledge/work unit",
        "authority":"rafaelmeloreisnovo/Mapa",
        "sources":[{"ref":"Drive:START_HERE","kind":"SOURCE","hash":None}],
        "context":{
            "scope":"bounded test",
            "boundary":"no scientific claim",
            "observed_at":"2026-09-13T00:05:00-03:00",
            "dependencies":[]
        },
        "artifact_refs":["artifact:A"],
        "execution_refs":["run:1"],
        "evidence":[{"ref":"receipt:1","type":"RECEIPT"}],
        "contradictions":[],
        "uncertainty":[{"id":"U1","state":"CLOSED","needed":None}],
        "reproduction":{"status":"PASS","procedure":"python test.py","environment_ref":"env:1"},
        "rollback":{"ready":True,"predecessor":"parent:1","procedure":"restore parent:1"},
        "reconstructibility":{
            "status":"PASS",
            "inputs_pinned":True,
            "versions_pinned":True,
            "outputs_identified":True
        },
        "state":"REPRODUCED",
        "claim_allowed":True,
        "next":"append receipt"
    }

class KnowledgeWorkHouseTests(unittest.TestCase):
    def test_promotable_unit(self):
        self.assertEqual(validate_unit(base_unit()), [])

    def test_open_contradiction_blocks_claim(self):
        u = base_unit()
        u["contradictions"] = [{"id":"C1","state":"OPEN","ref":"ref:c"}]
        self.assertIn("claim_gate:promotion_without_all_guards", validate_unit(u))

    def test_token_vazio_blocks_claim(self):
        u = base_unit()
        u["uncertainty"] = [{"id":"U1","state":"TOKEN_VAZIO","needed":"runtime"}]
        errs = validate_unit(u)
        self.assertIn("uncertainty:unresolved_but_claim_allowed", errs)

    def test_reproduction_required(self):
        u = base_unit()
        u["reproduction"]["status"] = "TOKEN_VAZIO"
        errs = validate_unit(u)
        self.assertIn("claim_gate:promotion_without_all_guards", errs)
        self.assertIn("reproduction:state_requires_pass", errs)

    def test_reconstructibility_required_for_closed(self):
        u = base_unit()
        u["state"] = "CLOSED"
        u["reconstructibility"]["outputs_identified"] = False
        errs = validate_unit(u)
        self.assertIn("reconstructibility:closed_requires_pass", errs)

if __name__ == "__main__":
    unittest.main()
