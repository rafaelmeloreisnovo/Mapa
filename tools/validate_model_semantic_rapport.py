#!/usr/bin/env python3
"""Validate the external rapport boundary around an AI model.

The validator proves only structural coherence of the supplied packet. It does
not inspect a provider model and it never promotes hidden weights, activations,
token IDs or architecture from inference to evidence.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTROL = ROOT / "contracts/model-semantic-rapport.v1.json"
DEFAULT_PACKET = ROOT / "examples/model-semantic-rapport.closed-provider.v1.json"

REQUIRED_INVARIANTS = {
    "semantic_token != tokenizer_token_id",
    "external_semantic_vector != native_model_embedding",
    "tensor != weight",
    "context_conditioning != parameter_training",
    "llm_label != transformer_architecture_proof",
    "LNN requires explicit expansion",
    "proprietary_withheld != measured_local",
    "repository_license != weights_tokenizer_dataset_license",
}

TOKENIZER_DEPENDENT_KINDS = {
    "TOKEN_IDS",
    "EMBEDDING_TABLE",
    "INPUT_EMBEDDINGS",
}

PACKET_FIELDS = {
    "schema_version",
    "rapport_id",
    "created_on",
    "mode",
    "claim_allowed",
    "model_surface",
    "context_effect",
    "instance_sources",
    "nodes",
    "edges",
    "gaps",
    "invariants",
    "F_ok",
    "F_gap",
    "F_next",
}

SURFACE_FIELDS = {
    "surface_id",
    "provider",
    "model_name",
    "model_version",
    "capability_class",
    "architecture_family",
    "architecture_expansion",
    "architecture_evidence_refs",
    "artifact_sha256",
    "tokenizer_id",
    "tokenizer_sha256",
    "execution_mode",
    "internal_access",
    "parameter_update_observed",
    "rights",
}

CONTEXT_FIELDS = {
    "changes_runtime_input",
    "parameter_update_observed",
    "parameter_update_state",
    "persistent_memory_observed",
    "persistent_memory_state",
    "invariant",
}

SOURCE_FIELDS = {"source_id", "kind", "reference", "scope"}
RIGHT_FIELDS = {"unit", "state", "source_refs"}
NODE_FIELDS = {
    "node_id",
    "kind",
    "label",
    "observability",
    "epistemic_state",
    "source_refs",
    "gap_refs",
}
EDGE_FIELDS = {
    "edge_id",
    "source",
    "target",
    "relation",
    "epistemic_state",
    "source_refs",
    "falsifier",
    "next_gate",
}
GAP_FIELDS = {
    "gap_id",
    "gap_class",
    "priority",
    "blocking",
    "reason",
    "affected_nodes",
    "next_probe",
}

PACKET_MODES = {
    "REFERENCE_BOUNDARY",
    "PROVIDER_DECLARATION",
    "LOCAL_INSPECTION",
    "MEASURED_EXECUTION",
}
CAPABILITY_CLASSES = {
    "LLM",
    "LANGUAGE_MODEL",
    "SEQUENCE_MODEL",
    "OTHER",
    "TOKEN_VAZIO",
}
ARCHITECTURE_FAMILIES = {
    "RNN",
    "LSTM",
    "GRU",
    "TRANSFORMER",
    "LIQUID_TIME_CONSTANT",
    "LOGICAL_NEURAL_NETWORK",
    "HYBRID",
    "OTHER",
    "TOKEN_VAZIO",
}
INTERNAL_ACCESS_STATES = {
    "OPEN_LOCAL",
    "PROVIDER_DECLARED",
    "PROPRIETARY_WITHHELD",
    "TOKEN_VAZIO",
}


class RapportError(ValueError):
    """Raised when a model-semantic rapport packet violates its boundary."""


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _unique_strings(values: Any, name: str, errors: list[str]) -> set[str]:
    if not isinstance(values, list) or any(not isinstance(v, str) or not v for v in values):
        errors.append(f"{name}:expected_nonempty_string_array")
        return set()
    unique = set(values)
    if len(unique) != len(values):
        errors.append(f"{name}:duplicates")
    return unique


def _exact_keys(
    value: Any, expected: set[str], name: str, errors: list[str]
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{name}:expected_object")
        return
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"{name}:missing:{','.join(missing)}")
    if extra:
        errors.append(f"{name}:unexpected:{','.join(extra)}")


def _is_iso_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return dt.date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def validate_control(control: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(control, dict):
        raise RapportError("control:expected_object")
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(
        control.get("schema_version")
        == "rafaelia.model-semantic-rapport-control/v1",
        "control:schema_version",
    )
    require(control.get("claim_allowed") is False, "control:claim_allowed")

    execution_modes = _unique_strings(
        control.get("execution_modes"), "control:execution_modes", errors
    )
    update_modes = _unique_strings(
        control.get("parameter_update_modes"),
        "control:parameter_update_modes",
        errors,
    )
    require(update_modes <= execution_modes, "control:update_modes_not_execution_modes")

    observability = _unique_strings(
        control.get("observability_states"),
        "control:observability_states",
        errors,
    )
    epistemic = _unique_strings(
        control.get("epistemic_states"), "control:epistemic_states", errors
    )
    node_kinds = _unique_strings(
        control.get("node_kinds"), "control:node_kinds", errors
    )
    internal_kinds = _unique_strings(
        control.get("internal_node_kinds"),
        "control:internal_node_kinds",
        errors,
    )
    require(internal_kinds <= node_kinds, "control:internal_kind_not_node_kind")
    edge_types = _unique_strings(
        control.get("edge_types"), "control:edge_types", errors
    )
    rights_units = _unique_strings(
        control.get("rights_units"), "control:rights_units", errors
    )
    gap_classes = _unique_strings(
        control.get("gap_classes"), "control:gap_classes", errors
    )

    require(
        rights_units == {"CODE", "WEIGHTS", "TOKENIZER", "DATASET"},
        "control:rights_units_exact_set",
    )
    require("UPDATES_PARAMETER" in edge_types, "control:updates_parameter_edge_missing")
    require(
        "NOT_EQUIVALENT_TO" in edge_types,
        "control:not_equivalent_edge_missing",
    )

    source_ids: set[str] = set()
    source_kinds: dict[str, str] = {}
    for index, source in enumerate(control.get("sources", [])):
        if not isinstance(source, dict):
            errors.append(f"control:source[{index}]:not_object")
            continue
        source_id = source.get("source_id")
        require(
            isinstance(source_id, str) and bool(source_id),
            f"control:source[{index}]:source_id",
        )
        require(source_id not in source_ids, f"control:source_duplicate:{source_id}")
        if isinstance(source_id, str):
            source_ids.add(source_id)
            source_kinds[source_id] = str(source.get("kind", ""))
        path = source.get("path")
        url = source.get("url")
        require(bool(path) ^ bool(url), f"control:source[{index}]:path_xor_url")
        if path:
            require((ROOT / str(path)).is_file(), f"control:source_path_missing:{path}")
        if url:
            require(str(url).startswith("https://"), f"control:source_url:{source_id}")

    acronyms: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(control.get("acronym_registry", [])):
        if not isinstance(item, dict):
            errors.append(f"control:acronym[{index}]:not_object")
            continue
        symbol = item.get("symbol")
        require(
            isinstance(symbol, str) and bool(symbol),
            f"control:acronym[{index}]:symbol",
        )
        require(symbol not in acronyms, f"control:acronym_duplicate:{symbol}")
        if isinstance(symbol, str):
            acronyms[symbol] = item
        expansions = item.get("expansions")
        require(
            isinstance(expansions, list)
            and len(expansions) >= 1
            and all(isinstance(v, str) and v for v in expansions),
            f"control:acronym[{index}]:expansions",
        )
        for ref in item.get("primary_refs", []):
            require(ref in source_ids, f"control:acronym[{index}]:source:{ref}")

    lnn = acronyms.get("LNN", {})
    require(
        lnn.get("resolution") == "AMBIGUOUS_REQUIRES_EXPANSION",
        "control:LNN_must_remain_ambiguous",
    )
    require(
        set(lnn.get("expansions", []))
        == {"LIQUID_TIME_CONSTANT_NETWORK", "LOGICAL_NEURAL_NETWORK"},
        "control:LNN_expansion_set",
    )
    llm = acronyms.get("LLM", {})
    require(
        llm.get("category") == "CAPABILITY_AND_SCALE_CLASS_NOT_ARCHITECTURE_PROOF",
        "control:LLM_not_architecture_proof",
    )

    control_invariants = {
        item.get("rule")
        for item in control.get("invariants", [])
        if isinstance(item, dict)
    }
    require(
        REQUIRED_INVARIANTS <= control_invariants,
        "control:required_invariants_missing",
    )
    for index, item in enumerate(control.get("invariants", [])):
        if not isinstance(item, dict):
            errors.append(f"control:invariant[{index}]:not_object")
            continue
        require(bool(item.get("id")), f"control:invariant[{index}]:id")
        require(bool(item.get("falsifier")), f"control:invariant[{index}]:falsifier")

    if errors:
        raise RapportError(";".join(errors))

    return {
        "execution_modes": execution_modes,
        "update_modes": update_modes,
        "observability": observability,
        "epistemic": epistemic,
        "node_kinds": node_kinds,
        "internal_kinds": internal_kinds,
        "edge_types": edge_types,
        "rights_units": rights_units,
        "gap_classes": gap_classes,
        "source_ids": source_ids,
        "source_kinds": source_kinds,
    }


def validate_rapport(
    control: dict[str, Any], packet: dict[str, Any]
) -> dict[str, Any]:
    allowed = validate_control(control)
    if not isinstance(packet, dict):
        raise RapportError("packet:expected_object")
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    _exact_keys(packet, PACKET_FIELDS, "packet", errors)
    require(
        packet.get("schema_version") == "rafaelia.model-semantic-rapport/v1",
        "packet:schema_version",
    )
    require(packet.get("claim_allowed") is False, "packet:claim_allowed")
    rapport_id = packet.get("rapport_id")
    require(
        isinstance(rapport_id, str) and rapport_id.startswith("MSR-"),
        "packet:rapport_id",
    )
    require(_is_iso_date(packet.get("created_on")), "packet:created_on")
    require(packet.get("mode") in PACKET_MODES, "packet:mode")

    source_ids = set(allowed["source_ids"])
    source_kinds = dict(allowed["source_kinds"])
    instance_sources = packet.get("instance_sources")
    require(isinstance(instance_sources, list), "packet:instance_sources")
    if not isinstance(instance_sources, list):
        instance_sources = []
    for index, source in enumerate(instance_sources):
        if not isinstance(source, dict):
            errors.append(f"packet:source[{index}]:not_object")
            continue
        _exact_keys(source, SOURCE_FIELDS, f"packet:source[{index}]", errors)
        source_id = source.get("source_id")
        require(
            isinstance(source_id, str) and source_id.startswith("SRC-"),
            f"packet:source[{index}]:source_id",
        )
        require(source_id not in source_ids, f"packet:source_duplicate:{source_id}")
        if isinstance(source_id, str):
            source_ids.add(source_id)
            source_kinds[source_id] = str(source.get("kind", ""))
        require(
            isinstance(source.get("kind"), str) and bool(source.get("kind")),
            f"packet:source[{index}]:kind",
        )
        require(bool(source.get("reference")), f"packet:source[{index}]:reference")
        require(bool(source.get("scope")), f"packet:source[{index}]:scope")

    surface = packet.get("model_surface")
    require(isinstance(surface, dict), "packet:model_surface")
    if not isinstance(surface, dict):
        surface = {}
    _exact_keys(surface, SURFACE_FIELDS, "surface", errors)

    require(
        isinstance(surface.get("surface_id"), str)
        and surface.get("surface_id", "").startswith("model:"),
        "surface:surface_id",
    )
    for field in ("provider", "model_name", "model_version", "tokenizer_id"):
        require(
            isinstance(surface.get(field), str) and bool(surface.get(field)),
            f"surface:{field}",
        )
    require(
        surface.get("capability_class") in CAPABILITY_CLASSES,
        "surface:capability_class",
    )
    require(
        surface.get("architecture_family") in ARCHITECTURE_FAMILIES,
        "surface:architecture_family",
    )
    require(
        surface.get("internal_access") in INTERNAL_ACCESS_STATES,
        "surface:internal_access",
    )
    require(
        surface.get("parameter_update_observed") is None
        or type(surface.get("parameter_update_observed")) is bool,
        "surface:parameter_update_observed",
    )

    execution_mode = surface.get("execution_mode")
    require(
        execution_mode in allowed["execution_modes"],
        "surface:execution_mode",
    )
    artifact_sha256 = surface.get("artifact_sha256")
    require(
        artifact_sha256 is None
        or (
            isinstance(artifact_sha256, str)
            and len(artifact_sha256) == 64
            and all(c in "0123456789abcdef" for c in artifact_sha256)
        ),
        "surface:artifact_sha256",
    )
    tokenizer_sha256 = surface.get("tokenizer_sha256")
    require(
        tokenizer_sha256 is None
        or (
            isinstance(tokenizer_sha256, str)
            and len(tokenizer_sha256) == 64
            and all(c in "0123456789abcdef" for c in tokenizer_sha256)
        ),
        "surface:tokenizer_sha256",
    )
    architecture_refs = _unique_strings(
        surface.get("architecture_evidence_refs"),
        "surface:architecture_evidence_refs",
        errors,
    )
    for ref in architecture_refs:
        require(ref in source_ids, f"surface:architecture_source:{ref}")

    architecture = surface.get("architecture_family")
    architecture_expansion = surface.get("architecture_expansion")
    require(
        architecture_expansion is None
        or (isinstance(architecture_expansion, str) and bool(architecture_expansion)),
        "surface:architecture_expansion",
    )
    if architecture == "TOKEN_VAZIO":
        require(
            architecture_expansion is None,
            "surface:unknown_architecture_has_expansion",
        )
    elif architecture in ARCHITECTURE_FAMILIES:
        require(
            isinstance(architecture_expansion, str) and bool(architecture_expansion),
            "surface:known_architecture_without_expansion",
        )
    if architecture not in {None, "TOKEN_VAZIO"}:
        require(
            bool(architecture_refs),
            "surface:architecture_without_evidence",
        )
        require(
            any(
                source_kinds.get(ref)
                in {
                    "PROVIDER_DECLARATION",
                    "LOCAL_ARTIFACT_MANIFEST",
                    "LOCAL_EXECUTION_RECEIPT",
                }
                for ref in architecture_refs
            ),
            "surface:architecture_without_producer_evidence",
        )
    if surface.get("capability_class") == "LLM" and architecture == "TRANSFORMER":
        require(
            bool(architecture_refs),
            "surface:llm_transformer_assumption",
        )
    if architecture in {"LIQUID_TIME_CONSTANT", "LOGICAL_NEURAL_NETWORK"}:
        expected = {
            "LIQUID_TIME_CONSTANT": "LIQUID_TIME_CONSTANT_NETWORK",
            "LOGICAL_NEURAL_NETWORK": "LOGICAL_NEURAL_NETWORK",
        }[architecture]
        require(
            surface.get("architecture_expansion") == expected,
            "surface:ambiguous_architecture_expansion",
        )

    rights_seen: set[str] = set()
    rights_unknown = False
    rights = surface.get("rights")
    require(isinstance(rights, list), "surface:rights")
    if not isinstance(rights, list):
        rights = []
    for index, right in enumerate(rights):
        if not isinstance(right, dict):
            errors.append(f"surface:right[{index}]:not_object")
            continue
        _exact_keys(right, RIGHT_FIELDS, f"surface:right[{index}]", errors)
        unit = right.get("unit")
        require(unit in allowed["rights_units"], f"surface:right[{index}]:unit")
        require(unit not in rights_seen, f"surface:right_duplicate:{unit}")
        if isinstance(unit, str):
            rights_seen.add(unit)
        state = right.get("state")
        require(isinstance(state, str) and bool(state), f"surface:right[{index}]:state")
        if isinstance(state, str) and state.startswith("TOKEN_VAZIO"):
            rights_unknown = True
        right_refs = _unique_strings(
            right.get("source_refs"), f"surface:right[{index}]:source_refs", errors
        )
        for ref in right_refs:
            require(ref in source_ids, f"surface:right[{index}]:source:{ref}")
        if isinstance(state, str) and not state.startswith("TOKEN_VAZIO"):
            require(bool(right_refs), f"surface:right[{index}]:license_source")
            require(
                any(
                    source_kinds.get(ref)
                    in {"AUTHORITATIVE_LICENSE", "PROVIDER_LICENSE"}
                    for ref in right_refs
                ),
                f"surface:right[{index}]:authoritative_license_source",
            )
    require(rights_seen == allowed["rights_units"], "surface:rights_exact_set")

    context_effect = packet.get("context_effect")
    require(isinstance(context_effect, dict), "packet:context_effect")
    if not isinstance(context_effect, dict):
        context_effect = {}
    _exact_keys(context_effect, CONTEXT_FIELDS, "context", errors)
    require(context_effect.get("changes_runtime_input") is True, "context:runtime_input")
    require(
        context_effect.get("parameter_update_observed") is None
        or type(context_effect.get("parameter_update_observed")) is bool,
        "context:parameter_update_observed",
    )
    require(
        isinstance(context_effect.get("parameter_update_state"), str)
        and bool(context_effect.get("parameter_update_state")),
        "context:parameter_update_state",
    )
    require(
        context_effect.get("persistent_memory_observed") is None
        or type(context_effect.get("persistent_memory_observed")) is bool,
        "context:persistent_memory_observed",
    )
    require(
        isinstance(context_effect.get("persistent_memory_state"), str)
        and bool(context_effect.get("persistent_memory_state")),
        "context:persistent_memory_state",
    )
    require(
        isinstance(context_effect.get("invariant"), str)
        and bool(context_effect.get("invariant")),
        "context:invariant",
    )
    if context_effect.get("parameter_update_observed") is None:
        require(
            str(context_effect.get("parameter_update_state", "")).startswith(
                "TOKEN_VAZIO"
            ),
            "context:unknown_parameter_update_without_token_vazio",
        )
    if context_effect.get("persistent_memory_observed") is None:
        require(
            str(context_effect.get("persistent_memory_state", "")).startswith(
                "TOKEN_VAZIO"
            ),
            "context:unknown_persistent_memory_without_token_vazio",
        )

    gaps = packet.get("gaps")
    require(isinstance(gaps, list), "packet:gaps")
    if not isinstance(gaps, list):
        gaps = []
    gap_ids: set[str] = set()
    for index, gap in enumerate(gaps):
        if not isinstance(gap, dict):
            errors.append(f"gap[{index}]:not_object")
            continue
        _exact_keys(gap, GAP_FIELDS, f"gap[{index}]", errors)
        gap_id = gap.get("gap_id")
        require(
            isinstance(gap_id, str) and gap_id.startswith("TV-"),
            f"gap[{index}]:gap_id",
        )
        require(gap_id not in gap_ids, f"gap:duplicate:{gap_id}")
        if isinstance(gap_id, str):
            gap_ids.add(gap_id)
        require(gap.get("gap_class") in allowed["gap_classes"], f"gap[{index}]:class")
        require(gap.get("priority") in {"P0", "P1", "P2", "P3", "P4"}, f"gap[{index}]:priority")
        require(type(gap.get("blocking")) is bool, f"gap[{index}]:blocking")
        require(bool(gap.get("reason")), f"gap[{index}]:reason")
        require(bool(gap.get("next_probe")), f"gap[{index}]:next_probe")
        affected_nodes = _unique_strings(
            gap.get("affected_nodes"), f"gap[{index}]:affected_nodes", errors
        )
        require(bool(affected_nodes), f"gap[{index}]:affected_nodes_empty")

    nodes = packet.get("nodes")
    require(isinstance(nodes, list) and bool(nodes), "packet:nodes")
    if not isinstance(nodes, list):
        nodes = []
    node_ids: set[str] = set()
    node_by_id: dict[str, dict[str, Any]] = {}
    closed_internals = (
        surface.get("internal_access") in {"PROPRIETARY_WITHHELD", "TOKEN_VAZIO"}
        or artifact_sha256 is None
    )
    tokenizer_unknown = str(surface.get("tokenizer_id", "")).startswith("TOKEN_VAZIO")

    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"node[{index}]:not_object")
            continue
        _exact_keys(node, NODE_FIELDS, f"node[{index}]", errors)
        node_id = node.get("node_id")
        require(
            isinstance(node_id, str) and node_id.startswith("N-"),
            f"node[{index}]:node_id",
        )
        require(node_id not in node_ids, f"node:duplicate:{node_id}")
        if isinstance(node_id, str):
            node_ids.add(node_id)
            node_by_id[node_id] = node
        kind = node.get("kind")
        require(kind in allowed["node_kinds"], f"node[{index}]:kind")
        require(
            isinstance(node.get("label"), str) and bool(node.get("label")),
            f"node[{index}]:label",
        )
        observability = node.get("observability")
        epistemic = node.get("epistemic_state")
        require(observability in allowed["observability"], f"node[{index}]:observability")
        require(epistemic in allowed["epistemic"], f"node[{index}]:epistemic")
        node_source_refs = _unique_strings(
            node.get("source_refs"), f"node[{index}]:source_refs", errors
        )
        node_gap_refs = _unique_strings(
            node.get("gap_refs"), f"node[{index}]:gap_refs", errors
        )
        for ref in node_source_refs:
            require(ref in source_ids, f"node[{index}]:source:{ref}")
        for ref in node_gap_refs:
            require(ref in gap_ids, f"node[{index}]:gap:{ref}")

        if closed_internals and kind in allowed["internal_kinds"]:
            require(
                observability
                in {"PROPRIETARY_WITHHELD", "TOKEN_VAZIO", "PROVIDER_DECLARED"},
                f"node[{index}]:closed_internal_promoted",
            )
            require(epistemic != "MEASURED_LOCAL", f"node[{index}]:hidden_measured")
        if kind in allowed["internal_kinds"] and (
            observability == "LOCAL_ARTIFACT_INSPECTED"
            or epistemic == "MEASURED_LOCAL"
        ):
            require(
                surface.get("internal_access") == "OPEN_LOCAL",
                f"node[{index}]:local_internal_without_open_access",
            )
            require(
                artifact_sha256 is not None,
                f"node[{index}]:local_internal_without_artifact_hash",
            )
            require(
                any(
                    source_kinds.get(ref)
                    in {"LOCAL_ARTIFACT_MANIFEST", "LOCAL_EXECUTION_RECEIPT"}
                    for ref in node_source_refs
                ),
                f"node[{index}]:local_internal_without_receipt",
            )
        if tokenizer_unknown and kind in TOKENIZER_DEPENDENT_KINDS:
            require(
                observability not in {"DIRECT_OBSERVED", "LOCAL_ARTIFACT_INSPECTED"},
                f"node[{index}]:tokenizer_dependent_promoted",
            )

    for index, gap in enumerate(gaps):
        if not isinstance(gap, dict):
            continue
        affected_nodes = gap.get("affected_nodes")
        if not isinstance(affected_nodes, list):
            continue
        for ref in affected_nodes:
            require(ref in node_ids, f"gap[{index}]:affected_node:{ref}")

    edges = packet.get("edges")
    require(isinstance(edges, list) and bool(edges), "packet:edges")
    if not isinstance(edges, list):
        edges = []
    edge_ids: set[str] = set()
    parameter_update_edges = 0
    has_semantic_non_equivalence = False
    has_context_non_weight_proof = False

    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"edge[{index}]:not_object")
            continue
        _exact_keys(edge, EDGE_FIELDS, f"edge[{index}]", errors)
        edge_id = edge.get("edge_id")
        require(
            isinstance(edge_id, str) and edge_id.startswith("E-"),
            f"edge[{index}]:edge_id",
        )
        require(edge_id not in edge_ids, f"edge:duplicate:{edge_id}")
        if isinstance(edge_id, str):
            edge_ids.add(edge_id)
        source = edge.get("source")
        target = edge.get("target")
        require(source in node_ids, f"edge[{index}]:source:{source}")
        require(target in node_ids, f"edge[{index}]:target:{target}")
        require(source != target, f"edge[{index}]:self_loop")
        relation = edge.get("relation")
        require(relation in allowed["edge_types"], f"edge[{index}]:relation")
        require(edge.get("epistemic_state") in allowed["epistemic"], f"edge[{index}]:epistemic")
        require(bool(edge.get("falsifier")), f"edge[{index}]:falsifier")
        require(bool(edge.get("next_gate")), f"edge[{index}]:next_gate")
        edge_source_refs = _unique_strings(
            edge.get("source_refs"), f"edge[{index}]:source_refs", errors
        )
        for ref in edge_source_refs:
            require(ref in source_ids, f"edge[{index}]:source_ref:{ref}")
        if edge.get("epistemic_state") not in {"TOKEN_VAZIO", "INVALIDATED"}:
            require(bool(edge_source_refs), f"edge[{index}]:evidence_source_missing")

        source_kind = node_by_id.get(str(source), {}).get("kind")
        target_kind = node_by_id.get(str(target), {}).get("kind")
        if relation == "UPDATES_PARAMETER":
            parameter_update_edges += 1
            require(
                execution_mode in allowed["update_modes"],
                f"edge[{index}]:parameter_update_mode",
            )
            require(
                surface.get("parameter_update_observed") is True,
                f"edge[{index}]:parameter_update_not_observed",
            )
            require(
                context_effect.get("parameter_update_observed") is True,
                f"edge[{index}]:context_parameter_update_not_observed",
            )
            require(
                edge.get("epistemic_state")
                in {"DOCUMENTED", "MEASURED_LOCAL", "REPRODUCED"},
                f"edge[{index}]:parameter_update_epistemic_state",
            )
            require(bool(edge_source_refs), f"edge[{index}]:parameter_update_receipt")
            require(
                any(
                    source_kinds.get(ref)
                    in {"LOCAL_EXECUTION_RECEIPT", "PROVIDER_EXECUTION_RECEIPT"}
                    for ref in edge_source_refs
                ),
                f"edge[{index}]:parameter_update_execution_receipt",
            )
            require(target_kind == "MODEL_PARAMETERS", f"edge[{index}]:parameter_target")

        if (
            relation == "NOT_EQUIVALENT_TO"
            and source_kind in {"EMBEDDING_TABLE", "INPUT_EMBEDDINGS", "HIDDEN_ACTIVATIONS"}
            and target_kind == "EXTERNAL_SEMANTIC_MAP"
        ):
            has_semantic_non_equivalence = True
        if (
            relation == "DOES_NOT_ESTABLISH"
            and source_kind == "CONTEXT_WINDOW"
            and target_kind == "MODEL_PARAMETERS"
        ):
            has_context_non_weight_proof = True

    require(
        context_effect.get("parameter_update_observed")
        == surface.get("parameter_update_observed"),
        "context:parameter_update_state_mismatch",
    )
    if surface.get("parameter_update_observed") is True:
        require(parameter_update_edges > 0, "context:update_observed_without_edge")
        require(
            not str(context_effect.get("parameter_update_state", "")).startswith(
                "TOKEN_VAZIO"
            ),
            "context:observed_update_still_token_vazio",
        )
    if execution_mode not in allowed["update_modes"]:
        require(parameter_update_edges == 0, "context:update_edge_in_non_update_mode")
        require(
            surface.get("parameter_update_observed") is not True,
            "context:update_observed_in_non_update_mode",
        )

    require(has_semantic_non_equivalence, "packet:semantic_embedding_boundary_missing")
    require(
        has_context_non_weight_proof or parameter_update_edges > 0,
        "packet:context_weight_boundary_missing",
    )

    if tokenizer_unknown:
        require("TV-ACCESS-MSR-TOKENIZER" in gap_ids, "packet:tokenizer_gap_missing")
    if closed_internals:
        require("TV-ACCESS-MSR-WEIGHTS" in gap_ids, "packet:weights_gap_missing")
        require("TV-ACCESS-MSR-ACTIVATIONS" in gap_ids, "packet:activations_gap_missing")
    if architecture == "TOKEN_VAZIO":
        require("TV-DEF-MSR-ARCHITECTURE" in gap_ids, "packet:architecture_gap_missing")
    if rights_unknown:
        require("TV-PROVENANCE-MSR-RIGHTS" in gap_ids, "packet:rights_gap_missing")

    invariants = _unique_strings(
        packet.get("invariants"), "packet:invariants", errors
    )
    require(REQUIRED_INVARIANTS <= invariants, "packet:required_invariants_missing")
    for field in ("F_ok", "F_gap", "F_next"):
        values = _unique_strings(packet.get(field), f"packet:{field}", errors)
        if field == "F_next":
            require(bool(values), "packet:F_next")
    require(
        packet.get("claim_allowed") is False,
        "packet:claim_gate_changed_during_validation",
    )

    if errors:
        raise RapportError(";".join(errors))

    return {
        "schema_version": "rafaelia.model-semantic-rapport-validation/v1",
        "status": "PASS",
        "rapport_id": packet.get("rapport_id"),
        "control_sha256": canonical_sha256(control),
        "packet_sha256": canonical_sha256(packet),
        "node_count": len(node_ids),
        "edge_count": len(edge_ids),
        "gap_count": len(gap_ids),
        "blocking_gap_count": sum(gap.get("blocking") is True for gap in gaps),
        "execution_mode": execution_mode,
        "internal_access": surface.get("internal_access"),
        "parameter_update_observed": surface.get("parameter_update_observed"),
        "model_internal_claim_allowed": False,
        "claim_allowed": False,
        "invariant": "coherent external rapport does not reveal or modify proprietary model internals",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--control", type=Path, default=DEFAULT_CONTROL)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        control = json.loads(args.control.read_text(encoding="utf-8"))
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        report = validate_rapport(control, packet)
    except (OSError, json.JSONDecodeError, RapportError) as exc:
        report = {
            "schema_version": "rafaelia.model-semantic-rapport-validation/v1",
            "status": "FAIL",
            "reason": str(exc),
            "model_internal_claim_allowed": False,
            "claim_allowed": False,
        }

    output = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    sys.stdout.write(output)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
