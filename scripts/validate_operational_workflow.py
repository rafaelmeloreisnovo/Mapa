#!/usr/bin/env python3
"""Validate the canonical RAFAELIA operational-workflow contract.

The JSON Schema is the structural contract. This module adds deterministic
semantic checks using only the Python standard library: dependency integrity,
acyclicity, data lineage, evidence gates, implementation references and
TOKEN_VAZIO preservation.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, deque
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "rafaelia.operational-workflow/v1"
PHASES = {
    "ingest", "validate", "normalize", "index", "analyze",
    "decide", "execute", "verify", "publish", "control",
}
STATES = {"active", "planned", "blocked", "retired"}
EPISTEMIC_STATES = {"FATO", "VERIFIED_LIMITED", "HIPOTESE", "TOKEN_VAZIO"}
EXECUTORS = {"script", "workflow", "human", "model", "hybrid"}
EVIDENCE_KINDS = {
    "artifact", "checksum", "commit", "log",
    "measurement", "review", "schema", "test",
}
STAGE_ID_RE = re.compile(r"^[a-z][a-z0-9_-]{2,63}$")
WORKFLOW_ID_RE = re.compile(r"^wf:[a-z0-9][a-z0-9._:-]{4,127}$")


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, field: str, defects: list[str], *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        defects.append(f"{field} must be an array")
        return []
    if not allow_empty and not value:
        defects.append(f"{field} must not be empty")
    result: list[str] = []
    for index, item in enumerate(value):
        if not _nonempty(item):
            defects.append(f"{field}[{index}] must be a non-empty string")
        else:
            result.append(item)
    if len(result) != len(set(result)):
        defects.append(f"{field} must contain unique values")
    return result


def _safe_relative_path(value: str) -> bool:
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts and value not in {"", "."}


def _topological_order(stage_ids: list[str], dependencies: dict[str, list[str]]) -> tuple[list[str], list[str]]:
    indegree = {stage_id: 0 for stage_id in stage_ids}
    dependents: dict[str, list[str]] = {stage_id: [] for stage_id in stage_ids}
    defects: list[str] = []
    for stage_id, deps in dependencies.items():
        for dep in deps:
            if dep not in indegree:
                continue
            indegree[stage_id] += 1
            dependents[dep].append(stage_id)
    queue = deque(sorted(stage_id for stage_id, degree in indegree.items() if degree == 0))
    order: list[str] = []
    while queue:
        current = queue.popleft()
        order.append(current)
        for child in sorted(dependents[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(stage_ids):
        cyclic = sorted(stage_id for stage_id, degree in indegree.items() if degree > 0)
        defects.append("workflow dependency graph contains a cycle involving: " + ", ".join(cyclic))
    return order, defects


def _ancestors(stage_id: str, dependencies: dict[str, list[str]], memo: dict[str, set[str]]) -> set[str]:
    if stage_id in memo:
        return memo[stage_id]
    result: set[str] = set()
    for dep in dependencies.get(stage_id, []):
        result.add(dep)
        result.update(_ancestors(dep, dependencies, memo))
    memo[stage_id] = result
    return result


def validate_workflow(document: Any, repo_root: Path | None = None) -> tuple[list[str], dict[str, Any]]:
    defects: list[str] = []
    if not isinstance(document, dict):
        return ["workflow document must be an object"], {}

    required = {
        "schema_version", "workflow_id", "title", "owner", "objective",
        "claim_allowed", "external_inputs", "terminal_outputs", "policy",
        "stages", "next_verifiable_step",
    }
    missing = sorted(required - set(document))
    if missing:
        defects.append("missing workflow fields: " + ", ".join(missing))

    if document.get("schema_version") != SCHEMA_VERSION:
        defects.append(f"schema_version must equal {SCHEMA_VERSION}")
    workflow_id = document.get("workflow_id")
    if not (_nonempty(workflow_id) and WORKFLOW_ID_RE.fullmatch(workflow_id)):
        defects.append("workflow_id must match wf:<canonical-id>")
    for field in ("title", "owner", "objective", "next_verifiable_step"):
        if not _nonempty(document.get(field)):
            defects.append(f"{field} must be a non-empty string")
    if not isinstance(document.get("claim_allowed"), bool):
        defects.append("claim_allowed must be boolean")

    external_inputs = _string_list(document.get("external_inputs"), "external_inputs", defects)
    terminal_outputs = _string_list(document.get("terminal_outputs"), "terminal_outputs", defects)

    policy = document.get("policy")
    if not isinstance(policy, dict):
        defects.append("policy must be an object")
        policy = {}
    for field in ("immutable_sources", "token_vazio_is_valid", "human_review_for_execute_publish"):
        if policy.get(field) is not True:
            defects.append(f"policy.{field} must be true")
    max_timeout = policy.get("max_active_stage_timeout_seconds")
    if not isinstance(max_timeout, int) or isinstance(max_timeout, bool) or max_timeout <= 0:
        defects.append("policy.max_active_stage_timeout_seconds must be a positive integer")
        max_timeout = 0

    stages = document.get("stages")
    if not isinstance(stages, list) or not stages:
        defects.append("stages must be a non-empty array")
        stages = []

    stage_by_id: dict[str, dict[str, Any]] = {}
    dependencies: dict[str, list[str]] = {}
    output_owner: dict[str, str] = {}
    all_inputs: set[str] = set()
    state_counts: Counter[str] = Counter()
    phase_counts: Counter[str] = Counter()

    for index, raw_stage in enumerate(stages):
        prefix = f"stages[{index}]"
        if not isinstance(raw_stage, dict):
            defects.append(f"{prefix} must be an object")
            continue
        stage = raw_stage
        stage_id = stage.get("id")
        if not (_nonempty(stage_id) and STAGE_ID_RE.fullmatch(stage_id)):
            defects.append(f"{prefix}.id must match {STAGE_ID_RE.pattern}")
            stage_id = f"__invalid_{index}"
        if stage_id in stage_by_id:
            defects.append(f"duplicate stage id: {stage_id}")
        else:
            stage_by_id[stage_id] = stage

        for field in ("operational_name", "transformation", "rollback", "next_verifiable_step"):
            if not _nonempty(stage.get(field)):
                defects.append(f"{prefix}.{field} must be a non-empty string")

        phase = stage.get("phase")
        state = stage.get("state")
        epistemic = stage.get("epistemic_state")
        executor = stage.get("executor")
        if phase not in PHASES:
            defects.append(f"{prefix}.phase is invalid")
        else:
            phase_counts[phase] += 1
        if state not in STATES:
            defects.append(f"{prefix}.state is invalid")
        else:
            state_counts[state] += 1
        if epistemic not in EPISTEMIC_STATES:
            defects.append(f"{prefix}.epistemic_state is invalid")
        if executor not in EXECUTORS:
            defects.append(f"{prefix}.executor is invalid")
        if not isinstance(stage.get("claim_allowed"), bool):
            defects.append(f"{prefix}.claim_allowed must be boolean")
        if not isinstance(stage.get("human_review_required"), bool):
            defects.append(f"{prefix}.human_review_required must be boolean")

        deps = _string_list(stage.get("depends_on"), f"{prefix}.depends_on", defects, allow_empty=True)
        dependencies[stage_id] = deps
        inputs = _string_list(stage.get("inputs"), f"{prefix}.inputs", defects)
        outputs = _string_list(stage.get("outputs"), f"{prefix}.outputs", defects)
        _string_list(stage.get("success_criteria"), f"{prefix}.success_criteria", defects)
        _string_list(stage.get("failure_modes"), f"{prefix}.failure_modes", defects)
        evidence = _string_list(stage.get("evidence_requirements"), f"{prefix}.evidence_requirements", defects)
        implementation_refs = _string_list(
            stage.get("implementation_refs"),
            f"{prefix}.implementation_refs",
            defects,
            allow_empty=(state != "active"),
        )

        all_inputs.update(inputs)
        for output in outputs:
            if output in output_owner:
                defects.append(f"output {output!r} is produced by both {output_owner[output]} and {stage_id}")
            else:
                output_owner[output] = stage_id

        resource_limits = stage.get("resource_limits")
        if not isinstance(resource_limits, dict):
            defects.append(f"{prefix}.resource_limits must be an object")
            resource_limits = {}
        timeout = resource_limits.get("timeout_seconds")
        memory = resource_limits.get("max_memory_mb")
        if not isinstance(timeout, int) or isinstance(timeout, bool) or timeout <= 0:
            defects.append(f"{prefix}.resource_limits.timeout_seconds must be positive")
        if not isinstance(memory, int) or isinstance(memory, bool) or memory <= 0:
            defects.append(f"{prefix}.resource_limits.max_memory_mb must be positive")
        if state == "active" and isinstance(timeout, int) and max_timeout and timeout > max_timeout:
            defects.append(f"{prefix} timeout exceeds workflow policy maximum")

        for evidence_kind in evidence:
            if evidence_kind not in EVIDENCE_KINDS:
                defects.append(f"{prefix}.evidence_requirements contains invalid kind {evidence_kind!r}")

        for ref in implementation_refs:
            if not _safe_relative_path(ref):
                defects.append(f"{prefix}.implementation_refs contains unsafe path {ref!r}")
            elif state == "active" and repo_root is not None and not (repo_root / ref).exists():
                defects.append(f"{prefix}.implementation_refs missing active artifact: {ref}")

        if state == "active":
            if epistemic not in {"FATO", "VERIFIED_LIMITED"}:
                defects.append(f"{prefix} active stage requires FATO or VERIFIED_LIMITED")
            if not implementation_refs:
                defects.append(f"{prefix} active stage requires implementation_refs")
            if stage.get("claim_allowed") is True and not evidence:
                defects.append(f"{prefix} claim_allowed=true requires evidence_requirements")
        elif state == "planned":
            if epistemic != "TOKEN_VAZIO":
                defects.append(f"{prefix} planned stage requires epistemic_state=TOKEN_VAZIO")
            if stage.get("claim_allowed") is not False:
                defects.append(f"{prefix} planned stage requires claim_allowed=false")
        elif state in {"blocked", "retired"} and stage.get("claim_allowed") is not False:
            defects.append(f"{prefix} {state} stage requires claim_allowed=false")

        if phase in {"execute", "publish"} and stage.get("human_review_required") is not True:
            defects.append(f"{prefix} {phase} stage requires human_review_required=true")

    stage_ids = list(stage_by_id)
    for stage_id, deps in dependencies.items():
        for dep in deps:
            if dep == stage_id:
                defects.append(f"stage {stage_id} must not depend on itself")
            elif dep not in stage_by_id:
                defects.append(f"stage {stage_id} depends on unknown stage {dep}")
            elif stage_by_id.get(stage_id, {}).get("state") == "active" and stage_by_id[dep].get("state") != "active":
                defects.append(f"active stage {stage_id} must not depend on non-active stage {dep}")

    order, graph_defects = _topological_order(stage_ids, dependencies)
    defects.extend(graph_defects)

    if not graph_defects:
        memo: dict[str, set[str]] = {}
        for stage_id, stage in stage_by_id.items():
            ancestors = {
                ancestor
                for ancestor in _ancestors(stage_id, dependencies, memo)
                if ancestor in stage_by_id
            }
            available_outputs = {
                output
                for ancestor in ancestors
                for output in stage_by_id[ancestor].get("outputs", [])
            }
            for input_id in stage.get("inputs", []):
                if input_id not in external_inputs and input_id not in available_outputs:
                    defects.append(
                        f"stage {stage_id} input {input_id!r} is not external and is not produced by an ancestor"
                    )

    known_outputs = set(output_owner)
    for terminal in terminal_outputs:
        if terminal not in known_outputs:
            defects.append(f"terminal output {terminal!r} is not produced by any stage")
    for output, producer in output_owner.items():
        if output not in all_inputs and output not in terminal_outputs:
            defects.append(f"output {output!r} from stage {producer} is neither consumed nor terminal")

    if document.get("claim_allowed") is True:
        non_active = sorted(stage_id for stage_id, stage in stage_by_id.items() if stage.get("state") != "active")
        denied = sorted(stage_id for stage_id, stage in stage_by_id.items() if stage.get("claim_allowed") is not True)
        if non_active or denied:
            defects.append("workflow claim_allowed=true requires every stage active and individually claim_allowed=true")

    report = {
        "schema_version": SCHEMA_VERSION,
        "workflow_id": workflow_id,
        "status": "PASS" if not defects else "FAIL",
        "stage_count": len(stage_by_id),
        "edge_count": sum(len(deps) for deps in dependencies.values()),
        "state_counts": dict(sorted(state_counts.items())),
        "phase_counts": dict(sorted(phase_counts.items())),
        "topological_order": order,
        "external_inputs": external_inputs,
        "terminal_outputs": terminal_outputs,
        "defects": defects,
        "claim_allowed": False,
        "next_verifiable_step": (
            "Attach the generated report and checksums to the CI run; preserve planned stages as TOKEN_VAZIO."
            if not defects
            else "Correct every listed defect before promoting or executing the workflow."
        ),
    }
    return defects, report


def load_document(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workflow",
        nargs="?",
        type=Path,
        default=Path("data/workflows/rafaelia-operational-workflow.v1.json"),
    )
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--write-report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    document = load_document(args.workflow)
    defects, report = validate_workflow(document, args.repo_root)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if defects else 0


if __name__ == "__main__":
    raise SystemExit(main())
