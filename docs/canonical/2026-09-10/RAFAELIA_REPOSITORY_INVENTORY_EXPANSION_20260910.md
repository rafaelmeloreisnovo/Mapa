# RAFAELIA — Federated Repository Inventory Expansion

**Cut:** 2026-09-10  
**Transaction:** append-only inventory delta  
**Control plane:** `rafaelmeloreisnovo/Mapa`  
**State:** `INVENTORY_OBSERVED / REVIEW_REQUIRED`  
**claim_allowed:** `false`

## 0. Invariants

```text
SOURCE != ARTEFACT != IMPLEMENTATION != EXECUTION != EVIDENCE != CLAIM
TOKEN_VAZIO != 0
BUILD != DEVICE_EXECUTION
FORK != ORIGINAL_AUTHORSHIP
RETRIEVAL_CONTEXT != WEIGHT_UPDATE
```

This document does **not** replace `indices/repository_authority_registry.json`. It records a larger observed repository universe and candidate authority relations that must be deduplicated, audited and promoted only through the existing federated registry validator/workflow.

## 1. Why this delta exists

The current canonical `indices/repository_authority_registry.json` contains a bounded set of repositories and already has a validator and CI route. The current authenticated repository listing exposes a materially larger RAFAELIA-adjacent universe. Therefore:

```text
CURRENT_AUTHORITY_REGISTRY_COVERAGE = PARTIAL
CURRENT_GITHUB_UNIVERSE = OBSERVED_LARGER_THAN_REGISTRY
EXACT_CANONICAL_REPO_COUNT = TOKEN_VAZIO_PENDING_DEDUP
```

No existing authority entry is downgraded or overwritten by this document.

## 2. Federated layers

```text
CORPUS
→ KNOWLEDGE / HYPOTHESES
→ MATHEMATICAL FORMALIZATION
→ IMPLEMENTATION
→ RUNTIME
→ RECEIPTS / EVIDENCE
→ GOVERNANCE
→ SCIENTIFIC CLAIM
→ PUBLICATION / INDEPENDENT REVIEW
```

`Mapa` remains orthogonal to those layers as the routing, authority, provenance and gap-control plane.

## 3. Inventory by family

### A — Control plane, governance, memory and receipts

- `Mapa` — federation, provenance, authority control, gap routing.
- `Recipt` — bounded execution/evidence receipts; streaming evidence kernel.
- `MemRafcode` — memory custody / re-entry routes.
- `MemRa` — memory/index candidate; detailed authority review pending.
- `OMEGAGIT` — Git/integration/governance seed.
- `TRABALHO_ROADMAP_AUDIT_GOV_DATA_ROTA_MAPwithCHAIN_security` — roadmap/governance seed; role not yet formally established.
- `Geral` — general holding/candidate routing surface.

### B — Mathematics, theorems and formal research

- `Matem-tica-` — mathematical formalization, proofs, finite verifiers, Ω-CUBE-42, Forma Normal 123.
- `TeoremasTesesTeorias` — theorem/thesis/theory and prior-art governance.
- `teoremas` — theorem repository; deeper canonical review pending.
- `RafPolimata` — mathematical + semantic + low-level + evidence-governance research.
- `RafaelIA_Solucoes_Clay` — Clay-problem research candidate.
- `Graditao` — mathematical/research material candidate.
- `GEOMETRIA_SOLAR_Maia_Inca` — geometry/archaeoastronomy research.

### C — Cosmology, physics and scientific programs

- `Cosmos` — transdisciplinary cosmology/knowledge program.
- `relativity-living-light` — RLL/MCRP scientific modeling, likelihoods, falsifiers and results.
- `Fisica` — physics research/formalization.
- `Catalogo-cosmologico` — cosmological catalogue / observation organization.
- `RafaelCiencias` — federated science candidate.
- `ChipQuantum` — T7/geometry/crypto/HPC/compiler/low-level research laboratory.

### D — Core computation, kernels and ZIPRAF

