#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes da revisao de publicacao (cruzamento declarado x evidenciado).

    python3 -m unittest codigo/test_revisao_publicacao.py
"""
import os
import tempfile
import unittest

import revisao_publicacao as R


class TestRevisao(unittest.TestCase):

    def test_parser_le_evidenciados(self):
        txt = ("repos:\n"
               "  - id: alfa\n"
               "    conceitos_evidenciados: [C01, C04, C13]\n"
               "  - id: beta\n"
               "    conceitos_evidenciados: []\n")
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(txt)
            p = fh.name
        try:
            ev = R.ler_evidenciados(p)
            self.assertEqual(ev["alfa"], {"C01", "C04", "C13"})
            self.assertEqual(ev["beta"], set())
        finally:
            os.unlink(p)

    def test_declarados_vem_das_fichas(self):
        dec = R.declarados()
        self.assertEqual(len(dec), 28)
        self.assertIn("chipquantum", dec)

    def test_revisar_classifica_divergencias(self):
        rev = R.revisar()
        self.assertEqual(len(rev), 28)
        for r in rev:
            # nenhuma sobreposicao entre as quatro classes
            s = set(r["confirmado"]) | set(r["declarado_sem_texto"]) \
                | set(r["nao_escaneado"])
            # confirmado e declarado_sem_texto/nao_escaneado sao disjuntos
            self.assertFalse(set(r["confirmado"]) & set(r["declarado_sem_texto"]))
            self.assertFalse(set(r["confirmado"]) & set(r["nao_escaneado"]))

    def test_manifesto_existe(self):
        self.assertTrue(os.path.exists(R.MANIFESTO))

    def test_markdown_tem_primeira_linha(self):
        rev = R.revisar()
        md = R.markdown(rev)
        self.assertIn("PRIMEIRA-LINHA", md)
        self.assertIn("declarado_sem_texto", md)


if __name__ == "__main__":
    unittest.main()
