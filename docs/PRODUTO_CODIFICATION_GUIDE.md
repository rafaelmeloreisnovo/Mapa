# PRODUTO Codification Guide — How to Read Product Cards

**Version**: 1.0  
**Last Updated**: 2026-08-30  
**Status**: REFERENCE (specification document)

---

## What is PRODUTO.json?

A **PRODUTO.json** file is a machine-readable product card for each repository in the RAFAELIA ecosystem. It codifies:

1. **What** the repository produces (product identity)
2. **Which layers** it occupies in the five-layer architecture
3. **Who** owns it (authority boundary)
4. **What gaps** remain open (TOKEN_VAZIO catalog)
5. **How** to reach federation-certified state (closure paths)

Each repository has one PRODUTO.json at its root, following the schema in `schemas/produto.schema.json`.

---

## Key Fields Explained

### `repository` and `product_id`

```json
"repository": "rafaelmeloreisnovo/Mapa",
"product_id": "MAPA-001"
```

- **repository**: GitHub `owner/repo` format (immutable)
- **product_id**: Unique 6-digit ID (e.g., MAPA-001, RCPT-001, CHIP-001)

### `layers`

```json
"layers": [
  "Biblioteconomic KOS",
  "Operational Ontology",
  "Federated Control Plane",
  "Evidence & Custody",
  "Visual Navigation"
]
```

Which of the five RAFAELIA layers does this repo occupy? Choose 1–5 from the enum.

**Meanings:**
- **Biblioteconomic KOS**: Controlled vocabulary, authority control, semantic cataloging
- **Operational Ontology**: Concepts, relations, trajectories, epistemic gaps
- **Federated Control Plane**: Modules, products, procedures, gates, workflows
- **Evidence & Custody**: Typed pointers, checksums, audit trails, immutable records
- **Visual Navigation**: Diagrams, indices, reports, human-facing synthesis

### `authority`

```json
"authority": {
  "primary_owner": "rafaelmeloreisnovo",
  "domain": "federation + validation authority",
  "responsibility_scope": "cross-repository routing, state reconciliation, gap documentation",
  "authority_boundary": "federates claims across repos; does not prove individual repo implementation"
}
```

**Critical**: Authority boundary is where you state what this repo is NOT responsible for. This prevents authority inflation and over-claiming.

- **primary_owner**: GitHub user or organization
- **domain**: Technical domain (2–3 words)
- **responsibility_scope**: What this repo IS responsible for
- **authority_boundary**: What this repo is NOT responsible for (fail-closed)

### `epistemic_state`

```json
"epistemic_state": {
  "state": "VERIFICATION_PENDING",
  "claim_allowed": false,
  "open_token_vazio_count": 12,
  "merged_pr_count": 3
}
```

**state** must be one of:
- **REFERENCE**: Specification/explanatory material only
- **IMPLEMENTED**: Code or data exists
- **VERIFICATION_PENDING**: Work in progress; claim not yet promoted
- **VERIFIED_LIMITED**: Verified in declared scope; TOKEN_VAZIO may remain
- **FEDERATION_CERTIFIED**: All cross-repo gates pass; ready for federation

**claim_allowed**:
- `false` (default): Do NOT promote this repo's claims to federation state yet
- `true` (rare): This repo's claims are promoted to federation state

**open_token_vazio_count**: How many gaps remain documented and unfixed?

**merged_pr_count**: How many PRs have been merged to main? (optional, for activity tracking)

### `github_identity`

```json
"github_identity": {
  "repo_url": "https://github.com/rafaelmeloreisnovo/Mapa",
  "main_sha": "eb9cb679d42f64da6e4e4e09abcb96848aae2a8f",
  "visibility": "private"
}
```

- **repo_url**: Canonical GitHub URL (immutable)
- **main_sha**: Observed HEAD of main branch at binding time (update when refactoring)
- **visibility**: "public" or "private"

### `token_vazio_catalog`

```json
"token_vazio_catalog": {
  "tv_code": 2,
  "tv_test": 2,
  "tv_data": 2,
  "tv_independence": 2,
  "tv_boundary": 1,
  "tv_access": 1,
  "total_open_gaps": 12
}
```

