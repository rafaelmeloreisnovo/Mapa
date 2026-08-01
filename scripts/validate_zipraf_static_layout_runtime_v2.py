#!/usr/bin/env python3
"""Validate the federated ZIPRAF static-layout runtime V2 evidence receipt."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "zipraf-static-layout-runtime.v2"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class ValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate(record: dict[str, Any]) -> dict[str, Any]:
    require(record.get("schema_version") == SCHEMA_VERSION, "schema_version inválida")
    require(record.get("claim_allowed") is False, "claim_allowed deve permanecer false")

    source = record.get("source")
    require(isinstance(source, dict), "source ausente")
    require(source.get("repository") == "rafaelmeloreisnovo/Vectras-VM-Android",
            "repositório-fonte inválido")
    require(source.get("pull_request") == 1075, "PR de origem inválida")
    require(isinstance(source.get("head_sha"), str) and SHA40.fullmatch(source["head_sha"]),
            "head_sha inválido")
    require(isinstance(source.get("merge_sha"), str) and SHA40.fullmatch(source["merge_sha"]),
            "merge_sha inválido")

    invariant = record.get("invariant")
    require(isinstance(invariant, dict), "invariant ausente")
    require(invariant.get("equation") ==
            "ADDRESS=ZIP_PAYLOAD_BASE+REGION_OFFSET+LOCAL_OFFSET",
            "equação ZIPRAF inválida")
    require(invariant.get("base_policy") == "BASE_RELATIVE",
            "ZIPRAF deve permanecer BASE_RELATIVE")
    require(invariant.get("fixed_offset_is_physical") is False,
            "FIXED_OFFSET não é endereço físico")

    identity = record.get("manifest_identity")
    require(isinstance(identity, dict), "manifest_identity ausente")
    require(identity.get("algorithm") == "FNV1A64", "algoritmo de identidade inválido")
    require(identity.get("byte_order") == "LITTLE_ENDIAN_FIELDS", "ordem de bytes inválida")
    require(identity.get("value_hex") == "dc16075f7047df36", "vetor C/Kotlin divergente")
    require(identity.get("c_kotlin_match") is True, "assinaturas C/Kotlin devem coincidir")
    require(identity.get("cryptographic") is False, "FNV-1a não pode ser promovido a criptográfico")

    changes = record.get("runtime_changes")
    require(isinstance(changes, dict), "runtime_changes ausente")
    require(changes.get("whole_payload_map_on_open") is False,
            "mmap integral na abertura deve permanecer removido")
    for key in (
        "bounded_l2_mapping_cache",
        "mapping_reuse",
        "caller_owned_crc_scratch",
        "sha256_direct_bytebuffer",
    ):
        require(changes.get(key) is True, f"mudança obrigatória ausente: {key}")
    require(changes.get("latency_percentiles") == ["p50", "p95", "p99"],
            "percentis obrigatórios inválidos")

    gates = record.get("gates")
    require(isinstance(gates, dict), "gates ausente")
    host = gates.get("host")
    require(isinstance(host, dict), "gate host ausente")
    require(host.get("run_id") == 30712981749, "run host divergente")
    require(host.get("conclusion") == "success", "gate host não passou")
    require(host.get("checks") == 31, "contagem do KAT divergente")
    require(host.get("artifact_id") == 8822466423, "artifact_id divergente")
    require(isinstance(host.get("artifact_sha256"), str) and
            SHA256.fullmatch(host["artifact_sha256"]), "digest do artefato inválido")

    android = gates.get("android")
    require(isinstance(android, dict), "gate Android ausente")
    require(android.get("state") == "BLOCKED_EXTERNAL_BEFORE_COMPILE",
            "estado Android deve refletir bloqueio externo")
    require(android.get("device_runtime") == "TOKEN_VAZIO",
            "runtime físico Android não foi demonstrado")
    require("qemu_rafaelia" in str(android.get("blocker", "")),
            "bloqueio externo não identificado")

    claims = record.get("claims")
    require(isinstance(claims, dict), "claims ausente")
    require(claims.get("host_reference") == "VERIFIED_LIMITED",
            "host deve permanecer VERIFIED_LIMITED")
    require(claims.get("android_compile") == "BLOCKED_EXTERNAL",
            "Android compile não pode ser promovido")
    require(claims.get("android_device") == "TOKEN_VAZIO",
            "Android device não pode ser promovido")
    require(claims.get("fixed_physical") == "REJECTED_BY_POLICY",
            "FIXED_PHYSICAL deve ser rejeitado")
    for key in ("zip64", "real_payload_over_2gib", "independent_reproduction"):
        require(claims.get(key) == "TOKEN_VAZIO", f"{key} deve permanecer TOKEN_VAZIO")

    return {
        "validator": "validate_zipraf_static_layout_runtime_v2",
        "record_id": record.get("record_id"),
        "status": "PASS",
        "claim_allowed": False,
        "host_run_id": host["run_id"],
        "android_state": android["state"],
        "merge_sha": source["merge_sha"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "record",
        nargs="?",
        default="data/evidence/zipraf-static-layout-runtime.v2.json",
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
