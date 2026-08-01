from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "semantic_incremental_runtime_receipt.py"
spec = importlib.util.spec_from_file_location("semantic_runtime", MODULE_PATH)
assert spec and spec.loader
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


def test_incremental_matches_full_scan(tmp_path: Path) -> None:
    root = tmp_path / "corpus"
    root.mkdir()
    (root / "a.txt").write_text("alpha\n", encoding="utf-8")
    (root / "b.json").write_text('{"b": 2}\n', encoding="utf-8")

    baseline = runtime.scan(root)
    inc, changed, reused = runtime.incremental(baseline, root)
    assert inc == baseline
    assert changed == []
    assert sorted(reused) == ["a.txt", "b.json"]

    (root / "a.txt").write_text("alpha-2\n", encoding="utf-8")
    inc2, changed2, _ = runtime.incremental(baseline, root)
    assert inc2 == runtime.scan(root)
    assert "a.txt" in changed2


def test_incremental_records_deletion(tmp_path: Path) -> None:
    root = tmp_path / "corpus"
    root.mkdir()
    target = root / "gone.txt"
    target.write_text("x", encoding="utf-8")
    baseline = runtime.scan(root)
    target.unlink()

    inc, changed, _ = runtime.incremental(baseline, root)
    assert inc == {}
    assert changed == ["DELETE:gone.txt"]
