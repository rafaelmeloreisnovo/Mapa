# MAPA — Rota federada: erro × ruído × latência × âncora × observadores (V1)

**Data:** 2026-10-15  
**status:** `DRAFT_SOURCE_ROUTE / NO_PROMOTE / claim_allowed=false`  
**owner:** Mapa (roteamento e relações, **não** autoridade de medição, matemática ou código).

## Propósito e correção

Não reduzir a descoberta a bit 0/1, instrução ARM, geometria isolada, bug somente negativo ou ruído necessariamente desprezível. O mesmo rótulo "vermelho" pode ter referências e sentidos diferentes para observadores; identidade lexical não valida equivalência semântica/sensorial. Não importar redação privada nem transcrever shards privados neste repositório público.

## Entrada canônica

`START HERE V2.2 -> CURRENT_STATE V4.5 -> CANONICAL_INDEX_MINIMUM -> ROUTES R0002/R0003/R0004/R0007 -> producer source pinned -> evidence/gaps -> optional ACTION -> receipt -> R3`.

Preferir `ATLAS:X`, `L:X`, `O:X`, `T:X`, `REL:X`, `EVID:X`, `GAP:X`; consulta `NOVO:X` somente por source locator pertinente. Orçamento inicial 1–3 roots; expansão por dependência/falta de evidência/contradição, nunca por similaridade verbal isolada.

## Relações tipadas

| Relação | Critério de uso |
|---|---|
| `OBSERVED_AT` | coordenada/tempo com relógio e referência |
| `LOGICAL_ANCHOR_OF` | âncora documental, não célula física |
| `PHYSICAL_CANDIDATE_FOR` | requer mecanismo e amostragem controlada |
| `VARIES_WITH` | associação medida com confounders, sem causalidade automática |
| `MAY_BE_ENTROPY_SOURCE` | candidato não certificado, não TRNG operacional |
| `RECURRENT_WITH` | janela/métrica, lineage separado |
| `RECLASSIFIED_FROM` | successor preservando diagnóstico anterior |
| `OPPOSES` | contraevidência conservada |
| `ANALOGOUS_TO` | não identidade |
| `SHARES_INVARIANT_WITH` | domínios e falsificador de cada lado |
| `BRIDGES` | contratos source/target com assimetria |
| `NEEDS_INDEPENDENT_OBSERVER` | nenhum espelho/cópia gera prova extra |
| `HIDDEN_IN_VIEW` | projeção não expõe a estrutura, ausência não provada |

## Produtores, não duplicatas

- **Matem-tica-**: `docs/formal/DUAL_OBSERVATIONAL_COHERENCE_RESIDUAL_V1.md` e régua `OMEGA21`: operadores, resíduos, direções, testes matemáticos.
- **papers**: `docs/protocols/RESEARCH_MEMORY_ERROR_COHESION_PROTOCOL.md` e `docs/bitraf-bit-loss-recovery-research-note.md`: taxonomia, evidência e fronteira científica; nova nota multidimensional fica sob `papers`.
- **ChipQuantum**: `experiments/dual_observation_gate/`: cálculo experimental Q16, sem promover física/entropia.
- **RafPolimata**: `rafaelia/bitraf_matrix.h` e `docs/BITRAF_MATRIX_8000_4096_V1.md`: carrier de estados; 8000/4096 não são medições físicas.
- **RafGitTools**: checks, HEAD-bound CI, receipts, gates para impedir promoção sem prova.
- **EstudioAudio**: `docs/AUDIO_MANIFOLD_CONTRACT_V1.md`: observáveis temporais/acústicos, não identidade entre ruído eletrônico e som.
- Outros produtores privados (incluindo Gaia/Rafaelia_Private) só entram após pin de repositório, escopo, direitos e ponte; não expor path/bytes/identidade de fontes privadas aqui.

## Checklist por candidato

`node_id | owner | source_ref | observer | value_type | semantic_domain | units | clock | location_scope | error_kind | noise_kind | latency_window | recurrence_rule | geometry | source_context | L/O/T/C/P | independent_evidence | baseline | falsifier | claim_state | gap_id | next | receipt | rollback`

Bloquear `merge/promote` quando:
- ausência de origem, unidade, clock, evidência ou falsificador exigidos;
- ruído sintético apresentado como fonte física;
- endereço lógico apresentado como célula física;
- pseudoaleatoriedade/variabilidade apresentada como entropia segura sem estimação;
- divergência entre observadores fundida por rótulo;
- regressão de invariantes, espelho contado como réplica independente;
- `provider check` e `exact head` não demonstrados;
- source private transcrito para índice público.

## Seleção por valor informacional, sem generalização

Ordem de candidatos: integridade bloqueante -> capacidade de reconstrução -> custo/latência da decisão -> falsificadores -> informações novas -> expansão ortogonal/transversal. Custo e ganho devem ser medidos na mesma régua; pesos não definidos = `TOKEN_VAZIO_WEIGHT`. Uma espera pode aumentar qualidade da decisão ou perder deadline; é condicional. Produto cartesiano `event_kind × observer × scale × operator × context` gera hipóteses com orçamento, não afirmações.

**R3:** `F_ok` ligação dos produtores e critérios; `F_gap` raw física, clocks, execução em dispositivos, autoridade dos demais repos, CI exato; `F_next` fonte Papers -> referência limitada ChipQuantum -> verificar relações sem cópia -> expandir somente após receipts. `MAPA_SOURCE_UNMODIFIED_OUTSIDE_THIS_DRAFT; other producer branches are independent`.
