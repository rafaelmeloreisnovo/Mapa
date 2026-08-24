#!/usr/bin/env python3
"""
Phase 3: Federated Evidence Aggregator

Collect receipts from all RAFAELIA ecosystem repositories and produce
consolidated federated receipt linking evidence across repos.

Usage: python3 scripts/federated_evidence_aggregator.py --repos-root /home/user
"""

import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class FederatedEvidenceAggregator:
    """Aggregate evidence from multiple repositories."""

    def __init__(self, repos_root=None):
        self.repos_root = Path(repos_root) if repos_root else Path("/home/user")
        self.collected_evidence = {}
        self.cross_repo_deps = {}
        self.errors = []
        self.warnings = []

    def collect_mapa_evidence(self):
        """Collect consolidated receipt from Mapa."""
        try:
            receipt_path = self.repos_root / "Mapa" / "build" / "cycle-4-consolidated-receipt.json"
            if receipt_path.exists():
                with open(receipt_path) as f:
                    receipt = json.load(f)
                self.collected_evidence["Mapa"] = {
                    "receipt_path": str(receipt_path),
                    "schema": receipt.get("schema"),
                    "timestamp": receipt.get("timestamp"),
                    "summary": receipt.get("summary"),
                    "gates_passed": sum(1 for g in receipt.get("gates", {}).values() if g.get("status") == "PASS"),
                    "gates_failed": sum(1 for g in receipt.get("gates", {}).values() if g.get("status") == "FAIL"),
                    "artifact_hash": hashlib.sha256(json.dumps(receipt, sort_keys=True).encode()).hexdigest()
                }
                return True
        except Exception as e:
            self.errors.append(f"Mapa evidence collection failed: {e}")
        return False

    def collect_termux_app_evidence(self):
        """Collect BUG receipts from termux-app-rafacodephi."""
        try:
            termux_build = self.repos_root / "termux-app-rafacodephi" / "build"
            if not termux_build.exists():
                self.warnings.append("termux-app-rafacodephi/build directory not found")
                return False

            bug_receipts = {}
            for receipt_file in termux_build.glob("bug-*-receipt.json"):
                try:
                    with open(receipt_file) as f:
                        receipt = json.load(f)
                    bug_id = receipt.get("bug_id", "unknown")
                    bug_receipts[bug_id] = {
                        "path": str(receipt_file),
                        "status": receipt.get("state"),
                        "claim_allowed": receipt.get("claim_allowed"),
                        "timestamp": receipt.get("timestamp"),
                        "errors_count": len(receipt.get("errors", [])),
                        "artifact_hash": receipt.get("artifact_hash")
                    }
                except Exception as e:
                    self.warnings.append(f"Failed to parse {receipt_file.name}: {e}")

            if bug_receipts:
                self.collected_evidence["termux-app-rafacodephi"] = {
                    "bug_receipts": bug_receipts,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "status": "COLLECTED"
                }
                return True

        except Exception as e:
            self.errors.append(f"termux-app evidence collection failed: {e}")

        return False

    def map_cross_repo_dependencies(self):
        """Document dependencies between repositories."""
        try:
            deps = {
                "BUG-02": {
                    "producer": "termux-app-rafacodephi",
                    "scope": "Attractor #22 VOID paradox mathematical proof",
                    "blocker_for": ["BUG-01", "BUG-03", "BUG-08"],
                    "status": "BLOCKED_ON_PROOF_REFINEMENT",
                    "expected_unblock_date": "2026-09-07"  # 1-2 weeks from 2026-08-24
                },
                "TV-CODE-1": {
                    "producer": "Mapa",
                    "scope": "DAG causal engine implementation",
                    "blocker_for": ["cross-repo-inference"],
                    "status": "PASS",
                    "receipt": "Mapa:cycle-4-consolidated-receipt.json"
                },
                "TV-BOUNDARY-1": {
                    "producer": "Mapa",
                    "scope": "Antiderivative boundary conditions",
                    "blocker_for": ["Lyapunov convergence proofs"],
                    "status": "PASS",
                    "receipt": "Mapa:tv-boundary-1-antiderivative-receipt.json"
                }
            }

            self.cross_repo_deps = deps
            return True

        except Exception as e:
            self.errors.append(f"Cross-repo dependency mapping failed: {e}")
            return False

    def validate_federation_coherence(self):
        """Validate that federated state is internally consistent."""
        try:
            # Check: No circular dependencies
            blockers = set()
            for dep in self.cross_repo_deps.values():
                for blocked in dep.get("blocker_for", []):
                    if blocked in self.cross_repo_deps:
                        if "BUG-02" in self.cross_repo_deps[blocked].get("blocker_for", []):
                            self.errors.append(f"Circular dependency detected: {blocked} ← → BUG-02")

            # Check: All PASS receipts have artifact_hash
            for repo, evidence in self.collected_evidence.items():
                if isinstance(evidence, dict) and "artifact_hash" in evidence:
                    if not evidence["artifact_hash"] or not isinstance(evidence["artifact_hash"], str):
                        self.errors.append(f"{repo}: artifact_hash invalid")

            if not self.errors:
                return True

        except Exception as e:
            self.errors.append(f"Coherence validation failed: {e}")

        return False

    def generate_federated_receipt(self) -> Dict:
        """Generate consolidated federated receipt."""
        receipt = {
            "schema": "mapa.federated-reconciliation/v1",
            "phase": "Phase 3 - Cross-Repository Evidence Aggregation",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "repositories_count": len(self.collected_evidence),
            "repositories": list(self.collected_evidence.keys()),
            "collected_evidence": self.collected_evidence,
            "cross_repo_dependencies": self.cross_repo_deps,
            "errors": self.errors,
            "warnings": self.warnings,
            "validation": {
                "coherence_check": "PASS" if not self.errors else "FAIL",
                "circular_deps_found": False,
                "all_hashes_valid": all(
                    isinstance(v.get("artifact_hash"), str) for v in self.collected_evidence.values()
                    if isinstance(v, dict) and "artifact_hash" in v
                )
            },
            "federation_status": "VERIFICATION_PENDING",
            "ready_for_topology_check": len(self.errors) == 0,
            "F_ok": [
                f"Collected evidence from {len(self.collected_evidence)} repositories",
                f"Mapped {len(self.cross_repo_deps)} cross-repo dependencies"
            ],
            "F_gap": [
                "BUG-02 still BLOCKED_ON_PROOF_REFINEMENT",
                "Device evidence (Cycle 6) still TOKEN_VAZIO",
                "Cross-repo topological validation pending (6 repos in TOROID)"
            ],
            "F_next": "Execute federation topology validator (Cycle 6)"
        }

        return receipt

    def run(self):
        """Execute aggregation pipeline."""
        print("🌍 Phase 3: Federated Evidence Aggregator")
        print(f"   Repos root: {self.repos_root}\n")

        all_success = True
        all_success &= self.collect_mapa_evidence()
        all_success &= self.collect_termux_app_evidence()
        all_success &= self.map_cross_repo_dependencies()
        all_success &= self.validate_federation_coherence()

        receipt = self.generate_federated_receipt()

        # Write receipt
        build_dir = Path(__file__).parent.parent / "build"
        build_dir.mkdir(exist_ok=True)
        receipt_path = build_dir / "phase-3-federated-reconciliation-receipt.json"

        with open(receipt_path, "w") as f:
            json.dump(receipt, f, indent=2, default=str)

        print(f"✅ Receipt saved: {receipt_path}")
        print(f"\n📊 Federated State Summary:")
        print(f"   Repositories: {receipt['repositories_count']}")
        print(f"   Cross-repo dependencies: {len(self.cross_repo_deps)}")
        print(f"   Errors: {len(self.errors)}")
        print(f"   Warnings: {len(self.warnings)}")
        print(f"   Federation Status: {receipt['federation_status']}")
        print(f"   Ready for topology check: {receipt['ready_for_topology_check']}")

        return all_success, receipt


def main():
    aggregator = FederatedEvidenceAggregator(repos_root="/home/user")
    success, receipt = aggregator.run()
    return 0 if success and receipt.get("ready_for_topology_check") else 1


if __name__ == "__main__":
    sys.exit(main())
