#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
varredura_conteudo.py — le os ARQUIVOS e o CONTEUDO VIVO dos 28 repositorios
ja mapeados e produz o sistema de coerencia / integridade / prova (HASHING TRIPLO),
mais a correlacao evolutiva de conceitos por EVIDENCIA TEXTUAL (nao so pelo README).

PRIMEIRA-LINHA: DIGNIDADE-HUMANA / PROTECAO-INFANTIL (ONU UDHR Art.1 / UNCRC Art.3).

Escopo: apenas o avesso dos 28 catalogados (clonados localmente). Nao le repos fora
de escopo. Determinista e reprodutivel: a mesma arvore -> os mesmos tres selos.

HASHING TRIPLO (por repositorio):
  coerencia   = blake2b(estrutura)      -> prova a FORMA (lista ordenada de arquivos)
  integridade = git tree SHA do HEAD    -> prova os BYTES (Merkle root do proprio git)
  prova       = blake2b(id|coerencia|integridade|head) -> SELO que amarra forma+bytes

Uso:
    python3 codigo/varredura_conteudo.py            # relatorio
    python3 codigo/varredura_conteudo.py --write    # grava indices/MANIFESTO_INTEGRIDADE.yaml
Base do acervo: env MAPA_ACERVO_BASE (default: pasta-mae do repo Mapa).
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from collections import Counter, defaultdict

# id (slug da ficha) -> nome do diretorio clonado
REPOS = {
    "chipquantum": "ChipQuantum", "deepseek-rafcoder": "DeepSeek-RafCoder",
    "gaia_phi": "GAIA_phi", "blake3": "BLAKE3", "rafgittools": "RafGitTools",
    "vectras-vm-android": "Vectras-VM-Android",
    "termux-app-rafacodephi": "termux-app-rafacodephi",
    "termux-api_rafcodephi": "termux-api_rafcodephi", "userland": "UserLAnd",
    "pcr_rafaelia_code_seed": "PCR_Rafaelia_Code_seed", "qemu_rafaelia": "qemu_rafaelia",
    "actions": "actions", "x0": "X0", "llamarafaelia": "llamaRafaelia",
    "conversations_chunks_private": "CONVERSATIONS_CHUNKS_PRIVATE", "home": "home",
    "relativity-living-light": "relativity-living-light", "matem-tica-": "Matem-tica-",
    "papers": "papers", "rafpolimata": "RafPolimata", "rafaelia_private": "Rafaelia_Private",
    "lgpd_constituicoes": "LGPD-Constituicoes-planetaria-paises-onu-direitos-humanos-e-"
                          "fundamentais-de-cada-continents-geologic",
    "livrovivo_thisbooklives": "LivroVivo_ThisBookLives", "blackhole": "Blackhole",
    "publicacientiespiritual": "publicacientiespiritual",
    "zipraf_omega_full": "ZIPRAF_OMEGA_FULL", "mapa": "Mapa", "memrafcode": "MemRafcode",
}

# conceito -> termos-âncora (evidencia textual FATO de ocorrencia; nao prova de
# implementacao correta). Termos muito ruidosos ficam de fora de proposito.
CONCEITO_TERMOS = {
    "C01_Determinismo": ["determinist", "reproducib", "constant-time", "branchless"],
    "C02_Invariante": ["invariant"],
    "C03_Hashing": ["blake", "sha256", "sha-256", "sha3", "merkle", "crc32", "hashing"],
    "C04_Custodia": ["custod", "provenance", "proveniencia", "manifest", "digest"],
    "C05_Assinatura": ["ed25519", "signature", "assinatur", "sigma-seal"],
    "C06_Toroide": ["toroid", "attractor", "atrator"],
    # C07: qualificado (evita o ruido do "42" nu) -> ver 04_FRICCAO_SEMANTICA F1
    "C07_Atrator42": ["attractorpool", "attractor_pool", "42 atratores",
                      "42 attractors", "42 estagios", "42 stages", "pool 42",
                      "atrator-42", "attractor-42"],
    "C08_Phi": ["phi_fst", "phi_attractor", "golden ratio", "razao aurea"],
    "C09_ZIPRAF": ["zipraf"],
    "C10_Vetor": ["hypervector", "hipervetor", "embedding", "vecdb"],
    "C11_CientiEspiritual": ["cientiespiritual", "cienti-espiritual", "cienti espiritual"],
    "C12_Verdade": ["verdade", "truth-"],
    "C13_Etica": ["ethica", "etica ", "ethics"],
    # C14/C15: termos afinados para PROSA do estrato L5 (17_ item 1)
    "C14_VerboVivo": ["verbovivo", "verbo vivo", "verbo-vivo", "verbum vivo",
                      "rafaelverbo", "living light", "living-light", "luz viva"],
    "C15_Universalismo": ["universal"],
    "C16_LACUNA": ["lacuna", "token_vazio", "token vazio"],
    "C17_NO_GOOD": ["no_good", "no good", "no-good", "no_good"],
}

