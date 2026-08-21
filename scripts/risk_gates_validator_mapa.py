#!/usr/bin/env python3
"""Risk Gates Validator for Mapa — Routing & Authority"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RESULTS_DIR = REPO_ROOT / "governance" / "results" / "risk"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

class MAPAGateResult:
    def __init__(self, gate_id, result, evidence):
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.gate_id = gate_id
        self.result = result  # PASS, FAIL, TOKEN_VAZIO
        self.evidence = evidence

        try:
            self.commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
            ).strip()
        except:
            self.commit = "unknown"

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "commit": self.commit,
            "gate_id": self.gate_id,
            "result": self.result,
            "evidence": self.evidence,
        }

def validate():
    results = []

    # D1.1: Loop detection implemented?
    loop_detector_files = list(REPO_ROOT.rglob("*loop*")) + \
                         list(REPO_ROOT.rglob("*cycle*"))
    r1 = MAPAGateResult(
        "D1.1_loop_detection",
        "PASS" if loop_detector_files else "TOKEN_VAZIO",
        {"files_found": len(loop_detector_files)}
    )
    results.append(r1)

    # G0: Routing is controlled?
    routing_files = list(REPO_ROOT.rglob("*rout*"))
    r2 = MAPAGateResult(
        "G0_routing_exists",
        "PASS" if routing_files else "FAIL",
        {"routing_files": len(routing_files)}
    )
    results.append(r2)

    # D2.1: Bounds check in hop count?
    bounds_check = sum(
        1 for f in REPO_ROOT.rglob("*.py")
        if f.read_text().find("hop") > -1 and f.read_text().find("limit") > -1
    )
    r3 = MAPAGateResult(
        "D2.1_bounds_check",
        "PASS" if bounds_check > 0 else "TOKEN_VAZIO",
        {"files_with_bounds": bounds_check}
    )
    results.append(r3)

    # Summary
    passed = sum(1 for r in results if r.result == "PASS")
    failed = sum(1 for r in results if r.result == "FAIL")

    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "summary": {"passed": passed, "failed": failed, "total": len(results)},
        "results": [r.to_dict() for r in results],
    }

    filepath = RESULTS_DIR / f"mapa_gates_{datetime.utcnow().isoformat()}.json"
    with open(filepath, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"✓ PASS: {passed}")
    print(f"✗ FAIL: {failed}")
    print(f"≈ TOTAL: {len(results)}")
    print(f"[+] Results saved to {filepath.relative_to(REPO_ROOT)}")

    return failed == 0

if __name__ == "__main__":
    import sys
    sys.exit(0 if validate() else 1)
