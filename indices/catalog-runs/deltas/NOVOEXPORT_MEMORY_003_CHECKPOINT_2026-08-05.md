# NOVOexport — checkpoint sanitizado de `conversations-003`

- **Modo:** `INCREMENTAL_APPEND_ONLY_FAIL_CLOSED`
- **Estado global:** `PARTIAL_PERSISTENCE`
- **Claim permitido:** `false`
- **Privacidade:** `PUBLIC_SANITIZED_POINTERS_ONLY`
- **Event ID:** `sha256:f00bc1cf6fcb4ca82f6ed692edf3b2fc2b51edacf59b0b4bbdeca1b79388b8da`
- **READY_FOR_GRAPH:** `false`

## Correção do cursor

O lote `conversations-003.json` não está pendente de leitura inicial. O checkpoint privado demonstra que ele já foi:

```text
hashed
→ extracted
→ normalized
→ exact-record deduplicated
→ checkpointed in 4 private micro-batches
```

O estado correto não é `PENDING_CATALOG`; é `PARTIAL_PERSISTENCE`.

## Fonte sanitizada

| Campo | Valor |
|---|---:|
| Caminho lógico | `NOVOexport/conversations-003.json` |
| SHA-256 | `8544e29a071bfa80a21ebc25719ec5d0462cff289d8ce27f9dbed778e7fefc38` |
| Bytes | `20.065.953` |
| Micro-batches | `4` |
| Conversas | `100` |
| Nós | `9.533` |
| Mensagens | `9.433` |
| Registros exatos duplicados | `568` |
| Arestas parent órfãs | `0` |
| Nós `TOKEN_VAZIO` | `100` |
| Checkpoints append-only | `4` |

Nenhum ID do Google Drive, título de conversa, corpo de mensagem, asset ou URL privada foi publicado.

## Adapters

- `GAIA_phi`: `L1_raw`, `L2_parsed`, `L3_indexed`;
- `Rafaelia_Private`: `RMRALPHA`;
- `RMRIA`: `HOLD`;
- treinamento executado: `false`.

## F_ok

- hash da fonte fixado;
- extração, normalização e deduplicação exata concluídas em quatro micro-batches privados;
- quatro checkpoints append-only persistidos;
- ausência de arestas parent órfãs registrada no checkpoint;
- separação entre indexação e treinamento preservada.

## F_gap

- transporte dos pares JSONL privados para `CHUNKS_PRIVATE` e `NORMALIZED_PRIVATE` bloqueado por rejeição de referência local de arquivo;
- reconciliação `conversations-002 ↔ conversations-003` ainda não demonstrada;
- contagem única cross-lot de mensagens permanece `TOKEN_VAZIO`;
- shard ainda não pode ser promovido a `READY_FOR_GRAPH`;
- treinamento, CI observável e runtime físico permanecem fora deste gate.

## F_next

1. Repetir o transporte dos quatro pares JSONL usando referências de arquivo nativas do conector.
2. Recuperar os oito objetos privados e comparar hashes/bytes.
3. Reconciliar `conversations-002 ↔ conversations-003`.
4. Registrar sobreposições de conversa, mensagem, nó, hash de título, hash estrutural e hashes recorrentes.
5. Somente então alterar `READY_FOR_GRAPH=false` por evento sucessor verificável.
6. Manter treinamento em `HOLD` até o grafo e os receipts estarem fechados.

## Agregado longitudinal

Após este checkpoint:

- lotes com leitura/processamento privado: `000` a `003`;
- conversas brutas cobertas: `400`;
- total único de mensagens entre os quatro lotes: `TOKEN_VAZIO_UNTIL_002_003_RECONCILIATION`;
- próximo cursor de ingestão não deve avançar para `004` enquanto transporte e reconciliação do `003` permanecerem abertos.

## Autoridade estruturada

`data/catalog_runs/RAFAELIA_NOVOEXPORT_MEMORY_003_CHECKPOINT_2026-08-05.json`
