#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    outdir = root / "artifacts" / "test_multidim_coherence"
    subprocess.check_call([
        "python3",
        str(root / "scripts" / "build_rafaelia_multidim_coherence.py"),
        "--root",
        str(root),
        "--outdir",
        str(outdir.relative_to(root)),
    ])
    receipt = json.loads((outdir / "run_receipt.json").read_text(encoding="utf-8"))
    assert receipt["claim_allowed"] is False
    assert "formula_candidates_extracted" in receipt["counts"]
    assert "TOKEN_VAZIO" in receipt["missing_expected_formula_coverage"]
    for name in ["formula_candidates.jsonl", "theorem_candidates.jsonl", "gaps.jsonl", "urgency_queue.jsonl"]:
        assert (outdir / name).exists(), name
    print("RAFAELIA multidim coherence tests PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
