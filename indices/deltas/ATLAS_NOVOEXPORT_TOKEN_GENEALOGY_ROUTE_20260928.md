# ATLAS — NOVOexport Token Genealogy Route — 2026-09-28

State: ROUTED_IMPLEMENTED_SCOPED / claim_allowed=false

## Intent

Provide the public-safe ATLAS route for reconstructing RAFAELIA token genealogy from the private current-source NOVOexport corpus without copying private message bodies into Mapa.

## Authority split

- Google Drive NOVOexport: raw current-source authority for conversations-000.json..conversations-050.json.
- CONVERSATIONS_CHUNKS_PRIVATE: private parser, occurrence identity, role-separated genealogy and private locators.
- Mapa: pointer-only routing, semantic state, typed relation boundary, gaps and receipts.
- producer repositories: implementation/domain authority for any token-to-code/project relation.

## Predecessor evidence

- indices/NOVOEXPORT_LONGITUDINAL_USAGE_COHERENCE_MAP_20260915_V1.md
- CONVERSATIONS_CHUNKS_PRIVATE/docs/NOVOEXPORT_JSON_ACTIVE_SOURCE_V3.md
- CONVERSATIONS_CHUNKS_PRIVATE/memory_bridge/reports/SEMANTIC_EXHAUSTIVITY_MATRIX_20260919_V2.md
- CONVERSATIONS_CHUNKS_PRIVATE/memory_bridge/indexes/ATLAS_COMPACT_ROUTER_V1.md

Existing source evidence closes the exact 000..050 SOURCE_COVERAGE plane. TOKEN_TEXT and global semantic exhaustivity remain partial/open.

## New producer delta

Private branch: rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE@codex/novoexport-token-genealogy-v1-20260928

Materialized surfaces:
- scripts/novoexport_token_genealogy.py
- tests/test_novoexport_token_genealogy.py
- memory_bridge/token_genealogy/README.md
- memory_bridge/token_genealogy/token_family_catalog.v1.json
- memory_bridge/token_genealogy/seed_shard_045.v1.json
- memory_bridge/receipts/2026-09-28_NOVOEXPORT_TOKEN_GENEALOGY_V1.json

Local unit test state: PASS.
Seed execution state: PASS_SCOPED_SHARD_045_ONLY.
Full 000..050 genealogy execution: PENDING.

## Route grammar

ATLAS:TOKEN:<literal>
 -> NOVO:TOKEN:<literal>
 -> SOURCE:<shard/fileId/hash>
 -> MSG:<conversation_id/message_id/node_id/role/time>
 -> L:<first/last/recurrence chronology>
 -> O:<same-period neighboring concepts>
 -> T:<cross-project/repository candidate>
 -> REL:<typed evidence-backed edge>
 -> EVID:<source/code/test/receipt>
 -> GAP:<unresolved sense/authority/causal edge>
 -> NEXT:<smallest verifiable action>

## Token families currently routed

RAFAELIA; Bitraf64; RAFCODE-Φ; ZIPRAFΩ; ♥φ; Ethica[8]; fΩ; Spiral√3/2; Trinity633; ToroidΔπφ; E↔C; OWLψ; Stack42H; FIAT LUX; 144.000hz; 963↔999; ψ→χ→ρ→Δ→Σ→Ω; ΣΩΔΦBITRAF.

These names are index addresses. Their appearance in text does not by itself establish physical meaning, novelty, authorship of quoted/retransmitted content, causal influence, model training, or implementation.

## Reconstruction contract

For a query such as ATLAS:TOKEN:Trinity633:
1. resolve private occurrence set in CONVERSATIONS_CHUNKS_PRIVATE;
2. separate user and assistant observations;
3. order by source timestamp while preserving shard/message identity;
4. review bounded context privately to disambiguate sense;
5. attach only evidence-backed typed relations to formulas/projects/repos;
6. emit public-safe pointer/count/state here;
7. leave unsupported edges TOKEN_VAZIO.

## Seed witness

Shard 045 was executed against the current source file conversations-045.json (Drive fileId 1POpVeIOZNuuS2hEGj1HB_j4FvturdFo2; 22,452,249 bytes; SHA-256 a490e4c7ad6f79f5f3f3eae2336fe87faf20a006df806173f0f4280eaf2039f2). The scoped scan observed 100 conversation objects, 4,109 message objects and all 18 configured token families.

High-value scoped user-source anchors include Trinity633 and E↔C in the 2026-05-29 Portal Andino Teorias message. This is not promoted as the global first occurrence until the exact 000..050 scan executes.

## Privacy and epistemic boundary

Mapa stores no raw private conversation body in this route. message_id/conversation_id may remain private-side when disclosure is unnecessary. Public projection should prefer opaque/private pointers plus counts/state.

USER_INPUT != ASSISTANT_OUTPUT
MESSAGE_ROLE_PROVENANCE != LEXICAL_AUTHORSHIP
LITERAL_OCCURRENCE != SEMANTIC_EQUIVALENCE
TEMPORAL_PRECEDENCE != CAUSAL_USE
RECURRENCE != TRAINING_EVIDENCE
RAW_SOURCE != DERIVED_INDEX
TOKEN_VAZIO != 0

## R3

F_ok = token-genealogy producer and public-safe ATLAS route materialized; scoped executable proof exists.
F_gap = 51-shard genealogy execution and token->project typed relation closure are not yet complete.
F_next = execute canonical 000..050 set, bind provider fileIds and derived hashes, then append one reconstruction proof per token family.