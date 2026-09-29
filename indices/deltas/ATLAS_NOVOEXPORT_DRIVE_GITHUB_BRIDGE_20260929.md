# ATLAS — NOVOexport Drive ↔ Mapa GitHub Bridge — 2026-09-29

**State:** POINTER_ONLY | APPEND_ONLY | claim_allowed=false  
**Intent:** Create a bounded, reconstructible route between the Google Drive NOVOexport source and the GitHub Mapa authority index without copying the raw corpus.

## Route card

- **Objective:** Navigate from the Drive source and its canonical index to the corresponding Mapa route and evidence.
- **Mode:** map / read-only source inspection; append-only map artifact.
- **Target:** Drive folder `NOVOexport` ↔ repository `rafaelmeloreisnovo/Mapa`.
- **Authority:** Drive owns source files and editorial navigation; Mapa owns cross-source routing, typed relations, and the evidence boundary; producer repositories own implementation.
- **Evidence state:** DOCUMENTED + provider metadata observed; source bytes and corpus completeness were not revalidated in this delta.
- **Gate:** pointers must resolve; no source contents or claims are promoted by the existence of this map.

## Exact source and index pointers

| Object | Stable identifier | Role |
|---|---|---|
| Google Drive source folder `NOVOexport` | `1P7hJq5R4fgYGEQIVNgRvllAad2lGxWEv` | Raw corpus/source boundary |
| Drive `00_INDEX` | `1C5XGG92HY3_QvEbuGYLStMdHBvCIPzUv` | Canonical navigation directory |
| Drive START HERE Ω | `1HWse8jj9PAz1zMFv2KW6Qv5-mfk8iBkNBQopmBAcook` | Reconstruction router; records the shard/message baseline and next route |
| Drive bridge artifact | `1TulThGJys7tJ2A8NGoqV7YbW2VYGlLN0` | This map in Drive `01_ATLAS`; uploaded as a linked successor artifact |
| GitHub repository | `rafaelmeloreisnovo/Mapa` | Cross-surface map, provenance, routes, gates |
| GitHub branch origin | `main@21c2f9aefab86cd31b8ea7da22533452690fd087` | Main head used when this branch was created; current merge base |
| Pull request | `#708` | Open PR; branch `atlas/novoexport-drive-github-bridge-20260929`; current base at inspection `main@6e705d38bedd352b97be7c8c2c8924f3bdabed54` |
| PR comparison | `main...atlas/novoexport-drive-github-bridge-20260929` | Diverged from its creation base; GitHub reported `mergeable=true` at readback. Recheck before merge |
| Existing source-universe index | `indices/NOVOEXPORT_ACTIVE_V2_SOURCE_UNIVERSE_20260907_V1.md` | Historical manifest-scope evidence and open gaps |
| Existing reconstruction route | `indices/deltas/ATLAS_NOVOEXPORT_TOKEN_GENEALOGY_ROUTE_20260928.md` | Drive-to-private-chunks route and authority boundary |
| This bridge delta | `indices/deltas/ATLAS_NOVOEXPORT_DRIVE_GITHUB_BRIDGE_20260929.md` | This map's GitHub-side record |

