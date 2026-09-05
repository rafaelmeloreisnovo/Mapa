# FIAT_LUX — Evidence Database Federation V1

**Data:** 2026-09-05  
**Estado:** IMPLEMENTED_PARTIAL / APPEND_ONLY / claim_allowed=false  
**Autoridades:** Drive ATLAS + Mapa + RafGitTools  
**Executor:** `rafaelmeloreisnovo/RafGitTools/tools/rafaelia_navigator/fiat_lux_evidence_db_v1.py`

## 1. Objetivo

Materializar as memórias, rotas, evidências, gates, receipts, vazios informacionais, passos e roadmap como planos lógicos persistentes dentro do `RAFAELIA_NAVIGATOR.sqlite3`, sem transformar Google Drive em banco transacional e sem duplicar o mesmo conhecimento em bancos independentes.

Princípio:

```text
mesmo objeto
  -> múltiplas projeções L/O/T
  -> evidências
  -> gates
  -> receipts
  -> estado atual
  -> próximos passos
```

A implementação preserva as invariantes já registradas no ATLAS:

```text
VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM
TOKEN_VAZIO != 0
resolved != deleted_history
latest_evidence_wins_for_current_routing
provider_scope_reproduction != exact_canonical_binding
host_runtime != physical_device_runtime
hash_integrity != authorship_or_scientific_truth
analogy != identity; symbol != evidence; cooccurrence != causality
```

## 2. Planos lógicos

A V1 cria os seguintes planos no mesmo arquivo SQLite:

| Nome pedido / plano | Função canônica |
|---|---|
| `databaseroot` | raízes, providers, autoridades e locators |
| `databaseStarthere` | rota mínima ATLAS/NOVO/L/O/T/REL/SCALE/EVID/DELTA |
| `database_∅` | TOKEN_VAZIO, lacunas, incerteza, falsificador e ação seguinte |
| `database_evidencias` | observações, medições, digests, receipts de origem |
| `database_gates` | critérios de promoção e decisões fail-closed |
| `database_receipts` | cadeia append-only de evidência e resultado |
| `database_invariants` | invariantes e falsificadores |
| `database_memory_axes` | projeções longitudinal, ortogonal e transversal |
| `database_routes` | caminho de navegação tipado |
| `database_hot_pathway` | hot path condicional e encadeamento |
| `database_one_hot_binding` | binding lógico MOD9 0..8 |
| `databaseSTEPStoDo&done` | eventos de TODO/DOING/DONE/BLOCKED/TOKEN_VAZIO |
| `roadmapDatabase` | roadmap ordenado por dependência/risco/informação |
| `atlas_urgency_queue` | snapshot/import da fila de urgência do Mapa |

Os nomes acima são **planos lógicos/tabelas**, não múltiplos arquivos de banco. A decisão evita divergência, duplicação e sincronização frágil entre vários SQLite separados.

## 3. Rota START_HERE

A rota canônica materializada é:

```text
ATLAS:X
  -> NOVO:X
  -> L:X
  -> O:X
  -> T:X
  -> REL:X
  -> SCALE:X
  -> EVID:X
  -> DELTA
```

Autoridade Drive correspondente:

- START_HERE: `1UZyuoEaoun19_peraI7sqoR_ojj54jD1y_BRGEgvchE`
- LONGITUDINAL: `1XHkixpMruPqrv22EJ5X0TeWUn7fWEXgmjnGSlxtaGzk`
- ORTHOGONAL: `1HXDWFSmHGNo7pouUge3AIGhTq4SL_EkfrurXdJzM6-E`
- TRANSVERSAL: `13oy53b9OAm7Fomyt_FANl7pAORrPtBAfnkZny7Kx-f8`
- RELATION_ONTOLOGY: `1zBRetiSqlpgZep4OU8Qqd8-tgktVMhzGxJP2IeeBkV8`
- SCALE: `1ExbWhj2dNsF-_4P5tjvB0StN55ll5T_ZtjleNTr3jY4`
- EVIDENCE_GATES: `1ZOIgUdffE9xoW_erxaeozNOqbC2M8KOkiumEYuTaPM8`
- RECEIPTS folder: `1AxTvlDsU4V_rnOsMYeRf7aG9r1IMFg8R`

## 4. Caminhada one-hot / hot_pathway

O binding implementado preserva a gramática MOD9 já formalizada:

```text
B0 = {0,1,2}
B1 = {3,4,5}
B2 = {6,7,8}

forward(i)   = (i + 1) mod 9
reverse(i)   = (i + 8) mod 9
bank_next(i) = (i + 3) mod 9
```

`database_one_hot_binding` exige:

- slot em `0..8`;
- bank em `0..2`;
- slot pertencente ao bank declarado;
- `bind_state` explícito;
- evidence/gate opcionais, mas necessários para promoção de runtime;
- `claim_allowed=false` por padrão.

