#!/usr/bin/env python3
"""Deterministic semantic tensor and parable governance overlay.

This program does not alter model weights, tokenizers, training data, or claims.
It tokenizes supplied content, computes bounded heuristic dimensions, applies
fail-closed decision rules, and emits an auditable receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

TOKEN_RE = re.compile(r"[^\W_]+(?:[-'][^\W_]+)*|\d+(?:[.,]\d+)?|[_]+|[^\w\s]", re.UNICODE)

MARKERS: dict[str, tuple[str, ...]] = {
    "source_provenance": (
        "fonte", "source", "referência", "referencia", "doi", "commit",
        "receipt", "hash", "sha256", "capítulo", "capitulo", "versículo",
        "versiculo", "sutta", "sutra", "registro",
    ),
    "evidence_strength": (
        "evidência", "evidencia", "teste", "dados", "medido", "medida",
        "resultado", "observado", "observada", "receipt", "hash", "pass",
        "fail", "amostra", "telemetria",
    ),
    "falsifiability": (
        "falsificador", "falsificabilidade", "refut", "falha se",
        "teste negativo", "contraprova", "critério de rejeição",
        "criterio de rejeicao", "condição de falha", "condicao de falha",
    ),
    "coherence": (
        "porque", "portanto", "logo", "então", "entao", "se", "quando",
        "invariante", "coerência", "coerencia", "conclusão", "conclusao",
    ),
    "contextual_integrity": (
        "contexto", "escopo", "limite", "classificação", "classificacao",
        "origem", "tradição", "tradicao", "autor", "data", "versão", "versao",
    ),
    "cultural_provenance": (
        "tradição", "tradicao", "fonte primária", "fonte primaria",
        "comunidade", "linhagem", "tradução", "traducao", "contexto cultural",
    ),
    "reproducibility": (
        "comando", "ambiente", "versão", "versao", "sha256", "hash",
        "seed", "fixture", "reproduz", "runtime", "entrada", "saída", "saida",
    ),
    "ethical_safety": (
        "privacidade", "consentimento", "respeito", "não atribuir",
        "nao atribuir", "não generalizar", "nao generalizar", "segurança",
        "seguranca", "ética", "etica", "comunidade específica",
    ),
    "epistemic_humility": (
        "token_vazio", "não sei", "nao sei", "incerto", "incerta",
        "hipótese", "hipotese", "limite", "não comprovado", "nao comprovado",
        "não observado", "nao observado", "fora do escopo",
    ),
}

ABSOLUTE_MARKERS = (
    "sempre", "nunca", "prova definitiva", "certeza absoluta",
    "sem qualquer dúvida", "sem qualquer duvida", "é impossível refutar",
    "e impossivel refutar",
)

CONTRADICTION_PAIRS = (
    ("provado", "hipótese"),
    ("provado", "hipotese"),
    ("definitivo", "token_vazio"),
    ("sem evidência", "comprovado"),
    ("sem evidencia", "comprovado"),
)

FACTUAL_CLASSES = {"FACTUAL", "SCIENTIFIC", "TECHNICAL"}
PARABLE_CLASSES = {"PARABLE", "MODELO_ANALOGICO"}
SPIRITUAL_CLASSES = {"CONFISSAO_ESPIRITUAL"}


class SemanticTensorError(ValueError):
    """Raised when the deterministic contract is invalid."""


def tokenize(text: str) -> list[str]:
    return [token.casefold() for token in TOKEN_RE.findall(text)]


def normalized_entropy(tokens: list[str]) -> float:
    """Return lexical Shannon entropy normalized to [0, 1].

    This value is not a measure of truth, intelligence, spirit, or human worth.
    """
    if len(tokens) <= 1:
        return 0.0
    counts = Counter(tokens)
    total = len(tokens)
    entropy = -sum((n / total) * math.log2(n / total) for n in counts.values())
    maximum = math.log2(total)
    return 0.0 if maximum == 0 else min(1.0, entropy / maximum)


def _marker_score(text_folded: str, markers: tuple[str, ...]) -> float:
    hits = sum(1 for marker in markers if marker in text_folded)
    return min(0.60, hits * 0.15)


def _bool_control(controls: dict[str, Any], name: str) -> float:
    return 1.0 if controls.get(name) is True else 0.0


def _coherence_score(text_folded: str, sentence_count: int) -> float:
    score = _marker_score(text_folded, MARKERS["coherence"])
    if sentence_count >= 2:
        score += 0.15
    if any(marker in text_folded for marker in ("source ->", "fonte ->", "→")):
        score += 0.15
    return min(1.0, score)


def contradiction_penalty(text: str) -> float:
    folded = text.casefold()
    hits = sum(
        1 for left, right in CONTRADICTION_PAIRS
        if left in folded and right in folded
    )
    if any(marker in folded for marker in ABSOLUTE_MARKERS):
        hits += 1
    return min(1.0, hits * 0.35)


def validate_control(control: dict[str, Any]) -> None:
    dimensions = control.get("tensor_dimensions")
    if not isinstance(dimensions, list) or len(dimensions) != 9:
        raise SemanticTensorError("control must declare exactly nine tensor dimensions")
    weights = [item.get("weight") for item in dimensions if isinstance(item, dict)]
    if len(weights) != 9 or any(not isinstance(weight, (int, float)) for weight in weights):
        raise SemanticTensorError("all tensor dimensions require numeric weights")
    if not math.isclose(sum(weights), 1.0, abs_tol=1e-9):
        raise SemanticTensorError("tensor weights must sum to 1.0")
    boundary = control.get("model_boundary", {})
    for field in ("changes_model_weights", "changes_tokenizer", "changes_training_data"):
        if boundary.get(field) is not False:
            raise SemanticTensorError(f"model boundary field {field} must be false")
    if control.get("automatic_promotion") is not False:
        raise SemanticTensorError("automatic_promotion must be false")


def compute_dimensions(record: dict[str, Any]) -> tuple[dict[str, float], float, float]:
    text = str(record.get("text", ""))
    folded = text.casefold()
    controls = record.get("controls") or {}
    if not isinstance(controls, dict):
        raise SemanticTensorError("controls must be an object")

    sentences = max(1, len(re.findall(r"[.!?]+", text)))
    tradition = str(record.get("tradition", "NONE")).upper()
    origin = str(record.get("authorial_origin", "")).upper()
    cultural_not_applicable = (
        tradition in {"NONE", "CROSS_CULTURAL_PATTERN"}
        or origin in {"USER_AUTHORED", "USER_SYNTHESIS"}
    )

    dimensions = {
        "source_provenance": max(
            _marker_score(folded, MARKERS["source_provenance"]),
            _bool_control(controls, "source_verified"),
        ),
        "evidence_strength": max(
            _marker_score(folded, MARKERS["evidence_strength"]),
            _bool_control(controls, "evidence_verified"),
        ),
        "falsifiability": max(
            _marker_score(folded, MARKERS["falsifiability"]),
            _bool_control(controls, "falsifier_defined"),
        ),
        "coherence": max(
            _coherence_score(folded, sentences),
            _bool_control(controls, "coherence_reviewed"),
        ),
        "contextual_integrity": max(
            _marker_score(folded, MARKERS["contextual_integrity"]),
            _bool_control(controls, "context_verified"),
        ),
        "cultural_provenance": max(
            1.0 if cultural_not_applicable else 0.0,
            _marker_score(folded, MARKERS["cultural_provenance"]),
            _bool_control(controls, "cultural_source_verified"),
        ),
        "reproducibility": max(
            _marker_score(folded, MARKERS["reproducibility"]),
            _bool_control(controls, "reproducible"),
        ),
        "ethical_safety": max(
            _marker_score(folded, MARKERS["ethical_safety"]),
            _bool_control(controls, "ethical_reviewed"),
        ),
        "epistemic_humility": max(
            _marker_score(folded, MARKERS["epistemic_humility"]),
            _bool_control(controls, "limits_declared"),
        ),
    }
    tokens = tokenize(text)
    return dimensions, normalized_entropy(tokens), contradiction_penalty(text)


def _unsupported_cultural_attribution(record: dict[str, Any]) -> bool:
    tradition = str(record.get("tradition", "NONE")).upper()
    source_state = str(record.get("source_state", "TOKEN_VAZIO")).upper()
    origin = str(record.get("authorial_origin", "")).upper()
    if tradition in {"NONE", "CROSS_CULTURAL_PATTERN", "RAFAELIA_AUTHORIAL"}:
        return False
    if origin in {"USER_AUTHORED", "USER_SYNTHESIS"}:
        return False
    allowed = {
        "VERIFIED_PRIMARY_SOURCE",
        "VERIFIED_CRITICAL_EDITION",
        "REFERENCE_DECLARED_NOT_VERIFIED",
        "ATTRIBUTION_CONTESTED",
    }
    return source_state not in allowed


def quality_score(
    control: dict[str, Any],
    dimensions: dict[str, float],
    entropy: float,
    contradiction: float,
    unsupported_attribution: bool,
) -> float:
    weights = {
        item["name"]: float(item["weight"])
        for item in control["tensor_dimensions"]
    }
    support = sum(weights[name] * dimensions[name] for name in weights)
    penalties = control["penalties"]
    effective_entropy = entropy * (1.0 - dimensions["coherence"])
    quality = support
    quality *= 1.0 - float(penalties["normalized_token_entropy_factor"]) * effective_entropy
    quality *= 1.0 - float(penalties["contradiction_factor"]) * contradiction
    if unsupported_attribution:
        quality *= 1.0 - float(penalties["unsupported_attribution_factor"])
    return round(max(0.0, min(1.0, quality)), 6)


def decide(
    control: dict[str, Any],
    record: dict[str, Any],
    dimensions: dict[str, float],
    quality: float,
    unsupported_attribution: bool,
) -> tuple[str, list[str]]:
    claim_class = str(record.get("claim_class", "TOKEN_VAZIO")).upper()
    reasons: list[str] = []

    if unsupported_attribution:
        return "BLOCKED_UNSOURCED_CULTURAL_ATTRIBUTION", [
            "named tradition lacks an acceptable source state"
        ]
    if claim_class in SPIRITUAL_CLASSES:
        return "PRESERVED_AS_CONFESSION_NOT_DOMAIN_CLAIM", [
            "spiritual confession is preserved without empirical promotion"
        ]
    if claim_class in PARABLE_CLASSES:
        return "PARABLE_ANALOGY_NO_FACT_PROMOTION", [
            "parable or analogy may guide interpretation but is not empirical evidence"
        ]
    if claim_class in FACTUAL_CLASSES:
        thresholds = control["thresholds"]
        required = (
            ("source_provenance", thresholds["minimum_factual_source"]),
            ("evidence_strength", thresholds["minimum_factual_evidence"]),
            ("falsifiability", thresholds["minimum_factual_falsifiability"]),
        )
        for name, minimum in required:
            if dimensions[name] < float(minimum):
                reasons.append(f"{name} below minimum {minimum}")
        if reasons:
            return "BLOCKED_TOKEN_VAZIO", reasons
    if quality >= float(control["thresholds"]["ready_for_human_review"]):
        return "READY_FOR_HUMAN_REVIEW", [
            "heuristic threshold met; human decision still required"
        ]
    return "TOKEN_VAZIO", [
        "quality threshold not met or claim class remains underspecified"
    ]


def analyze_record(control: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    record_id = str(record.get("id", "")).strip()
    text = str(record.get("text", ""))
    if not record_id:
        raise SemanticTensorError("record id is required")
    if not text.strip():
        raise SemanticTensorError(f"record {record_id}: text is required")

    dimensions, entropy, contradiction = compute_dimensions(record)
    unsupported = _unsupported_cultural_attribution(record)
    quality = quality_score(control, dimensions, entropy, contradiction, unsupported)
    decision, reasons = decide(control, record, dimensions, quality, unsupported)
    tokens = tokenize(text)

    return {
        "id": record_id,
        "claim_class": str(record.get("claim_class", "TOKEN_VAZIO")).upper(),
        "tradition": str(record.get("tradition", "NONE")),
        "source_state": str(record.get("source_state", "TOKEN_VAZIO")),
        "token_count": len(tokens),
        "unique_token_count": len(set(tokens)),
        "token_sha256": hashlib.sha256("\n".join(tokens).encode("utf-8")).hexdigest(),
        "tensor": dimensions,
        "normalized_token_entropy": round(entropy, 6),
        "contradiction_penalty": round(contradiction, 6),
        "unsupported_cultural_attribution": unsupported,
        "quality_score": quality,
        "decision": decision,
        "reasons": reasons,
    }


def build_receipt(control: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    validate_control(control)
    analyses = [analyze_record(control, record) for record in records]
    source_material = json.dumps(records, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return {
        "schema_version": "rafaelia.semantic-tensor-receipt.v1",
        "execution_mode": "DETERMINISTIC_GOVERNANCE_OVERLAY",
        "model_mutation": False,
        "claim_allowed": False,
        "automatic_promotion": False,
        "input_sha256": hashlib.sha256(source_material).hexdigest(),
        "record_count": len(analyses),
        "decision_counts": dict(Counter(item["decision"] for item in analyses)),
        "records": analyses,
        "invariant": "tokenization -> tensor -> entropy -> contradiction -> falsifier -> decision -> receipt",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--control",
        default="data/control-plane/rafaelia-semantic-tensor.v1.json",
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        control = json.loads(Path(args.control).read_text(encoding="utf-8"))
        records = json.loads(Path(args.input).read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise SemanticTensorError("input root must be a list")
        receipt = build_receipt(control, records)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, json.JSONDecodeError, SemanticTensorError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        "PASS: semantic tensor receipt emitted; "
        f"records={receipt['record_count']} model_mutation=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
