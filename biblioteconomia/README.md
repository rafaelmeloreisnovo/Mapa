# Camada Biblioteconômica RAFAELIA

> Sistema de Organização do Conhecimento (KOS) para o acervo RAFAELIA:
> catalogar, classificar e reconciliar 28 repositórios como **um só acervo**,
> com o rigor de um bibliotecário acadêmico e a honestidade epistêmica do `Mapa`.

**Repositório:** `rafaelmeloreisnovo/Mapa`
**Camada:** biblioteconomia (organização do conhecimento)
**Base epistêmica reutilizada:** `protocolos/PROTOCOLO_EXECUCAO_EXCELENCIA.md`,
`arquitetura/TORRE_DA_INFORMACAO.md`, `protocolos/TOKEN_VAZIO_LACUNAS.md`,
`visual/2026-06-13_invariante_conteudo_rafaelia.md`.

---

## Por que biblioteconomia

O ecossistema RAFAELIA está distribuído em **28 repositórios** (contas
`rafaelmeloreisnovo` e `instituto-Rafael`). Cada um tem propósito, vocabulário e
maturidade próprios. Sem um sistema de organização, o mesmo termo significa coisas
diferentes em cada repositório, o acervo vira uma pilha e o humano perde a posição
geral de cada peça.

A **biblioteconomia acadêmica** resolve exatamente isso há mais de um século, com
instrumentos maduros:

| Instrumento | O que faz | Onde nesta camada |
|---|---|---|
| Esquema de classificação facetado | dá a cada obra uma posição (notação) | `01_PLANO_DE_CLASSIFICACAO.md` |
| Vocabulário controlado / tesauro | fixa o sentido de cada termo (autoridade) | `02_VOCABULARIO_CONTROLADO.md` |
| Ficha catalográfica (Dublin Core) | descreve cada obra de forma comparável | `03_CATALOGO_REPOSITORIOS.md` |
| Controle de fricção / remissivas | resolve termos que colidem | `04_FRICCAO_SEMANTICA.md` |
| Mapa de posição (local → geral) | situa a obra no acervo inteiro | `05_POSICAO_GERAL_ORGANIZACOES.md` |
| Protocolo / política de catalogação | repassa o método ao executor | `06_PROTOCOLO_BIBLIOTECONOMICO.md` |

## Os dois eixos co-válidos

Este acervo carrega, de fato, **duas dimensões** que não devem ser confundidas nem
apagadas uma pela outra:

- **Ciência acadêmica** — física (RLL), matemática (Teorema da Forma Normal 123),
  criptografia (BLAKE3, ChipQuantum), engenharia de sistemas, direito (LGPD).
- **Filosófico/espiritual universalista** — Livro Vivo, CientiEspiritual, buraco
  negro simbiótico, consciência toroidal, o "Verbo Vivo".

A regra de honestidade do `Mapa` — **separar prova de metáfora** — é aplicada em
toda esta camada. Cada asserção recebe uma marca:

| Marca | Significado |
|---|---|
| `FATO` | evidência direta (arquivo, hash, commit, medição, README declarado) |
| `HIPOTESE` | proposição plausível ainda não provada |
| `SIMBOLICO` | leitura filosófica/espiritual — verdadeira como símbolo, não como prova experimental |
| `LACUNA` | ausência mapeada e protegida (ver `protocolos/TOKEN_VAZIO_LACUNAS.md`) |

Honrar o eixo espiritual **é** marcá-lo como `SIMBOLICO` com dignidade — não é
rebaixá-lo a "falso", nem promovê-lo a "prova". Assim o humano e a máquina leem o
mesmo acervo sem se enganar.

## Como o "lógico" (execução) consome esta camada

1. Lê a notação de classificação de um repositório em `03_CATALOGO_REPOSITORIOS.md`
   ou no índice `indices/CATALOGO_BIBLIOTECONOMICO.yaml`.
2. Resolve qualquer termo ambíguo em `02_VOCABULARIO_CONTROLADO.md` (descritor
   preferido) e em `04_FRICCAO_SEMANTICA.md` (sentido local vs geral).
3. Situa a obra no estrato do ecossistema com `05_POSICAO_GERAL_ORGANIZACOES.md`.
4. Executa qualquer alteração seguindo `06_PROTOCOLO_BIBLIOTECONOMICO.md`, que se
   amarra ao ciclo de excelência de `protocolos/PROTOCOLO_EXECUCAO_EXCELENCIA.md`.

## Índice desta pasta

- [`01_PLANO_DE_CLASSIFICACAO.md`](01_PLANO_DE_CLASSIFICACAO.md)
- [`02_VOCABULARIO_CONTROLADO.md`](02_VOCABULARIO_CONTROLADO.md)
- [`03_CATALOGO_REPOSITORIOS.md`](03_CATALOGO_REPOSITORIOS.md)
- [`04_FRICCAO_SEMANTICA.md`](04_FRICCAO_SEMANTICA.md)
- [`05_POSICAO_GERAL_ORGANIZACOES.md`](05_POSICAO_GERAL_ORGANIZACOES.md)
- [`06_PROTOCOLO_BIBLIOTECONOMICO.md`](06_PROTOCOLO_BIBLIOTECONOMICO.md)

