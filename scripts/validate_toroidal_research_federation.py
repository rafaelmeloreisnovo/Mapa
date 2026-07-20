#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA = "mapa.toroidal-research-federation.v1"
STATES = {"ACTIVE", "ADAPTER_PLANNED", "TOKEN_VAZIO"}
ROLES = {
    "GOVERNANCE",
    "MAP",
    "SCIENCE",
    "ORCHESTRATION",
    "RUNTIME",
    "MEMORY",
}
RUNTIME_EVIDENCE_STATES = {
    "TOKEN_VAZIO",
    "DEVICE_OBSERVED_INCOMPLETE",
    "DEVICE_RECEIPT_COMPLETE",
}
MEMORY_OBSERVATION_STATES = {
    "TOKEN_VAZIO",
    "SYNCED_BOUNDED",
    "STALE_CONSUMER",
    "CLAIM_BLOCKED",
}
HEX40 = re.compile(r"^[0-9a-f]{40}$")


class ValidationError(ValueError):
    pass


def load(path: Path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(str(exc)) from exc
    if not isinstance(data, dict):
        raise ValidationError("root must be object")
    return data


def digest(data):
    clone = json.loads(json.dumps(data))
    clone.setdefault("integrity", {})["digest"] = ""
    raw = json.dumps(
        clone,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.blake2b(raw, digest_size=32).hexdigest()


def validate(data):
    errors = []
    if data.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")

    contract = data.get("canonical_contract", {})
    if contract.get("repository") != "rafaelmeloreisnovo/RafGitTools":
        errors.append("canonical contract authority mismatch")
    if contract.get("schema") != "rafaelia.toroidal-research-cycle-contract.v1":
        errors.append("canonical contract schema mismatch")

    governance = data.get("governance", {})
    if governance.get("authority_repository") != "rafaelmeloreisnovo/Mapa":
        errors.append("Mapa must own the registry")
    if governance.get("claim_allowed") is not False:
        errors.append("registry must remain claim_allowed=false")

    repos = data.get("repositories")
    if not isinstance(repos, list):
        errors.append("repositories must be array")
        repos = []
    by_id = {}
    by_name = {}
    by_role = {}

    for index, repository in enumerate(repos):
        if not isinstance(repository, dict):
            errors.append(f"repositories[{index}] must be object")
            continue
        rid = repository.get("id")
        name = repository.get("full_name")
        role = repository.get("role")
        state = repository.get("state")
        if not isinstance(rid, str) or not rid:
            errors.append(f"repositories[{index}].id invalid")
            continue
        if rid in by_id:
            errors.append(f"duplicate repository id: {rid}")
        by_id[rid] = repository

        if not isinstance(name, str) or "/" not in name:
            errors.append(f"{rid}.full_name invalid")
        elif name in by_name:
            errors.append(f"duplicate full_name: {name}")
        else:
            by_name[name] = rid

        if role not in ROLES:
            errors.append(f"{rid}.role invalid")
        elif role in by_role:
            errors.append(f"duplicate role: {role}")
        else:
            by_role[role] = rid

        if state not in STATES:
            errors.append(f"{rid}.state invalid")
        dependencies = repository.get("depends_on")
        if not isinstance(dependencies, list):
            errors.append(f"{rid}.depends_on must be array")

        if state == "ACTIVE":
            for field in ("artifact_path", "evidence_locator"):
                if (
                    not isinstance(repository.get(field), str)
                    or not repository[field]
                    or repository[field] == "TOKEN_VAZIO"
                ):
                    errors.append(f"{rid}.{field} required for ACTIVE")
        else:
            criteria = repository.get("exit_criteria")
            if not isinstance(criteria, list) or not criteria:
                errors.append(f"{rid}.exit_criteria required for {state}")

        if role == "RUNTIME" and state == "ACTIVE":
            device_state = repository.get("device_evidence_state")
            if device_state not in RUNTIME_EVIDENCE_STATES:
                errors.append(f"{rid}.device_evidence_state invalid")
            if device_state != "DEVICE_RECEIPT_COMPLETE":
                criteria = repository.get("device_evidence_exit_criteria")
                if not isinstance(criteria, list) or not criteria:
                    errors.append(
                        f"{rid}.device_evidence_exit_criteria required"
                    )

        if role == "MEMORY" and state == "ACTIVE":
            observation = repository.get("latest_state_observation")
            if observation not in MEMORY_OBSERVATION_STATES:
                errors.append(f"{rid}.latest_state_observation invalid")
            observed_head = repository.get("producer_head_observed")
            if observation == "SYNCED_BOUNDED" and (
                not isinstance(observed_head, str)
                or HEX40.fullmatch(observed_head) is None
            ):
                errors.append(
                    f"{rid}.producer_head_observed required for SYNCED_BOUNDED"
                )

    if set(by_role) != ROLES:
        errors.append("roles must contain exactly one of each canonical role")

    for rid, repository in by_id.items():
        for dependency in repository.get("depends_on", []):
            if dependency not in by_id:
                errors.append(f"{rid} depends on unknown id: {dependency}")
            if dependency == rid:
                errors.append(f"{rid} self dependency")

    edges = data.get("edges")
    if not isinstance(edges, list):
        errors.append("edges must be array")
        edges = []
    seen = set()
    adjacency = {rid: [] for rid in by_id}
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"edges[{index}] must be object")
            continue
        source = edge.get("from")
        target = edge.get("to")
        key = (source, target, edge.get("relation"))
        if key in seen:
            errors.append(f"duplicate edge: {key}")
        seen.add(key)
        if source not in by_id or target not in by_id:
            errors.append(f"edge references unknown node: {source}->{target}")
        elif source == target:
            errors.append(f"self edge: {source}")
        else:
            adjacency[source].append(target)
        if not isinstance(edge.get("relation"), str) or not edge["relation"]:
            errors.append(f"edges[{index}].relation invalid")

    visiting = set()
    visited = set()
    cycle = False

    def dfs(node):
        nonlocal cycle
        if node in visiting:
            cycle = True
            return
        if node in visited:
            return
        visiting.add(node)
        for nxt in adjacency.get(node, []):
            dfs(nxt)
        visiting.remove(node)
        visited.add(node)

    for node in adjacency:
        dfs(node)
    if cycle:
        errors.append("federation graph must be acyclic")

    gaps = data.get("open_evidence_gaps")
    if not isinstance(gaps, list):
        errors.append("open_evidence_gaps must be array")
        gaps = []
    gap_ids = set()
    for index, gap in enumerate(gaps):
        if not isinstance(gap, dict):
            errors.append(f"open_evidence_gaps[{index}] must be object")
            continue
        gap_id = gap.get("id")
        if not isinstance(gap_id, str) or not gap_id:
            errors.append(f"open_evidence_gaps[{index}].id invalid")
            continue
        if gap_id in gap_ids:
            errors.append(f"duplicate evidence gap: {gap_id}")
        gap_ids.add(gap_id)
        if gap.get("repository_id") not in by_id:
            errors.append(
                f"evidence gap references unknown repository: {gap_id}"
            )
        if gap.get("state") != "TOKEN_VAZIO":
            errors.append(f"evidence gap must remain TOKEN_VAZIO: {gap_id}")
        criteria = gap.get("exit_criteria")
        if not isinstance(criteria, list) or not criteria:
            errors.append(f"evidence gap exit_criteria required: {gap_id}")

    derived = data.get("derived", {})
    actual = {
        "repository_count": len(by_id),
        "active_count": sum(
            repository.get("state") == "ACTIVE"
            for repository in by_id.values()
        ),
        "adapter_planned_count": sum(
            repository.get("state") == "ADAPTER_PLANNED"
            for repository in by_id.values()
        ),
        "token_vazio_count": sum(
            repository.get("state") == "TOKEN_VAZIO"
            for repository in by_id.values()
        ),
        "edge_count": len(edges),
        "cycle_count": int(cycle),
        "open_evidence_gap_count": len(gaps),
        "claim_allowed": False,
    }
    for key, value in actual.items():
        if derived.get(key) != value:
            errors.append(f"derived.{key} must be {value!r}")

    expected = digest(data)
    observed = data.get("integrity", {}).get("digest")
    if observed != expected:
        errors.append("integrity digest mismatch")
    if errors:
        raise ValidationError(
            "\n".join(f"- {error}" for error in errors)
        )
    return {
        "status": "PASS",
        **actual,
        "integrity_digest": expected,
        "inventory_state": governance.get("inventory_state"),
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("indices/TOROIDAL_RESEARCH_FEDERATION.json"),
    )
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args(argv)
    try:
        output = validate(load(args.path))
    except ValidationError as exc:
        print(exc, file=sys.stderr)
        return 1
    text = json.dumps(
        output,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    ) + "\n"
    if args.write_report:
        args.write_report.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
