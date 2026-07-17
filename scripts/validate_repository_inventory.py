#!/usr/bin/env python3
"""Fail-closed, stdlib-only validator for REPOSITORY_INVENTORY.json."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ALLOWED_OWNERS = {"rafaelmeloreisnovo", "instituto-Rafael"}
FULL_NAME_RE = re.compile(r"^[A-Za-z0-9-]+/[A-Za-z0-9._-]+$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_REPO_FIELDS = {
    "repository_full_name", "repository_id", "owner", "repository_name",
    "clone_url", "default_branch", "visibility", "archived", "size_kib",
    "metadata_status", "claim_scope", "observed_via",
}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("inventory root must be an object")
    return data


def canonical_digest(data: dict[str, Any]) -> str:
    clone = copy.deepcopy(data)
    clone.setdefault("integrity", {})["digest"] = ""
    raw = json.dumps(clone, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.blake2b(raw, digest_size=32).hexdigest()


def validate_inventory(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_top = {"schema", "schema_version", "generated_at", "inventory_source", "collection_method", "scope", "statistics", "repositories", "absence_ledger", "integrity"}
    missing_top = sorted(required_top - set(data))
    if missing_top:
        errors.append(f"missing top-level fields: {missing_top}")
        return errors
    if data["schema"] != "repository_inventory_v2": errors.append("schema must be repository_inventory_v2")
    if data["schema_version"] != "2.0.0": errors.append("schema_version must be 2.0.0")
    if data["inventory_source"] != "github_connector": errors.append("inventory_source must be github_connector")
    repos = data["repositories"]
    if not isinstance(repos, list):
        errors.append("repositories must be a list")
        return errors
    ids: set[int] = set(); names: set[str] = set()
    for i, repo in enumerate(repos):
        prefix=f"repositories[{i}]"
        if not isinstance(repo, dict): errors.append(f"{prefix} must be an object"); continue
        missing=sorted(REQUIRED_REPO_FIELDS-set(repo))
        if missing: errors.append(f"{prefix} missing fields: {missing}"); continue
        rid=repo["repository_id"]; full=repo["repository_full_name"]; owner=repo["owner"]; name=repo["repository_name"]
        if not isinstance(rid,int) or isinstance(rid,bool) or rid<=0: errors.append(f"{prefix}.repository_id must be a positive integer")
        elif rid in ids: errors.append(f"duplicate repository_id: {rid}")
        ids.add(rid)
        if not isinstance(full,str) or not FULL_NAME_RE.fullmatch(full): errors.append(f"{prefix}.repository_full_name invalid")
        elif full in names: errors.append(f"duplicate repository_full_name: {full}")
        names.add(full)
        if owner not in ALLOWED_OWNERS: errors.append(f"{prefix}.owner not allowed: {owner}")
        if full != f"{owner}/{name}": errors.append(f"{prefix}.repository_full_name does not match owner/name")
        if repo["clone_url"] != f"https://github.com/{full}.git": errors.append(f"{prefix}.clone_url is not canonical")
        if repo["visibility"] not in {"public","private"}: errors.append(f"{prefix}.visibility invalid")
        if not isinstance(repo["archived"],bool): errors.append(f"{prefix}.archived must be boolean")
        if not isinstance(repo["size_kib"],int) or isinstance(repo["size_kib"],bool) or repo["size_kib"]<0: errors.append(f"{prefix}.size_kib must be a non-negative integer")
        if repo["metadata_status"] != "FATO": errors.append(f"{prefix}.metadata_status must be FATO for connector-backed fields")
        if repo["claim_scope"] != "repository_identity_and_connector_metadata_only": errors.append(f"{prefix}.claim_scope invalid")
        if repo["observed_via"] != "github_connector.get_repo": errors.append(f"{prefix}.observed_via invalid")
        for field in ("repository_full_name","repository_id","owner","repository_name","clone_url","default_branch","visibility","size_kib"):
            if "TOKEN_VAZIO" in str(repo[field]): errors.append(f"{prefix}.{field} cannot be TOKEN_VAZIO")
    scope=data["scope"]; stats=data["statistics"]
    accounts=scope.get("included_accounts",[])
    accessible=sum(a.get("accessible_count_observed",-1) for a in accounts if isinstance(a,dict))
    if accessible != scope.get("accessible_total_observed"): errors.append("scope accessible total does not equal included account counts")
    materialized=len(repos)
    if scope.get("materialized_count") != materialized: errors.append("scope.materialized_count mismatch")
    if stats.get("materialized_count") != materialized: errors.append("statistics.materialized_count mismatch")
    expected_ratio=round(materialized/scope["accessible_total_observed"],12) if scope.get("accessible_total_observed",0)>0 else 0.0
    if scope.get("completeness_ratio") != expected_ratio: errors.append("scope.completeness_ratio mismatch")
    derived={
      "public_count":sum(r.get("visibility")=="public" for r in repos),
      "private_count":sum(r.get("visibility")=="private" for r in repos),
      "archived_count":sum(r.get("archived") is True for r in repos),
      "owner_counts":{o:sum(r.get("owner")==o for r in repos) for o in sorted(ALLOWED_OWNERS)},
    }
    for key,value in derived.items():
        if stats.get(key)!=value: errors.append(f"statistics.{key} mismatch: declared={stats.get(key)!r} derived={value!r}")
    state=scope.get("state"); claim_allowed=scope.get("claim_allowed")
    if state not in {"PARTIAL","COMPLETE"}: errors.append("scope.state must be PARTIAL or COMPLETE")
    if state=="PARTIAL" and claim_allowed is not False: errors.append("PARTIAL inventory requires claim_allowed=false")
    if state=="COMPLETE" and materialized != scope.get("accessible_total_observed"): errors.append("COMPLETE inventory requires all accessible records materialized")
    ledger=data["absence_ledger"]
    missing=scope.get("accessible_total_observed",0)-materialized
    if ledger.get("missing_materialized_records")!=missing: errors.append("absence_ledger missing count mismatch")
    if state=="PARTIAL":
        for field in ("state","reason","owner","next_action","exit_criteria"):
            if not ledger.get(field): errors.append(f"absence_ledger.{field} is required for PARTIAL state")
        if ledger.get("state")!="TOKEN_VAZIO": errors.append("PARTIAL absence_ledger.state must be TOKEN_VAZIO")
    integ=data["integrity"]
    if integ.get("algorithm")!="blake2b-256": errors.append("integrity.algorithm must be blake2b-256")
    digest=integ.get("digest","")
    if not isinstance(digest,str) or not HEX64_RE.fullmatch(digest): errors.append("integrity.digest must be 64 lowercase hex chars")
    elif digest != canonical_digest(data): errors.append("integrity.digest mismatch")
    return errors


def build_report(data: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    scope=data.get("scope",{})
    return {
      "schema":"repository_inventory_validation_report_v2",
      "source_generated_at":data.get("generated_at"),
      "status":"PASS" if not errors else "FAIL",
      "claim_allowed":bool(not errors and scope.get("state")=="COMPLETE" and scope.get("claim_allowed") is True),
      "inventory_state":scope.get("state","TOKEN_VAZIO"),
      "accessible_total_observed":scope.get("accessible_total_observed","TOKEN_VAZIO"),
      "materialized_count":len(data.get("repositories",[])),
      "errors":errors,
      "digest_blake2b_256":canonical_digest(data) if data else "TOKEN_VAZIO",
    }


def main(argv: list[str]|None=None) -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--inventory",default="indices/REPOSITORY_INVENTORY.json")
    ap.add_argument("--write-report",default=None)
    args=ap.parse_args(argv)
    try: data=load_json(Path(args.inventory)); errors=validate_inventory(data)
    except Exception as exc:
        data={}; errors=[f"load_error: {exc}"]
    report=build_report(data,errors)
    rendered=json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.write_report: Path(args.write_report).write_text(rendered,encoding="utf-8")
    print(rendered,end="")
    return 0 if not errors else 1

if __name__=="__main__": sys.exit(main())
