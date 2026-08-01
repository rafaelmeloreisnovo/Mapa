# Memória Longitudinal de Snapshots do Google Drive — V1

**Estado:** `VERIFIED_LIMITED`  
**Data de observação:** 2026-08-01  
**Fonte:** Google Drive privado, pasta `CientiEspiritual`  
**Fronteira de privacidade:** somente metadados no repositório; corpos de conversa, perfis, mídia e anexos permanecem no Drive.  
**claim_allowed para conteúdo:** `false`

## 1. Finalidade

Esta camada transforma exports repetidos do ChatGPT e seus pools de mídia em uma memória longitudinal navegável, sem concatenar snapshots e sem publicar dados privados.

A unidade principal é:

```text
snapshot temporal
→ conversation_id
→ grafo mapping
→ message_id
→ asset_pointer
→ Drive file_id
→ hash verificável
```

## 2. Seleção canônica observada

| Estado | Pasta | Tipo | `conversations.json` | Conversas |
|---|---|---|---:|---:|
| `CANONICAL_RAW` | `json22` | export completo | 499.885.038 bytes | 1.788 |
| `HISTORICAL_CHECKPOINT` | `json163` | export completo | 476.336.716 bytes | 1.664 |
| `DUPLICATE_CANDIDATE` | `js334` | export completo | 413.093.247 bytes | `TOKEN_VAZIO` |
| `DUPLICATE_CANDIDATE` | `json17` | export completo | 413.093.247 bytes | `TOKEN_VAZIO` |
| `ASSET_POOL` | `json170` | árvore por conversa/usuário | — | — |
| `ASSET_POOL` | `json800` | imagens e DALL·E | — | — |
| `ASSET_POOL` | `json600` | imagens e arquivos tipados por MIME | — | — |

Entre `json163` e `json22`, foram observadas 124 conversas novas, 25 modificadas e zero removidas. Essa observação classifica os diretórios como checkpoints cumulativos, não como fragmentos para concatenação.

## 3. Invariantes

1. O número no nome da pasta não representa tamanho nem quantidade de conversas.
2. Snapshots completos não devem ser concatenados.
3. `mapping` é um grafo; o caminho canônico e os ramos alternativos devem ser preservados.
4. O repositório nunca recebe corpos privados de mensagens ou mídia.
5. Hash desconhecido é `null`, nunca estimado.
6. Deduplicação exige identidade por hash, não apenas nome, tamanho ou data.
7. Todo `TOKEN_VAZIO` registra condição e próximo passo verificável.

## 4. Contexto contínuo — cinco variáveis ativas

```yaml
canonical_snapshot: snapshot-json22-2025-08-03
historical_checkpoint: snapshot-json163-2025-07-27
duplicate_candidate_group: dup-2025-07-07-js334-json17
asset_route: json170 + json600 + json800
open_gate: sha256_and_asset_pointer_reconciliation
```

Essas cinco variáveis formam uma cápsula curta para retomar o trabalho sem reabrir corpos privados.

## 5. Distribuição de responsabilidade

| Camada | Local correto |
|---|---|
| JSON bruto, `chat.html`, usuário, feedback e compartilhadas | Google Drive privado |
| Áudios, imagens, APKs, ZIPs, PDFs e demais anexos | Google Drive privado |
| Catálogo de snapshots, estados, tamanhos e IDs minimizados | `Mapa` |
| Esquema e validador determinístico | `Mapa` |
| Hashes e recibos de execução | Drive privado + ponteiro no `Mapa` |
| Claims derivados do conteúdo | somente após revisão e gate específico |

## 6. Pipeline aprovado

```text
01 DISCOVER
02 METADATA_CATALOG
03 HASH
04 SNAPSHOT_DIFF
05 GRAPH_INDEX
06 ASSET_RECONCILIATION
07 SEMANTIC_CARRIERS
08 CONTEXT_CAPSULE
09 RECEIPT
10 REVIEW
```

As etapas 03 e 06 permanecem `TOKEN_VAZIO`.

## 7. Artefatos desta implementação

- `schemas/drive_memory_snapshot_catalog.schema.json`
- `indices/memoria-longitudinal/drive_snapshot_catalog.v1.json`
- `scripts/validate_drive_snapshot_catalog.py`
- `tests/test_drive_snapshot_catalog.py`
- `auditoria/DRIVE_MEMORY_SNAPSHOT_IMPLEMENTATION_20260801.json`

## 8. Gates abertos

### G-HASH-001

`TOKEN_VAZIO`: falta calcular SHA-256 dos exports completos sem alterar as fontes.

### G-ASSET-002

`TOKEN_VAZIO`: falta reconciliar integralmente `asset_pointer → Drive file_id → hash`.

### G-DEDUP-003

`TOKEN_VAZIO`: `js334` e `json17` têm metadados coincidentes, mas a igualdade byte a byte não foi provada.

## 9. Próximo passo verificável

Executar hashing streaming dos quatro `conversations.json`, registrar os hashes no catálogo e comparar `js334` com `json17`. Em seguida, produzir índice append-only dos assets por `conversation_id`, sem copiar seus bytes para o repositório.

## 10. Espelho privado no Google Drive

- Pasta de continuidade: `MEMORIA_LONGITUDINAL_SNAPSHOTS`
- Folder ID: `1LvCpSISN8UXSs6z2H2IAdCLABd6Tpgpm`
- Documento canônico privado: `RAFAELIA_MEMORIA_LONGITUDINAL_DRIVE_SNAPSHOTS_V1`
- Document ID: `13OVLaO6H922KZKsTyCG0EEohN8sHKHbq__KLeriClWE`
- Índice tabular privado: `RAFAELIA_DRIVE_SNAPSHOT_INDEX_V1`
- Spreadsheet ID: `1Kj2apQdS4_Ss-W6wlL2NZSvNvhavsNyf1BemqHZiZQE`

O espelho no Drive é privado e contém apenas metadados desta camada. Ele não substitui os arquivos-fonte nem altera seus bytes.
