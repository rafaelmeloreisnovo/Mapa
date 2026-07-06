#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes das funcoes deterministas da varredura (sem depender de git/rede).

    python3 -m unittest codigo/test_varredura_conteudo.py
"""
import unittest

import varredura_conteudo as V


class TestPuro(unittest.TestCase):

    def test_blake_deterministico(self):
        self.assertEqual(V._blake("abc"), V._blake("abc"))
        self.assertNotEqual(V._blake("abc"), V._blake("abd"))
        self.assertEqual(len(V._blake("x")), 16)  # digest_size=8 -> 16 hex

    def test_28_repos_mapeados(self):
        self.assertEqual(len(V.REPOS), 28)
        self.assertEqual(len(set(V.REPOS.values())), 28)  # dirs unicos

    def test_acervo_prova_estavel_e_sensivel(self):
        base = [{"triple": {"prova": "aa"}}, {"triple": {"prova": "bb"}}]
        p1 = V.acervo_prova(base)
        self.assertEqual(p1, V.acervo_prova(list(reversed(base))))  # ordem nao importa
        mudou = [{"triple": {"prova": "aa"}}, {"triple": {"prova": "cc"}}]
        self.assertNotEqual(p1, V.acervo_prova(mudou))  # muda se um repo muda

    def test_correlacoes_indice_invertido(self):
        res = [
            {"id": "r1", "conceitos_evidenciados": ["C01", "C04"]},
            {"id": "r2", "conceitos_evidenciados": ["C04"]},
        ]
        cor = V.correlacoes(res)
        self.assertEqual(cor["C04"], ["r1", "r2"])
        self.assertEqual(cor["C01"], ["r1"])

    def test_manifesto_tem_primeira_linha_e_selo(self):
        res = [{"id": "r1", "dir": "R1", "head": "abc", "arquivos": 1,
                "conteudo_vivo": [".py:1"],
                "triple": {"coerencia": "a", "integridade": "b", "prova": "c"},
                "conceitos_evidenciados": ["C01"], "estado": "FATO"}]
        y = V.manifesto_yaml(res, base="/x")
        self.assertIn("DIGNIDADE-HUMANA", y)
        self.assertIn("selo_acervo_prova:", y)
        self.assertIn("metodo_triple:", y)

    def test_conceito_termos_sem_codigos_repetidos(self):
        codigos = [k.split("_")[0] for k in V.CONCEITO_TERMOS]
        self.assertEqual(len(codigos), len(set(codigos)))


if __name__ == "__main__":
    unittest.main()
