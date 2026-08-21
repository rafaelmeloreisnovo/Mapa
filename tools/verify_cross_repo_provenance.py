#!/usr/bin/env python3
"""
Federated Receipt Cross-Repo Provenance Verifier

Validates Rafaelia federated receipts and receipt chains for:
- Complete 8-observation compliance
- Provenance chain continuity
- Immutability marker presence
- Timestamp freshness
- Evidence artifact integrity

Part of Phase 2-P1-04c: Federated Producer Operations
Lane 04 (Validação) uses this tool for receipt validation
"""

import json
import sys
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


class ProvenanceValidator:
    """Validates federated receipts against Rafaelia specification."""

    # Required 8 observations (Layer 2 from framework)
    REQUIRED_OBSERVATIONS = [
        "identidade",       # producer_identity
        "proveniência",     # provenance_chain
        "contexto",         # producer_context (in cross_repo_observations)
        "privacidade",      # producer_privacy
        "estado_epistêmico", # producer_epistemic_level
        "dependências",     # producer_dependencies
        "evidência",        # producer_evidence
        "próximo_passo"     # producer_next_step
    ]

    # Immutability markers required
    IMMUTABILITY_MARKERS = [
        "run_id",
        "job_id",
        "timestamp",
        "received_at_utc"
    ]

    # Valid schema
    VALID_SCHEMA = "rafaelia.federated-producer-receipt.v1"

    def __init__(self, receipt: Dict[str, Any], strict_mode: bool = True):
        """Initialize validator with receipt."""
        self.receipt = receipt
        self.strict_mode = strict_mode
        self.issues: List[Dict[str, Any]] = []
        self.checks_passed: List[str] = []

    def validate(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Perform complete validation.

        Returns:
            (is_valid, report_dict)
        """
        self._check_schema()
        self._check_8_observations()
        self._check_immutability_markers()
        self._check_provenance_chain()
        self._check_timestamp_freshness()
        self._check_privacy_compliance()

        is_valid = len(self.issues) == 0
        return is_valid, self._generate_report()

    def _check_schema(self) -> None:
        """Verify receipt schema version."""
        schema = self.receipt.get("schema")
        if schema != self.VALID_SCHEMA:
            self.issues.append({
                "check": "schema_validation",
                "severity": "CRITICAL",
                "message": f"Invalid schema: expected {self.VALID_SCHEMA}, got {schema}"
            })
        else:
            self.checks_passed.append(f"schema_validation ({schema})")

    def _check_8_observations(self) -> None:
        """Verify all 8 observations present (Invariant 4: evidência prije promoção)."""
        cross_repo = self.receipt.get("cross_repo_observations", {})

        observations_present = {
            "identidade": self.receipt.get("producer_identity") is not None,
            "proveniência": self.receipt.get("provenance_chain") is not None,
            "contexto": cross_repo.get("producer_context") is not None,
            "privacidade": cross_repo.get("producer_privacy") is not None,
            "estado_epistêmico": cross_repo.get("producer_epistemic_level") is not None,
            "dependências": cross_repo.get("producer_dependencies") is not None,
            "evidência": cross_repo.get("producer_evidence") is not None,
            "próximo_passo": cross_repo.get("producer_next_step") is not None,
        }

        missing = [obs for obs, present in observations_present.items() if not present]
        if missing:
            self.issues.append({
                "check": "8_observations_complete",
                "severity": "CRITICAL",
                "message": f"Missing observations: {', '.join(missing)}",
                "missing_count": len(missing)
            })
        else:
            self.checks_passed.append(f"8_observations_complete (all {len(observations_present)} present)")

    def _check_immutability_markers(self) -> None:
        """Verify immutability markers (Invariant 7: artifact e hash antes VERIFIED)."""
        provenance = self.receipt.get("provenance_chain", {})
        markers_found = {}

        # Check for markers in provenance chain
        if "source_run_id" in provenance:
            markers_found["run_id"] = provenance["source_run_id"]
        if "source_job_id" in provenance:
            markers_found["job_id"] = provenance["source_job_id"]
        if "signature_timestamp" in self.receipt.get("producer_commitment", {}):
            markers_found["timestamp"] = self.receipt["producer_commitment"]["signature_timestamp"]
        if "received_at_utc" in provenance:
            markers_found["received_at_utc"] = provenance["received_at_utc"]

        missing_markers = [m for m in self.IMMUTABILITY_MARKERS if m not in markers_found]
        if missing_markers:
            self.issues.append({
                "check": "immutability_markers",
                "severity": "HIGH",
                "message": f"Missing immutability markers: {', '.join(missing_markers)}",
                "found": list(markers_found.keys()),
                "missing": missing_markers
            })
        else:
            self.checks_passed.append(f"immutability_markers_complete (all {len(self.IMMUTABILITY_MARKERS)} present)")

    def _check_provenance_chain(self) -> None:
        """Verify provenance chain continuity (Invariant 6: checkout real before claim)."""
        provenance = self.receipt.get("provenance_chain", {})
        cross_repo = self.receipt.get("cross_repo_observations", {})
        producer_prov = cross_repo.get("producer_provenance", {})

        # Check chain elements
        required_chain_fields = [
            ("source_producer_repository", "source repo identifier"),
            ("source_workflow", "source workflow"),
            ("source_run_id", "source run ID"),
            ("received_by", "receipt receiver"),
            ("received_at_utc", "receipt timestamp")
        ]

        missing_chain = []
        for field, desc in required_chain_fields:
            if field not in provenance or not provenance[field]:
                missing_chain.append(f"{field} ({desc})")

        if missing_chain:
            self.issues.append({
                "check": "provenance_chain_continuity",
                "severity": "HIGH",
                "message": f"Broken provenance chain: {', '.join(missing_chain)}"
            })
        else:
            self.checks_passed.append("provenance_chain_continuity")

        # Validate custody chain if present
        custody_chain = producer_prov.get("custody_chain", [])
        if custody_chain:
            if not isinstance(custody_chain, list) or len(custody_chain) == 0:
                self.issues.append({
                    "check": "custody_chain_format",
                    "severity": "MEDIUM",
                    "message": "Custody chain present but invalid format"
                })
            else:
                self.checks_passed.append(f"custody_chain_valid ({len(custody_chain)} links)")

    def _check_timestamp_freshness(self) -> None:
        """Verify timestamps are within acceptable window (24 hours)."""
        try:
            observed_at = self.receipt.get("observed_at_utc")
            signature_ts = self.receipt.get("producer_commitment", {}).get("signature_timestamp")
            received_at = self.receipt.get("provenance_chain", {}).get("received_at_utc")

            now = datetime.now(timezone.utc)
            freshness_window = timedelta(hours=24)

            timestamps_to_check = [
                ("observed_at_utc", observed_at),
                ("signature_timestamp", signature_ts),
                ("received_at_utc", received_at)
            ]

            stale_timestamps = []
            for name, ts_str in timestamps_to_check:
                if ts_str:
                    try:
                        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        age = now - ts
                        if age > freshness_window:
                            stale_timestamps.append({
                                "field": name,
                                "timestamp": ts_str,
                                "age_hours": age.total_seconds() / 3600
                            })
                    except ValueError:
                        self.issues.append({
                            "check": "timestamp_format",
                            "severity": "MEDIUM",
                            "message": f"Invalid timestamp format in {name}: {ts_str}"
                        })

            if stale_timestamps:
                self.issues.append({
                    "check": "timestamp_freshness",
                    "severity": "MEDIUM",
                    "message": f"Stale timestamps (> 24 hours): {len(stale_timestamps)}",
                    "stale": stale_timestamps
                })
            else:
                self.checks_passed.append("timestamp_freshness (all recent)")

        except Exception as e:
            self.issues.append({
                "check": "timestamp_validation",
                "severity": "HIGH",
                "message": f"Error validating timestamps: {str(e)}"
            })

    def _check_privacy_compliance(self) -> None:
        """Verify GDPR/LGPD compliance markers (Invariant 2: privacidade before interpretation)."""
        cross_repo = self.receipt.get("cross_repo_observations", {})
        privacy = cross_repo.get("producer_privacy", {})

        required_privacy_fields = [
            "data_classification",
            "pii_scan",
            "gdpr_compliant",
            "lgpd_compliant",
            "secrets_scan"
        ]

        missing_privacy = [f for f in required_privacy_fields if f not in privacy or privacy[f] is None]

        if missing_privacy:
            self.issues.append({
                "check": "privacy_compliance",
                "severity": "HIGH",
                "message": f"Missing privacy markers: {', '.join(missing_privacy)}"
            })
        else:
            # Check values
            if not privacy.get("gdpr_compliant") or not privacy.get("lgpd_compliant"):
                self.issues.append({
                    "check": "compliance_status",
                    "severity": "HIGH",
                    "message": "Receipt marked as non-compliant with GDPR/LGPD"
                })
            elif privacy.get("pii_scan") != "no_pii_detected":
                self.issues.append({
                    "check": "pii_detection",
                    "severity": "HIGH",
                    "message": f"PII detected in receipt: {privacy.get('pii_scan')}"
                })
            else:
                self.checks_passed.append("privacy_compliance (GDPR/LGPD compliant, no PII)")

    def _generate_report(self) -> Dict[str, Any]:
        """Generate structured validation report."""
        is_valid = len(self.issues) == 0

        return {
            "validation_status": "PASS" if is_valid else "FAIL",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "receipt_identity": {
                "schema": self.receipt.get("schema"),
                "observed_at": self.receipt.get("observed_at_utc"),
                "producer": f"{self.receipt.get('producer_identity', {}).get('repository_owner')}/{self.receipt.get('producer_identity', {}).get('repository_name')}"
            },
            "checks_passed": self.checks_passed,
            "checks_failed": len(self.issues),
            "issues": self.issues if self.issues else None,
            "summary": {
                "total_checks": len(self.checks_passed) + len(self.issues),
                "passed": len(self.checks_passed),
                "failed": len(self.issues),
                "severity_breakdown": self._count_severity()
            }
        }

    def _count_severity(self) -> Dict[str, int]:
        """Count issues by severity."""
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for issue in self.issues:
            severity = issue.get("severity", "MEDIUM")
            if severity in severity_counts:
                severity_counts[severity] += 1
        return {k: v for k, v in severity_counts.items() if v > 0}


def main():
    parser = argparse.ArgumentParser(
        description="Verify Rafaelia federated receipt provenance and completeness"
    )
    parser.add_argument(
        "--receipt",
        required=True,
        type=str,
        help="Path to receipt JSON file or '-' for stdin"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output (print all checks)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="json",
        choices=["json", "text"],
        help="Output format (default: json)"
    )

    args = parser.parse_args()

    # Load receipt
    try:
        if args.receipt == "-":
            receipt_data = json.load(sys.stdin)
        else:
            with open(args.receipt, "r") as f:
                receipt_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"ERROR: Failed to load receipt: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate
    validator = ProvenanceValidator(receipt_data)
    is_valid, report = validator.validate()

    # Output
    if args.output == "json":
        if args.verbose:
            print(json.dumps(report, indent=2))
        else:
            summary = {
                "validation_status": report["validation_status"],
                "receipt_identity": report["receipt_identity"],
                "summary": report["summary"]
            }
            if report["issues"]:
                summary["issues_sample"] = report["issues"][:3]
            print(json.dumps(summary, indent=2))
    else:
        # Text output
        print(f"Receipt Validation Report")
        print(f"======================")
        print(f"Status: {report['validation_status']}")
        print(f"Producer: {report['receipt_identity']['producer']}")
        print(f"Observed at: {report['receipt_identity']['observed_at']}")
        print(f"\nValidation Summary:")
        print(f"  Checks passed: {report['summary']['passed']}")
        print(f"  Checks failed: {report['summary']['failed']}")
        if report['summary'].get('severity_breakdown'):
            print(f"  Severity breakdown: {report['summary']['severity_breakdown']}")
        if args.verbose and report["issues"]:
            print(f"\nIssues found:")
            for issue in report["issues"]:
                print(f"  [{issue.get('severity', 'MEDIUM')}] {issue['check']}: {issue['message']}")

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
