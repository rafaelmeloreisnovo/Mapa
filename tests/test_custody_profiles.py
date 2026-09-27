#!/usr/bin/env python3
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_custody_profiles.py"
REGISTRY = ROOT / "data" / "governance" / "custody_profiles.v1.json"

def run_doc(doc):
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        path = f.name
    try:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), path],
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        Path(path).unlink(missing_ok=True)

def main():
    base = json.loads(REGISTRY.read_text(encoding="utf-8"))

    ok = run_doc(base)
    assert ok.returncode == 0, ok.stdout + ok.stderr

    duplicate = copy.deepcopy(base)
    duplicate["custody_types"].append(copy.deepcopy(duplicate["custody_types"][0]))
    r = run_doc(duplicate)
    assert r.returncode == 1 and "custody_type_set_or_duplicates" in r.stdout

    missing_evidence = copy.deepcopy(base)
    missing_evidence["custody_types"][0]["minimum_evidence"] = []
    r = run_doc(missing_evidence)
    assert r.returncode == 1 and "minimum_evidence" in r.stdout

    assistant_escalation = copy.deepcopy(base)
    for actor in assistant_escalation["actors"]:
        if actor["id"] == "ASSISTANT_SERVICE":
            actor["may_authorize_claim_promotion"] = True
    r = run_doc(assistant_escalation)
    assert r.returncode == 1 and "assistant_boundary_may_authorize_claim_promotion" in r.stdout

    durable_session = copy.deepcopy(base)
    for provider in durable_session["providers"]:
        if provider["id"] == "CHATGPT_SESSION":
            provider["durable"] = True
    r = run_doc(durable_session)
    assert r.returncode == 1 and "chatgpt_session_must_not_be_durable" in r.stdout

    auto_promote = copy.deepcopy(base)
    for rule in auto_promote["transition_rules"]:
        if rule["to"] == "C7_DECISION_CLAIM_GATE":
            rule["automatic_promotion"] = True
    r = run_doc(auto_promote)
    assert r.returncode == 1 and "decision_transition_must_not_auto_promote" in r.stdout

    print("PASS custody profile regression suite")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
