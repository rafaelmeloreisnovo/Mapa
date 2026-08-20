#!/usr/bin/env python3
"""Rafaelia 15-invariant validator compatibility hardening V2.

Preserves the original 15 checks while making I1 deterministic and explicitly
schema-aware for commit-bound receipts. Historical receipts are not rewritten.

This does not claim exhaustive receipt immutability coverage: I1 remains a
bounded deterministic sample, and the result says so explicitly.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Tuple

from check_invariants import InvariantsValidator


SHA40 = re.compile(r"^[0-9a-fA-F]{40}$")


class InvariantsValidatorV2(InvariantsValidator):
    """Compatibility-hardened validator without mutating historical receipts."""

    def i1_immutable_source(self) -> Tuple[bool, str]:
        try:
            receipts_dir = self.repo_root / "data" / "receipts"
            if not receipts_dir.exists():
                return False, "Receipt directory not found"

            receipt_files = sorted(receipts_dir.glob("*.json"), key=lambda p: p.name)
            if not receipt_files:
                return False, "No receipt files found"

            marker_keys = {
                "entry_sha256",
                "previous_entry_sha256",
                "observed_at_utc",
                "observed_at",
                "receipt_id",
                "manifest_git_blob_sha1",
                "manifest_commit_sha",
                "cycle_id",
                "chain_continuity",
                "created_at",
                "event_id",
                "timestamp",
                "head_sha",
                "base_sha",
                "merge_commit_sha",
                "source_sha",
                "commit_sha",
                "blob_sha",
            }
            sha_keys = {
                "manifest_git_blob_sha1",
                "manifest_commit_sha",
                "head_sha",
                "base_sha",
                "merge_commit_sha",
                "source_sha",
                "commit_sha",
                "blob_sha",
            }

            sample = receipt_files[:3]
            for receipt in sample:
                try:
                    data = json.loads(receipt.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as exc:
                    return False, f"Receipt {receipt.name} unreadable/invalid JSON: {exc}"

                present = [key for key in marker_keys if key in data and data[key] not in (None, "", [], {})]
                if not present:
                    return False, f"Receipt {receipt.name} missing immutability marker"

                sha_present = [key for key in present if key in sha_keys]
                for key in sha_present:
                    value = data[key]
                    if isinstance(value, str) and not SHA40.fullmatch(value):
                        return False, f"Receipt {receipt.name} has malformed {key}"

            return True, (
                f"✓ deterministic bounded sample {len(sample)}/{len(receipt_files)} receipts "
                "has schema-aware immutability markers"
            )
        except Exception as exc:
            return False, f"I1 check error: {exc}"

    def save_results(self):
        audit_file = super().save_results()
        data = json.loads(audit_file.read_text(encoding="utf-8"))
        data["tool"] = "check_invariants_v2.py"
        data["i1_scope"] = "DETERMINISTIC_BOUNDED_SAMPLE_NOT_EXHAUSTIVE"
        audit_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return audit_file


def main() -> int:
    validator = InvariantsValidatorV2()
    success = validator.run_all_checks()
    validator.save_results()

    passed = sum(1 for result in validator.results.values() if result["status"] == "PASS")
    failed = sum(1 for result in validator.results.values() if result["status"] == "FAIL")
    print("\n" + "=" * 60)
    print(f"Invariants Validation V2: {'PASS' if success else 'FAIL'}")
    print(f"Passed: {passed}/15")
    print(f"Failed: {failed}/15")
    print("I1 scope: deterministic bounded sample, not exhaustive coverage")
    print("Results saved to: data/audits/invariants-validation.json")
    print("=" * 60)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
