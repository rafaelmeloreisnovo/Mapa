#!/usr/bin/env python3
"""Validate the RAFAELIA Omega static-address control-plane record."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "omega-static-address-relocation.v1"
BASE_POLICIES = {"BASE_RELATIVE", "FIXED_VIRTUAL", "FIXED_PHYSICAL", "TOKEN_VAZIO"}
MOBILITY = {
    "MOVABLE_BASE",
    "FIXED_OFFSET",
    "PINNED_RUNTIME",
    "REMAP_ONLY",
    "PHYSICAL_FIXED",
    "TOKEN_VAZIO",
}
REGION_STATES = {"ABSENT", "EMPTY", "PRESENT", "FAULT", "TOKEN_VAZIO"}
EVIDENCE_STATES = {
    "DOCUMENTED_ROADMAP",
    "SOURCE_PRESENT",
    "SOURCE_AND_TESTS_PRESENT",
    "VERIFIED_LIMITED",
    "PR_PENDING",
    "TOKEN_VAZIO",
}


class ValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def is_power_of_two(value: int) -> bool:
    return value > 0 and value & (value - 1) == 0


def validate(record: dict[str, Any]) -> dict[str, Any]:
    require(record.get("schema_version") == SCHEMA_VERSION, "schema_version inválida")
    require(record.get("claim_allowed") is False, "claim_allowed deve permanecer false")

    model = record.get("address_model")
    require(isinstance(model, dict), "address_model ausente")
    require(model.get("equation") == "ADDRESS=BASE+STABLE_OFFSET", "equação canônica inválida")
    require(model.get("base_policy") in BASE_POLICIES, "base_policy inválida")
    require(isinstance(model.get("mapping_epoch"), int) and model["mapping_epoch"] >= 0,
            "mapping_epoch inválida")

    reuse = record.get("reuse_contract")
    require(isinstance(reuse, dict), "reuse_contract ausente")
    require(reuse.get("offset_table") == "SAME_MANIFEST_SIGNATURE",
            "offset table exige mesma assinatura")
    require(reuse.get("absolute_pointer") ==
            "SAME_MANIFEST_SIGNATURE_AND_BASE_AND_MAPPING_EPOCH",
            "ponteiro absoluto exige assinatura, base e época")

    guards = record.get("semantic_guards")
    require(isinstance(guards, dict), "semantic_guards ausente")
    require(guards.get("system_attribute_is_pinning") is False,
            "ATTR.SYSTEM não pode equivaler a pinning")
    require(guards.get("fixed_offset_is_fixed_physical") is False,
            "FIXED_OFFSET não pode equivaler a FIXED_PHYSICAL")
    require(guards.get("fragmentation_free_arena_is_fragmentation_free_system") is False,
            "arena sem fragmentação não prova sistema sem fragmentação")

    regions = record.get("regions")
    require(isinstance(regions, list) and regions, "regions deve ser lista não vazia")
    ids: set[int] = set()
    ordered: list[tuple[int, int, int]] = []
    physical_fixed_present = False
    token_vazio_present = False

    for region in regions:
        require(isinstance(region, dict), "região inválida")
        region_id = region.get("region_id")
        offset = region.get("offset")
        size = region.get("size")
        alignment = region.get("alignment")
        mobility = region.get("mobility")
        state = region.get("semantic_state")

        require(isinstance(region_id, int) and region_id >= 0, "region_id inválido")
        require(region_id not in ids, f"region_id duplicado: {region_id}")
        ids.add(region_id)
        require(isinstance(offset, int) and offset >= 0, f"offset inválido em {region_id}")
        require(isinstance(size, int) and size >= 0, f"size inválido em {region_id}")
        require(isinstance(alignment, int) and is_power_of_two(alignment),
                f"alignment inválido em {region_id}")
        require(offset % alignment == 0, f"offset desalinhado em {region_id}")
        require(mobility in MOBILITY, f"mobility inválida em {region_id}")
        require(state in REGION_STATES, f"semantic_state inválido em {region_id}")

        if state in {"ABSENT", "EMPTY"}:
            require(size == 0, f"{state} exige size=0 em {region_id}")
        if state == "PRESENT":
            require(size > 0, f"PRESENT exige size>0 em {region_id}")
        if mobility == "PHYSICAL_FIXED":
            physical_fixed_present = True
        if mobility == "TOKEN_VAZIO" or state == "TOKEN_VAZIO":
            token_vazio_present = True
        if size > 0:
            ordered.append((offset, offset + size, region_id))

    ordered.sort()
    for previous, current in zip(ordered, ordered[1:]):
        require(previous[1] <= current[0],
                f"overlap entre regiões {previous[2]} e {current[2]}")

    sources = record.get("sources")
    require(isinstance(sources, list) and sources, "sources deve ser lista não vazia")
    source_keys: set[tuple[str, str, str]] = set()
    for source in sources:
        require(isinstance(source, dict), "source inválida")
        repository = source.get("repository")
        path = source.get("path")
        ref = source.get("ref", "")
        require(isinstance(repository, str) and repository, "repository vazio")
        require(isinstance(path, str) and path, "path vazio")
        require(source.get("evidence_state") in EVIDENCE_STATES, "evidence_state inválido")
        key = (repository, path, ref)
        require(key not in source_keys, f"fonte duplicada: {repository}:{path}@{ref}")
        source_keys.add(key)

    boundary = record.get("claim_boundary")
    require(isinstance(boundary, dict), "claim_boundary ausente")
    limitations = boundary.get("limitations")
    require(isinstance(limitations, list) and limitations, "limitations não pode ser vazio")

    physical_evidence = model.get("physical_space")
    if model.get("base_policy") == "FIXED_PHYSICAL" or physical_fixed_present:
        require(physical_evidence == "VERIFIED_LIMITED",
                "FIXED_PHYSICAL exige physical_space=VERIFIED_LIMITED")
        require(boundary.get("physical_runtime") == "VERIFIED_LIMITED",
                "FIXED_PHYSICAL exige runtime físico verificado")

    if physical_evidence == "TOKEN_VAZIO" or token_vazio_present:
        require(record["claim_allowed"] is False, "TOKEN_VAZIO bloqueia promoção")

    if boundary.get("android_runtime") != "VERIFIED_LIMITED":
        require(model.get("base_policy") != "FIXED_VIRTUAL",
                "FIXED_VIRTUAL Android exige evidência runtime")

    return {
        "validator": "validate_omega_static_layout.v1",
        "record_id": record.get("record_id"),
        "status": "PASS",
        "claim_allowed": False,
        "regions": len(regions),
        "sources": len(sources),
        "mapping_epoch": model["mapping_epoch"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "record",
        nargs="?",
        default="data/control-plane/omega-static-address-relocation.v1.json",
    )
    parser.add_argument("--write-report")
    args = parser.parse_args()

    try:
        record = json.loads(Path(args.record).read_text(encoding="utf-8"))
        report = validate(record)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.write_report:
        target = Path(args.write_report)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
