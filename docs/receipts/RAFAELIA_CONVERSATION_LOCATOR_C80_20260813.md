# RAFAELIA — Conversation Locator Ω — Receipt C80 — 2026-08-13

State: `VERIFIED_LIMITED`

Claim gate: `claim_allowed=false`

Mode: `APPEND_ONLY / PRIVACY_BY_DEFAULT / DETERMINISTIC_DERIVATION / SOURCE_READ_ONLY`

## Authority and source

- custody contract: `data/indexes/conversation-custody-policy.v1.json`
- source ZIP SHA-256: `53fbfbc52d110d5815024ca851868555d23c3180cd73bb5433dd5f5bade9d93f`
- `conversations.json` SHA-256: `d2db8b130ed968b1b94768d98f6e1fcdba52233dc846b9b94a63749cee14b7cf`
- `conversations.json` bytes: `792693581`
- source rewrite: `false`

## Privacy contract

The derived locator stores no raw conversation IDs, titles or message bodies. Conversation identity is represented by SHA-256 pseudonyms. Title values are not stored; only title SHA-256 is retained. Semantic topic classification remains `TOKEN_VAZIO_PRIVACY_REVIEW_PENDING` rather than deriving sensitive labels without a dedicated privacy gate.

## Deterministic execution

Two complete derivations were executed independently from the same source archive.

- run 1 index SHA-256: `c227ebfc85fdf326bd9143ec1edfc884fe0e16c3f6f6671e37a0fc043b425c02`
- run 2 index SHA-256: `c227ebfc85fdf326bd9143ec1edfc884fe0e16c3f6f6671e37a0fc043b425c02`
- result: `BYTE_IDENTICAL_TWO_RUNS`
- index records: `2573`
- index bytes: `1734374`
- full derived manifest SHA-256: `ce6cc7390d87b46f719a9f11e12084087d9626ace453dddd2ec186cbb602caa4`

Observed aggregates:

- mapping nodes: `242079`
- messages with payload: `239506`
- roles: assistant `116174`; system `15701`; tool `22367`; user `85264`
- duplicate pseudonym count: `0`
- create time range: `2025-02-12T00:08:06.258886Z` through `2025-10-06T16:30:36.847311Z`
- latest update: `2025-10-06T21:40:42.753734Z`

## Locator shard gate

The full deterministic index was reduced into monthly locator shards containing only pseudonymized identity, source index, timestamps, topology counts, title hash, topic TOKEN_VAZIO and claim gate.

Validator result:

`PASS / records=2573 / unique_pids=2573 / source_index=0..2572 / errors=[] / claim_allowed=false`

Locator manifest SHA-256: `8050c1f988063e188df0412b2c8cb48ba4f9b7b0e5363cec0073ec02bb0305f1`.

A second shard build from the independently regenerated index produced a byte-identical manifest and identical shard directory.

## Drive materialization

Historical first import:

- provider ID: `1kUku3qtl-u4H0ppQwEieTLgIUtqgqPJueMboYDCwOQw`
- state: `SUPERSEDED_REPRESENTATION`
- reason: Google Sheets displayed imported UTC timestamp cells as spreadsheet serials; source/index bytes were not changed.

Canonical locator candidate V1.1:

- provider ID: `12MFNN72gG4Uvs76lOtIFF20odpfW2-MU1lQ5wxZJK8g`
- native Google Sheet: yes
- Locator grid rows: `2574` = header + `2573` records
- timezone normalized: `Etc/UTC`
- timestamp display normalized: ISO-8601 UTC to milliseconds
- first-row and last-row provider readback: observed
- raw private messages/titles: absent from locator columns

Provider readback proves materialization and structural coverage; it is not a byte-for-byte proof of every Google Sheets cell against the local JSONL.

## TOKEN_VAZIO delta

Resolved:

- `TOKEN_VAZIO_CONVERSATION_ID_INDEX_REMOTE` -> `RESOLVED_BY_PRIVATE_DRIVE_LOCATOR_V1_1`

Still open:

- `TOKEN_VAZIO_SEMANTIC_TOPIC_PRIVACY_REVIEW`
- `TOKEN_VAZIO_CHUNK_GRAPH_MATERIALIZATION`
- `TOKEN_VAZIO_CROSS_EXPORT_DEDUP`
- `TOKEN_VAZIO_PROVIDER_CELLWISE_EXACT_RECONCILIATION`

## F_ok

Exact source identity, deterministic two-run derivation, privacy-preserving 2573-record locator, fail-closed local validator, private Drive materialization and provider structural readback.

## F_gap

Semantic topic derivation remains intentionally blocked pending privacy review; chunk-level graph and cross-export dedup are not materialized; provider-wide cell-by-cell equality is not claimed.

## F_next

Use the locator to select a bounded set by time/PID first. Only then open corresponding raw source objects privately and create graph nodes/edges with evidence refs. In parallel, define a privacy-reviewed semantic carrier contract before adding topic labels.

No automatic publication, public payload release or scientific claim is authorized by this receipt.
