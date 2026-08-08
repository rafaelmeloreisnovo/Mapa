# RAFAELIA — Memória Ordinal em Floresta V1

**Data de corte:** 2026-08-07T21:47:00-03:00  
**Estado:** `CANONICAL_DRAFT`  
**Política:** `claim_allowed=false` por padrão  
**Modo:** append-only, não destrutivo, provenance-first  
**Autoridade metodológica:** `indices/RAFAELIA_IMPLEMENTACAO_LATENTES_PAPERS_V1.md`  
**Predecessor:** `indices/canonical/2026-07-30/FCEA_CORE_MEMORY_NONORDINAL_INDEX_V1.md`

## 0. Objetivo

Adicionar uma camada **ordinal** à memória relacional já existente, sem destruir a memória não ordinal.

A memória não ordinal preserva relações, aliases, hashes, linhagens e topologia. A memória ordinal acrescenta uma coordenada estável de navegação para responder:

1. o que veio antes/depois dentro de uma cadeia verificável;
2. de qual fonte um claim depende;
3. qual lacuna bloqueia qual artefato;
4. qual `TOKEN_VAZIO` deve ser fechado primeiro;
5. qual evidência promove ou falsifica um claim;
6. qual revisão substitui outra sem apagar histórico;
7. onde um vetor semântico se ramifica em uma floresta de entradas.

A ordem **não significa verdade**. Significa posição auditável.

## 1. Invariante de sustentação

```text
Fonte → Índice → Token Semântico → Claim → Evidência/Falsificador
      → Decisão → Artefato → Receipt → Retroalimentação
```

Regras invioláveis:

```text
ordem ≠ validade
nome ≠ identidade
cópia ≠ versão
implementação ≠ execução
execução ≠ evidência
ausência ≠ zero
TOKEN_VAZIO ≠ falha inventada
metáfora ≠ claim físico
```

## 2. Coordenada ordinal

Cada nó recebe duas identidades:

- `semantic_id`: identidade estável do objeto/conceito;
- `ordinal_path`: posição local em sua linhagem.

Formato:

```text
ordinal_path = [epoch, source, artifact, claim, evidence, revision]
```

Todos os componentes são inteiros não negativos. Comparação ordinal só é válida quando os nós compartilham a mesma linhagem ancestral relevante.

Exemplo:

```text
[1, 4, 2, 7, 0, 0]  claim sem evidência fechada
[1, 4, 2, 7, 1, 0]  primeira evidência
[1, 4, 2, 7, 2, 0]  segundo teste/falsificador
[1, 4, 2, 7, 2, 1]  revisão do mesmo registro
```

Nunca reutilizar um `ordinal_path` removido. Revisões são append-only.

## 3. Floresta de memória

A unidade de crescimento deixa de ser uma lista plana e passa a ser uma floresta direcionada acíclica por linhagem de custódia.

```text
ROOT      = domínio/projeto
TRUNK     = fonte canônica ou corpus
BRANCH    = artefato, conceito, módulo ou dataset
NODE      = claim ou decisão testável
LEAF      = evidência, falsificador, receipt ou observação
SEED      = TOKEN_VAZIO com teste de fechamento definido
FRUIT     = artefato promovido por gate explícito
```

Um objeto pode participar de mais de uma árvore por arestas semânticas, mas possui uma única linhagem de custódia primária.

## 4. Vetor mínimo por nó

```text
v = (
  provenance,
  semantics,
  evidence,
  reproducibility,
  dependency,
  contradiction,
  security,
  freshness,
  uncertainty,
  urgency
)
```

Cada eixo de qualidade usa intervalo `[0,1]` e deve possuir `measurement_basis`.

### 4.1 Incerteza

A incerteza é calculada por lacunas observáveis, não por impressão:

```text
uncertainty =
  0.20*(1-provenance) +
  0.15*(1-semantics) +
  0.25*(1-evidence) +
  0.15*(1-reproducibility) +
  0.10*contradiction +
  0.10*(1-security) +
  0.05*(1-freshness)
```

`uncertainty=0` só é permitido se todos os componentes forem medidos e fechados. Campo não medido produz `TOKEN_VAZIO_METRIC`, nunca zero implícito.

### 4.2 Urgência

Urgência prioriza fechamento, não dramatização:

```text
priority_base =
  0.35*impact +
  0.25*blockage +
  0.20*risk +
  0.10*staleness +
  0.10*dependency_centrality

urgency = round(100 * priority_base * (0.5 + 0.5*uncertainty))
```

Classes:

```text
P0 = 80..100  segurança, perda de custódia ou bloqueio crítico
P1 = 60..79   fecha gate estrutural
P2 = 40..59   reduz incerteza relevante
P3 = 20..39   melhoria não bloqueante
P4 = 0..19    arquivo/observação
```

