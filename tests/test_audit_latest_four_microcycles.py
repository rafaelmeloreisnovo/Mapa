from __future__ import annotations

import copy
import unittest

from scripts.append_microcycle_index import MicrocycleIndexError, sha256_value
from scripts.audit_latest_four_microcycles import build_audit


PHASES = ["chi", "delta", "omega", "chi"]


def make_index(count: int = 4) -> dict:
    entries = []
    previous = None
    for i in range(count):
        entry = {
            "cycle_id": f"RAF-CYCLE-TEST-{i}",
            "generated_at": f"2026-08-16T00:0{i}:00+00:00",
            "n_mod_42": 1 + (2 * i),
            "phase": PHASES[i % len(PHASES)],
            "decision": "EXECUTED_READ_ONLY",
            "claim_allowed": False,
            "receipt_sha256": f"{i + 1:064x}",
            "run_id": str(1000 + i),
            "run_attempt": "1",
            "run_url": f"https://example.invalid/runs/{1000 + i}",
            "repository": "rafaelmeloreisnovo/Mapa",
            "head_branch": "main",
            "head_sha": "a" * 40,
            "artifact_name": f"rafaelia-adaptive-cycle-{1000 + i}",
            "previous_entry_sha256": previous,
        }
        entry["entry_sha256"] = sha256_value(entry)
        previous = entry["entry_sha256"]
        entries.append(entry)

    index = {
        "schema": "rafaelia.microcycle-index.v1",
        "segment_id": "SEGMENT-TEST",
        "generated_at": "2026-08-16T00:04:00+00:00",
        "source_mode": "ARTIFACT_APPEND_ONLY",
        "claim_allowed": False,
        "automatic_mutation": False,
        "automatic_merge": False,
        "entry_count": len(entries),
        "entries": entries,
        "latest_four": entries[-4:],
        "previous_index_sha256": None,
        "continuity": {"state": "FOUND_IMMUTABLE_CACHE"},
        "boundaries": {"claim_allowed": False},
    }
    index["index_sha256"] = sha256_value(index)
    return index


class LatestFourAuditTests(unittest.TestCase):
    def test_projects_required_fields_and_preserves_non_promotion(self) -> None:
        audit = build_audit(make_index())
        self.assertEqual(audit["latest_four_count"], 4)
        self.assertEqual(audit["decision"], "VERIFIED_LATEST_FOUR_READ_ONLY")
        self.assertIs(audit["claim_allowed"], False)
        self.assertEqual([row["n_mod_42"] for row in audit["entries"]], [1, 3, 5, 7])
        self.assertTrue(all(row["claim_allowed"] is False for row in audit["entries"]))
        self.assertEqual(
            audit["entries"][1]["previous_entry_sha256"],
            audit["entries"][0]["entry_sha256"],
        )

    def test_rejects_claim_promotion(self) -> None:
        index = make_index()
        index["entries"][-1]["claim_allowed"] = True
        with self.assertRaises(MicrocycleIndexError):
            build_audit(index)

    def test_requires_four_after_history_is_established(self) -> None:
        with self.assertRaisesRegex(MicrocycleIndexError, "latest_four_count must be 4"):
            build_audit(make_index(3))

    def test_rejects_broken_predecessor_chain(self) -> None:
        index = make_index()
        broken = copy.deepcopy(index)
        broken["entries"][2]["previous_entry_sha256"] = "f" * 64
        broken["entries"][2].pop("entry_sha256")
        broken["entries"][2]["entry_sha256"] = sha256_value(broken["entries"][2])
        with self.assertRaises(MicrocycleIndexError):
            build_audit(broken)


if __name__ == "__main__":
    unittest.main()
