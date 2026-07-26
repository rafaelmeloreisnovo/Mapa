from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_memory_cohesion_registry import validate_registry


REGISTRY = Path("indices/MEMORY_COHESION_REGISTRY.v1.jsonl")


def test_registry_passes() -> None:
    assert validate_registry(REGISTRY) == []


def test_claim_cannot_be_promoted(tmp_path: Path) -> None:
    record = json.loads(REGISTRY.read_text(encoding="utf-8").splitlines()[0])
    record["claim_allowed"] = True
    candidate = tmp_path / "invalid.jsonl"
    candidate.write_text(json.dumps(record) + "\n", encoding="utf-8")
    assert any("claim_allowed" in error for error in validate_registry(candidate))


def test_mixed_producer_pins_are_rejected(tmp_path: Path) -> None:
    lines = REGISTRY.read_text(encoding="utf-8").splitlines()
    first = json.loads(lines[0])
    second = json.loads(lines[1])
    second["producer_ref"] = "0" * 40
    candidate = tmp_path / "mixed.jsonl"
    candidate.write_text(json.dumps(first) + "\n" + json.dumps(second) + "\n", encoding="utf-8")
    assert any("disagree" in error for error in validate_registry(candidate))


def test_authority_mismatch_is_rejected(tmp_path: Path) -> None:
    record = json.loads(REGISTRY.read_text(encoding="utf-8").splitlines()[0])
    record["authority"]["research_memory"] = "other/repository"
    candidate = tmp_path / "authority.jsonl"
    candidate.write_text(json.dumps(record) + "\n", encoding="utf-8")
    assert any("authority mismatch" in error for error in validate_registry(candidate))
