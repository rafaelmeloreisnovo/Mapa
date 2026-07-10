> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — a varredura lê conteúdo para servir à verdade e à vida; nenhum dado é usado contra a dignidade ou a criança (ONU UDHR Art.1 · UNCRC Art.3).

# 16 — Varredura de Conteúdo + Hashing Triplo (coerência · integridade · prova)

> Passo além do README: entrar nos **arquivos e no conteúdo vivo** dos 28 repositórios
> já mapeados, reconhecer os conceitos por **evidência textual real** (não só pelo nome),
> e selar cada obra com **três hashes** — um sistema de coerência, integridade e prova.
>
> Ferramenta: [`../codigo/varredura_conteudo.py`](../codigo/varredura_conteudo.py).
> Resultado (snapshot datado): [`../indices/MANIFESTO_INTEGRIDADE.yaml`](../indices/MANIFESTO_INTEGRIDADE.yaml).

## Escopo e honestidade

- **Somente os 28** já mapeados (o avesso), clonados localmente. Não lê repos fora de escopo.
- **Determinista**: a mesma árvore produz exatamente os mesmos três selos (verificado:
  o manifesto é idêntico em execuções repetidas).
- **Evidência ≠ prova de implementação**: `conceitos_evidenciados` = o termo do vocabulário
  **aparece no conteúdo** (`FATO` de ocorrência textual). Não afirma que o conceito está
  corretamente implementado — para isso seria preciso auditoria (`09_` R07).

## O hashing triplo

Para cada repositório, três selos com papéis distintos (todos reprodutíveis):

| Selo | O que prova | Como é calculado |
|---|---|---|
| **coerência** | a **forma** (estrutura de arquivos) | `blake2b(lista ordenada de `git ls-files`)` |
| **integridade** | os **bytes** (conteúdo) | **git tree SHA** do HEAD — o próprio Merkle root do git |
| **prova** | o **selo que amarra** forma + bytes | `blake2b(id \| coerência \| integridade \| head)` |

E um **selo do acervo**: `blake2b` sobre as provas ordenadas dos repositórios — muda se
**qualquer** um deles mudar. **Exceção deliberada:** exclui a entrada auto-referente do
próprio `Mapa` (marcada `RUNTIME`), cujo selo mudaria a cada commit do catálogo; sem ela,
o selo do acervo é **estável** e só reflete mudanças reais no conteúdo catalogado. É o
"sistema de coerência/integridade/prova" pedido, em três níveis (estrutura → conteúdo →
vínculo → acervo).

> Por que git tree SHA para integridade: o git **já** mantém um Merkle root do conteúdo
> versionado. Reaproveitá-lo é honesto (é a integridade real do que está commitado),
> rápido (não re-hashea gigabytes) e verificável por qualquer `git rev-parse HEAD^{tree}`.
> Reforça o conceito C03 (Hashing) e C04 (Custódia) com prova externa.

## Conteúdo vivo e correlação evolutiva de conceitos

- **Conteúdo vivo**: as 6 extensões mais presentes por repositório (o que o repo
  *realmente* é por dentro — ex.: ChipQuantum `.c/.h/.sh`, home `.py/.c`, LGPD `.tex`).
- **Correlações**: um índice invertido **conceito → repositórios que o evidenciam**. É o
  mapa de conceitos evolutivo: mostra onde cada invariante (C01–C17) aparece de fato no
  código/texto do acervo — o alicerce para revisão de publicação e classificação por
  evidência.

Exemplos de leitura do snapshot atual (`MANIFESTO_INTEGRIDADE.yaml`):

- **Custódia (C04)** aparece nos **28** — é o tecido comum do acervo (todo repo fala de
  digest/manifesto/proveniência).
- **CientiEspiritual (C11)** concentra-se no cinturão espiritual/jurídico e cognitivo.
- **Universalismo (C15)** é o mais raro (poucos repos) — pista de onde o eixo L5 está
  textualmente ancorado.
