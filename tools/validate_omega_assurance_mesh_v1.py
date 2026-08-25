#!/usr/bin/env python3
"""Fail-closed validator for the machine-readable Omega Assurance Mesh V1.

This validator proves structural and semantic contract integrity at one exact tree.
It does not prove runtime adoption, progress guarantees, performance, failover,
protocol interoperability, scientific claims, compliance, or certification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MESH_PATH = Path("data/control-plane/omega-assurance/omega-assurance-mesh.v1.json")
FIXTURE_ROOT = Path("data/fixtures/omega-assurance")

EXPECTED_AXES = ["D1", "D2", "D3", "D4", "D5", "D6", "D7"]
EXPECTED_THREADS = {
    "F_SOURCE", "F_BUILD", "F_RUNTIME", "F_EPISTEMIC",
    "F_SAFETY", "F_MEMORY", "F_SEMANTIC",
}
REQUIRED_INVARIANTS = {
    "TOKEN_VAZIO != PASS",
    "TOKEN_VAZIO != 0",
    "search_miss != absence",
    "prediction != evidence",
    "sandbox_pass != production_pass",
    "unknown_privacy => PRIVATE_DEFAULT_DENY",
    "unknown_authority => HOLD_FOR_AUTHORITY",
    "irreversible_unknown_risk => HOLD",
    "P0_non_compensatory = true",
}
REQUIRED_EPISTEMIC = {
    "OBSERVATION", "DEFINITION", "FORMULA", "DERIVATION", "HYPOTHESIS",
    "MODEL", "THEORY", "THEOREM", "PROOF", "EMPIRICAL_RESULT", "ANOMALY",
    "PARADOX", "COUNTEREXAMPLE", "FALSIFIER", "REFUTED", "REPLICATED",
    "META_ANALYSIS", "PARABLE", "ANALOGY", "TOKEN_VAZIO",
}
REQUIRED_ATTENTION = {
    "OBSERVED", "ACTIVE", "IGNORED_WITH_REASON", "IGNORED_WITHOUT_REASON",
    "DEFERRED", "ABORTED", "QUARANTINED", "SUPERSEDED", "DEPRECATED",
    "WITHHELD_BY_POLICY", "REDACTED_PRIVACY", "UNREVIEWED", "UNREACHABLE",
    "ORPHANED", "CONTRADICTED", "ANOMALOUS", "PARADOXICAL", "FALSIFIED",
    "TOKEN_VAZIO", "FORGOTTEN", "NORMALIZED", "DISMISSED", "LOW_PRIORITY",
    "ABANDONED", "REOPENED", "RECOVERED", "CLOSED",
}
REQUIRED_DOMAINS = {
    "LOCK_FREE", "PROFILING_BENCHMARKING", "SMART_GUARD",
    "PHASE_INTEGRATION", "NETWORK_PROTOCOL", "QUERY_SYSTEM", "RLL_COSMOLOGY",
}
MUTATING_OPERATIONS = {"MUTATE", "PROMOTE", "PUBLISH", "DELETE"}
PRIVATE_LOCATOR_PATTERNS = (
    re.compile(r"https?://drive\.google\.com/", re.I),
    re.compile(r"https?://docs\.google\.com/(?:document|spreadsheets|presentation)/d/", re.I),
    re.compile(r"\bdrive:[A-Za-z0-9_-]{16,}", re.I),
)


def load_json(root: Path, relative: str | Path) -> Any:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def is_token_vazio(value: Any) -> bool:
    return isinstance(value, dict) and value.get("state") == "TOKEN_VAZIO"


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def require_keys(errors: list[str], obj: Any, keys: set[str], label: str) -> None:
    if not isinstance(obj, dict):
        errors.append(f"{label} must be an object")
        return
    missing = sorted(keys - set(obj))
    if missing:
        errors.append(f"{label} missing keys: {missing}")


def validate_node(node: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    add(errors, node.get("schema_version") == "rafaelia.omega7-node/v1", "node schema_version mismatch")
    for key in ("D1_identity", "D2_epistemic", "D3_execution", "D4_safety", "D5_privacy", "D6_authority", "D7_transition"):
        add(errors, isinstance(node.get(key), dict), f"node missing {key}")
    if errors:
        return errors

    claim = node.get("claim_allowed")
    d1 = node["D1_identity"]
    d2 = node["D2_epistemic"]
    d5 = node["D5_privacy"]
    d6 = node["D6_authority"]
    promotion = node.get("promotion_gate", {})
    evidence = node.get("evidence", [])

    if d2.get("state") == "TOKEN_VAZIO":
        add(errors, claim is False, "TOKEN_VAZIO node cannot allow claim")
    if d5.get("classification") == "TOKEN_VAZIO":
        add(errors, d5.get("disclosure_state") in {"DENY", "HOLD"}, "unknown privacy must deny or hold disclosure")
        add(errors, claim is False, "unknown privacy cannot allow claim")
    if is_token_vazio(d6.get("owner")):
        add(errors, d6.get("write_state") in {"DENY", "HOLD"}, "unknown owner cannot allow write")
        add(errors, d6.get("promotion_state") in {"DENY", "HOLD"}, "unknown owner cannot allow promotion")
        add(errors, claim is False, "unknown owner cannot allow claim")
    if claim is True:
        add(errors, promotion.get("state") == "CLOSED_PASS", "claim requires CLOSED_PASS promotion gate")
        add(errors, d6.get("promotion_state") == "ALLOW", "claim requires promotion authority")
        add(errors, bool(evidence), "claim requires evidence")
        add(errors, d1.get("provenance_state") == "BOUND", "claim requires bound provenance")
        add(errors, not any(is_token_vazio(d1.get(k)) for k in ("source", "revision", "digest")), "claim cannot retain unknown identity")
    add(errors, isinstance(node.get("relations"), list), "node relations must be a list")
    relation_ids = [r.get("relation_id") for r in node.get("relations", []) if isinstance(r, dict)]
    add(errors, len(relation_ids) == len(set(relation_ids)), "node relation IDs must be unique")
    return errors


def validate_transition(event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    add(errors, event.get("schema_version") == "rafaelia.omega-transition/v1", "transition schema_version mismatch")
    add(errors, event.get("append_only") is True, "transition must be append-only")
    add(errors, event.get("from_state") != event.get("to_state"), "transition must change state")
    authority = event.get("authority", {})
    claim = event.get("claim_allowed")
    if authority.get("state") in {"DENY", "HOLD"} or is_token_vazio(authority.get("owner")):
        add(errors, claim is False, "denied, held or unknown authority cannot allow claim")
    if event.get("privacy_class") == "TOKEN_VAZIO":
        add(errors, authority.get("state") in {"DENY", "HOLD"}, "unknown privacy must deny or hold authority")
        add(errors, claim is False, "unknown privacy cannot allow claim")
    rollback = event.get("rollback", {})
    if authority.get("operation") in MUTATING_OPERATIONS and rollback.get("state") == "TOKEN_VAZIO":
        add(errors, event.get("watchdog_state") == "HOLD", "irreversible unknown risk must HOLD")
        add(errors, claim is False, "unknown rollback on material mutation cannot allow claim")
    p0 = set(event.get("risk_after", {}).get("p0_dimensions", []))
    if p0:
        add(errors, event.get("watchdog_state") == "HOLD", "P0 transition must HOLD")
        add(errors, claim is False, "P0 transition cannot allow claim")
    return errors


def validate_watchdog_event(event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    add(errors, event.get("schema_version") == "rafaelia.omega-watchdog-event/v1", "watchdog schema_version mismatch")
    action = event.get("action_mode")
    claim = event.get("claim_allowed")
    if event.get("severity") == "P0":
        add(errors, action == "HOLD", "P0 watchdog event must HOLD")
        add(errors, claim is False, "P0 watchdog event cannot allow claim")
    if event.get("evidence_state") == "TOKEN_VAZIO":
        add(errors, action in {"WATCH", "WARN", "HOLD"}, "unknown evidence cannot trigger ACT_BOUNDED")
        add(errors, claim is False, "unknown evidence cannot allow claim")
    if action == "ACT_BOUNDED":
        add(errors, event.get("authority_state") == "ALLOW", "ACT_BOUNDED requires authority")
        add(errors, event.get("privacy_state") in {"PUBLIC", "KNOWN_RESTRICTED"}, "ACT_BOUNDED requires known privacy")
        add(errors, event.get("rollback_state") in {"READY", "REHEARSED_LOCAL"}, "ACT_BOUNDED requires rollback")
    if event.get("heartbeat_state") in {"STALE", "FAILED", "TOKEN_VAZIO"}:
        add(errors, action == "HOLD", "unhealthy watchdog heartbeat must HOLD")
        add(errors, claim is False, "unhealthy heartbeat cannot allow claim")
    return errors


def event_digest(event: dict[str, Any]) -> str:
    payload = dict(event)
    payload.pop("event_hash_sha256", None)
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_ledger(root: Path, relative: str) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    previous_hash: str | None = None
    for line_no, raw in enumerate((root / relative).read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"ledger line {line_no} invalid JSON: {exc}")
            continue
        event_id = event.get("event_id")
        add(errors, isinstance(event_id, str) and event_id not in seen, f"ledger line {line_no} duplicate or missing event_id")
        if isinstance(event_id, str):
            seen.add(event_id)
        add(errors, event.get("claim_allowed") is False, f"ledger line {line_no} must keep claim_allowed=false")
        add(errors, event.get("previous_event_sha256") == previous_hash, f"ledger line {line_no} hash chain mismatch")
        expected = event_digest(event)
        add(errors, event.get("event_hash_sha256") == expected, f"ledger line {line_no} event hash mismatch")
        previous_hash = expected
    add(errors, bool(seen), "ledger must contain at least one event")
    return errors


def contains_private_locator(text: str) -> bool:
    return any(pattern.search(text) for pattern in PRIVATE_LOCATOR_PATTERNS)


def validate_bundle(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    mesh = load_json(root, MESH_PATH)
    add(errors, mesh.get("schema_version") == "rafaelia.omega-assurance-mesh/v1", "mesh schema_version mismatch")
    add(errors, mesh.get("status") == "DRAFT_FAIL_CLOSED", "mesh must remain DRAFT_FAIL_CLOSED")
    add(errors, mesh.get("claim_allowed") is False, "mesh claim_allowed must be false")
    add(errors, mesh.get("append_only") is True, "mesh must be append-only")
    add(errors, [a.get("id") for a in mesh.get("axes", [])] == EXPECTED_AXES, "mesh axes must be exact ordered D1..D7")
    add(errors, set(mesh.get("orthogonal_axes", [])) == set(EXPECTED_AXES), "orthogonal axis set mismatch")
    add(errors, set(mesh.get("multifilament_threads", [])) == EXPECTED_THREADS, "multifilament thread set mismatch")
    add(errors, REQUIRED_INVARIANTS.issubset(set(mesh.get("fail_closed_invariants", []))), "required fail-closed invariant missing")

    contracts = mesh.get("contracts", {})
    for name, relative in contracts.items():
        add(errors, isinstance(relative, str) and (root / relative).is_file(), f"contract {name} missing: {relative}")

    for schema_key in ("node_schema", "transition_schema", "watchdog_event_schema"):
        schema = load_json(root, contracts[schema_key])
        add(errors, schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", f"{schema_key} draft mismatch")
        add(errors, schema.get("additionalProperties") is False, f"{schema_key} must close additional properties")
        add(errors, "claim_allowed" in schema.get("required", []), f"{schema_key} must require claim_allowed")
        add(errors, bool(schema.get("allOf")), f"{schema_key} must encode fail-closed conditionals")

    epistemic = load_json(root, contracts["epistemic_registry"])
    observed_epistemic = {s.get("id") for s in epistemic.get("states", [])}
    add(errors, REQUIRED_EPISTEMIC.issubset(observed_epistemic), "epistemic state set incomplete")
    domain_set = {d.get("domain") for d in epistemic.get("domain_gates", [])}
    add(errors, REQUIRED_DOMAINS.issubset(domain_set), "epistemic domain gates incomplete")

    attention = load_json(root, contracts["attention_registry"])
    observed_attention = {s.get("id") for s in attention.get("states", [])}
    add(errors, REQUIRED_ATTENTION.issubset(observed_attention), "attention state set incomplete")
    add(errors, any("nonappearance" in rule for rule in attention.get("inference_rules", [])), "attention registry must forbid censorship inference")

    risk = load_json(root, contracts["risk_vector"])
    add(errors, [d.get("symbol") for d in risk.get("core_dimensions", [])] == list("ASPGIVCU"), "risk vector must be R=(A,S,P,G,I,V,C,U)")
    non_comp = {d.get("id") for d in risk.get("core_dimensions", []) if d.get("non_compensatory") is True}
    add(errors, {"authority", "security", "privacy", "governance", "reversibility", "uncertainty"}.issubset(non_comp), "risk non-compensatory set incomplete")
    add(errors, risk.get("unknown_is_zero") is False, "unknown risk must not become zero")
    add(errors, risk.get("p0_non_compensatory") is True, "P0 must be non-compensatory")

    cross = load_json(root, contracts["cross_layer_matrix"])
    add(errors, {c.get("id") for c in cross.get("layer_cases", [])} == {"XF-D1-D2", "XF-D2-D6", "XF-D3-D4", "XF-D4-D5", "XF-D5-D6", "XF-D6-D7", "XF-D7-HISTORY"}, "cross-layer case set mismatch")
    add(errors, REQUIRED_DOMAINS.issubset({d.get("domain") for d in cross.get("domain_routes", [])}), "cross-layer domain routes incomplete")
    add(errors, "TEST_DO_NOT_OVERREACT" in cross.get("test_families", []), "do-not-overreact test missing")

    auth = load_json(root, contracts["authorization_matrix"])
    add(errors, auth.get("default") == "HOLD_FOR_AUTHORITY", "authorization default must HOLD")
    add(errors, {o.get("id") for o in auth.get("operations", [])} == {"READ", "WRITE", "MUTATE", "PROMOTE", "PUBLISH", "DELETE"}, "authorization operation set mismatch")

    rollback = load_json(root, contracts["rollback_registry"])
    add(errors, rollback.get("meta_watch", {}).get("watchdog_depth_limit") == 2, "meta-watch depth must be bounded at 2")
    add(errors, any("creative adaptation" in rule for rule in rollback.get("rules", [])), "rollback registry must forbid creative recovery after failure")

    relations = load_json(root, contracts["relation_registry"])
    relation_ids = [r.get("id") for r in relations.get("relation_types", [])]
    add(errors, len(relation_ids) == len(set(relation_ids)), "relation type IDs must be unique")
    add(errors, {"DEPENDS_ON", "IMPLEMENTS", "TESTS", "FALSIFIES", "SUPERSEDES", "AUTHORIZED_BY", "TOKEN_VAZIO_RELATION"}.issubset(set(relation_ids)), "structural relation types incomplete")

    scales = load_json(root, contracts["scale_lattice"])
    levels = scales.get("ordered_levels", [])
    level_ids = [level.get("id") for level in levels]
    add(errors, level_ids == ["META", "FEDERATION", "SYSTEM", "DOMAIN", "COMPONENT", "ARTIFACT", "RECORD", "FIELD", "TOKEN", "BIT", "YOCTO"], "scale lattice order mismatch")
    for index, level in enumerate(levels):
        expected_parent = None if index == 0 else levels[index - 1].get("id")
        add(errors, level.get("parent") == expected_parent, f"scale parent mismatch at {level.get('id')}")
    add(errors, any("YOCTO" in rule and "TOKEN_VAZIO" in rule for rule in scales.get("rules", [])), "YOCTO fail-closed rule missing")

    errors.extend(validate_node(load_json(root, FIXTURE_ROOT / "valid-node.v1.json")))
    errors.extend(validate_transition(load_json(root, FIXTURE_ROOT / "valid-transition.v1.json")))
    errors.extend(validate_watchdog_event(load_json(root, FIXTURE_ROOT / "valid-watchdog-event.v1.json")))
    errors.extend(validate_ledger(root, contracts["event_ledger"]))

    negative_sets = [
        validate_node(load_json(root, FIXTURE_ROOT / "invalid-token-vazio-promotion.v1.json")),
        validate_transition(load_json(root, FIXTURE_ROOT / "invalid-authority-transition.v1.json")),
        validate_watchdog_event(load_json(root, FIXTURE_ROOT / "invalid-watchdog-overreaction.v1.json")),
    ]
    for index, result in enumerate(negative_sets, 1):
        add(errors, bool(result), f"negative fixture {index} unexpectedly passed")

    receipt_paths = [
        str(path.relative_to(root))
        for path in sorted((root / "data/receipts").glob("OMEGA_ASSURANCE_MESH_V1_*.json"))
    ]
    public_paths = list(contracts.values()) + ["indices/OMEGA_ASSURANCE_MESH_V1.md"] + receipt_paths
    for relative in public_paths:
        path = root / relative
        if path.is_file():
            add(errors, not contains_private_locator(path.read_text(encoding="utf-8")), f"private locator found in {relative}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate_bundle(args.root)
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({
        "status": "PASS",
        "mesh": "OMEGA_ASSURANCE_MESH_V1",
        "axes": 7,
        "multifilament_threads": 7,
        "negative_fixtures_rejected": 3,
        "claim_allowed": False,
        "proof_scope": "STRUCTURAL_FAIL_CLOSED_CONTRACT_ONLY",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
