# RAFAELIA — Operational Coherence Map V1 — 2026-08-13

State: `VERIFIED_LIMITED`  
Claim boundary: `claim_allowed=false`  
Mode: `append-only / no protected-branch write / no auto-merge / no release`

## Authority anchors

- Canonical method (Drive): provider `1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88`.
- Current longitudinal predecessor: `C81`, provider `1YD_Vs34QyvjWe4sHCRifWl_bbM6HjPoDiyMPar5u3Pc`.
- GitHub base used for this delta: `Mapa/main@39c0e38cc885bde18686871760453540545f9199`.

## Mother invariant

`idea != implementation != execution != evidence != claim`

Derived guards:

- `TOKEN_VAZIO != FAIL != PASS`
- `artifact_present != provenance_closed`
- `build_artifact != installed_artifact`
- `installed_artifact != runtime_semantic_proof`
- `single_execution != independent_reproduction`

## Seven operational windows

| Window | Priority | Purpose |
|---|---:|---|
| Security / integrity | 1 | Fail-closed, hashes, signatures, corruption, traversal, parser and I/O faults |
| Build / runtime | 2 | Build, ABI, APK, install, launch, physical workload |
| Contract / compatibility | 3 | API, ABI, schema, producer/verifier and identity semantics |
| Evidence / provenance | 4 | Source ↔ artifact ↔ receipt ↔ provider ↔ reproduction binding |
| Memory / index | 5 | Drive↔GitHub drift, stale state, orphan recovery, context reconstruction |
| Efficiency | 6 | Deduplication, dependency ordering, CI observability, micro-batches |
| Evolution | 7 | New research/capability only when earlier gates remain coherent |

## Material reclassification in this cycle

The RAFCODEPHI APK build gap is no longer an artifact-absence gap. A GitHub Actions artifact from `termux-app-rafacodephi@31df72137513885ec2535077141f8597496fce73` was recovered from workflow run `31281091629`, artifact `9028461291`.

Artifact archive SHA-256: `0f55449ce3a7907fe7f16454e9c362d16192d1e77e744bc362d5f1fc6cb27a0a`.

Exact APK identities:

- ARM32: `6988d308c37975e227d352ce54c4dee952c2a13e5b04245ef00b1a4b0f92af64`
- ARM64: `86c3708ca346e7882664e7308b026386a4ffdffbc17ff2ab870928120212473e`
- universal: `17ce6f4efd48e2e84fecbc3129304473d5fb60170decbd8d304e9f47439312bc`

Static package identity: `com.termux.rafacodephi`, version `0.118.0-rafacodephi`.

Correct state transition:

`TOKEN_VAZIO_ARTIFACT -> BUILD_ARTIFACT_BOUND_VERIFIED_STATIC`

Not allowed:

`BUILD_ARTIFACT_BOUND_VERIFIED_STATIC -> PHYSICAL_RUNTIME_PASS`

without an exact device-bound receipt.

## Priority route

1. `PHYSICAL_ARM32_EXACT_ARTIFACT` — install the exact ARM32 hash and capture `pm path`, installed `base.apk` hash, launch/log/workload evidence.
2. `INDEPENDENT_REPRODUCTION_MISSING` — repeat with identical provenance independently.
3. `CI_OBSERVABILITY_BILLING_OR_STARTUP` — rerun the same SHA only after runner/billing restoration; require actual steps/logs.
4. `PRODUCTION_SIGNING_RECEIPT_MISSING` — keep debug signing separate from release signing.
5. `RAFCODEPHI_PACKAGE_REPOSITORY_UNPUBLISHED` — signed metadata and device `apt/pkg` tests remain required.
6. `FG006_REPOSITORY_WIDE_COVERAGE_UNMEASURED` — enumerate tracked provenance/custody objects and require ledger coverage.
7. `DRIVE_GITHUB_STATE_DRIFT` — resolve newest receipt before every execution; C81 supersedes C79/C80 as the current predecessor.

## Categories intentionally preserved instead of erased

`forgotten`, `ignored`, `aborted`, `left-behind`, `suggested`, `obvious`, `important`, `urgent`, `necessary`, `absence`, and `TOKEN_VAZIO` are discovery labels, not proof states. They may alter triage priority but cannot promote evidence.

An empty or negative observation is valid information when represented as a typed state with provenance, falsifier and next probe.

## Closure grammar

Every actionable gap should converge to:

`gap_id | reason_code | provenance | repo/object | impact | urgency | dependencies | evidence_needed | falsifier | next_probe | closure_gate | epistemic_status | owner`

Missing values remain explicit `TOKEN_VAZIO`, never silently defaulted.

## F_next

Exactly one highest-information action remains: execute the exact ARM32 RAFCODEPHI APK SHA-256 `6988d308c37975e227d352ce54c4dee952c2a13e5b04245ef00b1a4b0f92af64` on physical Android and emit a receipt bound to source commit, workflow run, artifact ID, APK hash, installed package/hash and workload output.
