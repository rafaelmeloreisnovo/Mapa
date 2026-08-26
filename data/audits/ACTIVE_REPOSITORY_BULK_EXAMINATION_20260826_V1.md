# ACTIVE REPOSITORY BULK EXAMINATION — 2026-08-26 — V1

status: `MATERIALIZED_PRELIMINARY_EVIDENCE_BOUND`
claim_allowed: `false`
release_allowed: `false`
base: `Mapa/main@a47eb393c2622cb6f110921aaa0e530d22ee0a49`
backlog_authority: `indices/BACKLOG_ACERVO.yaml@ce0933a98ebd2b951d9a4d4771752c5dd7e1e40e`

## Scope

This append-only audit pass executes the first bulk examination of the 82 repositories marked `pendente` in the active 110-repository topology. It does **not** rewrite the L01 catalog and does not promote a repository merely because commits, files or documentation exist.

Audit levels used:

- `T0_IDENTITY`: repository identity is present in the reconciled backlog.
- `T0_ACTIVITY`: commit-history probe returned at least one concrete commit.
- `T1_STRUCTURE`: code/search probe exposed an implementation, test, validator, receipt or runtime-evidence artifact.
- `T2_EXECUTION`: exact test/CI/runtime execution was independently bound in this pass.
- `TOKEN_VAZIO`: this pass did not obtain enough evidence for the next level.
- `EMPTY_API`: repository API explicitly reported an empty Git repository / zero-size repository metadata in the observed provider surface.

`COMMIT_EXISTS != CODE_PASS != TEST_PASS != CI_PASS != RUNTIME_PASS != CLAIM`.

## Global result

- pending identities routed: **82/82**
- topology covered at T0 identity: **82/82**
- deep file/tree/license/runtime exhaustiveness: **TOKEN_VAZIO**
- catalog promotion: **0 automatic promotions**
- explicit empty/zero-content observations: `rafaelmeloreisnovo/fcea-originum`, `rafaelmeloreisnovo/RAIAREIS_FRAMEWORK`, `rafaelmeloreisnovo/rafaelia_privado`, `rafaelmeloreisnovo/new`, `instituto-Rafael/Pesquisa`
- important correction: `pendente` in the backlog does not mean `immature`; several pending repositories already expose code, validators, tests, CI/evidence receipts or deterministic prototypes.

## Preliminary examination matrix

Legend: `S` = implementation/test/evidence signal observed; `D` = primarily documentation/research signal in this pass; `E` = explicit empty; `U` = no sufficiently discriminating signal returned by the bounded batch probe.

### rafaelmeloreisnovo — pending set

