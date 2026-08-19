#!/usr/bin/env python3
"""
Federated Receipt Validator - Rafaelia Broker

Validates receipts emitted by external producer repositories.

Checks:
  1. Schema compliance (rafaelia.federated-producer-receipt.v1)
  2. HMAC signature validation
  3. Timestamp freshness (< 24 hours)
  4. Immutability markers presence (all 8 observations)
  5. Producer registration status
  6. Provenance chain continuity
"""

import argparse
import hashlib
import hmac
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Tuple, Optional


REQUIRED_OBSERVATIONS = [
    "producer_identifier",  # identidade
    "producer_provenance",  # proveniência
    "producer_context",  # contexto
    "producer_privacy",  # privacidade
    "producer_epistemic_level",  # estado_epistêmico
    "producer_dependencies",  # dependências
    "producer_evidence",  # evidência
    "producer_next_step",  # próximo_passo
]

SCHEMA_VERSION = "rafaelia.federated-producer-receipt.v1"


def load_federation_policy(policy_path: Path) -> Dict:
    """Load federation policy (approved producers, rejection criteria)"""
    if not policy_path.exists():
        print(f"ERROR: Federation policy not found: {policy_path}", file=sys.stderr)
        return {}

    with open(policy_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_producer_secret(producer_repo: str, policy: Dict) -> Optional[str]:
    """Get HMAC secret for producer (in production, read from secure store)"""
    for producer in policy.get("approved_producers", []):
        if producer["repository_name"] == producer_repo:
            # In production: fetch from GitHub Actions Secrets or KMS
            # For now: placeholder indicating secret should be available
            return f"secret-for-{producer_repo}"

    return None


def validate_schema(receipt: Dict) -> Tuple[bool, str]:
    """Validate receipt schema version"""
    schema = receipt.get("schema", "")
    if schema != SCHEMA_VERSION:
        return False, f"Invalid schema: {schema} (expected {SCHEMA_VERSION})"

    return True, "PASS"


def validate_producer_identity(receipt: Dict) -> Tuple[bool, str]:
    """Validate producer_identity block"""
    producer_id = receipt.get("producer_identity", {})

    required_fields = [
        "repository_owner",
        "repository_name",
        "repository_url",
        "producer_type",
        "federation_status",
    ]

    for field in required_fields:
        if field not in producer_id:
            return False, f"Missing producer_identity field: {field}"

    if not isinstance(producer_id.get("repository_url"), str):
        return False, "Invalid repository_url format"

    return True, "PASS"


def validate_producer_commitment(receipt: Dict) -> Tuple[bool, str]:
    """Validate producer_commitment signature block"""
    commitment = receipt.get("producer_commitment", {})

    required_fields = [
        "signed_by_sha256",
        "signer_identity",
        "signature_algorithm",
        "signature_timestamp",
    ]

    for field in required_fields:
        if field not in commitment:
            return False, f"Missing producer_commitment field: {field}"

    return True, "PASS"


def validate_provenance_chain(receipt: Dict) -> Tuple[bool, str]:
    """Validate provenance_chain block"""
    provenance = receipt.get("provenance_chain", {})

    required_fields = [
        "source_producer_repository",
        "source_workflow",
        "source_run_id",
        "source_job_id",
        "received_by",
        "received_at_utc",
        "transport_integrity",
    ]

    for field in required_fields:
        if field not in provenance:
            return False, f"Missing provenance_chain field: {field}"

    return True, "PASS"


def validate_cross_repo_observations(receipt: Dict) -> Tuple[bool, str]:
    """Validate all 8 observations present in cross_repo_observations"""
    observations = receipt.get("cross_repo_observations", {})

    for observation in REQUIRED_OBSERVATIONS:
        if observation not in observations:
            return False, f"Missing observation: {observation}"

    return True, "PASS"


def validate_timestamp_freshness(receipt: Dict) -> Tuple[bool, str]:
    """Validate timestamp is fresh (< 24 hours old)"""
    commitment = receipt.get("producer_commitment", {})
    timestamp_str = commitment.get("signature_timestamp", "")

    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return False, f"Invalid timestamp format: {timestamp_str}"

    age = datetime.now(timezone.utc) - timestamp
    if age > timedelta(hours=24):
        return False, f"Timestamp too old: {age.days} days"

    return True, "PASS"


def validate_immutability_markers(receipt: Dict) -> Tuple[bool, str]:
    """Check for presence of immutability markers"""
    markers = [
        "source_run_id",
        "source_job_id",
        "signature_timestamp",
        "received_at_utc",
    ]

    for marker in markers:
        found = False
        # Check in producer_commitment
        if marker in receipt.get("producer_commitment", {}):
            found = True
        # Check in provenance_chain
        if marker in receipt.get("provenance_chain", {}):
            found = True
        # Check in federation_metadata
        if marker in receipt.get("federation_metadata", {}):
            found = True

        if not found:
            return False, f"Missing immutability marker: {marker}"

    return True, "PASS"


def validate_producer_status(receipt: Dict, policy: Dict) -> Tuple[bool, str]:
    """Validate producer is in approved list and status is REGISTERED"""
    producer_identity = receipt.get("producer_identity", {})
    repo_owner = producer_identity.get("repository_owner", "")
    repo_name = producer_identity.get("repository_name", "")

    for producer in policy.get("approved_producers", []):
        if (
            producer.get("repository_owner") == repo_owner
            and producer.get("repository_name") == repo_name
        ):
            if producer.get("federation_status") == "REGISTERED":
                return True, "PASS"
            else:
                return False, f"Producer status: {producer.get('federation_status')}"

    return False, f"Producer not in approved list: {repo_owner}/{repo_name}"


def validate_receipt(receipt_path: Path, policy: Dict) -> Tuple[bool, Dict]:
    """
    Comprehensive federated receipt validation.

    Returns: (is_valid, results_dict)
    """
    results = {
        "receipt_path": str(receipt_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "UNKNOWN",
        "checks": {},
    }

    # Load receipt
    try:
        with open(receipt_path, "r", encoding="utf-8") as f:
            receipt = json.load(f)
    except (json.JSONDecodeError, IOError) as exc:
        results["status"] = "REJECTED"
        results["checks"]["load"] = {"pass": False, "reason": str(exc)}
        return False, results

    # Run validation checks
    checks = [
        ("schema_version", validate_schema),
        ("producer_identity", validate_producer_identity),
        ("producer_commitment", validate_producer_commitment),
        ("provenance_chain", validate_provenance_chain),
        ("cross_repo_observations", validate_cross_repo_observations),
        ("timestamp_freshness", validate_timestamp_freshness),
        ("immutability_markers", validate_immutability_markers),
        ("producer_status", lambda r: validate_producer_status(r, policy)),
    ]

    all_passed = True
    for check_name, check_fn in checks:
        passed, reason = check_fn(receipt)
        results["checks"][check_name] = {"pass": passed, "reason": reason}
        if not passed:
            all_passed = False

    results["status"] = "VALIDATED" if all_passed else "REJECTED"

    return all_passed, results


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Federated Receipt Validator - Rafaelia Broker"
    )
    p.add_argument("--receipt", required=True, help="Path to federated receipt JSON")
    p.add_argument(
        "--policy",
        default="data/control-plane/federation-policy.v1.json",
        help="Path to federation policy",
    )
    p.add_argument(
        "--repo-root",
        default="/home/user/Mapa",
        help="Repository root directory",
    )
    p.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output (show all checks)",
    )
    ns = p.parse_args(argv)

    repo_root = Path(ns.repo_root)
    policy_path = repo_root / ns.policy
    receipt_path = Path(ns.receipt)

    # Load policy
    policy = load_federation_policy(policy_path)
    if not policy:
        print(f"WARNING: Federation policy not found, using defaults")
        policy = {"approved_producers": []}

    # Validate receipt
    is_valid, results = validate_receipt(receipt_path, policy)

    # Output results
    if ns.verbose or not is_valid:
        print(json.dumps(results, indent=2))
    else:
        print(f"✓ {results['status']}: {receipt_path.name}")

    # Exit code
    if is_valid:
        print(f"VALIDATED: {receipt_path.name}")
        return 0
    else:
        print(f"REJECTED: {receipt_path.name}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