- `Rafaelia_Core` — deterministic multiarch kernel/benchmark layer.
- `rafaelia-core-enterprise` — enterprise/core synchronization layer.
- `RafNet-Core` — network/core candidate.
- `ZIPRAF_CORE` — ZIPRAF core, compression/security/data structures.
- `ZIPRAF_OMEGA_FULL` — extended ZIPRAF implementation/corpus.
- `Rafcodephi_Sdk_ndkJni_c_py_sh_asm_lua_rs_go_swift_perl_yml_` — SDK/multilanguage tooling surface.
- `Rafaelia` — private/legacy RAFAELIA surface; lineage requires reconciliation.

### E — Android, Termux, virtualization and physical runtime

- `termux-app-rafacodephi`
- `termux-api_rafcodephi`
- `termux-packages`
- `Vectras-VM-Android`
- `qemu_rafaelia`
- `frida-desktop`
- `ROM-emulator`
- `androidRom`
- `android_frameworks_base_rafaelia`
- `androidx_RmR`
- `UserLAnd`
- `UserLAnd2`
- `Shizuku`

These require strict upstream/license/provenance separation where derived from external projects.

### F — AI, model experiments and semantic adapters

- `llamaRafaelia`
- `TinyGPT`
- `nanoGPT`
- `DeepSeek-RafCoder`
- `treinarModelos`
- `IaFcea`
- `GAIA_phi`
- `GAIA-PDS-PHI`
- `GaiaPhiRafcode`

Model/retrieval/training states must remain separated. Presence of a corpus, prompt, adapter or retrieval route does not establish a weight update.

### G — Private corpus, raw sources and custody

- `CONVERSATIONS_CHUNKS_PRIVATE`
- `Rafaelia_Private`
- `rafaelia_privado`
- `privadoFazendo`
- `home`
- `Img`
- `Semente`
- `X0`
- `new`
- `V79-1`

These are primarily source/corpus/custody candidates until each producer role is explicitly audited.

### H — Philosophy, spirituality, language and humanities

- `CientiEspiritual`
- `CientiEspiritual-tiEs-`
- `Espiritual-espirualidade`
- `verbum-vivo`
- `Tora`
- `templo-vivo-arcs`
- `CreFeBerna`
- `fcea-originum`

Claims from these surfaces must be typed so that manifesto, metaphor, theology/philosophy, hypothesis, technical model and empirical science do not silently collapse into one state.

### I — Legal, security and standards

- `Judicial-`
- `IA_nist`
- `Seguran-a-informacional-`
- `CryptoSwift_RmR`
- `BLAKE3`
- `openssl`

External/upstream components belong to `SOURCE/DERIVED` provenance unless and until local modifications are audited. Public visibility does not establish ownership or license selection.

### J — Publication and scientific communication

- `papers` — synthesis, drafts, claim ledgers, methods and publication staging.
- `arxiv-docs` — publication/documentation tooling; upstream status must be preserved where applicable.

### K — Applications and experiments

- `PCR_Rafaelia_Code_seed`
- `Clima`
- `myCat-iahelpsus`
- `RAIAREIS_FRAMEWORK`
- `RAFNATIONS_CORE`

These remain application/experiment/seed surfaces until their producer authority and evidence boundaries are established.

### L — External/upstream-derived bases

Examples observed in the reachable universe include:

- `BLAKE3`
- `openssl`
- `gradle`
- `linuxkernel`
- `LuaJIT`
- `androidx_RmR`
- `Shizuku`
- `florisboard`
- `nanoGPT`
- `UserLAnd*`
- QEMU-derived, Termux-derived and Android/Lineage-derived code

Required provenance tuple:

```text
upstream source
→ repository/commit
→ copyright holder
→ license/version
→ copied/adapted material
→ RAFAELIA destination
→ modifications
→ affected files
→ attribution/NOTICE obligations
→ compatibility
→ evidence/hash
→ gap/action
```

## 4. High-value semantic/authority collisions

