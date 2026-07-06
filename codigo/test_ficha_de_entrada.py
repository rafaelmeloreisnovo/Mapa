#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes de coerencia da ficha de entrada (stdlib unittest).

Cobre a coluna 'testes' da resiliencia (09_RESILIENCIA_TOP10.md):
determinismo reprodutivel, primeira linha, honestidade e integridade referencial.

    python3 -m unittest codigo/test_ficha_de_entrada.py
"""
import unittest

from ficha_de_entrada import (
    EXEMPLOS, GRUPAMENTOS, MARCAS, validar, canonico, Ficha,
)


class TestCoerencia(unittest.TestCase):

    def test_todas_as_fichas_sao_coerentes(self):
        problemas = []
        for f in EXEMPLOS:
            problemas += validar(f)
        self.assertEqual(problemas, [], "\n".join(problemas))

    def test_sao_28_fichas(self):
        self.assertEqual(len(EXEMPLOS), 28)

    def test_ids_unicos(self):
        ids = [f.id for f in EXEMPLOS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_cobre_os_sete_grupamentos(self):
        usados = {f.no_grupo for f in EXEMPLOS}
        self.assertEqual(usados, set(GRUPAMENTOS))

    def test_omega_coord_e_deterministica(self):
        # mesma ficha -> mesma coordenada, sempre (invariante C01).
        for f in EXEMPLOS:
            self.assertEqual(f.omega_coord(), f.omega_coord())

    def test_omega_coord_reproduz_apos_reconstrucao(self):
        f = EXEMPLOS[0]
        clone = Ficha(id=f.id, objeto=f.objeto, origem=f.origem,
                      no_grupo=f.no_grupo, camada_L=f.camada_L,
                      conceitos=list(f.conceitos), notacao=f.notacao,
                      marca=f.marca)
        self.assertEqual(f.omega_coord(), clone.omega_coord())

    def test_primeira_linha_conferida(self):
        for f in EXEMPLOS:
            self.assertTrue(f.primeira_linha_ok, f.id)

    def test_lacuna_tem_proxima_acao(self):
        for f in EXEMPLOS:
            if f.marca == "LACUNA":
                self.assertTrue(f.proxima_acao, f.id)

    def test_marca_valida(self):
        for f in EXEMPLOS:
            self.assertIn(f.marca, MARCAS)

    def test_json_canonico_e_estavel(self):
        # duas emissoes produzem exatamente o mesmo texto.
        self.assertEqual(canonico(EXEMPLOS), canonico(EXEMPLOS))

    def test_validador_pega_erro(self):
        ruim = Ficha(id="x", objeto="x", origem="x", no_grupo="NGX",
                     camada_L="L9", conceitos=["C99"], notacao="ERR",
                     marca="TALVEZ")
        self.assertTrue(validar(ruim))


if __name__ == "__main__":
    unittest.main()