# evidencia em CODIGO (implementado) vs em PROSA (discutido) — granularidade 16_
CODE_EXT = {".c", ".h", ".cpp", ".hpp", ".py", ".rs", ".java", ".kt", ".js", ".ts",
            ".sh", ".yaml", ".yml", ".toml", ".cfg", ".json"}
PROSE_EXT = {".md", ".rst", ".txt", ".tex", ".html"}
TEXT_EXT = CODE_EXT | PROSE_EXT


def classificar_origem(in_code: bool, in_prose: bool):
    """codigo (implementado) vs prosa (discutido) vs ambos vs None."""
    if in_code and in_prose:
        return "codigo+prosa"
    if in_code:
        return "codigo"
    if in_prose:
        return "prosa"
    return None


def _git(repo_dir, *args, timeout=60):
    try:
        out = subprocess.run(["git", "-C", repo_dir, *args],
                             capture_output=True, text=True, timeout=timeout)
        return out.stdout if out.returncode == 0 else ""
    except (subprocess.TimeoutExpired, OSError):
        return ""


def _blake(s: str) -> str:
    return hashlib.blake2b(s.encode("utf-8"), digest_size=8).hexdigest()


def escanear(repo_id: str, base: str) -> dict:
    d = os.path.join(base, REPOS[repo_id])
    if not os.path.isdir(os.path.join(d, ".git")):
        return {"id": repo_id, "erro": "sem .git", "estado": "LACUNA"}

    files = [l for l in _git(d, "ls-files").splitlines() if l]
    head = _git(d, "rev-parse", "HEAD").strip()[:12]
    tree = _git(d, "rev-parse", "HEAD^{tree}").strip()[:16]  # Merkle root do git

    # extensoes (conteudo vivo por tipo). git pode citar caminhos: sanitiza o token.
    def _ext(path):
        e = os.path.splitext(path.strip('"'))[1].lower()
        e = "".join(ch for ch in e if ch.isalnum() or ch == ".")
        return e or "<sem-ext>"
    ext = Counter(_ext(f) for f in files)
    top_ext = [f"{e}:{n}" for e, n in ext.most_common(6)]

    # HASHING TRIPLO
    coerencia = _blake("\n".join(sorted(files)))            # forma
    integridade = tree                                      # bytes (git tree SHA)
    prova = _blake(f"{repo_id}|{coerencia}|{integridade}|{head}")  # selo

    # conceitos evidenciados: CODIGO (implementado) vs PROSA (discutido)
    code_globs = [f"*{e}" for e in sorted(CODE_EXT)]
    prose_globs = [f"*{e}" for e in sorted(PROSE_EXT)]

    def _presente(termos, globs):
        args = ["grep", "-I", "-i", "-l"]
        for t in termos:
            args += ["-e", t]
        return bool(_git(d, *args, "--", *globs, timeout=40).strip())

    evidencia = {}   # Cxx -> "codigo" | "prosa" | "codigo+prosa"
    for conceito, termos in CONCEITO_TERMOS.items():
        cod = conceito.split("_")[0]
        origem = classificar_origem(_presente(termos, code_globs),
                                    _presente(termos, prose_globs))
        if origem:
            evidencia[cod] = origem

    return {
        "id": repo_id, "dir": REPOS[repo_id], "head": head, "arquivos": len(files),
        "conteudo_vivo": top_ext,
        "triple": {"coerencia": coerencia, "integridade": integridade, "prova": prova},
        "conceitos_evidenciados": sorted(evidencia),
        "evidencia_origem": evidencia,
        "metricas": metricas(d, files),
        # Mapa e auto-referente: seu selo muda a cada commit do proprio catalogo -> RUNTIME
        "estado": "RUNTIME" if repo_id == "mapa" else "FATO",
    }


