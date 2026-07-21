#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

API_VERSION = "2022-11-28"
USER_AGENT = "Mapa-G006-Materializer/1.0"


class MaterializationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise MaterializationError(message)


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_contents_payload(payload: dict[str, Any]) -> bytes:
    require(isinstance(payload, dict), "GitHub response must be an object")
    require(payload.get("type", "file") == "file", "GitHub content must be a file")
    require(payload.get("encoding") == "base64", "GitHub content encoding must be base64")
    content = payload.get("content")
    require(isinstance(content, str) and content, "GitHub Base64 content is missing")
    compact = "".join(content.split())
    try:
        return base64.b64decode(compact, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise MaterializationError(f"invalid Base64 content: {exc}") from exc


def verify_materialization(
    data: bytes,
    *,
    expected_blob_sha1: str,
    expected_size: int | None = None,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    require(
        isinstance(expected_blob_sha1, str)
        and len(expected_blob_sha1) == 40
        and all(char in "0123456789abcdef" for char in expected_blob_sha1),
        "expected Git blob SHA-1 must be 40 lowercase hex characters",
    )
    observed_blob = git_blob_sha1(data)
    require(observed_blob == expected_blob_sha1, "Git blob SHA-1 mismatch")
    observed_sha256 = sha256_hex(data)
    if expected_size is not None:
        require(expected_size >= 0, "expected size must be non-negative")
        require(len(data) == expected_size, "decoded size mismatch")
    if expected_sha256 is not None:
        require(
            len(expected_sha256) == 64
            and all(char in "0123456789abcdef" for char in expected_sha256),
            "expected SHA-256 must be 64 lowercase hex characters",
        )
        require(observed_sha256 == expected_sha256, "SHA-256 mismatch")
    return {
        "decoded_size_bytes": len(data),
        "git_blob_sha1": observed_blob,
        "sha256": observed_sha256,
        "identity_verified": True,
    }


def build_contents_url(api_url: str, repository: str, path: str, ref: str) -> str:
    require("/" in repository and not repository.startswith("/"), "repository must be owner/name")
    require(path and not path.startswith("/"), "path must be repository-relative")
    require(ref, "ref is required")
    base = api_url.rstrip("/")
    quoted_repo = "/".join(urllib.parse.quote(part, safe="") for part in repository.split("/", 1))
    quoted_path = urllib.parse.quote(path, safe="/")
    quoted_ref = urllib.parse.quote(ref, safe="")
    return f"{base}/repos/{quoted_repo}/contents/{quoted_path}?ref={quoted_ref}"


def fetch_contents_payload(
    *,
    repository: str,
    path: str,
    ref: str,
    token: str | None,
    api_url: str = "https://api.github.com",
    timeout_seconds: int = 60,
) -> tuple[dict[str, Any], str]:
    url = build_contents_url(api_url, repository, path, ref)
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": API_VERSION,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raise MaterializationError(f"GitHub HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise MaterializationError(f"GitHub connection failed: {exc.reason}") from exc
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MaterializationError(f"invalid GitHub JSON response: {exc}") from exc
    require(isinstance(payload, dict), "GitHub response root must be an object")
    return payload, url


def atomic_write(path: Path, data: bytes, *, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def build_receipt(
    *,
    repository: str,
    path: str,
    ref: str,
    source_url: str,
    output_path: Path,
    verification: dict[str, Any],
    github_reported_sha: str | None,
    github_reported_size: int | None,
) -> dict[str, Any]:
    return {
        "schema": "mapa.github-content-materialization-receipt.v1",
        "status": "PASS",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": {
            "repository": repository,
            "path": path,
            "ref": ref,
            "url": source_url,
            "github_reported_sha": github_reported_sha,
            "github_reported_size": github_reported_size,
        },
        "output": {
            "path": str(output_path),
            **verification,
            "atomic_write": True,
            "file_mode": "0600",
        },
        "boundaries": {
            "credential_recorded": False,
            "claim_allowed": False,
            "certification_claim": False,
            "portfolio_exit_criteria_met": False,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--expected-blob-sha1", required=True)
    parser.add_argument("--expected-size", type=int)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--token-env", default="GITHUB_TOKEN")
    parser.add_argument("--api-url", default="https://api.github.com")
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args(argv)

    try:
        token = os.environ.get(args.token_env)
        payload, source_url = fetch_contents_payload(
            repository=args.repository,
            path=args.path,
            ref=args.ref,
            token=token,
            api_url=args.api_url,
            timeout_seconds=args.timeout_seconds,
        )
        data = decode_contents_payload(payload)
        verification = verify_materialization(
            data,
            expected_blob_sha1=args.expected_blob_sha1,
            expected_size=args.expected_size,
            expected_sha256=args.expected_sha256,
        )
        reported_sha = payload.get("sha")
        reported_size = payload.get("size")
        require(reported_sha in {None, verification["git_blob_sha1"]}, "GitHub-reported SHA differs")
        require(reported_size in {None, verification["decoded_size_bytes"]}, "GitHub-reported size differs")
        atomic_write(args.output, data)
        receipt = build_receipt(
            repository=args.repository,
            path=args.path,
            ref=args.ref,
            source_url=source_url,
            output_path=args.output,
            verification=verification,
            github_reported_sha=reported_sha,
            github_reported_size=reported_size,
        )
        atomic_write(
            args.receipt,
            (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"),
        )
    except (MaterializationError, OSError) as exc:
        print(
            json.dumps(
                {
                    "status": "FAIL",
                    "error": str(exc),
                    "credential_recorded": False,
                    "claim_allowed": False,
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1

    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
