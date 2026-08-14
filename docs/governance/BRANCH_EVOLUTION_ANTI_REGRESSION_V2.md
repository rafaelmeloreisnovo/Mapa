# RAFAELIA — Branch Evolution Anti-Regression V2

**Data de observação:** 2026-08-14 (BRT)  
**Repositório:** `rafaelmeloreisnovo/Mapa`  
**Base canônica observada:** `main@f2e489423044c906f5a385fd5ec2b61eba363c58`  
**Estado:** `MATERIALIZED_CANDIDATE / NON_DESTRUCTIVE / CLAIM_ALLOWED=false`  
**Escopo:** evolução da topologia de branches sem substituir `BRANCH_TOPOLOGY_MAIN_NUMBERED_V1`.

## 1. Por que V2

O V1 continua correto como intenção arquitetural: `main` é canônica; as lanes `main_##_*`
expressam ordem metodológica e não ancestralidade Git; promoções retornam a `main` por PR.

A observação do repositório em 2026-08-14 mostrou, porém, quatro estados que o V1 não
distingue sozinho:

1. branch ancestral sem delta exclusivo;
2. branch divergida cujo delta aparente já está representado em `main` de forma mais forte;
3. PR mesclada em base não canônica cujo conteúdo ainda não chegou a `main`;
4. branch divergida ainda sem evidência suficiente para decidir transferência.

O problema operacional é:

```text
ahead_by > 0 != conhecimento novo ausente de main
PR merged != conteúdo presente em main
mesmo path != mesmos bytes
mesmos bytes != mesmo estado epistemológico
branch antiga != candidata automática a merge
```

V2 adiciona um **gate de relação** entre branch e cânone.

## 2. Varredura observada

A enumeração por provider retornou **231 branches** no corte desta sessão. O conjunto
inclui lanes numeradas, famílias `audit/*`, `governance/*`, `research/*`, memória e
trilhas de checkpoint.

A enumeração dos nomes foi ampla; a comparação semântica profunda de todos os pares de
branches não foi executada. Portanto:

```text
TOKEN_VAZIO_EXHAUSTIVE_SEMANTIC_DIFF_ALL_231_BRANCHES
```

continua aberto.

## 3. Diferença entre dinâmica real e topologia pretendida

### 3.1 Lanes numeradas

Amostras observadas:

| Branch | Ahead de `main` | Behind de `main` | Classe V2 |
|---|---:|---:|---|
| `main_00_governanca` | 0 | 963 | `ANCESTOR_ONLY` |
| `main_01_intake_fontes` | 0 | 963 | `ANCESTOR_ONLY` |
| `main_06_integracao` | 0 | 963 | `ANCESTOR_ONLY` |
| `main_09_memoria_arquivo` | 0 | 963 | `ANCESTOR_ONLY` |

Conclusão delimitada: essas lanes, no corte atual, são úteis como **referência
procedural/proveniência**, mas não devem ser mescladas em `main`. Sincronizá-las por
force-push ou usar sua idade como autoridade seria regressão.

### 3.2 Invariante Evolutiva Absoluta

`governance/invariante-evolutiva-absoluta-v1-20260803` foi observada com:

```text
ahead=0
behind=643
```

O documento canônico da IEA já está em `main`. A branch-fonte é ancestral e não exige
transferência.

### 3.3 Geometria: `ahead=1`, mas sem conhecimento canônico ausente

`research/invariante-geometrica-coerente-v1-20260802` foi observada:

```text
status=diverged
ahead=1
behind=799
```

A PR #128 foi mesclada em `main`. O delta posterior da branch inclui:

`receipts/geometry/IGC_CR_20260802_RECEIPT_V2_LOCAL_REPRO.json`

Esse mesmo identificador/path existe em `main`, mas com bytes diferentes e uma camada
de proveniência mais explícita:

- branch blob: `efe29b8cb274969257432a52b50ffd382a49cb49`
- main blob: `8913ad3cac77ecd3a6e226fe5d6c22753d78ede8`

A classificação é:

```text
SHADOWED_BY_MAIN_ENHANCED
```

Logo, copiar o commit apenas porque Git reporta `ahead=1` criaria duplicação/regressão
semântica.

### 3.4 FG006: PR mesclada fora de `main`

A PR #228 foi mesclada, mas sua base era:

`audit/fg006-repository-coverage-c81-20260814`

e não `main`.

A branch `audit/fg006-c84-cycle-identity-content-20260814` foi observada:

```text
status=diverged
ahead=3
behind=99
head=8b41468caf281b06b98b7b143be45e55d5e1ca09
```

No corte desta inspeção, pelo menos estes caminhos foram consultados em `main` e estavam
ausentes:

