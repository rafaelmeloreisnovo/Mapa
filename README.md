# Mapa — RAFAELIA Knowledge Organization & Federated Control Plane

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Domain](https://img.shields.io/badge/Domain-KOS%20%7C%20Governance%20%7C%20Control%20Plane-purple)](biblioteconomia/)
[![Research](https://img.shields.io/badge/Research-RAFAELIA%20Ecosystem-orange)](https://github.com/rafaelmeloreisnovo/ChipQuantum)

> Central repository for organization, authority mapping, provenance, epistemic state,
> operational contracts and cross-repository routing across the RAFAELIA ecosystem.

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

## Índice de READMEs por Repositório

Estado do README raiz de cada repositório do ecossistema RAFAELIA após a refatoração de 2026-07.
Níveis: **Alto** (completo, técnico, navegável) · **Bom** (estruturado, sem lacunas críticas) · **Refatorado** (conteúdo não-técnico separado em arquivo auxiliar) · **Expandido** (stub mínimo expandido com estrutura técnica) · **Sem alteração** (não avaliado ou não modificado nesta fase).

### rafaelmeloreisnovo

| Repositório | Nível | Observação |
|---|---|---|
| `BLAKE3` | Alto | Fork BLAKE3 com documentação upstream completa |
| `ChipQuantum` | Alto | Documentação técnica detalhada (C/ASM, geometria, criptografia) |
| `Vectras-VM-Android` | Alto | README upstream VM Android completo |
| `androidx_RmR` | Alto | Fork AndroidX com changelog e estrutura upstream |
| `openssl` | Alto | Fork OpenSSL com documentação upstream |
| `termux-api_rafcodephi` | Alto | Fork Termux API com documentação técnica |
| `Mapa` | Bom | Plano de controle federado — este repositório |
| `Matem-tica-` | Bom | Catálogo matemático com estrutura clara |
| `RafPolimata` | Bom | 14 READMEs internos padronizados (Fase A) |
| `TeoremasTesesTeorias` | Bom | Estrutura de teoremas organizada |
| `X0` | Bom | Experimental/pesquisa, estrutura legível |
| `papers` | Bom | Manuscritos com referências e protocolos |
| `termux-app-rafacodephi` | Bom | Fork Termux App com documentação técnica |
| `home` | Bom | Configurações de ambiente documentadas |
| `RafaelCiencias` | Expandido | Fase D: adicionada tabela de 13 arquivos + estados TOKEN_VAZIO |
| `llamaRafaelia` | Refatorado | Fase C: ensaio → `ANALISE_CRUZADA.md`; README técnico criado |
| `privadoFazendo` | Refatorado | Fase C: 18 MVPs mantidos; contexto teórico → `CONTEXTO_TEORICO.md` |
| `Rafaelia_Private` | Refatorado | Fase C: dissertação pós-doutoral → `DISSERTACAO_SINTETICA.md` |
| `RafGitTools` | Refatorado | Fase C: parábola → `MANIFESTO.md`; README técnico de entrada |
| `qemu_rafaelia` | Refatorado | Fase B: README criado do zero (ausente); 9 docs referenciados |
| `teoremas` | Refatorado | Fase B: tese PhD → `TEORIA_ATRACTOR_42.md`; README de navegação |
| `gaia_phi` | Sem alteração | Não avaliado nesta fase |
| `Cosmos` | Sem alteração | Não avaliado nesta fase |
| `Clima` | Sem alteração | Não avaliado nesta fase |
| `Fisica` | Sem alteração | Não avaliado nesta fase |
| `Geral` | Sem alteração | Não avaliado nesta fase |
| `MemRa` | Sem alteração | Não avaliado nesta fase |
| `MemRafcode` | Sem alteração | Não avaliado nesta fase |
| `templo-vivo-arcs` | Sem alteração | Não avaliado nesta fase |
| `cientiespiritual` | Sem alteração | Não avaliado nesta fase |
| `rafaelia-core-enterprise` | Sem alteração | Não avaliado nesta fase |
| `ZIPRAF_OMEGA_FULL` | Sem alteração | Não avaliado nesta fase |
| `ZIPRAF_CORE` | Sem alteração | Não avaliado nesta fase |
| `catalogo-cosmologico` | Sem alteração | Não avaliado nesta fase |
| `GEOMETRIA_SOLAR_Maia_Inca` | Sem alteração | Não avaliado nesta fase |
| `CONVERSATIONS_CHUNKS_PRIVATE` | Sem alteração | Não avaliado nesta fase |
| `Seguran-a-informacional-` | Sem alteração | Não avaliado nesta fase |
| `ChipQuantum` | Sem alteração | Não avaliado nesta fase |

### instituto-Rafael

| Repositório | Nível | Observação |
|---|---|---|
| `relativity-living-light` | Alto | Validação científica falsificável com documentação completa |
| `apk-ethics-rafaelia` | Expandido | Fase D: stub 3 linhas → README técnico com uso, estrutura e evidências |
| `apk-guardian-rafaelia` | Expandido | Fase D: stub 3 linhas → README técnico com dois modos (detect_apk + detect_apk_abuse) |
| `apk-privacy-rafaelia` | Expandido | Fase D: stub 3 linhas → README técnico com foco LGPD/GDPR |
| `apk-antitrust-rafaelia` | Expandido | Fase D: manifesto 13 linhas → README técnico com estrutura pages/ e metodologia |
| `apk-gboard-insight` | Expandido | Fase D: manifesto genérico → README técnico de análise Gboard (NetRAF/ZipRAF/ZRF) |
| `apk-js-zrf-privacy` | Expandido | Fase D: manifesto genérico → README técnico foco vetor JavaScript/ZRF |
| `LivroVivo_ThisBookLives` | Refatorado | Fase C: parábola → `PARABOLA.md`; README de navegação mantido |
| `Firewall` | Refatorado | Fase B: texto de licença → `License.md`; README técnico de regras iptables criado |
| `QUANTUM_source_code` | Refatorado | Fase B: manifesto espiritual → `MANIFESTO_CIENTIESPIRITUAL.md`; README técnico criado |
| `RAFAELIA_CORE` | Sem alteração | Não avaliado nesta fase |
| `Bitraf-Bit-quantum` | Sem alteração | Não avaliado nesta fase |
| `Clay-Maths` | Sem alteração | Não avaliado nesta fase |
| `BIOSINTETICOS` | Sem alteração | Não avaliado nesta fase |
| `PlamaticGravity-` | Sem alteração | Não avaliado nesta fase |
| `LGPD-Constituicoes-...` | Sem alteração | Não avaliado nesta fase |
| `Eletron-efeitos-qu-ntico` | Sem alteração | Não avaliado nesta fase |
| `QUANTUM_auth_certificate` | Sem alteração | Não avaliado nesta fase |
| `publicacientiespiritual` | Sem alteração | Não avaliado nesta fase |

---

## License

**MIT** — see [`LICENSE`](LICENSE).
