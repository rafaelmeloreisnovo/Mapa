# NOVOexport RAW018 — Wave 3 PID Reconciliation — 2026-08-24

## Estado

`PARTIAL_EVIDENCED_PID_SET_CURRENT_BYTE_CUSTODY_OPEN`

`claim_allowed=false`

A Wave 3 refina, sem reescrever, a Wave 2. O gap composto antigo é separado por dimensão:

| Dimensão | Estado |
|---|---|
| `RAW018_PID_HASH_SET` | `EVIDENCED_RECONCILED_100_PRIVACY_PRESERVING` |
| `RAW018_CURRENT_PROVIDER` | `TOKEN_VAZIO_HARD_CUSTODY` |
| `RAW018_CURRENT_BYTES` | `TOKEN_VAZIO_HARD_CUSTODY` |
| `RAW018_CURRENT_SHA256` | `TOKEN_VAZIO_HARD_CUSTODY` |
| `RAW018_CURRENT_JSON_PARSE` | `TOKEN_VAZIO_HARD_CUSTODY` |

## Evidência composta

O conjunto não foi promovido por cardinalidade isolada.

1. O Locator histórico contém 2.573 PIDs hashados.
2. O índice atual `000..047 except 018` contém 4.698 PIDs hashados.
3. A interseção histórica-atual é 2.473.
4. A diferença `historical - current` é exatamente 100.
5. Os 100/100 candidatos ficam estritamente entre as fronteiras temporais observadas nos shards físicos adjacentes:
   - fim de RAW017: `2025-08-04T07:36:49.264419Z`;
   - início de RAW019: `2025-08-09T16:00:53.999997Z`.
6. Um export histórico independente, byte-backed, contém 100/100 desses PIDs.
7. Os timestamps do witness histórico concordam 100/100 com o Locator dentro da precisão de milissegundos.

## Compromissos públicos, sem lista de PIDs

- candidate set: `766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e`
- ordem temporal: `c29cbc493b2401d0d875a49a71999f4b32f8b3faab8a86cd2c1d9a4e4ca83706`
- objetos do witness histórico: `f14cd8767241255d64dba51b818e1bf3d5eefb6af157f1b321199cb102223156`

A lista de 100 hashes e IDs brutos não é publicada neste repositório.

## Falsificadores preservados

- Adjacência no export histórico não reproduz a ordem do sharding atual: hipótese rejeitada.
- Janela temporal sozinha não estabelece identidade.
- Cardinalidade 100 sozinha não estabelece identidade.
- `MESSAGES-00018.jsonl.txt` não substitui `conversations-018.json`.
- Search miss não prova ausência global.

## Limite atual

A Wave 3 **não** produz o SHA-256 de `conversations-018.json` e **não** afirma possuir os bytes atuais do shard.

O fechamento de custódia exige:

`current byte witness → 12,115,336 bytes → SHA256 → JSON parse fail-closed → PID hash set → commitment == 766644...`

## F_ok

`RAW018_PID_HASH_SET = EVIDENCED_RECONCILED_100_PRIVACY_PRESERVING`.

## F_gap

`CURRENT_PROVIDER + CURRENT_BYTES + CURRENT_SHA256 + CURRENT_JSON_PARSE = TOKEN_VAZIO_HARD_CUSTODY`.

## F_next

Recuperar um witness imutável dos bytes atuais do RAW018 e comparar deterministically seu PID-set ao commitment congelado nesta Wave.
