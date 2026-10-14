#!/usr/bin/env python3
"""Hosted metadata-only fail-closed gate, NEVER a freestanding L0 dependency.

No Drive credentials, no network, no raw conversations, no chart execution.
This checks the published registry's internal contract; it does not attest
provider permissions, source authorship, legal status or scientific validity.
"""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/assurance/chart_component_atlas_20261014.v2.json"
EXPECTED_COUNTS = {
    "records": 51, "visual_mapa": 20, "office_third_party": 6,
    "dart_upstream": 3, "graphviz_representations": 6,
    "toroid_document": 1, "formal_models": 2,
    "rll_figures": 10, "native_sheet_registries": 3,
}
GUARDS = {
    "GLOBAL_DRIVE_SEARCH_NOT_NOVOEXPORT_MEMBERSHIP",
    "CHART_CACHE_NOT_MEASUREMENT", "SAME_NAME_NOT_SAME_BYTES",
    "SOURCE_NOT_ARTIFACT_NOT_EXECUTION_NOT_EVIDENCE_NOT_CLAIM",
    "TOKEN_VAZIO_NOT_ZERO", "DART_UPSTREAM_NOT_AUTHORIAL",
    "MAPA_ROUTES_NOT_PRODUCER_AUTHORITY", "CI_UNTESTED_NOT_PASS",
    "COOCCURRENCE_NOT_CAUSATION", "RLL_SMOKE_NOT_FINAL_FIT",
}


def validate(doc):
    faults = []
    if not isinstance(doc, dict):
        return ["ROOT_SCHEMA"]
    if doc.get("schema") != "rafaelia.chart-component-atlas/v2":
        faults.append("SCHEMA_DRIFT")
    if doc.get("status") != "SCOPED_OBSERVED_SOURCES_NOT_GLOBAL_COMPLETENESS":
        faults.append("FALSE_GLOBAL_COVERAGE")
    if doc.get("claim_allowed") is not False or doc.get("raw_private_payload_included") is not False:
        faults.append("UNSAFE_CLAIM_OR_PRIVACY")
    if doc.get("counts") != EXPECTED_COUNTS:
        faults.append("COUNT_SCOPE_DRIFT")
    if set(doc.get("invariants", [])) != GUARDS:
        faults.append("INVARIANT_DOWNGRADE")
    records = doc.get("records")
    if not isinstance(records, list):
        return faults + ["RECORDS_NOT_LIST"]
    ids = []
    classes = {}
    for item in records:
        if not isinstance(item, dict):
            faults.append("INVALID_RECORD")
            continue
        ids.append(item.get("id"))
        kind = item.get("kind")
        classes[kind] = classes.get(kind, 0) + 1
        if item.get("claim_allowed") is not False:
            faults.append("UNAUTHORIZED_RECORD_CLAIM")
        if not isinstance(item.get("source"), dict) or not item["source"].get("provider"):
            faults.append("MISSING_SOURCE")
        if not isinstance(item.get("gates"), list) or not item["gates"]:
            faults.append("MISSING_GATE")
        if kind == "OFFICE_OOXML_CHART_CACHE_SECURITY_FIXTURE":
            if item.get("state") != "THIRD_PARTY_CVE_FIXTURE_NOT_NOVOEXPORT" or item.get("upstream") != "METASPLOIT_SECURITY_FIXTURE":
                faults.append("FOREIGN_SOURCE_MISPROMOTION")
        if kind == "THIRD_PARTY_DART_UI_COMPONENT":
            if item.get("upstream") != "FLUTTER_GALLERY" or item.get("state") != "UPSTREAM_EXAMPLE_NOT_AUTHORIAL":
                faults.append("UPSTREAM_AUTHORSHIP_MISPROMOTION")
        if kind == "RLL_SCIENTIFIC_FIGURE":
            if item.get("id") != "RLL_F1" and item.get("state") == "DOC_READY":
                faults.append("RLL_UNEXECUTED_FIGURE_PROMOTION")
    if len(records) != 51 or len(set(ids)) != 51 or any(not isinstance(x, str) or not x for x in ids):
        faults.append("RECORD_IDENTITY_OR_CARDINALITY")
    if classes.get("SVG_SOURCE_VISUAL", 0) != 5 or classes.get("PNG_RASTER_VISUAL", 0) != 13:
        faults.append("VISUAL_TYPE_COUNTS")
    if classes.get("OFFICE_OOXML_CHART_CACHE_SECURITY_FIXTURE", 0) != 6:
        faults.append("OFFICE_FAMILY_COUNT")
    if classes.get("THIRD_PARTY_DART_UI_COMPONENT", 0) != 3:
        faults.append("DART_FAMILY_COUNT")
    if classes.get("RLL_SCIENTIFIC_FIGURE", 0) != 10:
        faults.append("RLL_FAMILY_COUNT")
    try:
        lookup = {x["id"]: x for x in records if isinstance(x, dict)}
        c = lookup["C42_CIRCULANT"]["components"]
        f = lookup["ICOSPHERE_F2"]["components"]
        if c["vertices"] != 42 or c["edges"] != 84 or f["vertices"] != 42 or f["edges"] != 120:
            faults.append("FALSE_GEOMETRIC_GRAPH_EQUIVALENCE")
    except (KeyError, TypeError):
        faults.append("MISSING_GRAPH_FIXTURES")
    return sorted(set(faults))


def self_test(document):
    if validate(document):
        return ["BASELINE_FAIL:" + ",".join(validate(document))]
    def apply(change):
        copy_doc = copy.deepcopy(document)
        change(copy_doc)
        return len(validate(copy_doc)) > 0
    cases = [
        lambda d: d.update(claim_allowed=True),
        lambda d: d.update(raw_private_payload_included=True),
        lambda d: d["records"].pop(),
        lambda d: d["records"][0].update(claim_allowed=True),
        lambda d: d["records"][0].update(gates=[]),
        lambda d: d["records"][20].update(state="AUTHORIAL_PASS"),
        lambda d: next(r for r in d["records"] if r["id"] == "C42_CIRCULANT")["components"].update(edges=120),
        lambda d: next(r for r in d["records"] if r["id"] == "ICOSPHERE_F2")["components"].update(edges=84),
        lambda d: next(r for r in d["records"] if r["id"] == "FLUTTER_RALLY_LINE_CHART").update(upstream="RAFAELIA_AUTHORIAL"),
        lambda d: d["records"].append(copy.deepcopy(d["records"][0])),
        lambda d: d["records"][0].update(source={}),
        lambda d: d["invariants"].remove("TOKEN_VAZIO_NOT_ZERO"),
        lambda d: next(r for r in d["records"] if r["id"] == "RLL_F9").update(state="DOC_READY"),
    ]
    return ["MUTATION_NOT_REJECTED:" + str(i + 1) for i,change in enumerate(cases) if not apply(change)]


def main():
    with SOURCE.open(encoding="utf-8") as handle:
        document = json.load(handle)
    faults = validate(document)
    if faults:
        print("CHART_COMPONENT_ATLAS=BLOCKED", ",".join(faults))
        return 1
    if "--self-test" in sys.argv:
        faults = self_test(document)
        if faults:
            print("CHART_COMPONENT_ATLAS_ADVERSARIAL=BLOCKED", ",".join(faults))
            return 1
        print("CHART_COMPONENT_ATLAS_NEGATIVE_MUTATIONS=13_REJECTED")
    print("CHART_COMPONENT_ATLAS=PASS_METADATA_ONLY_NOT_SOURCE_OR_RUNTIME")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
