# RAFAELIA Relationship House V1

Status: `BOOTSTRAP / Ω0→Ω1`

This directory defines the evidence-first, reconstructible substrate for the RAFAELIA 136+ area relationship house.

## Invariant

`source → identity → digest → evidence → transformation → projection → claim`

A projection is never authority over its source. A metric is never a fact without its method and source-set digest. An unresolved field is `null`/`TOKEN_VAZIO`, never an invented value.

## Public/private boundary

This repository is public. Private Drive locators, raw conversations, private document IDs, credentials and restricted source contents MUST NOT be committed here. Public manifests may carry opaque source aliases and content digests only when disclosure is authorized.

## Canonical policies

- Raw sources are immutable; this tree stores pointers/manifests and deterministic projections.
- TXT chunks are UTF-8 and MUST be at most `2,000,000` bytes.
- Split order: conversation → message → content block → UTF-8-safe byte boundary.
- The semantic canonical form is a property graph/hypergraph. Tensor and manifold views are derived projections.
- The model has 17 dimensions: D1–D3 base dimensions plus D4–D17 analytical/governance dimensions.
- Unknown taxonomy slots remain `TOKEN_VAZIO`; the label `136+` is namespace capacity, not a claim that all labels are already evidenced.
- `TOKEN_VAZIO` governance is federated to the existing Mapa registry at `data/audits/TOKEN_VAZIO_REGISTRY.jsonl`.
- GeoJSON is visualization-only, never the canonical semantic graph.
- Illustrative numbers from design discussions are not observations.

## Bootstrap layout

- `00_AUTHORITY/` — contract, authority, versions and privacy boundary.
- `01_RAW_POINTERS/` — source-pointer/manifest schema.
- `02_PROJECTIONS_TXT/` — deterministic <=2 MB chunk schema.
- `03_TAXONOMY/` — versioned 136+ namespace schema.
- `04_SEMANTIC_GRAPH/` — nodes, edges, hyperedges and derived tensor-view contract.
- `05_EVIDENCE/` — evidence, claims and TOKEN_VAZIO bridge.
- `06_INDICES/` — master navigation contract.
- `07_ANALYTICS/` — reproducible metrics contract.
- `10_AUDIT/` — append-only derivation events.

## Promotion rule

`IDEA != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`

Every promotion must be supported by a reproducible artifact or remain unresolved.
