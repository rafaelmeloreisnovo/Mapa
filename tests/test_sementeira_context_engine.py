from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sementeira_context_engine.py"
SPEC = importlib.util.spec_from_file_location("sementeira_engine", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SementeiraEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_manifest(self, files: dict[str, str]) -> Path:
        sources = []
        for index, (name, text) in enumerate(files.items(), start=1):
            path = self.root / name
            path.write_text(text, encoding="utf-8")
            raw = path.read_bytes()
            sources.append({
                "source_id": f"src-{index}",
                "conversation_export_title": path.stem,
                "path_hint": name,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
                "lines": len(text.splitlines()),
            })
        manifest = {"schema": "sementeira.source-manifest/v1", "source_count": len(sources), "sources": sources}
        manifest_path = self.root / "manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        return manifest_path

    def test_token_vazio_is_not_zero(self) -> None:
        manifest = self.write_manifest({"a.txt": "TOKEN_VAZIO: não sabemos ainda o valor."})
        report = MODULE.run_engine(manifest, self.root)
        self.assertEqual(report["statistics"]["gap_counts"]["TOKEN_VAZIO"], 1)
        self.assertFalse(report["claim_allowed"])

    def test_hypothesis_without_falsifier_emits_tv_test(self) -> None:
        manifest = self.write_manifest({"a.txt": "Hipótese: o padrão pode aumentar a coerência."})
        report = MODULE.run_engine(manifest, self.root)
        event = report["events"][0]
        self.assertEqual(event["plane"], "HYPOTHESIS_CANDIDATE")
        self.assertTrue(any(gap["class"] == "TV-TEST" for gap in event["token_vazio"]))

    def test_hypothesis_with_falsifier_does_not_emit_tv_test(self) -> None:
        manifest = self.write_manifest({"a.txt": "Hipótese: o padrão aumenta a coerência. Falsificador: rejeitar se o teste não superar o baseline."})
        report = MODULE.run_engine(manifest, self.root)
        event = report["events"][0]
        self.assertTrue(event["falsifier_present"])
        self.assertFalse(any(gap["class"] == "TV-TEST" for gap in event["token_vazio"]))

    def test_antiderivative_roundtrip_uses_source_coordinates_and_hash(self) -> None:
        manifest = self.write_manifest({"a.txt": "Origem preservada.\nHash preservado.\n"})
        report = MODULE.run_engine(manifest, self.root)
        self.assertEqual(report["events"][0]["antiderivative"]["roundtrip_state"], "PASS_SOURCE_COORDINATE_HASH")

    def test_source_hash_mismatch_blocks(self) -> None:
        manifest = self.write_manifest({"a.txt": "conteúdo"})
        payload = json.loads(manifest.read_text())
        payload["sources"][0]["sha256"] = "0" * 64
        manifest.write_text(json.dumps(payload))
        report = MODULE.run_engine(manifest, self.root)
        self.assertGreater(report["blocking_findings"], 0)

    def test_derivative_is_not_causality(self) -> None:
        sig = MODULE.derivative_signature(["origem", "ponte", "teste", "resultado"])
        self.assertIn("not causal proof", sig["interpretation"])

    def test_correlation_relations_never_claim_causality(self) -> None:
        manifest = self.write_manifest({
            "a.txt": "origem prova coerência semântica",
            "b.txt": "origem prova coerência matemática",
        })
        report = MODULE.run_engine(manifest, self.root)
        self.assertTrue(report["relations"])
        self.assertTrue(all(not relation["causality_claimed"] for relation in report["relations"]))
        self.assertTrue(all(not relation["claim_allowed"] for relation in report["relations"]))

    def test_metric_without_unit_emits_boundary_gap(self) -> None:
        manifest = self.write_manifest({"a.txt": "Definir índice de estabilidade e margem estatística."})
        report = MODULE.run_engine(manifest, self.root)
        event = report["events"][0]
        self.assertEqual(event["plane"], "METRIC_CANDIDATE")
        self.assertTrue(any(gap["class"] == "TV-BOUNDARY" for gap in event["token_vazio"]))

    def test_metric_with_unit_does_not_emit_boundary_gap(self) -> None:
        manifest = self.write_manifest({"a.txt": "Definir métrica de latência em ms com margem de ±3%."})
        report = MODULE.run_engine(manifest, self.root)
        event = report["events"][0]
        self.assertFalse(any(gap["class"] == "TV-BOUNDARY" for gap in event["token_vazio"]))

    def test_duplicate_hashes_are_grouped_not_counted_as_independent(self) -> None:
        manifest = self.write_manifest({"a.txt": "mesmo", "b.txt": "mesmo"})
        report = MODULE.run_engine(manifest, self.root)
        self.assertEqual(report["statistics"]["duplicate_source_groups"], 1)

    def test_paradox_candidate_preserves_opposition(self) -> None:
        manifest = self.write_manifest({"a.txt": "A evidência confirma o modelo, mas o teste contradiz o resultado e está bloqueado."})
        report = MODULE.run_engine(manifest, self.root)
        self.assertTrue(report["events"][0]["paradox_candidate"])

    def test_initial_events_are_never_promoted(self) -> None:
        manifest = self.write_manifest({"a.txt": "Resultado executado PASS com hash e receipt."})
        report = MODULE.run_engine(manifest, self.root)
        self.assertTrue(all(event["state"] == "BRAINSTORM_CANDIDATE" for event in report["events"]))
        self.assertTrue(all(event["claim_allowed"] is False for event in report["events"]))


if __name__ == "__main__":
    unittest.main()
