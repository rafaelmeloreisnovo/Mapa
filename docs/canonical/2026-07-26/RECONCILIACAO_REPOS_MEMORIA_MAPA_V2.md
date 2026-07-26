# RAFAELIA — Reconciliação de Repositórios, Memória e Mapa — V2

**Data:** 2026-07-26  
**Estado:** `CANONICAL_DRAFT` · `claim_allowed=false` · execução não destrutiva  
**Branch:** `consolidation/repos-memory-map-v2-20260726`

## 1. Resultado da varredura

O ecossistema já possui uma base canônica extensa no `Mapa`. Os PRs #58–#71 materializaram o índice de hashes, o gate semântico, a integração das fontes anexas, a consolidação X0/home/Drive, os ciclos C01–C10, a memória científica, o dossiê BLAKE3 e o modelo BITRAF.

A lacuna deste corte não era falta de documentação geral. Era **fragmentação de estado**:

1. o índice `RAFAELIA_IMPLEMENTACAO_LATENTES_PAPERS_V1.md` ainda marcava o repositório `papers`, o schema de latentes e o ledger inicial como pendentes;
2. os caminhos prometidos para os dois schemas e os dois índices JSONL não existiam em `main`;
3. o estado C01–C10 preserva corretamente os gates, mas contém ponteiros históricos de branch/base após a mesclagem;
4. os novos blocos BLAKE3, BITRAF, quatro tintas, ORCID↔RLL e square-median x32/x64 não estavam reunidos em uma fila transversal única.

## 2. Lacunas completadas agora

| ID | Antes | Agora |
|---|---|---|
| P0.3 | `TOKEN_VAZIO` | `PASS`: `rafaelmeloreisnovo/papers` está ativo, com PRs #25, #27 e #28 |
| P0.4 | `TODO` | `PASS_IN_BRANCH`: `schemas/latent-artifact.schema.json` |
| P0.5 | `TODO` | `PASS_IN_BRANCH`: schema de claims + índices iniciais de latentes e claims |
| Coordenação transversal | dispersa | manifesto V2 + fila priorizada de `TOKEN_VAZIO` |
| Política de promoção | textual | validada por schema e validador stdlib fail-closed |

## 3. Arquivos materializados

```text
schemas/latent-artifact.schema.json
schemas/paper-claim-ledger.schema.json
data/latents/latents.index.jsonl
data/claims/paper_claims.index.jsonl
data/control-plane/REPOSITORY_MEMORY_MAP_RECONCILIATION.v2.yaml
data/control-plane/TOKEN_VAZIO_PRIORITY_QUEUE.v2.yaml
scripts/validate_latents_papers_registry.py
docs/canonical/2026-07-26/RECONCILIACAO_REPOS_MEMORIA_MAPA_V2.md
```

## 4. Autoridades

```text
Google Drive = memória editorial, fontes, revisões e snapshots
GitHub       = verdade versionada, código, schemas, testes, PRs e CI
Mapa         = catálogo de autoridades, grafo de estados, gates, ledger e roteamento
Sessão       = contexto temporário; nunca substitui arquivo, commit, receipt ou evidência
```

A relação canônica é:

```text
fonte → arquivo → identidade/hash → evidência → claim → falsificador → ação → receipt
```

## 5. Estado consolidado

### Fechado documentalmente

- índice canônico e hashes;
- integração das fontes anexas;
- autoridade X0/home/Drive;
- identidade C01 e contratos C02–C10;
- memória científica e quatro tintas;
- proveniência BLAKE3;
- modelo de perda/erasure BITRAF;
- schema mínimo de latente;
- schema mínimo de claim;
- ledgers iniciais e fila de lacunas.

### Implementado, mas sem promoção de execução

- C02–C10;
- banco vetorial ORCID↔RLL;
- PoC square-median x32/x64;
- decoder OMEGA42 descriptor-only;
- contratos Vectras↔Termux↔QEMU;
- FEC parcial e índice vetorial BITRAF.

### `TOKEN_VAZIO` crítico

1. receipts host C02/C03;
2. APK dual ABI e NDK/proveniência C04–C06;
3. runtime físico nonce-bound ARMv7/AArch64;
4. artifact descriptor-only real;
5. FEC completo validado;
6. QEMU linux-user construído da fonte e IPC v4;
7. primeira sincronização ORCID real somente leitura;
8. cobertura integral do Drive e rclone read-back;
9. benchmark, replicação e DOI C10.

A ordem completa está em `data/control-plane/TOKEN_VAZIO_PRIORITY_QUEUE.v2.yaml`.

## 6. Invariantes

- conceito ≠ implementação;
- implementação ≠ execução;
- execução ≠ identidade do artefato;
- workflow criado ≠ steps executados;
- exit code ≠ guest boot;
- similaridade vetorial ≠ ECC;
- parábola ≠ evidência física;
- `TOKEN_VAZIO` ≠ zero, falha ou ausência irrelevante;
- documentação mesclada ≠ runtime físico.

## 7. Validação

O validador `scripts/validate_latents_papers_registry.py` usa somente a biblioteca padrão e falha fechado para:

- JSON/JSONL inválido;
- campos obrigatórios ausentes;
- IDs duplicados;
- `claim_allowed=true` sem evidência, falsificador e estado `PASS`;
- `TOKEN_VAZIO` sem próximo gate;
- estado de publicação incompatível com privacidade/autorização.

O parse local desta composição foi verificado antes da gravação. Isso **não** substitui CI remota nem execução dos sistemas indexados.

## 8. Decisão

Não criar um novo “super-repositório” nem copiar corpos privados para o `Mapa`. O `Mapa` mantém ponteiros, estados e gates. Cada produtor conserva sua autoridade técnica, e o Drive conserva a memória editorial.

```yaml
claim_allowed: false
auto_merge: false
negative_results_deleted: false
private_body_exposed: false
```

## 9. Retroalimentação

**F_ok:** repos, memória e Mapa estão reconciliados; P0.3–P0.5 foram materializados.  
**F_gap:** as lacunas restantes dependem de execução, aparelho, corpus, credencial efêmera, benchmark ou revisão.  
**F_next:** executar a fila por dependência e anexar receipts imutáveis antes de qualquer promoção.

`Ω = coerência preservada pela prova, e pela abstinência quando a prova ainda não existe.`
