from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "scripts"))

from validate_claim_review_chain import (
    ChainValidationError,
    canonical_digest,
    load_json,
    validate_chain,
)

HEAD = Path("indices/CLAIM_CONTRADICTION_HEAD.json")
BATCHES = [
    "indices/claim_review_batches/CLAIM_REVIEW_BATCH_001_2026-07-20.json",
    "indices/claim_review_batches/CLAIM_REVIEW_BATCH_002_2026-07-20.json",
    "indices/claim_review_batches/CLAIM_REVIEW_BATCH_003_2026-07-21.json",
]
RESOLUTION = "indices/CLAIM_REVIEW_RESOLUTION_CC028.json"


class ClaimReviewChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.head = load_json(HEAD)

    def test_valid_chain_reaches_full_indexed_review(self):
        result = validate_chain(ROOT, copy.deepcopy(self.head))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["candidate_count"], 36)
        self.assertEqual(result["review_batch_count"], 3)
        self.assertEqual(result["review_decision_count"], 30)
        self.assertEqual(result["reviewed_safe_count"], 36)
        self.assertEqual(result["reviewed_blocking_count"], 0)
        self.assertEqual(result["token_vazio_count"], 0)
        self.assertEqual(result["review_completion_ratio"], 1.0)
        self.assertEqual(result["exact_absence_resolution_count"], 1)
        self.assertEqual(
            result["next_gate"],
            "OBSERVABLE_SCANNER_RECEIPT_AND_SCOPE_REFRESH",
        )
        self.assertFalse(result["portfolio_exit_criteria_met"])
        self.assertFalse(result["claim_allowed"])

    def _isolated_tree(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "indices" / "claim_review_batches").mkdir(parents=True)
        for relative in [
            "indices/CLAIM_CONTRADICTION_LEDGER.json",
            "indices/CLAIM_CONTRADICTION_HEAD.json",
            RESOLUTION,
            *BATCHES,
        ]:
            source = ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        return temp, root

    def _rewrite_json(self, path: Path, mutate) -> dict:
        data = json.loads(path.read_text(encoding="utf-8"))
        mutate(data)
        data["integrity"]["digest"] = canonical_digest(data)
        path.write_text(
            json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        return data

    def _rewrite_batch_and_head(self, root: Path, batch_index: int, mutate) -> dict:
        head_path = root / "indices/CLAIM_CONTRADICTION_HEAD.json"
        head = json.loads(head_path.read_text(encoding="utf-8"))
        ref = head["review_batches"][batch_index]
        batch_path = root / ref["path"]
        batch = self._rewrite_json(batch_path, mutate)
        ref["digest_blake2b_256"] = batch["integrity"]["digest"]
        ref["decision_count"] = len(batch["decisions"])
        head["integrity"]["digest"] = canonical_digest(head)
        return head

    def test_base_ledger_digest_drift_rejected(self):
        head = copy.deepcopy(self.head)
        head["base_ledger"]["digest_blake2b_256"] = "0" * 64
        head["integrity"]["digest"] = canonical_digest(head)
        with self.assertRaises(ChainValidationError):
            validate_chain(ROOT, head)

    def test_duplicate_batch_reference_rejected(self):
        head = copy.deepcopy(self.head)
        head["review_batches"].append(copy.deepcopy(head["review_batches"][0]))
        head["derived"]["review_batch_count"] = 4
        head["integrity"]["digest"] = canonical_digest(head)
        with self.assertRaises(ChainValidationError):
            validate_chain(ROOT, head)

    def test_resolution_blob_identity_drift_rejected(self):
        temp, root = self._isolated_tree()
        try:
            resolution_path = root / RESOLUTION
            resolution = self._rewrite_json(
                resolution_path,
                lambda data: data["materialization"].__setitem__("git_blob_sha1", "0" * 40),
            )
            head = json.loads((root / HEAD).read_text(encoding="utf-8"))
            ref = head["review_batches"][2]
            batch_path = root / ref["path"]
            batch = json.loads(batch_path.read_text(encoding="utf-8"))
            batch["materialization_receipt"]["digest_blake2b_256"] = resolution["integrity"]["digest"]
            batch["integrity"]["digest"] = canonical_digest(batch)
            batch_path.write_text(json.dumps(batch, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            ref["digest_blake2b_256"] = batch["integrity"]["digest"]
            head["integrity"]["digest"] = canonical_digest(head)
            with self.assertRaises(ChainValidationError):
                validate_chain(root, head)
        finally:
            temp.cleanup()

    def test_resolution_size_tampering_rejected(self):
        temp, root = self._isolated_tree()
        try:
            resolution_path = root / RESOLUTION
            resolution = self._rewrite_json(
                resolution_path,
                lambda data: data["materialization"].__setitem__("decoded_size_bytes", 1),
            )
            head = json.loads((root / HEAD).read_text(encoding="utf-8"))
            ref = head["review_batches"][2]
            batch_path = root / ref["path"]
            batch = json.loads(batch_path.read_text(encoding="utf-8"))
            batch["materialization_receipt"]["digest_blake2b_256"] = resolution["integrity"]["digest"]
            batch["integrity"]["digest"] = canonical_digest(batch)
            batch_path.write_text(json.dumps(batch, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            ref["digest_blake2b_256"] = batch["integrity"]["digest"]
            head["integrity"]["digest"] = canonical_digest(head)
            with self.assertRaises(ChainValidationError):
                validate_chain(root, head)
        finally:
            temp.cleanup()

    def test_resolution_exact_token_tampering_rejected(self):
        temp, root = self._isolated_tree()
        try:
            resolution_path = root / RESOLUTION
            resolution = self._rewrite_json(
                resolution_path,
                lambda data: data["token_scan"]["strong_token_counts"].__setitem__("COMPLETE", 1),
            )
            head = json.loads((root / HEAD).read_text(encoding="utf-8"))
            ref = head["review_batches"][2]
            batch_path = root / ref["path"]
            batch = json.loads(batch_path.read_text(encoding="utf-8"))
            batch["materialization_receipt"]["digest_blake2b_256"] = resolution["integrity"]["digest"]
            batch["integrity"]["digest"] = canonical_digest(batch)
            batch_path.write_text(json.dumps(batch, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            ref["digest_blake2b_256"] = batch["integrity"]["digest"]
            head["integrity"]["digest"] = canonical_digest(head)
            with self.assertRaises(ChainValidationError):
                validate_chain(root, head)
        finally:
            temp.cleanup()

    def test_resolution_receipt_digest_drift_rejected(self):
        temp, root = self._isolated_tree()
        try:
            head = self._rewrite_batch_and_head(
                root,
                2,
                lambda batch: batch["materialization_receipt"].__setitem__(
                    "digest_blake2b_256", "0" * 64
                ),
            )
            with self.assertRaises(ChainValidationError):
                validate_chain(root, head)
        finally:
            temp.cleanup()

    def test_duplicate_entry_transition_rejected(self):
        temp, root = self._isolated_tree()
        try:
            def mutate(batch):
                batch["decisions"].append(copy.deepcopy(batch["decisions"][0]))
                batch["derived"]["decision_count"] += 1
                batch["derived"]["safe_transitions"] += 1
            head = self._rewrite_batch_and_head(root, 2, mutate)
            with self.assertRaises(ChainValidationError):
                validate_chain(root, head)
        finally:
            temp.cleanup()

    def test_resulting_count_tampering_rejected(self):
        temp, root = self._isolated_tree()
        try:
            head = self._rewrite_batch_and_head(
                root,
                2,
                lambda batch: batch["derived"].__setitem__("result_token_vazio_count", 1),
            )
            with self.assertRaises(ChainValidationError):
                validate_chain(root, head)
        finally:
            temp.cleanup()

    def test_stale_next_gate_rejected(self):
        head = copy.deepcopy(self.head)
        head["derived"]["next_gate"] = "MATERIALIZE_FULL_CC028_AND_OBSERVABLE_SCANNER_RECEIPT"
        head["integrity"]["digest"] = canonical_digest(head)
        with self.assertRaises(ChainValidationError):
            validate_chain(ROOT, head)

    def test_head_promotion_rejected(self):
        head = copy.deepcopy(self.head)
        head["derived"]["claim_allowed"] = True
        head["integrity"]["digest"] = canonical_digest(head)
        with self.assertRaises(ChainValidationError):
            validate_chain(ROOT, head)

    def test_head_integrity_tampering_rejected(self):
        head = copy.deepcopy(self.head)
        head["derived"]["next_gate"] = "SILENT_PROMOTION"
        with self.assertRaises(ChainValidationError):
            validate_chain(ROOT, head)


if __name__ == "__main__":
    unittest.main()
