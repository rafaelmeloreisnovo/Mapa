from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_architecture_family_registry.py"
REGISTRY = ROOT / "data/ontology/architectures/ARCHITECTURE_FAMILY_REGISTRY_V1.yaml"
INDEX = ROOT / "indices/semantic/ARCHITECTURE_FAMILY_INDEX_V1.yaml"


def test_architecture_family_registry_gate_passes():
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "PASS architecture-family-registry-v1" in result.stdout


def test_registry_preserves_epistemic_boundaries():
    text = REGISTRY.read_text(encoding="utf-8")
    assert "CONCEPT != IMPLEMENTATION != BUILD != EXECUTION != EVIDENCE != CLAIM" in text
    assert "HISTORICAL_ASSISTANT_ASSERTION != PRIMARY_EVIDENCE" in text
    assert "TOKEN_VAZIO != ZERO" in text
    assert "claim_allowed: false" in text


def test_index_routes_only_known_architecture_ids():
    registry = REGISTRY.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    for arch_id in (
        "ARCH-FCEA",
        "ARCH-ZETA",
        "ARCH-V79-1",
        "ARCH-MAYA-LINEAGE",
        "ARCH-HCPM",
        "ARCH-NEXUS",
        "ARCH-EXACORDEX",
    ):
        assert arch_id in registry
        assert arch_id in index
