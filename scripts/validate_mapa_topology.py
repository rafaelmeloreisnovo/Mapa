#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Valida a topologia estrutural do repositório Mapa.

Características:
- apenas biblioteca padrão;
- lê JSON canônico compatível com YAML 1.2;
- recalcula hash BLAKE2b-256;
- detecta referências ausentes, auto-dependências e ciclos;
- deriva camadas topológicas e métricas;
- verifica coerência FATO/LACUNA e presença de arquivos obrigatórios;
- produz relatório JSON determinístico.

Uso:
    python3 scripts/validate_mapa_topology.py
    python3 scripts/validate_mapa_topology.py --write-report indices/RELATORIO_TOPOLOGIA.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
ALLOWED_STATES = {"active", "planned"}
ALLOWED_MARKS = {"FATO", "LACUNA"}
HEADER_TOKEN = "PRIMEIRA-LINHA"


def parse_document(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    header = lines[0] if lines else ""
    start = raw.find("{")
    if start < 0:
        raise ValueError("documento não contém objeto JSON")
    try:
        data = json.loads(raw[start:])
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON/YAML canônico inválido: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("raiz do documento deve ser objeto")
    return data, header


def canonical_digest(data: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(data, ensure_ascii=False))
    integrity = clone.setdefault("integrity", {})
    integrity["digest"] = ""
    payload = json.dumps(
        clone,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.blake2b(payload, digest_size=32).hexdigest()


def derive_topology(nodes: list[dict[str, Any]]) -> tuple[list[str], dict[str, int], dict[str, list[str]], list[str]]:
    node_ids = {node["id"] for node in nodes}
    indegree = {node["id"]: 0 for node in nodes}
    outgoing: dict[str, list[str]] = defaultdict(list)

    for node in nodes:
        for dependency in node.get("depends_on", []):
            if dependency in node_ids:
                indegree[node["id"]] += 1
                outgoing[dependency].append(node["id"])

    queue = deque(sorted(node_id for node_id, degree in indegree.items() if degree == 0))
    order: list[str] = []
    levels: dict[str, int] = {node_id: 0 for node_id in queue}

    while queue:
        current = queue.popleft()
        order.append(current)
        for target in sorted(outgoing[current]):
            levels[target] = max(levels.get(target, 0), levels[current] + 1)
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)

    cyclic = sorted(node_id for node_id, degree in indegree.items() if degree > 0)
    for values in outgoing.values():
        values.sort()
    return order, levels, dict(outgoing), cyclic


def build_layers(levels: dict[str, int]) -> dict[str, list[str]]:
    layers: dict[int, list[str]] = defaultdict(list)
    for node_id, level in levels.items():
        layers[level].append(node_id)
    return {str(level): sorted(node_ids) for level, node_ids in sorted(layers.items())}


def validate_graph(data: dict[str, Any], repo_root: Path, header: str) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if HEADER_TOKEN not in header:
        errors.append("primeira linha física não contém o selo PRIMEIRA-LINHA")

    if data.get("schema") != "mapa_topology_v2":
        errors.append("schema deve ser mapa_topology_v2")

    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        errors.append("nodes deve ser lista não vazia")
        nodes = []

    seen: set[str] = set()
    node_ids: set[str] = set()
    normalized_nodes: list[dict[str, Any]] = []

    for index, node in enumerate(nodes):
        prefix = f"nodes[{index}]"
        if not isinstance(node, dict):
            errors.append(f"{prefix}: nó deve ser objeto")
            continue

        node_id = node.get("id")
        if not isinstance(node_id, str) or not ID_PATTERN.fullmatch(node_id):
            errors.append(f"{prefix}: id inválido: {node_id!r}")
            continue
        if node_id in seen:
            errors.append(f"{prefix}: id duplicado: {node_id}")
        seen.add(node_id)
        node_ids.add(node_id)
        normalized_nodes.append(node)

        state = node.get("state")
        mark = node.get("epistemic_mark")
        if state not in ALLOWED_STATES:
            errors.append(f"{node_id}: state inválido: {state!r}")
        if mark not in ALLOWED_MARKS:
            errors.append(f"{node_id}: epistemic_mark inválida: {mark!r}")
        if state == "active" and mark != "FATO":
            errors.append(f"{node_id}: active exige epistemic_mark=FATO")
        if state == "planned" and mark != "LACUNA":
            errors.append(f"{node_id}: planned exige epistemic_mark=LACUNA")

        criticality = node.get("criticality")
        if not isinstance(criticality, (int, float)) or isinstance(criticality, bool) or not 0 <= criticality <= 1:
            errors.append(f"{node_id}: criticality deve estar entre 0 e 1")

        path_value = node.get("path")
        if not isinstance(path_value, str) or not path_value:
            errors.append(f"{node_id}: path obrigatório")
        else:
            path = Path(path_value)
            if path.is_absolute() or ".." in path.parts:
                errors.append(f"{node_id}: path deve ser relativo e não escapar do repositório")
            required = node.get("required_file")
            if not isinstance(required, bool):
                errors.append(f"{node_id}: required_file deve ser booleano")
            elif required and not (repo_root / path).is_file():
                errors.append(f"{node_id}: arquivo obrigatório ausente: {path_value}")
            elif state == "planned" and (repo_root / path).is_file():
                warnings.append(f"{node_id}: arquivo planejado já existe; revisar promoção para active")

        dependencies = node.get("depends_on")
        if not isinstance(dependencies, list) or any(not isinstance(item, str) for item in dependencies):
            errors.append(f"{node_id}: depends_on deve ser lista de ids")
            continue
        if len(dependencies) != len(set(dependencies)):
            errors.append(f"{node_id}: dependências duplicadas")
        if node_id in dependencies:
            errors.append(f"{node_id}: auto-dependência")

    for node in normalized_nodes:
        node_id = node["id"]
        for dependency in node.get("depends_on", []):
            if dependency not in node_ids:
                errors.append(f"{node_id}: dependência inexistente: {dependency}")

    root = data.get("governance", {}).get("root_node")
    if root not in node_ids:
        errors.append(f"root_node inexistente: {root!r}")
    else:
        root_node = next(node for node in normalized_nodes if node["id"] == root)
        if root_node.get("depends_on"):
            errors.append(f"{root}: nó raiz não pode depender de outro nó")

    orphan_ids = sorted(
        node["id"]
        for node in normalized_nodes
        if node["id"] != root and not node.get("depends_on")
    )
    if orphan_ids:
        errors.append(f"nós órfãos: {orphan_ids}")

    order, levels, outgoing, cyclic = derive_topology(normalized_nodes)
    if cyclic:
        errors.append(f"ciclo detectado envolvendo: {cyclic}")

    edge_count = sum(len(node.get("depends_on", [])) for node in normalized_nodes)
    active_count = sum(node.get("state") == "active" for node in normalized_nodes)
    planned_count = sum(node.get("state") == "planned" for node in normalized_nodes)
    max_depth = max(levels.values(), default=0)

    derived_metrics = {
        "node_count": len(normalized_nodes),
        "edge_count": edge_count,
        "active_count": active_count,
        "planned_count": planned_count,
        "orphan_count": len(orphan_ids),
        "cycle_count": 1 if cyclic else 0,
        "max_depth": max_depth,
        "critical_path_nodes": max_depth + 1 if normalized_nodes else 0,
        "topological_layers": build_layers(levels),
    }

    declared_metrics = data.get("declared_metrics")
    if declared_metrics != derived_metrics:
        errors.append("declared_metrics diverge das métricas derivadas")

    expected_digest = data.get("integrity", {}).get("digest")
    calculated_digest = canonical_digest(data)
    if expected_digest != calculated_digest:
        errors.append(
            "digest BLAKE2b-256 divergente: "
            f"declarado={expected_digest!r} calculado={calculated_digest}"
        )

    planned_nodes = sorted(
        node["id"] for node in normalized_nodes if node.get("state") == "planned"
    )
    critical_nodes = sorted(
        node["id"]
        for node in normalized_nodes
        if isinstance(node.get("criticality"), (int, float)) and node["criticality"] >= 0.98
    )

    return {
        "schema": "mapa_topology_validation_v1",
        "source_schema": data.get("schema"),
        "source_version": data.get("schema_version"),
        "source_generated_at": data.get("generated_at"),
        "ok": not errors,
        "errors": sorted(errors),
        "warnings": sorted(warnings),
        "integrity": {
            "algorithm": "blake2b-256",
            "declared": expected_digest,
            "calculated": calculated_digest,
            "match": expected_digest == calculated_digest,
        },
        "derived_metrics": derived_metrics,
        "topological_order": order,
        "critical_nodes": critical_nodes,
        "planned_nodes": planned_nodes,
        "derived_dependents": {key: value for key, value in sorted(outgoing.items())},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Valida o DAG estrutural do Mapa")
    parser.add_argument(
        "--graph",
        default="indices/GRAFO_DEPENDENCIAS_MAPA.yaml",
        help="caminho relativo ao repositório",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="raiz do repositório; padrão: pai de scripts/",
    )
    parser.add_argument(
        "--write-report",
        default=None,
        help="grava o relatório JSON no caminho informado",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    graph_path = (repo_root / args.graph).resolve()

    try:
        data, header = parse_document(graph_path)
        report = validate_graph(data, repo_root, header)
    except (OSError, ValueError) as exc:
        report = {
            "schema": "mapa_topology_validation_v1",
            "ok": False,
            "errors": [str(exc)],
            "warnings": [],
        }

    output = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    sys.stdout.write(output)

    if args.write_report:
        target = (repo_root / args.write_report).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")

    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
