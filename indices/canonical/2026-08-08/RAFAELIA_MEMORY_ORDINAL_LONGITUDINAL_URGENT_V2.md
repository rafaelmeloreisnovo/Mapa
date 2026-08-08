# RAFAELIA — Modelo de Memória Ordinal × Longitudinal × Urgente V2

**Data de corte:** 2026-08-08T17:24:00-03:00  
**Estado:** `CANONICAL_DRAFT`  
**Modo:** `APPEND_ONLY / NON_DESTRUCTIVE / PROVENANCE_FIRST`  
**Política:** `claim_allowed=false` por padrão

## 0. Objetivo

Unificar três funções que antes existiam separadamente no `Mapa`:

1. **Memória ordinal** — responde *onde este objeto está na linhagem verificável*.
2. **Memória longitudinal** — responde *como este objeto persiste e evolui entre sessões, fontes, snapshots e receipts*.
3. **Memória urgente** — responde *qual lacuna deve ser fechada primeiro e qual gate produz a evidência de fechamento*.

A nova camada não substitui os artefatos V1. Ela cria uma ponte compatível e fail-closed.

## 1. Invariante do modelo

```text
SOURCE
  ↓ provenance
ORDINAL NODE ──────→ position / lineage
  ↓
LONGITUDINAL LINK ─→ predecessor / checkpoint / cursor / receipt
  ↓
URGENT ITEM ───────→ priority / risk / next_gate / closure_contract
  ↓
EVIDENCE + RECEIPT
  ↓
REVISION APPEND
```

Regras:

```text
ordem ≠ verdade
persistência ≠ evidência
prioridade ≠ sucesso
checkpoint ≠ payload
implementação ≠ execução
estimativa ≠ medição
TOKEN_VAZIO ≠ zero
CLOSED_PASS(urgência) ≠ claim_allowed=true automático
```

## 2. As três coordenadas

### 2.1 Coordenada ordinal `O`

```text
O = [epoch, source, artifact, claim, evidence, revision]
```

Serve para navegação e comparação dentro de uma linhagem comprovada. A ordem nunca é usada como proxy de validade.

### 2.2 Coordenada longitudinal `L`

```text
L = (
  source_identity,
  predecessor,
  checkpoint,
  cursor,
  observed_at,
  source_hash,
  derived_hash,
  receipt
)
```

Campos desconhecidos permanecem `null`/`TOKEN_VAZIO`; não são inferidos a partir do nome do arquivo.

### 2.3 Coordenada urgente `U`

```text
U = (
  urgent_id,
  priority,
  priority_basis,
  state,
  category,
  problem,
  risk,
  next_gate,
  closure_contract
)
```

`priority_basis` separa prioridade herdada da fonte, prioridade computada e override explícito de governança.

## 3. Função de composição

```text
MEMORY_OBJECT = O ⊕ L ⊕ U
```

Nem todo objeto possui as três coordenadas materializadas.

- sem `O`: `TOKEN_VAZIO_LINEAGE`;
- sem `L`: continuidade não comprovada;
- sem `U`: objeto não está na fila operacional;
- sem evidence/receipt: `claim_allowed=false`.

A ausência de uma coordenada é estado válido e auditável.

## 4. Memória urgente como fila de fechamento

A memória urgente não duplica corpus nem transforma o `Mapa` em task manager genérico. Ela é uma **projeção de gaps verificáveis**.

Estados normalizados:

```text
OPEN
TESTABLE
RUNNING
BLOCKED_EXTERNAL
CLOSED_PASS
CLOSED_FAIL
ARCHIVED
```

Prioridades:

```text
P0 = segurança, integridade, custódia ou bloqueio estrutural crítico
P1 = gate estrutural necessário para continuidade confiável
P2 = redução relevante de incerteza
P3 = melhoria não bloqueante
P4 = arquivo/observação
```

Se não houver score medido, `urgency_score=null` e a base deve registrar `TOKEN_VAZIO_METRIC`. A classe herdada não autoriza inventar um número.

## 5. Closure contract obrigatório

Todo item urgente deve possuir:

```text
expected_evidence
closure_test
receipt_required=true
```

Fechamento exige evidência observável. `CLOSED_PASS` fecha a pendência operacional, mas **não promove automaticamente o claim upstream**.

## 6. Privacidade e federação

O `Mapa` mantém projeções minimizadas.

Proibido na projeção pública:

