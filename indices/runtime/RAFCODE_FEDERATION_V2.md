# RafCode Federation V2 — post-merge evidence route

**State:** `PRODUCER_MERGED_POSTMERGE_REMEDIATION_OPEN`  
**Claim gate:** `claim_allowed=false`  
**Producer:** `rafaelmeloreisnovo/RafGitTools`  
**Federated authority:** `rafaelmeloreisnovo/Mapa`

## Supersession

This index supersedes the **state** recorded by `RAFCODE_FEDERATION_V1.md` without rewriting that historical artifact.

- V1 machine blob preserved: `7922b93e23dec385d5f20b34c1eb73e6dfff7283`
- producer PR `RafGitTools#381`: `MERGED`
- merge commit: `40fe688d30977967dd3b880b7b63a94e1d03694e`
- merged at: `2026-08-25T16:15:06Z`

## What is proven

The bounded freestanding evidence from V1 remains valid at its exact evidence scope:

- x86-64: compile/link/ELF/hotpath + smoke execution `PASS`;
- ARMv7: compile/link/ELF/hotpath `PASS`;
- AArch64: compile/link/ELF/hotpath `PASS`;
- no promotion from cross-compilation to physical-device execution.

## Post-merge health observation

Producer `main@40fe688d30977967dd3b880b7b63a94e1d03694e` has repository-wide build failure. The coherence/anti-regression job passed, while the Android build gate failed before application tests/lint/assemble could execute.

Observed root cause: wrapper `Gradle 9.6.1` with `AGP 8.13.2`; the Android plugin path relies on `org.gradle.api.problems.internal.InternalProblems`, removed in Gradle 9.6.0.

Classification: `BUILD_TOOLING_COMPATIBILITY_NOT_RAFCODE_LOGIC`.

## Active remediation

`RafGitTools#382` changes only `gradle/wrapper/gradle-wrapper.properties`:

`Gradle 9.6.1 → Gradle 9.5`

Head: `da46beed28d63ba0d7d99a0731bb75c63b8dc5fa`.

At observation time its workflows are queued/in progress. This is not yet a PASS.

## Open evidence

- `TOKEN_VAZIO_REMEDIATION_PR_382_CI`
- `TOKEN_VAZIO_PRODUCER_MAIN_POST_FIX_RECEIPT`
- `TOKEN_VAZIO_PHYSICAL_ARMV7_DEVICE_RECEIPT`
- `TOKEN_VAZIO_PHYSICAL_AARCH64_DEVICE_RECEIPT`
- `TOKEN_VAZIO_HMAC_AUTHENTICITY`

`TOKEN_VAZIO_PRODUCER_PR_MERGE` is closed by observed merge evidence.

## Machine/receipt bindings

- machine route: `data/federation/rafcode-federation-v2.json`
- post-merge receipt: `data/receipts/rafcode/2026-08-25-rafcode-producer-postmerge-remediation.v1.json`
- historical route: `data/federation/rafcode-federation-v1.json`

## R3

- `F_ok`: producer merge observed; bounded freestanding evidence preserved; repository-wide failure classified to a concrete build-tool incompatibility; minimal remediation exists.
- `F_gap`: remediation CI, post-fix main receipt, physical ARMv7/AArch64 execution and HMAC authenticity.
- `F_next`: evaluate PR #382 CI; convert each resulting failure into an evidenced causal node and correct only that node until no actionable unclassified gaps remain.
