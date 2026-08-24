#!/usr/bin/env python3
"""Fail-closed validator for RAFAELIA Ω Assurance Skills V1."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills" / "omega-assurance-skills.v1.json"

EXPECTED_IDS = {
    "omega-assurance-router",
    "identity-provenance",
    "epistemic-discernment",
    "execution-evidence",
    "resilience-safety",
    "privacy-information",
    "authority-governance",
    "transition-ledger",
    "knowledge-attention",
    "crossfail-secure-sandbox",
}

REQUIRED_MARKERS = {
    "omega-assurance-router": ["SEE_MORE != CLAIM_MORE", "CAN_DO != MAY_DO", "F_ok", "F_gap", "F_next"],
    "identity-provenance": ["search_miss != absence", "TOKEN_VAZIO_PROVIDER"],
    "epistemic-discernment": ["HYPOTHESIS", "THEOREM", "PARABLE", "falsifier"],
    "execution-evidence": ["fixture != live", "sandbox_pass != production_pass"],
    "resilience-safety": ["minimum sufficient intervention", "FAIL_CLOSED_HOLD", "P0"],
    "privacy-information": ["PRIVATE_DEFAULT_DENY", "TOKEN_VAZIO_REASON"],
    "authority-governance": ["capability != authority", "HOLD_FOR_AUTHORITY"],
    "transition-ledger": ["NO_STATE_TRANSITION_WITHOUT_REASON", "append_only=true"],
    "knowledge-attention": ["FORGOTTEN", "IGNORED_WITHOUT_REASON", "HISTORICAL_ONLY"],
    "crossfail-secure-sandbox": ["TEST_DO_NOT_OVERREACT", "TEST_AUTHORITY_DENY", "TEST_WATCHDOG_FAILURE"],
}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    out: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def validate_dependency_graph(skills: list[dict]) -> list[str]:
    errors: list[str] = []
    ids = {s.get("id") for s in skills}
    graph = {s["id"]: list(s.get("depends_on", [])) for s in skills if s.get("id")}
    for skill_id, deps in graph.items():
        for dep in deps:
            if dep not in ids:
                errors.append(f"{skill_id}: unknown dependency {dep}")
            if dep == skill_id:
                errors.append(f"{skill_id}: self dependency")

    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(node: str) -> None:
        if node in visiting:
            errors.append(f"dependency cycle at {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dep in graph.get(node, []):
            if dep in graph:
                dfs(dep)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        dfs(node)
    return errors


def validate_registry(data: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "rafaelia.omega-assurance-skills/v1":
        errors.append("schema_version mismatch")
    if data.get("claim_allowed") is not False:
        errors.append("registry claim_allowed must be false")
    if data.get("router") != "omega-assurance-router":
        errors.append("router mismatch")

    skills = data.get("skills")
    if not isinstance(skills, list):
        return errors + ["skills must be a list"]
    ids = [s.get("id") for s in skills]
    if len(ids) != len(set(ids)):
        errors.append("duplicate skill id")
    if set(ids) != EXPECTED_IDS:
        errors.append(f"skill set mismatch: {sorted(set(ids) ^ EXPECTED_IDS)}")

    errors.extend(validate_dependency_graph(skills))

    for skill in skills:
        skill_id = skill.get("id")
        rel = skill.get("path")
        if not skill_id or not rel:
            errors.append("skill missing id/path")
            continue
        path = root / rel
        if not path.is_file():
            errors.append(f"{skill_id}: missing {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        if meta.get("name") != skill_id:
            errors.append(f"{skill_id}: frontmatter name mismatch")
        if meta.get("version") != "1.0.0":
            errors.append(f"{skill_id}: version mismatch")
        if meta.get("status") != "DRAFT_FAIL_CLOSED":
            errors.append(f"{skill_id}: status must be DRAFT_FAIL_CLOSED")
        if not meta.get("description"):
            errors.append(f"{skill_id}: description missing")
        for marker in REQUIRED_MARKERS.get(skill_id, []):
            if marker not in text:
                errors.append(f"{skill_id}: required marker missing: {marker}")
        if re.search(r"drive:[A-Za-z0-9_-]{16,}", text):
            errors.append(f"{skill_id}: private Drive-style locator must not be embedded")

    invariants = set(data.get("fail_closed_invariants", []))
    for required in {
        "TOKEN_VAZIO != PASS",
        "prediction != evidence",
        "capability != authority",
        "sandbox_pass != production_pass",
        "search_miss != absence",
        "unknown_privacy => PRIVATE_DEFAULT_DENY",
        "unknown_authority => HOLD_FOR_AUTHORITY",
        "irreversible_unknown_risk => HOLD",
    }:
        if required not in invariants:
            errors.append(f"missing fail-closed invariant: {required}")
    return errors


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    errors = validate_registry(data)
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({
        "status": "PASS",
        "schema": data["schema_version"],
        "skills": len(data["skills"]),
        "claim_allowed": data["claim_allowed"],
        "dependency_graph": "ACYCLIC",
        "private_locator_scan": "PASS",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
