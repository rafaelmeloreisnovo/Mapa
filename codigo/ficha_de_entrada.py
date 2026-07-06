#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ficha_de_entrada.py — codificacao coerente do modelo da camada biblioteconomica.

PRIMEIRA-LINHA: DIGNIDADE-HUMANA / PROTECAO-INFANTIL (ONU UDHR Art.1 / UNCRC Art.3).
Nenhuma ficha entra no mapa contra a vida ou a crianca.

Este modulo transforma o molde de `biblioteconomia/15_FICHA_DE_ENTRADA.md` em codigo
executavel, deterministico e sem dependencias (apenas stdlib). Ele:

  1. define o vocabulario fechado (substrato Lb0-Lb5, camadas L0-L5, Omega, marcas,
     conceitos C01-C17, grupamentos de no NG1-NG7);
  2. modela a Ficha e valida cada entrada (coerencia + honestidade + primeira linha);
  3. calcula uma coordenada Omega REPRODUTIVEL (mesma ficha -> mesma coordenada);
  4. traz os 28 repositorios ja mapeados como exemplos preenchidos;
  5. emite um relatorio e um JSON canonico (determinismo = invariante C01).

Uso:
    python3 codigo/ficha_de_entrada.py            # valida e imprime relatorio
    python3 codigo/ficha_de_entrada.py --json     # emite fichas.json canonico
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from dataclasses import dataclass, field, asdict

# --------------------------------------------------------------------------- #
# 1. Vocabulario fechado (autoridade). Alterar aqui = alterar o tesauro.
# --------------------------------------------------------------------------- #

SUBSTRATO = {                       # ver biblioteconomia/14_SUBSTRATO_BASE2.md
    "Lb0": "base-2 (bit: conduz/nao conduz)",
    "Lb1": "silicio/semicondutor (diodo, transistor B/C/E, current-leak, nm)",
    "Lb2": "eletromagnetismo (Tesla, bobina linear/radial/toroidal, spin)",
    "Lb3": "eletron/foton/plasma (corona, LED, UV, plasma-som, radiacao, SEU cosmico)",
    "Lb4": "quimica (tabela periodica, ions, osmose, pH, Van de Graaff)",
    "Lb5": "bio integrada (mitocondria, clorofila, bioeletricidade mV)",
}

CAMADAS = ["L0", "L1", "L2", "L3", "L4", "L5"]     # ver 07_ secao 2
OMEGA = "Omega { multidimensional . fractal }"     # topo geometrico

MARCAS = {"FATO", "HIPOTESE", "SIMBOLICO", "LACUNA"}   # regra de honestidade

CONCEITOS = {                       # ver 07_MATRIZ_DE_CONCEITOS.md (C01-C17)
    "C01": "Determinismo", "C02": "Invariante", "C03": "Hashing",
    "C04": "Custodia", "C05": "Assinatura", "C06": "Toroide-T7",
    "C07": "Atrator-42", "C08": "Phi", "C09": "ZIPRAF", "C10": "Vetor",
    "C11": "CientiEspiritual", "C12": "Verdade", "C13": "Etica",
    "C14": "Verbo-Vivo", "C15": "Universalismo", "C16": "LACUNA",
    "C17": "NO_GOOD",
}

# Grupamentos de no: id -> (nome, raio_normalizado_no_fractal_Omega)
# raio 0.0 = eixo central (NG7 cataloga tudo); ~1.0 = borda simbolica (NG6).
GRUPAMENTOS = {
    "NG7": ("meta-organizacao", 0.00),
    "NG1": ("nucleo-deterministico", 0.20),
    "NG2": ("plataforma-vm", 0.45),
    "NG3": ("cognicao-dados", 0.55),
    "NG4": ("ciencia-matematica", 0.65),
    "NG5": ("juridico-etico", 0.78),
    "NG6": ("espiritual-publicacao", 0.95),
}

PRIMEIRA_LINHA = "DIGNIDADE-HUMANA/PROTECAO-INFANTIL (UDHR Art.1; UNCRC Art.3)"


# --------------------------------------------------------------------------- #
# 2. Modelo
# --------------------------------------------------------------------------- #

