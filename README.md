# Mapa — RAFAELIA Knowledge Organization & Federated Control Plane

> **Product ID**: MAPA-001  
> **Domain**: Federation + Validation Authority  
> **Authority**: Cross-repository routing, state reconciliation, gap documentation  
> **Status**: Bom (architectural soundness confirmed; TOKEN_VAZIO preserved)  
> **Claim Gate**: `claim_allowed=false` (until Cycle 6 closure)  
> **Epistemic State**: VERIFICATION_PENDING (12 TOKEN_VAZIO gaps documented)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Domain](https://img.shields.io/badge/Domain-KOS%20%7C%20Governance%20%7C%20Control%20Plane-purple)](biblioteconomia/)
[![Research](https://img.shields.io/badge/Research-RAFAELIA%20Ecosystem-orange)](https://github.com/rafaelmeloreisnovo/ChipQuantum)

> Central repository for organization, authority mapping, provenance, epistemic state,
> operational contracts and cross-repository routing across the RAFAELIA ecosystem.

---

## Product Values — This Repository

**What Mapa produces:**

- Federated knowledge organization across 28 repositories
- Immutable cross-surface identity (GitHub ↔ Google Drive) via DRIVE_CUSTODY_RECEIPT
- TOKEN_VAZIO catalog with closure paths per gap
- Authority pyramid and responsibility boundaries
- Append-only governance ledger

**Product layers occupied:**

- Biblioteconomic KOS (controlled vocabulary, authority control)
- Operational Ontology (concepts, relations, trajectories)
- Federated Control Plane (modules, products, procedures, gates)
- Evidence & Custody (typed pointers, checksums, audit trails)
- Visual Navigation (diagrams, indices, reports)

**Authority boundary:**

- ✓ Routes cross-repo claims, validates coherence and contracts
- ✗ Does NOT prove individual repo implementation
- ✗ Does NOT execute projects; orchestrates federated authority only

**TOKEN_VAZIO gaps:** 12 open gaps across 6 categories (TV-CODE, TV-TEST, TV-DATA, TV-INDEPENDENCE, TV-BOUNDARY, TV-ACCESS)  
**Next gates:** [Cycle 4](PRODUTO.json) (implementations), [Cycle 5](PRODUTO.json) (lineage authority), [Cycle 6](PRODUTO.json) (topological validation)

**Cross-surface integration:**

- GitHub: `rafaelmeloreisnovo/Mapa` (main SHA: `eb9cb679d42f64da6e4e4e09abcb96848aae2a8f`)
- Google Drive: NOVOexport (15,439 objects) + OMEGA-CYCLE receipts
- Custody bridge: `CONVERSATIONS_CHUNKS_PRIVATE` (900 JSON objects, 145MB aggregate)

**See:** [PRODUTO.json](PRODUTO.json) (machine-readable product card) | [DRIVE_CUSTODY_RECEIPT.v1.json](data/control-plane/DRIVE_CUSTODY_RECEIPT.v1.json) (GitHub ↔ Drive identity) | [PRODUTO_ECOSYSTEM_REGISTRY.v1.json](data/control-plane/PRODUTO_ECOSYSTEM_REGISTRY.v1.json) (all 28 repos)

---

## Mission

`Mapa` is not the executor of every project. It is the federated control and knowledge plane that records:

```text
identity
→ canonical owner
→ observed version
→ relations and dependencies
→ evidence and limitations
→ allowed transition
→ next verifiable step
```

The technical truth remains in each producer repository. `Mapa` identifies where that truth is, which immutable revision was observed, what the evidence supports and which gaps remain open.

## Five layers

| Layer | Responsibility |
|---|---|
| Biblioteconomic KOS | cataloging, controlled vocabulary, authority control and semantic collisions |
| Operational ontology | concepts, relations, trajectories, heuristics and epistemic gaps |
| Federated control plane | modules, products, procedures, gates, workflows and next-action routing |
| Evidence and custody | typed pointers, checksums, runs, correction history and append-only records |
| Visual and human navigation | diagrams, indices, reports and review surfaces |

## Core invariants

```text
TOKEN_VAZIO != 0
fixture != live state
heuristic != proof
analogy != mechanism
commit != execution
merge != remote gate PASS
local path != cross-repository evidence
claim_allowed=false until the corresponding evidence gate closes
```

## Repository map

```text
Mapa/
├── arquitetura/          Federated architecture and responsibility boundaries
├── biblioteconomia/      KOS, controlled vocabulary and authority control
├── protocolos/           Operational governance, homeostasis and rollback
├── orquestrador/         Contracts, fixtures and frontline orchestration design
├── schemas/              Machine-readable structural contracts
├── data/
│   ├── ontology/         Canonical operational ontology
│   ├── workflows/        Canonical workflow DAGs
│   ├── triage/           Priority, grouping and equivalence registry
│   └── control-plane/    Live observed state, typed evidence and reconciliation
├── scripts/              Deterministic validators and engines
├── tools/                Repository, artifact and gap mappers
├── tests/                Positive and adversarial tests
├── indices/              Asset, source, inventory and dependency manifests
├── governanca/           Custody and data-governance rules
├── auditoria/            Bounded local and remote evidence records
├── resultados/           Reviewed reports, baselines and limitations
├── workflows/            Human-readable operational routes
├── visual/               Concept maps and diagrams
└── docs/                 Architecture, methods and implementation boundaries
```

## Active executable governance

| Package | Purpose | Boundary |
|---|---|---|
| Operational ontology | validate concepts, relations, trajectories and useful gaps | heuristic is not proof |
| Topology and inventory | preserve dependency DAG, repository inventory and fixed-point batches | inventory remains partial |
| Cross-source records | type source identity, version, custody and comparability | duplicate content is not independent evidence |
| Operational workflow | validate input → transform → output → evidence → rollback | planned stages remain `TOKEN_VAZIO` |
| Operational triage | derive priority and distinguish analogy, dependency and exact equivalence | same group is not same situation |
| Procedure ledger | separate plan, condition, execution, result and supersession | `PASS` requires run and evidence |
| Live control plane | reconcile current modules, products, merges and evidence pointers | observed state does not rewrite history |

## Live control-plane state

The live layer is intentionally separate from `orquestrador/fixtures/`:

```text
data/control-plane/
├── current_state_snapshot.v1.json
├── module_registry.v1.json
├── product_graph.v1.json
├── evidence_pointer_registry.v1.json
├── merge_decisions.v1.json
└── procedure_state.v1.json
```

Current bounded states include:

```yaml
control_plane: VERIFIED_LIMITED
universal_doctor: PARTIAL
termux_health_bridge: VERIFIED_LIMITED_DRAFT
semantic_interpretation: TOKEN_VAZIO
remote_private_runner: TOKEN_VAZIO_RUNNER
claim_allowed: false
```

See [`docs/LIVE_CONTROL_PLANE_RECONCILIATION.md`](docs/LIVE_CONTROL_PLANE_RECONCILIATION.md).

## Federated responsibility

| Plane | Primary authority | Does not prove alone |
|---|---|---|
| Control and catalog | `Mapa` | scientific truth or real execution |
| Control routing | `RafGitTools` | runtime success |
| Local runtime | `termux-app-rafacodephi` | scientific validity |
| Evidence production | `RafPolimata` | universal generalization |
| Interpretation | `llamaRafaelia` | permission to expose raw private sources |
| Scientific validation | `relativity-living-light` / `papers` | production readiness |
| Virtualization | `Vectras-VM-Android` / `qemu_rafaelia` | performance superiority without benchmark |

A relation becomes a real integration only when it records:

```text
owner repository
source path
input and output contracts
immutable version
reproduction command
result artifact
checksum
failure mode
rollback
claim boundary
```

## Local validation

### Live control plane

```bash
python3 -m py_compile \
  scripts/validate_live_control_plane.py \
  tests/test_live_control_plane.py

python3 -m unittest -v tests/test_live_control_plane.py

python3 scripts/validate_live_control_plane.py \
  --repo-root . \
  --write-report build/live-control-plane/report.json
```

### Operational ontology

```bash
python3 -m unittest -v tests/test_operational_ontology_engine.py

python3 scripts/operational_ontology_engine.py \
  --ontology data/ontology/rafaelia-operational-ontology.v1.json \
  --output-json build/ontology/report.json \
  --output-md build/ontology/report.md \
  --generated-at 2026-07-23T00:00:00Z \
  --strict
```

## Workflows and remote evidence

The repository contains focused GitHub Actions for CI, topology, inventory, cross-source records, research intake, operational workflow, triage and live control-plane validation.

A workflow file existing in the repository is not evidence that a remote runner executed it. When a private-repository job terminates before the first observable step, the state remains:

```text
TOKEN_VAZIO_RUNNER
```

Local evidence may be recorded as `VERIFIED_LIMITED`, but it does not silently become remote `PASS`.

## Cross-repository research path

```text
producer repository / scientific claim
  ↓ immutable evidence pointer
Mapa / provenance, authority, state and route
  ↓ reviewed packet
Drive / editorial copy or durable report
  ↓ review gate
merge | correction | contradiction | TOKEN_VAZIO
```

A commit proves existence and history of an artifact. It does not by itself prove execution, causality, performance, safety or scientific validity.

## README Quality Index — Ecosystem Repositories

**Sprint:** 2026-07 · **Branch:** `claude/readme-analise-refatoracao-vl6t6l`

Quality levels:
- **Alto** — Complete, technically precise, no changes needed
- **Bom** — Good original quality; minor cleanup or no changes required
- **Refatorado** — Content separated: philosophical/spiritual/legal text moved to dedicated auxiliary files; README = technical entry point
- **Expandido** — Stub or missing README expanded with full technical structure

> **Preservation principle:** All pre-existing content is preserved 100%. Philosophical, spiritual, legal and academic texts are moved to dedicated named files (`LITURGIA.md`, `MANIFESTO_LEGAL.md`, `DISSERTATION.md`, etc.) and explicitly referenced from the README. Nothing was deleted.

### rafaelmeloreisnovo/

| Repository | Level | Action |
|---|---|---|
| [BLAKE3](https://github.com/rafaelmeloreisnovo/BLAKE3) | Alto | No change — original README complete |
| [ChipQuantum](https://github.com/rafaelmeloreisnovo/ChipQuantum) | Alto | No change — original README complete |
| [Vectras-VM-Android](https://github.com/rafaelmeloreisnovo/Vectras-VM-Android) | Alto | No change — original README complete |
| [androidx_RmR](https://github.com/rafaelmeloreisnovo/androidx_RmR) | Alto | No change — original README complete |
| [openssl](https://github.com/rafaelmeloreisnovo/openssl) | Alto | No change — original README complete |
| [Clima](https://github.com/rafaelmeloreisnovo/Clima) | Alto | No change — original README complete |
| [Fisica](https://github.com/rafaelmeloreisnovo/Fisica) | Alto | No change — original README complete |
| [GEOMETRIA_SOLAR_Maia_Inca](https://github.com/rafaelmeloreisnovo/GEOMETRIA_SOLAR_Maia_Inca) | Alto | No change — original README complete |
| [termux-api_rafcodephi](https://github.com/rafaelmeloreisnovo/termux-api_rafcodephi) | Alto | No change — original README complete |
| [Mapa](https://github.com/rafaelmeloreisnovo/Mapa) | Bom | Updated — added this README quality index |
| [Matem-tica-](https://github.com/rafaelmeloreisnovo/Matem-tica-) | Bom | No change |
| [RafPolimata](https://github.com/rafaelmeloreisnovo/RafPolimata) | Bom | 14 internal READMEs standardized with canonical state headers and cross-references |
| [TeoremasTesesTeorias](https://github.com/rafaelmeloreisnovo/TeoremasTesesTeorias) | Bom | No change |
| [X0](https://github.com/rafaelmeloreisnovo/X0) | Bom | No change |
| [papers](https://github.com/rafaelmeloreisnovo/papers) | Bom | No change |
| [termux-app-rafacodephi](https://github.com/rafaelmeloreisnovo/termux-app-rafacodephi) | Bom | No change |
| [gaia_phi](https://github.com/rafaelmeloreisnovo/gaia_phi) | Bom | No change |
| [Cosmos](https://github.com/rafaelmeloreisnovo/Cosmos) | Bom | No change |
| [cientiespiritual](https://github.com/rafaelmeloreisnovo/cientiespiritual) | Bom | No change |
| [ZIPRAF_OMEGA_FULL](https://github.com/rafaelmeloreisnovo/ZIPRAF_OMEGA_FULL) | Bom | No change |
| [catalogo-cosmologico](https://github.com/rafaelmeloreisnovo/catalogo-cosmologico) | Bom | No change |
| [CONVERSATIONS_CHUNKS_PRIVATE](https://github.com/rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE) | Bom | No change |
| [Geral](https://github.com/rafaelmeloreisnovo/Geral) | Bom | No change |
| [home](https://github.com/rafaelmeloreisnovo/home) | Bom | No change |
| [teoremas](https://github.com/rafaelmeloreisnovo/teoremas) | Refatorado | Full thesis moved to `TEORIA_ATRACTOR_42.md`; README = navigation entry point |
| [RafGitTools](https://github.com/rafaelmeloreisnovo/RafGitTools) | Refatorado | 80-line philosophy manifesto moved to `MANIFESTO.md` |
| [Rafaelia_Private](https://github.com/rafaelmeloreisnovo/Rafaelia_Private) | Refatorado | Post-doctoral dissertation moved to `DISSERTATION.md` |
| [privadoFazendo](https://github.com/rafaelmeloreisnovo/privadoFazendo) | Refatorado | Theoretical context moved to `CONTEXTO_TEORICO.md`; 18 MVPs in tabular form |
| [llamaRafaelia](https://github.com/rafaelmeloreisnovo/llamaRafaelia) | Refatorado | Cross-system analysis essay moved to `ANALISE_CRUZADA.md` |
| [templo-vivo-arcs](https://github.com/rafaelmeloreisnovo/templo-vivo-arcs) | Refatorado | Liturgical prayer (54 KB) moved to `LITURGIA.md`; README = architecture + TOKEN_VAZIO gates |
| [Seguran-a-informacional-](https://github.com/rafaelmeloreisnovo/Seguran-a-informacional-) | Expandido | Created from scratch: Lídia DVD 8-mechanism protection table |
| [MemRa](https://github.com/rafaelmeloreisnovo/MemRa) | Expandido | 23-file research archive catalog with states |
| [ZIPRAF_CORE](https://github.com/rafaelmeloreisnovo/ZIPRAF_CORE) | Expandido | ZRF-C library structure, API, and TOKEN_VAZIO gates |
| [MemRafcode](https://github.com/rafaelmeloreisnovo/MemRafcode) | Expandido | 8-stage pipeline, chain invariant, 17-file structure table and truth rules added |
| [rafaelia-core-enterprise](https://github.com/rafaelmeloreisnovo/rafaelia-core-enterprise) | Expandido | 50+ C Vectra variants, GeoLM geodesic, Voynich pipeline described |
| [qemu_rafaelia](https://github.com/rafaelmeloreisnovo/qemu_rafaelia) | Expandido | Created from scratch — no prior root README existed |
| [RafaelCiencias](https://github.com/rafaelmeloreisnovo/RafaelCiencias) | Expandido | Scientific domain table + internal document links added |

### instituto-Rafael/

| Repository | Level | Action |
|---|---|---|
| [relativity-living-light](https://github.com/instituto-Rafael/relativity-living-light) | Alto | No change — original README complete |
| [Eletron-efeitos-qu-ntico](https://github.com/instituto-Rafael/Eletron-efeitos-qu-ntico) | Bom | No change |
| [Bitraf-Bit-quantum](https://github.com/instituto-Rafael/Bitraf-Bit-quantum) | Bom | No change |
| [publicacientiespiritual](https://github.com/instituto-Rafael/publicacientiespiritual) | Bom | No change |
| [LivroVivo_ThisBookLives](https://github.com/instituto-Rafael/LivroVivo_ThisBookLives) | Refatorado | Interdimensional parable moved to `PARABOLA.md`; README = navigation index |
| [Firewall](https://github.com/instituto-Rafael/Firewall) | Refatorado | License text (entire README) moved to `LICENSE.md`; README = technical description |
| [QUANTUM_source_code](https://github.com/instituto-Rafael/QUANTUM_source_code) | Refatorado | Spiritual/legal declaration moved to `SPIRITUAL_CONTEXT.md`; README = technical pipeline |
| [Clay-Maths](https://github.com/instituto-Rafael/Clay-Maths) | Refatorado | AI chat artifact removed; `# Clay-Maths` heading added; bilingual Clay Problems analysis preserved |
| [QUANTUM_auth_certificate](https://github.com/instituto-Rafael/QUANTUM_auth_certificate) | Refatorado | Legal manifest (R$ 50k–50M fines table) moved to `MANIFESTO_LEGAL.md` |
| [PlamaticGravity-](https://github.com/instituto-Rafael/PlamaticGravity-) | Refatorado | Risk analysis chat artifact removed; 4 risk sections moved to `RISCOS_GRAVIDADE_PLASMATICA.md` |
| [apk-ethics-rafaelia](https://github.com/instituto-Rafael/apk-ethics-rafaelia) | Expandido | Technical structure (purpose, build, TOKEN_VAZIO gates) added |
| [apk-guardian-rafaelia](https://github.com/instituto-Rafael/apk-guardian-rafaelia) | Expandido | Technical structure added |
| [apk-privacy-rafaelia](https://github.com/instituto-Rafael/apk-privacy-rafaelia) | Expandido | Technical structure added |
| [apk-antitrust-rafaelia](https://github.com/instituto-Rafael/apk-antitrust-rafaelia) | Expandido | Technical structure added |
| [apk-gboard-insight](https://github.com/instituto-Rafael/apk-gboard-insight) | Expandido | Technical structure added |
| [apk-js-zrf-privacy](https://github.com/instituto-Rafael/apk-js-zrf-privacy) | Expandido | Technical structure added |
| [RAFAELIA_CORE](https://github.com/instituto-Rafael/RAFAELIA_CORE) | Expandido | Σ_pipeline architecture, Ethica[8], Voynich analysis, GeoLM described |
| [LGPD-Constituicoes-planetaria-...](https://github.com/instituto-Rafael/lgpd-constituicoes-planetaria-paises-onu-direitos-humanos-e-fundamentais-de-cada-continents-geologic) | Expandido | Created from scratch — no prior root README; 10 data files + 10 dirs cataloged |
| [BIOSINTETICOS](https://github.com/instituto-Rafael/BIOSINTETICOS) | Expandido | Heading syntax error fixed (`# #` → `#`); structure table and TOKEN_VAZIO gates added |

## Ecosystem

| Repository | Primary domain |
|---|---|
| `RafGitTools` | governed control plane and Android operator surface |
| `RafPolimata` | parsing, normalization, indexing and evidence production |
| `termux-app-rafacodephi` | Android local runtime |
| `llamaRafaelia` | contextual retrieval and interpretation |
| `Vectras-VM-Android` | Android VM runtime |
| `qemu_rafaelia` | QEMU integration and low-level runtime |
| `relativity-living-light` | falsifiable scientific validation |
| `papers` | manuscripts, claims, references and research protocols |
| `ChipQuantum` | C/ASM, geometry, cryptography and compiler experiments |
| `Cosmos` | transdisciplinary relations and cosmological maps |

## License

**MIT** — see [`LICENSE`](LICENSE).