# heuristica de vendored/gerado (peso que nao e contribuicao original)
VENDORED = ("vendor/", "third_party/", "dist/", "node_modules/", ".cargo/",
            ".cpan/", "site-packages/", "_deps/", "external/")


def metricas(d: str, files: list) -> dict:
    """Bytes por bucket (codigo/prosa/dados), LOC de codigo e razao original.
    Bounded: nao le arquivos > 512KB para LOC (marca-os so por bytes)."""
    bc = bp = bd = 0            # bytes codigo / prosa / dados
    loc = 0                     # linhas de codigo (arquivos <= 512KB)
    n_vend = 0
    for f in files:
        rel = f.strip('"')
        low = rel.lower()
        if any(v in low for v in VENDORED):
            n_vend += 1
        p = os.path.join(d, rel)
        try:
            sz = os.path.getsize(p)
        except OSError:
            continue
        e = os.path.splitext(rel)[1].lower()
        if e in CODE_EXT:
            bc += sz
            if sz <= 512 * 1024:
                try:
                    with open(p, "rb") as fh:
                        loc += fh.read().count(b"\n")
                except OSError:
                    pass
        elif e in PROSE_EXT:
            bp += sz
        else:
            bd += sz
    n = len(files) or 1
    return {
        "loc_codigo": loc,
        "kb_codigo": bc // 1024, "kb_prosa": bp // 1024, "kb_dados": bd // 1024,
        "arquivos_vendored": n_vend,
        "original_ratio": round(1 - n_vend / n, 3),
    }


def acervo_prova(resultados) -> str:
    """Selo do acervo: blake2b sobre as provas por repo, ordenadas (Merkle simples).
    EXCLUI o proprio Mapa (id='mapa'): a entrada auto-referente e RUNTIME e mudaria
    a cada commit do catalogo. Excluindo-a, o selo so muda se um dos OUTROS repos muda."""
    provas = sorted(r["triple"]["prova"] for r in resultados
                    if "triple" in r and r["id"] != "mapa")
    return _blake("|".join(provas))


def correlacoes(resultados) -> dict:
    """Indice invertido conceito -> repos que o evidenciam (mapa evolutivo)."""
    inv = defaultdict(list)
    for r in resultados:
        for c in r.get("conceitos_evidenciados", []):
            inv[c].append(r["id"])
    return {c: sorted(v) for c, v in sorted(inv.items())}


def origem_por_repo(r) -> tuple:
    """(n_codigo, n_prosa) — conceitos com evidencia em codigo vs em prosa."""
    org = r.get("evidencia_origem", {})
    cod = sum(1 for v in org.values() if "codigo" in v)
    pro = sum(1 for v in org.values() if "prosa" in v)
    return cod, pro


def resumo_origem(resultados) -> dict:
    tot = Counter()
    for r in resultados:
        for v in r.get("evidencia_origem", {}).values():
            tot[v] += 1
    return dict(tot)


def resumo_metricas(resultados) -> dict:
    loc = sum(r.get("metricas", {}).get("loc_codigo", 0) for r in resultados)
    kbc = sum(r.get("metricas", {}).get("kb_codigo", 0) for r in resultados)
    kbp = sum(r.get("metricas", {}).get("kb_prosa", 0) for r in resultados)
    kbd = sum(r.get("metricas", {}).get("kb_dados", 0) for r in resultados)
    return {"loc_codigo": loc, "kb_codigo": kbc, "kb_prosa": kbp, "kb_dados": kbd}


def base_dir() -> str:
    env = os.environ.get("MAPA_ACERVO_BASE")
    if env:
        return env
    # pasta-mae do repo Mapa (…/<base>/Mapa/codigo/este_arquivo)
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def rodar(base: str):
    return [escanear(rid, base) for rid in REPOS]


