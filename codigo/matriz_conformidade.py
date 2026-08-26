#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
matriz_conformidade.py — esqueleto norma x evidencia x gap por repositorio
(08_ANCORAGEM_NORMATIVA secao 6). Prepara a auditoria futura, honestamente.

PRIMEIRA-LINHA: DIGNIDADE-HUMANA / PROTECAO-INFANTIL (ONU UDHR Art.1 / UNCRC Art.3).

Nao afirma conformidade: liga cada conceito evidenciado a sua ancora normativa
(REFERENCE, de 08_) e abre uma linha de auditoria com estado PENDENTE. A passagem de
PENDENTE -> CONFORME exige auditoria real. Repos com exposicao a dados pessoais/infantis
recebem prioridade, mas aplicabilidade juridica depende do fluxo factual, jurisdicao,
autoridade, vigencia e evidencia.

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
CANON_PRIVACY = "docs/legal/GLOBAL_DATA_PRIVACY_GNSS_AI_GOVERNANCE_V1.md"
ATLAS_PRIVACY = "data/normative-graph/GLOBAL_DATA_PRIVACY_GNSS_AI_SEMANTIC_ATLAS_V1.json"

# conceito -> ancora normativa externa (REFERENCE, de 08_ANCORAGEM_NORMATIVA)
CONCEITO_NORMA = {
    "C01": "SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade)",
    "C03": "NIST FIPS 180-4 / FIPS 202 (hashing)",
    "C04": "W3C PROV-O; ISO 15489 (proveniencia/custodia)",
    "C05": "IETF RFC 8032 (assinatura Ed25519)",
    "C11": "UNESCO Etica da IA 2021 (enquadramento)",
    "C13": "ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos)",
}

# repos com exposicao material a dados pessoais/publico -> prioridade alta.
# O nome do repo nao prova aplicabilidade; cada linha continua PENDENTE ate fluxo factual.
DADOS_PESSOAIS = {
    "conversations_chunks_private": "corpus de conversas (dados pessoais)",
    "home": "analise de codigo/dados do usuario",
    "gaia_phi": "indexacao/dataset",
    "x0": "ecossistema cognitivo com dados",
    "lgpd_constituicoes": "framework LGPD/direitos (proprio dominio)",
    "termux-api_rafcodephi": (
        "ponte Android com APIs de localizacao, contatos, call log, SMS, microfone, "
        "telefonia e outros dados conforme metodo/permissao"
    ),
}
NORMA_DADOS = (
    "CF/88 privacidade+dados; Marco Civil; LGPD 13.709/2018; "
    "GDPR 2016/679 quando aplicavel; ISO/IEC 27701 como REFERENCE"
)


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
        if rid in DADOS_PESSOAIS:
            rows.append({"repo": rid, "norma": NORMA_DADOS, "conceito": "dados",
                         "evidencia": DADOS_PESSOAIS[rid], "auditoria": "PENDENTE",
                         "prioridade": "ALTA"})
        for c, origem in sorted(ev[rid].items()):
            if c in CONCEITO_NORMA:
                rows.append({"repo": rid, "norma": CONCEITO_NORMA[c], "conceito": c,
                             "evidencia": origem, "auditoria": "PENDENTE",
                             "prioridade": prioridade})
    return rows


def relatorio(rows) -> str:
    L = ["MATRIZ DE CONFORMIDADE :: norma x evidencia x gap (REFERENCE, nao atestado)",
         "PRIMEIRA-LINHA: DIGNIDADE-HUMANA / PROTECAO-INFANTIL",
         f"CANON_PRIVACY: {CANON_PRIVACY}",
         f"ATLAS_PRIVACY: {ATLAS_PRIVACY}", ""]
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
         "de conformidade; a passagem `PENDENTE`→`CONFORME` exige auditoria real. Repos com "
         "dados pessoais têm **prioridade ALTA**, mas o nome do repo não prova aplicabilidade.",
         "",
         f"Cânone jurídico de privacidade/GNSS/IA: `{CANON_PRIVACY}`.",
         f"Atlas semântico: `{ATLAS_PRIVACY}`.",
         "",
         "> `permissão_do_SO != base_jurídica`; `data_no_dispositivo != dado_no_modelo`; "
         "`TOKEN_VAZIO != falso`. Cada fluxo deve ser provado ponta a ponta.",
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