Count of open TOKEN_VAZIO gaps by category:
- **tv_code**: Missing implementations
- **tv_test**: Missing tests or fixtures
- **tv_data**: Missing data or datasets
- **tv_independence**: Missing independence/dedup validation
- **tv_boundary**: Missing boundary condition specifications
- **tv_access**: Missing access control specifications

**total_open_gaps**: Sum of all categories. Used to track federation progress.

### `next_gates`

```json
"next_gates": [
  "Cycle 4: Implement TV-CODE (DAG causal engine, Bootstrap UQ)",
  "Cycle 5: Define TV-INDEPENDENCE (lineage authority, dedup rules)",
  "Cycle 6: Validate 6-repo TOROID topology"
]
```

Ordered list of gates that must close before this repo reaches FEDERATION_CERTIFIED state. Each gate should:
1. Name the cycle or milestone
2. State what must be implemented/validated
3. Link to the TOKEN_VAZIO gap(s) it closes

---

## drive_integration (Special Repos Only)

Only Mapa, CONVERSATIONS_CHUNKS_PRIVATE, and similar "custody bridge" repos have this section:

```json
"drive_integration": {
  "novoexport_folder_id": "1T41msBTBXITyd_NEOEKVfq2miVwqGQ1O",
  "novoexport_objects": 15439,
  "governance_docs": [
    {
      "name": "00_MAPA_ROTAS_INVENTARIO_NOVOEXPORT",
      "doc_id": "1iaUnAFbsPBO3dZtEQk40i13ZPOmhPd7d81Ujhf4O8Og",
      "role": "navigation authority"
    }
  ]
}
```

- **novoexport_folder_id**: Google Drive folder ID (immutable; documented in DRIVE_CUSTODY_RECEIPT.v1.json)
- **novoexport_objects**: Count of objects in custody (e.g., 15,439 for NOVOexport)
- **governance_docs**: Array of Google Doc records (receipts, navigation, audit trails)

---

## Reading PRODUTO.json in Practice

### Example: Is this repo ready for federation?

```bash
# Check claim_allowed
jq .epistemic_state.claim_allowed PRODUCTO.json
# false → NOT ready yet

# Check remaining gaps
jq .token_vazio_catalog.total_open_gaps PRODUCTO.json
# 12 → What must be fixed before claiming readiness?
```

### Example: What is the authority boundary?

```bash
jq .authority.authority_boundary PRODUCTO.json
# Output tells you what this repo does NOT guarantee
```

### Example: When will this repo reach FEDERATION_CERTIFIED?

```bash
jq .next_gates PRODUCTO.json
# Shows the ordered closure path
```

---

## Validation

All PRODUTO.json files are validated against `schemas/produto.schema.json` during CI:

```bash
python3 -m jsonschema \
  -i PRODUCTO.json \
  schemas/producto.schema.json
```

If this fails, the product card is malformed and CI blocks promotion.

---

## Refactoring Rules

When updating PRODUCTO.json:

1. **Never erase TOKEN_VAZIO** without implementing the corresponding gate
2. **Update main_sha** if HEAD of main branch changes significantly (new cycle, major refactoring)
3. **Preserve github_identity** immutably (repo URL, original SHA for historical reference)
4. **Record authority_boundary changes** only with explicit closure evidence
5. **Append to next_gates** instead of replacing (preserve history)

---

## Handoff

Each repository's refactoring should end with:

- [ ] PRODUCTO.json created/updated
- [ ] README refactored with navigation header
- [ ] All content preserved (nothing deleted; philosophical/spiritual text moved to dedicated files)
- [ ] Links to PRODUCTO.json added to README
- [ ] CI validation passes
- [ ] Cross-repo authority conflicts checked (via PRODUCTO_ECOSYSTEM_REGISTRY)

---

**See also:**
- [DRIVE_GITHUB_IDENTITY_MODEL.md](DRIVE_GITHUB_IDENTITY_MODEL.md) — Cross-surface binding
- [TOKEN_VAZIO_CATALOG.md](TOKEN_VAZIO_CATALOG.md) — Gap definitions and closure paths
- [PRODUTO_ECOSYSTEM_REGISTRY.v1.json](../data/control-plane/PRODUTO_ECOSYSTEM_REGISTRY.v1.json) — All 28 repos
