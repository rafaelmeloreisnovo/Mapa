import copy
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "model_semantic_rapport_validator",
    ROOT / "tools" / "validate_model_semantic_rapport.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ModelSemanticRapportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_control = json.loads(
            (ROOT / "contracts/model-semantic-rapport.v1.json").read_text(
                encoding="utf-8"
            )
        )
        cls.base_packet = json.loads(
            (ROOT / "examples/model-semantic-rapport.closed-provider.v1.json")
            .read_text(encoding="utf-8")
        )

    def control(self):
        return copy.deepcopy(self.base_control)

    def packet(self):
        return copy.deepcopy(self.base_packet)

    def test_schema_declares_the_expected_packet_boundary(self):
        schema = json.loads(
            (ROOT / "schemas/model-semantic-rapport.v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            "https://json-schema.org/draft/2020-12/schema", schema["$schema"]
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertIn("model_surface", schema["required"])
        self.assertIn("nodes", schema["required"])
        self.assertIn("edges", schema["required"])
        self.assertIn("gaps", schema["required"])

    def node(self, packet, node_id):
        return next(item for item in packet["nodes"] if item["node_id"] == node_id)

    def test_closed_provider_boundary_passes_without_internal_claim(self):
        report = MODULE.validate_rapport(self.control(), self.packet())
        self.assertEqual("PASS", report["status"])
        self.assertEqual(13, report["node_count"])
        self.assertEqual(15, report["edge_count"])
        self.assertEqual(6, report["gap_count"])
        self.assertGreater(report["blocking_gap_count"], 0)
        self.assertIsNone(report["parameter_update_observed"])
        self.assertFalse(report["model_internal_claim_allowed"])
        self.assertFalse(report["claim_allowed"])

    def test_lnn_ambiguity_cannot_be_silently_resolved(self):
        control = self.control()
        lnn = next(item for item in control["acronym_registry"] if item["symbol"] == "LNN")
        lnn["resolution"] = "RESOLVED"
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(control, self.packet())

    def test_hidden_weights_cannot_be_promoted_to_measured(self):
        packet = self.packet()
        node = self.node(packet, "N-PARAMETERS")
        node["observability"] = "LOCAL_ARTIFACT_INSPECTED"
        node["epistemic_state"] = "MEASURED_LOCAL"
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)

    def test_unknown_tokenizer_cannot_yield_observed_native_ids(self):
        packet = self.packet()
        node = self.node(packet, "N-TOKEN-IDS")
        node["observability"] = "DIRECT_OBSERVED"
        node["epistemic_state"] = "DOCUMENTED"
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)

    def test_llm_label_and_generic_paper_do_not_prove_transformer_runtime(self):
        packet = self.packet()
        surface = packet["model_surface"]
        surface["architecture_family"] = "TRANSFORMER"
        surface["architecture_expansion"] = "TRANSFORMER_ARCHITECTURE"
        surface["architecture_evidence_refs"] = ["REF-TRANSFORMER-2017"]
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)

    def test_context_cannot_update_parameters_in_unknown_runtime(self):
        packet = self.packet()
        edge = next(
            item for item in packet["edges"]
            if item["edge_id"] == "E-CONTEXT-NOT-WEIGHT-PROOF"
        )
        edge["relation"] = "UPDATES_PARAMETER"
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)

    def test_parameter_update_requires_execution_receipt(self):
        packet = self.packet()
        packet["model_surface"]["execution_mode"] = "ONLINE_LEARNING"
        packet["model_surface"]["parameter_update_observed"] = True
        packet["context_effect"]["parameter_update_observed"] = True
        packet["context_effect"]["parameter_update_state"] = "DOCUMENTED"
        edge = next(
            item for item in packet["edges"]
            if item["edge_id"] == "E-CONTEXT-NOT-WEIGHT-PROOF"
        )
        edge["relation"] = "UPDATES_PARAMETER"
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)

    def test_parameter_update_with_typed_receipt_is_structurally_allowed(self):
        packet = self.packet()
        packet["instance_sources"].append(
            {
                "source_id": "SRC-MSR-TRAINING-RECEIPT",
                "kind": "PROVIDER_EXECUTION_RECEIPT",
                "reference": "receipt:synthetic-contract-test",
                "scope": "Synthetic structural fixture for the allowed update route; not a real provider claim.",
            }
        )
        packet["model_surface"]["execution_mode"] = "ONLINE_LEARNING"
        packet["model_surface"]["parameter_update_observed"] = True
        packet["context_effect"]["parameter_update_observed"] = True
        packet["context_effect"]["parameter_update_state"] = "DOCUMENTED_BY_RECEIPT"
        edge = next(
            item for item in packet["edges"]
            if item["edge_id"] == "E-CONTEXT-NOT-WEIGHT-PROOF"
        )
        edge["relation"] = "UPDATES_PARAMETER"
        edge["source_refs"] = ["SRC-MSR-TRAINING-RECEIPT"]
        edge["epistemic_state"] = "DOCUMENTED"
        report = MODULE.validate_rapport(self.control(), packet)
        self.assertEqual("PASS", report["status"])
        self.assertTrue(report["parameter_update_observed"])

    def test_observed_parameter_update_requires_a_typed_edge(self):
        packet = self.packet()
        packet["model_surface"]["execution_mode"] = "ONLINE_LEARNING"
        packet["model_surface"]["parameter_update_observed"] = True
        packet["context_effect"]["parameter_update_observed"] = True
        packet["context_effect"]["parameter_update_state"] = "DOCUMENTED_BY_RECEIPT"
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)

    def test_dangling_rapport_edge_is_rejected(self):
        packet = self.packet()
        packet["edges"][0]["target"] = "N-MISSING"
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)

    def test_external_semantics_native_embedding_boundary_is_required(self):
        packet = self.packet()
        packet["edges"] = [
            item for item in packet["edges"]
            if item["edge_id"] != "E-EMBEDDINGS-NOT-SEMANTICS"
        ]
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)

    def test_gap_requires_a_next_probe(self):
        packet = self.packet()
        packet["gaps"][0]["next_probe"] = ""
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)

    def test_missing_machine_field_fails_closed(self):
        packet = self.packet()
        del packet["nodes"][0]["label"]
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)

    def test_unexpected_machine_field_fails_closed(self):
        packet = self.packet()
        packet["latent_truth"] = "invented"
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)

    def test_non_object_packet_fails_closed(self):
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), [])

    def test_all_eight_boundary_invariants_are_required(self):
        packet = self.packet()
        packet["invariants"].remove("LNN requires explicit expansion")
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)

    def test_code_license_cannot_be_copied_to_weights_without_authority(self):
        packet = self.packet()
        right = next(
            item for item in packet["model_surface"]["rights"]
            if item["unit"] == "WEIGHTS"
        )
        right["state"] = "MIT_FROM_REPOSITORY"
        with self.assertRaises(MODULE.RapportError):
            MODULE.validate_rapport(self.control(), packet)


if __name__ == "__main__":
    unittest.main()
