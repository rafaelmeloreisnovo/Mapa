# Receipt — Drive Authorial Census + Personal Corpus Custody — 2026-09-20

state: METADATA_CENSUS_BOUNDED_COMPLETE_WITH_PAGINATION_GAPS  
claim_allowed: false  
privacy: PRIVATE_BODIES_NOT_COPIED

## GitHub surface

- personal namespace repositories: 86
- institutional namespace repositories: 47
- total repository surfaces observed: 133

## Drive census executed in this recovery

- RAFAELIA_DATA_NAVIGATOR first-level sectors: 15
- census snapshot files materialized: 26
- folder nodes directly inspected: 154
- directory entries observed across inspected nodes: 893
- ordinary scanned folders at 100-item cap: none
- private folders at 100-item cap:
  - NOVOexport_INDEX/MEMORY_PRIVATE
  - NOVOexport_INDEX/PIPELINE_STATE
  - NOVOexport_INDEX/CHUNKS_PRIVATE

These three remain `TOKEN_VAZIO_PAGINATION_PENDING`; no false completeness claim is made.

## Manifest-backed private corpus denominator

Verified from `CONVERSATIONS_CHUNKS_PRIVATE/auditoria/RAFAELIA_NOVOEXPORT_CATALOG_IMPLEMENTATION_V1_20260822.json`:

- physical files: **15,439**
- logical files: **15,369**
- declared bytes: **25,132,295,924**
- conversation shards: **51** (`conversations-000..050`)
- declared conversation-family bytes: **1,107,289,897**
- Codex shards: **21**
- asset-name records: **14,973**
- library records: **3,470**
- raw corpus bodies committed to the private catalog repository: **false**

## Recovery meaning

This census reattaches custody and navigation. It does **not** declare that every observed object is authored by Rafael Melo Reis.

```text
CUSTODY != AUTHORSHIP
NAMESPACE != COPYRIGHT
PRIVATE_CORPUS != PUBLIC_ASSET
MANIFEST_COUNT != FILE_LEVEL_RIGHTS_PROOF
```

## R3

F_ok: GitHub repository surface + Drive control tree + NOVOexport denominator reattached to one recovery route.  
F_gap: pagination for three 100-item private folders; per-file authorship/rightsholder classification; cross-provider dedup.  
F_next: use manifest/provider IDs and file-level Git history to promote only evidenced assets to AUTHORIAL_PROVEN.
