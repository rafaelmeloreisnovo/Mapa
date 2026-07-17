#!/usr/bin/env python3
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from validate_repository_inventory import canonical_digest, validate_inventory

class InventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path=Path("indices/REPOSITORY_INVENTORY.json")
        cls.base=json.loads(cls.path.read_text(encoding="utf-8"))

    def reseal(self,d): d["integrity"]["digest"]=canonical_digest(d)
    def errors(self,d): return validate_inventory(d)

    def test_current_partial_snapshot_is_structurally_valid(self):
        self.assertEqual(self.errors(self.base),[])
        self.assertEqual(self.base["scope"]["state"],"PARTIAL")
        self.assertFalse(self.base["scope"]["claim_allowed"])

    def test_counts_are_exactly_derived(self):
        d=copy.deepcopy(self.base); d["statistics"]["public_count"]+=1; self.reseal(d)
        self.assertTrue(any("public_count mismatch" in e for e in self.errors(d)))

    def test_declared_materialized_count_cannot_differ(self):
        d=copy.deepcopy(self.base); d["scope"]["materialized_count"]=126; self.reseal(d)
        self.assertTrue(any("materialized_count mismatch" in e for e in self.errors(d)))

    def test_duplicate_repository_id_is_blocked(self):
        d=copy.deepcopy(self.base); d["repositories"][1]["repository_id"]=d["repositories"][0]["repository_id"]; self.reseal(d)
        self.assertTrue(any("duplicate repository_id" in e for e in self.errors(d)))

    def test_owner_name_identity_is_blocked(self):
        d=copy.deepcopy(self.base); d["repositories"][0]["owner"]="rafaelmeloreisnovo"; self.reseal(d)
        self.assertTrue(any("does not match owner/name" in e for e in self.errors(d)))

    def test_canonical_clone_url_is_required(self):
        d=copy.deepcopy(self.base); d["repositories"][0]["clone_url"]="https://example.invalid/x"; self.reseal(d)
        self.assertTrue(any("clone_url is not canonical" in e for e in self.errors(d)))

    def test_partial_cannot_promote_claim(self):
        d=copy.deepcopy(self.base); d["scope"]["claim_allowed"]=True; self.reseal(d)
        self.assertTrue(any("claim_allowed=false" in e for e in self.errors(d)))

    def test_complete_requires_all_records(self):
        d=copy.deepcopy(self.base); d["scope"]["state"]="COMPLETE"; self.reseal(d)
        self.assertTrue(any("all accessible records" in e for e in self.errors(d)))

    def test_absence_ledger_is_non_optional(self):
        d=copy.deepcopy(self.base); d["absence_ledger"]["exit_criteria"]=""; self.reseal(d)
        self.assertTrue(any("exit_criteria" in e for e in self.errors(d)))

    def test_tampering_without_reseal_is_blocked(self):
        d=copy.deepcopy(self.base); d["repositories"][0]["size_kib"]+=1
        self.assertTrue(any("digest mismatch" in e for e in self.errors(d)))

    def test_size_unit_is_kib_and_non_negative(self):
        d=copy.deepcopy(self.base); d["repositories"][0]["size_kib"]=-1; self.reseal(d)
        self.assertTrue(any("size_kib" in e for e in self.errors(d)))

    def test_scope_account_counts_sum_to_accessible_total(self):
        d=copy.deepcopy(self.base); d["scope"]["included_accounts"][0]["accessible_count_observed"]-=1; self.reseal(d)
        self.assertTrue(any("accessible total" in e for e in self.errors(d)))

if __name__=="__main__": unittest.main(verbosity=2)
