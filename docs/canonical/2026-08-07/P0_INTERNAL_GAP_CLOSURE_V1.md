# RAFAELIA — P0 Internal Gap Closure V1

**Data:** 2026-08-07  
**Modo:** `APPEND_ONLY / FAIL_CLOSED / CLAIM_ALLOWED=false`  
**Autoridade:** `rafaelmeloreisnovo/Mapa`

## Objetivo

Reduzir os cinco gaps internos priorizados sem criar nova camada conceitual:

1. reconciliação GitHub ↔ Drive;
2. proveniência Poincaré / fórmulas;
3. geometria V/E/F;
4. política numérica;
5. corpus no escopo evidenciado.

A regra é **zero lacuna anônima**, não zero lacuna artificialmente preenchida.

## 1. Reconciliação cross-surface

Artefato: `data/reconciliation/cross_surface_reconciliation_p0.v1.jsonl`.

Foram presos por `provider_id`, path e SHA de objeto Git os documentos centrais do método, contrato de conclusão, IGC, auditoria Poincaré e matriz de rastreabilidade. Representações Google Docs e Markdown não precisam ser byte-idênticas; a invariante é núcleo canônico + lineage + estado explícito.

**Estado:** `REDUCED_CORE_ANCHORS_RECONCILED_REMAINDER_TYPED`.

## 2. Poincaré / proveniência

Artefato: `data/provenance/poincare_formula_provenance.v1.json`.

Ficaram separados:

```text
Poincare-ball embedding != Poincare return map != Poincare conjecture
```

A fonte privada de 64 blocos foi localizada por repositório, commit, path e blob SHA. Os 64 `raw_block_id` receberam esquema ordinal estável. O contrato `FORM-*`, sua função de hash, a contagem de 486 fórmulas e o SHA-256 esperado de `formulas.json` também foram presos.

O join `RAW -> FORM-* -> object_id` **não é inventado**: os bytes canônicos de `formulas.json` não estão materializados no repo/release observado. O vazio genérico foi convertido em dependência objetiva e falsificável.

**Estado:** `REDUCED_SOURCE_AND_BLOCK_IDENTITY_CLOSED_FORM_JOIN_BLOCKED`.

## 3. Geometria V/E/F

Artefato: `data/geometry/piramide_triedrica_dupla_candidates.v1.json`.

- `G1`: fixture combinatória base-base, `V=5`, `E=9`, `F=6`, Euler externo `2`;
- `G2`: fixture ápice-ápice, `V=7`, `E=12`, `F=8`, junção central em vértice;
- `G3`: preservado como `TOKEN_VAZIO_TYPED_ABSTRACT_ONLY`;
- fixture negativa: aresta pendente que deve falhar.

`G1` é referência de teste, **não escolha autoral**. A seleção exata exige evidência de fonte/imagem/medição.

**Estado:** `REDUCED_CANDIDATE_VEF_MATERIALIZED_EXACT_SELECTION_EXTERNALIZED`.

## 4. Política numérica

Artefato: `data/numerics/numeric_policy.v1.json`.

Políticas explícitas para:

- combinatória inteira exata;
- geometria `binary64`;
- replay ARM `binary32`;
- Q16/fixed-point.

Cada uma declara tolerância, arredondamento, overflow e regra fail-closed. Epsilon de engenharia não é tratado como incerteza física.

**Estado:** `CLOSED_GOVERNANCE_NUMERIC_POLICY_MATERIALIZED`.

## 5. Corpus

Artefato: `data/corpus/corpus_manifest_p0.v1.json`.

O lote Ω7 já evidenciado contém:

```text
arquivos observados = 62.822
arquivos com hash   = 62.821
resíduo de hash     = 1
```

O manifesto prende inventário CSV, relation graph, SQLite de auditoria, receipt, fontes P0 e estados de privacidade/licença. Não declara cobertura de todo o Google Drive.

**Estado:** `REDUCED_SCOPED_CORPUS_GOVERNED_SINGLE_HASH_RESIDUAL_TYPED`.

## Validação

- `tools/validate_p0_internal_gap_closure.py`
- `tests/test_p0_internal_gap_closure.py`

O validador exige:

- V/E/F e Euler coerentes para G1;
- G3 sem V/E/F inventado;
- fixture negativa realmente inválida;
- política numérica fail-closed;
- 64 raw IDs completos;
- FORM join bloqueado sem bytes canônicos;
- escopo do corpus sem sobreclaim;
- cinco anchors de reconciliação sem pointer anônimo.

## Resíduos que deixam de ser internos genéricos

```text
exact_glue_selection
  -> TOKEN_VAZIO_TYPED_SOURCE_EVIDENCE_REQUIRED

RAW -> FORM join
  -> BLOCKED_CANONICAL_FORMULAS_JSON_BYTES

Omega7 missing hash
  -> TOKEN_VAZIO_TYPED_SINGLE_HASH_RESIDUAL

physical ARM execution
  -> BLOCKED_EXTERNAL_PHYSICAL_RUNTIME

independent replay
  -> BLOCKED_EXTERNAL_INDEPENDENT_REPLAY
```

O próximo ciclo técnico deve atacar o mismatch `CLASS <-> CAMB` como erro de backend/convencao reproduzível, sem aumentar tolerância para forçar PASS. Depois disso, evidência ARM física e reprodução independente continuam fora do alcance de simulação interna.

## R3

- **F_ok:** cinco gaps internos possuem artefatos, locators, estados e falsificadores verificáveis.
- **F_gap:** bytes canônicos de `formulas.json`, escolha geométrica autoral, um hash do corpus Ω7, mismatch CLASS/CAMB, runtime físico e replay independente.
- **F_next:** rodar CI desta branch; corrigir somente falhas reais; em seguida atacar CLASS/CAMB pelo primeiro ponto de divergência.
