#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

GAP_KINDS = {
    "MISSING_SOURCE",
    "MISSING_EXECUTION",
    "MISSING_EVIDENCE",
    "MISSING_MAPPING",
    "MISSING_DECOMPOSITION",
    "MISSING_METRIC",
    "UNRESOLVED_AMBIGUITY",
    "OPEN_COVERAGE",
    "SYMBOLIC_SEMANTICS_UNBOUND",
}
GAP_STATES = {
    "TOKEN_VAZIO_NAVIGABLE",
    "TOKEN_VAZIO_NESTED",
    "TOKEN_VAZIO_NOT_RUN",
    "TOKEN_VAZIO_AMBIGUOUS",
    "PARTIAL_BOUNDED",
    "CLOSED_VERIFIED",
    "SUPERSEDED",
}
DECOMP_STATES = {
    "DECOMPOSED",
    "PARTIAL",
    "TOKEN_VAZIO_UNDECOMPOSED",
    "NOT_APPLICABLE",
}
CATALOG_STATES = {"NP_CATALOG", "P_CATALOG", "TOKEN_VAZIO"}
NOISE_CLASSES = {
    "NONE",
    "DELTA_P",
    "DELTA_NP",
    "DELTA_SECTION_NOISE",
    "MIXED",
    "TOKEN_VAZIO_UNCLASSIFIED",
}

def read_jsonl(path):
    rows = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{n}: invalid JSON: {exc}")
    return rows

def require(obj, keys, ctx):
    missing = [key for key in keys if key not in obj]
    if missing:
        raise SystemExit(f"{ctx}: missing {missing}")

def _nonempty_strings(values):
    return isinstance(values, list) and bool(values) and all(isinstance(v, str) and v for v in values)

def validate(path):
    rows = read_jsonl(path)
    ids = set()
    by_id = {}

    required = [
        "gap_id",
        "parent_gap_id",
        "kind",
        "summary",
        "origin_ref",
        "expected_type",
        "state",
        "decomposition_state",
        "child_gap_refs",
        "evidence_needed",
        "closure_criterion",
        "catalog_reduction",
        "noise",
        "markers",
        "claim_allowed",
    ]

    for i, obj in enumerate(rows, 1):
        ctx = f"gap[{i}]"
        require(obj, required, ctx)
        gid = obj["gap_id"]
        if not isinstance(gid, str) or not re.fullmatch(r"G\d{4,}", gid):
            raise SystemExit(f"{ctx}: bad gap_id")
        if gid in ids:
            raise SystemExit(f"{ctx}: duplicate gap_id")
        ids.add(gid)
        by_id[gid] = obj

        parent = obj["parent_gap_id"]
        if parent is not None and (not isinstance(parent, str) or not re.fullmatch(r"G\d{4,}", parent)):
            raise SystemExit(f"{ctx}: bad parent_gap_id")
        if parent == gid:
            raise SystemExit(f"{ctx}: self parent")

        if obj["kind"] not in GAP_KINDS:
            raise SystemExit(f"{ctx}: bad kind")
        if obj["state"] not in GAP_STATES:
            raise SystemExit(f"{ctx}: bad state")
        if obj["decomposition_state"] not in DECOMP_STATES:
            raise SystemExit(f"{ctx}: bad decomposition_state")

        for key in ("summary", "origin_ref", "expected_type"):
            if not isinstance(obj[key], str) or not obj[key]:
                raise SystemExit(f"{ctx}: empty {key}")

        children = obj["child_gap_refs"]
        if not isinstance(children, list) or len(children) != len(set(children)):
            raise SystemExit(f"{ctx}: bad child_gap_refs")
        if any(not isinstance(child, str) or not re.fullmatch(r"G\d{4,}", child) for child in children):
            raise SystemExit(f"{ctx}: bad child ref")
        if obj["decomposition_state"] == "PARTIAL" and not children:
            raise SystemExit(f"{ctx}: PARTIAL requires child_gap_refs")
        if obj["decomposition_state"] == "TOKEN_VAZIO_UNDECOMPOSED" and children:
            raise SystemExit(f"{ctx}: undecomposed gap cannot already list children")

        if not _nonempty_strings(obj["evidence_needed"]):
            raise SystemExit(f"{ctx}: bad evidence_needed")
        if not _nonempty_strings(obj["closure_criterion"]):
            raise SystemExit(f"{ctx}: bad closure_criterion")
        if not isinstance(obj["markers"], list) or any(not isinstance(v, str) or not v for v in obj["markers"]):
            raise SystemExit(f"{ctx}: bad markers")
        if obj["claim_allowed"] is not False:
            raise SystemExit(f"{ctx}: gap registry cannot promote claims")

        reduction = obj["catalog_reduction"]
        require(reduction, ["before", "after", "method", "complexity_claim"], f"{ctx}.catalog_reduction")
        if reduction["before"] not in CATALOG_STATES or reduction["after"] not in CATALOG_STATES:
            raise SystemExit(f"{ctx}: bad catalog state")
        if not isinstance(reduction["method"], str) or not reduction["method"]:
            raise SystemExit(f"{ctx}: empty reduction method")
        if reduction["complexity_claim"] is not False:
            raise SystemExit(f"{ctx}: catalog reduction must not be a P-vs-NP complexity claim")

        noise = obj["noise"]
        require(
            noise,
            ["class", "delta_p_catalog", "delta_np_catalog", "delta_section_noise", "classification_note"],
            f"{ctx}.noise",
        )
        if noise["class"] not in NOISE_CLASSES:
            raise SystemExit(f"{ctx}: bad noise class")
        for key in ("delta_p_catalog", "delta_np_catalog", "delta_section_noise"):
            value = noise[key]
            if value is not None and not isinstance(value, (int, float)):
                raise SystemExit(f"{ctx}: {key} must be number or null")
        if not isinstance(noise["classification_note"], str):
            raise SystemExit(f"{ctx}: classification_note must be string")

    for gid, obj in by_id.items():
        parent = obj["parent_gap_id"]
        if parent is not None and parent not in by_id:
            raise SystemExit(f"{gid}: missing parent {parent}")
        for child in obj["child_gap_refs"]:
            if child not in by_id:
                raise SystemExit(f"{gid}: missing child {child}")
            if by_id[child]["parent_gap_id"] != gid:
                raise SystemExit(f"{gid}: child {child} does not point back to parent")

    for gid in by_id:
        seen = set()
        cur = gid
        while cur is not None:
            if cur in seen:
                raise SystemExit(f"{gid}: parent cycle detected")
            seen.add(cur)
            cur = by_id[cur]["parent_gap_id"] if cur in by_id else None

    nested = sum(1 for obj in rows if obj["parent_gap_id"] is not None)
    print(json.dumps({
        "status": "PASS",
        "gaps": len(rows),
        "nested_gaps": nested,
        "claim_allowed": False,
        "complexity_claim": False,
    }, sort_keys=True))
    return rows

def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: validate_manifold_gap_registry.py GAPS.jsonl")
    validate(argv[1])

if __name__ == "__main__":
    main(sys.argv)