A view `v_one_hot_walk` calcula `next_slot`, `prev_slot` e `bank_next_slot` sem reinterpretar MOD9 como hardware físico.

## 5. Hot pathway

`database_hot_pathway` registra cada passo como evento:

```text
pathway_id
object_id
ordinal
slot
node_ref
condition_expr
next_ref
binding_id
gate_id
evidence_id
state
```

Nenhuma condição textual executa ação arbitrária. O plano é descritivo e deve ser consumido por um executor governado.

## 6. Evidência -> gate -> receipt -> estado

Regra operacional:

```text
observation
  -> database_evidencias
  -> database_gates
  -> database_receipts
  -> memory L/O/T delta
  -> databaseSTEPStoDo&done
  -> roadmapDatabase
```

Fechamento permitido somente quando o gate referencia evidência suficiente e o receipt liga:

```text
request/source -> artifact/input -> execution/measurement -> output -> decision
```

O histórico nunca é reescrito. Transição de estado é novo evento.

## 7. database_∅

`database_∅` é a materialização explícita do vazio informacional. Cada linha deve conter, quando conhecido:

```text
gap_id
subject_id
priority
state
authority
evidence_required
uncertainty
falsifier
next_action
source_ref
predecessor_event_id
```

`TOKEN_VAZIO` não significa zero, falso ou inexistente. Significa ausência tipada de evidência/definição/binding necessária.

## 8. Urgência do Mapa

Fonte corrente de prioridade:

`data/control-plane/TOKEN_VAZIO_PRIORITY_QUEUE.v3.json`

Ordem registrada na fonte:

```text
dependency_then_risk_then_information_gain_then_latest_evidence
```

P0 atual da fonte:

1. `P0-MAIN-SERVER-ENFORCEMENT`
2. `P0-INDEPENDENT-APPROVAL`

P1 atual inclui:

- `TV-MESSAGES-EXACT-CANONICAL-FULL-SCOPE-BINDING`
- `TV-ANDROID-PHYSICAL-RUNTIME`
- `TV-NOVOEXPORT-PER-OBJECT-COVERAGE`
- `TV-LEGACY-MESSAGE-NODE-PROJECTION-GENERATOR`
- `TV-ACTIVE20-LICENSE-PROVENANCE`
- `TV-MATRIX-C-IPA-SOURCE-CONTRACTS`

A implementação RafGitTools possui `import-urgency` para materializar um snapshot da fila diretamente em `atlas_urgency_queue`, `database_∅`, `databaseSTEPStoDo&done` e `roadmapDatabase`.

## 9. Passos TODO/DONE sem perda de história

`databaseSTEPStoDo&done` não é uma lista mutável. Cada transição cria um evento novo:

```text
TODO -> DOING -> DONE
          |-> BLOCKED
          |-> TOKEN_VAZIO
```

Views de estado atual selecionam o evento mais recente; o histórico permanece inteiro.

## 10. FIAT_LUX

Neste contrato, `FIAT_LUX` significa:

```text
fonte visível
-> identidade preservada
-> relação explícita
-> evidência ligada
-> gate verificável
-> receipt reconstruível
-> próximo passo finito
```

Não significa promoção automática de claim.

## 11. Executor e comandos

```bash
python tools/rafaelia_navigator/fiat_lux_evidence_db_v1.py selftest
python tools/rafaelia_navigator/fiat_lux_evidence_db_v1.py init "$DB"
python tools/rafaelia_navigator/fiat_lux_evidence_db_v1.py seed-canonical "$DB"
python tools/rafaelia_navigator/fiat_lux_evidence_db_v1.py import-urgency "$DB" TOKEN_VAZIO_PRIORITY_QUEUE.v3.json --source-ref Mapa:data/control-plane/TOKEN_VAZIO_PRIORITY_QUEUE.v3.json
python tools/rafaelia_navigator/fiat_lux_evidence_db_v1.py walk 8 forward
python tools/rafaelia_navigator/fiat_lux_evidence_db_v1.py bind "$DB" MOD9-EXAMPLE 8 CONTROL_SYNC --source-ref Mapa/Drive
```

## 12. Gate de fechamento

V1 somente pode ser promovida de `IMPLEMENTED_PARTIAL` quando houver:

- Python syntax PASS;
- SQLite selftest PASS;
- append-only trigger PASS;
- MOD9 walk PASS;
- import de uma fila de urgência real PASS;
- receipt com commit/CI;
- nenhuma modificação dos sources originais;
- `claim_allowed=false` mantido para inferências não provadas.

## R3

**F_ok:** schema e executor foram materializados em branch de RafGitTools; contrato canônico e registry de roteamento são materializados no Mapa.  
**F_gap:** CI/PR e execução em dispositivo físico ainda não são evidência neste documento.  
**F_next:** executar CI, registrar receipt, importar a fila real e então promover apenas os gates efetivamente fechados.