@dataclass
class Ficha:
    """Uma entrada do 'livro de entrada' — do substrato base-2 ate Omega."""
    id: str
    objeto: str
    origem: str
    no_grupo: str                       # NG1..NG7
    camada_L: str                       # L0..L5
    conceitos: list                     # ["C01", ...]
    notacao: str                        # RAF.<Dom>.<Op>.<Dim>.<Est>
    marca: str                          # FATO|HIPOTESE|SIMBOLICO|LACUNA
    substrato: dict = field(default_factory=dict)   # {"Lb0": "...", ...}
    descritores: list = field(default_factory=list)
    relacoes: list = field(default_factory=list)
    ancora: str = ""                    # REFERENCE (ISO/NIST/RFC/ONU...)
    proxima_acao: str = ""              # obrigatorio se marca == LACUNA
    primeira_linha_ok: bool = True

    # --- coordenada Omega reprodutivel (determinismo = C01) --------------- #
    def _digest(self) -> bytes:
        canon = "|".join([
            self.id, self.no_grupo, self.camada_L,
            ",".join(sorted(self.conceitos)), self.notacao, self.marca,
        ])
        # blake2b: mesma linhagem de hashing do acervo (cf. BLAKE3), stdlib.
        return hashlib.blake2b(canon.encode("utf-8"), digest_size=8).digest()

    def omega_coord(self) -> dict:
        """Posicao geometrica no invariante Omega. Deterministica e reprodutivel."""
        d = self._digest()
        raio = GRUPAMENTOS[self.no_grupo][1]                 # raio do no-grupo
        theta = (int.from_bytes(d[:4], "big") % 3600) / 10.0  # angulo 0..360
        z = CAMADAS.index(self.camada_L) / (len(CAMADAS) - 1)  # altura 0..1 (L0..L5)
        # phi de coerencia em [0,1): assinatura reprodutivel da ficha
        phi = (int.from_bytes(d[4:], "big") % 100000) / 100000.0
        return {
            "raio": round(raio, 3),
            "theta_deg": round(theta, 1),
            "z_camada": round(z, 3),
            "phi": round(phi, 5),
            "x": round(raio * math.cos(math.radians(theta)), 4),
            "y": round(raio * math.sin(math.radians(theta)), 4),
        }


# --------------------------------------------------------------------------- #
# 3. Validacao (coerencia + honestidade + primeira linha)
# --------------------------------------------------------------------------- #

def validar(f: Ficha) -> list:
    """Retorna lista de problemas (vazia = coerente)."""
    p = []
    if not f.primeira_linha_ok:
        p.append(f"{f.id}: primeira_linha_ok=False (I1-I5 nao conferidos)")
    if f.marca not in MARCAS:
        p.append(f"{f.id}: marca invalida '{f.marca}'")
    if f.no_grupo not in GRUPAMENTOS:
        p.append(f"{f.id}: no_grupo invalido '{f.no_grupo}'")
    if f.camada_L not in CAMADAS:
        p.append(f"{f.id}: camada_L invalida '{f.camada_L}'")
    for c in f.conceitos:
        if c not in CONCEITOS:
            p.append(f"{f.id}: conceito desconhecido '{c}'")
    for k in f.substrato:
        if k not in SUBSTRATO:
            p.append(f"{f.id}: substrato desconhecido '{k}'")
    if not (f.notacao.startswith("RAF.") and f.notacao.count(".") == 4):
        p.append(f"{f.id}: notacao mal formada '{f.notacao}'")
    if f.marca == "LACUNA" and not f.proxima_acao:
        p.append(f"{f.id}: marca LACUNA exige proxima_acao (protecao da lacuna, I4)")
    if f.marca == "SIMBOLICO" and f.ancora and "REFERENCE" not in f.ancora:
        # simbolico pode ter ancora, mas nao deve alegar conformidade dura
        pass
    return p


# --------------------------------------------------------------------------- #
# 4. Os 28 ja mapeados, como exemplos preenchidos (o campo e maior).
#    Substrato preenchido nos casos em que o README o torna FATO/REFERENCE;
#    "-" onde nao se aplica (nao inventar).
# --------------------------------------------------------------------------- #

def _f(id, objeto, ng, L, conc, nota, marca, sub=None, desc=None,
       rel=None, anc="", prox=""):
    return Ficha(id=id, objeto=objeto, origem=f"{objeto} :: README",
                 no_grupo=ng, camada_L=L, conceitos=conc, notacao=nota,
                 marca=marca, substrato=sub or {}, descritores=desc or [],
                 relacoes=rel or [], ancora=anc, proxima_acao=prox)

