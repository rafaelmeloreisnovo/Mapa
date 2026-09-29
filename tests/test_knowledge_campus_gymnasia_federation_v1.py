import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ATLAS=ROOT/'data'/'atlas'/'knowledge-campus-gymnasia.v1.json'

class KnowledgeCampusFederationTests(unittest.TestCase):
    def load(self): return json.loads(ATLAS.read_text(encoding='utf-8'))

    def test_sources_merged_main_bound_claims_still_fail_closed(self):
        d=self.load()
        self.assertEqual(d['state'],'SOURCE_MERGES_BOUND_CLAIMS_GATED')
        self.assertFalse(d['claim_allowed'])
        self.assertEqual(d['executor_source']['state'],'MERGED_MAIN_BOUND')
        self.assertEqual(d['executor_source']['head'],'0057ce61fbc186745f4427d3a0a0ca9df59d3715')
        self.assertEqual(d['executor_source']['merge'],'6b0f00e3fa912c295587d32e9c4a546c811e8ddf')
        self.assertEqual(d['private_library_source']['state'],'MERGED_MAIN_BOUND')
        self.assertEqual(d['private_library_source']['head'],'6c5a6aa0fc1e631bcb2ab5d851a7f75e1785c78b')
        self.assertEqual(d['private_library_source']['merge'],'e36c5a36f090a8d21ac337c227a18b6208fab005')

    def test_tiers_are_existing_carrier_vocabulary(self):
        self.assertEqual(self.load()['tiers']['allowed'],['HOT','WARM','COLD','ARCHIVE'])

    def test_analogy_and_evidence_are_separate(self):
        d=self.load()['relation_dimensions']
        self.assertIn('ANALOGY_TO',d['semantic'])
        self.assertNotIn('ANALOGY_TO',d['epistemic'])

    def test_query_is_bounded(self):
        q=self.load()['campus_query_rule']
        self.assertLessEqual(q['roots_max'],3)
        self.assertEqual(q['depth_default'],1)

if __name__=='__main__': unittest.main()
