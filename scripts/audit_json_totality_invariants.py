#!/usr/bin/env python3
"""Fail-closed auditor for RAFAELIA JSON/JSONL invariant preservation.

The auditor is deliberately profile-aware: it does not pretend that every JSON object
has the same schema. It classifies records and then checks the invariants appropriate
for that profile while preserving a global totality contract:

  identity -> provenance -> lineage -> epistemic boundary -> claim gate

Unknown governed records are not silently promoted: they become typed gaps.
Stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

HEX64 = re.compile(r"^[a-f0-9]{64}$")
TOKEN = re.compile(r"^TOKEN_VAZIO_[A-Z0-9_]+$")

MESSAGE_REQUIRED = (
    "conversation_id", "message_id", "node_id", "parent_id",
    "source_path", "source_pointer", "text_hash",
    "epistemic_state", "privacy_class", "claim_allowed",
)
LONGITUDINAL_INVARIANTS = {
    "source_is_not_interpretation",
    "parable_is_not_physical_proof",
    "token_vazio_is_not_zero",
    "new_dimension_requires_semantics_type_source_and_state",
    "weights_require_calibration_and_evidence",
    "no_hidden_model_state_claim",
    "append_never_silently_overwrites_ancestor",
    "relation_requires_type_and_source",
}
LONGITUDINAL_GATES = (
    "provenance", "delta_identity", "semantic_consistency",
    "evidence_or_typed_gap", "reversibility",
)

@dataclass
class Finding:
    path: str
    record_index: int
    profile: str
    state: str
    gaps: list[str]
    invariant_vector: dict[str, bool]
    stable_id: str | None


def canonical_sha256(obj: Any) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def hash_or_token(v: Any) -> bool:
    return isinstance(v, str) and bool(HEX64.fullmatch(v) or TOKEN.fullmatch(v))


def classify(obj: Any) -> str:
    if not isinstance(obj, dict):
        return "scalar_or_array"
    if obj.get("kind") == "message" or {"conversation_id", "message_id", "source_pointer"} <= set(obj):
        return "message"
    if obj.get("schema") == "rafaelia.longitudinal-vector-evolution/v1":
        return "longitudinal_vector"
    if "claim_allowed" in obj or "epistemic_state" in obj or "f_gap" in obj or "source_pointer" in obj:
        return "governed_generic"
    return "ungoverned_generic"


def stable_id_for(obj: dict[str, Any]) -> str | None:
    for key in (
        "message_id", "node_id", "conversation_id", "vector_id", "artifact_id",
        "receipt_id", "event_id", "id", "schema",
    ):
        v = obj.get(key)
        if isinstance(v, (str, int)) and str(v):
            return f"{key}:{v}"
    return None


def has_provenance(obj: dict[str, Any]) -> bool:
    if obj.get("source_pointer") or obj.get("source_path") or obj.get("source_ref"):
        return True
    src = obj.get("source")
    if isinstance(src, dict) and (src.get("source_pointer") or src.get("source_id")):
        return True
    if isinstance(obj.get("github"), dict) or isinstance(obj.get("drive"), dict):
        return True
    return False


def has_lineage(obj: dict[str, Any]) -> bool:
    # Explicit null is meaningful for roots; field presence therefore counts.
    keys = {"parent_id", "previous_revision", "previous_event_hash", "lineage", "revision"}
    if keys & set(obj):
        return True
    layers = obj.get("layers")
    if isinstance(layers, dict):
        temporal = layers.get("temporal")
        if isinstance(temporal, dict) and "lineage" in temporal:
            return True
    return False


def has_epistemic_boundary(obj: dict[str, Any]) -> bool:
    if "epistemic_state" in obj or "claim_allowed" in obj or "privacy_class" in obj:
        return True
    layers = obj.get("layers")
    return isinstance(layers, dict) and isinstance(layers.get("epistemic"), dict)


def audit_message(obj: dict[str, Any], gaps: list[str]) -> dict[str, bool]:
    for key in MESSAGE_REQUIRED:
        if key not in obj:
            gaps.append(f"TOKEN_VAZIO_MESSAGE_{key.upper()}_ABSENT")
    identity = bool(obj.get("conversation_id")) and bool(obj.get("message_id")) and bool(obj.get("node_id"))
    if obj.get("message_id") and obj.get("node_id") and obj.get("message_id") != obj.get("node_id"):
        gaps.append("TOKEN_VAZIO_MESSAGE_NODE_ID_DIVERGENCE")
    provenance = bool(obj.get("source_path")) and bool(obj.get("source_pointer")) and hash_or_token(obj.get("text_hash"))
    lineage = "parent_id" in obj
    epistemic = bool(obj.get("epistemic_state")) and bool(obj.get("privacy_class"))
    claim_gate = obj.get("claim_allowed") is False
    if "claim_allowed" in obj and not claim_gate:
        gaps.append("TOKEN_VAZIO_CLAIM_GATE_OPEN")
    return {
        "identity": identity,
        "provenance": provenance,
        "lineage": lineage,
        "epistemic_boundary": epistemic,
        "claim_gate": claim_gate,
    }


def audit_longitudinal(obj: dict[str, Any], gaps: list[str]) -> dict[str, bool]:
    identity = bool(obj.get("vector_id")) and isinstance(obj.get("revision"), int)
    src = obj.get("source") if isinstance(obj.get("source"), dict) else {}
    provenance = bool(src.get("source_pointer")) and hash_or_token(src.get("source_sha256"))
    lineage = "previous_revision" in obj and (
        obj.get("revision") == 1 or hash_or_token(obj.get("previous_event_hash"))
    )
    layers = obj.get("layers") if isinstance(obj.get("layers"), dict) else {}
    epi = layers.get("epistemic") if isinstance(layers.get("epistemic"), dict) else {}
    epistemic = bool(epi.get("status")) and bool(epi.get("falsifier"))
    claim_gate = obj.get("claim_allowed") is False

    missing_inv = sorted(LONGITUDINAL_INVARIANTS - set(obj.get("invariants", [])))
    for inv in missing_inv:
        gaps.append(f"TOKEN_VAZIO_INVARIANT_{inv.upper()}")
    gates = obj.get("gates") if isinstance(obj.get("gates"), dict) else {}
    for gate in LONGITUDINAL_GATES:
        if gates.get(gate) is not True:
            gaps.append(f"TOKEN_VAZIO_GATE_{gate.upper()}_NOT_CLOSED")
    if obj.get("state") == "EVOLVED_LOCAL" and any(gates.get(g) is not True for g in LONGITUDINAL_GATES):
        gaps.append("TOKEN_VAZIO_EVOLVED_WITH_OPEN_GATE")
    if not claim_gate:
        gaps.append("TOKEN_VAZIO_CLAIM_GATE_OPEN")
    return {
        "identity": identity,
        "provenance": provenance,
        "lineage": lineage,
        "epistemic_boundary": epistemic,
        "claim_gate": claim_gate,
    }


def audit_generic(obj: dict[str, Any], governed: bool, gaps: list[str]) -> dict[str, bool]:
    identity = stable_id_for(obj) is not None
    provenance = has_provenance(obj)
    lineage = has_lineage(obj)
    epistemic = has_epistemic_boundary(obj)
    claim_gate = (obj.get("claim_allowed") is False) if "claim_allowed" in obj else not governed

    if governed:
        if not identity:
            gaps.append("TOKEN_VAZIO_IDENTITY_ABSENT")
        if not provenance:
            gaps.append("TOKEN_VAZIO_PROVENANCE_ABSENT")
        if not lineage:
            gaps.append("TOKEN_VAZIO_LINEAGE_ABSENT")
        if not epistemic:
            gaps.append("TOKEN_VAZIO_EPISTEMIC_BOUNDARY_ABSENT")
        if "claim_allowed" in obj and not claim_gate:
            gaps.append("TOKEN_VAZIO_CLAIM_GATE_OPEN")
    return {
        "identity": identity,
        "provenance": provenance,
        "lineage": lineage,
        "epistemic_boundary": epistemic,
        "claim_gate": claim_gate,
    }


def audit_record(obj: Any, path: Path, idx: int) -> Finding:
    profile = classify(obj)
    if not isinstance(obj, dict):
        return Finding(str(path), idx, profile, "SKIP_NON_OBJECT", [], {
            "identity": False, "provenance": False, "lineage": False,
            "epistemic_boundary": False, "claim_gate": False,
        }, None)

    gaps: list[str] = []
    if profile == "message":
        vector = audit_message(obj, gaps)
    elif profile == "longitudinal_vector":
        vector = audit_longitudinal(obj, gaps)
    elif profile == "governed_generic":
        vector = audit_generic(obj, True, gaps)
    else:
        vector = audit_generic(obj, False, gaps)

    if profile == "ungoverned_generic":
        state = "UNCLASSIFIED_NON_GOVERNED"
    else:
        state = "PASS" if all(vector.values()) and not gaps else "GAP"
    return Finding(str(path), idx, profile, state, gaps, vector, stable_id_for(obj))


def iter_records(path: Path) -> Iterable[tuple[int, Any]]:
    suffix = path.name.lower()
    if suffix.endswith(".jsonl") or suffix.endswith(".jsonl.txt"):
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh, 1):
                if not line.strip():
                    continue
                try:
                    yield i, json.loads(line)
                except json.JSONDecodeError as exc:
                    yield i, {"__parse_error__": str(exc), "claim_allowed": False, "f_gap": ["TOKEN_VAZIO_JSON_PARSE_ERROR"]}
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        yield 1, {"__parse_error__": str(exc), "claim_allowed": False, "f_gap": ["TOKEN_VAZIO_JSON_PARSE_ERROR"]}
        return
    if isinstance(data, list):
        for i, item in enumerate(data, 1):
            yield i, item
    else:
        yield 1, data


def discover(inputs: list[Path]) -> list[Path]:
    found: list[Path] = []
    for p in inputs:
        if p.is_file():
            found.append(p)
            continue
        if not p.exists():
            continue
        for q in p.rglob("*"):
            n = q.name.lower()
            if q.is_file() and (n.endswith(".json") or n.endswith(".jsonl") or n.endswith(".jsonl.txt")):
                found.append(q)
    return sorted(set(found))


def summarize(findings: list[Finding], files: list[Path]) -> dict[str, Any]:
    governed = [f for f in findings if f.profile not in {"ungoverned_generic", "scalar_or_array"}]
    pass_n = sum(f.state == "PASS" for f in governed)
    gap_n = sum(f.state == "GAP" for f in governed)
    gap_counter = Counter(g for f in governed for g in f.gaps)
    dimensions = {}
    for dim in ("identity", "provenance", "lineage", "epistemic_boundary", "claim_gate"):
        ok = sum(bool(f.invariant_vector.get(dim)) for f in governed)
        dimensions[dim] = {
            "ok": ok,
            "total": len(governed),
            "coverage": (ok / len(governed)) if governed else None,
        }
    return {
        "schema": "rafaelia.json-totality-invariant-audit/v1",
        "state": "PASS" if governed and gap_n == 0 else ("TOKEN_VAZIO_NO_GOVERNED_RECORDS" if not governed else "GAP"),
        "claim_allowed": False,
        "contract": "representation_may_evolve_but_identity_provenance_lineage_epistemic_boundary_must_remain_traceable",
        "files_scanned": len(files),
        "records_scanned": len(findings),
        "governed_records": len(governed),
        "governed_pass": pass_n,
        "governed_gap": gap_n,
        "conservation_rate": (pass_n / len(governed)) if governed else None,
        "dimension_coverage": dimensions,
        "profile_counts": dict(Counter(f.profile for f in findings)),
        "gap_counts": dict(gap_counter.most_common()),
        "f_ok": ["profile_aware_scan", "typed_gaps", "claim_gate_fail_closed", "dimension_coverage"],
        "f_gap": [] if gap_n == 0 and governed else (["TOKEN_VAZIO_GOVERNED_RECORD_GAPS"] if governed else ["TOKEN_VAZIO_NO_GOVERNED_RECORDS"]),
        "f_next": "close typed gaps at the original source pointer; rerun until conservation_rate=1.0 for the governed scope",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("--report", type=Path)
    ap.add_argument("--findings", type=Path, help="optional JSONL findings output")
    ap.add_argument("--strict", action="store_true", help="exit 2 when any governed record has a gap")
    ns = ap.parse_args()

    files = discover(ns.inputs)
    findings: list[Finding] = []
    for path in files:
        for idx, obj in iter_records(path):
            findings.append(audit_record(obj, path, idx))

    report = summarize(findings, files)
    report["canonical_report_sha256"] = canonical_sha256(report)
    text = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if ns.report:
        ns.report.parent.mkdir(parents=True, exist_ok=True)
        ns.report.write_text(text, encoding="utf-8")
    if ns.findings:
        ns.findings.parent.mkdir(parents=True, exist_ok=True)
        with ns.findings.open("w", encoding="utf-8") as fh:
            for f in findings:
                fh.write(json.dumps(asdict(f), ensure_ascii=False, sort_keys=True) + "\n")
    print(text, end="")
    if ns.strict and report["state"] != "PASS":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
