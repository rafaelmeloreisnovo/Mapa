# NOVOexport federated library: catalog, semantics, routes

State: `ACTIVE_SEED` · Authority: routing and cataloging only · `claim_allowed=false`

## Purpose and scope

This extension binds the existing Mapa biblioteconomic KOS to the Google Drive NOVOexport corpus. It supplies one repeatable bibliographic flow for terms, literal tokens, semantic records, data objects, memories, and evidence pointers. It complements the current controlled vocabulary, catalog, semantic dictionary, manifold registries, and NOVOexport active-source-universe records; it does not replace them.

**Authority split:** Google Drive remains source authority for raw NOVOexport objects and current provider IDs. Producer repositories remain authority for their code and domain claims. Mapa owns cross-surface catalog metadata, typed routing, and gap reconciliation. A catalog entry or graph edge never proves its subject.

## Grounded inventory

Existing Drive navigation identifies NOVOexport root `1P7hJq5R4fgYGEQIVNgRvllAad2lGxWEv`, its system/custody route `1T41msBTBXITyd_NEOEKVfq2miVwqGQ1O`, quarantine route `1q7NThjg5FBiVB8L2wNspijef25kDRCFi`, and active map/context route `1s54c6R4R6MT-Ralb4gCx1ez_pl2AMSFq`. The map route already holds the Navigation Hub, longitudinal usage map, shard inventory, time-series projections, and receipt.

The existing source-universe record reports 15,439 physical manifest entries, 15,369 logical files, 15,358 `.dat` entries, 51 conversation shards, and 21 Codex shards. These are inherited manifest observations, not a fresh full-corpus semantic recount. The provider listing sampled for this extension returned a bounded direct-child view; it does not establish exhaustive current listing or message coverage.

Existing gates remain open: `TV-INDEX-INGEST-000-050` and `TV-MESSAGES-FULL-COVERAGE`. Keep `ACTIVE_PARTIAL`; do not infer semantic exhaustivity, runtime use, training, or scientific truth.

## Bibliographic instruments

| Instrument | Use in this extension | Authority |
|---|---|---|
| Description / catalog record | Stable ID, source identity, type, title/literal, dates only when observed, media, access, scope, provenance, state, and gap pointers | descriptive metadata |
| Controlled vocabulary | Preferred label, aliases, definition, language, domain, sense version, source, semantic state, and supersession | term authority; unresolved tokens stay unresolved |
| Faceted classification | Multiple independent retrieval dimensions; labels are navigation coordinates, not exclusive truths | Mapa routing |
| Authority control | Separate same-spelling terms by scope; connect synonyms only with evidence; keep inverse relations distinct | explicit source bindings |
| Manifold | Typed edges between IDs with relation, direction, scope, evidence effect, guard, and state | graph structure, never proof |
| Atlas | Curated human-facing views over catalog and graph, selected by domain, time, scale, status, or route | derived view; no duplicate source |
| Retrieval scaffold | Minimal context packet assembled from selected catalog records and typed edges; source pointers first, excerpts only when permitted | retrieval only |
| Receipt / custody | Append-only record of source, action, result, gap, next step, and rollback/supersession pointer | audit trail |

Reuse the existing Dublin Core-oriented catalog and Mapa semantic dictionary fields where applicable. This extension is a local crosswalk; it does not claim conformance to an external cataloging standard.

## Facets (retrieval coordinates)

Each record may carry multiple values per facet. Unknown values are `TOKEN_VAZIO`, not a default category.

- **Domain / subject:** corpus, conversation, code, mathematics, science, runtime, governance, law, symbolic/philosophical.
- **Object / carrier:** export, file, shard, conversation, message, asset, term, expression, dataset, memory event, relation, route, receipt.
- **Operation:** discover, identify, describe, classify, normalize, index, relate, retrieve, verify, supersede.
- **Scale:** corpus → project → file → shard → object → message/token, only as far as the source binds the identity.
- **Time:** source-declared time, observation time, and event time remain distinct.
- **Provenance / authority:** Drive source ID, GitHub repository/ref/path/commit, producer authority, and custody receipt.
- **Epistemic state:** observed, asserted, candidate, tested, supported, contradicted, gap, or symbolic; retain the local vocabulary and never silently map unlike states.
- **Access / sensitivity:** public, private, restricted, or unknown; unknown blocks publication of content.

For L9 use only dimensions supported by a task: L longitudinal, O orthogonal, T transversal, P provenance, C contextual, R relational, I indexical, E evidential, A adaptive. A missing dimension stays empty.

## Canonical record and term rules

The machine-readable seed is `data/biblioteconomia/novoexport_library_model.v1.json`. Every catalog object has a stable library ID and preserves the source's original ID. A record carries: object type; source surface and exact pointer; descriptive fields; facets; access class; semantic state; typed relation references; evidence/gap pointers; route; and append-only predecessor/supersession. Hashes are included only when actually observed, with algorithm and scope.

