import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ATLAS=ROOT/'data'/'atlas'/'knowledge-campus-gymnasia.v1.json'

class KnowledgeCampusFederationTests(unittest.TestCase):
    def load(self): return json.loads(ATLAS.read_text(encoding='utf-8'))

    def test_sources_unmerged_fail_closed(self):
        d=self.load()
        self.assertEqual(d['state'],'PENDING_SOURCE_MERGES')
        self.assertFalse(d['claim_allowed'])
        self.assertEqual(d['executor_source']['state'],'UNMERGED')
        self.assertEqual(d['private_library_source']['state'],'UNMERGED')

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
