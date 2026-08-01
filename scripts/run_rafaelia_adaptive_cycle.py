#!/usr/bin/env python3
"""RAFAELIA adaptive read-only cycle engine.

The engine never mutates sources or promotes claims. It converts one repository
snapshot into deterministic, hash-bound receipts that expose measured state,
formula boundaries, unresolved gaps, and the next verifiable action.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "rafaelia.adaptive-cycle.v1"
REGISTRY_SCHEMA = "rafaelia.formula-registry.v1"
RECEIPT_SCHEMA = "rafaelia.adaptive-cycle-receipt.v1"
EXCLUDED_DIRS = {".git", ".venv", "node_modules", "artifacts", "__pycache__"}


class CycleError(ValueError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CycleError(f"{path}: root must be an object")
    return value


def validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("schema") != SCHEMA:
        raise CycleError("wrong cycle contract schema")
    for flag in ("claim_allowed", "publication_ready", "automatic_mutation", "automatic_merge"):
        if contract.get(flag) is not False:
            raise CycleError(f"{flag} must remain false")
    if contract.get("source_mode") != "READ_ONLY":
        raise CycleError("source_mode must be READ_ONLY")
    expected = ["source", "index", "semantic_token", "claim", "evidence", "falsifier", "decision", "artifact"]
    if contract.get("pipeline") != expected:
        raise CycleError("pipeline order drift")
    cadence = contract.get("cadence", {})
    if cadence.get("microcycle_minutes") != 15 or cadence.get("period") != 42:
        raise CycleError("cadence must preserve 15-minute microcycles and period 42")
    cycle = contract.get("cycle", {})
    if cycle.get("alpha") != 0.25:
        raise CycleError("alpha must be 0.25")
    if cycle.get("state_fields") != ["u", "v", "psi", "chi", "rho", "delta", "sigma"]:
        raise CycleError("state vector must preserve seven typed coordinates")
    fibonacci = contract.get("fibonacci_rafael", {})
    if set(fibonacci.get("variants", {})) != {"canonical_plus_sin", "listed_minus_sin"}:
        raise CycleError("both Fibonacci-Rafael sign variants are required")
    if fibonacci.get("conflict_policy") != "COMPUTE_BOTH_NO_SILENT_SELECTION":
        raise CycleError("formula conflict must remain explicit")
    tasks = contract.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise CycleError("tasks are required")
    ids = [task.get("id") for task in tasks if isinstance(task, dict)]
    if len(ids) != len(tasks) or len(ids) != len(set(ids)):
        raise CycleError("task ids must be present and unique")
    if any(str(task.get("state", "")).startswith("TOKEN_VAZIO") and not task.get("next_step") for task in tasks):
        raise CycleError("every TOKEN_VAZIO task requires a next_step")


def validate_registry(registry: dict[str, Any]) -> None:
    if registry.get("schema") != REGISTRY_SCHEMA:
        raise CycleError("wrong formula registry schema")
    if registry.get("claim_allowed") is not False or registry.get("automatic_promotion") is not False:
        raise CycleError("formula registry must remain non-promoting")
    records = registry.get("records")
    if not isinstance(records, list) or len(records) != 50:
        raise CycleError("formula registry must contain exactly 50 records")
    ids = [item.get("id") for item in records if isinstance(item, dict)]
    if ids != list(range(1, 51)):
        raise CycleError("formula ids must be exactly 1..50")
    if records[21].get("classification") != "CONFLICTING_DEFINITION":
        raise CycleError("formula 22 sign conflict must remain explicit")
    for item in records:
        if not isinstance(item.get("expression"), str) or not item["expression"]:
            raise CycleError("every formula requires an expression")
        if item.get("claim_state") is None:
            raise CycleError("every formula requires a claim_state")


def parse_timestamp(text: str | None) -> datetime:
    if text is None:
        return datetime.now(timezone.utc)
    value = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def normalized_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    length = len(data)
    entropy = -sum((count / length) * math.log2(count / length) for count in counts.values())
    return min(1.0, entropy / 8.0)


def git_head(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() or None


def repository_metrics(root: Path, required_paths: list[str]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    total_bytes = 0
    for path in iter_files(root):
        rel = path.relative_to(root).as_posix()
        size = path.stat().st_size
        total_bytes += size
        records.append({"path": rel, "bytes": size})
    manifest = canonical_bytes(records)
    present = [name for name in required_paths if (root / name).exists()]
    coverage = len(present) / len(required_paths) if required_paths else 1.0
    return {
        "files": len(records), "bytes": total_bytes,
        "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
        "path_entropy_normalized": normalized_entropy(manifest),
        "required_paths": required_paths, "required_paths_present": present,
        "coverage": coverage, "git_head": git_head(root),
    }


def fibonacci_pair(contract: dict[str, Any], n: int) -> dict[str, float | bool | int]:
    spec = contract["fibonacci_rafael"]
    a = float(spec["a"])
    theta = math.radians(float(spec["theta_degrees"]))
    plus = minus = float(spec["initial"])
    perturbation = math.pi * math.sin(theta)
    for _ in range(n):
        plus = a * plus + perturbation
        minus = a * minus - perturbation
    return {
        "n": n, "a": a, "theta_degrees": float(spec["theta_degrees"]),
        "pi_sin_theta": perturbation, "canonical_plus_sin": plus,
        "listed_minus_sin": minus, "absolute_divergence": abs(plus - minus),
        "silent_selection": False,
    }


def smooth_state(contract: dict[str, Any], metrics: dict[str, Any]) -> dict[str, float]:
    cycle = contract["cycle"]
    alpha = float(cycle["alpha"])
    c0, h0 = float(cycle["initial_C"]), float(cycle["initial_H"])
    c_in, h_in = float(metrics["coverage"]), float(metrics["path_entropy_normalized"])
    c_next = (1.0 - alpha) * c0 + alpha * c_in
    h_next = (1.0 - alpha) * h0 + alpha * h_in
    return {
        "alpha": alpha, "C_previous": c0, "C_input": c_in, "C_next": c_next,
        "H_previous": h0, "H_input": h_in, "H_next": h_next,
        "phi_metric": (1.0 - h_next) * c_next,
    }


def fractional(value: float) -> float:
    return value - math.floor(value)


def toroidal_state(metrics: dict[str, Any], state: dict[str, float], fib: dict[str, Any], phase_index: int) -> dict[str, float]:
    vector = {
        "u": fractional(metrics["files"] / 42.0),
        "v": fractional(metrics["bytes"] / 1_000_000.0),
        "psi": fractional(phase_index / 6.0),
        "chi": fractional(state["C_next"]),
        "rho": fractional(state["H_next"]),
        "delta": fractional(float(fib["absolute_divergence"])),
        "sigma": fractional(state["phi_metric"]),
    }
    if any(not (0.0 <= value < 1.0) for value in vector.values()):
        raise CycleError("toroidal state escaped [0,1)^7")
    return vector


def formula_evaluation(registry: dict[str, Any], state: dict[str, float], fib: dict[str, Any]) -> dict[str, Any]:
    records = registry["records"]
    counts = Counter(item["classification"] for item in records)
    executable = [item["id"] for item in records if item.get("executable_safely") is True]
    kat = {
        "formula_5_C_next": state["C_next"],
        "formula_6_H_next": state["H_next"],
        "formula_7_alpha": state["alpha"],
        "formula_8_phi_metric": state["phi_metric"],
        "formula_18_spiral_n_7": (math.sqrt(3.0) / 2.0) ** 7,
        "formula_19_golden_ratio": (1.0 + math.sqrt(5.0)) / 2.0,
        "formula_22_plus_variant": fib["canonical_plus_sin"],
        "formula_22_minus_variant": fib["listed_minus_sin"],
        "formula_22_divergence": fib["absolute_divergence"],
        "formula_43_sample_entropy_milli": int((128 * 6000 / 256) + (8 * 2000 / 15)),
    }
    return {
        "schema": "rafaelia.formula-evaluation.v1", "claim_allowed": False,
        "registry_sha256": sha256_value(registry), "formula_count": len(records),
        "classification_counts": dict(sorted(counts.items())),
        "safe_executable_ids": executable, "safe_executable_count": len(executable),
        "known_refuted_as_written": [item["id"] for item in records if item["claim_state"] == "REFUTED_AS_WRITTEN"],
        "token_vazio_or_model": [item["id"] for item in records if item["claim_state"].startswith("TOKEN_VAZIO") or item["claim_state"] == "MODEL_OR_TOKEN_VAZIO"],
        "known_answer_tests": kat,
    }


def task_score(task: dict[str, Any], phase: str, phi_metric: float, fib: dict[str, Any]) -> float:
    score = float(task["base_priority"])
    if task.get("preferred_phase") == phase:
        score += 12.0
    score += 5.0 * phi_metric
    score += 1.0 / (1.0 + float(fib["absolute_divergence"]))
    if task.get("automation_allowed") is True:
        score += 2.0
    return score


def choose_next_task(contract: dict[str, Any], phase: str, phi_metric: float, fib: dict[str, Any]) -> dict[str, Any]:
    scored = []
    for task in contract["tasks"]:
        item = dict(task)
        item["score"] = round(task_score(task, phase, phi_metric, fib), 9)
        scored.append(item)
    scored.sort(key=lambda item: (-item["score"], item["id"]))
    return {
        "schema": "rafaelia.next-action.v1", "claim_allowed": False,
        "phase": phase, "selected": scored[0], "ranked": scored,
        "selection_boundary": "priority is operational ordering, not truth probability",
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def render_summary(receipt: dict[str, Any]) -> str:
    next_task = receipt["next_action"]["selected"]
    gaps = [item for item in receipt["next_action"]["ranked"] if str(item.get("state", "")).startswith("TOKEN_VAZIO")]
    lines = [
        "# RAFAELIA Adaptive Cycle Receipt", "",
        f"- Cycle: `{receipt['cycle']['cycle_id']}`",
        f"- Phase: `{receipt['cycle']['phase']}`",
        f"- Decision: `{receipt['decision']}`",
        f"- Claim allowed: `{str(receipt['claim_allowed']).lower()}`",
        f"- Repository coverage: `{receipt['repository']['coverage']:.6f}`",
        f"- Formula registry: `{receipt['formula_evaluation']['formula_count']}/50` records",
        f"- Next action: `{next_task['id']}`", "", "## F_ok", "",
        "Read-only scan, toroidal state, dual Fibonacci-Rafael evaluation, formula KATs, task ranking and receipt hashing completed.",
        "", "## F_gap", "",
    ]
    lines.extend(f"- `{item['id']}` — `{item['state']}`" for item in gaps)
    lines.extend(["", "## F_next", "", next_task["next_step"], "",
                  "> Automatic != unsupervised. Automatic = repeatable + auditable + reversible + observable."])
    return "\n".join(lines) + "\n"


def execute(root: Path, contract_path: Path, registry_path: Path, out_dir: Path, timestamp: datetime) -> dict[str, Any]:
    contract, registry = load_object(contract_path), load_object(registry_path)
    validate_contract(contract)
    validate_registry(registry)
    cadence = contract["cadence"]
    slot = int(timestamp.timestamp()) // (int(cadence["microcycle_minutes"]) * 60)
    n = slot % int(cadence["period"])
    phases = contract["cycle"]["phases"]
    phase_index, phase = slot % len(phases), phases[slot % len(phases)]
    metrics = repository_metrics(root, list(contract["required_paths"]))
    state = smooth_state(contract, metrics)
    fib = fibonacci_pair(contract, n)
    vector = toroidal_state(metrics, state, fib, phase_index)
    formulas = formula_evaluation(registry, state, fib)
    next_action = choose_next_task(contract, phase, state["phi_metric"], fib)
    cycle_id = f"RAF-CYCLE-{timestamp.strftime('%Y%m%dT%H%M%SZ')}-N{n:02d}"
    receipt: dict[str, Any] = {
        "schema": RECEIPT_SCHEMA, "generated_at": timestamp.isoformat(),
        "claim_allowed": False, "publication_ready": False,
        "automatic_mutation": False, "automatic_merge": False,
        "decision": "EXECUTED_READ_ONLY",
        "cycle": {"cycle_id": cycle_id, "slot": slot, "n_mod_42": n,
                  "phase": phase, "phase_index": phase_index,
                  "microcycle_minutes": cadence["microcycle_minutes"],
                  "consolidation_microcycles": cadence["consolidation_microcycles"]},
        "pipeline": contract["pipeline"], "repository": metrics,
        "smoothed_state": state, "toroidal_state": vector,
        "fibonacci_rafael": fib, "formula_evaluation": formulas,
        "next_action": next_action,
        "token_vazio": [item["id"] for item in next_action["ranked"] if str(item.get("state", "")).startswith("TOKEN_VAZIO")],
        "boundaries": {"schedule_is_not_evidence": True, "hash_is_not_truth": True,
                       "ci_is_not_physical_runtime": True, "parabola_is_not_mechanism": True,
                       "human_review_required_for_promotion": True},
        "inputs": {"contract_path": contract_path.as_posix(), "contract_sha256": sha256_value(contract),
                   "registry_path": registry_path.as_posix(), "registry_sha256": sha256_value(registry)},
    }
    receipt["receipt_sha256"] = sha256_value(receipt)
    write_json(out_dir / "cycle_receipt.json", receipt)
    write_json(out_dir / "formula_evaluation.json", formulas)
    write_json(out_dir / "next_action.json", next_action)
    (out_dir / "cycle_summary.md").write_text(render_summary(receipt), encoding="utf-8")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--contract", type=Path, default=Path("data/control-plane/RAFAELIA_ADAPTIVE_CYCLE.v1.json"))
    parser.add_argument("--registry", type=Path, default=Path("data/formulas/RAFAELIA_FORMULA_REGISTRY.v1.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/rafaelia-cycle"))
    parser.add_argument("--timestamp")
    args = parser.parse_args()
    try:
        receipt = execute(args.root.resolve(), args.contract, args.registry, args.output_dir, parse_timestamp(args.timestamp))
    except (OSError, json.JSONDecodeError, CycleError) as error:
        failure = {"schema": RECEIPT_SCHEMA, "decision": "BLOCKED_TOKEN_VAZIO",
                   "claim_allowed": False, "publication_ready": False,
                   "error": f"{type(error).__name__}: {error}"}
        write_json(args.output_dir / "cycle_receipt.json", failure)
        print(json.dumps(failure, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps({"cycle_id": receipt["cycle"]["cycle_id"], "decision": receipt["decision"],
                      "phase": receipt["cycle"]["phase"],
                      "next_action": receipt["next_action"]["selected"]["id"],
                      "receipt_sha256": receipt["receipt_sha256"],
                      "claim_allowed": receipt["claim_allowed"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
