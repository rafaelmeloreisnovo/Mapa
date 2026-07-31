# Índice — FAROL-Σ Conversation Custody First Layer V1

**Evento:** `FAROL-SIGMA-CONVERSATION-CUSTODY-V1-20260730`  
**Estado:** `LOCAL_REFERENCE_VALIDATED · SOURCE_REASSEMBLY_PENDING`  
**Claim:** `false`

## Fontes do Google Drive observadas

| Objeto | ID | Papel | Estado |
|---|---|---|---|
| `ARQUITETURA_ABRANGENTE_INTERPRETATIVA_V2_DERIVADA_DE_CONVERSAS` | `1DQW0le_acpBDOB76Vc-r8jy0AyvdD4gM` | raiz numerada | `SOURCE_TREE_OBSERVED_DEPTH_2` |
| `00_CATALOGO` | `1tw8Sdh81SxcjNDRy3azcrgx29ZeOgQs0` | catálogo humano | `ROUTE_SELECTED` |
| `04_CONVERSATIONS_ESTRUTURADAS` | `1mF0iIJVgvbGC0KNUZU5H82IIQuVA-Gop` | derivados estruturados | `ROUTE_SELECTED` |
| `07_AUDITORIA_E_PROVENIENCIA` | `1LcpaKk2FF_cpOLKav5jzBpc6V_q7M8_F` | custódia e receipts | `ROUTE_SELECTED` |
| `09_INDICES_HUMANO_E_IA` | `1HOP3fmeTsmITy30BV2dkNryH7D-U29qm` | índices de recuperação | `ROUTE_SELECTED` |
| `CONVERSATIONS_CHUNKS_PRIVATE` | `1TdrEcICmejWaLvsdU7uFd44Uj9NRVjuN` | genealogia privada | `PRIVATE_SOURCE_AUTHORITY` |
| `conversations_chunk_01.json` | `1IS-XFlcorZsDag9HtXO4tZyA4DquvYOc` | fragmento 01 | `TOKEN_VAZIO_REASSEMBLY_REQUIRED` |

## Evidência do fragmento 01

```text
bytes  = 94.371.840
sha256 = 72886416eb73cb4bb8fb5beabe828f9e0582995296e1111393043cc6fa19ada3
first_non_whitespace = "
last_non_whitespace  = -
standalone_json       = false
```

Nenhum corpo privado foi copiado para o Mapa.

## Entrada técnica

| Função | Caminho |
|---|---|
| arquitetura | `docs/architecture/FAROL_SIGMA_CONVERSATION_CUSTODY_V1.md` |
| política | `data/indexes/conversation-custody-policy.v1.json` |
| schema | `schemas/conversation-custody-index.schema.json` |
| indexador | `scripts/index_conversations_export.py` |
| testes | `tests/test_index_conversations_export.py` |
| receipt local | `auditoria/CONVERSATION_CUSTODY_LOCAL_RECEIPT_20260730.json` |

## Gate atual

```text
SOURCE_FRAGMENT_HASHED               PASS
SOURCE_UNMODIFIED                     PASS
PRIVACY_PRESERVING_INDEXER            IMPLEMENTED
LOCAL_TESTS                            PASS
COMPLETE_ORDERED_REASSEMBLY            TOKEN_VAZIO
REAL_EXPORT_INDEX_RUN                  TOKEN_VAZIO
TERMUX_RECEIPT                         TOKEN_VAZIO
INDEPENDENT_PRIVACY_REVIEW             TOKEN_VAZIO
claim_allowed                          false
```

## F_next

Localizar todas as partes ou o `conversations.json` original, verificar ordem e SHA-256 lógico, executar localmente e comparar contagens sem publicar títulos, textos, identificadores pessoais ou inferências sensíveis.