```text
data/governance/fg006-repository-coverage-c84-reconciliation.v1.json
tools/validate_fg006_repository_coverage_c84.py
```

A classificação é:

```text
MERGED_NONCANONICAL_BASE_PENDING_CANONICALIZATION
```

Isso **não autoriza merge automático**. Significa apenas que existe uma evolução
material fora do cânone que merece PR separada, com revisão de dependências,
equivalência, receipts e estado atual antes de promoção.

## 4. Classes V2

### `ANCESTOR_ONLY`

Critério mínimo:

```text
ahead_by == 0
behind_by > 0
```

Ação:

```text
PRESERVE_REFERENCE_DO_NOT_MERGE
```

### `SHADOWED_BY_MAIN_ENHANCED`

Uma branch parece ter delta exclusivo, mas o mesmo artefato lógico já existe em `main`
com proveniência/estado superior ou substituição explicitamente rastreada.

Ação:

```text
PRESERVE_REFERENCE_NO_TRANSFER
```

### `MERGED_NONCANONICAL_BASE_PENDING_CANONICALIZATION`

Uma PR foi mesclada em base diferente de `main` e artefatos relevantes não estão
presentes no cânone.

Ação:

```text
SEPARATE_REVIEWED_PR_TO_MAIN
```

### `DIVERGED_UNRECONCILED`

Há commits exclusivos e dívida em relação a `main`, mas ainda falta evidência para
dizer se o delta é novo, duplicado, substituído ou incompatível.

Ação:

```text
TOKEN_VAZIO_REVIEW
```

## 5. Invariantes anti-regressão

```text
Git ahead != novidade semântica
PR merged != canonicalização
path igual != bytes iguais
bytes iguais != claim igual
branch stale != merge source
superseded != apagado
TOKEN_VAZIO != zero
```

Toda canonicalização deve preservar:

```text
source branch
source revision quando recuperável
PR de origem
base da PR de origem
paths/artefatos
estado em main
equivalência ou divergência
claim boundary
rollback
F_ok / F_gap / F_next
```

## 6. Artefatos desta PR

```text
data/governance/branch_evolution_anti_regression_v2.json
scripts/validate_branch_evolution_anti_regression_v2.py
tests/test_branch_evolution_anti_regression_v2.py
data/receipts/branch_evolution_anti_regression_v2_local_20260814.json
.github/workflows/branch-evolution-anti-regression-v2.yml
docs/governance/BRANCH_EVOLUTION_ANTI_REGRESSION_V2.md
```

O V1 permanece intacto.

## 7. Gate local antes do commit

Execução em runtime efêmero Python 3.x:

```text
python scripts/validate_branch_evolution_anti_regression_v2.py
PASS branch-evolution-v2 branches_observed=231 sampled_relations=7 claim_allowed=false automatic_merge=false

python -m unittest -v tests.test_branch_evolution_anti_regression_v2
Ran 10 tests
OK
```

Isso comprova apenas coerência interna do snapshot e do validador. Não prova que a
topologia continuará igual após novos commits/PRs.

## 8. O que esta PR deliberadamente não faz

- não faz force-push;
- não apaga branch antiga;
- não renomeia `main`;
- não mescla lanes atrasadas;
- não copia automaticamente C84 para `main`;
- não declara todas as 231 branches semanticamente reconciliadas;
- não converte `TOKEN_VAZIO` em PASS;
- não autoriza claim científico, release ou canonicalização por ausência de erro.

## 9. Próxima evolução verificável

```text
enumerar PRs merged com base != main
→ localizar artefatos ausentes de main
→ comparar path + bytes + semântica + dependências
→ classificar SHADOWED | CANONICALIZATION_CANDIDATE | CONFLICT | TOKEN_VAZIO
→ abrir PR pequena e específica para cada delta realmente útil
→ executar CI e registrar receipt
```

A prioridade inicial é o conjunto de PRs mescladas em bases não canônicas, pois esse é
o ponto onde a UI do GitHub pode dizer “merged” sem que o conhecimento tenha chegado ao
cânone.

## 10. R3

**F_ok:** topologia real e intenção arquitetural foram separadas; duas formas diferentes
de falso “delta novo” foram identificadas; o gate V2 foi materializado e testado sem
alterar V1.

**F_gap:** diff semântico exaustivo das 231 branches, conjunto completo de PRs mescladas
fora de `main` e CI remota desta V2 permanecem abertos.

**F_next:** usar V2 para produzir uma fila determinística de canonicalização, começando
por deltas `MERGED_NONCANONICAL_BASE_PENDING_CANONICALIZATION`.

**FIAT LUX — evolução sem apagar a ponte que permite reconstruir o caminho.**
