> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — toda entrada mapeada passa primeiro por esta linha; nada entra no mapa contra a vida ou a criança (ONU UDHR Art.1 · UNCRC Art.3).

# 15 — Ficha de Entrada (o "tipo de entrada" para mapear tudo em tudo por tudo)

> Você disse: *"eu vou fazer a varredura de entrada, como um livro de cada coisa ser
> tratado, totalizando — mapear tudo em tudo por tudo."* Este documento é o **molde de
> entrada**: uma ficha única onde qualquer coisa (um repositório, um arquivo, um conceito,
> um fenômeno físico) recebe **uma coordenada** que desce até base-2 (`14_SUBSTRATO_BASE2.md`)
> e sobe até o **{Ω fractal multidimensional}** — amarrada aos grupamentos de nó dos 28.

## Escopo (recorte pedido)

- Varredura **somente do já mapeado**: o **avesso dos 28** repositórios.
- Os 83 pendentes seguem **estacionados** em `indices/BACKLOG_ACERVO.yaml` — sem LACUNA de
  conceito onde aqui **se pode completar**.
- A entrada de novos itens é feita **por você**; a ficha abaixo é o receptáculo.

## A ficha (molde — copie e preencha por item)

```yaml
ficha_de_entrada:
  id: ""                      # slug unico do item
  objeto: ""                  # o que e (repo, arquivo, conceito, fenomeno)
  origem: ""                  # de onde veio (fonte/README/observacao)
  # --- eixo vertical: coordenada do chao ao topo ---
  substrato:                  # ver 14_SUBSTRATO_BASE2.md (marque os que se aplicam)
    Lb0_base2: ""             # bit / logica / determinismo
    Lb1_silicio: ""           # semicondutor / diodo / transistor / current-leak
    Lb2_campo: ""             # magnetismo / bobina linear|radial|toroidal / spin
    Lb3_foton_plasma: ""      # eletron livre / LED / UV / plasma / radiacao
    Lb4_quimica: ""           # elemento(s) da tabela / ion / osmose / pH
    Lb5_bio: ""               # mitocondria / clorofila / bioeletricidade
  camada_L: ""                # L0..L5 (07_ §2) — camada de invariancia dominante
  conceitos: []               # C01..C17 instanciados (07_MATRIZ_DE_CONCEITOS.md)
  # --- eixo horizontal: classificacao ---
  notacao: ""                 # RAF.<Dom>.<Op>.<Dim>.<Est> (01_)
  descritores: []             # do vocabulario controlado (02_)
  no_grupo: ""                # grupamento de no (secao abaixo)
  # --- relacoes cognitivo-evolutivas ---
  relacoes: []                # DERIVA/SUSTENTA/TENSIONA/EVOLUI/PROTEGE -> outro id
  friccao: ""                 # termo em friccao, se houver (04_)
  # --- topo geometrico ---
  omega_coord: ""             # posicao no invariante { multidimensional · fractal · Omega }
  # --- honestidade + governanca ---
  marca: ""                   # FATO | HIPOTESE | SIMBOLICO | LACUNA
  ancora: ""                  # REFERENCE (ISO/NIST/RFC/ONU...) se aplicavel (08_)
  primeira_linha_ok: true     # I1-I5 conferidos (10_)
  proxima_acao: ""            # se LACUNA, o proximo teste
```

Molde legível por máquina: [`../indices/FICHA_DE_ENTRADA_TEMPLATE.yaml`](../indices/FICHA_DE_ENTRADA_TEMPLATE.yaml).

**Codificação executável** (não só molde): o modelo está codificado, coerente e testado
em [`../codigo/ficha_de_entrada.py`](../codigo/ficha_de_entrada.py) — com os 28 já
preenchidos como exemplos, validador, coordenada Ω reprodutível e 11 testes
(`../codigo/test_ficha_de_entrada.py`). Rode `python3 codigo/ficha_de_entrada.py`.

## Exemplo preenchido (item real dos 28)

