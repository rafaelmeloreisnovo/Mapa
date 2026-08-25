#!/usr/bin/env python3
"""Fail-closed validator for the RAFAELIA Omega Assurance Adoption V2 pilot."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "control-plane" / "omega-assurance-adoption.v2.json"
LEDGER = ROOT / "data" / "ledgers" / "omega-assurance-adoption-events.v2.jsonl"
RECEIPT = ROOT / "data" / "receipts" / "OMEGA_ASSURANCE_ADOPTION_V2_20260824.v1.json"

EXPECTED_AXES = {f"D{i}" for i in range(1, 8)}
EXPECTED_CROSSFAIL = {f"CF-{i:02d}" for i in range(1, 13)}
EXPECTED_TRACKS = {f"TP-{i:02d}" for i in range(1, 16)}
EXPECTED_SOURCES = {f"EXT-{i:03d}" for i in range(1, 17)}
REQUIRED_INVARIANTS = {
    "TOKEN_VAZIO != PASS",
    "SEE_MORE != CLAIM_MORE",
    "CAN_DO != MAY_DO",
    "sandbox_pass != production_pass",
    "search_miss != absence",
    "unknown_privacy => PRIVATE_DEFAULT_DENY",
    "unknown_authority => HOLD_FOR_AUTHORITY",
    "irreversible_unknown_risk => HOLD",
    "P0_non_compensatory = true",
}
RISK_DIMENSIONS = {
    "authority",
    "security",
    "privacy",
    "governance",
    "integrity",
    "availability",
    "reversibility",
    "uncertainty",
}
SOURCE_KINDS = {"OFFICIAL_STANDARD", "OFFICIAL_SPEC", "OFFICIAL_DOCS", "PRIMARY_PAPER"}
PROHIBITED_LOCATOR = re.compile(r"drive:[A-Za-z0-9_-]{16,}|docs\.google\.com/(?:spreadsheets|document|presentation)/d/[A-Za-z0-9_-]{16,}")


def _ids(items: object) -> list[str]:
    if not isinstance(items, list):
        return []
    return [str(item.get("id")) for item in items if isinstance(item, dict)]


def _unique_exact(label: str, items: object, expected: set[str]) -> list[str]:
    ids = _ids(items)
    errors: list[str] = []
    if len(ids) != len(set(ids)):
        errors.append(f"{label}: duplicate id")
    if set(ids) != expected:
        errors.append(f"{label}: id set mismatch: {sorted(set(ids) ^ expected)}")
    return errors


def validate_manifest(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "rafaelia.omega-assurance-adoption/v2":
        errors.append("schema_version mismatch")
    if data.get("status") != "DRAFT_FAIL_CLOSED":
        errors.append("status must remain DRAFT_FAIL_CLOSED")
    if data.get("claim_allowed") is not False:
        errors.append("claim_allowed must be false")
    if data.get("append_only") is not True:
        errors.append("append_only must be true")

    errors.extend(_unique_exact("omega7_axes", data.get("omega7_axes"), EXPECTED_AXES))
    for axis in data.get("omega7_axes", []):
        if not isinstance(axis, dict):
            errors.append("omega7 axis must be object")
            continue
        for field in ("name", "question", "skill", "gate", "falsifier", "adoption_state"):
            if not axis.get(field):
                errors.append(f"{axis.get('id', 'axis')}: missing {field}")

    invariants = set(data.get("invariants", []))
    for required in REQUIRED_INVARIANTS:
        if required not in invariants:
            errors.append(f"missing invariant: {required}")

    risk = data.get("risk_vector", {})
    if set(risk.get("dimensions", [])) != RISK_DIMENSIONS:
        errors.append("risk dimensions mismatch")
    if risk.get("unknown_value") != "TOKEN_VAZIO":
        errors.append("unknown risk must remain TOKEN_VAZIO")
    if risk.get("p0_action") != "HOLD":
        errors.append("P0 action must be HOLD")
    if risk.get("compensation_allowed") is not False:
        errors.append("P0 risk must remain non-compensatory")

    watchdog = data.get("quiet_watchdog", {})
    if watchdog.get("modes") != ["WATCH", "WARN", "HOLD", "ACT_BOUNDED"]:
        errors.append("quiet watchdog modes mismatch")
    if watchdog.get("meta_watch_depth") != 2:
        errors.append("meta_watch_depth must equal 2")
    if watchdog.get("overflow_action") != "HOLD_FOR_AUDIT":
        errors.append("watchdog overflow must HOLD_FOR_AUDIT")
    if watchdog.get("heartbeat_loss_action") != "FAIL_CLOSED_HOLD":
        errors.append("heartbeat loss must FAIL_CLOSED_HOLD")

    tracks = data.get("producer_tracks")
    errors.extend(_unique_exact("producer_tracks", tracks, EXPECTED_TRACKS))
    if isinstance(tracks, list):
        if not any(t.get("authority") == "TOKEN_VAZIO_PRODUCER" for t in tracks if isinstance(t, dict)):
            errors.append("unresolved producer authority must remain visible")
        for track in tracks:
            if not isinstance(track, dict):
                errors.append("producer track must be object")
                continue
            for field in ("domain", "authority", "state", "receipt", "next_gate"):
                if not track.get(field):
                    errors.append(f"{track.get('id', 'track')}: missing {field}")
            if track.get("authority") == "TOKEN_VAZIO_PRODUCER" and track.get("state") not in {
                "ROUTE_REFERENCE_ONLY",
                "MODEL_ROUTE_ONLY",
            }:
                errors.append(f"{track.get('id')}: unresolved authority cannot claim execution")

    cases = data.get("crossfail_cases")
    errors.extend(_unique_exact("crossfail_cases", cases, EXPECTED_CROSSFAIL))
    if isinstance(cases, list):
        for case in cases:
            if not isinstance(case, dict):
                errors.append("crossfail case must be object")
                continue
            if case.get("execution_state") != "SPECIFIED_NOT_EXECUTED":
                errors.append(f"{case.get('id')}: execution state must remain SPECIFIED_NOT_EXECUTED in the seed manifest")
            expected = str(case.get("expected", ""))
            if not expected or expected in {"PASS", "PRODUCTION_PASS", "CLAIM_PASS"}:
                errors.append(f"{case.get('id')}: expected outcome cannot manufacture PASS")
            if not str(case.get("test_type", "")).startswith("TEST_"):
                errors.append(f"{case.get('id')}: invalid test_type")

    sources = data.get("primary_sources")
    errors.extend(_unique_exact("primary_sources", sources, EXPECTED_SOURCES))
    if isinstance(sources, list):
        for source in sources:
            if not isinstance(source, dict):
                errors.append("primary source must be object")
                continue
            if source.get("source_kind") not in SOURCE_KINDS:
                errors.append(f"{source.get('id')}: source must be official or primary")
            parsed = urlparse(str(source.get("url", "")))
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"{source.get('id')}: source URL must be HTTPS")
            if not source.get("boundary"):
                errors.append(f"{source.get('id')}: epistemic boundary missing")
            maps_to = source.get("maps_to")
            if not isinstance(maps_to, list) or not maps_to or not set(maps_to).issubset(EXPECTED_AXES):
                errors.append(f"{source.get('id')}: invalid maps_to")

    serialized = json.dumps(data, sort_keys=True)
    if PROHIBITED_LOCATOR.search(serialized):
        errors.append("private Drive-style locator must not be embedded")

    surface = data.get("session_surface", {})
    if surface.get("raw_private_content_embedded") is not False:
        errors.append("raw_private_content_embedded must be false")
    pet = surface.get("pet", {})
    if pet.get("authority") != "NONE":
        errors.append("session mascot must have no technical authority")
    return errors


def load_ledger(path: Path = LEDGER) -> tuple[list[dict], list[str]]:
    events: list[dict] = []
    errors: list[str] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"ledger line {line_number}: invalid JSON: {exc}")
            continue
        events.append(event)
    return events, errors


def validate_ledger(events: list[dict]) -> list[str]:
    errors: list[str] = []
    ids: list[str] = []
    previous: str | None = None
    for event in events:
        event_id = str(event.get("event_id", ""))
        ids.append(event_id)
        if event.get("schema_version") != "rafaelia.omega-assurance-adoption-event/v2":
            errors.append(f"{event_id}: ledger schema mismatch")
        if event.get("claim_allowed") is not False:
            errors.append(f"{event_id}: claim_allowed must be false")
        if event.get("append_only") is not True:
            errors.append(f"{event_id}: append_only must be true")
        for field in (
            "observed_on",
            "event_type",
            "surface",
            "source_ref",
            "from_state",
            "to_state",
            "reason",
            "evidence_state",
            "authority",
            "privacy_class",
            "prior_event_id",
            "next_gate",
        ):
            if not event.get(field):
                errors.append(f"{event_id}: missing {field}")
        if previous is None:
            if event.get("prior_event_id") != "TOKEN_VAZIO_FIRST_LOCAL_EVENT":
                errors.append(f"{event_id}: first event must preserve TOKEN_VAZIO predecessor")
        elif event.get("prior_event_id") != previous:
            errors.append(f"{event_id}: prior_event_id must equal {previous}")
        previous = event_id
    if not events:
        errors.append("ledger must contain at least one event")
    if len(ids) != len(set(ids)):
        errors.append("ledger event IDs must be unique")
    return errors


def validate_receipt(receipt: dict, manifest: dict) -> list[str]:
    errors: list[str] = []
    if receipt.get("schema_version") != "rafaelia.omega-assurance-adoption-receipt/v1":
        errors.append("receipt schema_version mismatch")
    if receipt.get("status") != "MATERIALIZED_VALIDATED_GOVERNANCE_PENDING":
        errors.append("receipt status mismatch")
    if receipt.get("claim_allowed") is not False:
        errors.append("receipt claim_allowed must be false")
    if receipt.get("append_only") is not True:
        errors.append("receipt append_only must be true")
    if receipt.get("base_main") != manifest.get("baseline", {}).get("commit"):
        errors.append("receipt base_main must match manifest baseline")
    if receipt.get("pull_request") != 393 or receipt.get("pull_request_state") != "DRAFT":
        errors.append("receipt must bind draft PR 393")

    drive = receipt.get("drive_first_delta", {})
    if drive.get("provider_write") != "SUCCESS" or drive.get("provider_readback") != "SUCCESS":
        errors.append("receipt Drive write/readback must be successful")
    if drive.get("tab_count_after") - drive.get("tab_count_before", 0) != 5:
        errors.append("receipt Drive tab delta must equal five")
    if drive.get("raw_private_content_embedded_in_github") is not False:
        errors.append("receipt must deny raw private Drive content embedding")

    local = receipt.get("local_qualification", {})
    if local.get("python_compile") != "PASS":
        errors.append("receipt local compile must PASS")
    tests = local.get("negative_and_structural_tests", {})
    if tests.get("count") != 15 or tests.get("conclusion") != "PASS":
        errors.append("receipt must bind 15 passing local tests")
    if local.get("validator", {}).get("conclusion") != "PASS":
        errors.append("receipt local validator must PASS")

    github = receipt.get("github_qualification", {})
    for gate in (
        "omega_assurance_adoption_v2",
        "general_ci",
        "branch_topology",
        "live_control_plane_reconciliation",
    ):
        record = github.get(gate, {})
        if not isinstance(record.get("run_id"), int) or record.get("conclusion") != "success":
            errors.append(f"receipt {gate} must bind a successful run")

    governance = receipt.get("independent_governance", {})
    promotion = governance.get("promotion_control", {})
    if promotion.get("conclusion") != "failure":
        errors.append("receipt promotion control must preserve observed failure")
    if promotion.get("interpretation") != "EXPECTED_FAIL_CLOSED_GOVERNANCE_DENIAL":
        errors.append("receipt promotion failure interpretation mismatch")
    if set(promotion.get("blocking_reasons", [])) != {
        "PULL_REQUEST_DRAFT_OR_UNKNOWN",
        "INDEPENDENT_APPROVAL_MISSING",
    }:
        errors.append("receipt promotion blocking reasons mismatch")

    server = governance.get("server_merge_enforcement", {})
    if server.get("conclusion") != "failure":
        errors.append("receipt server merge enforcement must preserve observed failure")
    if set(server.get("failure_modes", [])) != {
        "BRANCH_PROTECTION_DISABLED",
        "PROTECTION_NOT_ENABLED",
    }:
        errors.append("receipt server enforcement failure modes mismatch")
    if server.get("server_side_merge_binding") != "NOT_ENFORCED_OBSERVED":
        errors.append("receipt must preserve server merge enforcement gap")

    serialized = json.dumps(receipt, sort_keys=True)
    if PROHIBITED_LOCATOR.search(serialized):
        errors.append("receipt must not embed a private Drive-style locator")
    return errors


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    events, parse_errors = load_ledger()
    errors = validate_manifest(data) + parse_errors + validate_ledger(events) + validate_receipt(receipt, data)
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(
        json.dumps(
            {
                "status": "PASS",
                "manifest_id": data["manifest_id"],
                "axes": len(data["omega7_axes"]),
                "producer_tracks": len(data["producer_tracks"]),
                "crossfail_cases": len(data["crossfail_cases"]),
                "primary_sources": len(data["primary_sources"]),
                "ledger_events": len(events),
                "receipt_status": receipt["status"],
                "claim_allowed": data["claim_allowed"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
