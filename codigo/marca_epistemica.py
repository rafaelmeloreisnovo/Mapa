#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
marca_epistemica.py — usa a evidencia (codigo vs prosa) para REFORCAR ou REBAIXAR a
marca epistemica de cada conceito declarado, por estrato (16_ proxima acao).

PRIMEIRA-LINHA: DIGNIDADE-HUMANA / PROTECAO-INFANTIL (ONU UDHR Art.1 / UNCRC Art.3).

Regra (honesta, nao automatica-cega):
  - Estrato de codigo (nucleo/plataforma/cognicao/meta) + evidencia em CODIGO
        -> REFORCA_FATO (implementado, nao so declarado).
  - Estrato de codigo + evidencia so em PROSA
        -> CANDIDATO_HIPOTESE (declarado como tecnico, mas so discutido em texto).
  - Estrato simbolico (espiritual) + evidencia em CODIGO
        -> REFORCA (surpreende positivamente: o simbolico virou codigo).
  - Estrato simbolico + evidencia so em PROSA
        -> COERENTE_SIMBOLICO (esperado; a prosa e o lugar certo).
  - Sem evidencia -> ver revisao_publicacao (RISCO), aqui marcado SEM_EVIDENCIA.

Nao reescreve fichas automaticamente: EMITE SUGESTOES para revisao humana (PDCA 13_).
Sem dependencias (stdlib). Le indices/MANIFESTO_INTEGRIDADE.yaml (parser minimo).

    python3 codigo/marca_epistemica.py            # relatorio
    python3 codigo/marca_epistemica.py --write    # grava indices/MARCA_EPISTEMICA.md
"""
from __future__ import annotations

import os
import re
import sys

from ficha_de_entrada import EXEMPLOS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFESTO = os.path.join(ROOT, "indices", "MANIFESTO_INTEGRIDADE.yaml")

CODE_ESPERADO = {"NG1", "NG2", "NG3", "NG7"}   # nucleo, plataforma, cognicao, meta
PROSA_ESPERADO = {"NG6"}                        # espiritual
# NG4 (ciencia) e NG5 (juridico) sao mistos -> neutro


def ler_origem(path: str) -> dict:
    """{id: {Cxx: 'codigo'|'prosa'|'codigo+prosa'}} do manifesto."""
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


def sugerir(no_grupo: str, origem: str | None) -> str:
    tem_codigo = origem is not None and "codigo" in origem
    so_prosa = origem == "prosa"
    if origem is None:
        return "SEM_EVIDENCIA"
    if no_grupo in CODE_ESPERADO:
        return "REFORCA_FATO" if tem_codigo else "CANDIDATO_HIPOTESE"
    if no_grupo in PROSA_ESPERADO:
        return "REFORCA" if tem_codigo else "COERENTE_SIMBOLICO"
    return "OK_MISTO"


def avaliar():
    origem = ler_origem(MANIFESTO)
    linhas = []
    for f in EXEMPLOS:
        og = origem.get(f.id, {})
        itens = []
        for c in sorted(f.conceitos):
            o = og.get(c)
            itens.append({"conceito": c, "origem": o or "-",
                          "sugestao": sugerir(f.no_grupo, o)})
        linhas.append({"id": f.id, "no_grupo": f.no_grupo,
                       "marca_atual": f.marca, "itens": itens})
    return linhas


def relatorio(av) -> str:
    L = ["MARCA EPISTEMICA :: reforco/rebaixamento por evidencia (codigo vs prosa)",
         "PRIMEIRA-LINHA: DIGNIDADE-HUMANA / PROTECAO-INFANTIL", ""]
    cand, ref = [], 0
    for r in av:
        for it in r["itens"]:
            if it["sugestao"] == "CANDIDATO_HIPOTESE":
                cand.append(f"{r['id']}:{it['conceito']}")
            if it["sugestao"] in ("REFORCA_FATO", "REFORCA"):
                ref += 1
    L.append(f"reforcos (evidencia em codigo): {ref}")
    L.append(f"candidatos a HIPOTESE (declarado tecnico, so em prosa): "
             f"{len(cand)}")
    for c in cand:
        L.append(f"  - {c}")
    return "\n".join(L)


def markdown(av) -> str:
    cand = [(r["id"], it["conceito"]) for r in av for it in r["itens"]
            if it["sugestao"] == "CANDIDATO_HIPOTESE"]
    L = ["> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ "
         "(ONU UDHR Art.1 · UNCRC Art.3)",
         "",
         "# Marca Epistêmica por Evidência (código vs prosa)",
         "",
         "Gerado por `codigo/marca_epistemica.py`. Usa `evidencia_origem` do manifesto "
         "para **sugerir** reforço (`FATO`) ou rebaixamento (`HIPOTESE`) da marca de cada "
         "conceito declarado, por estrato. **Não reescreve fichas** — sugere para revisão "
         "humana (PDCA, `biblioteconomia/13_CERTIFICACAO_METODOLOGICA.md`).",
         "",
         "## Candidatos a HIPOTESE (declarado como técnico, mas só em prosa)",
         ""]
    if cand:
        for rid, c in cand:
            L.append(f"- `{rid}` · **{c}** — estrato de código, evidência só em prosa → revisar.")
    else:
        L.append("- (nenhum) — todos os conceitos técnicos declarados têm evidência em código.")
    L += ["",
          "## Leitura por repositório",
          "",
          "| repo | nó | marca | conceitos (origem → sugestão) |",
          "|---|---|---|---|"]
    for r in av:
        itens = "; ".join(f"{it['conceito']}:{it['origem']}→{it['sugestao']}"
                          for it in r["itens"])
        L.append(f"| {r['id']} | {r['no_grupo']} | {r['marca_atual']} | {itens or '—'} |")
    L += ["",
          "> Honestidade: a sugestão é heurística por estrato, não veredito. Evidência só "
          "em prosa não prova ausência de implementação (pode estar em binário ou nomeada "
          "de outro modo). Cada candidato vira teste, não conclusão."]
    return "\n".join(L) + "\n"


def main(argv=None):
    av = avaliar()
    if argv is None:
        argv = sys.argv[1:]
    if "--write" in argv:
        out = os.path.join(ROOT, "indices", "MARCA_EPISTEMICA.md")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(markdown(av))
        sys.stderr.write(f"gravado: {out}\n")
    print(relatorio(av))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
