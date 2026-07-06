#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
revisao_publicacao.py — cruza o DECLARADO (fichas) com o EVIDENCIADO (varredura de
conteudo) e produz achados reais de revisao de publicacao.

PRIMEIRA-LINHA: DIGNIDADE-HUMANA / PROTECAO-INFANTIL (ONU UDHR Art.1 / UNCRC Art.3).

Faz o conteudo "acontecer": para cada repo compara os conceitos que a ficha DECLARA
com os que a varredura ACHOU no conteudo, e classifica cada divergencia:

  confirmado           = declarado E evidenciado no conteudo         (FATO)
  declarado_sem_texto  = declarado mas NAO achado (entre os escaneados) -> RISCO/revisar
  nao_escaneado        = declarado mas fora do vocabulario de scan    -> nao verificavel por texto
  evidenciado_extra    = achado no conteudo mas NAO declarado         -> possivel descoberta

Sem dependencias (stdlib). Le indices/MANIFESTO_INTEGRIDADE.yaml (formato proprio,
parser minimo) e importa as fichas de ficha_de_entrada.py.

    python3 codigo/revisao_publicacao.py            # relatorio
    python3 codigo/revisao_publicacao.py --write    # grava indices/REVISAO_PUBLICACAO.md
"""
from __future__ import annotations

import os
import re
import sys

from ficha_de_entrada import EXEMPLOS
from varredura_conteudo import CONCEITO_TERMOS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFESTO = os.path.join(ROOT, "indices", "MANIFESTO_INTEGRIDADE.yaml")

# conceitos que a varredura de fato escaneia (tem termos-ancora)
ESCANEADOS = {k.split("_")[0] for k in CONCEITO_TERMOS}


def ler_evidenciados(path: str) -> dict:
    """Extrai {id: set(conceitos_evidenciados)} do manifesto (parser minimo)."""
    ev, cur = {}, None
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            m = re.match(r"\s*-\s*id:\s*(\S+)", ln)
            if m:
                cur = m.group(1)
                continue
            m = re.match(r"\s*conceitos_evidenciados:\s*\[(.*)\]", ln)
            if m and cur is not None:
                cods = [c.strip() for c in m.group(1).split(",") if c.strip()]
                ev[cur] = set(cods)
    return ev


def declarados() -> dict:
    return {f.id: set(f.conceitos) for f in EXEMPLOS}


def revisar():
    ev = ler_evidenciados(MANIFESTO)
    dec = declarados()
    linhas = []
    for rid in sorted(dec):
        d = dec[rid]
        e = ev.get(rid, set())
        confirmado = sorted(d & e)
        declarado_sem_texto = sorted((d - e) & ESCANEADOS)
        nao_escaneado = sorted((d - e) - ESCANEADOS)
        evidenciado_extra = sorted(e - d)
        linhas.append({
            "id": rid,
            "confirmado": confirmado,
            "declarado_sem_texto": declarado_sem_texto,
            "nao_escaneado": nao_escaneado,
            "evidenciado_extra": evidenciado_extra,
        })
    return linhas


def relatorio(rev) -> str:
    L = ["REVISAO DE PUBLICACAO :: declarado (ficha) x evidenciado (conteudo)",
         "PRIMEIRA-LINHA: DIGNIDADE-HUMANA / PROTECAO-INFANTIL", ""]
    achados = 0
    for r in rev:
        marca = ""
        if r["declarado_sem_texto"]:
            marca = "  <-- RISCO: declarado sem evidencia textual"
            achados += 1
        L.append(f"{r['id']:<28} ok={len(r['confirmado'])} "
                 f"sem_texto={r['declarado_sem_texto'] or '-'} "
                 f"extra={len(r['evidenciado_extra'])}{marca}")
    L.append("")
    L.append(f"repos com declarado-sem-evidencia (revisar): {achados}")
    return "\n".join(L)


def markdown(rev) -> str:
    L = ["> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ "
         "(ONU UDHR Art.1 · UNCRC Art.3)",
         "",
         "# Revisão de Publicação — declarado (ficha) × evidenciado (conteúdo)",
         "",
         "Gerado por `codigo/revisao_publicacao.py`. Cruza os conceitos que cada ficha "
         "**declara** com os que a varredura **achou no conteúdo** "
         "(`indices/MANIFESTO_INTEGRIDADE.yaml`).",
         "",
         "- **confirmado**: declarado E no conteúdo (`FATO`).",
         "- **declarado_sem_texto**: declarado, escaneado, mas não achado → `RISCO`, revisar.",
         "- **nao_escaneado**: declarado, mas fora do vocabulário de scan → não verificável por texto.",
         "- **evidenciado_extra**: no conteúdo, mas não declarado → possível descoberta.",
         "",
         "| repo | confirmado | declarado_sem_texto (RISCO) | nao_escaneado | evidenciado_extra |",
         "|---|---|---|---|---|"]
    for r in rev:
        L.append(f"| {r['id']} | {len(r['confirmado'])} | "
                 f"{', '.join(r['declarado_sem_texto']) or '—'} | "
                 f"{', '.join(r['nao_escaneado']) or '—'} | "
                 f"{len(r['evidenciado_extra'])} |")
    risco = [r['id'] for r in rev if r['declarado_sem_texto']]
    L += ["",
          f"**Repos a revisar** (declarado sem evidencia textual): "
          f"{', '.join(risco) if risco else 'nenhum'}.",
          "",
          "> Honestidade: ausência de evidência textual não prova ausência do conceito "
          "(pode estar em binário, em imagem, ou nomeado de outro modo). Cada linha de RISCO "
          "vira um teste, não uma conclusão — ver `biblioteconomia/13_CERTIFICACAO_METODOLOGICA.md` (PDCA)."]
    return "\n".join(L) + "\n"


def main(argv=None):
    rev = revisar()
    if argv is None:
        argv = sys.argv[1:]
    if "--write" in argv:
        out = os.path.join(ROOT, "indices", "REVISAO_PUBLICACAO.md")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(markdown(rev))
        sys.stderr.write(f"gravado: {out}\n")
    print(relatorio(rev))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
