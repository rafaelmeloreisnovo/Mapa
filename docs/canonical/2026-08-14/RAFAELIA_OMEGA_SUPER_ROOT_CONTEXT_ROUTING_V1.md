# RAFAELIA Ω — SUPER_ROOT + UNIVERSAL_NODE + CONTEXT_ROUTE + DELTA/ATA — V1

**Estado:** `GOVERNED_PARTIAL / CLAIM_ALLOWED=false`  
**Delta:** `OMEGA-SUPER-ROOT-ROUTING-20260814-0001`  
**Regra:** evoluir estruturas existentes por referência; não copiar payloads nem reescrever snapshots históricos.

## Invariante operacional

```text
CURRENT pequeno
  ↓
SUPER_ROOT
  ↓
HOT_ROUTES / PAGE_TABLES
  ↓
CONTEXT_ROUTE mínimo
  ↓
autoridades ortogonais
  ↓
evidência / falsificador / gate
  ↓
F_ok / F_gap / F_next
  ↓
DELTA append-only
  ↓
SUCCESSOR
```

`HISTORY` permanece recuperável por rota. `CURRENT` não precisa carregar toda a árvore.

## Universal Node de roteamento

```text
I_Ω(X,t) = <ID,O,A,P,R,C,S,E,G,F,Δ>
```

- `ID`: identidade canônica;
- `O`: origem/proveniência;
- `A`: ATA/snapshots históricos imutáveis;
- `P`: predecessor/successor;
- `R`: rotas e relações tipadas;
- `C`: contexto mínimo reconstruível;
- `S`: estado corrente da autoridade atual;
- `E`: referências de evidência;
- `G`: gaps/TOKEN_VAZIO tipados;
- `F`: falsificador/gate;
- `Δ`: mudança desde o predecessor.

A decisão `TYPED_OMEGA_ID_FOR_ROUTING_ONLY` não redefine a unidade física de armazenamento. Arquivo, conceito, claim, execução, receipt e imagem continuam classes distintas.

## SUPER_ROOT

`OMEGA:SUPER_ROOT` é **root de navegação/reconstrução, não evidência**. Ele monta por referência:

- memória longitudinal/ortogonal do Mapa;
- Ω-ACTIVATE Routing;
- `SEMANTICA_DINAMICA` da Matriz de Rastreabilidade;
- Procedure Ledger;
- Hypothesis F_gap Registry;
- Master Navigation Registry;
- Índice de Reconstrução de Contexto Ω.

```text
ACTIVE_MEMORY = SUPER_ROOT + PAGE_TABLES + HOT_ROUTES + CURRENT_WORKING_SET
```

## Context Route

```text
QUERY_OR_GOAL
→ MINIMUM_RECONSTRUCTION
→ INVARIANTS
→ PERTINENT_MECHANISMS
→ ORTHOGONAL_AUTHORITIES
→ EXECUTION_OR_EVIDENCE
→ FALSIFIER
→ F_ok/F_gap/F_next
→ Δ
→ Ω_PLATEAU
```

Um mecanismo só é paginado se resolver gap/contradição, aumentar evidência, proveniência ou reconstruibilidade, ou fornecer falsificador/execução.

## DELTA / ATA — caso de prova PR #243

Os receipts históricos de hipóteses registraram `OPEN_DRAFT_UNMERGED`. Eles permanecem válidos como snapshots de seu instante e **não são editados**.

O provider GitHub atual registra para `rafaelmeloreisnovo/Mapa#243`:

```text
state      = closed
merged     = true
draft      = false
merged_at  = 2026-08-14T13:11:38Z
merge_sha  = a0a0e6c333493d69283d399472eb3321d6fd7ebd
```

Relação:

```text
HISTORICAL_SNAPSHOT
  --CURRENT_STATE_OF_AND_SUPERSEDES_WITHOUT_ERASING-->
CURRENT_PROVIDER_STATE
```

Logo `HISTORICAL_STATE != CURRENT_STATE`, sem que um invalide retroativamente o outro.

## TOKEN_VAZIO

A meta não é `TOKEN_VAZIO=0`.

Para cada gap:

```text
{id, type, reason, dependencies, next_gate}
```

Estados terminais permitidos: `FILLED_BY_EVIDENCE`, `FALSIFIED`, `NOT_APPLICABLE`, `LEGITIMATELY_OPEN_TOKEN_VAZIO`.

## Validade de sucessor

```text
Valid(Ω[t+1]) =
  PRESERVE(ATA)
  ∧ TRACE(Δ)
  ∧ NO_FALSE_PROMOTION
  ∧ TYPE(GAPS)
  ∧ RECONSTRUCTIBLE(CONTEXT)
```

## Prioridade

```text
Priority(G_i) = Criticality × UnlockValue × DependencyCentrality
```

Safety, claim gate, privacidade e fail-closed têm precedência sobre a pontuação.

## F_ok

- Knowledge Hypervisor preservado como predecessor;
- memória longitudinal/ortogonal e Ω router reutilizados;
- `SEMANTICA_DINAMICA` e Procedure Ledger montados, não copiados;
- PR #243 virou primeiro state-transition receipt do overlay;
- um único contrato de composição cobre SUPER_ROOT, UNIVERSAL_NODE, CONTEXT_ROUTE e DELTA/ATA.

## F_gap

- cobertura global de mounts ainda não é terminal;
- migração global para Universal Nodes não foi executada;
- terminalidade global continua `TOKEN_VAZIO`.

## F_next

Executar **um piloto bounded** pelo `SUPER_ROOT` usando um P0/P1 de alto `UnlockValue`; registrar páginas/contextos efetivamente abertos, autoridades consultadas, gaps resolvidos, stop condition e receipt da rota. Só depois avaliar expansão do mount table.
