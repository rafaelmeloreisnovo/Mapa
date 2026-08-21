# Lanes Touchpoints Catalog

## Overview
Maps execution lanes (R1-R12) to specific touchpoints where external systems observe or modify Mapa state. Enables isolation of side effects and coordination across federated producers.

## Lane Definitions & Primary Touchpoints

### Lane R1: qemu_rafaelia Source Resolution
**Provider**: rafaelmeloreisnovo/qemu_rafaelia  
**Touchpoint 1 (Source)**: `.github/workflows/qemu-ci.yml` → verifies master branch
**Touchpoint 2 (Consumer)**: Vectras-VM-Android/tools/ci/external_sources.manifest (pinned commit reference)
**Touchpoint 3 (Evidence)**: Vectras-VM-Android/reports/external-sources-receipt.json (generated)
**Touchpoint 4 (Mapa Intake)**: RafPolimata/scripts/external_source_evidence_producer.py (consumes receipt)

**State Transitions**:
- R1.init: Manifest defines pinned commit
- R1.validate: verify_external_sources_v2.sh executes (CI gate O1)
- R1.recover: Fallback to rank_1 if O1 fails
- R1.evidence: Receipt generated with status (VERIFIED_ORIGINAL_PIN or recovery_rank)
- R1.federate: RafPolimata produces raf.external-source-evidence.v1

**Blocking Conditions**:
- Pinned commit inaccessible (recovery_rank >= 1)
- Receipt timestamp stale (>24h from current_cycle)
- ABI validation missing (O2 TOKEN_VAZIO)

---

### Lane R2: androidx_RmR Source Resolution  
**Provider**: wojcikiewicz17/androidx_RmR  
**Touchpoint 1 (Source)**: androidx-main branch (continuous)
**Touchpoint 2 (Consumer)**: Vectras-VM-Android/tools/ci/external_sources.manifest (pinned commit reference)
**Touchpoint 3 (Evidence)**: Vectras-VM-Android/reports/external-sources-receipt.json (generated)
**Touchpoint 4 (Mapa Intake)**: RafPolimata federated evidence

**State Transitions**: (Same as R1)

**Blocking Conditions**: (Same as R1)

---

### Lane R3: Gradle Build Execution
**Provider**: Vectras-VM-Android/tools/gradle_with_jdk21.sh  
**Touchpoint 1 (Trigger)**: android-ci.yml: Build job (O4 gate)
**Touchpoint 2 (Input)**: Resolved external sources from R1/R2
**Touchpoint 3 (Output)**: app/build/outputs/apk/ (O5 artifact)
**Touchpoint 4 (Evidence)**: ci-artifacts/android-reports/ (build receipt)

**State Transitions**:
- R3.init: resolve job completes (O0-O3 gates pass)
- R3.build: gradle_with_jdk21.sh assembleDebug
- R3.artifact: APK checksum computed (O5 TESTED_LOCAL)
- R3.evidence: APK_ABI_BOOTSTRAP_INVENTORY.md generated

**Blocking Conditions**:
- R1/R2 not VERIFIED (external sources missing)
- Android SDK unavailable (O3 TOKEN_VAZIO)
- Gradle exit code != 0 (O4 FAIL)

---

### Lane R4: ABI Validation
**Provider**: Vectras-VM-Android/tools/ci/validate_lowlevel_abi.sh  
**Touchpoint 1 (Input)**: compiled artifact from R3
**Touchpoint 2 (Contract)**: orquestrador/contracts/abi_profile.v1.json
**Touchpoint 3 (Output)**: ABI signature + compatibility matrix
**Touchpoint 4 (Gate)**: O7 enforcement (abi-contract-gate job)

**State Transitions**:
- R4.init: R3 artifact available
- R4.validate: compare compiled vs contract signature
- R4.evidence: validation receipt generated
- R4.result: VERIFIED_LIMITED or TOKEN_VAZIO (device pending)

**Blocking Conditions**:
- Artifact missing (R3 FAIL)
- Contract undefined (O2 TOKEN_VAZIO)
- Signature mismatch (O7 CONTRADICTION)

---

### Lane R5: Device Runtime (BLOCKED)
**Provider**: Physical Android device or emulator  
**Touchpoint 1 (Input)**: Signed APK from R3
**Touchpoint 2 (Installation)**: `adb install` or emulator launch
**Touchpoint 3 (Execution)**: ANativeActivity observation + logcat capture
**Touchpoint 4 (Evidence)**: device_runtime_receipt.json (O8 TESTED_DEVICE)

**State Transitions**:
- R5.init: APK signed (O6 PASS assumed)
- R5.install: adb install (device_unavailable → TOKEN_VAZIO)
- R5.run: ANativeActivity.onCreate observed
- R5.evidence: logcat lines captured + exit code recorded

**Blocking Conditions**:
- Device unavailable (O3/O8 → TOKEN_VAZIO)
- APK signature invalid (O6 FAIL)
- Device policy restricts installation

---

### Lanes R6-R12: Reserved for Expansion
**R6**: Termux package integration  
**R7**: RafPolimata federated doctor pass  
**R8**: Mapa governance reconciliation  
**R9**: Rollback ledger audit  
**R10**: Independent replication (external)  
**R11**: Performance baseline  
**R12**: Security audit  

