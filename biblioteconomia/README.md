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
- Índice legível por máquina: [`../indices/CATALOGO_BIBLIOTECONOMICO.yaml`](../indices/CATALOGO_BIBLIOTECONOMICO.yaml)
- Mapa visual: [`../visual/MAPA_BIBLIOTECONOMICO_RAFAELIA.svg`](../visual/MAPA_BIBLIOTECONOMICO_RAFAELIA.svg)

## Fonte e honestidade

Todas as fichas derivam da **leitura direta do `README.md` de cada repositório**
(2026-07-05). Onde o README é ausente ou stub, a ficha declara `LACUNA` de entrada
em vez de inventar conteúdo. Esta camada é uma **representação de organização do
conhecimento**; não substitui prova experimental, benchmark ou auditoria de código.
