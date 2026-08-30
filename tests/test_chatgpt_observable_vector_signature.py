import copy
import json
import unittest
from pathlib import Path

from scripts.validate_chatgpt_observable_vector_signature import validate

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


class ObservableVectorSignatureTests(unittest.TestCase):
    def setUp(self):
        self.contract = load('data/control-plane/CHATGPT_OBSERVABLE_VECTOR_SIGNATURE_V1_20260829.json')
        self.fixture = load('fixtures/chatgpt_observable_vector_signature.sample.v1.json')

    def test_reference_fixture_passes(self):
        self.assertEqual(validate(self.contract, self.fixture), [])

    def test_hidden_activation_claim_fails(self):
        bad = copy.deepcopy(self.contract)
        bad['transformer_boundary']['hidden_activations_accessible'] = True
        self.assertTrue(validate(bad, self.fixture))

    def test_private_payload_key_fails(self):
        bad = copy.deepcopy(self.fixture)
        bad['nodes'][0]['private_payload'] = 'forbidden'
        self.assertTrue(validate(self.contract, bad))

    def test_vector_shape_fails_closed(self):
        bad = copy.deepcopy(self.fixture)
        bad['nodes'][0]['content_vector']['values'].pop()
        self.assertTrue(validate(self.contract, bad))

    def test_out_of_range_score_fails(self):
        bad = copy.deepcopy(self.fixture)
        bad['nodes'][1]['evidence_vector']['values'][0] = 1.1
        self.assertTrue(validate(self.contract, bad))

    def test_claim_gate_must_remain_false(self):
        bad = copy.deepcopy(self.fixture)
        bad['claim_allowed'] = True
        self.assertTrue(validate(self.contract, bad))


if __name__ == '__main__':
    unittest.main()
