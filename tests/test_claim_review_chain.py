from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_claim_review_chain import (
    ChainValidationError,
    canonical_digest,
    load_json,
    validate_chain,
)

ROOT = Path.cwd()
HEAD = Path("indices/CLAIM_CONTRADICTION_HEAD.json")


class ClaimReviewChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.head = load_json(HEAD)

    def test_valid_chain(self):
        result = validate_chain(ROOT, copy.deepcopy(self.head))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["candidate_count"], 36)
        self.assertEqual(result["reviewed_safe_count"], 20)
        self.assertEqual(result["token_vazio_count"], 16)
        self.assertEqual(result["review_completion_ratio"], 0.555555555556)
        self.assertFalse(result["portfolio_exit_criteria_met"])

    def _isolated_tree(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "indices" / "claim_review_batches").mkdir(parents=True)
        for relative in [
            "indices/CLAIM_CONTRADICTION_LEDGER.json",
            "indices/CLAIM_CONTRADICTION_HEAD.json",
            "indices/claim_review_batches/CLAIM_REVIEW_BATCH_001_2026-07-20.json",
        ]:
            source = ROOT / relative
            target = root / relative
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        return temp, root

    def test_base_ledger_digest_drift_rejected(self):
        head = copy.deepcopy(self.head)
        head["base_ledger"]["digest_blake2b_256"] = "0" * 64
        head["integrity"]["digest"] = canonical_digest(head)
        with self.assertRaises(ChainValidationError):
            validate_chain(ROOT, head)

    def test_duplicate_batch_reference_rejected(self):
        head = copy.deepcopy(self.head)
        head["review_batches"].append(copy.deepcopy(head["review_batches"][0]))
        head["derived"]["review_batch_count"] = 2
        head["integrity"]["digest"] = canonical_digest(head)
        with self.assertRaises(ChainValidationError):
            validate_chain(ROOT, head)

    def test_batch_digest_reference_drift_rejected(self):
        head = copy.deepcopy(self.head)
        head["review_batches"][0]["digest_blake2b_256"] = "0" * 64
        head["integrity"]["digest"] = canonical_digest(head)
        with self.assertRaises(ChainValidationError):
            validate_chain(ROOT, head)

    def test_automatic_dismissal_rejected(self):
        head = copy.deepcopy(self.head)
        head["boundaries"]["automatic_dismissal"] = True
        head["integrity"]["digest"] = canonical_digest(head)
        with self.assertRaises(ChainValidationError):
            validate_chain(ROOT, head)

    def test_head_promotion_rejected(self):
        head = copy.deepcopy(self.head)
        head["derived"]["claim_allowed"] = True
        head["integrity"]["digest"] = canonical_digest(head)
        with self.assertRaises(ChainValidationError):
            validate_chain(ROOT, head)

    def test_batch_transition_path_mismatch_rejected(self):
        temp, root = self._isolated_tree()
        try:
            batch_path = root / "indices/claim_review_batches/CLAIM_REVIEW_BATCH_001_2026-07-20.json"
            batch = json.loads(batch_path.read_text(encoding="utf-8"))
            batch["decisions"][0]["path"] = "wrong/path.md"
            batch["integrity"]["digest"] = canonical_digest(batch)
            batch_path.write_text(json.dumps(batch, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            head_path = root / "indices/CLAIM_CONTRADICTION_HEAD.json"
            head = json.loads(head_path.read_text(encoding="utf-8"))
            head["review_batches"][0]["digest_blake2b_256"] = batch["integrity"]["digest"]
            head["integrity"]["digest"] = canonical_digest(head)
            with self.assertRaises(ChainValidationError):
                validate_chain(root, head)
        finally:
            temp.cleanup()

    def test_batch_evidence_commit_mismatch_rejected(self):
        temp, root = self._isolated_tree()
        try:
            batch_path = root / "indices/claim_review_batches/CLAIM_REVIEW_BATCH_001_2026-07-20.json"
            batch = json.loads(batch_path.read_text(encoding="utf-8"))
            decision = batch["decisions"][0]
            decision["evidence_pointer"] = decision["path"] + "@" + "0" * 40
            batch["integrity"]["digest"] = canonical_digest(batch)
            batch_path.write_text(json.dumps(batch, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            head = load_json(root / "indices/CLAIM_CONTRADICTION_HEAD.json")
            head["review_batches"][0]["digest_blake2b_256"] = batch["integrity"]["digest"]
            head["integrity"]["digest"] = canonical_digest(head)
            with self.assertRaises(ChainValidationError):
                validate_chain(root, head)
        finally:
            temp.cleanup()

    def test_duplicate_entry_transition_rejected(self):
        temp, root = self._isolated_tree()
        try:
            batch_path = root / "indices/claim_review_batches/CLAIM_REVIEW_BATCH_001_2026-07-20.json"
            batch = json.loads(batch_path.read_text(encoding="utf-8"))
            batch["decisions"].append(copy.deepcopy(batch["decisions"][0]))
            batch["derived"]["decision_count"] += 1
            batch["derived"]["safe_transitions"] += 1
            batch["integrity"]["digest"] = canonical_digest(batch)
            batch_path.write_text(json.dumps(batch, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            head = load_json(root / "indices/CLAIM_CONTRADICTION_HEAD.json")
            head["review_batches"][0]["digest_blake2b_256"] = batch["integrity"]["digest"]
            head["review_batches"][0]["decision_count"] += 1
            head["integrity"]["digest"] = canonical_digest(head)
            with self.assertRaises(ChainValidationError):
                validate_chain(root, head)
        finally:
            temp.cleanup()

    def test_weak_rationale_rejected(self):
        temp, root = self._isolated_tree()
        try:
            batch_path = root / "indices/claim_review_batches/CLAIM_REVIEW_BATCH_001_2026-07-20.json"
            batch = json.loads(batch_path.read_text(encoding="utf-8"))
            batch["decisions"][0]["rationale"] = "safe"
            batch["integrity"]["digest"] = canonical_digest(batch)
            batch_path.write_text(json.dumps(batch, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            head = load_json(root / "indices/CLAIM_CONTRADICTION_HEAD.json")
            head["review_batches"][0]["digest_blake2b_256"] = batch["integrity"]["digest"]
            head["integrity"]["digest"] = canonical_digest(head)
            with self.assertRaises(ChainValidationError):
                validate_chain(root, head)
        finally:
            temp.cleanup()

    def test_head_integrity_tampering_rejected(self):
        head = copy.deepcopy(self.head)
        head["derived"]["next_gate"] = "SILENT_PROMOTION"
        with self.assertRaises(ChainValidationError):
            validate_chain(ROOT, head)


if __name__ == "__main__":
    unittest.main()
