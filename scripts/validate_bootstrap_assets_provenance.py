#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

EXPECTED_MISSING = {
    "arm64-v8a.tar",
    "armeabi-v7a.tar",
    "x86.tar",
    "x86_64.tar",
}
FALSE_BOUNDARIES = {
    "loader_apk_is_complete_bootstrap",
    "apk_build_is_device_runtime",
    "digest_is_provenance",
    "drive_copy_is_original_source",
    "documentation_claim_is_file_presence",
    "blocked_contract_is_release_permission",
}


def fail(message: str) -> None:
    raise ValueError(message)


def validate(data: dict[str, Any]) -> None:
    if data.get("schema_version") != "bootstrap-assets-provenance.v1": fail("schema_version")
    if data.get("claim_allowed") is not False or data.get("release_allowed") is not False:
        fail("global promotion")
    producer = data.get("producer", {})
    if producer.get("repository") != "rafaelmeloreisnovo/Vectras-VM-Android": fail("producer")
    if producer.get("pull_request") != 1080 or producer.get("base_pull_request") != 1078:
        fail("stacked producer")
    if producer.get("merged") is not False: fail("producer merged")
    head = producer.get("head_sha")
    if not isinstance(head, str) or len(head) != 40: fail("head_sha")
    int(head, 16)
    if producer.get("gate_name") != "Bootstrap Assets Provenance V1": fail("gate name")

    reality = data.get("observed_reality", {})
    if reality.get("loader_apk_generated_in_ci") is not True: fail("loader observation")
    if reality.get("architecture_tar_count_required") != 4: fail("required count")
    if reality.get("architecture_tar_count_present") != 0: fail("present count")
    if set(reality.get("missing", [])) != EXPECTED_MISSING: fail("missing set")
    if reality.get("android_ci_state") != "BETA_BLOCKED_MISSING_BOOTSTRAP_ASSETS":
        fail("Android blocked state")

    boundaries = data.get("authority_separation", {})
    for key in FALSE_BOUNDARIES:
        if boundaries.get(key) is not False: fail(f"unsafe authority: {key}")

    required = set(data.get("required_per_asset", []))
    if required != {"ABI", "EXACT_FILENAME", "SOURCE_URI", "IMMUTABLE_SOURCE_REF", "LICENSE_OR_PROVENANCE", "SHA256", "SIZE_BYTES", "SAFE_READABLE_TAR"}:
        fail("required asset evidence")

    sequence = data.get("promotion_sequence", [])
    if not isinstance(sequence, list) or sequence[-1:] != ["SEPARATE_RELEASE_DECISION"]:
        fail("promotion sequence")
    if sequence.index("ANDROID_BUILD_PASS") >= sequence.index("DEVICE_BOOTSTRAP_RECEIPT"):
        fail("build/device ordering")

    storage = data.get("privacy_and_storage", {})
    if storage.get("network_download_by_materializer") is not False: fail("network materializer")
    if storage.get("drive_may_store_verified_copy") is not True: fail("Drive storage")
    if storage.get("drive_replaces_source_provenance") is not False: fail("Drive provenance")
    if storage.get("private_source_may_be_published_by_default") is not False: fail("privacy")

    claims = data.get("claims", {})
    for key in ("official_bootstrap_assets_present", "beta_installable", "android_runtime_verified", "device_bootstrap_verified", "release_allowed", "claim_allowed"):
        if claims.get(key) is not False: fail(f"claim promoted: {key}")


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/control-plane/bootstrap-assets-provenance.v1.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict): fail("root")
    validate(data)
    print("BOOTSTRAP_ASSETS_PROVENANCE_FEDERATION PASS")
    return 0


if __name__ == "__main__": raise SystemExit(main())
