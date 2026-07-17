from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_federated_map_v2.py"
spec = importlib.util.spec_from_file_location("federated_map", VALIDATOR)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture() -> dict:
    return json.loads((ROOT / "data" / "federation" / "rafaelia-federated-map-v2.json").read_text())


def test_projection_valid() -> None:
    assert module.validate(fixture()) == []


def test_unmeasured_weight_rejected() -> None:
    data = fixture()
    data["coordinates"][0]["weights"]["runtime"] = 2
    assert module.validate(data)


def test_private_payload_rejected() -> None:
    data = fixture()
    data["private_payload"] = "x"
    assert module.validate(data)


def test_claim_promotion_rejected() -> None:
    data = fixture()
    data["claim_allowed"] = True
    assert module.validate(data)


def test_digest_stable() -> None:
    assert module.digest(fixture()) == module.digest(copy.deepcopy(fixture()))
