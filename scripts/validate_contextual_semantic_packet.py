#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

LAYERS = {
    "literal", "technical", "mathematical", "statistical", "historical",
    "economic", "symbolic", "ethical", "operational",
}
GAPS = {
    "TV-DEF", "TV-SOURCE", "TV-ACCESS", "TV-DATA", "TV-UNIT",
    "TV-BOUNDARY", "TV-CODE", "TV-TEST", "TV-ENV",
    "TV-INDEPENDENCE", "TV-IRREDUCIBLE",
}
EPI = {"FATO", "EVIDENCIADO", "HIPOTESE", "TOKEN_VAZIO", "CONTRADICAO"}


class PacketError(ValueError):
    pass


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_packet(packet: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(
        packet.get("schema_version") == "rafaelia.contextual-semantic-packet/v1",
        "schema_version",
    )
    require(packet.get("claim_allowed") is False, "claim_allowed_must_be_false")

    for key in (
        "query", "sources", "memory_claims", "entities", "relations", "layers",
        "invariants", "gaps", "hypotheses", "retrieval_plan", "answer_gate",
        "F_ok", "F_gap", "F_next",
    ):
        require(key in packet, f"missing:{key}")

    sources = packet.get("sources", [])
    source_ids: set[str] = set()
    for index, source in enumerate(sources):
        sid = source.get("source_id") if isinstance(source, dict) else None
        require(
            isinstance(sid, str) and sid.startswith("src:"),
            f"source[{index}].id",
        )
        require(sid not in source_ids, f"duplicate_source:{sid}")
        source_ids.add(sid)
        require(
            source.get("authorization") in {"authorized", "public", "withheld", "unknown"},
            f"source[{index}].authorization",
        )
        require(source.get("epistemic_state") in EPI, f"source[{index}].state")

    entity_ids: set[str] = set()
    for index, entity in enumerate(packet.get("entities", [])):
        eid = entity.get("entity_id") if isinstance(entity, dict) else None
        require(
            isinstance(eid, str) and eid.startswith("ent:"),
            f"entity[{index}].id",
        )
        require(eid not in entity_ids, f"duplicate_entity:{eid}")
        entity_ids.add(eid)
        require(entity.get("layer") in LAYERS, f"entity[{index}].layer")

    for index, claim in enumerate(packet.get("memory_claims", [])):
        for ref in claim.get("source_refs", []):
            require(ref in source_ids, f"claim[{index}].source:{ref}")
        require(claim.get("epistemic_state") in EPI, f"claim[{index}].state")

    for index, relation in enumerate(packet.get("relations", [])):
        require(relation.get("subject") in entity_ids, f"relation[{index}].subject")
        require(relation.get("object") in entity_ids, f"relation[{index}].object")
        for ref in relation.get("source_refs", []):
            require(ref in source_ids, f"relation[{index}].source:{ref}")
        require(relation.get("epistemic_state") in EPI, f"relation[{index}].state")

    blocking_gaps = 0
    for index, gap in enumerate(packet.get("gaps", [])):
        require(gap.get("gap_class") in GAPS, f"gap[{index}].class")
        require(bool(gap.get("reason")), f"gap[{index}].reason")
        require(bool(gap.get("next_gate")), f"gap[{index}].next_gate")
        if gap.get("blocking") is True:
            blocking_gaps += 1

    for index, hypothesis in enumerate(packet.get("hypotheses", [])):
        require(
            hypothesis.get("epistemic_state") in {"HIPOTESE", "TOKEN_VAZIO", "CONTRADICAO"},
            f"hypothesis[{index}].state",
        )
        confidence = hypothesis.get("confidence")
        require(
            isinstance(confidence, (int, float)) and 0 <= confidence <= 1,
            f"hypothesis[{index}].confidence",
        )
        for ref in hypothesis.get("source_refs", []):
            require(ref in source_ids, f"hypothesis[{index}].source:{ref}")
        for ref in hypothesis.get("entity_refs", []):
            require(ref in entity_ids, f"hypothesis[{index}].entity:{ref}")

    gate = packet.get("answer_gate", {})
    answer_allowed = gate.get("allowed") is True
    unresolved_required = [
        source.get("source_id")
        for source in sources
        if source.get("required") is True
        and (
            source.get("observed") is not True
            or source.get("authorization") not in {"authorized", "public"}
        )
    ]

    if answer_allowed:
        require(blocking_gaps == 0, "answer_allowed_with_blocking_gap")
        require(not unresolved_required, "answer_allowed_with_unresolved_source")

    require(
        isinstance(packet.get("F_next"), list) and len(packet.get("F_next", [])) > 0,
        "F_next",
    )

    if errors:
        raise PacketError(";".join(errors))

    return {
        "schema": "rafaelia.contextual-semantic-validation/v1",
        "status": "PASS",
        "packet_id": packet.get("packet_id"),
        "canonical_sha256": canonical_sha256(packet),
        "sources": len(source_ids),
        "entities": len(entity_ids),
        "relations": len(packet.get("relations", [])),
        "blocking_gaps": blocking_gaps,
        "unresolved_required_sources": unresolved_required,
        "answer_allowed": answer_allowed,
        "claim_allowed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    try:
        report = validate_packet(json.loads(args.packet.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, PacketError) as exc:
        report = {
            "schema": "rafaelia.contextual-semantic-validation/v1",
            "status": "FAIL",
            "claim_allowed": False,
            "reason": str(exc),
        }

    text = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