| Repository | Signal | Evidence class | Preliminary maturity boundary |
|---|---|---|---|
| ZIPRAF_CORE | S | runtime/module docs + test-oriented structure found | T1_STRUCTURE; execution TOKEN_VAZIO |
| Rafaelia_Core | S | ARM32 C core + invariant contracts + claim verifier | T1_STRUCTURE; prior execution claims require exact receipt rebind |
| Semente | S | ARM32 validation-status artifact found | T1_STRUCTURE; physical/runtime closure TOKEN_VAZIO |
| rafaelia-core-enterprise | S | multiple C implementation files found | T1_STRUCTURE; CI/runtime TOKEN_VAZIO |
| GAIA-PDS-PHI | U | bounded probe did not establish current implementation gate | TOKEN_VAZIO |
| Tora | U | bounded probe not discriminating | TOKEN_VAZIO |
| Geral | U | bounded probe not discriminating | TOKEN_VAZIO |
| RafNet-Core | S | runtime/MPLS probes + evidence JSON found | T1_STRUCTURE; physical MPLS runtime remains bounded |
| Seguran-a-informacional- | U | bounded probe not discriminating | TOKEN_VAZIO |
| MemRa | U | bounded probe not discriminating | TOKEN_VAZIO |
| rafaelia_privado | E | zero-size/empty provider observation | EMPTY_API |
| Rafaelia | U | bounded probe not discriminating | TOKEN_VAZIO |
| RAFNATIONS_CORE | D | minimal repository surface in provider metadata | T0_ACTIVITY/TOKEN_VAZIO |
| RAIAREIS_FRAMEWORK | E | zero-size provider observation | EMPTY_API |
| fcea-originum | E | zero-size provider observation | EMPTY_API |
| privadoFazendo | S | extensive security regression, CI and receipt history observed | T1_STRUCTURE; repository-wide current security/runtime certification TOKEN_VAZIO |
| new | E | empty provider observation | EMPTY_API |
| V79-1 | U | bounded probe not discriminating | TOKEN_VAZIO |
| Img | U | data repository; implementation maturity not established | TOKEN_VAZIO |
| nanoGPT | S | freestanding Python/Rust/C+ASM triad + falsification gates observed | T1/T2 partial; checkpoint equivalence/training/2x remain TOKEN_VAZIO |
| treinarModelos | U | bounded probe not discriminating | TOKEN_VAZIO |
| IaFcea | U | bounded probe not discriminating in current pass | TOKEN_VAZIO |
| IA_nist | U | bounded probe not discriminating | TOKEN_VAZIO |
| RafaelCiencias | D | technical/scientific documentation; benchmark gaps preserved | T0/T1 partial; execution TOKEN_VAZIO |
| Fisica | S | executable invariant/test/CI history observed | T1/T2 partial; physical measurement claims remain gated |
| Catalogo-cosmologico | D | catalog/documentation signal | T0_ACTIVITY; execution TOKEN_VAZIO |
| Cosmos | D | scientific bridge/audit history | T0/T1 research; empirical closure TOKEN_VAZIO |
| Clima | D | documentation/state signal | T0_ACTIVITY; execution TOKEN_VAZIO |
| TeoremasTesesTeorias | D | theorem correction/audit history | T0/T1 formalization; proof obligations repo-wide TOKEN_VAZIO |
| teoremas | D | proof-obligation/audit history | T0/T1 formalization; theorem proof closure TOKEN_VAZIO |
| RafaelIA_Solucoes_Clay | U | bounded probe not discriminating | TOKEN_VAZIO |
| GEOMETRIA_SOLAR_Maia_Inca | S | deterministic cycle generator/data/self-test history | T1/T2 partial; scientific causal claims gated |
| Judicial- | U | bounded probe not discriminating | TOKEN_VAZIO |
| verbum-vivo | U | bounded probe not discriminating | TOKEN_VAZIO |
| CientiEspiritual | D | active research/cleanup and conceptual registry history | T0/T1 documentation; scientific/runtime claims gated |
| CientiEspiritual-tiEs- | U | bounded probe not discriminating | TOKEN_VAZIO |
| templo-vivo-arcs | S | append-only audit, blockers and custody gates observed | T1_STRUCTURE; domain claims remain evidence-gated |
| Espiritual-espirualidade | U | bounded probe not discriminating | TOKEN_VAZIO |
| CreFeBerna | U | bounded probe not discriminating | TOKEN_VAZIO |
| Graditao | U | bounded probe not discriminating | TOKEN_VAZIO |

### instituto-Rafael — pending set

