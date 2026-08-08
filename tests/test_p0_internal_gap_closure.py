from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_p0_internal_gap_validator_passes():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/validate_p0_internal_gap_closure.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["state"] == "PASS"
    assert payload["claim_allowed"] is False
    assert len(payload["validated_gaps"]) == 5


def test_geometry_keeps_exact_selection_unknown():
    doc = json.loads((ROOT / "data/geometry/piramide_triedrica_dupla_candidates.v1.json").read_text(encoding="utf-8"))
    assert doc["selection_state"].startswith("TOKEN_VAZIO_TYPED")
    assert doc["canonical_test_fixture_is_authorial_selection"] is False
    assert doc["fixtures"][2]["id"] == "G3"
    assert doc["fixtures"][2]["state"].startswith("TOKEN_VAZIO_TYPED")


def test_poincare_formula_join_fails_closed_without_exact_formula_bytes():
    doc = json.loads((ROOT / "data/provenance/poincare_formula_provenance.v1.json").read_text(encoding="utf-8"))
    assert doc["formula_artifact_manifest"]["formulas_json_materialized_in_repo_or_release"] is False
    assert doc["mapping_state"]["FORM_id"].startswith("TOKEN_VAZIO_TYPED")
    assert len(doc["raw_blocks"]) == 64


def test_corpus_does_not_overclaim_global_drive_coverage():
    doc = json.loads((ROOT / "data/corpus/corpus_manifest_p0.v1.json").read_text(encoding="utf-8"))
    assert doc["global_drive_complete_claim"] is False
    assert doc["omega7_audit"]["files_observed"] - doc["omega7_audit"]["files_with_hash"] == 1
    assert doc["residual_classification"]["anonymous_gap_count_for_listed_p0_sources"] == 0