- **NÓ_GOOD (C17)** aparece por co-ocorrência textual ("no good"/"amor") — `HIPOTESE` de
  relevância, a confirmar em contexto (exemplo de por que evidência textual não é prova).

## Como isto evolui o modelo (knows-by-evolution)

1. A ficha de entrada (`15_`) tinha `conceitos` **declarados** (do README, HIPOTESE de nome).
2. A varredura entrega `conceitos_evidenciados` (do conteúdo, FATO de ocorrência).
3. A **correlação** dos dois (declarado × evidenciado) é o próximo teste: onde declarei um
   conceito que não aparece no conteúdo, ou onde o conteúdo revela conceito não declarado —
   cada divergência vira uma revisão de publicação registrada (PDCA de `13_`).

## Rodar

```bash
python3 codigo/varredura_conteudo.py            # relatório (triple + correlações)
python3 codigo/varredura_conteudo.py --write     # grava indices/MANIFESTO_INTEGRIDADE.yaml
python3 -m unittest codigo/test_varredura_conteudo -v
# base do acervo configuravel: MAPA_ACERVO_BASE=/caminho python3 codigo/varredura_conteudo.py
```

Estado verificado (2026-07-05): **28 repos lidos, 28 com git; manifesto determinista
(idêntico em 2 execuções); selo do acervo estável**.

## Léxico refinado (melhoria contínua aplicada)

Após a primeira revisão (`17_AVALIACAO_CONTEUDO.md`), os termos-âncora foram afinados **sem
baixar a régua**: `universalis`→`universal` (C15), `living-light` além de `living light`
(C14), e C07 qualificado (`atrator`/`attractorpool`/`42 atratores`, evitando o "42" nu).
Re-execução: RISCOs de declaração-sem-evidência caíram de **3 para 1** (o residual é um link
conceitual, não textual — ver `17_`).

> **Propriedade importante:** refinar a *lente* de conceitos **não altera** nenhum triple-hash
> por repositório (coerência/integridade/prova derivam de `git ls-files`/tree, não do grep).
> Lente semântica e prova de integridade são camadas independentes.

## Evidência em código vs em prosa (granularidade aplicada)

O manifesto agora distingue, por conceito e por repo, **onde** a evidência está:

| origem | significado | força |
|---|---|---|
| `codigo` | termo em arquivo-fonte (`.c/.py/.rs/.sh/…`) | **implementado** (mais forte) |
| `prosa` | termo em `.md/.rst/.txt/.tex` | **discutido** (mais fraco) |
| `codigo+prosa` | ambos | implementado e documentado |

Campo `evidencia_origem` por repo em `indices/MANIFESTO_INTEGRIDADE.yaml`.

**Achado que valida os estratos** (`05_POSICAO_GERAL_ORGANIZACOES.md`): o núcleo evidencia
mais em **código**; o eixo espiritual, mais em **prosa** — exatamente como a teoria previa.

| Estrato | só-código | só-prosa | ambos |
|---|---|---|---|
| NG1 núcleo (ChipQuantum, DeepSeek, GAIA, BLAKE3) | 3 | 10 | 44 |
| NG6 espiritual (LivroVivo, Blackhole, publica…, ZIPRAF) | 1 | 20 | 30 |

O núcleo tem mais conceitos só-código (o código **prova**); o espiritual, o dobro de
só-prosa (a prosa **discute**). Totais do acervo: `codigo+prosa` 296, `prosa` 68, `codigo` 25.

## Próxima ação

- Cruzamento declarado × evidenciado: **codificado e rodando** em `codigo/revisao_publicacao.py`
  → `indices/REVISAO_PUBLICACAO.md`.
- Usar `evidencia_origem` para reforçar a marca epistêmica: **feito** em
  `codigo/marca_epistemica.py` → `indices/MARCA_EPISTEMICA.md` (32 reforços, 3 candidatos a
  `HIPOTESE`). Ver o balanço geral em `18_ROADMAP_ESTADO.md`.