| Repository | Signal | Evidence class | Preliminary maturity boundary |
|---|---|---|---|
| RAFAELIA_CORE | S | shell/pipeline + technical documentation history | T1 partial; current execution receipt TOKEN_VAZIO |
| RAFNET_CORE | U | bounded batch signal insufficient | TOKEN_VAZIO |
| omega-rafaelia | D | initial-seed history observed | T0_ACTIVITY; implementation TOKEN_VAZIO |
| Zrf | S | refactor + verification script + mathematical operations history | T1_STRUCTURE; current reproducible execution TOKEN_VAZIO |
| ziprar | D | initial-seed history observed | T0_ACTIVITY; implementation TOKEN_VAZIO |
| Bitraf-Bit-quantum | S | implementation/refactor + mathematical library history | T1_STRUCTURE; current validation/claims TOKEN_VAZIO |
| QUANTUM_source_code | D | technical README/research source organization | T0/T1 partial; runtime TOKEN_VAZIO |
| QUANTUM_auth_certificate | D | provenance/license/documentation signal | T0_ACTIVITY; executable certification claim not allowed |
| StudiesArm64 | D | ARM64 study/refactor history | T0/T1 educational; runtime TOKEN_VAZIO |
| Firewall | D | technical firewall documentation, underlying scripts referenced | T0/T1 partial; runtime/security efficacy TOKEN_VAZIO |
| apk-privacy-rafaelia | D | technical privacy-analysis docs; scripts referenced | T0/T1 partial; device/runtime TOKEN_VAZIO |
| apk-guardian-rafaelia | D | technical APK analysis docs; scripts referenced | T0/T1 partial; device/runtime TOKEN_VAZIO |
| apk-gboard-insight | D | technical analysis docs | T0/T1 partial; empirical/device proof TOKEN_VAZIO |
| apk-js-zrf-privacy | D | technical JS/ZRF privacy docs | T0/T1 partial; empirical/device proof TOKEN_VAZIO |
| ESTADO-FRACTAL-HAJA | S | machine-readable governance, validator and adversarial tests | T1/T2 partial; legal/runtime claims gated |
| ASTRA-FRACTAL-PIPE | U | bounded batch signal insufficient | TOKEN_VAZIO |
| IA-Generativa | D | mixed conceptual/AI material; no current bounded validation established | T0_ACTIVITY; model/medical-performance claims TOKEN_VAZIO |
| Ia-rafaelProjeto | U | bounded batch signal insufficient | TOKEN_VAZIO |
| Clay-Maths | S | deterministic MTRE prototype/benchmark + claim boundaries | T1/T2 partial; Millennium-problem solution claims explicitly not promoted |
| solvedClayMaths | D | historical-name/claim-boundary correction | T0/T1 governance; solution claim not established |
| Tegmark | D | academic restructuring/documentation history | T0/T1 research; empirical validation TOKEN_VAZIO |
| Entropia-aponta-a-origem-do-feito | D | academic restructuring/documentation history | T0/T1 research; empirical validation TOKEN_VAZIO |
| Atomic_EX_WASTE | S | scripts/refactor/code-review fixes + academic structure | T1_STRUCTURE; current tests/runtime TOKEN_VAZIO |
| Eletron-efeitos-qu-ntico | S | requirements/test script + implementation/refactor history | T1_STRUCTURE; experimental quantum claims gated |
| PlamaticGravity- | D | plasma/MHD research boundaries, mostly documentation in recent history | T0/T1 research; empirical validation TOKEN_VAZIO |
| Whilehole | S | implementations + tests/documentation history | T1_STRUCTURE; current reproducible receipt TOKEN_VAZIO |
| BIOSINTETICOS | D | documentation-centric recent history | T0_ACTIVITY; implementation/runtime TOKEN_VAZIO |
| Bio | D | minimal README/initial history | T0_ACTIVITY; implementation TOKEN_VAZIO |
| Etica-nas-Intelig-ncia-artificial- | S | scripts/refactor/input validation history | T1_STRUCTURE; empirical/operational validation TOKEN_VAZIO |
| Analise-juridica | U | bounded batch signal insufficient | TOKEN_VAZIO |
| Constituicao-brasileira-leis | D | legal/markdown corpus history | T0_ACTIVITY; software runtime not applicable/unproven |
| manifesto-antioligopolio-rafaelia | D | manifesto/documentation history | T0_ACTIVITY; software implementation TOKEN_VAZIO |
| Manifesto-publico | D | manifesto/license/document corpus | T0_ACTIVITY; software runtime not inferred |
| apk-ethics-rafaelia | D | technical README, structure/evidence descriptions | T0/T1 partial; executable/device proof TOKEN_VAZIO |
| apk-antitrust-rafaelia | D | technical README/pages methodology | T0/T1 partial; executable/device proof TOKEN_VAZIO |
| Particula-Omega- | D | historical uploaded/conceptual material | T0_ACTIVITY; scientific/runtime validation TOKEN_VAZIO |
| Unify_Teory_of_mission_holly_espiritual_ciencias_ | S | Python module/examples + tests-claimed refactor history | T1_STRUCTURE; independent current execution TOKEN_VAZIO |
| cienti-espiritual-verbo-vivo | D | active academic/research framework and cleanup history | T0/T1 documentation; scientific claim validation TOKEN_VAZIO |
| CIENTIESPIRITUAL_MANIFESTO | D | manifesto repository | T0_ACTIVITY; software runtime not inferred |
| Cren-as-ESPIRITUAL-amparo-LEGAL-SAGRADO | D | document/upload history | T0_ACTIVITY; software runtime not inferred |
| Motorhall-4.x | D | README/license-only activity observed | T0_ACTIVITY; implementation TOKEN_VAZIO |
| Pesquisa | E | Git provider returned empty repository | EMPTY_API |