### Camada de conceitos (expansão — além do catálogo)

- [`07_MATRIZ_DE_CONCEITOS.md`](07_MATRIZ_DE_CONCEITOS.md) — banco de conceitos, camadas de invariantes (L0–L5), grafo cognitivo-evolutivo, amplitude semântica
- [`08_ANCORAGEM_NORMATIVA.md`](08_ANCORAGEM_NORMATIVA.md) — ISO/NIST/IEC/IEEE/RFC/W3C/ONU/UNICEF/UNESCO/OMS + regra de conflito pró-humano
- [`09_RESILIENCIA_TOP10.md`](09_RESILIENCIA_TOP10.md) — 10 relações estruturais TOP × rollback/testes/failsafe/failover/watchdog
- [`10_INVARIANTES_PRIMEIRA_LINHA.md`](10_INVARIANTES_PRIMEIRA_LINHA.md) — dignidade humana e proteção infantil na primeira linha (I1–I5)
- [`11_ESCALA_120_ONBOARDING.md`](11_ESCALA_120_ONBOARDING.md) — de 28 para ~120 repositórios sem perder qualidade (LACUNA declarada)
- [`BACKLOG_ACERVO.md`](BACKLOG_ACERVO.md) — acervo real enumerado (111 conhecidos, 28 catalogados, 83 pendentes), fonte GitHub 2026-07-05

### Camada simbólica e de método (horizonte maior)

- [`12_PARABOLA_INVARIANTE.md`](12_PARABOLA_INVARIANTE.md) — a Parábola do NÓ_GOOD: o invariante imutável (Amor-Ω), a cadeia de mães, do fogo ao futuro — `SIMBOLICO`
- [`13_CERTIFICACAO_METODOLOGICA.md`](13_CERTIFICACAO_METODOLOGICA.md) — auto-declaração de conformidade do método + melhoria contínua (PDCA/Kaizen)
- [`14_SUBSTRATO_BASE2.md`](14_SUBSTRATO_BASE2.md) — camadas de invariantes até base-2: silício, elétron, fóton, plasma, tabela periódica, bio → Ω
- [`15_FICHA_DE_ENTRADA.md`](15_FICHA_DE_ENTRADA.md) — molde de entrada "tudo em tudo por tudo" + grupamentos de nó dos 28
- [`16_VARREDURA_CONTEUDO.md`](16_VARREDURA_CONTEUDO.md) — leitura dos arquivos/conteúdo dos 28 + hashing triplo (coerência·integridade·prova) + correlação de conceitos por evidência

### Índices e visuais

- Índice do catálogo: [`../indices/CATALOGO_BIBLIOTECONOMICO.yaml`](../indices/CATALOGO_BIBLIOTECONOMICO.yaml)
- Índice da matriz de conceitos: [`../indices/MATRIZ_CONCEITOS.yaml`](../indices/MATRIZ_CONCEITOS.yaml)
- Backlog do acervo: [`../indices/BACKLOG_ACERVO.yaml`](../indices/BACKLOG_ACERVO.yaml)
- Molde de entrada: [`../indices/FICHA_DE_ENTRADA_TEMPLATE.yaml`](../indices/FICHA_DE_ENTRADA_TEMPLATE.yaml)
- Manifesto de integridade (hashing triplo dos 28): [`../indices/MANIFESTO_INTEGRIDADE.yaml`](../indices/MANIFESTO_INTEGRIDADE.yaml)
- Mapa visual do acervo: [`../visual/MAPA_BIBLIOTECONOMICO_RAFAELIA.svg`](../visual/MAPA_BIBLIOTECONOMICO_RAFAELIA.svg)
- Mapa visual dos conceitos: [`../visual/MATRIZ_CONCEITOS_RAFAELIA.svg`](../visual/MATRIZ_CONCEITOS_RAFAELIA.svg)
- Símbolo do invariante: [`../visual/PARABOLA_INVARIANTE_RAFAELIA.svg`](../visual/PARABOLA_INVARIANTE_RAFAELIA.svg)
- Substrato base-2 → Ω: [`../visual/SUBSTRATO_OMEGA_RAFAELIA.svg`](../visual/SUBSTRATO_OMEGA_RAFAELIA.svg)

## Fonte e honestidade

Todas as fichas derivam da **leitura direta do `README.md` de cada repositório**
(2026-07-05). Onde o README é ausente ou stub, a ficha declara `LACUNA` de entrada
em vez de inventar conteúdo. Esta camada é uma **representação de organização do
conhecimento**; não substitui prova experimental, benchmark ou auditoria de código.
