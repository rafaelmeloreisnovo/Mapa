# ATLAS — NOVOexport Token Genealogy Reconstruction Route — 2026-09-28

**State:** POINTER_ONLY | APPEND_ONLY | claim_allowed=false  
**Authority:** Mapa routes; Drive NOVOexport remains raw-source authority; CONVERSATIONS_CHUNKS_PRIVATE owns private derived chunks/edges.

## Intent

Provide a reconstructible route from raw NOVOexport conversation shards to private role-bound chunks, token genealogy, formulas/works and evidence without copying private conversation text into Mapa.

## Route

```text
ATLAS:NOVO:TOKEN
  -> Drive NOVOexport
  -> conversations-000..050
  -> conversation_id
  -> message_id
  -> role/timestamp
  -> CONVERSATIONS_CHUNKS_PRIVATE::memory_bridge/data/novoexport_token_chunks_*.jsonl
  -> typed edges
  -> token/concept/formula/work
  -> producer repository/file
  -> execution/evidence
  -> receipt
  -> gap / next
```

## Authority pointers

### Raw source

- Drive folder: `NOVOexport`
- Drive ID: `1P7hJq5R4fgYGEQIVNgRvllAad2lGxWEv`
- Raw shards: `conversations-000..050`
- Raw mutation policy: forbidden for derived indexing work.

### Drive reconstruction topology

- `00_INDEX`: `1C5XGG92HY3_QvEbuGYLStMdHBvCIPzUv`
- `01_ATLAS`: `1Rfj6cb_ItIAWFj9_VR3GocMiTNHJAeBe`
- `02_ROUTES`: `15EsVIToWrbL1d-yPv7ezMXaDrKZBWIKi`
- `03_MANIFOLD`: `1vIXXMdxORWl5TqRzSfySdMy9YrdzYQiv`
- `04_SCAFFOLDS`: `1FoJUzsTHA1SQwRnZs1syw61OXklR5pkX`
- `05_EDGES`: `1ICdebJ7-j111tO7_G6BImLYY0JzCI_cW`
- `06_GAPS`: `1uDuU71EGBAM9V_mwUo9WjLZGNUFv66v4`
- `07_EVIDENCE`: `1iRetxfJjJV7_y6yrxsD3Mn2gM_vjWg1v`
- `08_RECEIPTS`: `1sEPDyyapkNrVASliV2oScmJUBstkOUY6`
- `09_CONVERSATION_CHUNKS`: `1cv8r6PDtjOQk2-yAhLS3J4CfjVMt4gIW`

### Private derived registry

- repo: `rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE`
- Wave 1 PR: `#58`
- branch: `work/novoexport-token-reconstruction-v1-20260928`
- head observed when route created: `038b6b1beec49bebefbeb71254437fd046ffd241`

## Invariants

`SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`  
`USER_INPUT != ASSISTANT_OUTPUT`  
`RAW_SOURCE != DERIVED_INDEX`  
`FIRST_IN_SHARD != FIRST_IN_CORPUS`  
`CO_OCCURRENCE != EQUIVALENCE != CAUSALITY`  
`TOKEN_VAZIO != 0`

## Current evidence state

Wave 1 is bound to `conversations-045.json`. It contains role-separated literal token counts and exact source IDs for three anchor chains. It does **not** establish corpus-wide first occurrence.

Important correction preserved by route: the `ψ χ ρ Δ Σ Ω` semantic definitions in “Tokens de início RAFAELIA” are `ASSISTANT_OUTPUT` responding to a user question; they are not promoted as user lexical authorship.

## Promotion rule

`OBSERVED -> SOURCE_BOUND -> CONTEXT_BOUND -> RELATION_BOUND -> EVIDENCE_BOUND -> VERIFIED_SCOPE`.

Token-to-formula, token-to-work and token-to-repository edges remain `TOKEN_VAZIO` until an explicit source bridge exists.

## R3

`F_ok`: Drive topology + private schema/chunks/edges + Mapa route are federated by pointer.  
`F_gap`: exhaustive 51-shard genealogy and corpus-wide first-seen are open.  
`F_next`: scan remaining shards, append predecessor/successor evidence, then create work/formula/repository edges only where demonstrable.
