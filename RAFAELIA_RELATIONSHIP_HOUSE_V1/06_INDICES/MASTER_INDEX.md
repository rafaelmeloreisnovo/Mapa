# MASTER_INDEX — Relationship House V1

Status: `Ω1 + PRIVATE_LEXICAL_CHECKPOINT_V1 / claim_allowed=false`

## Canonical navigation

`objective → authority → source → evidence → projection → area/concept → relation → gap/claim → gate → delta`

| Object | Primary key | Resolves to |
|---|---|---|
| Source | `SRC-*` | digest, visibility, source class |
| Chunk | `CHK-*` | source + byte/message bounds + digest |
| Literal token | observed token | frequency + source projection; private content stays private |
| Normalized token | normalized projection | literal forms + method; never replaces literal |
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
- ALL_TOKEN public checkpoint: `06_INDICES/ALL_TOKEN_INDEX_STATUS_V1.md`
- ALL_TOKEN machine receipt: `06_INDICES/all_token_index.public.v1.json`

## ALL_TOKEN lexical checkpoint — 2026-08-23

A private source set was processed externally under a no-filter lexical contract. Only aggregate, public-safe evidence is recorded here.

Observed aggregate receipt:

- 19 message shards (`MESSAGES-00001..00019`)
- 185,953,216 message bytes
- 91,232 valid JSON messages; 0 invalid JSON records
- 1,000 distinct conversations
- 44,185,626 raw token occurrences
- 675,638 distinct literal tokens
- 612,471 distinct normalized forms
- 1,245,720 token→source frequency rows
- 27,065 explicit area/domain/field mentions
- 962 distinct structural headings
- 15,437 physical-inventory entries recognized

Identity invariant:

`LITERAL != NORMALIZED != CONCEPT != AREA != CLAIM`

The checkpoint is `COMPLETE_FOR_MOUNTED_SOURCE_SET`, **not** complete for the entire NOVOexport. The observed semantic source range is `conversations-003.json..conversations-012.json`; coverage outside that range remains unresolved.

## Current namespace state

- Capacity: A001–A136 remains a prior/provisional namespace, not a ceiling on corpus-derived areas.
- `CONFIRMED`: no area is promoted merely from lexical frequency.
- Provisional labels: recorded in `03_TAXONOMY/areas_namespace.bootstrap.json`.
- Explicit design conflicts: A004, A005, A134, A136.
- Unlisted/unevidenced slots remain `TOKEN_VAZIO`.
- Future corpus-derived families/areas MAY exceed 136 when evidence supports them; literal occurrences must remain traceable.

## Current generated/recorded indices

### Executed lexical layer

1. Private `tokens_literal` projection — 675,638 distinct literal tokens for mounted set.
2. Private `tokens_normalized` projection — 612,471 normalized forms for mounted set.
3. Private `token_source_counts` projection — 1,245,720 token→source rows.
4. Private `explicit_area_mentions` projection — 27,065 occurrences.
5. Private `structural_headings` projection — 962 distinct headings.
6. Public-safe status: `ALL_TOKEN_INDEX_STATUS_V1.md`.
7. Public-safe receipt: `all_token_index.public.v1.json`.

### Still required after complete source materialization / semantic extraction

1. `concept_to_chunk.jsonl`
2. `area_to_chunk.jsonl`
3. `formula_to_chunk.jsonl`
4. `source_to_evidence.jsonl`
5. `claim_to_evidence.jsonl`
6. `gap_to_subject.jsonl`

Generated indices are projections, not manually curated authority.

## Open TOKEN_VAZIO bridges from ALL_TOKEN V1

- `TV-RAW-OUTSIDE-003-012` — remaining private raw bytes not mounted under this execution.
- `TV-SEMANTIC-AREA-CLUSTER` — exact semantic-area count not yet derived from complete lexical coverage.
- `TV-GITHUB-FULL-TEXT` — repository full text not exhaustively tokenized in this V1.

These local bridge names do not replace the canonical `data/audits/TOKEN_VAZIO_REGISTRY.jsonl` authority.

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

Materialize the private raw source set outside `conversations-003..012`, apply the **same ALL_TOKEN contract without domain filtering**, append/merge by stable provenance, and only then derive expressions/ngrams → concepts/entities → semantic families → areas/domains → graph edges. No later projection may erase the literal occurrence or its source lineage.
