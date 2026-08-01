from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "append_microcycle_index.py"
spec = importlib.util.spec_from_file_location("microcycle_index", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class MicrocycleAppendIndexTests(unittest.TestCase):
    def receipt(self, n: int, phase: str = "psi") -> dict:
        receipt = {
            "schema": module.RECEIPT_SCHEMA,
            "generated_at": f"2026-08-01T18:{n:02d}:00+00:00",
            "claim_allowed": False,
            "publication_ready": False,
            "automatic_mutation": False,
            "automatic_merge": False,
            "decision": "EXECUTED_READ_ONLY",
            "cycle": {
                "cycle_id": f"RAF-CYCLE-20260801T18{n:02d}00Z-N{n % 42:02d}",
                "n_mod_42": n % 42,
                "phase": phase,
            },
        }
        receipt["receipt_sha256"] = module.sha256_value(receipt)
        return receipt

    def kwargs(self, n: int = 1) -> dict[str, str]:
        return {
            "run_id": str(3000 + n),
            "run_attempt": "1",
            "run_url": f"https://github.com/example/repo/actions/runs/{3000 + n}",
            "repository": "example/repo",
            "head_branch": "main",
            "head_sha": f"{n:040x}",
            "artifact_name": f"rafaelia-adaptive-cycle-{3000 + n}",
        }

    def test_genesis_segment_is_hash_bound_and_non_promoting(self) -> None:
        index, operation = module.append_receipt(
            self.receipt(1),
            None,
            {"state": "TOKEN_VAZIO_NO_PREVIOUS_INDEX"},
            **self.kwargs(1),
        )
        self.assertEqual(operation, "APPENDED")
        self.assertEqual(index["entry_count"], 1)
        self.assertFalse(index["claim_allowed"])
        self.assertIsNone(index["entries"][0]["previous_entry_sha256"])
        module.validate_index(index)

    def test_second_receipt_extends_entry_and_index_chains(self) -> None:
        first, _ = module.append_receipt(
            self.receipt(1), None, {"state": "TOKEN_VAZIO_NO_PREVIOUS_INDEX"}, **self.kwargs(1)
        )
        second, _ = module.append_receipt(
            self.receipt(2, "chi"),
            first,
            {
                "state": "FOUND_VERIFIED_TRANSPORT",
                "artifact_id": 10,
                "run_id": 3001,
                "head_branch": "main",
            },
            **self.kwargs(2),
        )
        self.assertEqual(second["entry_count"], 2)
        self.assertEqual(
            second["entries"][1]["previous_entry_sha256"],
            second["entries"][0]["entry_sha256"],
        )
        self.assertEqual(second["previous_index_sha256"], first["index_sha256"])
        module.validate_index(second)

    def test_latest_four_is_derived_without_deleting_history(self) -> None:
        index = None
        for n, phase in zip(range(1, 7), ["psi", "chi", "rho", "delta", "sigma", "omega"]):
            index, _ = module.append_receipt(
                self.receipt(n, phase),
                index,
                {"state": "FOUND_VERIFIED_TRANSPORT" if index else "TOKEN_VAZIO_NO_PREVIOUS_INDEX"},
                **self.kwargs(n),
            )
        assert index is not None
        self.assertEqual(index["entry_count"], 6)
        self.assertEqual(index["latest_four"], index["entries"][-4:])
        self.assertEqual(len(index["entries"]), 6)

    def test_exact_duplicate_is_idempotent(self) -> None:
        receipt = self.receipt(3)
        first, _ = module.append_receipt(
            receipt, None, {"state": "TOKEN_VAZIO_NO_PREVIOUS_INDEX"}, **self.kwargs(3)
        )
        second, operation = module.append_receipt(
            receipt,
            first,
            {"state": "FOUND_VERIFIED_TRANSPORT"},
            **self.kwargs(4),
        )
        self.assertEqual(operation, "IDEMPOTENT_ALREADY_PRESENT")
        self.assertEqual(second["entry_count"], 1)

    def test_same_cycle_id_with_different_receipt_is_rejected(self) -> None:
        receipt = self.receipt(4)
        first, _ = module.append_receipt(
            receipt, None, {"state": "TOKEN_VAZIO_NO_PREVIOUS_INDEX"}, **self.kwargs(4)
        )
        altered = json.loads(json.dumps(receipt))
        altered["generated_at"] = "2026-08-01T19:00:00+00:00"
        altered["receipt_sha256"] = module.sha256_value(
            {key: value for key, value in altered.items() if key != "receipt_sha256"}
        )
        with self.assertRaises(module.MicrocycleIndexError):
            module.append_receipt(
                altered,
                first,
                {"state": "FOUND_VERIFIED_TRANSPORT"},
                **self.kwargs(5),
            )

    def test_tampered_previous_index_is_rejected(self) -> None:
        index, _ = module.append_receipt(
            self.receipt(5), None, {"state": "TOKEN_VAZIO_NO_PREVIOUS_INDEX"}, **self.kwargs(5)
        )
        tampered = json.loads(json.dumps(index))
        tampered["entries"][0]["phase"] = "omega"
        with self.assertRaises(module.MicrocycleIndexError):
            module.validate_index(tampered)

    def test_claim_promotion_in_receipt_is_rejected(self) -> None:
        receipt = self.receipt(6)
        receipt["claim_allowed"] = True
        receipt["receipt_sha256"] = module.sha256_value(
            {key: value for key, value in receipt.items() if key != "receipt_sha256"}
        )
        with self.assertRaises(module.MicrocycleIndexError):
            module.append_receipt(
                receipt, None, {"state": "TOKEN_VAZIO_NO_PREVIOUS_INDEX"}, **self.kwargs(6)
            )

    def test_markdown_exposes_four_runs_and_boundaries(self) -> None:
        index = None
        for n in range(1, 5):
            index, operation = module.append_receipt(
                self.receipt(n),
                index,
                {"state": "FOUND_VERIFIED_TRANSPORT" if index else "TOKEN_VAZIO_NO_PREVIOUS_INDEX"},
                **self.kwargs(n),
            )
        assert index is not None
        text = module.render_markdown(index, operation)
        self.assertIn("Four most recent indexed microcycles", text)
        self.assertIn("claim_allowed=false", text)
        self.assertIn("Artifact retention is not permanent archival storage", text)


if __name__ == "__main__":
    unittest.main()
