#!/usr/bin/env python3
"""Fail-closed validator for RAFAELIA branch-evolution anti-regression V2."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

H40 = re.compile(r"^[0-9a-f]{40}$")
CLASSES = {
    "ANCESTOR_ONLY",
    "SHADOWED_BY_MAIN_ENHANCED",
    "MERGED_NONCANONICAL_BASE_PENDING_CANONICALIZATION",
    "DIVERGED_UNRECONCILED",
}


class BranchEvolutionError(ValueError):
    pass


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BranchEvolutionError(f"manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise BranchEvolutionError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise BranchEvolutionError("manifest root must be an object")
    return data


def _relation(obs: dict[str, Any], errors: list[str], p: str) -> dict[str, Any]:
    rel = obs.get("relation_to_main")
    if not isinstance(rel, dict):
        errors.append(f"{p}.relation_to_main")
        return {}
    status = rel.get("status")
    if status not in {"behind", "ahead", "diverged", "identical"}:
        errors.append(f"{p}.relation.status")
    for k in ("ahead_by", "behind_by"):
        if not isinstance(rel.get(k), int) or rel[k] < 0:
            errors.append(f"{p}.relation.{k}")
    rev = rel.get("observed_head_or_merge_base_sha")
    if not (isinstance(rev, str) and (H40.fullmatch(rev) or rev.startswith("TOKEN_VAZIO_"))):
        errors.append(f"{p}.relation.revision")
    return rel


def validate_manifest(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if data.get("schema_version") != "rafaelia.branch-evolution-anti-regression.v2":
        errors.append("schema_version")
    if data.get("repository") != "rafaelmeloreisnovo/Mapa":
        errors.append("repository")
    base = data.get("base")
    if not isinstance(base, dict) or base.get("branch") != "main" or base.get("role") != "CANONICAL":
        errors.append("base")
    elif not H40.fullmatch(str(base.get("sha", ""))):
        errors.append("base.sha")

    if data.get("claim_allowed") is not False:
        errors.append("claim_allowed")
    if data.get("repository_wide_closed") is not False:
        errors.append("repository_wide_closed")
    if data.get("automatic_merge") is not False:
        errors.append("automatic_merge")
    if data.get("canonicalization_requires_new_pr_to_main") is not True:
        errors.append("canonicalization_requires_new_pr_to_main")

    count = data.get("branch_count_observed")
    if not isinstance(count, int) or count <= 0:
        errors.append("branch_count_observed")

    classes = data.get("decision_classes")
    if not isinstance(classes, dict) or set(classes) != CLASSES:
        errors.append("decision_classes")

    observations = data.get("observations")
    if not isinstance(observations, list) or not observations:
        return errors + ["observations"]
    if isinstance(count, int) and count < len(observations):
        errors.append("branch_count_less_than_observations")

    seen: set[str] = set()
    for i, obs in enumerate(observations):
        p = f"observations[{i}]"
        if not isinstance(obs, dict):
            errors.append(p)
            continue
        branch = obs.get("branch")
        if not isinstance(branch, str) or not branch:
            errors.append(f"{p}.branch")
            continue
        if branch in seen:
            errors.append(f"{p}.duplicate_branch")
        seen.add(branch)

        rel = _relation(obs, errors, p)
        cls = obs.get("classification")
        if cls not in CLASSES:
            errors.append(f"{p}.classification")
            continue
        if obs.get("merge_to_main_authorized") is not False:
            errors.append(f"{p}.merge_to_main_authorized")

        ahead = rel.get("ahead_by")
        behind = rel.get("behind_by")
        status = rel.get("status")

        if cls == "ANCESTOR_ONLY":
            if not (status == "behind" and ahead == 0 and isinstance(behind, int) and behind > 0):
                errors.append(f"{p}.ancestor_rule")
            if obs.get("transfer_required") is not False:
                errors.append(f"{p}.ancestor_transfer")

        elif cls == "SHADOWED_BY_MAIN_ENHANCED":
            eq = obs.get("artifact_equivalence")
            if not isinstance(eq, dict):
                errors.append(f"{p}.artifact_equivalence")
            else:
                if eq.get("main_state") != "PRESENT_PROVENANCE_ENHANCED":
                    errors.append(f"{p}.main_state")
                if eq.get("byte_identical") is not False:
                    errors.append(f"{p}.byte_identity_boundary")
                for key in ("branch_blob_sha1", "main_blob_sha1"):
                    if not H40.fullmatch(str(eq.get(key, ""))):
                        errors.append(f"{p}.{key}")
            if not (status == "diverged" and isinstance(ahead, int) and ahead > 0):
                errors.append(f"{p}.shadow_relation")
            if obs.get("transfer_required") is not False:
                errors.append(f"{p}.shadow_transfer")

        elif cls == "MERGED_NONCANONICAL_BASE_PENDING_CANONICALIZATION":
            pr = obs.get("source_pr")
            presence = obs.get("main_presence")
            if not isinstance(pr, dict):
                errors.append(f"{p}.source_pr")
            else:
                if pr.get("merged") is not True or pr.get("state") != "closed":
                    errors.append(f"{p}.source_pr_merge_state")
                if pr.get("base") == "main":
                    errors.append(f"{p}.source_pr_noncanonical_base")
                if not isinstance(pr.get("number"), int) or pr["number"] <= 0:
                    errors.append(f"{p}.source_pr_number")
                if not H40.fullmatch(str(pr.get("head_sha", ""))):
                    errors.append(f"{p}.source_pr_head_sha")
            if not isinstance(presence, dict):
                errors.append(f"{p}.main_presence")
            else:
                missing = presence.get("missing_in_main")
                checked = presence.get("checked_paths")
                if presence.get("all_present") is not False:
                    errors.append(f"{p}.main_presence_all_present")
                if not isinstance(missing, list) or not missing:
                    errors.append(f"{p}.main_presence_missing")
                if not isinstance(checked, list) or not set(missing or []).issubset(set(checked or [])):
                    errors.append(f"{p}.main_presence_checked")
            if not (status == "diverged" and isinstance(ahead, int) and ahead > 0 and isinstance(behind, int) and behind > 0):
                errors.append(f"{p}.canonicalization_relation")
            if obs.get("transfer_required") != "REVIEW_REQUIRED":
                errors.append(f"{p}.canonicalization_transfer")

        elif cls == "DIVERGED_UNRECONCILED":
            if not (status == "diverged" and isinstance(ahead, int) and ahead > 0 and isinstance(behind, int) and behind > 0):
                errors.append(f"{p}.diverged_rule")
            if not str(obs.get("transfer_required", "")).startswith("TOKEN_VAZIO"):
                errors.append(f"{p}.diverged_transfer")

    tv = data.get("token_vazio")
    if not isinstance(tv, dict):
        errors.append("token_vazio")
    else:
        open_tokens = tv.get("open")
        if not isinstance(open_tokens, list) or not open_tokens:
            errors.append("token_vazio.open")
        elif any(not isinstance(x, str) or not x.startswith("TOKEN_VAZIO_") for x in open_tokens):
            errors.append("token_vazio.open_format")

    invariants = data.get("invariants")
    required_invariants = {
        "git_ahead_does_not_imply_semantic_novelty",
        "merged_pr_does_not_imply_main_presence",
        "supersession_preserves_source_pointer",
        "token_vazio_is_auditable",
    }
    if not isinstance(invariants, list) or not required_invariants.issubset(set(invariants)):
        errors.append("invariants")

    return errors


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "manifest",
        nargs="?",
        default="data/governance/branch_evolution_anti_regression_v2.json",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        data = load_manifest(Path(args.manifest))
    except BranchEvolutionError as exc:
        print(f"REJECT: {exc}", file=sys.stderr)
        return 1

    errors = validate_manifest(data)
    if errors:
        for error in errors:
            print(f"REJECT: {error}", file=sys.stderr)
        return 1

    print(
        "PASS branch-evolution-v2 "
        f"branches_observed={data['branch_count_observed']} "
        f"sampled_relations={len(data['observations'])} "
        "claim_allowed=false automatic_merge=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
