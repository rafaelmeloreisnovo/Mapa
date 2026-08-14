# RAFAELIA Ω — Knowledge Hypervisor / Biblioteca Virtual — Mapa V0.1

State: `BRAINSTORM_GOVERNED / DECISION_PENDING / CLAIM_ALLOWED=false`

## Purpose

Mapear, sem canonizar, a proposta de virtualização da biblioteca RAFAELIA para recuperação bounded/lazy entre sessões.

## Candidate topology

`ROOT Ω → Mount Table → Identity Table → Semantic Graph → Skill Graph → Evidence Graph → Active Working Set → Append-only Δ`

## Candidate invariants

- `identity != name != physical_location`
- `filesystem_tree != knowledge_graph`
- one canonical content identity may have many aliases/locations
- memory/index/symbol are not evidence
- `TOKEN_VAZIO` remains explicit
- only bounded evidence windows should be opened by default
- append-only deltas preserve historical states

## Candidate typed object

`K_i = <ID, Identity, Meaning, Relations, Authority, Locations, Evidence, EpistemicState, RecoveryRoute, Next>`

## Source checkpoint

`SKILL_ALL.zip`  
bytes: `468285`  
SHA-256: `5c1693b21de50dc0da4f2bdae85c57f01c0812aca1534d1305e5f56679d0eb1f`

Reaudit: 22 top entries; 9 nested ZIP nodes; 120 leaf files; 90 unique SHA-256 contents; 30 duplicate occurrences. `MANIFEST(1).json` declares 17 paths, with 0/17 materialized in the current recursive package inspection: `DECLARED_NOT_PRESENT / TOKEN_VAZIO_MATERIALIZATION`.

## Cross-authority pointers

- Drive brainstorm provider: `1_7x6IRqETh5D8huzjoWwDh4GrSVrh-NUiTbaQREQUx4`
- Memory Bridge report: `CONVERSATIONS_CHUNKS_PRIVATE/memory_bridge/reports/KNOWLEDGE_HYPERVISOR_BRAINSTORM_V0_1_2026-08-14.md`
- Memory Bridge index: `CONVERSATIONS_CHUNKS_PRIVATE/memory_bridge/indexes/KNOWLEDGE_HYPERVISOR_INDEX_V0_1.md`

## Open decisions

`fundamental_unit = TOKEN_VAZIO_DECISION`  
Candidates: `file | concept | typed Ω-ID`.

`namespace_policy = TOKEN_VAZIO_DECISION`  
Candidate display family: `✓Ω_#####_...`; immutable ID should remain separate from display name.

`super_root_schema = TOKEN_VAZIO`  
`mount_table_schema = TOKEN_VAZIO`  
`identity_table_schema = TOKEN_VAZIO`  
`semantic_edge_schema = TOKEN_VAZIO`

No reorganization, rename, installation, merge, or canonical promotion is authorized by this document.
