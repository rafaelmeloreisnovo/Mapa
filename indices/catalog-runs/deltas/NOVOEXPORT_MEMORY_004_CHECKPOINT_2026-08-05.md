# NOVOexport — checkpoint sanitizado de `conversations-004`

- **Evento:** `sha256:dc341b30151ad5ae9a6818457774a44bcf31016e6edfedd8da479f47df9460c5`
- **Modo:** `INCREMENTAL_APPEND_ONLY_FAIL_CLOSED`
- **Estado:** `PARTIAL_PERSISTENCE`
- **Claim permitido:** `false`
- **Treinamento:** `false`
- **READY_FOR_GRAPH:** `false`

## Fonte verificada

| Campo | Valor |
|---|---:|
| Arquivo lógico | `NOVOexport/conversations-004.json` |
| Bytes | 21.320.257 |
| SHA-256 | `477f650a94d535b76f0ce9283b22429df229cf93d44f11d9209be2ffd435a8c5` |
| Conversas | 100 |
| Nós de mapping | 9.413 |
| Mensagens | 9.313 |
| Nós sem mensagem | 100 |
| Duplicatas exatas declaradas | 604 |
| Classificações `TOKEN_VAZIO` | 252 |

## Cadeia Stage 2

Os quatro checkpoints históricos cobrem continuamente os índices `0–99` e os totais de `items` foram reproduzidos diretamente da fonte bruta.

| Batch | Conversas | Nós | Mensagens | Duplicatas | TOKEN_VAZIO |
|---:|---:|---:|---:|---:|---:|
| 1 | 0–24 | 2.610 | 2.585 | 169 | 83 |
| 2 | 25–49 | 2.291 | 2.266 | 129 | 68 |
| 3 | 50–74 | 2.813 | 2.788 | 193 | 44 |
| 4 | 75–99 | 1.699 | 1.674 | 113 | 57 |

## Estado honesto

```text
SOURCE_MATERIALIZED=true
SOURCE_HASH_VERIFIED=true
STAGE2_CHECKPOINT_CHAIN_VERIFIED=true
DERIVED_JSONL_MATERIALIZED=false
READY_FOR_GRAPH=false
TRAINING_EXECUTED=false
claim_allowed=false
```

Os hashes históricos dos outputs estão preservados nos checkpoints, mas os payloads antigos não estão em custódia durável. Portanto, os hashes não demonstram por si mesmos a identidade byte a byte dos objetos derivados.

## F_ok

- fonte recuperada por referência nativa do conector;
- SHA-256 e bytes fixados;
- quatro checkpoints Stage 2 encadeados;
- cobertura `0–99` confirmada;
- contagens de nós e mensagens reproduzidas diretamente da fonte.

## F_gap

- pares privados `CHUNKS/NORMALIZED` ainda não materializados;
- round-trip de bytes ainda ausente;
- shard não promovido a `READY_FOR_GRAPH`;
- reconciliação `003↔004` não executada;
- treinamento permanece em `HOLD`.

## F_next

1. Construir o par V2 do batch `0001` como correção append-only.
2. Validar JSONL, parent edges, contagem e privacidade.
3. Transportar por referência nativa.
4. Baixar e exigir SHA-256 byte-idêntico.
5. Repetir os batches `0002–0004` somente após o primeiro fechar.
6. Construir o grafo e reconciliar `003↔004`.

## Autoridade estruturada

`data/catalog_runs/RAFAELIA_NOVOEXPORT_MEMORY_004_CHECKPOINT_2026-08-05.json`