Drive links: [NOVOexport folder](https://drive.google.com/drive/folders/1P7hJq5R4fgYGEQIVNgRvllAad2lGxWEv) · [START HERE Ω](https://docs.google.com/document/d/1HWse8jj9PAz1zMFv2KW6Qv5-mfk8iBkNBQopmBAcook/edit) · [this Drive bridge artifact](https://drive.google.com/file/d/1TulThGJys7tJ2A8NGoqV7YbW2VYGlLN0/view)  
GitHub links: [Mapa](https://github.com/rafaelmeloreisnovo/Mapa) · [this bridge PR](https://github.com/rafaelmeloreisnovo/Mapa/pull/708) · [source-universe index](https://github.com/rafaelmeloreisnovo/Mapa/blob/main/indices/NOVOEXPORT_ACTIVE_V2_SOURCE_UNIVERSE_20260907_V1.md) · [reconstruction route](https://github.com/rafaelmeloreisnovo/Mapa/blob/main/indices/deltas/ATLAS_NOVOEXPORT_TOKEN_GENEALOGY_ROUTE_20260928.md)

## Drive navigation topology observed

The folder listing returned 100 direct items. The canonical numbered navigation folders below were present. The listed responsibilities are routing labels; folder contents were not audited here. This bounded listing is not a complete inventory of the 15,000+ source objects.

| Folder | Drive ID | Navigation responsibility |
|---|---|---|
| `00_INDEX` | `1C5XGG92HY3_QvEbuGYLStMdHBvCIPzUv` | Entry point and current route |
| `01_ATLAS` | `1Rfj6cb_ItIAWFj9_VR3GocMiTNHJAeBe` | Cross-source map artifacts |
| `02_ROUTES` | `15EsVIToWrbL1d-yPv7ezMXaDrKZBWIKi` | Reconstructible workflows |
| `03_MANIFOLD` | `1vIXXMdxORWl5TqRzSfySdMy9YrdzYQiv` | Typed relation graph |
| `04_SCAFFOLDS` | `1FoJUzsTHA1SQwRnZs1syw61OXklR5pkX` | Templates and structural supports |
| `05_EDGES` | `1ICdebJ7-j111tO7_G6BImLYY0JzCI_cW` | Edge records and provenance |
| `06_GAPS` | `1uDuU71EGBAM9V_mwUo9WjLZGNUFv66v4` | Open questions and exact next probes |
| `07_EVIDENCE` | `1iRetxfJjJV7_y6yrxsD3Mn2gM_vjWg1v` | Evidence pointers and bounded results |
| `08_RECEIPTS` | `1sEPDyyapkNrVASliV2oScmJUBstkOUY6` | Execution and change receipts |
| `09_CONVERSATION_CHUNKS` | `1cv8r6PDtjOQk2-yAhLS3J4CfjVMt4gIW` | Derived chunk storage; check its access contract before processing |

Other direct folders were also observed, including `RAFAELIA_CONVERSATION_MANIFOLD_V1`, `03_ATLAS_DAT_SEMANTIC_VOID_V1`, `02_CONVERSAS_SOLTAS_QUARENTENA`, `01_SISTEMA_CORPUS_CUSTODIA`, `NOVOEXPORT_CUSTODY_LEDGER_OMEGA`, and `AUDIT_NOVOexport_Temporal_Varredura_20260822`. They remain adjacent source/support directories; this map does not move, merge, or reclassify their contents.

## Typed route

```text
Drive/NOVOexport [SOURCE]
  -> Drive/00_INDEX/START HERE Ω [NAVIGATION]
  -> Drive/09_CONVERSATION_CHUNKS [DERIVED ARTIFACTS; private scope applies]
  -> Drive/05_EDGES + 03_MANIFOLD [TYPED RELATIONS]
  -> Drive/02_ROUTES + 01_ATLAS [RECONSTRUCTION]
  -> Drive/07_EVIDENCE + 08_RECEIPTS [EVIDENCE / EXECUTION RECORDS]
  -> Drive/06_GAPS [OPEN ITEMS]
  -> GitHub/Mapa indices and validators [ROUTING AUTHORITY]
  -> producer repository / exact artifact [IMPLEMENTATION AUTHORITY]
```

| Edge | From | To | Gate |
|---|---|---|---|
| `SOURCE_OF` | Drive folder ID above | source shards / export objects | Verify current provider identity before processing |
| `INDEXES` | Drive START HERE Ω | numbered Drive topology | Index is navigation, not source-byte proof |
| `ROUTES_TO` | Mapa NOVOexport route | private derived chunks and typed edges | Keep raw source separate; do not copy private conversation text into Mapa |
| `DOCUMENTS_SCOPE` | Mapa ACTIVE_V2 index | physical manifest snapshot | Snapshot is historical documentation until exact source/hash is re-read |
| `POINTS_TO` | Mapa | producer repo and receipt | No implementation or execution claim from a pointer alone |

## Current state and epistemic limits

The Drive START HERE document records 51 conversation shards, 5,054 roots, 5,052 non-empty conversations, 2 empty placeholders, 111,367 user messages, and 185,427 assistant messages. These figures are reproduced as **documented baseline values**, not independently recounted here.

The Mapa ACTIVE_V2 index records a 15,439-entry physical manifest snapshot, 15,369 logical files, and open gaps `TV-INDEX-INGEST-000-050` and `TV-MESSAGES-FULL-COVERAGE`. This delta links that existing record; it does not revalidate its hashes or establish semantic exhaustivity.

Invariants:  
`SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`  
`RAW_SOURCE != DERIVED_INDEX`  
`USER_INPUT != ASSISTANT_OUTPUT`  
`CO_OCCURRENCE != EQUIVALENCE != CAUSALITY`  
`TOKEN_VAZIO != 0`

## Query and topology audit

- Drive target resolution: exact folder ID and Drive account `rafaelmeloreis@gmail.com`.
- Drive inspection: direct folder listing, capped at 100 items; START HERE Ω text read.
- GitHub inspection: exact repository, `main` head, and the two existing NOVOexport route documents.
- Search and cache behavior: no corpus-wide content query, cache implementation, cache hit-rate, or performance experiment was part of this map. Cache/performance lane: `NOT_NEEDED` for pointer-only indexing.

## Evolution gate

- **Baseline:** existing Drive START HERE and Mapa routes remain intact.
- **H1:** one append-only bridge improves navigation if Drive IDs, GitHub paths, and authority boundaries resolve.
- **H0:** the bridge adds no value if it duplicates a current canonical route or introduces stale/ambiguous pointers.
- **Acceptance:** confirm both pointers resolve and preserve the source/derived/evidence boundaries.
- **Rollback:** revert this PR and record a Drive map successor if correction is needed; do not delete historical records or modify raw source shards.

## Open gaps and next probe

- `TOKEN_VAZIO_CURRENT_SOURCE_HASH`: re-read the exact current export manifest and bind its provider file ID, byte scope, and digest to a new receipt.
- `TOKEN_VAZIO_FULL_INVENTORY`: paginate or otherwise verify the complete direct-child/member inventory; the 100-item listing is bounded.
- `TOKEN_VAZIO_SEMANTIC_COVERAGE`: validate shard/message coverage independently before promoting corpus-wide genealogy.

## R3

- **F_ok:** exact Drive folder, START HERE, and uploaded map artifact pointers resolved; canonical numbered hierarchy observed; PR #708 is open and reported mergeable.
- **F_gap:** full current member inventory and exact current source-manifest hash remain unresolved; prior counts are documented, not remeasured.
- **F_next:** obtain the PR review/CI result, then revalidate the current manifest hash and full inventory in a successor receipt.