### COLLISION-42

Observed terminology spans:

```text
42 pipeline stages
42 routed/candidate states
42 attractor candidates
42 attractors
```

Safe current rule:

```text
42 candidates / routed states != proven dynamical attractors
```

Promotion of `attractor` requires explicit dynamics, basin definition, convergence/stability criteria and evidence appropriate to the claimed domain.

### COLLISION-FREESTANDING

An artifact can be freestanding without the entire repository being freestanding.

```text
FREESTANDING_ARTIFACT != WHOLE_REPOSITORY_FREESTANDING
```

Claims must be path/commit/receipt scoped.

### COLLISION-RLL-AUTHORITY

Both `instituto-Rafael/relativity-living-light` and `rafaelmeloreisnovo/relativity-living-light` appear in the existing authority registry with different roles/states. Preserve that lineage; do not merge identities by name alone.

### COLLISION-ALIASES-SUCCESSORS

Candidate groups requiring predecessor/successor/fork/alias review include:

```text
Rafaelia / Rafaelia_Core / rafaelia-core-enterprise / Rafaelia_Private / rafaelia_privado
GAIA_phi / GAIA-PDS-PHI / GaiaPhiRafcode
UserLAnd / UserLAnd2
CientiEspiritual / CientiEspiritual-tiEs-
ZIPRAF_CORE / ZIPRAF_OMEGA_FULL
```

Allowed relation types should include:

```text
PREDECESSOR | SUCCESSOR | FORK | ALIAS | MIRROR | ARCHIVE | INDEPENDENT | TOKEN_VAZIO
```

## 5. Priority gaps

```text
F_GAP_001  authority-registry coverage vs current repository universe
F_GAP_002  exact deduplicated canonical repository count
F_GAP_003  predecessor/successor/fork/alias reconciliation
F_GAP_004  42-state/attractor semantic authority
F_GAP_005  artifact-scoped freestanding claims
F_GAP_006  ARM32/ARM64 physical execution receipts where still absent
F_GAP_007  independent scientific reproduction for promoted scientific claims
F_GAP_008  CientiEspiritual claim typing and evidence pointers
F_GAP_009  full third-party copyright/license ledger
F_GAP_010  global REPO × CLAIM × SOURCE × EXECUTION × EVIDENCE × LICENSE registry
```

## 6. Proposed registry surfaces

Do **not** create parallel competing authorities. Extend or generate from the existing Mapa governance once schemas are reconciled:

```text
repository_authority_registry
claim_registry
source_license_registry
execution_registry
evidence_registry
relationship_registry
token_vazio_registry
```

The target join is:

```text
REPOSITORY
→ AUTHORITY
→ CLAIM
→ SOURCE
→ IMPLEMENTATION
→ EXECUTION
→ EVIDENCE
→ REVIEW
→ CLAIM_ALLOWED
```

## 7. Promotion order

```text
P0 inventory current repos
P1 deduplicate aliases/lineage
P2 authority reconciliation
P3 claim registry linkage
P4 source/license linkage
P5 execution/evidence linkage
P6 semantic collision resolution
P7 independent reproduction
P8 publication promotion
```

## 8. R3 / receipt

```text
F_ok:
- larger repository universe observed
- canonical registry preserved without destructive overwrite
- families and candidate roles enumerated
- upstream separated from original authorship
- high-value semantic collisions identified
- gap and promotion order recorded

F_gap:
- full content audit of every repository not performed in this transaction
- exact deduplicated canonical count remains TOKEN_VAZIO
- lineage relations remain incomplete
- external license/copyright audit remains incomplete
- device/scientific evidence remains non-uniform

F_next:
- reconcile this candidate inventory against indices/repository_authority_registry.json
- promote only entries that pass owner/role/lineage/source/evidence review
- preserve all unresolved relations as TOKEN_VAZIO
```

**Transaction boundary:** documentation/inventory only. No executor repository, scientific claim, runtime state or canonical authority entry was promoted by this write.
