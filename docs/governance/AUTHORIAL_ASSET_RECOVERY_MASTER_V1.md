# RAFAELIA — Authorial Asset Recovery Master V1

**Status:** `RESTORE_AND_AUDIT / claim_allowed=false`  
**Canonical human author:** Rafael Melo Reis  
**Date:** 2026-09-20

## Mission

Bring every known work, research object, code artifact, document, dataset, conversation-derived artifact, formula, figure, receipt, hash, commit, archive and other candidate asset back into a navigable provenance graph associated with Rafael Melo Reis **without converting repository control into false authorship**.

The recovery operation is:

```text
DISCOVER
→ IDENTIFY
→ SOURCE
→ HASH/REF
→ CLASSIFY_RIGHTS
→ LINK_PROVENANCE
→ DEDUP
→ RECEIPT
→ CLAIM_ONLY_IF_EVIDENCED
```

## Current observed surface

- GitHub personal namespace: **86 repositories**
- GitHub institutional namespace: **47 repositories**
- Total observed repository surface: **133 repositories**
- Drive canonical navigator: `RAFAELIA_DATA_NAVIGATOR`, 15 first-level control folders observed
- Drive census: **154 folder nodes / 893 entries observed** across the governed Navigator/NOVOexport route
- Three private directories hit the connector cap of 100 entries and remain `TOKEN_VAZIO_PAGINATION_PENDING`
- NOVOexport manifest denominator: **15,439 physical files / 15,369 logical files / 25,132,295,924 declared bytes**

## What is being restored

1. **Authorial expression:** texts, books, manifestos, papers, documentation, figures, diagrams and original source code.
2. **Research provenance:** formulas, hypotheses, models, discoveries, observations, experiments and notebooks; abstract ideas/mathematics remain provenance objects rather than automatic copyright claims.
3. **Software:** original RAFAELIA/RAFCODE modules tracked separately from forks, upstreams and dependencies.
4. **Data/corpus:** datasets, NOVOexport/conversation corpora, indices and compilations under privacy/contract/source constraints.
5. **Evidence:** commits, hashes, receipts, CI runs, timestamps, archives and chain-of-custody records.
6. **Personal data:** indexed only to the extent needed for custody/identity; not made public or copied into public registries by this recovery.
7. **Third-party/mixed material:** preserved with upstream attribution and license; never absorbed into Rafael authorship by namespace alone.

## Immediate canonical routes

- `docs/legal/BERNE_AUTHORIAL_SCOPE_ROLLBACK_V2.md`
- `docs/legal/DECLARACAO_UNIVERSAL_PROTECAO_ACESSO_PROVENIENCIA_V1.md`
- `data/authorship/AUTHORIAL_ASSET_RECOVERY_REGISTRY_V1.json`
- `governance/authorship/AUTHORSHIP_PROVENANCE_REGISTRY.v1.json`
- `governance/authorship/COPYRIGHT_AUDIT_V1.jsonl`

## Fail-closed rules

```text
NAMESPACE != COPYRIGHT
FORK != NEW_AUTHORSHIP
REFACTOR != CLEAN_ROOM
FORMULA_PROVENANCE != COPYRIGHT_OF_ABSTRACT_MATH
PRIVATE_DATA != PUBLIC_ASSET
SEARCH_MISS != ABSENCE
TOKEN_VAZIO != CLEARED
```

## R3

**F_ok:** 133 repository surfaces reattached to the authorial recovery graph; Drive canonical navigator and primary indexes reattached; universal declaration restored as an active author statement subordinate to artifact-specific rights.  
**F_gap:** pagination of three 100-item private folders, cross-provider deduplication and file-level copyright/contributor evidence remain incomplete; private corpus bodies stay restricted.  
**F_next:** resolve the three pagination-bounded private folders through manifest/provider IDs, then promote assets one-by-one from candidate → evidenced state, preserving upstream boundaries.
