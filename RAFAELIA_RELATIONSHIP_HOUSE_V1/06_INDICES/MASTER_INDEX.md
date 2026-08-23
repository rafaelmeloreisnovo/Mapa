# MASTER_INDEX — Relationship House V1

Status: `BOOTSTRAP / no corpus ingested yet`

## Canonical navigation

`objective → authority → source → evidence → projection → area/concept → relation → gap/claim → gate → delta`

| Object | Primary key | Resolves to |
|---|---|---|
| Source | `SRC-*` | digest, visibility, source class |
| Chunk | `CHK-*` | source + byte/message bounds + digest |
| Area | `A###` | taxonomy version + evidence |
| Node | stable graph ID | areas + evidence + derivations |
| Edge | stable graph edge ID | source/destination/relation + evidence |
| Evidence | `EV-*` | source digest + public-safe locator |
| Claim | `CLAIM-*` | evidence set + falsifier + promotion state |
| Gap | `GAPBR-*` | existing Mapa `TOKEN_VAZIO` ID |
| Derivation | append-only event ID | input digests + transform + outputs |

## Authority

- Bootstrap entry: `bootstrap/RAFAELIA_CHATGPT_BOOTSTRAP_V1.md`
- TOKEN_VAZIO authority: `data/audits/TOKEN_VAZIO_REGISTRY.jsonl`
- Relationship House contracts: `RAFAELIA_RELATIONSHIP_HOUSE_V1/00_AUTHORITY/`
- Private longitudinal sources: external/private authority; never copied into this public index.

## Current namespace state

- Capacity: A001–A136.
- `CONFIRMED`: none at bootstrap; confirmation requires corpus/source evidence.
- Provisional labels: recorded in `03_TAXONOMY/areas_namespace.bootstrap.json`.
- Explicit design conflicts: A004, A005, A134, A136.
- Unlisted slots: `TOKEN_VAZIO`.

## Required generated indices after first ingestion

1. `concept_to_chunk.jsonl`
2. `area_to_chunk.jsonl`
3. `formula_to_chunk.jsonl`
4. `source_to_evidence.jsonl`
5. `claim_to_evidence.jsonl`
6. `gap_to_subject.jsonl`

These files MUST be generated from manifests; they are projections, not manually curated authority.

## Gate sequence

1. `G0_SOURCE_DIGEST` — source identity and digest present.
2. `G1_CHUNK_INTEGRITY` — UTF-8, <=2,000,000 bytes, source linkage, digest.
3. `G2_EVIDENCE_LINK` — every promoted graph record has evidence or remains TOKEN_VAZIO/HYPOTHESIS.
4. `G3_TAXONOMY_CONSISTENCY` — no area-ID collision promoted silently.
5. `G4_METRIC_REPRODUCIBILITY` — algorithm/version/source-set digest/support present.
6. `G5_CLAIM_PROMOTION` — falsifier/evidence policy satisfied before claim_allowed=true.
7. `G6_PUBLIC_BOUNDARY` — no private locator/content leaked into public projection.

## Stop conditions

Stop promotion and create/federate `TOKEN_VAZIO` when evidence is absent, conflicting, private-withheld, stale, unparsable or non-reproducible.

## Next executable delta

Build a manifest generator against an explicitly authorized source set, emit the first `SRC-*` records, then produce deterministic chunks and run G0/G1 before semantic extraction.
