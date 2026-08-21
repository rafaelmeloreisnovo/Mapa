#!/usr/bin/env python3
"""
Federated Audit Aggregator

Centralizes federation-related audit trails from:
- federated-receipts-audit.jsonl (receipt submission events)
- hmac-key-audit.jsonl (cryptographic key usage events)
- TOKEN_VAZIO_APPROVAL_DECISIONS.jsonl (governance decisions)

Generates summary reports for:
- Lane 07 (Segurança): Key management & anomaly detection
- Lane 08 (Observabilidade): Submission patterns & compliance metrics
- Lane 00 (Governança): Approval timeline & decision history

Part of Phase 2-P1-04c: Federated Producer Operations
"""

import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


class AuditAggregator:
    """Aggregates federated audit trails."""

    def __init__(self, audit_dir: Path = None):
        """Initialize aggregator with audit directory."""
        self.audit_dir = audit_dir or Path("data/audits")
        self.receipts_log = self.audit_dir / "federated-receipts-audit.jsonl"
        self.keys_log = self.audit_dir / "hmac-key-audit.jsonl"
        self.decisions_log = self.audit_dir / "TOKEN_VAZIO_APPROVAL_DECISIONS.jsonl"

        self.receipts_events = []
        self.keys_events = []
        self.decisions = []
        self.errors = []

    def load_logs(self) -> bool:
        """Load all audit logs. Return False if critical logs missing."""
        # Try to load receipt logs (most important)
        if self.receipts_log.exists():
            try:
                with open(self.receipts_log, "r") as f:
                    for line in f:
                        if line.strip():
                            try:
                                self.receipts_events.append(json.loads(line))
                            except json.JSONDecodeError as e:
                                self.errors.append(f"Invalid JSON in receipts log: {e}")
            except Exception as e:
                self.errors.append(f"Error reading receipts log: {e}")
        else:
            self.errors.append(f"Receipts log not found: {self.receipts_log}")

        # Load key logs (secondary)
        if self.keys_log.exists():
            try:
                with open(self.keys_log, "r") as f:
                    for line in f:
                        if line.strip():
                            try:
                                self.keys_events.append(json.loads(line))
                            except json.JSONDecodeError as e:
                                self.errors.append(f"Invalid JSON in keys log: {e}")
            except Exception as e:
                self.errors.append(f"Error reading keys log: {e}")

        # Load decision logs (tertiary)
        if self.decisions_log.exists():
            try:
                with open(self.decisions_log, "r") as f:
                    for line in f:
                        if line.strip():
                            try:
                                self.decisions.append(json.loads(line))
                            except json.JSONDecodeError as e:
                                self.errors.append(f"Invalid JSON in decisions log: {e}")
            except Exception as e:
                self.errors.append(f"Error reading decisions log: {e}")

        return len(self.receipts_events) > 0 or len(self.keys_events) > 0

    def aggregate_receipts(self) -> Dict[str, Any]:
        """Aggregate receipt submission events."""
        by_producer = defaultdict(lambda: {
            "submitted": 0,
            "validated": 0,
            "rejected": 0,
            "statuses": defaultdict(int),
            "first_submission": None,
            "last_submission": None
        })

        by_status = defaultdict(int)
        total = len(self.receipts_events)

        for event in self.receipts_events:
            producer = event.get("producer", "unknown")
            status = event.get("validation_status", "unknown")
            timestamp = event.get("timestamp")

            # Track by producer
            producer_data = by_producer[producer]
            if status == "VALIDATED":
                producer_data["validated"] += 1
            elif status == "REJECTED":
                producer_data["rejected"] += 1
            producer_data["submitted"] += 1
            producer_data["statuses"][status] += 1

            # Track timestamp range
            if timestamp:
                if not producer_data["first_submission"]:
                    producer_data["first_submission"] = timestamp
                producer_data["last_submission"] = timestamp

            # Track overall status
            by_status[status] += 1

        return {
            "total_receipts": total,
            "by_status": dict(by_status),
            "by_producer": {
                prod: {
                    "submitted": data["submitted"],
                    "validated": data["validated"],
                    "rejected": data["rejected"],
                    "statuses": dict(data["statuses"]),
                    "first_submission": data["first_submission"],
                    "last_submission": data["last_submission"],
                    "success_rate": round(
                        (data["validated"] / data["submitted"] * 100) if data["submitted"] > 0 else 0, 2
                    )
                }
                for prod, data in sorted(by_producer.items())
            },
            "producers_count": len(by_producer)
        }

    def aggregate_keys(self) -> Dict[str, Any]:
        """Aggregate HMAC key events."""
        by_event = defaultdict(int)
        by_producer = defaultdict(int)
        total = len(self.keys_events)
        signature_failures = 0

        for event in self.keys_events:
            event_type = event.get("event", "unknown")
            producer = event.get("producer", "unknown")
            is_valid = event.get("signature_valid", True)

            by_event[event_type] += 1
            by_producer[producer] += 1

            if not is_valid:
                signature_failures += 1

        anomalies = []
        # Detect anomaly: multiple signature failures from same producer
        for producer, count in by_producer.items():
            if count > 10:  # Threshold for "unusual"
                anomalies.append({
                    "type": "high_submission_volume",
                    "producer": producer,
                    "count": count,
                    "threshold": 10
                })

        return {
            "total_key_events": total,
            "by_event_type": dict(by_event),
            "producers_with_events": len(by_producer),
            "signature_failure_count": signature_failures,
            "anomalies": anomalies
        }

    def aggregate_decisions(self) -> Dict[str, Any]:
        """Aggregate governance decisions."""
        by_status = defaultdict(int)
        by_phase = defaultdict(int)
        total = len(self.decisions)

        for decision in self.decisions:
            status = decision.get("decision_status", "unknown")
            phase = decision.get("phase", "unknown")

            by_status[status] += 1
            by_phase[phase] += 1

        return {
            "total_decisions": total,
            "by_status": dict(by_status),
            "by_phase": dict(by_phase),
            "decisions": self.decisions[:10] if len(self.decisions) > 0 else []
        }

    def calculate_compliance(self) -> Dict[str, Any]:
        """Calculate compliance metrics."""
        compliance = {
            "receipt_immutability": "UNKNOWN",
            "audit_trail_completeness": "UNKNOWN",
            "all_lanes_confirmed": "UNKNOWN",
            "issues": []
        }

        # Check receipt immutability markers
        if self.receipts_events:
            receipts_with_markers = sum(
                1 for e in self.receipts_events
                if all(k in e for k in ["run_id", "job_id", "timestamp"])
            )
            total_receipts = len(self.receipts_events)
            immutability_rate = receipts_with_markers / total_receipts if total_receipts > 0 else 0
            compliance["receipt_immutability"] = f"{round(immutability_rate * 100, 1)}%"
            if immutability_rate < 0.95:
                compliance["issues"].append(
                    f"Low immutability marker rate: {round(immutability_rate * 100, 1)}%"
                )

        # Check audit trail gaps
        if not self.receipts_log.exists():
            compliance["issues"].append("Receipt audit log missing")
        if not self.keys_log.exists():
            compliance["issues"].append("Key audit log missing")

        # Overall
        if not compliance["issues"]:
            compliance["audit_trail_completeness"] = "PASS"
        else:
            compliance["audit_trail_completeness"] = "PARTIAL"

        return compliance

    def generate_report(self, format: str = "json") -> str:
        """Generate aggregated report."""
        report = {
            "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "audit_dir": str(self.audit_dir),
            "receipts": self.aggregate_receipts(),
            "keys": self.aggregate_keys(),
            "decisions": self.aggregate_decisions(),
            "compliance": self.calculate_compliance(),
            "errors": self.errors if self.errors else None
        }

        if format == "json":
            return json.dumps(report, indent=2)
        elif format == "markdown":
            return self._format_markdown(report)
        elif format == "csv":
            return self._format_csv(report)
        else:
            return json.dumps(report, indent=2)

    def _format_markdown(self, report: Dict[str, Any]) -> str:
        """Format report as markdown."""
        lines = [
            "# Federated Audit Report",
            f"Generated: {report['generated_at']}",
            "",
            "## Receipt Statistics",
            f"- Total receipts: {report['receipts'].get('total_receipts', 0)}",
            f"- Producers: {report['receipts'].get('producers_count', 0)}",
        ]

        receipts_status = report['receipts'].get('by_status', {})
        for status, count in receipts_status.items():
            lines.append(f"  - {status}: {count}")

        lines.extend([
            "",
            "## Key Management",
            f"- Total key events: {report['keys'].get('total_key_events', 0)}",
            f"- Signature failures: {report['keys'].get('signature_failure_count', 0)}",
        ])

        if report['keys'].get('anomalies'):
            lines.append("- Anomalies detected:")
            for anomaly in report['keys']['anomalies']:
                lines.append(f"  - {anomaly['type']}: {anomaly}")

        lines.extend([
            "",
            "## Governance Decisions",
            f"- Total decisions: {report['decisions'].get('total_decisions', 0)}",
        ])

        decisions_status = report['decisions'].get('by_status', {})
        for status, count in decisions_status.items():
            lines.append(f"  - {status}: {count}")

        lines.extend([
            "",
            "## Compliance",
            f"- Receipt immutability: {report['compliance'].get('receipt_immutability', 'UNKNOWN')}",
            f"- Audit trail: {report['compliance'].get('audit_trail_completeness', 'UNKNOWN')}",
        ])

        if report['compliance'].get('issues'):
            lines.append("- Issues:")
            for issue in report['compliance']['issues']:
                lines.append(f"  - {issue}")

        if report.get('errors'):
            lines.extend(["", "## Errors", "```"])
            for error in report['errors']:
                lines.append(f"- {error}")
            lines.append("```")

        return "\n".join(lines)

    def _format_csv(self, report: Dict[str, Any]) -> str:
        """Format receipts summary as CSV."""
        lines = ["producer,submitted,validated,rejected,success_rate"]
        by_producer = report['receipts'].get('by_producer', {})
        for producer, data in by_producer.items():
            lines.append(
                f"{producer},{data['submitted']},{data['validated']},"
                f"{data['rejected']},{data['success_rate']}"
            )
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate federated audit trails"
    )
    parser.add_argument(
        "--audit-dir",
        default="data/audits",
        help="Directory containing audit logs (default: data/audits)"
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "markdown", "csv"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Write report to file (default: stdout)"
    )

    args = parser.parse_args()

    aggregator = AuditAggregator(audit_dir=Path(args.audit_dir))
    if not aggregator.load_logs():
        print("WARNING: No audit logs found. Report will be incomplete.", file=sys.stderr)

    report = aggregator.generate_report(format=args.format)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
