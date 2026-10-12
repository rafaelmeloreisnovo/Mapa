"""Adversarial tests for sanitized NOVOexport chart and route metadata (not raw files)."""
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from validate_novoexport_chart_routes_v1 import SOURCE,validate
BASE=json.loads(SOURCE.read_text("utf-8"))

def mutant(changes, item=None):
    v=copy.deepcopy(BASE)
    if item is not None:
        r=next(x for x in v["entries"] if x["id"]==item)
        r.update(changes)
    else:
        v.update(changes)
    return v

class ChartRouteFalsification(unittest.TestCase):
    def test_scoped_baseline(self):
        self.assertEqual([],validate(BASE))
    def test_all_global_claims_blocked(self):
        for key,value in [
            ("claim_allowed",True),("all_claims_blocked",False),
            ("raw_private_payload_included",True),("all_chart_data_ingested",True),
            ("live_provider_provenance_verified",True)]:
            with self.subTest(key=key):
                self.assertTrue(validate(mutant({key:value})))
    def test_covered_shards_are_not_semantically_scanned(self):
        v=mutant({})
        v["observed_novo_baseline"]["state"]="EXHAUSTIVE_RECOUNT_PASS"
        self.assertIn("BASELINE_AS_LIVE_SCAN",validate(v))
    def test_role_input_is_not_assistant_output(self):
        v=mutant({})
        v["boundaries"]["role_input_not_assistant_output"]=False
        self.assertIn("INVARIANT_DOWNGRADE",validate(v))
    def test_collision_42_not_icosphere_identity(self):
        v=mutant({})
        v["formal_fixtures"]["C42pm6pm7"]["edges"]=120
        self.assertIn("Z42_ICOSPHERE_COLLISION",validate(v))
    def test_template_cache_not_cosmology(self):
        v=mutant({})
        v["observed_chart_cache"]["specific_dataset"]="DESI_DR2"
        self.assertIn("OFFICE_TEMPLATE_MISPROMOTION",validate(v))
    def test_template_is_not_measurement(self):
        self.assertTrue(any("MATERIAL_DOMAIN_DRIFT" in x for x in
            validate(mutant({"chart_role":"REAL_MEASUREMENT"},item="OFFICE_CHART1_6"))))
    def test_rll_figure_does_not_evidence_posterior(self):
        self.assertIn("RLL_QUANTITATIVE_UNVERIFIED",
            validate(mutant({"state":"SCIENTIFICALLY_VALIDATED"},item="RLL_QUANTITATIVE_F2_F10")))
    def test_rapport_not_evidence(self):
        v=mutant({})
        v["boundaries"]["rapport_evidence_weight_zero"]=False
        self.assertIn("INVARIANT_DOWNGRADE",validate(v))
    def test_private_drive_links_cannot_leak_into_manifest(self):
        v=mutant({"source_alias":"https://drive.google.com/private"},item="SOURCE_ARTIFACT_RECON")
        self.assertTrue(any("PRIVATE_LINK_IN_PUBLIC_CATALOG" in x for x in validate(v)))
    def test_no_missing_entries(self):
        v=mutant({})
        v["entries"].pop()
        self.assertIn("ENTRY_COUNT",validate(v))
    def test_no_shallow_fake_approval(self):
        v=mutant({})
        v["entries"][2]["approval"]="PASS"
        self.assertIn("ENTRY_2:SCHEMA",validate(v))
    def test_no_inappropriate_authority(self):
        v=mutant({})
        v["roles"]["RafPolimata"]="REVIEWER_AND_PROVIDER_AUTHORITY"
        self.assertIn("PRODUCER_AUTHORITY_DRIFT",validate(v))
    def test_unknown_entry_cannot_be_silent(self):
        v=mutant({"id":"UNRECORDED_OUTPUT"},item="Z42_CIRCULANT")
        self.assertTrue(any("IDENTITY" in x for x in validate(v)))
    def test_no_external_code_transplant(self):
        v=mutant({})
        v["boundaries"]["no_external_code_transplant"]=False
        self.assertIn("INVARIANT_DOWNGRADE",validate(v))
    def test_chart_has_no_unbound_workbook_promotions(self):
        v=mutant({})
        v["observed_chart_cache"]["source_workbook"]="Sheet1_PROVEN"
        self.assertIn("OFFICE_TEMPLATE_MISPROMOTION",validate(v))
    def test_invalid_root(self):
        self.assertEqual(["ROOT_NOT_OBJECT"],validate(None))

if __name__=="__main__":
    unittest.main()
