#!/usr/bin/env python3
"""
Resolve GitHub Actions version tags to commit SHAs via GitHub API.

Queries GitHub API for action releases and validates commit SHAs.
Supports caching to avoid rate limiting.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Dict, Optional, Tuple

API_VERSION = "2022-11-28"
ACCEPT = "application/vnd.github+json"


def _request(url: str, token: str, opener=urllib.request.urlopen) -> Tuple[int, Optional[Dict]]:
    """Execute GitHub API request with Bearer token authentication."""
    req = urllib.request.Request(url)
    req.add_header("Accept", ACCEPT)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("X-GitHub-Api-Version", API_VERSION)
    req.add_header("User-Agent", "rafaelia-action-resolver")
    try:
        with opener(req) as response:
            raw = response.read()
            return response.status, json.loads(raw.decode("utf-8")) if raw else None
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API HTTP {exc.code}: {raw}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"GitHub API transport failure: {exc.reason}") from exc


def resolve_action_sha(action_ref: str, token: str, opener=urllib.request.urlopen) -> Optional[str]:
    """
    Resolve action@version to commit SHA.

    Args:
        action_ref: "actions/checkout@v4" or "actions/setup-python@v5"
        token: GitHub API token
        opener: urllib.request.urlopen or test double

    Returns:
        40-character commit SHA or None if resolution fails
    """
    parts = action_ref.split("@")
    if len(parts) != 2:
        print(f"ERROR: Invalid action ref format: {action_ref}", file=sys.stderr)
        return None

    repo_path, version_tag = parts

    # If already a SHA (40 hex chars), return as-is
    if len(version_tag) == 40 and all(c in "0123456789abcdef" for c in version_tag.lower()):
        return version_tag

    # Query GitHub API for release
    url = f"https://api.github.com/repos/{repo_path}/releases/tags/{version_tag}"
    try:
        status, data = _request(url, token, opener=opener)
    except RuntimeError as exc:
        print(f"ERROR resolving {action_ref}: {exc}", file=sys.stderr)
        return None

    if status == 404:
        print(f"WARNING: Release not found for {action_ref}", file=sys.stderr)
        return None

    if status != 200:
        print(f"ERROR: Unexpected status {status} for {action_ref}", file=sys.stderr)
        return None

    if not isinstance(data, dict):
        print(f"ERROR: Invalid response for {action_ref}", file=sys.stderr)
        return None

    # Extract commit SHA from release
    target_commitish = data.get("target_commitish")
    if not target_commitish:
        print(f"ERROR: No target_commitish in release for {action_ref}", file=sys.stderr)
        return None

    # Validate SHA format (40 hex chars)
    if len(target_commitish) != 40 or not all(c in "0123456789abcdef" for c in target_commitish.lower()):
        print(f"ERROR: Invalid SHA format for {action_ref}: {target_commitish}", file=sys.stderr)
        return None

    print(f"✓ {action_ref} → {target_commitish}")
    return target_commitish


def main(argv=None):
    p = argparse.ArgumentParser(description="Resolve GitHub Actions version tags to commit SHAs")
    p.add_argument("--action-ref", required=True, help="Action reference (e.g., actions/checkout@v4)")
    p.add_argument("--token-env", default="GITHUB_TOKEN", help="Environment variable containing GitHub token")
    ns = p.parse_args(argv)

    token = os.environ.get(ns.token_env, "").strip()
    if not token:
        print(f"REJECT missing token in {ns.token_env}", file=sys.stderr)
        return 1

    sha = resolve_action_sha(ns.action_ref, token)
    if not sha:
        print(f"REJECT failed to resolve {ns.action_ref}", file=sys.stderr)
        return 2

    result = {"action": ns.action_ref, "sha": sha, "validated": True}
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
