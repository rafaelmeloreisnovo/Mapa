from __future__ import annotations

import importlib.util
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools/validate_open_work_execution_contract.py"
CONTRACT = ROOT / "data/gaps/open_work_execution_contract.20260808.v1.json"

spec = importlib.util.spec_from_file_location("open_work_validator", VALIDATOR)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_canonical_contract_passes():
    result = module.validate(CONTRACT)
    assert result["state"] == "PASS"
    assert result["tokens"] == 14
    assert result["in_flight_pass_draft"] == 2


def test_no_open_token_is_anonymous():
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    for row in data["items"]:
        assert row["authority_required"].strip()
        assert row["minimal_evidence"].strip()
        assert row["promotion_condition"].strip()
        assert row["falsifier"].strip()
        assert row["next_producer"].strip()


def test_external_and_human_authorities_are_not_internalized():
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    for row in data["items"]:
        if row["authority_state"] in {"OPEN_EXTERNAL", "OPEN_HUMAN"}:
            assert row["execution_state"] != "IN_FLIGHT_PASS_DRAFT"


def test_draft_pass_does_not_mutate_authoritative_open_state():
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    rows = {row["token"]: row for row in data["items"]}
    act = rows["TOKEN_VAZIO_ACT_DR6_CMBONLY_MATERIALIZATION_REPRODUCTION"]
    rd = rows["TOKEN_VAZIO_H0_RD_FULL_BOLTZMANN_REPRODUCTION"]
    assert act["authority_state"] == "OPEN_INTERNAL"
    assert act["execution_state"] == "IN_FLIGHT_PASS_DRAFT"
    assert rd["authority_state"] == "OPEN_MIXED"
    assert rd["execution_state"] == "IN_FLIGHT_PASS_DRAFT"


def test_critical_scientific_dependencies_are_explicit():
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    rows = {row["token"]: row for row in data["items"]}
    impl = rows["TOKEN_VAZIO_RLL_CLASS_CAMB_IMPLEMENTATION"]
    assert impl["dependencies"] == ["TOKEN_VAZIO_RLL_PERTURBATION_CLOSURE_RELATIONS"]
    joint = rows["TOKEN_VAZIO_REAL_BAYES_JOINT_MULTI_PROBE"]
    assert "TOKEN_VAZIO_DESI_DR2_OFFICIAL_JOINT_CROSSBLOCK_REPRODUCTION" in joint["dependencies"]
    assert "TOKEN_VAZIO_DES_Y6_3X2PT_LIKELIHOOD" in joint["dependencies"]
