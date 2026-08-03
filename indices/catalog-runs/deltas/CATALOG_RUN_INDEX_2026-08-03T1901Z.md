# RAFAELIA — Índice incremental B7 e governança

Ciclo: `CAT-20260803T1901Z`  
Checkpoint: `Mapa@5138828775058f2bf1650cf6f4b3e640e3f158a9`  
Modo: `APPEND_ONLY` · `claim_allowed=false`

## Entrada rápida para humanos e IAs

| Pergunta | Autoridade e rota |
|---|---|
| Onde está o contrato B7 no runtime virtualizado? | `rafaelmeloreisnovo/Vectras-VM-Android` · PR `#1088` · merge `dca59d023fe432560a833e41af887a53d2f19fb7` |
| Onde está a integração B7 no runtime Termux nomalloc? | `rafaelmeloreisnovo/termux-app-rafacodephi` · PR `#326` · merge `0e4330273375344042eba8ff17de47c5bc8af573` |
| Onde está o receipt editorial do ciclo B7? | Drive `1vm0Uo0Rj_1Do_614Bznn89VRppMpJAKDzS1sXeASLZY` |
| Onde está a governança e memória federada? | `rafaelmeloreisnovo/Mapa` · head observada `1ff6b9877c73214045029ca72f940ca3e878a365` |
| Onde está o receipt machine-readable deste ciclo? | `data/catalog_runs/RAFAELIA_CATALOG_CYCLE_2026-08-03T1901Z.json` |

## Delta material

### B7 em Vectras

A PR `#1088` adiciona um orquestrador portátil com região fornecida pelo chamador, três bancos alinhados, 16 lanes, CRC32C, transformação determinística, caminhos NEON/escalar, callbacks de disco, interface GPU opcional, receipts por estágio e self-test.

Vetor host declarado:

```text
PASS bytes=8192 crc32c=caf1abc5 caps=00000009 receipts=4
```

Classificação:

- fonte e merge: `PROVADO`;
- PASS host declarado: `EVIDENCIADO_LOCAL_LIMITED`;
- ARM, Android e GPU: `TOKEN_VAZIO`.

### B7 em Termux

A PR `#326` integra o mesmo contrato funcional à `librafaelia_core` nomalloc, preservando o orquestrador histórico para comparação e migração controlada.

Rotas principais:

```text
rmr/Rrr/raf_b7_orchestrator.c
rmr/Rrr/raf_b7_orchestrator.h
rmr/Rrr/Android_nomalloc.mk
scripts/run_raf_b7_selftest.sh
tools/raf_b7_orchestrator_selftest.c
```

Classificação:

- integração e merge: `PROVADO`;
- CRC de referência `caf1abc5`: `EVIDENCIADO_LOCAL_LIMITED`;
- build NDK, Termux físico, equivalência NEON e GPU: `TOKEN_VAZIO`.

### Relação federada

```text
B7 contrato compartilhado
├── Vectras: engine/RMR e superfície VM
└── Termux: rmr/Rrr e librafaelia_core nomalloc
```

Relação: `PARALLEL_INTEGRATION_OF_SHARED_B7_CONTRACT`.

Isso demonstra duas materializações com estrutura e vetor host compatíveis. Não demonstra identidade binária, equivalência ARM, desempenho ou execução física.

### Mapa e governança

Desde o checkpoint, o `Mapa` avançou 23 commits até a head observada `1ff6b9877c73214045029ca72f940ca3e878a365`, adicionando:

- integral gate e workflow;
- manifestos e receipts com SHA-256;
- verificador e testes;
- session boot e eventos longitudinais;
- memória `F_GAP/F_NEXT` append-only;
- reconciliação de promoção da PR `#143`.

O próprio registro observa que a PR `#143` foi mesclada apesar de restrições descritivas de revisão e `automatic_merge=false`. O merge é `EVIDENCIADO`; ator, regra e mecanismo causal permanecem `TOKEN_VAZIO`.

## Dependências

```text
C compiler
├── scalar fallback
├── ARM NEON, condicionado ao alvo
└── ARM CRC32, condicionado ao alvo

caller-provided memory
callbacks read_at/write_at
optional Vulkan/OpenCL probes
producer-specific build manifests
external witness before claim promotion
```

## Fronteiras epistemológicas

| Classe | Resultado |
|---|---|
| `PROVADO` | objetos Drive/GitHub, PRs, commits, caminhos e novos arquivos do Mapa existem |
| `EVIDENCIADO` | vetor host B7 foi declarado de forma consistente; há duas integrações paralelas |
| `HIPÓTESE` | ambos os runtimes podem produzir receipts equivalentes após reprodução congelada |
| `MODELO_ANALÓGICO` | INGEST → COMPUTE → EGRESS modela o fluxo operacional, não superioridade universal |
| `PARÁBOLA` | nenhuma nova |
| `REFUTADO` | host PASS prova Android/NEON/GPU; política textual bloqueia merge; fonte semelhante prova binário idêntico |
| `TOKEN_VAZIO` | device, CI observável, exports Drive, equivalência cruzada e rulesets executáveis |

## F_ok

- receipt Drive B7 localizado após o corte;
- merges B7 em Vectras e Termux resolvidos com base, head e merge SHA;
- relação federada tipada sem duplicar os fontes;
- delta interno do `Mapa` reconciliado;
- receipt e índice append-only gravados.

## F_gap

- nenhum SHA-256 de exportação Drive;
- nenhum receipt Android/Termux físico;
- nenhuma equivalência ARMv7/ARM64;
- nenhum receipt Vulkan/OpenCL;
- falha CI pré-step sem log causal fechado;
- regras de promoção não foram demonstradas por teste negativo.

## F_next

```text
congelar os dois merges
→ executar o mesmo vetor host/ARMv7/ARM64/Android
→ comparar saída, CRC e sequência de receipts
→ registrar toolchain, flags, ABI, stdout/stderr e hashes
→ capturar rulesets
→ executar teste negativo de promoção
→ emitir receipts sucessores append-only
```

## Ações não executadas

Nenhuma escrita no Drive, reexecução de workflow, execução Android/Termux, alteração nos produtores, deduplicação destrutiva ou promoção de claim.

\[
\boxed{\text{mesmo contrato} \neq \text{mesmo binário} \neq \text{mesmo runtime} \neq \text{equivalência comprovada}}
\]