Term records preserve the literal surface form independently from preferred label, alias, and definition. Keep glyphs, spelling, case, punctuation, and sequence unchanged in a literal field. A token with no evidenced meaning is indexed as `TOKEN_VAZIO_SEMANTIC`; do not replace it with zero, false, deletion, or a guessed gloss. Sense changes create a successor version and point to the predecessor.

## Biblioflow: intake and lifecycle

`DISCOVER → IDENTITY_BIND → DESCRIBE → CLASSIFY → AUTHORITY_CHECK → INDEX → RELATE → ROUTE → EVIDENCE_CHECK → RECEIPT → LEARN`

1. **Discover:** search only the authorized corpus route and capture provider identifiers.
2. **Bind identity:** preserve Drive file ID or GitHub repository/ref/path/commit; do not deduplicate by title alone.
3. **Describe:** populate observed metadata; leave unavailable fields explicitly empty.
4. **Classify:** apply multiple facets; uncertain classification remains pending/quarantined.
5. **Authority-check:** resolve aliases and collisions against the preferred-term register; keep unresolved symbols as literal tokens.
6. **Index:** generate lexical, alias, domain, provenance, temporal, and status lookups as derived projections.
7. **Relate:** add typed, directed edges only when the source supports the relationship; distinguish “co-occurs”, “derived from”, “implements”, “evidences”, and “supersedes”.
8. **Route:** emit a deterministic pointer to source, producer, evidence, or gap; ambiguity returns a typed empty state.
9. **Evidence-check:** a catalog or route is not an execution receipt or a claim gate.
10. **Receipt and learn:** append only material deltas; a correction creates a successor record, never silent history replacement.

## Biblio-manifold and Atlas projections

**Biblioflow** is the ordered processing lifecycle above. **Biblio-manifold** is the graph of stable entities and typed relations. A flow step may emit graph nodes/edges, but graph traversal does not imply flow completion. Atlas pages are read-only projections over these registries. Scaffolds select a bounded neighborhood and carry back source pointers, state, and gaps so a later session can reconstruct why each item was retrieved.

Minimum edge fields: `edge_id`, `source_id`, `relation_type`, `target_id`, direction, scope, source reference, evidence effect, promotion cap, guard, state, and supersession reference. Preserve `TOKEN_VAZIO` for any missing endpoint or evidence binding.

## Privacy and source boundaries

- Do not copy raw conversation messages, personal settings, credentials, or private asset contents into GitHub or public indexes.
- Public projections contain the minimum metadata and opaque references needed for navigation.
- Unread or unbound objects stay pending or in quarantine; “not found” is not “does not exist”.
- A file hash identifies bytes in its declared scope; it does not certify semantic identity or truth.
- Existing raw exports and Drive IDs are not mutated by this catalog layer.

## Current closure ledger

**F_ok:** Mapa already has the core biblioteconomic layer, semantic dictionary, typed relation index, machine-readable manifold, and NOVOexport source-universe/lineage indices. This extension supplies their explicit bridge and a bounded machine-readable model.

**F_gap:** full 15,439-entry source re-enumeration, per-object semantic coverage, complete messages, and current physical hash coverage remain unproven; these gaps are inherited, not closed here.

**F_next:** validate the model against the existing Drive navigation/inventory; then ingest a small, source-bound pilot from existing maps/receipts, compare records by stable source ID, and append only validated deltas. Preserve the 000..050 and message-coverage gates until their own receipts close them.

## Source pointers

- Google Drive root ID: `1P7hJq5R4fgYGEQIVNgRvllAad2lGxWEv`
- Existing route map: `00_MAPA_ROTAS_INVENTARIO_NOVOEXPORT`, ID `1iaUnAFbsPBO3dZtEQk40i13ZPOmhPd7d81Ujhf4O8Og`
- Existing inventory: `RAFAELIA — NOVOexport Inventário Navegável Ω — Obras e Dados — V1`, ID `1-2Kg5km6EgbjLKhSGf1lMMY0OVJk3eUGDewlIk1le80`
- Existing navigation hub: `RAFAELIA — NOVOexport Navigation Hub Ω — Obras, Rotas, Memória e Evidência`, ID `1QqwzIWJO1J3BkOjDnUp37JjOtuMF2iCNxyhCG6Vn4xc`
- Existing Drive map route folder: `1s54c6R4R6MT-Ralb4gCx1ez_pl2AMSFq`
- Mapa base observed: `main@7b17ba431d4be7c957a4cf668bdbe33dcd89c652`
- Related Mapa authorities: `biblioteconomia/`, `indices/CATALOGO_BIBLIOTECONOMICO.yaml`, `data/semantics/semantic-dictionary.v1.jsonl`, `data/semantics/semantic-relation-index.v1.json`, `data/manifold/routes_omega_v1.jsonl`, `data/manifold/edges_omega_v1.jsonl`, `indices/NOVOEXPORT_ACTIVE_V2_SOURCE_UNIVERSE_20260907_V1.md`
