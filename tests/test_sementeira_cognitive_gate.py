import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "sementeira_cognitive_gate.py"
spec = importlib.util.spec_from_file_location("sementeira_cognitive_gate", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def sha(ch: str) -> str:
    return ch * 64


def base_payload():
    return {
        "protocol_version": "SEMENTEIRA-5X7-V1",
        "event_id": "evt-001",
        "variables": {
            "intention": "Materializar um gate auditável.",
            "evidence": "Fonte e teste local identificados.",
            "human_state": "Urgência alta; resposta deve reduzir carga cognitiva.",
            "execution_capacity": "Python stdlib disponível.",
            "next_falsifiable_gate": "Executar testes e conferir receipt determinístico."
        },
        "directions": {
            "fact": "Existe protocolo textual 5x7.",
            "gap": "Pesos permanecem sem calibração.",
            "invariant": "Ausência não vira zero.",
            "variant": "Motor stdlib-only.",
            "proof_or_falsifier": "Teste unitário e receipt SHA-256.",
            "parable": "A régua mede antes de cortar.",
            "feedback": "Preservar F_ok, F_gap e F_next."
        },
        "evidence": [
            {"id": "src", "kind": "SOURCE", "locator": "docs/protocolo.md", "sha256": sha("a")},
            {"id": "method", "kind": "METHOD", "locator": "scripts/gate.py", "sha256": sha("b")},
            {"id": "test", "kind": "TEST_RECEIPT", "locator": "auditoria/receipt.json", "sha256": sha("c")}
        ],
        "claims": [{
            "id": "claim-1",
            "statement": "O contrato rejeita TOKEN_VAZIO convertido em zero.",
            "falsifier": "Um payload com TOKEN_VAZIO e value=0 passar sem bloqueio.",
            "evidence_refs": ["src", "method", "test"],
            "requested_state": "EVIDENCED",
            "weight": None
        }],
        "claim_allowed": False
    }


class CognitiveGateTests(unittest.TestCase):
    def test_valid_structure_passes_but_claim_stays_closed(self):
        receipt = module.build_receipt(base_payload())
        self.assertTrue(receipt["structural_pass"])
        self.assertFalse(receipt["claim_allowed"])
        self.assertEqual(receipt["claims"][0]["inferred_state"], "LOCAL_EVIDENCE_CANDIDATE")

    def test_sixth_human_variable_is_blocked(self):
        payload = base_payload()
        payload["variables"]["extra"] = "Não permitido"
        receipt = module.build_receipt(payload)
        self.assertFalse(receipt["structural_pass"])
        self.assertIn("FIVE_VARIABLES_EXCEEDED", {x["code"] for x in receipt["blocking_findings"]})

    def test_missing_direction_is_blocked(self):
        payload = base_payload()
        del payload["directions"]["feedback"]
        receipt = module.build_receipt(payload)
        self.assertFalse(receipt["structural_pass"])
        self.assertIn("SEVEN_DIRECTIONS_MISSING", {x["code"] for x in receipt["blocking_findings"]})

    def test_token_vazio_is_not_zero(self):
        payload = base_payload()
        payload["unknown_metric"] = {"state": "TOKEN_VAZIO", "value": 0, "weight": None}
        receipt = module.build_receipt(payload)
        self.assertIn("TOKEN_VAZIO_NOT_ZERO", {x["code"] for x in receipt["blocking_findings"]})

    def test_token_vazio_weight_must_remain_null(self):
        payload = base_payload()
        payload["unknown_metric"] = {"state": "TOKEN_VAZIO_CALIBRATION", "weight": 0.2}
        receipt = module.build_receipt(payload)
        codes = {x["code"] for x in receipt["blocking_findings"]}
        self.assertIn("TOKEN_VAZIO_WEIGHT_MUST_BE_NULL", codes)

    def test_numeric_claim_weight_needs_calibration_receipt(self):
        payload = base_payload()
        payload["claims"][0]["weight"] = 0.8
        receipt = module.build_receipt(payload)
        self.assertIn("UNSUPPORTED_NUMERIC_WEIGHT", {x["code"] for x in receipt["blocking_findings"]})

    def test_emotional_context_is_not_claim_evidence(self):
        payload = base_payload()
        payload["evidence"].append({"id": "emotion", "kind": "HUMAN_STATE", "locator": "self-report", "sha256": sha("d")})
        receipt = module.build_receipt(payload)
        codes = {x["code"] for x in receipt["blocking_findings"]}
        self.assertIn("EVIDENCE_KIND_INVALID", codes)
        self.assertIn("HUMAN_STATE_IS_NOT_EVIDENCE", codes)

    def test_replication_request_without_replication_is_blocked(self):
        payload = base_payload()
        payload["claims"][0]["requested_state"] = "REPLICATED"
        receipt = module.build_receipt(payload)
        self.assertIn("REPLICATION_REQUIRED", {x["code"] for x in receipt["blocking_findings"]})

    def test_receipt_is_deterministic(self):
        first = module.build_receipt(base_payload())
        second = module.build_receipt(base_payload())
        self.assertEqual(first["input_sha256"], second["input_sha256"])
        self.assertEqual(first["receipt_sha256"], second["receipt_sha256"])


if __name__ == "__main__":
    unittest.main()
