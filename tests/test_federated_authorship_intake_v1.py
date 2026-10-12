"""Adversarial source-attribution policy tests, metadata only, no source copies."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from validate_federated_authorship_intake_v1 import DEFAULT,verify

BASE=json.loads(DEFAULT.read_text(encoding="utf-8"))

def item(key,field,value):
    obj=copy.deepcopy(BASE)
    next(x for x in obj["entries"] if x["id"]==key)[field]=value
    return obj

class SourceAttributionFalsifiers(unittest.TestCase):
    def test_original_registry_is_structurally_closed(self):
        self.assertEqual([],verify(BASE))
    def test_global_claim_and_decision_cannot_upgrade(self):
        for field,value in (("claim_allowed",True),("decision","PASS"),
                            ("all_entries_copy_blocked",False),
                            ("scientific_novelty_proven",True)):
            with self.subTest(field=field):
                d=copy.deepcopy(BASE);d[field]=value
                self.assertIn("GLOBAL_PROMOTION_OR_SCHEMA_DRIFT",verify(d))
    def test_individual_source_import_blocked(self):
        self.assertIn("entry[2]:SOURCE_PROMOTION_OR_PRIVACY_BYPASS",
                      verify(item("VECTRAS_RMR_VECTOR","copy_policy","COPY_ALLOWED")))
    def test_synthetic_review_cannot_create_legal_rights(self):
        self.assertTrue(any("SOURCE_PROMOTION_OR_PRIVACY_BYPASS" in x for x in
                            verify(item("VECTRAS_RMR_VECTOR","independent_rights_review","PASS"))))
    def test_private_payload_forbidden(self):
        self.assertTrue(any("SOURCE_PROMOTION_OR_PRIVACY_BYPASS" in x for x in
                            verify(item("RAFAELIA_PRIVATE","personal_data_included",True))))
    def test_cannot_erase_upstream_kind(self):
        self.assertTrue(any("ORIGIN_UNTYPED" in x for x in
                            verify(item("VECTRAS_FORK_ABOUT","origin_class","MINE_EXCLUSIVE"))))
    def test_cannot_silently_relicense_vectras(self):
        self.assertTrue(any("VECTRAS_LICENSE_DOWNGRADE" in x for x in
                            verify(item("VECTRAS_RMR_VECTOR","license_state","MIT"))))
    def test_cannot_silently_relicense_rafgittools(self):
        self.assertTrue(any("RAFGITTOOLS_LICENSE_DOWNGRADE" in x for x in
                            verify(item("RAFGITTOOLS_LICENSE","license_state","GPL-2.0-only"))))
    def test_cannot_label_hosted_bitstack_l0(self):
        self.assertTrue(any("HOSTED_BITSTACK_MISLABELED_AS_L0" in x for x in
                            verify(item("LLAMA_BITSTACK","source_layer","C_FREESTANDING"))))
    def test_cannot_label_os_network_pure_l0(self):
        self.assertTrue(any("NETWORK_SYSCALLS_MISLABELED_AS_L0" in x for x in
                            verify(item("GAIA_PHI_NET","source_layer","C_FREESTANDING"))))
    def test_dont_promote_rll_from_scientific_reference(self):
        self.assertTrue(any("SCIENTIFIC_CLAIM_PROMOTION" in x for x in
                            verify(item("RLL_COSMOLOGY","origin_class","PROJECT_DECLARED_AUTHORIAL"))))
    def test_no_shadowed_approval_field(self):
        d=copy.deepcopy(BASE);d["entries"][2]["approval"]="PASS"
        self.assertTrue(any("SCHEMA_DRIFT" in x for x in verify(d)))
    def test_no_loss_of_an_entry(self):
        d=copy.deepcopy(BASE);d["entries"].pop()
        self.assertIn("SOURCE_CARDINALITY_DRIFT",verify(d))
    def test_bad_blob_is_not_evidence(self):
        self.assertTrue(any("BLOB_UNVERIFIED_FORMAT" in x for x in
                            verify(item("GAIA_PHI_BL0","observed_git_blob","0"))))
    def test_no_policy_waiver(self):
        d=copy.deepcopy(BASE);d["policy"]["no_private_payload"]=False
        self.assertIn("POLICY_INVARIANT_DISABLED",verify(d))
    def test_lama_barro_is_not_llama_cpp(self):
        d=copy.deepcopy(BASE)
        d["namespace_boundaries"]["LAMA_BARRO_PLUGIN"]["may_alias_llama_cpp"]=True
        self.assertIn("LAMA_LLAMA_NAMESPACE_OR_AUTHORITY_CONFLATION",verify(d))

    def test_no_fabricated_lama_plugin_path(self):
        d=copy.deepcopy(BASE)
        d["namespace_boundaries"]["LAMA_BARRO_PLUGIN"]["implementation_file"]="src/llama.cpp"
        self.assertIn("LAMA_LLAMA_NAMESPACE_OR_AUTHORITY_CONFLATION",verify(d))

    def test_no_false_standalone_lama_engine(self):
        d=copy.deepcopy(BASE)
        d["namespace_boundaries"]["LAMA_BARRO_PLUGIN"]["may_claim_standalone_engine"]=True
        self.assertIn("LAMA_LLAMA_NAMESPACE_OR_AUTHORITY_CONFLATION",verify(d))

    def test_opt_in_extension_not_the_model(self):
        d=copy.deepcopy(BASE)
        d["namespace_boundaries"]["LLAMARAFAELIA_EXTENSION"]["default_feature_state"]="ON"
        self.assertIn("LAMA_LLAMA_NAMESPACE_OR_AUTHORITY_CONFLATION",verify(d))

    def test_no_unaudited_missing_namespace(self):
        d=copy.deepcopy(BASE)
        del d["namespace_boundaries"]["LAMA_BARRO_PLUGIN"]
        self.assertIn("LAMA_LLAMA_NAMESPACE_OR_AUTHORITY_CONFLATION",verify(d))

    def test_non_object_input(self):
        self.assertEqual(["INVALID_ROOT"],verify([]))

if __name__=="__main__":
    unittest.main()
