#!/usr/bin/env python3
"""Build RAFAELIA multidimensional formula/theorem coherence artifacts.

This is a stdlib-only derived scanner. It does not prove formulas and does not
claim novelty. It reads configured source files when present in the checkout and
emits audit artifacts with TOKEN_VAZIO for missing coverage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

FORMULA_MARKERS = ["=", "\\", "lim", "sum", "int", "Omega", "Ω", "phi", "π", "sqrt", "F_", "RLL", "RAFAELIA"]
DOMAIN_KEYWORDS = {
    "math": ["theorem", "teorema", "formula", "fórmula", "proof", "prova", "lim", "sum", "integral", "π", "sqrt"],
    "physics": ["gravity", "gravidade", "plasma", "magnetic", "magnético", "photon", "fóton", "field", "campo"],
    "cosmology": ["RLL", "DESI", "BAO", "dark energy", "energia escura", "dark matter", "matéria escura", "H(z)", "E(a)"],
    "biology_biophoton": ["mitochondria", "mitocôndria", "chlorophyll", "clorofila", "biophoton", "biofóton", "melanin", "melanina", "glucose", "glicose", "CO2", "O2"],
    "computation": ["JSONL", "ONES", "CTI", "kernel", "gate", "workflow", "script", "hash"],
    "governance": ["claim_allowed", "TOKEN_VAZIO", "append-only", "provenance", "receipt", "evidence"],
    "spiritual_symbolic": ["espiritual", "verbo", "amor", "parábola", "symbolic", "simbólico", "sagrado"]
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def flatten_json(obj: Any, prefix: str = "") -> Iterable[tuple[str, Any]]:
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten_json(v, f"{prefix}.{k}" if prefix else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten_json(v, f"{prefix}[{i}]")
    else:
        yield prefix, obj


def detect_domains(text: str) -> List[str]:
    t = text.lower()
    domains = []
    for domain, words in DOMAIN_KEYWORDS.items():
        for word in words:
            if word.lower() in t:
                domains.append(domain)
                break
    return domains or ["TOKEN_VAZIO_DOMAIN"]


def is_formula_like(text: str) -> bool:
    if len(text.strip()) < 3:
        return False
    score = 0
    for marker in FORMULA_MARKERS:
        if marker in text:
            score += 1
    if re.search(r"[A-Za-zΑ-Ωα-ω_]+\s*\([^)]*\)\s*=", text):
        score += 2
    if re.search(r"[=→↔≤≥∑∫√πΩλφψ]", text):
        score += 1
    return score >= 1


def maturity_for(text: str) -> str:
    low = text.lower()
    if "known" in low or "equivalent" in low or "conhecido" in low:
        return "M0"
    if "candidate" in low or "candidato" in low or "hypothesis" in low or "hipótese" in low:
        return "M2"
    if "token_vazio" in low or "pending" in low or "lacuna" in low:
        return "TOKEN_VAZIO"
    return "M1"


def candidate_from_text(repo: str, path: str, locator: str, text: str) -> Dict[str, Any]:
    domains = detect_domains(text)
    claim_allowed = False
    gaps = []
    if "TOKEN_VAZIO" in text or "pending" in text.lower():
        gaps.append("TOKEN_VAZIO_IN_SOURCE_OR_PENDING")
    if not any(d in domains for d in ["math", "physics", "biology_biophoton", "cosmology"]):
        gaps.append("DOMAIN_LOW_CONFIDENCE")
    maturity = maturity_for(text)
    if maturity in ["M0", "M1"]:
        next_gate = "classify_known_equivalence_or_parametrization"
    elif maturity == "M2":
        next_gate = "define_assumptions_proof_or_falsifier"
    else:
        next_gate = "fill_source_provenance"
    urgency = len(domains) + len(gaps)
    if any(d in domains for d in ["cosmology", "biology_biophoton"]):
        urgency += 2
    if "claim_allowed" in text:
        urgency += 1
    return {
        "id": "RAF-FORMULA-CAND-" + sha256_text(repo + path + locator + text)[:16],
        "source_repo": repo,
        "source_path": path,
        "source_line": locator,
        "formula_text": text[:2000],
        "domain_axes": domains,
        "maturity": maturity,
        "claim_allowed": claim_allowed,
        "proof_status": "TOKEN_VAZIO_PROOF_REQUIRED",
        "evidence_routes": [{"repo": repo, "path": path, "locator": locator}],
        "paper_links": [],
        "gaps": gaps or ["PROOF_AND_PRIOR_ART_REQUIRED"],
        "urgency_score": urgency,
        "next_gate": next_gate
    }


def extract_candidates(root: Path, routes: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    candidates: List[Dict[str, Any]] = []
    gaps: List[Dict[str, Any]] = []
    for route in routes:
        repo = route.get("repo", "TOKEN_VAZIO_REPO")
        for rel in route.get("paths", []):
            if rel.startswith("TOKEN_VAZIO"):
                gaps.append({"repo": repo, "path": rel, "gap": rel})
                continue
            path = root / rel
            if not path.exists():
                gaps.append({"repo": repo, "path": rel, "gap": "TOKEN_VAZIO_PATH_NOT_IN_CHECKOUT"})
                continue
            try:
                if path.suffix.lower() == ".json":
                    data = load_json(path)
                    for locator, value in flatten_json(data):
                        if isinstance(value, (str, int, float)):
                            text = str(value)
                            if is_formula_like(text):
                                candidates.append(candidate_from_text(repo, rel, locator, text))
                else:
                    with path.open("r", encoding="utf-8") as handle:
                        for idx, line in enumerate(handle, 1):
                            text = line.strip()
                            if is_formula_like(text):
                                candidates.append(candidate_from_text(repo, rel, str(idx), text))
            except Exception as exc:
                gaps.append({"repo": repo, "path": rel, "gap": "READ_ERROR", "error": str(exc)})
    return candidates, gaps


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    n = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--control", default="data/control-plane/RAFAELIA_MULTIDIMENSIONAL_COHERENCE.v1.json")
    ap.add_argument("--root", default=".")
    ap.add_argument("--outdir", default="artifacts/multidim_coherence")
    args = ap.parse_args()
    root = Path(args.root)
    control = load_json(root / args.control)
    candidates, gaps = extract_candidates(root, control.get("source_routes", []))
    theorem_candidates = [c for c in candidates if c["maturity"] in ["M2", "M3", "M4"]]
    urgency_queue = sorted(candidates, key=lambda r: (-int(r.get("urgency_score", 0)), r["id"]))[:200]
    outdir = root / args.outdir
    n_formula = write_jsonl(outdir / "formula_candidates.jsonl", candidates)
    n_theorem = write_jsonl(outdir / "theorem_candidates.jsonl", theorem_candidates)
    n_gaps = write_jsonl(outdir / "gaps.jsonl", gaps)
    n_urgency = write_jsonl(outdir / "urgency_queue.jsonl", urgency_queue)
    receipt = {
        "schema": "RAFAELIA_MULTIDIMENSIONAL_COHERENCE_RUN_RECEIPT_V1",
        "claim_allowed": False,
        "control": args.control,
        "reported_formula_stock": control.get("reported_formula_stock", {}),
        "counts": {
            "formula_candidates_extracted": n_formula,
            "theorem_candidates_extracted": n_theorem,
            "gaps": n_gaps,
            "urgency_queue": n_urgency
        },
        "coverage_state": "DERIVED_FROM_AVAILABLE_CHECKOUT_ONLY",
        "missing_expected_formula_coverage": "TOKEN_VAZIO_UNTIL_FULL_SCAN_OF_653_TARGET",
        "outputs": control.get("outputs", {})
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "run_receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    print(json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
