#!/usr/bin/env python3
"""Retrieve the newest prior RAFAELIA microcycle index artifact for one branch.

No absence is hidden. A genuine first run emits TOKEN_VAZIO_NO_PREVIOUS_INDEX and
continues as a new append-only segment. API, authorization, malformed ZIP, or
integrity transport failures block the workflow instead of silently resetting
history.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

ARTIFACT_FILE = "microcycle_index.json"


class PreviousIndexFetchError(RuntimeError):
    pass


def request_json(url: str, token: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "rafaelia-microcycle-index-v1",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        value = json.load(response)
    if not isinstance(value, dict):
        raise PreviousIndexFetchError("GitHub API returned a non-object response")
    return value


def download_zip(url: str, token: str, destination: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "rafaelia-microcycle-index-v1",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        with destination.open("wb") as handle:
            shutil.copyfileobj(response, handle)


def write_state(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def choose_artifact(
    artifacts: list[dict[str, Any]], *, current_run_id: str, head_branch: str
) -> dict[str, Any] | None:
    candidates = []
    for artifact in artifacts:
        if not isinstance(artifact, dict) or artifact.get("expired") is True:
            continue
        workflow_run = artifact.get("workflow_run")
        if not isinstance(workflow_run, dict):
            continue
        if str(workflow_run.get("id")) == str(current_run_id):
            continue
        if workflow_run.get("head_branch") != head_branch:
            continue
        candidates.append(artifact)
    candidates.sort(key=lambda item: str(item.get("created_at", "")), reverse=True)
    return candidates[0] if candidates else None


def extract_index(archive: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive) as bundle:
        matches = [name for name in bundle.namelist() if Path(name).name == ARTIFACT_FILE]
        if len(matches) != 1:
            raise PreviousIndexFetchError(
                f"expected exactly one {ARTIFACT_FILE} in artifact, found {len(matches)}"
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        with bundle.open(matches[0]) as source, destination.open("wb") as target:
            shutil.copyfileobj(source, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--artifact-name", required=True)
    parser.add_argument("--current-run-id", required=True)
    parser.add_argument("--head-branch", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--api-url", default="https://api.github.com")
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    state_path = args.output_dir / "fetch_state.json"
    if not token:
        write_state(
            state_path,
            {
                "state": "BLOCKED_TOKEN_VAZIO_TOKEN_UNAVAILABLE",
                "claim_allowed": False,
            },
        )
        print("GitHub token unavailable; refusing to reset append-only continuity")
        return 2

    query = urllib.parse.urlencode(
        {"name": args.artifact_name, "per_page": 100}
    )
    url = f"{args.api_url.rstrip('/')}/repos/{args.repository}/actions/artifacts?{query}"
    try:
        payload = request_json(url, token)
        artifacts = payload.get("artifacts")
        if not isinstance(artifacts, list):
            raise PreviousIndexFetchError("artifact listing is missing artifacts[]")
        selected = choose_artifact(
            artifacts,
            current_run_id=args.current_run_id,
            head_branch=args.head_branch,
        )
        if selected is None:
            write_state(
                state_path,
                {
                    "state": "TOKEN_VAZIO_NO_PREVIOUS_INDEX",
                    "artifact_name": args.artifact_name,
                    "head_branch": args.head_branch,
                    "claim_allowed": False,
                },
            )
            print("No previous index artifact exists for this branch; starting a new segment")
            return 0

        archive_url = selected.get("archive_download_url")
        if not isinstance(archive_url, str) or not archive_url:
            raise PreviousIndexFetchError("selected artifact lacks archive_download_url")
        archive = args.output_dir / "previous_index.zip"
        download_zip(archive_url, token, archive)
        output = args.output_dir / "previous_index.json"
        extract_index(archive, output)
        workflow_run = selected.get("workflow_run") or {}
        write_state(
            state_path,
            {
                "state": "FOUND_VERIFIED_TRANSPORT",
                "artifact_id": selected.get("id"),
                "artifact_name": selected.get("name"),
                "artifact_digest": selected.get("digest"),
                "created_at": selected.get("created_at"),
                "run_id": workflow_run.get("id"),
                "head_branch": workflow_run.get("head_branch"),
                "head_sha": workflow_run.get("head_sha"),
                "claim_allowed": False,
            },
        )
        print(f"Previous index artifact {selected.get('id')} retrieved")
        return 0
    except (
        OSError,
        json.JSONDecodeError,
        urllib.error.URLError,
        zipfile.BadZipFile,
        PreviousIndexFetchError,
    ) as error:
        write_state(
            state_path,
            {
                "state": "BLOCKED_PREVIOUS_INDEX_RETRIEVAL",
                "error": f"{type(error).__name__}: {error}",
                "claim_allowed": False,
            },
        )
        print(f"Previous index retrieval failed closed: {type(error).__name__}: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
