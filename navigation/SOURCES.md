# RAFAELIA — Navigation Sources, Authority and Provenance

## Purpose

This file defines how the universal navigation index resolves source authority without collapsing proximity into proof.

## Authority order

1. **Google Drive — `RAFAELIA — Master Navigation Registry V1`**  
   `SRC:DRIVE:1x_5x3_NdSaHtPLF9hbu8M1i0kvza_MnhtWeZycav19Y`  
   Longitudinal navigation authority.

2. **Google Drive — `RAFAELIA — Implementação Latentes e Papers — Drive GitHub V1`**  
   `SRC:DRIVE:1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88`  
   Operational/evidence memory and cross-source reconstruction.

3. **GitHub `rafaelmeloreisnovo/Mapa`**  
   `navigation/INDEX.md` + `navigation/RAFAELIA_MASTER_REGISTRY.v1.json`  
   Federated, inspectable GitHub mirror of the navigation model.

4. **Producer repository / concrete artifact**  
   Authority for implementation of that domain/path/ref.

5. **Receipt / run / hash / workflow evidence**  
   Evidence pointer; never automatically a scientific or runtime claim.

## Provenance rules

- Every node should eventually bind `source → owner → ref/path → observed version/hash → relation → evidence → state → next gate`.
- Similar names do not imply identity.
- Search hits do not establish canonical authority.
- `structural_owner != human_owner` unless explicitly proven.
- A receipt is immutable evidence of an observation, not proof beyond its stated scope.
- A PR in `OPEN` state is a proposal/working edge, not canonical implementation.
- A merged commit can establish repository state but not physical execution unless execution evidence is bound.
- Missing evidence is recorded as `TOKEN_VAZIO`.

## Deduplication policy

Drive and GitHub candidates are deduplicated only when sufficient identity evidence exists. Prefer:

1. exact document/repository ID;
2. exact hash/ref/version;
3. explicit mirror/derived-from declaration;
4. content fingerprint plus provenance;
5. title/name similarity only as a candidate relation.

Unresolved duplicates remain separate nodes with `possible_same_as=TOKEN_VAZIO` rather than being collapsed.

## Temporal indexing

Temporal snapshots are leaves of the universal graph.

`TS:2026-08-21:5H → navigation/GITHUB_DELTA_5H_20260821.md`

The 5-hour file answers a historical status question only. It is **not** the root index and does not constrain universal coverage.

## Coverage discipline

Observed GitHub repository inventory in the current pass: `84`.

This is not treated as an exhaustive proof of every account/repository/file, therefore:

`github_inventory_complete=TOKEN_VAZIO`

Drive search returned many RAFAELIA-related candidates, but deduplication, authority classification and full-content coverage are not closed:

`drive_inventory_complete=TOKEN_VAZIO`

## Append-only lineage

When an item changes:

`old_state → new_observation → evidence → gate → new_state`

The old state remains addressable. Use `SUPERSEDES` instead of erasing historical truth.

## Safety invariants

- `OPEN != CANONICAL`
- `TOKEN_VAZIO != PASS`
- `VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`
- `SEARCH_HIT != AUTHORITY`
- `MERGED != PHYSICAL_RUNTIME`
- `COHERENCE != CLAIM_AUTHORITY`

## Current expansion frontier

`repository inventory → artifact inventory → evidence binding → Drive dedupe → gap/falsifier binding → cross-repo causal navigation`
