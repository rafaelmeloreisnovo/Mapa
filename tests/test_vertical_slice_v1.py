import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/run_vertical_slice_v1.py"

spec = importlib.util.spec_from_file_location("vertical_slice", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_registry_is_fail_closed_and_has_falsifiers():
    registry = module.load_registry(ROOT)
    assert registry["claim_allowed"] is False
    assert len(registry["sources"]) == 9
    assert len(registry["claims"]) == 3
    assert all(claim["falsifier"] for claim in registry["claims"])


def test_expected_apk_contract_has_four_abis_and_two_libraries():
    registry = module.load_registry(ROOT)
    entries = registry["expected"]["apk_entries"]
    assert len(entries) == 8
    for abi in ("arm64-v8a", "armeabi-v7a", "x86", "x86_64"):
        assert f"lib/{abi}/libtermux.so" in entries
        assert f"lib/{abi}/libtermux-bootstrap.so" in entries


def test_expected_export_root_is_exact_and_bounded():
    registry = module.load_registry(ROOT)
    assert sorted(registry["expected"]["chat_export_root_entries"]) == sorted(
        [
            "chat.html",
            "conversations.json",
            "message_feedback.json",
            "shared_conversations.json",
            "user.json",
        ]
    )


def test_record_schema_remains_closed():
    schema = json.loads(
        (ROOT / "schemas/operational-record.v1.schema.json").read_text(encoding="utf-8")
    )
    assert schema["properties"]["claim_allowed"]["const"] is False
    assert "falsifier" in schema["required"]
    assert "next_verifiable_step" in schema["required"]
