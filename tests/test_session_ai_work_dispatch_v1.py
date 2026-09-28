import json, unittest, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('dispatch_validator',ROOT/'tools/audit/validate_session_ai_work_dispatch_v1.py')
MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)
class SessionDispatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.data=json.loads((ROOT/'data/control-plane/SESSION_AI_WORK_DISPATCH_V1.json').read_text(encoding='utf-8'))
    def test_registry_passes(self):
        out=MOD.validate(self.data); self.assertEqual(out['status'],'PASS'); self.assertFalse(out['claim_allowed']); self.assertGreaterEqual(out['roles'],10); self.assertGreaterEqual(out['packets'],8)
    def test_every_packet_is_bounded(self):
        for p in self.data['session_packets']:
            self.assertLessEqual(len(p['source_min']),3); self.assertTrue(p['authority']); self.assertTrue(p['execution_target']); self.assertTrue(p['evidence_rule'])
    def test_assignment_never_means_execution(self): self.assertIn('AGENT_ASSIGNMENT != AGENT_EXECUTION',self.data['invariants'])
    def test_private_body_not_public_router(self): self.assertIn('NO_RAW_PRIVATE_BODY_IN_PUBLIC_ROUTER',self.data['invariants'])
if __name__=='__main__': unittest.main()
