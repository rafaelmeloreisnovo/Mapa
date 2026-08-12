#!/usr/bin/env python3
import argparse
import json
import os
import urllib.error
import urllib.request

API_VERSION = "2026-03-10"
ACCEPT = "application/vnd.github+json"


def build_payload(contexts):
    contexts = [c.strip() for c in contexts if c and c.strip()]
    if not contexts:
        raise ValueError("at least one required status-check context is required")
    return {
        "required_status_checks": {"strict": True, "contexts": contexts},
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 1,
            "require_last_push_approval": True,
        },
        "restrictions": None,
        "required_linear_history": False,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_conversation_resolution": True,
        "lock_branch": False,
        "allow_fork_syncing": False,
    }


def _request(url, token, method="GET", payload=None, opener=urllib.request.urlopen):
    data = None if payload is None else json.dumps(payload, sort_keys=True).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", ACCEPT)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("X-GitHub-Api-Version", API_VERSION)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with opener(req) as response:
            raw = response.read()
            return response.status, json.loads(raw.decode("utf-8")) if raw else None
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API HTTP {exc.code}: {raw}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"GitHub API transport failure: {exc.reason}") from exc


def verify_branch_metadata(doc):
    if not isinstance(doc, dict):
        return False, "branch metadata must be object"
    if doc.get("protected") is not True:
        return False, "protected!=true"
    protection = doc.get("protection")
    if not isinstance(protection, dict) or protection.get("enabled") is not True:
        return False, "protection.enabled!=true"
    checks = protection.get("required_status_checks")
    if not isinstance(checks, dict):
        return False, "required_status_checks missing"
    if checks.get("enforcement_level") in (None, "", "off"):
        return False, "status-check enforcement off"
    return True, "PASS"


def apply(owner, repo, branch, contexts, token, opener=urllib.request.urlopen):
    payload = build_payload(contexts)
    base = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
    status, _ = _request(base + "/protection", token, "PUT", payload, opener=opener)
    if status != 200:
        raise RuntimeError(f"unexpected protection update status: {status}")
    status, metadata = _request(base, token, "GET", opener=opener)
    if status != 200:
        raise RuntimeError(f"unexpected branch metadata status: {status}")
    ok, reason = verify_branch_metadata(metadata)
    if not ok:
        raise RuntimeError(f"postcondition failed: {reason}")
    return payload, metadata


def main(argv=None):
    p = argparse.ArgumentParser(description="Fail-closed default-branch protection applicator")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--branch", default="main")
    p.add_argument("--required-context", action="append", default=[])
    p.add_argument("--apply", action="store_true", help="perform provider mutation; default is dry-run")
    p.add_argument("--yes", action="store_true", help="explicitly acknowledge provider mutation")
    p.add_argument("--token-env", default="GITHUB_TOKEN")
    ns = p.parse_args(argv)
    try:
        payload = build_payload(ns.required_context)
    except ValueError as exc:
        print(f"REJECT {exc}")
        return 2
    print(json.dumps({"target": f"{ns.owner}/{ns.repo}:{ns.branch}", "payload": payload}, sort_keys=True))
    if not ns.apply:
        print("DRY_RUN no provider mutation performed")
        return 0
    if not ns.yes:
        print("REJECT --apply requires --yes")
        return 3
    token = os.environ.get(ns.token_env, "").strip()
    if not token:
        print(f"REJECT missing token in {ns.token_env}")
        return 4
    try:
        _, metadata = apply(ns.owner, ns.repo, ns.branch, ns.required_context, token)
    except RuntimeError as exc:
        print(f"REJECT {exc}")
        return 5
    print(json.dumps({"postcondition": "PASS", "branch": metadata.get("name")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
