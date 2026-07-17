#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_mapa_topology.py"
SPEC = importlib.util.spec_from_file_location("validate_mapa_topology", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class TopologyValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph_path = ROOT / "indices" / "GRAFO_DEPENDENCIAS_MAPA.yaml"
        cls.data, cls.header = validator.parse_document(cls.graph_path)

    def validate(self, data: dict) -> dict:
        return validator.validate_graph(data, ROOT, self.header)

    def test_repository_graph_is_valid(self) -> None:
        report = self.validate(copy.deepcopy(self.data))
        self.assertTrue(report["ok"], json.dumps(report["errors"], ensure_ascii=False))
        self.assertEqual(report["derived_metrics"]["node_count"], 33)
        self.assertEqual(report["derived_metrics"]["cycle_count"], 0)
        self.assertEqual(report["derived_metrics"]["orphan_count"], 0)

    def test_cycle_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        root = next(node for node in data["nodes"] if node["id"] == "I_00")
        root["depends_on"] = ["QUALITY_gate"]
        data["integrity"]["digest"] = validator.canonical_digest(data)
        report = self.validate(data)
        self.assertFalse(report["ok"])
        self.assertTrue(any("ciclo detectado" in error for error in report["errors"]))

    def test_missing_dependency_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        node = next(node for node in data["nodes"] if node["id"] == "QUERY_engine")
        node["depends_on"].append("TOKEN_VAZIO_NAO_DECLARADO")
        data["integrity"]["digest"] = validator.canonical_digest(data)
        report = self.validate(data)
        self.assertFalse(report["ok"])
        self.assertTrue(any("dependência inexistente" in error for error in report["errors"]))

    def test_planned_node_cannot_claim_fact(self) -> None:
        data = copy.deepcopy(self.data)
        node = next(node for node in data["nodes"] if node["id"] == "F_04")
        node["epistemic_mark"] = "FATO"
        data["integrity"]["digest"] = validator.canonical_digest(data)
        report = self.validate(data)
        self.assertFalse(report["ok"])
        self.assertTrue(any("planned exige epistemic_mark=LACUNA" in error for error in report["errors"]))

    def test_integrity_tampering_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["nodes"][0]["name"] = "ALTERADO SEM RESELAGEM"
        report = self.validate(data)
        self.assertFalse(report["ok"])
        self.assertFalse(report["integrity"]["match"])


if __name__ == "__main__":
    unittest.main()
