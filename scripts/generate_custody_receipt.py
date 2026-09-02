#!/usr/bin/env python3
"""
Generate Connector Custody Receipt

Creates an immutable custody receipt with merkle chain integrity.
Each receipt links to the prior receipt via SHA-256 hash.
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


def read_prior_receipt_hash(chain_file: Path) -> str:
    """Read the hash of the last receipt in the chain."""
    if not chain_file.exists() or chain_file.stat().st_size == 0:
        return "null"  # No prior receipts

    with open(chain_file, 'r') as f:
        lines = f.readlines()
        if not lines:
            return "null"

        # Last line is the most recent receipt
        try:
            last_receipt = json.loads(lines[-1].strip())
            return last_receipt.get("immutable_hash", "null")
        except json.JSONDecodeError:
            return "null"


def compute_receipt_hash(receipt_dict: Dict[str, Any]) -> str:
    """Compute SHA-256 hash of receipt (excluding the hash field itself)."""
    # Create a copy without the immutable_hash field for computation
    copy = {k: v for k, v in receipt_dict.items() if k != "immutable_hash"}
    json_str = json.dumps(copy, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(json_str.encode()).hexdigest()


def generate_receipt(
    connector_id: str,
    gate_id: str,
    executor_identity: str,
    repository_ref: str,
    source_commit: str,
    exit_code: int,
    evidence_scope: str = "local",
    producer_authority: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a custody receipt for a gate execution.

    Args:
        connector_id: Connector ID (e.g., CONN-001)
        gate_id: Gate identifier (e.g., RM-01)
        executor_identity: Who executed the gate
        repository_ref: Repository reference (owner/repo)
        source_commit: Commit hash of the gate execution
        exit_code: Exit code (0=PASS, nonzero=FAIL)
        evidence_scope: Scope of evidence (local/federated/third-party)
        producer_authority: Producer authority name

    Returns:
        Dictionary receipt ready for JSON serialization
    """
    timestamp = datetime.utcnow().isoformat() + "Z"

    receipt = {
        "receipt_id": f"CONNECTOR_{connector_id}_{gate_id}_{timestamp.replace(':', '').replace('-', '')}",
        "timestamp": timestamp,
        "repository_ref": repository_ref,
        "source_commit": source_commit,
        "gate_identifier": f"CONNECTOR_REGISTRATION_PROTOCOL.v1#{gate_id}",
        "execution_timestamp": timestamp,
        "executor_identity": executor_identity,
        "evidence_scope": evidence_scope,
        "producer_authority": producer_authority or "Mapa (federation validation authority)",
        "connector_id": connector_id,
        "exit_code": exit_code,
        "result": "PASS" if exit_code == 0 else "FAIL"
    }

    return receipt


def append_to_chain(
    chain_file: Path,
    receipt: Dict[str, Any]
) -> bool:
    """
    Append receipt to custody chain and compute merkle hash.

    Args:
        chain_file: Path to JSONL custody chain file
        receipt: Receipt dictionary

    Returns:
        True if successful, False otherwise
    """
    try:
        # Read prior hash before writing
        prior_hash = read_prior_receipt_hash(chain_file)

        # Add chain position and prior hash
        chain_position = 1
        if chain_file.exists() and chain_file.stat().st_size > 0:
            with open(chain_file, 'r') as f:
                chain_position = sum(1 for line in f) + 1

        receipt["chain_position"] = chain_position
        receipt["prior_receipt_hash"] = prior_hash

        # Compute immutable hash
        receipt["immutable_hash"] = compute_receipt_hash(receipt)
        receipt["custody_status"] = "APPENDED"

        # Append to chain
        with open(chain_file, 'a') as f:
            f.write(json.dumps(receipt) + "\n")

        print(f"✓ Receipt appended at chain position {chain_position}")
        print(f"  Receipt ID: {receipt['receipt_id']}")
        print(f"  Hash: {receipt['immutable_hash']}")
        print(f"  Prior hash: {prior_hash}")

        return True
    except Exception as e:
        print(f"✗ Failed to append receipt: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 8:
        print("Usage: python3 generate_custody_receipt.py <connector_id> <gate_id> "
              "<executor> <repo_ref> <commit> <exit_code> <evidence_scope> [producer_authority]")
        sys.exit(1)

    connector_id = sys.argv[1]
    gate_id = sys.argv[2]
    executor = sys.argv[3]
    repo_ref = sys.argv[4]
    commit = sys.argv[5]
    exit_code = int(sys.argv[6])
    evidence_scope = sys.argv[7]
    producer_authority = sys.argv[8] if len(sys.argv) > 8 else None

    # Generate receipt
    receipt = generate_receipt(
        connector_id, gate_id, executor, repo_ref, commit, exit_code, evidence_scope, producer_authority
    )

    # Append to chain
    chain_file = Path(__file__).parent.parent / "data" / "control-plane" / "CONNECTOR_CUSTODY_CHAIN.jsonl"
    if append_to_chain(chain_file, receipt):
        sys.exit(0)
    else:
        sys.exit(1)