## High-value findings

1. **Backlog semantics correction** — `pendente` means not yet integrated into the canonical catalog/evidence coverage, not necessarily lacking implementation.
2. **Implementation-rich pending repositories exist** — examples include `Rafaelia_Core`, `RafNet-Core`, `nanoGPT`, `Fisica`, `GEOMETRIA_SOLAR_Maia_Inca`, `privadoFazendo`, `Clay-Maths`, `ESTADO-FRACTAL-HAJA`, `Zrf`, `Whilehole`, and `Eletron-efeitos-qu-ntico`.
3. **Explicit empty/stub set exists** — five repositories are currently evidenced as empty/zero-content in the bounded provider observations above. They should not consume the same deep-audit priority as implementation-rich repositories.
4. **Documentation-heavy repositories must not be scored as failed software** — several are manifestos, research collections or legal/academic corpora. Their maturity axis is provenance/structure/evidence quality, not device runtime.
5. **Security/provenance needs separate scoring** — `privadoFazendo` contains a substantial remediation history for previously embedded credentials and fail-closed security regression gates; current safety must be evaluated from the present tree, not inferred solely from remediation commit messages.

## Proposed maturity vector for V2

For each repository, score independently rather than collapsing unlike domains:

`M = (I, C, T, CI, R, P, G)`

- `I`: identity/tree coverage
- `C`: executable/code substance where applicable
- `T`: tests/falsifiers
- `CI`: provider execution
- `R`: runtime/device/empirical evidence where applicable
- `P`: provenance/license
- `G`: gaps/claim governance

No scalar `%` is authorized until each component has a current source pointer and the non-applicable dimensions are explicitly marked `N/A`, not zero.

## Remaining TOKEN_VAZIO / next gate

The original P0 gap is **narrowed, not closed**. Identity-level routing is now complete for the 82 backlog entries, but the closure gate from cycle 005 requires, for every pending active repository:

`repo identity -> current HEAD -> tree boundary -> license/provenance -> receipt state`.

V2 must therefore:

1. bind exact current HEAD + default branch for every non-empty repository;
2. inspect root tree and classify repo kind (`software`, `research`, `data`, `manifesto`, `legal`, `mixed`);
3. bind license/provenance pointer;
4. identify tests/workflows and most recent executable receipt;
5. classify runtime/empirical state without transferring evidence between domains;
6. produce one machine-readable record per repository;
7. only then compute domain-normalized maturity percentages.

## R3

- F_ok: 82/82 pending identities routed; implementation-rich, documentation-heavy, empty and unresolved classes separated; no automatic promotion.
- F_gap: current HEAD/tree/license/receipt exhaustiveness remains open; T2 execution not uniformly re-run.
- F_next: V2 exact-HEAD/tree/provenance pass, highest-value implementation-rich repositories first, while empty/document-only repos receive bounded low-cost closure.
