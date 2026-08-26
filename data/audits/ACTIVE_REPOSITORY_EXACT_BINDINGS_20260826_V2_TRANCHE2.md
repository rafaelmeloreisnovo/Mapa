# ACTIVE REPOSITORY EXACT BINDINGS — V2 — TRANCHE 2

status: `MATERIALIZED_EXACT_HEAD_TREE_COHORT_CLOSED`
claim_allowed: `false`
release_allowed: `false`

## Inventory erratum

V1 counted `S_IMPLEMENTATION_TEST_EVIDENCE = 20`, but its `implementation_rich_priority` name array contained only 18 entries. The omitted names were:

- `rafaelmeloreisnovo/ZIPRAF_CORE`
- `instituto-Rafael/RAFAELIA_CORE`

The total was correct; the enumeration was incomplete. V2 repairs this explicitly and defines the canonical implementation-rich cohort as 20 repositories.

## Exact HEAD/tree closure

Tranche 1 bound 6 repositories. Tranche 2 binds the remaining 14. Therefore:

`exact HEAD + root tree = 20/20 = 100% of implementation-rich cohort`

This is an **identity/tree closure percentage**, not technological maturity.

### Tranche 2 exact bindings

| Repository | Branch | HEAD | Root tree | Signature | Protected |
|---|---|---|---|---|---|
| ZIPRAF_CORE | main | `060f7f28...` | `df077727...` | verified | no |
| Semente | main | `fca23ee9...` | `098ed49c...` | verified | no |
| rafaelia-core-enterprise | fcea-auto-sync | `de12cfb0...` | `95216ee8...` | verified | no |
| templo-vivo-arcs | main | `ebbf8c2f...` | `06be0a79...` | **unsigned** | no |
| instituto-Rafael/RAFAELIA_CORE | main | `5af6d636...` | `19476a25...` | verified | no |
| instituto-Rafael/Zrf | main | `ea863fc3...` | `2a11a37a...` | verified | no |
| instituto-Rafael/Bitraf-Bit-quantum | main | `cffd71e0...` | `00a4762b...` | verified | no |
| instituto-Rafael/ESTADO-FRACTAL-HAJA | main | `92c592e8...` | `75677837...` | verified | no |
| instituto-Rafael/Clay-Maths | main | `8a15ddb7...` | `1f72cd9f...` | **unsigned** | no |
| instituto-Rafael/Atomic_EX_WASTE | main | `ae9ee346...` | `20b2cafc...` | verified | no |
| instituto-Rafael/Eletron-efeitos-qu-ntico | main | `3451046f...` | `b8d803db...` | verified | no |
| instituto-Rafael/Whilehole | main | `08798d8d...` | `24e3ca3c...` | verified | no |
| instituto-Rafael/Etica-nas-Intelig-ncia-artificial- | main | `ebc3cf50...` | `4fa6bbb6...` | verified | no |
| instituto-Rafael/Unify_Teory_of_mission_holly_espiritual_ciencias_ | main | `ac303f56...` | `d6d896e5...` | verified | no |

Unsigned HEAD is recorded only as a provenance signal. It is not evidence of compromise.

## Current-tree CI boundary

- `ZIPRAF_CORE`: zero Actions runs observed on `main` -> execution `TOKEN_VAZIO`.
- `Semente`: zero Actions runs observed on `main` -> execution `TOKEN_VAZIO`.
- `rafaelia-core-enterprise`: one branch run exists, but it belongs to SHA `40aaea...`, not current HEAD `de12cf...`; therefore current-head execution remains `TOKEN_VAZIO`.
- `templo-vivo-arcs`: a success exists on exact HEAD, but it is a dynamic **Codespaces prebuild** platform automation. It is not promoted to project-code CI PASS.
- all ten `instituto-Rafael` tranche-2 repositories: zero Actions runs observed on current branch -> execution `TOKEN_VAZIO`.

Thus tranche 2 contributes **zero new project-code CI PASS promotions**.

## Provenance/license boundary

The pass distinguishes a file name from the legal/content class:

- `ESTADO-FRACTAL-HAJA`: `LICENSE.md` is a machine-readable-minded layered draft: docs under `CC-BY-NC-SA-4.0`, original software under `PolyForm-Noncommercial-1.0.0`, datasets fail-closed when manifests are absent; it explicitly records `counsel_review=TOKEN_VAZIO` and `claim_allowed=false`.
- `templo-vivo-arcs`: `LICENSE` is manifesto/chat-style content with legal assertions, not a conventional license grant -> `NONSTANDARD_MANIFEST_LICENSE`.
- `Clay-Maths`: `License.md` mixes RAFCODE/Sovereign restrictions and a generic AGPL reference -> `CONFLICTING_NONSTANDARD_LICENSE`; automatic AGPL classification is forbidden.
- `Etica-nas-Intelig-ncia-artificial-`: the file starts with a complete MIT grant but appends unrelated symbolic/parabolic content -> `MIT_CORE_WITH_APPENDED_NONLICENSE_CONTENT`.
- `Unify_Teory...`: `LICENSE` contains nonstandard symbolic/restrictive text -> clarity gap.
- several remaining repositories return 404 for the exact standard `LICENSE` path; those are retained as `TOKEN_VAZIO_STANDARD_PATH`, not interpreted as absence of all rights information.

## Exact structure corrections

Two repositories that could have been understated by latest-commit wording are concretely non-empty implementations:

- `ZIPRAF_CORE` root contains `include/`, `src/`, `tests/`, `tools/`, `examples/`, and `docs/`.
- `rafaelia-core-enterprise` current tree contains multiple substantial C files, including `geolm.c` and `geolm_raf.c`.
- `Semente` exposes an ARM32 validation-status artifact and benchmark evidence packs at current HEAD.

Therefore a recent documentation commit does not downgrade underlying implementation substance.

## Cohort result

`20/20 HEAD+tree bound`

`0/20 protected default branches observed`

`runtime/empirical promotions = 0`

The next percentage that matters is **not** another inventory percentage. It is the fraction of these 20 with a current-tree executable receipt whose scope matches the claim being assessed.

## F_next

For each of the 20:

`exact HEAD/tree -> runnable gate -> execution receipt -> runtime/empirical evidence where applicable -> provenance cleanup -> domain-normalized score`

Historical test claims and old-SHA CI runs cannot be transferred to current HEAD.

## R3

- F_ok: implementation-rich cohort exact identity/tree coverage closed at 20/20; V1 enumeration defect repaired.
- F_gap: current-tree executable receipts, runtime/empirical proof and license clarity remain heterogeneous.
- F_next: execute/bind current-tree gates by repository class, prioritizing code-rich repos with runnable tests and unresolved provider execution.
