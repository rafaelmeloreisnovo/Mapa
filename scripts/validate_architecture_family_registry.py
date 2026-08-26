#!/usr/bin/env python3
"""Dependency-free structural gate for RAFAELIA architecture-family semantics."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/ontology/architectures/ARCHITECTURE_FAMILY_REGISTRY_V1.yaml"
INDEX = ROOT / "indices/semantic/ARCHITECTURE_FAMILY_INDEX_V1.yaml"
RULES = ROOT / "data/ontology/architectures/ARCHITECTURE_DISCOVERY_RULES_V1.json"
DISCOVERY = ROOT / "scripts/discover_architecture_families.py"
DISCOVERY_TEST = ROOT / "tests/test_architecture_discovery.py"
DISCOVERY_FIXTURE = ROOT / "tests/fixtures/architecture_discovery/novoexport_sample.json"

REQUIRED_REGISTRY_MARKERS = (
    "schema: rafaelia.architecture-family-registry/v1",
    "claim_allowed: false",
    "TOKEN_VAZIO != ZERO",
    "HISTORICAL_ASSISTANT_ASSERTION != PRIMARY_EVIDENCE",
    "PROVENANCE_PRECEDES_PROMOTION",
    "families:",
    "unresolved_terms:",
    "next_verifiable_steps:",
)

REQUIRED_INDEX_MARKERS = (
    "schema: rafaelia.architecture-family-index/v1",
    "claim_allowed: false",
    "source_registry: data/ontology/architectures/ARCHITECTURE_FAMILY_REGISTRY_V1.yaml",
    "discovery_rules: data/ontology/architectures/ARCHITECTURE_DISCOVERY_RULES_V1.json",
    "discovery_pipeline: scripts/discover_architecture_families.py",
    "default_when_missing: TOKEN_VAZIO",
)

FORBIDDEN_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*[A-Za-z0-9_./+\-=]{12,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def ids_from_registry(text: str) -> list[str]:
    return re.findall(r"^  - id: (ARCH-[A-Z0-9-]+)\s*$", text, flags=re.MULTILINE)


def architecture_refs(text: str) -> set[str]:
    return set(re.findall(r"\bARCH-[A-Z0-9-]+\b", text))


def validate_rules(known: set[str]) -> tuple[int, int]:
    rules_text = read(RULES)
    try:
        data = json.loads(rules_text)
    except json.JSONDecodeError as exc:
        fail(f"invalid discovery rules JSON: {exc}")
    if data.get("schema") != "rafaelia.architecture-discovery-rules/v1":
        fail("unexpected discovery rules schema")
    if data.get("claim_allowed") is not False:
        fail("discovery rules must keep claim_allowed=false")
    privacy = data.get("privacy", {})
    if privacy.get("emit_raw_text") is not False:
        fail("discovery rules must prohibit raw text emission")

    rule_ids = [rule.get("id") for rule in data.get("rules", [])]
    if not rule_ids or any(not rid for rid in rule_ids):
        fail("discovery rules require non-empty IDs")
    if len(rule_ids) != len(set(rule_ids)):
        fail("duplicate architecture discovery rule IDs")

    unknown_refs = sorted(
        {rule.get("architecture_id") for rule in data["rules"] if rule.get("architecture_id")}
        - known
    )
    if unknown_refs:
        fail(f"discovery rules reference unknown architecture IDs: {unknown_refs}")

    token_vazio_rules = 0
    for rule in data["rules"]:
        state = str(rule.get("state", ""))
        if rule.get("architecture_id") is None:
            if not state.startswith("TOKEN_VAZIO"):
                fail(f"unresolved discovery rule must remain TOKEN_VAZIO: {rule.get('id')}")
            token_vazio_rules += 1
        if not rule.get("patterns"):
            fail(f"discovery rule missing patterns: {rule.get('id')}")

    for signal in data.get("structural_signals", []):
        if not signal.get("id") or not signal.get("kind_hint") or not signal.get("patterns"):
            fail("malformed structural signal rule")

    for pattern in FORBIDDEN_PATTERNS:
        if pattern.search(rules_text):
            fail("possible secret material detected in public discovery rules")

    return len(rule_ids), token_vazio_rules


def validate() -> None:
    registry = read(REGISTRY)
    index = read(INDEX)
    read(DISCOVERY)
    read(DISCOVERY_TEST)
    read(DISCOVERY_FIXTURE)

    for marker in REQUIRED_REGISTRY_MARKERS:
        if marker not in registry:
            fail(f"registry missing invariant/section: {marker}")
    for marker in REQUIRED_INDEX_MARKERS:
        if marker not in index:
            fail(f"index missing invariant/section: {marker}")

    ids = ids_from_registry(registry)
    if not ids:
        fail("no architecture family IDs found")
    if len(ids) != len(set(ids)):
        dupes = sorted({x for x in ids if ids.count(x) > 1})
        fail(f"duplicate architecture IDs: {dupes}")

    known = set(ids)
    referenced = architecture_refs(index)
    missing = sorted(referenced - known)
    if missing:
        fail(f"index references unknown architecture IDs: {missing}")

    unresolved_block = registry.split("unresolved_terms:", 1)[-1].split("source_registry:", 1)[0]
    unresolved_terms = re.findall(r"^  - term: .+$", unresolved_block, flags=re.MULTILINE)
    unresolved_states = re.findall(r"^    state: (.+)$", unresolved_block, flags=re.MULTILINE)
    if len(unresolved_terms) != len(unresolved_states):
        fail("every unresolved term must have exactly one explicit state")
    bad_states = [state for state in unresolved_states if not state.startswith("TOKEN_VAZIO")]
    if bad_states:
        fail(f"unresolved terms must remain TOKEN_VAZIO states: {bad_states}")

    for pattern in FORBIDDEN_PATTERNS:
        if pattern.search(registry) or pattern.search(index):
            fail("possible secret material detected in public semantic artifacts")

    if "PRIVATE_POINTER_ONLY" not in registry:
        fail("private source pointers must stay pointer-only")

    rules_count, unresolved_rules = validate_rules(known)

    print(
        "PASS architecture-family-registry-v1 "
        f"families={len(ids)} unresolved={len(unresolved_terms)} "
        f"discovery_rules={rules_count} token_vazio_rules={unresolved_rules} claim_allowed=false"
    )


if __name__ == "__main__":
    validate()