- corpo de conversas;
- perfil de usuário;
- mídia privada;
- segredo;
- URL/ID de Drive privado quando não necessário;
- inferência de identidade por nome;
- cópia de bases pesadas.

Permitido:

- IDs semânticos públicos;
- categorias de gap;
- prioridades;
- gates;
- hashes/receipts já destinados à auditoria;
- ponteiros sanitizados.

O validador de memória urgente rejeita URL de Drive privado em entradas marcadas `drive_private_sanitized`.

## 7. Gates unificados

```text
G0 SOURCE_DISCOVERED
G1 IDENTITY_PROVENANCE
G2 BYTE_INTEGRITY_PARSE
G3 ORDINAL_LINEAGE
G4 LONGITUDINAL_CHECKPOINT
G5 JOIN_DEDUP_SEMANTICS
G6 EXECUTION_EVIDENCE
G7 PROMOTION_REVIEW
```

Qualquer gate pode gerar um `URGENT_ITEM`. O item só fecha quando o `closure_contract` produz receipt.

## 8. Fila urgente inicial sanitizada

Artefato:

```text
data/memory/urgent-memory.public.v1.jsonl
```

A primeira projeção contém 8 itens:

- 4 × P0;
- 4 × P1;
- 0 claims promovidos;
- scores numéricos não inventados.

Ela integra:

- incidente P0 já presente na memória ordinal;
- lacunas de medição, hash, tokenizer, receipts, joins, proveniência e evidência de execução registradas no ledger longitudinal privado;
- somente referências públicas ou sanitizadas no repositório.

## 9. Relação com os artefatos existentes

```text
indices/canonical/2026-08-07/RAFAELIA_ORDINAL_MEMORY_FOREST_V1.md
  └─ posição e linhagem

auditoria/memoria_longitudinal/RAFAELIA_LONGITUDINAL_MEMORY_PUBLIC_RECEIPT_V1_2026-08-05.md
  └─ estado público longitudinal e gaps de materialização

indices/memoria-longitudinal/*
  └─ ponteiros federados e snapshots minimizados

data/memory/urgent-memory.public.v1.jsonl
  └─ fila operacional de fechamento
```

## 10. Validação

```bash
python3 tools/validate_ordinal_memory.py data/memory/ordinal-memory.seed.v1.jsonl
python3 tools/validate_urgent_memory.py data/memory/urgent-memory.public.v1.jsonl
python3 -m unittest tests.test_urgent_memory
```

Critério de gate:

```text
schema parse PASS
+ ordinal validator PASS
+ urgent validator PASS
+ urgent negative tests PASS
= STRUCTURAL_PASS
```

`STRUCTURAL_PASS` não equivale a runtime/produção/validade científica.

## 11. Próxima expansão sem regressão

1. adicionar links urgentes a nós ordinais somente quando `semantic_id`/`ordinal_path` forem observáveis;
2. produzir receipts de fechamento append-only;
3. materializar a matriz de cobertura longitudinal `source→hash→normalized→chunks→graph→memory→receipt`;
4. resolver `TOKEN_VAZIO_LINEAGE` antes de impor ordem;
5. manter o `Mapa` como índice/federação, não como duplicador de corpus privado.

## 12. Invariante 7×7 de navegação

| Vetor | Pergunta | Evidência mínima | Falha válida | Saída |
|---|---|---|---|---|
| Proveniência | de onde veio? | source ref/hash | TOKEN_VAZIO_PROVENANCE | link |
| Identidade | o que é? | semantic id/hash | TOKEN_VAZIO_IDENTITY | node |
| Ordem | onde está? | parent + ordinal path | TOKEN_VAZIO_LINEAGE | O |
| Continuidade | o que precede/sucede? | checkpoint/cursor | PARTIAL | L |
| Evidência | o que sustenta? | receipt/test | NOT_PROVEN | evidence |
| Urgência | o que fecha primeiro? | priority basis | TOKEN_VAZIO_METRIC | U |
| Promoção | pode virar claim? | gates completos | BLOCKED | decision |

## 13. Retroalimentação

`F_ok`: ordinalidade, continuidade e urgência passam a ter papéis distintos e interligáveis.  
`F_gap`: a fila urgente ainda é projeção; os gaps precisam de execução/receipts para fechar.  
`F_next`: executar primeiro os P0 testáveis e anexar receipts sem transformar ausência em sucesso.
