# RAFAELIA Provenance Examination Matrix V1

State: `MATERIALIZED_FOR_REVIEW / FAIL_CLOSED`
Observed: `2026-08-25`

Purpose: turn the authorship/provenance control plane into five independent examination tracks that converge on the same release gate.

Core invariant:

`SOURCE_ORIGIN_PASS != AUTHORSHIP_PASS != LICENSE_PASS != BUILD_PASS != RUNTIME_PASS != RELEASE_PASS`

A failed or unknown stage does not erase successful stages. Unknown evidence remains `TOKEN_VAZIO`.

## Common examination spine

Every track is evaluated through:

1. `ORIGIN` — repo/ref/path/blob and upstream lineage.
2. `LICENSE` — applicable license/NOTICE/corresponding-source obligations.
3. `AUTHORSHIP` — RAFAELIA-only scope proven path+commit or clean-room receipt.
4. `BUILD` — source/compiler/flags/ABI/artifact hash/exit status.
5. `RUNTIME` — device/runtime transcript and evidence hash when applicable.
6. `DISTRIBUTION` — actual shipped set, third-party notices, source obligations, trademark/privacy boundaries.

No track may skip directly from implementation to release.

## Track T1 — Termux / RAFCODEPHI

Observed strengths:
- Termux-derived authority and GPL licensing are already acknowledged by the control plane.
- `RAFAELIA_MODULE_ORGANIZATION.md` documents a concrete `rafaelia/` module, JNI boundary and prior Gradle build result.

Observed contradiction requiring correction:
- the module documentation calls the C layer `zero dependencies`, while the same document states use of standard libc, `malloc`, `memcpy` and `math.h`.

Therefore:
- classify the existing JNI/native module as `NATIVE_INTEGRATION`, not as `FREESTANDING_PASS`;
- reserve `FREESTANDING_PASS` for a separately evidenced kernel that actually has no libc/heap/runtime helper dependency.

Exams:
- T1.E1 distributable manifest: enumerate files/resources/native objects that enter the APK.
- T1.E2 lineage split: classify each shipped path as inherited Termux, RAFCODEPHI original, third-party, or unresolved.
- T1.E3 license/NOTICE: bind each shipped component to its license and source obligation.
- T1.E4 freestanding audit: inspect actual native symbols/imports for libc, allocator, compiler helpers and JNI boundary.
- T1.E5 build receipt: record Gradle/NDK versions, flags, ABI, APK/native hashes and exit status.
- T1.E6 physical runtime receipt: bind device fingerprint, APK hash, source revision, command/transcript hashes and exit code.

Promotion rule: only RAFCODEPHI paths with path+commit evidence may move to class A; inherited Termux remains class B.

## Track T2 — QEMU / RAFAELIA RMR

Observed strengths:
- upstream QEMU licensing surfaces are acknowledged;
- `hw/core/rafaelia-rmr-license.txt` declares a separate RAFAELIA RMR low-level license.

Unresolved boundary:
- a component-specific license file does not prove that every surrounding source file is covered by that license or that combined-work/linkage obligations are closed.

Exams:
- T2.E1 RMR path inventory: enumerate every RMR source/header/build-system reference.
- T2.E2 origin/header exam: classify each RMR path against upstream QEMU and third-party history.
- T2.E3 linkage exam: identify compile units, symbols and QEMU interfaces crossed by RMR.
- T2.E4 license compatibility exam: record the applicable license for each side of the boundary; unresolved compatibility stays `TOKEN_VAZIO`.
- T2.E5 standalone-kernel exam: for genuinely new RAFAELIA kernels, prove explicit ABI, no libc/heap/helpers, fixed/caller-owned storage and bounded behavior.
- T2.E6 deterministic build/test receipt: source hash → compiler → flags → object/binary hash → test vector → exit code.

Promotion rule: only isolated paths with authorship evidence can become class A; a standalone clean-room successor requires its own specification and receipt before class E.

## Track T3 — Vectras legacy → RAFAELIA Virtual Runtime (RVR)