## 5. TOKEN_VAZIO como semente fechável

Todo `TOKEN_VAZIO` deve conter:

```text
token_vazio_id
reason
blocked_claims[]
missing_object
expected_evidence
closure_test
owner_domain
priority
created_at
last_checked_at
status
```

Estados permitidos:

```text
OPEN → TESTABLE → RUNNING → CLOSED_PASS
                         ↘ CLOSED_FAIL
                         ↘ BLOCKED_EXTERNAL
```

Proibido converter `OPEN` diretamente em `CLOSED_PASS` sem evidência anexada.

## 6. Arestas permitidas

```text
DERIVED_FROM
DUPLICATES
ALIASES
DEPENDS_ON
SUPPORTS
FALSIFIES
CONTRADICTS
REPLACES
EXECUTED_BY
PRODUCES
BLOCKED_BY
CLOSES_TOKEN_VAZIO
```

Cada aresta deve carregar `source`, `observed_at`, `confidence` e, quando aplicável, hash/receipt.

## 7. Gate de promoção

Um nó só pode mudar `claim_allowed=false → true` quando:

1. fonte rastreável;
2. identidade resolvida;
3. semântica definida;
4. evidência específica presente;
5. falsificador declarado ou justificadamente não aplicável;
6. reprodução compatível com o tipo de claim;
7. riscos de segurança/governança tratados;
8. limitações declaradas;
9. receipt ou registro de decisão anexado.

Se algum requisito obrigatório estiver ausente:

```text
claim_allowed=false
status=TOKEN_VAZIO | BLOCKED | PARTIAL
```

## 8. Estratégia de redução de lacunas

Ordem operacional padrão:

```text
P0 segurança/custódia
→ identidade/proveniência
→ duplicidade/alias
→ execução/receipt
→ evidência/falsificador
→ reprodução
→ integração semântica
→ publicação
```

Isso evita gastar computação refinando um ramo cuja raiz ainda é incerta.

## 9. Compatibilidade com memória não ordinal

O arquivo predecessor continua válido como fotografia relacional. Esta V1 não o reescreve.

Conversão:

```text
NONORDINAL_NODE
  + primary_parent
  + append_event_number
  + revision
  + uncertainty_vector
  + closure_contract
= ORDINAL_FOREST_NODE
```

Quando `primary_parent` não puder ser determinado, registrar:

```text
primary_parent = null
status = TOKEN_VAZIO_LINEAGE
```

## 10. Floresta de entrada operacional

Toda nova entrada passa por sete filtros antes de entrar no corpus principal:

1. **proveniência** — de onde veio;
2. **identidade** — o que é e se é duplicata/alias;
3. **semântica** — qual conceito representa;
4. **evidência** — o que sustenta;
5. **falsificabilidade** — como pode falhar;
6. **custódia/segurança** — o que pode ser exposto/executado;
7. **destino** — qual árvore, branch, claim ou paper recebe a entrada.

Entrada sem filtro suficiente vai para `SEED/TOKEN_VAZIO`, não é descartada nem promovida.

## 11. Artefatos desta implementação

```text
indices/canonical/2026-08-07/RAFAELIA_ORDINAL_MEMORY_FOREST_V1.md
schemas/ordinal-memory-node.schema.json
data/memory/ordinal-memory.seed.v1.jsonl
```

## 12. Primeiro ciclo de migração

- preservar o índice não ordinal como origem;
- registrar o método canônico Drive ↔ GitHub como raiz de autoridade;
- transformar gaps conhecidos em `SEED` com contrato de fechamento;
- priorizar incidentes de segurança/custódia como P0;
- não promover nenhuma alegação histórica apenas por ter sido importada;
- adicionar ordinalidade somente onde a linhagem for observável;
- usar `TOKEN_VAZIO_LINEAGE` onde a ordem ainda não puder ser provada.

## 13. Critério de excelência operacional

```text
EXCELLENCE =
  provenance
  × auditability
  × reproducibility
  × uncertainty_reduction
  × safe_execution
  × semantic_cohesion
```

Produto multiplicativo: um eixo zerado bloqueia promoção, em vez de ser escondido pela média dos demais.

## 14. Retroalimentação

`F_ok`: memória relacional preservada e camada ordinal definida sem reescrita retroativa.  
`F_gap`: migração integral do universo ainda não executada; linhagens sem fonte/receipt permanecem `TOKEN_VAZIO`.  
`F_next`: validar schema, ingerir sementes prioritárias, produzir receipts de fechamento e só então expandir a floresta.
