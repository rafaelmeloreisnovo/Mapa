# RAFAELIA Relationship House V1

Status: `Ω1 / PRIVATE_LEXICAL_CHECKPOINT_V1 / claim_allowed=false`

This directory defines the evidence-first, reconstructible substrate for the RAFAELIA relationship house and now records the first executed private lexical checkpoint without copying the private corpus into this public repository.

## Invariant

`source → identity → digest → evidence → transformation → projection → claim`

A projection is never authority over its source. A metric is never a fact without its method and source-set digest. An unresolved field is `null`/`TOKEN_VAZIO`, never an invented value.

Lexical identity invariant:

`LITERAL != NORMALIZED != CONCEPT != AREA != CLAIM`

## Public/private boundary

This repository is public. Private Drive locators, raw conversations, private document IDs, credentials and restricted source contents MUST NOT be committed here. Public manifests may carry opaque source aliases and aggregate receipts only when disclosure is authorized.

The ALL_TOKEN checkpoint records aggregate execution evidence only. Literal token tables, token→source rows and private source-level manifests remain private/external.

## Canonical policies

- Raw sources are immutable; this tree stores pointers/manifests and deterministic projections.
- TXT chunks are UTF-8 and MUST be at most `2,000,000` bytes.
- Split order: conversation → message → content block → UTF-8-safe byte boundary.
- The semantic canonical form is a property graph/hypergraph. Tensor and manifold views are derived projections.
- The model has 17 dimensions: D1–D3 base dimensions plus D4–D17 analytical/governance dimensions.
- Unknown taxonomy slots remain `TOKEN_VAZIO`; the label `136+` is a prior namespace capacity, not a ceiling on future corpus-derived semantic families/areas.
- `TOKEN_VAZIO` governance is federated to the existing Mapa registry at `data/audits/TOKEN_VAZIO_REGISTRY.jsonl`.
- GeoJSON is visualization-only, never the canonical semantic graph.
- Illustrative numbers from design discussions are not observations.
- ALL_TOKEN literal indexing preserves stopwords, symbols, punctuation, repetitions and provenance before semantic classification.

## Executed ALL_TOKEN checkpoint

See:

- `06_INDICES/ALL_TOKEN_INDEX_STATUS_V1.md`
- `06_INDICES/all_token_index.public.v1.json`
- `06_INDICES/MASTER_INDEX.md`

Public-safe aggregate receipt for the mounted private source set:

- 19 message shards
- 185,953,216 message bytes
- 91,232 valid JSON messages / 0 invalid
- 1,000 distinct conversations
- 44,185,626 raw token occurrences
- 675,638 distinct literal tokens
- 612,471 normalized forms
- 1,245,720 token→source rows
- 27,065 explicit area/domain/field mentions
- 962 distinct structural headings

This is `COMPLETE_FOR_MOUNTED_SOURCE_SET`, not total NOVOexport coverage. Raw coverage outside `conversations-003..012` remains `TOKEN_VAZIO` until materialized under the same contract.

## Layout

- `00_AUTHORITY/` — contract, authority, versions and privacy boundary.
- `01_RAW_POINTERS/` — source-pointer/manifest schema.
- `02_PROJECTIONS_TXT/` — deterministic <=2 MB chunk schema.
- `03_TAXONOMY/` — versioned namespace schema; corpus-derived areas may extend prior capacity when evidenced.
- `04_SEMANTIC_GRAPH/` — nodes, edges, hyperedges and derived tensor-view contract.
- `05_EVIDENCE/` — evidence, claims and TOKEN_VAZIO bridge.
- `06_INDICES/` — master navigation plus ALL_TOKEN lexical checkpoint.
- `07_ANALYTICS/` — reproducible metrics contract.
- `10_AUDIT/` — append-only derivation events.

## Promotion rule

`IDEA != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`

Every promotion must be supported by a reproducible artifact or remain unresolved.