Observed strengths:
- `AUTHORSHIP_CLEANROOM_PLAN.md` already defines inventory, classification, quarantine, independent specification, reimplementation, similarity review, license consolidation and release gate.

Primary gap:
- the clean-room plan is a protocol, not proof that its backlog has been executed for the distributable set.

Exams:
- T3.E1 forensic inventory: file/path/hash/type/origin/license/risk/status for the full candidate distribution.
- T3.E2 quarantine exam: all C/D code, assets and binaries must be excluded from the clean-room implementation workspace and release candidate.
- T3.E3 specification-before-implementation exam: specification hash/timestamp must precede implementation ref for each class-E candidate.
- T3.E4 independent implementation exam: bind implementation paths to permitted specification sources only.
- T3.E5 dissimilarity/provenance review: record reviewer, method, findings and falsifier; similarity alone never proves clean-room status.
- T3.E6 acceptance/runtime exam: behavior against independently written acceptance tests and device/runtime receipts.
- T3.E7 release/legal exam: NOTICE/licenses/source obligations plus product-name/trademark state.

Promotion rule: `B/D legacy != E RVR`; class E is module-scoped and requires a complete clean-room receipt.

## Track T4 — llamaRafaelia

Observed strengths:
- repository `LICENSE` records MIT terms and copyright for the ggml authors.

Primary gap:
- file-level lineage of RAFAELIA additions versus inherited/substantial upstream material is not yet closed.

Exams:
- T4.E1 lineage inventory: enumerate source paths and map upstream/ref/blob where obtainable.
- T4.E2 MIT notice retention exam: verify copyright and permission notice in copies/substantial portions and distributions.
- T4.E3 RAFAELIA delta exam: identify commits/paths created independently by RAFAELIA and their authorship evidence.
- T4.E4 dependency/model-data exam: separate code license from model weights, tokenizers, datasets or other artifacts with independent terms.
- T4.E5 build/runtime receipt: compiler/backend/flags/ABI/model-or-fixture identity/artifact hashes/exit status.
- T4.E6 freestanding-candidate exam: treat any new inference/dataflow kernel separately from the llama.cpp-derived integration layer.

Promotion rule: repository-level naming does not promote inherited MIT code to class A; only evidenced RAFAELIA deltas may be A.

## Track T5 — AndroidX / Gradle / native dependencies

Role: third-party dependency surface shared by Android-facing artifacts.

Exams:
- T5.E1 resolved dependency graph: exact group/artifact/version and native package identities.
- T5.E2 license-source exam: bind each dependency to official license/NOTICE source.
- T5.E3 packaging exam: determine what is actually embedded, dynamically required, generated or only build-time.
- T5.E4 THIRD_PARTY_NOTICES generation: build notice candidate from the resolved shipped set, not from declared dependencies alone.
- T5.E5 corresponding-source/source-offer exam where applicable.
- T5.E6 privacy/security boundary: record account/data-processing permissions separately from copyright/license review.

Promotion rule: these components normally remain class B; success means obligations are closed, not that authorship changes.

## Convergence gate

A release candidate may advance only when every shipped component has:

`object identity + origin + class + license basis + notice/source obligation + build identity + release decision`

and every class A/E claim additionally has authorship/clean-room evidence appropriate to its class.

Any C/D item in the shipped set => `release_allowed=false`.

## Execution order

1. T1 Termux/RAFCODEPHI distributable manifest — highest leverage because it exposes the actual APK boundary.
2. T2 QEMU/RMR path+linkage split — highest legal/technical ambiguity at a mixed-license integration boundary.
3. T3 Vectras/RVR forensic inventory + quarantine — prerequisite for any clean-room successor claim.
4. T4 llamaRafaelia lineage — comparatively tractable once path inventory is generated.
5. T5 AndroidX/Gradle/native notice graph — close distribution obligations against the real packaged set.

R3:
- `F_ok`: per-component examination routes defined.
- `F_gap`: most file-level/build/runtime evidence remains uncollected.
- `F_next`: execute T1.E1 and bind its output into a receipt before promoting any authorship or release claim.
