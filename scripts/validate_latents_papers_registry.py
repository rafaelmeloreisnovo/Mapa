#!/usr/bin/env python3
"""Fail-closed validator for RAFAELIA latent and paper-claim JSONL registries.

Stdlib-only by design. It validates the operational invariants used by the
repository. Full JSON Schema validation may be added in CI, but this script
must remain usable in Termux and minimal runners.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
LATENTS = ROOT / "data" / "latents" / "latents.index.jsonl"
CLAIMS = ROOT / "data" / "claims" / "paper_claims.index.jsonl"

LATENT_REQUIRED = {
    "schema", "latent_id", "title", "latent_type", "source_references",
    "domains", "summary", "epistemic_state", "evidence_ids", "falsifiers",
    "gaps", "next_gate", "destination", "privacy_class",
    "license_or_authorization", "claim_allowed",
}
CLAIM_REQUIRED = {
    "schema", "claim_id", "statement", "claim_type", "ink", "state",
    "source_refs", "evidence_refs", "falsifiers", "limitations",
    "privacy_class", "license_or_authorization", "claim_allowed",
}

ID_RE = re.compile(r"^(LAT|CLM)-[A-Z0-9][A-Z0-9._-]{2,63}$")
TOKEN_RE = re.compile(r"^TOKEN_VAZIO(?:_[A-Z0-9_]+)?$")
PUBLICATION_PRIVACY = {"PUBLIC", "AUTHORIZED_PRIVATE"}


class ValidationError(RuntimeError):
    pass


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValidationError(f"missing registry: {path.relative_to(ROOT)}")
    records: list[dict[str, Any]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValidationError(f"{path}:{line_no}: record must be an object")
        records.append(value)
    if not records:
        raise ValidationError(f"empty registry: {path.relative_to(ROOT)}")
    return records


def require(record: dict[str, Any], fields: set[str], label: str) -> None:
    missing = sorted(fields - record.keys())
    if missing:
        raise ValidationError(f"{label}: missing fields: {', '.join(missing)}")


def require_nonempty_strings(values: Any, label: str) -> None:
    if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
        raise ValidationError(f"{label}: expected list of non-empty strings")


def validate_unique(records: Iterable[dict[str, Any]], key: str) -> None:
    seen: set[str] = set()
    for record in records:
        value = record.get(key)
        if not isinstance(value, str) or not ID_RE.fullmatch(value):
            raise ValidationError(f"invalid {key}: {value!r}")
        if value in seen:
            raise ValidationError(f"duplicate {key}: {value}")
        seen.add(value)


def validate_latent(record: dict[str, Any]) -> None:
    label = str(record.get("latent_id", "<unknown latent>"))
    require(record, LATENT_REQUIRED, label)
    if record["schema"] != "rafaelia.latent-artifact.v1":
        raise ValidationError(f"{label}: wrong schema")
    require_nonempty_strings(record["domains"], f"{label}.domains")
    require_nonempty_strings(record["destination"], f"{label}.destination")
    if not isinstance(record["source_references"], list) or not record["source_references"]:
        raise ValidationError(f"{label}: source_references must be non-empty")
    if not isinstance(record["gaps"], list):
        raise ValidationError(f"{label}: gaps must be a list")
    for gap in record["gaps"]:
        if not isinstance(gap, dict):
            raise ValidationError(f"{label}: gap must be an object")
        token = gap.get("token")
        if not isinstance(token, str) or not TOKEN_RE.fullmatch(token):
            raise ValidationError(f"{label}: invalid TOKEN_VAZIO: {token!r}")
        if not gap.get("reason") or not gap.get("expected_artifact"):
            raise ValidationError(f"{label}: TOKEN_VAZIO needs reason and expected_artifact")
    if record["gaps"] and not str(record["next_gate"]).strip():
        raise ValidationError(f"{label}: gaps require next_gate")
    if record["claim_allowed"] is True:
        if record["epistemic_state"] not in {"PASS", "VERIFIED_LOCAL"}:
            raise ValidationError(f"{label}: claim_allowed requires PASS/VERIFIED_LOCAL")
        if record["gaps"]:
            raise ValidationError(f"{label}: claim_allowed cannot coexist with gaps")
        require_nonempty_strings(record["evidence_ids"], f"{label}.evidence_ids")
        require_nonempty_strings(record["falsifiers"], f"{label}.falsifiers")
        if record["privacy_class"] not in PUBLICATION_PRIVACY:
            raise ValidationError(f"{label}: privacy class blocks claim promotion")
        if record["license_or_authorization"] == "TOKEN_VAZIO":
            raise ValidationError(f"{label}: authorization is TOKEN_VAZIO")


def validate_claim(record: dict[str, Any]) -> None:
    label = str(record.get("claim_id", "<unknown claim>"))
    require(record, CLAIM_REQUIRED, label)
    if record["schema"] != "rafaelia.paper-claim-ledger.v1":
        raise ValidationError(f"{label}: wrong schema")
    require_nonempty_strings(record["source_refs"], f"{label}.source_refs")
    if record["claim_allowed"] is True:
        if record["state"] != "PASS":
            raise ValidationError(f"{label}: claim_allowed requires state PASS")
        if record["ink"] in {"PARABLE", "TOKEN_VAZIO"}:
            raise ValidationError(f"{label}: ink cannot be promoted")
        require_nonempty_strings(record["evidence_refs"], f"{label}.evidence_refs")
        require_nonempty_strings(record["falsifiers"], f"{label}.falsifiers")
        require_nonempty_strings(record["limitations"], f"{label}.limitations")
        if record["privacy_class"] not in PUBLICATION_PRIVACY:
            raise ValidationError(f"{label}: privacy class blocks publication")
        if record["license_or_authorization"] == "TOKEN_VAZIO":
            raise ValidationError(f"{label}: authorization is TOKEN_VAZIO")


def main() -> int:
    latents = read_jsonl(LATENTS)
    claims = read_jsonl(CLAIMS)
    validate_unique(latents, "latent_id")
    validate_unique(claims, "claim_id")
    for record in latents:
        validate_latent(record)
    for record in claims:
        validate_claim(record)
    promoted = sum(1 for record in claims if record["claim_allowed"] is True)
    print(
        json.dumps(
            {
                "state": "PASS",
                "latent_records": len(latents),
                "claim_records": len(claims),
                "claim_allowed_true_count": promoted,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
