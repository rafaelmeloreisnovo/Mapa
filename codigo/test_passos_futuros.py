#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes dos passos futuros: marca_epistemica e matriz_conformidade.

    python3 -m unittest codigo/test_passos_futuros.py
"""
import os
import tempfile
import unittest

import marca_epistemica as ME
import matriz_conformidade as MC


class TestMarcaEpistemica(unittest.TestCase):

    def test_sugerir_estrato_codigo(self):
        self.assertEqual(ME.sugerir("NG1", "codigo"), "REFORCA_FATO")
        self.assertEqual(ME.sugerir("NG1", "codigo+prosa"), "REFORCA_FATO")
        self.assertEqual(ME.sugerir("NG1", "prosa"), "CANDIDATO_HIPOTESE")
        self.assertEqual(ME.sugerir("NG7", None), "SEM_EVIDENCIA")

    def test_sugerir_estrato_simbolico(self):
        self.assertEqual(ME.sugerir("NG6", "prosa"), "COERENTE_SIMBOLICO")
        self.assertEqual(ME.sugerir("NG6", "codigo"), "REFORCA")

    def test_sugerir_misto_neutro(self):
        self.assertEqual(ME.sugerir("NG4", "prosa"), "OK_MISTO")
        self.assertEqual(ME.sugerir("NG5", "codigo"), "OK_MISTO")

    def test_ler_origem_parser(self):
        txt = ("  - id: alfa\n"
               "    evidencia_origem: {C01: codigo, C11: prosa}\n")
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(txt); p = fh.name
        try:
            og = ME.ler_origem(p)
            self.assertEqual(og["alfa"], {"C01": "codigo", "C11": "prosa"})
        finally:
            os.unlink(p)

    def test_avaliar_roda_nos_28(self):
        av = ME.avaliar()
        self.assertEqual(len(av), 28)


class TestMatrizConformidade(unittest.TestCase):

    def test_conceito_norma_tem_ancoras(self):
        self.assertIn("C03", MC.CONCEITO_NORMA)
        self.assertIn("C13", MC.CONCEITO_NORMA)

    def test_linhas_conformidade_pendente(self):
        rows = MC.linhas_conformidade()
        self.assertTrue(rows)
        # tudo PENDENTE (nada atestado)
        self.assertTrue(all(r["auditoria"] == "PENDENTE" for r in rows))

    def test_dados_pessoais_prioridade_alta(self):
        rows = MC.linhas_conformidade()
        altas = {r["repo"] for r in rows if r["prioridade"] == "ALTA"}
        self.assertIn("conversations_chunks_private", altas)
        self.assertIn("home", altas)

    def test_ler_evidencia_parser(self):
        txt = ("  - id: beta\n"
               "    evidencia_origem: {C03: codigo+prosa}\n")
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(txt); p = fh.name
        try:
            ev = MC.ler_evidencia(p)
            self.assertEqual(ev["beta"], {"C03": "codigo+prosa"})
        finally:
            os.unlink(p)


if __name__ == "__main__":
    unittest.main()
