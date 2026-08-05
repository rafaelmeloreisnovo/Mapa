# NOVOexport — shard `003` transportado, grafo construído e reconciliado

- **Evento:** `sha256:96a12751ea6bd27897b7b308971b8080981a4edc865419a37c90c4ad261a86cf`
- **Modo:** `INCREMENTAL_APPEND_ONLY_FAIL_CLOSED`
- **Privacidade:** `PUBLIC_SANITIZED_AGGREGATES_ONLY`
- **Claim permitido:** `false`
- **Treinamento executado:** `false`
- **Cobertura longitudinal:** `4/51` shards de conversas

## Correção append-only do estado

O checkpoint anterior classificava `conversations-003.json` como `PARTIAL_PERSISTENCE` porque os pares privados `CHUNKS/NORMALIZED` ainda não estavam em custódia durável.

O estado sucessor verificável agora é:

```text
SOURCE_HASH_VERIFIED
→ 4 V2 CHUNKS/NORMALIZED PAIRS MATERIALIZED
→ 8/8 JSONL PARSE PASS
→ 8/8 DRIVE ROUNDTRIP BYTE_IDENTICAL_PASS
→ READY_FOR_GRAPH
→ 4 GRAPH MICRO-BATCHES
→ INDEX_BUILT
→ 002↔003 RECONCILED
```

A identidade byte a byte dos payloads locais antigos, que foram perdidos antes da persistência, continua `TOKEN_VAZIO_NOT_AVAILABLE`. Os artefatos V2 são uma reconstrução determinística validada por round-trip; não são declarados idênticos aos payloads perdidos.

## Shard `003`

| Métrica | Valor |
|---|---:|
| Conversas | 100 |
| Registros de mapping | 9.533 |
| Mensagens | 9.433 |
| Nós `TOKEN_VAZIO` | 100 |
| Pares CHUNKS/NORMALIZED V2 | 4 |
| JSONL válidos | 8/8 |
| Round-trip Drive | 8/8 PASS |
| Micro-batches de grafo | 4 |
| Registros do grafo | 132.850 |
| Nós únicos do grafo | 9.982 |
| Arestas únicas do grafo | 122.794 |
| Relações quebradas | 0 |
| Órfãos | 0 |
| Ciclos parent | 0 |

```text
graph_merkle_root =
a357b03f27a3d9427bc0d282eb5f0c5fc89d22a0b9b771b6bcf1b349045b22ba
```

## Reconciliação `002 ↔ 003`

| Verificação | Resultado |
|---|---:|
| IDs de conversa sobrepostos | 0 |
| IDs de mensagem sobrepostos | 0 |
| IDs de nó sobrepostos | 1 |
| Classificação do nó | `REUSED_NON_MESSAGE_NULL_ROOT_SENTINEL` |
| Hashes exatos de conteúdo recorrentes | 55 |
| Ocorrências mínimas pareadas | 310 |
| Hashes de título recorrentes | 1 |
| Hashes estruturais recorrentes | 0 |
| Fronteira temporal ordenada | 283,578783 s |

A recorrência por hash é somente sinal estrutural. Ela não autoriza interpretação semântica.

## Fechamento de identidade `000–003`

| Métrica | Ocorrências | Únicos |
|---|---:|---:|
| Conversas | 400 | 400 |
| Mensagens | 29.492 | 29.492 |
| Nós de mapping | 29.892 | 29.653 |

- IDs de conversa repetidos entre shards: `0`;
- IDs de mensagem repetidos entre shards: `0`;
- reutilizações de nó: `3`, todas sentinelas-raiz sem mensagem em fronteiras adjacentes;
- sobreposição não adjacente de identidade: `0`.

Portanto, a contagem cumulativa única de mensagens dos lotes `000–003` deixa de ser `TOKEN_VAZIO` e passa a **29.492**, limitada exatamente a esses quatro shards.

## Custódia privada

```text
envelope = conversations-002-003.reconciliation.private.v2.zip.b64.txt
decoded_zip_bytes = 9.347
decoded_zip_sha256 =
713ad0579bcfd6cf8a743f9dcffcf1f320529a9b9c017bffbf6aa74afac1e322
upload → download → decode → SHA-256 = PASS
```

Nenhum corpo de mensagem, título bruto ou ID privado foi incluído neste delta público.

## F_ok

- transporte privado V2 fechado;
- grafo do shard `003` construído;
- reconciliação adjacente `002↔003` concluída;
- contagem global de identidade `000–003` concluída;
- cobertura longitudinal promovível para `4/51`.

## F_gap

- identidade byte a byte dos payloads antigos perdidos continua `TOKEN_VAZIO`;
- recorrência de conteúdo não é prova semântica;
- fechamento do corpus além de `003` continua aberto;
- treinamento permanece `HOLD`;
- execução física e reprodução científica independente estão fora deste gate.

## F_next

1. Acrescentar cobertura longitudinal `4/51`.
2. Rotear relações privadas de recorrência ao ledger do grafo.
3. Enfileirar `conversations-004.json` somente após fechamento dos receipts.
4. Manter `claim_allowed=false`, treinamento desabilitado e merge automático bloqueado.

## Autoridade estruturada

`data/catalog_runs/RAFAELIA_NOVOEXPORT_MEMORY_003_GRAPH_RECONCILED_2026-08-05.json`