EXEMPLOS = [
    # -------- NG1 nucleo --------
    _f("chipquantum", "ChipQuantum", "NG1", "L1", ["C01", "C03", "C06", "C07"],
       "RAF.CRP.EXEC.TEC.ATV", "FATO",
       sub={"Lb0": "branchless; execucao determinista bit-a-bit",
            "Lb1": "ARM32/64 (Termux)",
            "Lb2": "pipeline TOROIDAL de 42 estagios (forma de bobina/T7)"},
       desc=["Criptografia", "Determinismo", "Toroide", "Atrator-42"],
       rel=["SUSTENTA->custodia(C04)", "DERIVA->toroide(C06)"],
       anc="ISO/IEC 9899; NIST FIPS 180-4 (REFERENCE)"),
    _f("deepseek-rafcoder", "DeepSeek-RafCoder", "NG1", "L1", ["C01", "C05"],
       "RAF.RTM.EXEC.TEC.ATV", "FATO",
       sub={"Lb0": "kernel de estado determinista", "Lb1": "JNI/NDK ARM"},
       desc=["Runtime", "Determinismo", "Assinatura"],
       anc="ISO/IEC 9899 (REFERENCE)"),
    _f("gaia_phi", "GAIA_phi", "NG1", "L2", ["C01", "C03", "C04"],
       "RAF.RTM.ANALIS.TEC.ATV", "FATO",
       sub={"Lb0": "hashing reproduzivel", "Lb1": "nucleo C baixo overhead"},
       desc=["Determinismo", "Hashing", "Custodia"],
       anc="W3C PROV-O; ISO 15489 (REFERENCE)"),
    _f("blake3", "BLAKE3 (fork)", "NG1", "L1", ["C03", "C04"],
       "RAF.CRP.HASH.TEC.CAN", "FATO",
       sub={"Lb0": "arvore de Merkle paralelizavel"},
       desc=["Hashing", "Criptografia", "Custodia", "Fork"],
       anc="upstream BLAKE3; NIST FIPS 202 (REFERENCE)"),
    # -------- NG2 plataforma --------
    _f("rafgittools", "RafGitTools", "NG2", "L2", ["C01", "C02"],
       "RAF.PLT.BUILD.TEC.ATV", "FATO",
       sub={"Lb1": "build NDK/Gradle para ARM"},
       desc=["Determinismo", "Android-NDK", "Invariante"]),
    _f("vectras-vm-android", "Vectras-VM-Android", "NG2", "L2", ["C04"],
       "RAF.PLT.EMUL.TEC.CAN", "FATO",
       sub={"Lb1": "VM/engine nativo Android"},
       desc=["Virtualizacao", "Build", "Rastreabilidade"]),
    _f("termux-app-rafacodephi", "termux-app-rafacodephi (fork)", "NG2", "L2",
       [], "RAF.PLT.EXEC.TEC.ATV", "FATO",
       desc=["Plataforma", "Fork"], anc="upstream termux/termux-app GPLv3"),
    _f("termux-api_rafcodephi", "termux-api_rafcodephi (fork)", "NG2", "L2",
       [], "RAF.PLT.EXEC.TEC.CAN", "FATO",
       desc=["Plataforma", "Fork"], anc="upstream termux/termux-api"),
    _f("userland", "UserLAnd (fork)", "NG2", "L2", [],
       "RAF.PLT.EXEC.TEC.CAN", "FATO",
       desc=["Plataforma", "Virtualizacao", "Fork"],
       anc="upstream CypherpunkArmory/UserLAnd"),
    _f("pcr_rafaelia_code_seed", "PCR_Rafaelia_Code_seed (fork Magisk)", "NG2",
       "L2", ["C01"], "RAF.PLT.EXEC.TEC.ATV", "FATO",
       desc=["Plataforma", "Fork", "Determinismo"], anc="upstream topjohnwu/Magisk"),
    _f("qemu_rafaelia", "qemu_rafaelia (fork)", "NG2", "L2", [],
       "RAF.PLT.EMUL.TEC.CAN", "FATO",
       sub={"Lb1": "emulacao de CPU/ABI cross-arch"},
       desc=["Virtualizacao", "Emulacao", "Fork"], anc="upstream QEMU"),
    _f("actions", "actions (fork gradle/actions)", "NG2", "L2", [],
       "RAF.INF.BUILD.TEC.CAN", "FATO",
       desc=["Infraestrutura", "Build", "Fork"], anc="upstream gradle/actions"),
    # -------- NG3 cognicao --------
    _f("x0", "X0", "NG3", "L3", ["C10"], "RAF.IAC.ANALIS.TEC.ATV", "FATO",
       sub={"Lb0": "core C de baixo nivel", "Lb3": "quantica SIMULADA (nao fisica)"},
       desc=["Inteligencia-artificial", "Fractal", "Toroide"]),
    _f("llamarafaelia", "llamaRafaelia", "NG3", "L0", ["C02", "C08"],
       "RAF.IAC.ANALIS.MAT.SPEC", "HIPOTESE",
       desc=["Inteligencia-artificial", "Matematica", "Invariante"],
       rel=["TENSIONA->invariante(C02)"],
       anc="recursao Fibonacci-Rafael (HIPOTESE de originalidade)"),
    _f("conversations_chunks_private", "CONVERSATIONS_CHUNKS_PRIVATE", "NG3", "L2",
       ["C04", "C10"], "RAF.DAT.STORE.TEC.ATV", "FATO",
       desc=["Dados", "Custodia", "Vetor"],
       rel=["SUSTENTA->cognicao(C10)"], anc="ISO/IEC 25012 (REFERENCE)"),
    _f("home", "home (Sistema RAFAELIA)", "NG3", "L3", ["C04"],
       "RAF.IAC.ANALIS.CIE.ATV", "FATO",
       desc=["Analise", "Documentacao-cientifica", "Custodia"]),
    # -------- NG4 ciencia --------
    _f("relativity-living-light", "relativity-living-light (RLL)", "NG4", "L0",
       ["C02", "C08", "C14"], "RAF.FIS.PROV.CIE.CAN", "FATO",
       sub={"Lb4": "modelo cosmologico (materia/energia escura)"},
       desc=["Fisica", "Cosmologia", "Verbo-Vivo"],
       anc="DOI 10.5281/zenodo.17188137 (FATO); modelo = HIPOTESE cientifica"),
    _f("matem-tica-", "Matem-tica- (Forma Normal 123)", "NG4", "L0", ["C02"],
       "RAF.MTM.PROV.MAT.ATV", "FATO",
       desc=["Matematica", "Invariante"],
       anc="prova formal red(0^n 1123)=123 (REFERENCE interno)"),
    _f("papers", "papers (exacordex/raefaelos)", "NG4", "L1", ["C02", "C16"],
       "RAF.RTM.EXEC.TEC.SPEC", "LACUNA",
       desc=["Runtime", "LACUNA"],
       prox="expandir README.md descrevendo exacordex_*/raefaelos_*"),
    # -------- NG5 juridico --------
    _f("rafpolimata", "RafPolimata", "NG5", "L4", ["C07", "C13", "C06"],
       "RAF.JUR.GOVERN.JUR.ATV", "FATO",
       desc=["Direito", "Governanca", "Atrator-42", "Toroide"],
       rel=["SUSTENTA->etica(C13)"], anc="LGPD; ISO/IEC 42001 (REFERENCE)"),
    _f("rafaelia_private", "Rafaelia_Private (ZIPRAF_OMEGA)", "NG5", "L4",
       ["C13", "C05"], "RAF.RTM.GOVERN.TEC.ATV", "FATO",
       desc=["Governanca", "Etica", "Assinatura"],
       anc="Ethica[8]; 24+ standards (HIPOTESE de conformidade)"),
    _f("lgpd_constituicoes", "LGPD-Constituicoes-...", "NG5", "L4",
       ["C11", "C13", "C16"], "RAF.JUR.GOVERN.JUR.ATV", "LACUNA",
       desc=["Direito", "Etica", "CientiEspiritual", "LACUNA"],
       anc="LGPD 13.709; UDHR; UNCRC (REFERENCE)",
       prox="criar README.md de topo apontando para README_MASTER.md"),
    # -------- NG6 espiritual --------
    _f("livrovivo_thisbooklives", "LivroVivo_ThisBookLives", "NG6", "L5",
       ["C12", "C14", "C15", "C17"], "RAF.ESP.PUBL.ESP.CAN", "FATO",
       desc=["Verbo-Vivo", "Verdade", "Universalismo", "Assinatura"],
       rel=["EVOLUI->universalismo(C15)", "SUSTENTA->NO_GOOD(C17)"],
       anc="DOI 10.5281/zenodo.17187966; Ed25519 (FATO); doutrina = SIMBOLICO"),
    _f("blackhole", "Blackhole (CientiEspiritual)", "NG6", "L5",
       ["C09", "C11", "C14"], "RAF.ESP.PUBL.ESP.SPEC", "SIMBOLICO",
       desc=["CientiEspiritual", "ZIPRAF", "Verbo-Vivo"],
       rel=["TENSIONA->verdade(C12)"]),
    _f("publicacientiespiritual", "publicacientiespiritual", "NG6", "L5",
       ["C11", "C15"], "RAF.ESP.PUBL.ESP.CAN", "FATO",
       desc=["CientiEspiritual", "Universalismo"], anc="UNESCO Etica IA (REFERENCE)"),
    _f("zipraf_omega_full", "ZIPRAF_OMEGA_FULL", "NG6", "L5", ["C06", "C09", "C13"],
       "RAF.ESP.PUBL.ESP.ATV", "FATO",
       desc=["Toroide", "ZIPRAF", "Etica"],
       anc="OPTIMIZATION_LIBRARY/TRL; bibliografia (REFERENCE)"),
    # -------- NG7 meta --------
    _f("mapa", "Mapa (hub)", "NG7", "L2", ["C02", "C04", "C16"],
       "RAF.ORG.CATAL.TEC.ATV", "FATO",
       desc=["Organizacao-do-conhecimento", "Custodia", "Invariante"],
       rel=["PROTEGE->todos", "SUSTENTA->catalogo"],
       anc="ISO 25964; ISO 15836 Dublin Core (REFERENCE)"),
    _f("memrafcode", "MemRafcode", "NG7", "L2", ["C04", "C02", "C16"],
       "RAF.ORG.STORE.TEC.ATV", "FATO",
       desc=["Custodia", "Invariante", "Rastreabilidade"],
       rel=["SUSTENTA->reentrada"]),
]


