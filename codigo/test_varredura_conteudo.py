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
        base = [{"id": "r1", "triple": {"prova": "aa"}},
                {"id": "r2", "triple": {"prova": "bb"}}]
        p1 = V.acervo_prova(base)
        self.assertEqual(p1, V.acervo_prova(list(reversed(base))))  # ordem nao importa
        mudou = [{"id": "r1", "triple": {"prova": "aa"}},
                 {"id": "r2", "triple": {"prova": "cc"}}]
        self.assertNotEqual(p1, V.acervo_prova(mudou))  # muda se um repo muda

    def test_acervo_prova_ignora_mapa_autoreferente(self):
        a = [{"id": "r1", "triple": {"prova": "aa"}},
             {"id": "mapa", "triple": {"prova": "X"}}]
        b = [{"id": "r1", "triple": {"prova": "aa"}},
             {"id": "mapa", "triple": {"prova": "Y"}}]  # mapa mudou
        self.assertEqual(V.acervo_prova(a), V.acervo_prova(b))  # selo NAO muda

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

    def test_classificar_origem(self):
        self.assertEqual(V.classificar_origem(True, True), "codigo+prosa")
        self.assertEqual(V.classificar_origem(True, False), "codigo")
        self.assertEqual(V.classificar_origem(False, True), "prosa")
        self.assertIsNone(V.classificar_origem(False, False))

    def test_code_prose_ext_disjuntos(self):
        self.assertFalse(V.CODE_EXT & V.PROSE_EXT)
        self.assertTrue(V.PROSE_EXT.issubset(V.TEXT_EXT))

    def test_origem_por_repo_conta(self):
        r = {"evidencia_origem": {"C01": "codigo", "C11": "prosa",
                                  "C04": "codigo+prosa"}}
        cod, pro = V.origem_por_repo(r)
        self.assertEqual((cod, pro), (2, 2))  # C01+C04 codigo; C11+C04 prosa

    def test_resumo_origem(self):
        res = [{"evidencia_origem": {"C01": "codigo", "C02": "prosa"}},
               {"evidencia_origem": {"C01": "codigo+prosa"}}]
        self.assertEqual(V.resumo_origem(res),
                         {"codigo": 1, "prosa": 1, "codigo+prosa": 1})

    def test_resumo_metricas_soma(self):
        res = [{"metricas": {"loc_codigo": 10, "kb_codigo": 2, "kb_prosa": 1,
                             "kb_dados": 0}},
               {"metricas": {"loc_codigo": 5, "kb_codigo": 3, "kb_prosa": 0,
                             "kb_dados": 4}}]
        self.assertEqual(V.resumo_metricas(res),
                         {"loc_codigo": 15, "kb_codigo": 5, "kb_prosa": 1,
                          "kb_dados": 4})

    def test_vendored_heuristica(self):
        self.assertIn("vendor/", V.VENDORED)
        self.assertIn(".cargo/", V.VENDORED)


if __name__ == "__main__":
    unittest.main()