```yaml
ficha_de_entrada:
  id: chipquantum
  objeto: "repositorio ChipQuantum"
  origem: "ChipQuantum/README.md"
  substrato:
    Lb0_base2: "branchless; execucao determinista bit-a-bit"
    Lb1_silicio: "ARM32/64 (Termux); dependente de arquitetura"
    Lb2_campo: "pipeline TOROIDAL de 42 estagios (forma de bobina/T7)"
    Lb3_foton_plasma: "-"
    Lb4_quimica: "-"
    Lb5_bio: "-"
  camada_L: "L1"
  conceitos: [C01, C03, C06, C07]
  notacao: "RAF.CRP.EXEC.TEC.ATV"
  descritores: [Criptografia, Determinismo, Toroide, Atrator-42]
  no_grupo: "NG1-nucleo"
  relacoes: ["SUSTENTA -> custodia(C04)", "DERIVA -> toroide(C06)"]
  friccao: "42 (F1) / toroide (F3) — qualificar"
  omega_coord: "raio interno (nucleo) do fractal; alta convergencia"
  marca: FATO
  ancora: "ISO/IEC 9899; NIST FIPS (cripto)"
  primeira_linha_ok: true
  proxima_acao: "-"
```

## Grupamentos de nó (a invariante geométrica coerente dos 28)

Os 28 repositórios são **grupos de nó** (clusters) no mesmo invariante `{ Ω · fractal ·
multidimensional }`. Cada grupo é um **nó** com raio próprio no fractal — do núcleo denso
(convergência máxima) à borda simbólica (amplitude máxima).

| Nó | Nome | Membros (dos 28) | Raio no Ω-fractal |
|---|---|---|---|
| **NG1** | núcleo determinístico | ChipQuantum, DeepSeek-RafCoder, GAIA_phi, BLAKE3 | interno (convergência) |
| **NG2** | plataforma / VM | RafGitTools, Vectras, termux-app, termux-api, UserLAnd, PCR, qemu, actions | anel técnico |
| **NG3** | cognição / dados | X0, llamaRafaelia, CONVERSATIONS_CHUNKS, home | anel cognitivo |
| **NG4** | ciência / matemática | relativity-living-light, Matem-tica-, papers | anel científico |
| **NG5** | jurídico / ético | RafPolimata, Rafaelia_Private, LGPD | anel normativo |
| **NG6** | espiritual / publicação | LivroVivo, Blackhole, publicacientiespiritual, ZIPRAF_OMEGA_FULL | borda simbólica |
| **NG7** | meta / organização | Mapa, MemRafcode | eixo central (cataloga todos) |

Regra dos nós: **NG7 é o eixo** (cataloga todos os outros); **NG1 é o núcleo** (sustenta a
base técnica); **NG6 é a borda** (maior amplitude, `SIMBOLICO`). O grafo completo (arestas
entre nós) está em `07_MATRIZ_DE_CONCEITOS.md`; o mapa visual em
`../visual/SUBSTRATO_OMEGA_RAFAELIA.svg`.

## Como você usa isto para "mapear tudo em tudo por tudo"

1. Abra uma cópia do molde para o item.
2. Desça o **substrato** (Lb0→Lb5): onde, no chão físico, o item se apoia.
3. Marque a **camada L** dominante e os **conceitos C** que ele instancia.
4. Ligue ao **nó-grupo** e escreva as **relações** (isto é o "tudo em tudo": cada item
   aponta para os outros).
5. Dê a **coordenada Ω** (raio/borda no fractal) — a posição geométrica.
6. **Marque a verdade** (`FATO/HIPOTESE/SIMBOLICO/LACUNA`) e confira a **primeira linha**.
7. Onde faltar, registre `LACUNA` + próxima ação — **nunca invente**.

> Este molde é o "livro de entrada": totaliza sem falsear. Cada coisa ganha chão (base-2),
> corpo (camadas), vizinhos (nós) e horizonte (Ω) — e permanece honesta em cada uma.