def relatorio(resultados, base) -> str:
    L = [f"varredura de conteudo :: base={base}",
         f"repos: {len(resultados)}  |  selo do acervo (prova): {acervo_prova(resultados)}",
         ""]
    L.append(f"{'id':<28} {'arq':>6}  {'cod/pro':>8}  conceitos evidenciados")
    for r in resultados:
        if "triple" not in r:
            L.append(f"{r['id']:<28} {'--':>6}  {'(sem git)':>8}  {r.get('erro','')}")
            continue
        cod, pro = origem_por_repo(r)
        L.append(f"{r['id']:<28} {r['arquivos']:>6}  {cod:>3}/{pro:<4}  "
                 + ",".join(r["conceitos_evidenciados"]))
    L.append("")
    L.append(f"evidencia por origem (conceito x repo): {resumo_origem(resultados)}")
    L.append(f"metricas totais: {resumo_metricas(resultados)}")
    L.append("")
    L.append("correlacoes (conceito -> repos que o evidenciam no conteudo):")
    for c, repos in correlacoes(resultados).items():
        L.append(f"  {c} ({len(repos)}): " + ", ".join(repos))
    return "\n".join(L)


def manifesto_yaml(resultados, base) -> str:
    """YAML escrito a mao (sem dependencia de PyYAML), determinista."""
    import datetime
    L = ["schema: mapa_manifesto_integridade_v1",
         "primeira_linha: 'DIGNIDADE-HUMANA / PROTECAO-INFANTIL (UDHR Art.1; UNCRC Art.3)'",
         f"gerado_por: codigo/varredura_conteudo.py",
         "metodo_triple: 'coerencia=blake2b(estrutura); integridade=git tree SHA; "
         "prova=blake2b(id|coerencia|integridade|head)'",
         f"selo_acervo_prova: {acervo_prova(resultados)}",
         "selo_nota: 'exclui a entrada auto-referente mapa (RUNTIME); estavel enquanto os "
         "outros repos nao mudarem'",
         "honestidade: 'conceitos_evidenciados = ocorrencia textual (FATO de ocorrencia), "
         "nao prova de implementacao correta'",
         "evidencia_origem_legenda: 'codigo = termo em fonte (implementado/mais forte); "
         "prosa = termo em .md/.txt/.tex (discutido); codigo+prosa = ambos'",
         "repos:"]
    for r in resultados:
        if "triple" not in r:
            L += [f"  - id: {r['id']}", f"    estado: {r.get('estado','LACUNA')}",
                  f"    erro: {r.get('erro','')}"]
            continue
        L += [
            f"  - id: {r['id']}",
            f"    dir: \"{r['dir']}\"",
            f"    head: {r['head']}",
            f"    arquivos: {r['arquivos']}",
            f"    conteudo_vivo: [{', '.join(r['conteudo_vivo'])}]",
            f"    coerencia: {r['triple']['coerencia']}",
            f"    integridade: {r['triple']['integridade']}",
            f"    prova: {r['triple']['prova']}",
            f"    conceitos_evidenciados: [{', '.join(r['conceitos_evidenciados'])}]",
            "    evidencia_origem: {"
            + ", ".join(f"{k}: {v}"
                        for k, v in sorted(r.get("evidencia_origem", {}).items()))
            + "}",
            "    metricas: {"
            + ", ".join(f"{k}: {v}" for k, v in r.get("metricas", {}).items())
            + "}",
            f"    estado: {r.get('estado', 'FATO')}",
        ]
    L.append("correlacoes:")
    for c, repos in correlacoes(resultados).items():
        L.append(f"  {c}: [{', '.join(repos)}]")
    L.append(f"evidencia_origem_totais: {resumo_origem(resultados)}")
    L.append(f"metricas_totais: {resumo_metricas(resultados)}")
    L.append(f"totais: {{repos: {len(resultados)}, "
             f"com_git: {sum(1 for r in resultados if 'triple' in r)}}}")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    base = base_dir()
    resultados = rodar(base)
    if argv is None:
        argv = sys.argv[1:]
    if "--write" in argv:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        out = os.path.join(root, "indices", "MANIFESTO_INTEGRIDADE.yaml")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(manifesto_yaml(resultados, base))
        sys.stderr.write(f"gravado: {out}\n")
    print(relatorio(resultados, base))
    faltando = [r["id"] for r in resultados if "triple" not in r]
    if faltando:
        sys.stderr.write("sem git (LACUNA): " + ", ".join(faltando) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
