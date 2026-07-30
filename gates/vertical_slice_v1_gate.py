#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
registry = json.loads((ROOT / "data/vertical_slice_v1/registry.json").read_text(encoding="utf-8"))
status = json.loads((ROOT / "resultados/RAFAELIA_VERTICAL_SLICE_STATUS_V1.json").read_text(encoding="utf-8"))
receipt = json.loads((ROOT / "receipts/vertical_slice/RECEIPT-VSLICE-001.reference.json").read_text(encoding="utf-8"))

errors = []
if registry.get("claim_allowed") is not False:
    errors.append("registry is not fail-closed")
if receipt.get("claim_allowed") is not False:
    errors.append("receipt is not fail-closed")
if receipt.get("exit_code") != 0 or receipt.get("result", {}).get("overall_pass") is not True:
    errors.append("reference receipt did not pass")
if any(not claim.get("falsifier") for claim in registry.get("claims", [])):
    errors.append("claim without falsifier")
if status["steps"].get("13_human_review") != "TOKEN_VAZIO_HUMAN_REVIEW_PENDING":
    errors.append("unexpected human-review state")
if status["metrics"].get("termux_replication") != "TOKEN_VAZIO_RUNTIME_NOT_EXECUTED":
    errors.append("unexpected Termux state")

if errors:
    raise SystemExit("FAIL_CLOSED: " + "; ".join(errors))
print("PASS: structural slice is valid; promotion remains blocked pending Termux and human review")
