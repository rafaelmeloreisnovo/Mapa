#!/usr/bin/env python3
"""Fail-closed validator for RAFAELIA shared-data release manifests.

This validator intentionally has no Drive API or credential support. It validates
only explicit manifest files already present in the checkout.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

CRITICALITIES = {"C0_PUBLIC", "C1_INTERNAL", "C2_SENSITIVE", "C3_RESTRICTED", "C4_CRITICAL"}
APPROVALS = {"BLOCKED", "APPROVED_LIMITED", "APPROVED", "REJECTED", "EXPIRED", "REVOKED"}
RISKS = {"LOW", "MEDIUM", "HIGH", "TOKEN_VAZIO"}
REDACTION = {"NOT_REQUIRED", "PASS", "FAIL", "TOKEN_VAZIO"}
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
SHARE_ID_RE = re.compile(r"^SHARE-[A-Za-z0-9._-]+$")
REPOSITORY_RE = re.compile(r"^[^/]+/[^/]+$")

REQUIRED = {
    "schema_version", "share_id", "source_locator", "source_revision_or_sha256",
    "source_criticality", "fragment_sha256", "fragment_size", "purpose",
    "allowed_repository", "allowed_workflow", "allowed_operation", "created_at",
    "expires_at", "redaction_status", "reidentification_risk",
    "semantic_reconstruction_risk", "approval_state", "revoked",
    "credential_or_secret_presence", "claim_allowed", "token_vazio"
}

OPTIONAL = {"downstream_effects_summary", "human_awareness_summary", "human_approval"}


def _parse_timestamp(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("missing timestamp")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_manifest(manifest, now=None):
    errors = []

    missing = sorted(REQUIRED - set(manifest))
    if missing:
        return ["missing:" + ",".join(missing)]

    extra = sorted(set(manifest) - REQUIRED - OPTIONAL)
    if extra:
        errors.append("additional_properties:" + ",".join(extra))

    if manifest["schema_version"] != "rafaelia.shared-data-release/v1":
        errors.append("schema_version")
    if not isinstance(manifest["share_id"], str) or not SHARE_ID_RE.fullmatch(manifest["share_id"]):
        errors.append("share_id")
    if manifest["source_criticality"] not in CRITICALITIES:
        errors.append("source_criticality")
    if not isinstance(manifest["fragment_sha256"], str) or not SHA256_RE.fullmatch(manifest["fragment_sha256"]):
        errors.append("fragment_sha256")
    if not isinstance(manifest["fragment_size"], int) or isinstance(manifest["fragment_size"], bool) or manifest["fragment_size"] < 0:
        errors.append("fragment_size")

    for key in ("source_locator", "source_revision_or_sha256", "purpose", "allowed_workflow", "allowed_operation"):
        if not isinstance(manifest[key], str) or not manifest[key].strip():
            errors.append(key)

    if not isinstance(manifest["allowed_repository"], str) or not REPOSITORY_RE.fullmatch(manifest["allowed_repository"]):
        errors.append("allowed_repository")
    if manifest["approval_state"] not in APPROVALS:
        errors.append("approval_state")
    if manifest["redaction_status"] not in REDACTION:
        errors.append("redaction_status")
    if manifest["reidentification_risk"] not in RISKS:
        errors.append("reidentification_risk")
    if manifest["semantic_reconstruction_risk"] not in RISKS:
        errors.append("semantic_reconstruction_risk")
    if manifest["claim_allowed"] is not False:
        errors.append("claim_allowed_must_be_false")
    if manifest["revoked"] is not False:
        errors.append("revoked")
    if manifest["credential_or_secret_presence"] is not False:
        errors.append("credential_or_secret_presence")
    if not isinstance(manifest["token_vazio"], list):
        errors.append("token_vazio")

    try:
        created = _parse_timestamp(manifest["created_at"])
        expires = _parse_timestamp(manifest["expires_at"])
        if expires <= created:
            errors.append("expires_not_after_created")
        check_now = now or datetime.now(timezone.utc)
        if check_now.tzinfo is None:
            check_now = check_now.replace(tzinfo=timezone.utc)
        if expires.astimezone(timezone.utc) <= check_now.astimezone(timezone.utc):
            errors.append("expired")
    except (TypeError, ValueError):
        errors.append("timestamps")

    criticality = manifest["source_criticality"]

    # C4 raw-byte automation is categorically blocked by this V1 contract.
    if criticality == "C4_CRITICAL":
        errors.append("C4_raw_automation_prohibited")

    # C2/C3 require explicit privacy-risk closure before a fragment is releaseable.
    if criticality in {"C2_SENSITIVE", "C3_RESTRICTED"}:
        if manifest["redaction_status"] != "PASS":
            errors.append("C2plus_redaction_required")
        if manifest["reidentification_risk"] == "TOKEN_VAZIO":
            errors.append("C2plus_reidentification_TOKEN_VAZIO")
        if manifest["semantic_reconstruction_risk"] == "TOKEN_VAZIO":
            errors.append("C2plus_semantic_TOKEN_VAZIO")

    if criticality in {"C3_RESTRICTED", "C4_CRITICAL"} and manifest.get("human_approval") is not True:
        errors.append("human_approval_required")

    if manifest["approval_state"] not in {"APPROVED", "APPROVED_LIMITED"}:
        errors.append("approval_not_releaseable")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="+")
    parser.add_argument("--expect-blocked", action="store_true")
    args = parser.parse_args()

    failed = False
    for manifest_path in args.manifest:
        path = Path(manifest_path)
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # fail closed on unreadable/malformed input
            print(f"FAIL {path}: json:{exc}")
            failed = True
            continue

        errors = validate_manifest(manifest)
        blocked = bool(errors)
        print(("BLOCKED" if blocked else "PASS") + f" {path}")
        for error in errors:
            print(f"  - {error}")

        if args.expect_blocked:
            if not blocked:
                print(f"FAIL {path}: expected blocked")
                failed = True
        elif blocked:
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