# --------------------------------------------------------------------------- #
# 5. Relatorio e emissao
# --------------------------------------------------------------------------- #

def relatorio(fichas) -> str:
    linhas = [f"PRIMEIRA-LINHA: {PRIMEIRA_LINHA}",
              f"fichas: {len(fichas)}", ""]
    # por grupamento de no
    linhas.append("por grupamento de no (raio no Omega-fractal):")
    for ng, (nome, raio) in sorted(GRUPAMENTOS.items(), key=lambda kv: kv[1][1]):
        membros = [f.id for f in fichas if f.no_grupo == ng]
        linhas.append(f"  {ng} {nome:<22} r={raio:<4} ({len(membros)}): "
                      + ", ".join(membros))
    # por marca de honestidade
    linhas.append("")
    linhas.append("por marca de honestidade:")
    for m in sorted(MARCAS):
        ids = [f.id for f in fichas if f.marca == m]
        linhas.append(f"  {m:<10} ({len(ids)}): " + ", ".join(ids))
    # coordenada Omega de cada ficha
    linhas.append("")
    linhas.append("coordenada Omega (reprodutivel):")
    for f in fichas:
        c = f.omega_coord()
        linhas.append(f"  {f.id:<28} r={c['raio']:<5} theta={c['theta_deg']:>5}"
                      f"  z={c['z_camada']:<5} phi={c['phi']}")
    return "\n".join(linhas)


def canonico(fichas) -> str:
    """JSON canonico e determinista (ordenado) — invariante C01."""
    data = []
    for f in fichas:
        d = asdict(f)
        d["omega_coord"] = f.omega_coord()
        data.append(d)
    data.sort(key=lambda d: d["id"])
    return json.dumps({"primeira_linha": PRIMEIRA_LINHA, "fichas": data},
                      ensure_ascii=False, sort_keys=True, indent=2)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Ficha de entrada RAFAELIA (28).")
    ap.add_argument("--json", action="store_true", help="emite fichas.json canonico")
    args = ap.parse_args(argv)

    problemas = []
    for f in EXEMPLOS:
        problemas += validar(f)

    if args.json:
        print(canonico(EXEMPLOS))
    else:
        print(relatorio(EXEMPLOS))

    if problemas:
        sys.stderr.write("\nPROBLEMAS DE COERENCIA:\n  " + "\n  ".join(problemas) + "\n")
        return 1
    sys.stderr.write(f"\nOK: {len(EXEMPLOS)} fichas coerentes, 0 problemas.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
