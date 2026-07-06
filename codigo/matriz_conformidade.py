#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
matriz_conformidade.py — esqueleto norma x evidencia x gap por repositorio
(08_ANCORAGEM_NORMATIVA secao 6). Prepara a auditoria futura, honestamente.

PRIMEIRA-LINHA: DIGNIDADE-HUMANA / PROTECAO-INFANTIL (ONU UDHR Art.1 / UNCRC Art.3).

Nao afirma conformidade: liga cada conceito evidenciado a sua ancora normativa
(REFERENCE, de 08_) e abre uma linha de auditoria com estado PENDENTE. A passagem de
PENDENTE -> CONFORME exige auditoria real (fora do escopo desta sessao). Repos com
exposicao a dados pessoais/infantis recebem prioridade (regra pro-humano de 08_).

Sem dependencias (stdlib). Le indices/MANIFESTO_INTEGRIDADE.yaml.

    python3 codigo/matriz_conformidade.py            # relatorio
    python3 codigo/matriz_conformidade.py --write    # grava indices/MATRIZ_CONFORMIDADE.md
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFESTO = os.path.join(ROOT, "indices", "MANIFESTO_INTEGRIDADE.yaml")

# conceito -> ancora normativa externa (REFERENCE, de 08_ANCORAGEM_NORMATIVA)
CONCEITO_NORMA = {
    "C01": "SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade)",
    "C03": "NIST FIPS 180-4 / FIPS 202 (hashing)",
    "C04": "W3C PROV-O; ISO 15489 (proveniencia/custodia)",
    "C05": "IETF RFC 8032 (assinatura Ed25519)",
    "C11": "UNESCO Etica da IA 2021 (enquadramento)",
    "C13": "ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos)",
}

# repos com exposicao a dados pessoais/publico -> LGPD/GDPR, prioridade alta
DADOS_PESSOAIS = {
    "conversations_chunks_private": "corpus de conversas (dados pessoais)",
    "home": "analise de codigo/dados do usuario",
    "gaia_phi": "indexacao/dataset",
    "x0": "ecossistema cognitivo com dados",
    "lgpd_constituicoes": "framework LGPD/direitos (proprio dominio)",
}
NORMA_DADOS = "LGPD 13.709/2018; GDPR 2016/679; ISO/IEC 27701 (privacidade)"


def ler_evidencia(path: str) -> dict:
    """{id: {Cxx: origem}} do manifesto."""
    out, cur = {}, None
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            m = re.match(r"\s*-\s*id:\s*(\S+)", ln)
            if m:
                cur = m.group(1)
                continue
            m = re.match(r"\s*evidencia_origem:\s*\{(.*)\}", ln)
            if m and cur is not None:
                d = {}
                for par in m.group(1).split(","):
                    if ":" in par:
                        k, v = par.split(":", 1)
                        d[k.strip()] = v.strip()
                out[cur] = d
    return out


def linhas_conformidade():
    ev = ler_evidencia(MANIFESTO)
    rows = []
    for rid in sorted(ev):
        prioridade = "ALTA" if rid in DADOS_PESSOAIS else "normal"
        # linha de dados pessoais (se aplicavel)
        if rid in DADOS_PESSOAIS:
            rows.append({"repo": rid, "norma": NORMA_DADOS, "conceito": "dados",
                         "evidencia": DADOS_PESSOAIS[rid], "auditoria": "PENDENTE",
                         "prioridade": "ALTA"})
        # linhas por conceito com ancora normativa
        for c, origem in sorted(ev[rid].items()):
            if c in CONCEITO_NORMA:
                rows.append({"repo": rid, "norma": CONCEITO_NORMA[c], "conceito": c,
                             "evidencia": origem, "auditoria": "PENDENTE",
                             "prioridade": prioridade})
    return rows


def relatorio(rows) -> str:
    L = ["MATRIZ DE CONFORMIDADE :: norma x evidencia x gap (REFERENCE, nao atestado)",
         "PRIMEIRA-LINHA: DIGNIDADE-HUMANA / PROTECAO-INFANTIL", ""]
    alta = [r for r in rows if r["prioridade"] == "ALTA"]
    L.append(f"linhas: {len(rows)}  |  prioridade ALTA (dados pessoais): {len(alta)}")
    L.append("estado global de auditoria: PENDENTE (nenhuma conformidade atestada)")
    L.append("")
    L.append("prioridade ALTA (auditar primeiro):")
    for r in sorted({r['repo'] for r in alta}):
        L.append(f"  - {r}")
    return "\n".join(L)


def markdown(rows) -> str:
    L = ["> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ "
         "(ONU UDHR Art.1 · UNCRC Art.3)",
         "",
         "# Matriz de Conformidade — norma × evidência × gap",
         "",
         "Gerado por `codigo/matriz_conformidade.py`. Liga cada conceito evidenciado à sua "
         "**âncora normativa** (`REFERENCE`, de `biblioteconomia/08_ANCORAGEM_NORMATIVA.md`) "
         "e abre uma linha de auditoria. **Estado global: `PENDENTE`** — nada aqui é atestado "
         "de conformidade; a passagem `PENDENTE`→`CONFORME` exige auditoria real (próximo "
         "ciclo). Repos com dados pessoais têm **prioridade ALTA** (regra pró-humano).",
         "",
         "| prioridade | repo | conceito | norma (REFERENCE) | evidência | auditoria |",
         "|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["prioridade"] != "ALTA", r["repo"])):
        L.append(f"| {r['prioridade']} | {r['repo']} | {r['conceito']} | {r['norma']} "
                 f"| {r['evidencia']} | {r['auditoria']} |")
    L += ["",
          "> Honestidade: `REFERENCE` = alvo/orientação, não conformidade demonstrada. "
          "Evidência do conceito ≠ prova de que a norma é cumprida. Cada linha é uma tarefa "
          "de auditoria, não um selo."]
    return "\n".join(L) + "\n"


def main(argv=None):
    rows = linhas_conformidade()
    if argv is None:
        argv = sys.argv[1:]
    if "--write" in argv:
        out = os.path.join(ROOT, "indices", "MATRIZ_CONFORMIDADE.md")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(markdown(rows))
        sys.stderr.write(f"gravado: {out}\n")
    print(relatorio(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