---

## Touchpoint Coordination Rules

### Rule T1: No Concurrent Modification
**Scope**: Manifest, receipt files, control-plane snapshots  
**Enforcement**: Lock file (lane_lock.v1.json) + timestamp check  
**Violation**: Last-write-wins + conflict recorded in audit log

### Rule T2: Evidence Immutability  
**Scope**: All receipt files (*.receipt.json, *-receipt.json)
**Enforcement**: git commit hash + append-only ledger  
**Violation**: Falsified receipt invalidates chain (O10 FAIL)

### Rule T3: Upstream Notification
**Scope**: When lane output affects another lane's input  
**Enforcement**: Event envelope posted to data/events/lane_*.jsonl  
**Violation**: Cascading failure without audit trail (O11 FAIL)

### Rule T4: Cycle Boundary  
**Scope**: Observations must complete within calendar cycle  
**Enforcement**: next_verifiable_step defines deadline  
**Violation**: Stale evidence demoted to TOKEN_VAZIO after 7 days

---

## Touchpoint Health Dashboard

```
Lane R1 (QEMU Source)
  ├─ Touchpoint 1 (Source)      ✓ VERIFIED (master = b274de47)
  ├─ Touchpoint 2 (Consumer)    ✓ VERIFIED (manifest updated)
  ├─ Touchpoint 3 (Evidence)    ✓ GENERATED (2026-08-21T05:57:25Z)
  └─ Touchpoint 4 (Intake)      ✓ PROCESSED (external-source-evidence.v1)

Lane R2 (AndroidX Source)
  ├─ Touchpoint 1 (Source)      ✓ VERIFIED (androidx-main = e3c10c6a)
  ├─ Touchpoint 2 (Consumer)    ✓ VERIFIED (manifest updated)
  ├─ Touchpoint 3 (Evidence)    ✓ GENERATED (2026-08-21T05:57:23Z)
  └─ Touchpoint 4 (Intake)      ✓ PROCESSED (external-source-evidence.v1)

Lane R3 (Gradle Build)
  ├─ Touchpoint 1 (Trigger)     ⊘ PENDING (awaiting CI run)
  ├─ Touchpoint 2 (Input)       ✓ READY (R1/R2 verified)
  ├─ Touchpoint 3 (Output)      ⊘ TOKEN_VAZIO (no APK yet)
  └─ Touchpoint 4 (Evidence)    ⊘ TOKEN_VAZIO (no build receipt)

Lane R4 (ABI Validation)
  ├─ Touchpoint 1 (Input)       ⊘ TOKEN_VAZIO (R3 artifact pending)
  ├─ Touchpoint 2 (Contract)    ✓ DEFINED (abi_profile.v1.json)
  ├─ Touchpoint 3 (Output)      ⊘ TOKEN_VAZIO
  └─ Touchpoint 4 (Gate)        ⊘ TOKEN_VAZIO

Lane R5 (Device Runtime)
  ├─ Touchpoint 1 (Input)       ⊘ TOKEN_VAZIO (R3 APK pending)
  ├─ Touchpoint 2 (Installation)⊘ BLOCKED (no device available)
  ├─ Touchpoint 3 (Execution)   ⊘ TOKEN_VAZIO (device unavailable)
  └─ Touchpoint 4 (Evidence)    ⊘ TOKEN_VAZIO (device unavailable)
```

---

## Troubleshooting Guide

### Symptom: Lane R1 recovery_rank >= 1
**Root Cause**: Pinned commit not found in remote  
**Investigation**: `git ls-remote https://github.com/rafaelmeloreisnovo/qemu_rafaelia master`  
**Recovery**: Execute fallback (rank 1: use master HEAD)  
**Prevention**: Update manifest with verified SHA weekly

### Symptom: Lane R3 artifact missing despite Gradle exit=0
**Root Cause**: expect_app_artifacts=false or build variant mismatch  
**Investigation**: Check `resolve` job outputs + build.log  
**Recovery**: Re-run with correct profile (official_arm64)  
**Prevention**: Validate artifact_variants before build

### Symptom: Lane R4 signature mismatch
**Root Cause**: ABI contract changed; artifact not rebuilt  
**Investigation**: Compare compiled signature vs contract definition  
**Recovery**: Rebuild R3 with new contract  
**Prevention**: Versioning + schema migration gate

### Symptom: Lane R5 always TOKEN_VAZIO
**Root Cause**: No device/emulator in CI environment  
**Investigation**: `adb devices` or emulator availability  
**Recovery**: Mark as expected gap (O8 TOKEN_VAZIO)  
**Prevention**: Document device unavailability in contract

---

## Lane Dependencies (DAG)

```
R1 (QEMU source) ─┐
                  ├─→ R3 (Gradle build) ─┬─→ R4 (ABI validation)
R2 (AndroidX)    ─┘                      └─→ R5 (Device runtime, BLOCKED)
                                         └─→ R6-R12 (reserved)
```

**Critical Path**: R1 → R2 → R3 → (R4 or R5)  
**Blocked**: R5 requires device provisioning  
**Alternative**: R4 validates without device (O7 PARTIAL state)
