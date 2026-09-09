#!/usr/bin/env python3
import json
import sys
from pathlib import Path

EXPECTED = set(range(10))


def fail(msg):
    print(json.dumps({"status":"FAIL","error":msg,"canonical_mapping_allowed":False,"claim_allowed":False}, sort_keys=True))
    raise SystemExit(1)


def main():
    if len(sys.argv) != 2:
        fail("usage: validate_rafbit_context_hypergraph.py <file.json>")
    doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if doc.get("schema_version") != "rafaelia.rafbit-context-hypergraph/v1":
        fail("schema_version mismatch")
    if doc.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")
    domain = doc.get("domain", {})
    states = domain.get("states")
    if states != list(range(10)):
        fail("domain states must be exactly 0..9")
    edges = doc.get("hyperedges")
    if not isinstance(edges, list) or not edges:
        fail("hyperedges required")
    coverage = set()
    occurrences = {i:0 for i in range(10)}
    for i, edge in enumerate(edges):
        members = edge.get("digit_members")
        if not isinstance(members, list) or not members:
            fail(f"hyperedges[{i}].digit_members required")
        if any((not isinstance(v, int)) or v not in EXPECTED for v in members):
            fail(f"hyperedges[{i}] contains invalid digit")
        if len(set(members)) != len(members):
            fail(f"hyperedges[{i}] contains duplicate digit")
        if not isinstance(edge.get("label"), str) or not edge["label"]:
            fail(f"hyperedges[{i}].label required")
        if not isinstance(edge.get("source_anchor"), str) or not edge["source_anchor"]:
            fail(f"hyperedges[{i}].source_anchor required")
        for v in members:
            coverage.add(v)
            occurrences[v] += 1
    if coverage != EXPECTED:
        fail("context coverage must include all RafBit digits 0..9")
    derived = doc.get("derived", {})
    if derived.get("canonical_single_state_label_supported") is not False:
        fail("context hypergraph must not promote canonical state labels")
    if derived.get("bitomega_equivalence_supported") is not False:
        fail("context hypergraph must not promote BitOmega equivalence")
    operational = doc.get("operational_contexts", [])
    for i, item in enumerate(operational):
        if item.get("classification") != "OPERATIONAL_HEURISTIC_NOT_ONTOLOGY":
            fail(f"operational_contexts[{i}] must remain heuristic-not-ontology")
    out = {
        "status":"PASS",
        "coverage":sorted(coverage),
        "all_10_digits_contextually_observed":True,
        "occurrences":{str(k):occurrences[k] for k in range(10)},
        "many_to_many_contexts_observed":any(v > 1 for v in occurrences.values()),
        "canonical_mapping_allowed":False,
        "bitomega_equivalence_allowed":False,
        "claim_allowed":False,
    }
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
