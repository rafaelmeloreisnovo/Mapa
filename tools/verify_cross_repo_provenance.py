#!/usr/bin/env python3
"""Fail-closed cross-repository provenance verifier for RAFAELIA receipts.

The verifier does not prove scientific truth. It checks that a receipt's declared
producer identity, source repository/workflow and directly-addressable local
artifacts are mutually coherent before the broker may state that provenance was
verified.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


def fail(msg: str) -> None:
    print(json.dumps({"status": "REJECTED", "reason": msg}, ensure_ascii=False))
    raise SystemExit(2)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--receipt", required=True)
    p.add_argument("--policy", required=True)
    args = p.parse_args()

    receipt_path = Path(args.receipt)
    policy_path = Path(args.policy)
    if not receipt_path.is_file():
        fail(f"receipt not found: {receipt_path}")
    if not policy_path.is_file():
        fail(f"policy not found: {policy_path}")

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    policy = json.loads(policy_path.read_text(encoding="utf-8"))

    ident = receipt.get("producer_identity") or {}
    prov = receipt.get("provenance_chain") or {}
    obs = receipt.get("cross_repo_observations") or {}
    deps = (obs.get("producer_dependencies") or {}).get("direct") or []

    owner = ident.get("repository_owner")
    repo = ident.get("repository_name")
    declared_repo = prov.get("source_producer_repository")
    expected_repo = f"{owner}/{repo}" if owner and repo else None
    if not expected_repo or declared_repo != expected_repo:
        fail(f"producer identity/provenance mismatch: {expected_repo!r} != {declared_repo!r}")

    repo_url = ident.get("repository_url", "")
    parsed = urlparse(repo_url)
    if parsed.netloc.lower() != "github.com" or parsed.path.strip("/") != expected_repo:
        fail("repository_url does not match producer identity")

    approved = False
    for producer in policy.get("approved_producers", []):
        if producer.get("repository_owner") == owner and producer.get("repository_name") == repo:
            approved = producer.get("federation_status") in {"REGISTERED", "PROVISIONAL"}
            break
    if not approved and ident.get("producer_type") != "internal-test":
        fail("producer is not registered/provisional in federation policy")

    # For receipts emitted by this repository, source paths and direct dependencies
    # are locally inspectable and therefore must exist. For external producers they
    # remain a separate remote-evidence gate; this verifier must not invent them.
    local_repo = expected_repo == "rafaelmeloreisnovo/Mapa"
    checked: list[str] = []
    token_vazio: list[str] = []
    if local_repo:
        workflow = prov.get("source_workflow")
        if not isinstance(workflow, str) or not Path(workflow).is_file():
            fail(f"declared source_workflow missing locally: {workflow!r}")
        checked.append(workflow)
        for dep in deps:
            if not isinstance(dep, str):
                fail("direct dependency must be a path string for local producer")
            if not Path(dep).exists():
                fail(f"declared direct dependency missing locally: {dep}")
            checked.append(dep)
    else:
        token_vazio.append("REMOTE_SOURCE_CHECKOUT_NOT_OBSERVED")

    result = {
        "status": "VERIFIED_LIMITED" if token_vazio else "PASS",
        "producer": expected_repo,
        "checked_local_paths": sorted(set(checked)),
        "token_vazio": token_vazio,
        "claim_allowed": False,
        "boundary": "provenance coherence only; not execution/scientific validation",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
