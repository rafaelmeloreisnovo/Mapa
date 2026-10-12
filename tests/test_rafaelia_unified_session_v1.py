"""Adversarial falsifiers: prevent an invented unified ChatGPT event or inflated claims."""
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from validate_rafaelia_unified_session_v1 import SOURCE,validate
BASE=json.loads(SOURCE.read_text(encoding="utf-8"))

def modified(path,value):
    d=copy.deepcopy(BASE)
    t=d
    for k in path[:-1]:
        t=t[k]
    t[path[-1]]=value
    return d

def assert_reject(case,path,value,reason):
    state=modified(path,value)
    problems=validate(state)
    case.assertIn(reason,problems,problems)

class UnifiedInteractionAdversarialTests(unittest.TestCase):
    def test_baseline_is_only_a_scoped_metadata_pass(self):
        self.assertEqual(validate(BASE),[])
    def test_root_cannot_be_string(self):
        self.assertEqual(validate("APPROVED"),["ROOT_NOT_OBJECT"])
    def test_schema_is_versioned(self):
        assert_reject(self,["schema"],"v99","SCHEMA_VERSION")
    def test_snapshot_mutation_requires_new_version(self):
        assert_reject(self,["version"],"S2","IMMUTABLE_SNAPSHOT_VERSION")
    def test_composite_cannot_claim_single_real_event(self):
        assert_reject(self,["logical_interaction","type"],"SINGLE_SOURCE_EVENT","PHANTOM_SINGLE_SOURCE_SESSION")
    def test_composite_cannot_claim_exact_chat_id(self):
        assert_reject(self,["logical_interaction","raw_chat_session_id"],"42","PHANTOM_SINGLE_SOURCE_SESSION")
    def test_unknown_original_time_stays_unknown(self):
        assert_reject(self,["logical_interaction","historical_exact_message_boundaries"],"VERIFIED","PHANTOM_MESSAGE_GENEALOGY")
    def test_no_raw_source_copies(self):
        assert_reject(self,["read_model","no_raw_corpus_replication"],False,"SOURCE_FIRST_AND_PRIVATE_ROUTING")
    def test_bootstrap_v22_supersedes_old_lite(self):
        assert_reject(self,["read_model","start"],"START_LITE","SOURCE_FIRST_AND_PRIVATE_ROUTING")
    def test_l9_dimensionality(self):
        assert_reject(self,["axes","L9"],["LONGITUDINAL"],"L9_S7_SOURCE_PLANES")
    def test_s7_dimensionality(self):
        assert_reject(self,["axes","S7"],["FILE"],"L9_S7_SOURCE_PLANES")
    def test_proof_plane_separation(self):
        assert_reject(self,["axes","plane5"],["SOURCE","CLAIM"],"L9_S7_SOURCE_PLANES")
    def test_zero_not_empty(self):
        assert_reject(self,["typed_null_discriminants"],["NUMERIC_ZERO"],"TYPED_EMPTY_NOT_ZERO")
    def test_no_conflation_invariants(self):
        xs=BASE["critical_invariants"].copy()
        xs.remove("IMPLEMENTED_UNTESTED_NE_PASS")
        assert_reject(self,["critical_invariants"],xs,"BOUNDARIES_REMOVED")
    def test_producer_authority_not_invented(self):
        assert_reject(self,["producers"],{"Mapa":"ALL_AUTHORITY"},"FEDERATED_PRODUCER_AUTHORITY")
    def test_missing_family_detected(self):
        d=copy.deepcopy(BASE)
        d["vectors"].pop()
        self.assertIn("VECTOR_COVERAGE_MISSING",validate(d))
    def test_missing_gap_detected(self):
        d=copy.deepcopy(BASE)
        d["gaps"].pop()
        self.assertIn("GAP_COVERAGE_MISSING",validate(d))
    def test_token_vazio_is_useful_and_typed(self):
        assert_reject(self,["gaps",0,"token_type"],"NUMERIC_ZERO","GAP_TYPE_LOSS:G001")
    def test_gap_reason_cannot_vanish(self):
        assert_reject(self,["gaps",0,"missing_reason"],"","GAP_TYPE_LOSS:G001")
    def test_prior_partial_cannot_be_closed_by_memo(self):
        assert_reject(self,["gaps",8,"state"],"VERIFIED","GAP_STATE_OR_AUTHORITY:G009")
    def test_missing_evidence_request(self):
        assert_reject(self,["gaps",10,"evidence_required"],"","GAP_NO_evidence_required:G011")
    def test_missing_falsifier(self):
        assert_reject(self,["gaps",16,"falsifier"],"","GAP_NO_falsifier:G017")
    def test_missing_next_action(self):
        assert_reject(self,["gaps",12,"next_action"],"","GAP_NO_next_action:G013")
    def test_receipt_cannot_be_marked_pass_by_hand(self):
        assert_reject(self,["gaps",0,"receipt_state"],"SEALED","GAP_FAKE_CLOSURE:G001")
    def test_claim_cannot_auto_pass(self):
        assert_reject(self,["gaps",9,"claim_allowed"],True,"GAP_FAKE_CLOSURE:G010")
    def test_rollback_cannot_be_deleted(self):
        assert_reject(self,["gaps",22,"rollback"],"NO_ROLLBACK","GAP_ROLLBACK_MUTATION:G023")
    def test_gaps_must_be_connected(self):
        d=copy.deepcopy(BASE)
        for f in d["vectors"]:
            f["gaps"]=[g for g in f["gaps"] if g!="G020"]
        self.assertIn("ORPHANED_GAP",validate(d))
    def test_every_vector_must_have_gap_relation(self):
        assert_reject(self,["vectors",9,"gaps"],[],"VECTOR_GAP_EDGE_MISSING:F10")
    def test_no_false_licence_owner_in_map(self):
        assert_reject(self,["vectors",16,"producer"],"Mapa-LICENSE-AUTHORITY","VECTOR_INCOMPLETE:F17")
    def test_no_rll_smoke_as_runtime(self):
        assert_reject(self,["vectors",9,"runtime_evidence_state"],"SCIENCE_PASS","VECTOR_OVERCLAIM:F10")
    def test_no_lama_llama_name_collision(self):
        assert_reject(self,["vectors",19,"family"],"LLAMA_CPP_NATIVE","SEMANTIC_NAMESPACE_COLLAPSE:F20")
    def test_42_nodes_do_not_mean_isomorphic(self):
        assert_reject(self,["formal_falsification_fixtures","circulant_C42_pm6_pm7","e"],120,"GRAPH42_FALSE_ISOMORPHISM")
    def test_euler_falsifier(self):
        assert_reject(self,["formal_falsification_fixtures","icosphere_f2","euler"],0,"GRAPH42_FALSE_ISOMORPHISM")
    def test_136_metrics_not_137_complete(self):
        assert_reject(self,["formal_falsification_fixtures","historical_zone_metric_rows","count"],137,"ZONE136_VS137_FALSE_COVERAGE")
    def test_chart_cache_not_data(self):
        assert_reject(self,["formal_falsification_fixtures","office_chart_xml","chart_cache_not_observational_data"],False,"UNSOURCED_OFFICE_CHART_PROMOTION")
    def test_chart_workbook_remains_unbound(self):
        assert_reject(self,["formal_falsification_fixtures","office_chart_xml","source_workbook"],"WORKBOOK_PROVEN","UNSOURCED_OFFICE_CHART_PROMOTION")
    def test_graph_nodes_cannot_disappear(self):
        d=copy.deepcopy(BASE)
        d["semantic_graph"]["nodes"].pop()
        self.assertIn("NODE_MISSING_OR_DUPLICATE",validate(d))
    def test_graph_edges_cannot_disappear(self):
        d=copy.deepcopy(BASE)
        d["semantic_graph"]["edges"].pop()
        self.assertIn("GRAPH_EDGE_BIJECTION_MISSING",validate(d))
    def test_graph_edges_need_provenance(self):
        assert_reject(self,["semantic_graph","edges",0,"provenance"],"","EDGE_WITHOUT_SOURCE_OR_STATE")
    def test_graph_edges_cannot_cause_by_cooccur(self):
        assert_reject(self,["semantic_graph","edges",0,"relation"],"CAUSES","DANGLING_OR_UNTYPED_EDGE")
    def test_dangling_graph_endpoint_rejected(self):
        assert_reject(self,["semantic_graph","edges",1,"to"],"NONEXISTENT","DANGLING_OR_UNTYPED_EDGE")
    def test_prior_ci_requires_exact_head_refresh(self):
        assert_reject(self,["evidence_register",0,"state"],"GREEN_GLOBAL","PRIOR_CI_FALSE_PROMOTION")
    def test_receipt_template_is_not_execution(self):
        assert_reject(self,["receipts",0,"state"],"EXECUTED","RECEIPT_FAKE_EXECUTION")
    def test_no_merging_without_provider(self):
        assert_reject(self,["promotion","repo_merge_allowed"],True,"PROMOTION_UNAUTHORIZED")
    def test_no_private_drive_urls_in_public_projection(self):
        assert_reject(self,["logical_interaction","definition"],"https://drive.google.com/file/d/secret","PRIVATE_LINK_OR_SECRET_IN_PUBLIC_MANIFEST")
    def test_no_tokens_or_secrets(self):
        assert_reject(self,["logical_interaction","definition"],"sk-supersecretkeywithlength1234","PRIVATE_LINK_OR_SECRET_IN_PUBLIC_MANIFEST")
    def test_office_security_fixture_is_not_novoexport(self):
        assert_reject(self,["discovery_provenance","office_xml","source_bucket"],
            "NOVOEXPORT_SOURCE_PROVEN","EXTERNAL_CHART_ORIGIN_GATE:office_xml")
    def test_office_folder_ancestry_is_enforced(self):
        assert_reject(self,["discovery_provenance","office_xml","not_within_verified_novoexport_subtree"],
            False,"EXTERNAL_CHART_ORIGIN_GATE:office_xml")
    def test_flutter_upstream_not_own_math_core(self):
        assert_reject(self,["discovery_provenance","dart_charts","source_bucket"],
            "AUTHORIAL_KERNEL","EXTERNAL_CHART_ORIGIN_GATE:dart_charts")
    def test_rafaelia_upload_not_novoexport_shard(self):
        assert_reject(self,["discovery_provenance","graphviz","source_bucket"],
            "RAW_NOVOEXPORT_SHARD","EXTERNAL_CHART_ORIGIN_GATE:graphviz")
    def test_correction_is_append_only(self):
        assert_reject(self,["discovery_provenance","predecessor_retain"],
            False,"MISSING_PROVENANCE_CORRECTION")
    def test_chart_cache_security_source_not_a_real_sample(self):
        assert_reject(self,["formal_falsification_fixtures","office_chart_xml","origin_class"],
            "OBSERVATIONAL_DATA","SECURITY_FIXTURE_MISATTRIBUTED_NOVOEXPORT")
    def test_extra_root_promotion_field_rejected(self):
        d=copy.deepcopy(BASE)
        d["provider_approved"]=True
        self.assertIn("ROOT_UNKNOWN_FIELDS",validate(d))
    def test_extra_gap_false_sealed_field_rejected(self):
        d=copy.deepcopy(BASE)
        d["gaps"][0]["proof"]=True
        self.assertIn("GAP_SCHEMA_DRIFT:G001",validate(d))
    def test_extra_vector_runtime_claim_rejected(self):
        d=copy.deepcopy(BASE)
        d["vectors"][1]["runtime_approved"]=True
        self.assertIn("VECTOR_SCHEMA_DRIFT:F02",validate(d))
    def test_gap_owner_requires_canonical_producer(self):
        assert_reject(self,["gaps",10,"authority"],"Mapa","GAP_OWNER_TAMPER:G011")
    def test_vector_owner_cannot_shift_with_valid_repo_name(self):
        assert_reject(self,["vectors",6,"producer"],"Mapa","VECTOR_OWNER_TAMPER:F07")
    def test_graph_node_extra_confidence_rejected(self):
        d=copy.deepcopy(BASE)
        d["semantic_graph"]["nodes"][0]["confidence"]=1.0
        self.assertIn("NODE_SCHEMA_DRIFT",validate(d))
    def test_producer_node_ownership_cannot_be_reassigned(self):
        d=copy.deepcopy(BASE)
        d["semantic_graph"]["nodes"][1]["owner"]="RafGitTools"
        self.assertIn("PRODUCER_NODE_TAMPER:Mapa",validate(d))
    def test_edge_cannot_assert_causality(self):
        assert_reject(self,["semantic_graph","edges",0,"epistemic"],
            "PROVEN_CAUSAL","EDGE_FALSE_PROVENANCE_OR_CAUSALITY")
    def test_edge_cannot_invent_provider_provenance(self):
        assert_reject(self,["semantic_graph","edges",0,"provenance"],
            "SIGNED_PROVIDER_READBACK","EDGE_FALSE_PROVENANCE_OR_CAUSALITY")
    def test_edge_cannot_hide_approval_field(self):
        d=copy.deepcopy(BASE)
        d["semantic_graph"]["edges"][0]["approved"]=True
        self.assertIn("EDGE_SCHEMA_DRIFT",validate(d))
    def test_evidence_extra_promotion_field_rejected(self):
        d=copy.deepcopy(BASE)
        d["evidence_register"][0]["provider_success"]=True
        self.assertIn("EVIDENCE_SCHEMA_DRIFT",validate(d))
    def test_receipt_tamper_proof_field_rejected(self):
        d=copy.deepcopy(BASE)
        d["receipts"][0]["signature_valid"]=True
        self.assertIn("RECEIPT_SCHEMA_DRIFT",validate(d))
    def test_rollback_receipt_must_keep_action_scope(self):
        d=copy.deepcopy(BASE)
        d["receipts"][1]["signature_valid"]=True
        self.assertIn("RECEIPT_SCHEMA_DRIFT",validate(d))
    def test_promotion_extra_scope_rejected(self):
        d=copy.deepcopy(BASE)
        d["promotion"]["auto_promote"]=True
        self.assertIn("PROMOTION_SCHEMA_DRIFT",validate(d))

    def test_predecessor_is_not_deleted(self):
        assert_reject(self,["predecessor","relation"],"REPLACES_ERASES","LOSS_OF_PREDECESSOR")

if __name__=="__main__":
    unittest.main()
