#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "verify_promotion_control.py"
SPEC = importlib.util.spec_from_file_location("verify_promotion_control", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

POLICY = json.loads(
    (ROOT / "data" / "control-plane" / "promotion-control.v1.json").read_text(encoding="utf-8")
)


def event(
    *,
    body: str = "",
    draft: bool = False,
    auto_merge=None,
    state: str = "open",
    merged: bool = False,
    author: str = "author",
):
    return {
        "pull_request": {
            "state": state,
            "draft": draft,
            "merged": merged,
            "auto_merge": auto_merge,
            "body": body,
            "user": {"login": author},
        }
    }


def review(login: str, state: str):
    return {"user": {"login": login}, "state": state}


class PromotionControlTests(unittest.TestCase):
    def test_draft_is_denied(self):
        result = MODULE.evaluate(event(draft=True), [], POLICY)
        self.assertEqual(result["result"], "DENIED")
        self.assertIn("PULL_REQUEST_DRAFT_OR_UNKNOWN", result["blocking_reasons"])

    def test_explicit_do_not_merge_is_denied(self):
        result = MODULE.evaluate(event(body="Não mesclar antes do receipt físico."), [], POLICY)
        self.assertIn("EXPLICIT_BODY_DENIAL", result["blocking_reasons"])

    def test_ready_for_graph_false_is_denied(self):
        result = MODULE.evaluate(event(body="READY_FOR_GRAPH=false"), [], POLICY)
        self.assertIn("EXPLICIT_BODY_DENIAL", result["blocking_reasons"])

    def test_required_review_without_approval_is_denied(self):
        result = MODULE.evaluate(
            event(body="human_review_required=true"),
            [review("reviewer", "COMMENTED")],
            POLICY,
        )
        self.assertIn("HUMAN_REVIEW_MISSING", result["blocking_reasons"])

    def test_author_approval_does_not_count(self):
        result = MODULE.evaluate(
            event(body="human_review_required=true", author="rafael"),
            [review("rafael", "APPROVED")],
            POLICY,
        )
        self.assertEqual(result["observed_independent_approvals"], 0)
        self.assertIn("HUMAN_REVIEW_MISSING", result["blocking_reasons"])

    def test_latest_review_state_wins(self):
        result = MODULE.evaluate(
            event(body="human_review_required=true"),
            [review("reviewer", "APPROVED"), review("reviewer", "CHANGES_REQUESTED")],
            POLICY,
        )
        self.assertEqual(result["observed_independent_approvals"], 0)
        self.assertIn("HUMAN_REVIEW_MISSING", result["blocking_reasons"])

    def test_auto_merge_enabled_is_denied(self):
        result = MODULE.evaluate(event(auto_merge={"enabled_by": {"login": "author"}}), [], POLICY)
        self.assertIn("AUTO_MERGE_ENABLED", result["blocking_reasons"])

    def test_clean_pr_with_independent_approval_is_allowed(self):
        result = MODULE.evaluate(
            event(body="human_review_required=true"),
            [review("reviewer", "APPROVED")],
            POLICY,
        )
        self.assertEqual(result["result"], "ALLOWED_FOR_MANUAL_MERGE")
        self.assertEqual(result["approved_by"], ["reviewer"])
        self.assertFalse(result["automatic_merge"])
        self.assertFalse(result["claim_allowed"])


if __name__ == "__main__":
    unittest.main()
