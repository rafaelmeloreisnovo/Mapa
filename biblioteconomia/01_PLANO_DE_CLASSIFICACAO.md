# 01 — Plano de Classificação Facetada RAFAELIA

> Esquema facetado no estilo **Ranganathan (PMEST)**, afinado ao ecossistema
> RAFAELIA, com **ponte cruzada para a CDU** (Classificação Decimal Universal)
> para interoperar com bibliotecas acadêmicas reais.

## Princípio

Uma classificação facetada não força cada obra numa gaveta única. Ela descreve a
obra por **facetas independentes** e compõe uma **notação** a partir delas. Isso é
mais fiel a um acervo híbrido (código + ciência + direito + espírito) do que uma
árvore rígida.

As cinco facetas fundamentais de Ranganathan (PMEST) são adaptadas assim:

| PMEST | Nome original | Faceta RAFAELIA | Pergunta que responde |
|---|---|---|---|
| **P** | Personality | **Domínio** | Do que a obra trata, essencialmente? |
| **M** | Matter | **Substrato** | Em que matéria/tecnologia se realiza? |
| **E** | Energy | **Operação** | O que a obra faz (ação principal)? |
| **S** | Space | **Âmbito** | Onde vive (conta, origem, acesso)? |
| **T** | Time | **Maturidade** | Em que estado de vida está? |

E uma **faceta transversal** obrigatória, que é a marca do acervo:

| — | **Dimensão epistêmica (D)** | Sob que regime de verdade a obra fala? |

---

## Faceta P — Domínio

| Código | Domínio |
|---|---|
| `CRP` | Criptografia / hashing |
| `RTM` | Runtime / núcleo determinístico de baixo nível |
| `IAC` | Inteligência artificial / cognição |
| `DAT` | Dados / corpus |
| `FIS` | Física / cosmologia |
| `MTM` | Matemática |
| `JUR` | Direito / normativo |
| `ESP` | Espiritual / publicação simbólica |
| `PLT` | Plataforma / SO / virtualização |
| `INF` | Infraestrutura / CI / build |
| `ORG` | Meta / organização do conhecimento |

## Faceta M — Substrato

`C-ASM` (C/assembly freestanding) · `RUST` · `PY` (Python) · `AND` (Android/NDK/Java) ·
`JS` · `DOC` (prosa/documentação) · `DAT` (dados/binário) · `MIX` (múltiplos).

## Faceta E — Operação

`HASH` · `COMP` (compilar) · `EXEC` (executar runtime) · `EMUL` (emular) ·
`BUILD` (CI/empacotar) · `ANALIS` (analisar) · `PROV` (provar) · `PUBL` (publicar) ·
`GOVERN` (governar/compliance) · `STORE` (armazenar/custódia) · `CATAL` (catalogar).

## Faceta S — Âmbito (registrada em campo, não na notação)

- Conta: `RMN` (rafaelmeloreisnovo) · `IRF` (instituto-Rafael)
- Origem: `ORIG` (original) · `FORK` (fork de upstream — declarar o upstream)
- Acesso: `PUB` (público) · `PRIV` (privado)

## Faceta T — Maturidade (estados de vida)

Reaproveita os estados do `Mapa` mais um grau de maturidade:

| Código | Estado |
|---|---|
| `CAN` | canônico / consolidado |
| `ATV` | ativo / em desenvolvimento |
| `PROT` | protótipo |
| `SPEC` | especificação / pesquisa |
| `LAC` | LACUNA (entrada ausente ou stub) |

## Faceta D — Dimensão epistêmica (transversal, marca do acervo)

| Código | Regime de verdade |
|---|---|
| `CIE` | científico (evidência experimental/observacional) |
| `MAT` | matemático (prova formal) |
| `TEC` | técnico-instrumental (engenharia, reprodutibilidade) |
| `JUR` | jurídico (norma, tratado, constituição) |
| `ESP` | espiritual/simbólico (leitura filosófica universalista) |

Uma obra pode carregar **mais de uma** dimensão; a notação usa a **primária** e a
ficha lista as demais. Toda dimensão `ESP` é lida sob a regra `SIMBOLICO` (ver
`README.md` desta pasta).

---

## Notação

```
RAF.<Domínio>.<Operação>.<Dimensão>.<Maturidade>
```

Exemplos (derivados do catálogo):

| Repositório | Notação | Leitura |
|---|---|---|
| BLAKE3 | `RAF.CRP.HASH.TEC.CAN` | criptografia, hashear, técnico, canônico (fork) |
| ChipQuantum | `RAF.CRP.EXEC.TEC.ATV` | cripto/runtime freestanding, técnico, ativo |
| relativity-living-light | `RAF.FIS.PROV.CIE.CAN` | física/cosmologia, provar, científico, canônico (DOI) |
| Matem-tica- | `RAF.MTM.PROV.MAT.ATV` | matemática, provar, matemático, ativo |
| RafPolimata | `RAF.JUR.GOVERN.JUR.ATV` | jurídico-semântico, governar, jurídico, ativo |
| LivroVivo_ThisBookLives | `RAF.ESP.PUBL.ESP.CAN` | publicação, publicar, espiritual, canônico (DOI) |
| Mapa | `RAF.ORG.CATAL.TEC.ATV` | organização, catalogar, técnico, ativo |

## Ponte cruzada para a CDU

Para interoperar com bibliotecas acadêmicas, cada domínio recebe uma âncora CDU
aproximada (`HIPOTESE` de correspondência; a CDU oficial deve prevalecer em contexto
formal):

| Domínio RAFAELIA | CDU aproximada | Área CDU |
|---|---|---|
| `CRP` | 004.056.55 | Criptografia / segurança |
| `RTM` | 004.31 | Arquitetura / execução de baixo nível |
| `IAC` | 004.8 | Inteligência artificial |
| `DAT` | 004.65 | Dados / bases de dados |
| `FIS` | 52/53 | Astronomia / física |
| `MTM` | 51 | Matemática |
| `JUR` | 34 | Direito |
| `ESP` | 1 / 2 | Filosofia / Religião |
| `PLT` | 004.451 | Sistemas operacionais / virtualização |
| `INF` | 004.415.5 | Build / integração |
| `ORG` | 025.4 | Organização do conhecimento / classificação |

> Nota de escopo: a CDU é usada aqui como **ponte de interoperabilidade**, não como
> classificação primária. A notação primária do acervo é a facetada `RAF.*`.
