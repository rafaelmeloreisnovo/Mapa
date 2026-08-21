# Observations Mapping Matrix

## Purpose
Maps ecosystem observations (O0-O11 orchestrator gates) to evidence states and determines promotion pathways through TOKEN_VAZIO boundaries.

## O0-O11 Orchestration Gate Mapping

### Tier 1: Source Identity Gates (O0-O2)

| Gate | Observation | State | Evidence Required | Falsifier | Blocked By |
|------|-------------|-------|-------------------|-----------|-----------|
| O0 | Source repository exists | VERIFIED | Repository URL resolvable | 404 on remote | None |
| O1 | Pinned commit accessible | VERIFIED_LIMITED | Commit reachable from branch | commit_not_found OR not_ancestor | recovery_required |
| O2 | ABI contracts defined | DECLARED | Schema file present + valid | schema_validation_fail | contract_missing |

### Tier 2: Compilation Gates (O3-O5)

| Gate | Observation | State | Evidence Required | Falsifier | Blocked By |
|------|-------------|-------|-------------------|-----------|-----------|
| O3 | Android SDK/NDK available | TOKEN_VAZIO | Environment provisioned | sdk_not_found | O0-O2 |
| O4 | Gradle tasks execute | TESTED_LOCAL | build.log + exit_code=0 | exit_code!=0 | O3 |
| O5 | APK artifact produced | TESTED_LOCAL | apk_path + sha256 | apk_not_found OR hash_mismatch | O4 |

### Tier 3: Validation Gates (O6-O8)

| Gate | Observation | State | Evidence Required | Falsifier | Blocked By |
|------|-------------|-------|-------------------|-----------|-----------|
| O6 | APK signature valid | TESTED_LOCAL | signature_receipt + verifier_log | signature_fail | O5 |
| O7 | ABI compatibility proven | PARTIAL | abi_profile_match | abi_mismatch OR test_fail | O6 |
| O8 | Device runtime executable | TOKEN_VAZIO | device_launch_receipt + ANativeActivity_log | launch_fail OR device_unavailable | O7 |

### Tier 4: Ledger & Closure Gates (O9-O11)

| Gate | Observation | State | Evidence Required | Falsifier | Blocked By |
|------|-------------|-------|-------------------|-----------|-----------|
| O9 | Rollback ledger recorded | IMPLEMENTED | append-only_jsonl + entry_count>0 | ledger_corrupted OR entry_missing | O8 |
| O10 | Audit trail complete | AUDIT | git_commits + validation_runs + workflow_metadata | gap_in_trail | O9 |
| O11 | Closure criteria satisfied | TOKEN_VAZIO | all_gates_status_recorded | any_gate_unresolved | O10 |

## TOKEN_VAZIO Preservation Rules

### Rule 1: No Silent Promotion
Condition: `gate_state == TOKEN_VAZIO`
Action: Explicitly list gap in `F_gap` + require `next_verifiable_step`
Violation: claim_allowed → false (unrecoverable)

### Rule 2: Evidence Binding
Condition: Claim state change
Action: Bind evidence to commit/timestamp/environment
Violation: Stale evidence treated as TOKEN_VAZIO

### Rule 3: Fallback Transparency
Condition: Recovery rank >= 1
Action: Log attempt + reason + result in append-only ledger
Violation: Unrecorded fallback invalidates chain

## Observation Lifecycle per Module

### MOD-QEMU-INTEGRATION
```
O0 ✓ VERIFIED (rafaelmeloreisnovo/qemu_rafaelia exists)
O1 ✓ VERIFIED (2346c30c2ba77881c2930add83523ea903b173fe accessible)
O2 ✓ DECLARED (abi_validation.v1.schema defined)
O3 ⊘ TOKEN_VAZIO (no emulator in CI environment)
O4 ⊘ TOKEN_VAZIO (gradle tasks pending O3)
O5 ⊘ TOKEN_VAZIO (APK pending O4)
O6 ⊘ TOKEN_VAZIO (signature pending O5)
O7 ⊘ PARTIAL (ABI profile defined, validation pending)
O8 ⊘ TOKEN_VAZIO (device unavailable)
O9 ⊘ IMPLEMENTED (rollback ledger structure ready)
O10 ⊘ AUDIT (audit trail collection in progress)
O11 ⊘ TOKEN_VAZIO (closure blocked on O8)
```

### MOD-ANDROIDX-ABI-VALIDATOR
```
O0 ✓ VERIFIED (wojcikiewicz17/androidx_RmR exists)
O1 ✓ VERIFIED (e3c10c6ac1acff50774d14417d93eaa6b5f8169a accessible)
O2 ✓ DECLARED (androidx_contracts.v1.json defined)
O3 ⊘ TOKEN_VAZIO (AndroidX API level pinning pending)
O4-O8 ⊘ TOKEN_VAZIO (cascading dependency on O3)
O9-O11 ⊘ TOKEN_VAZIO (awaiting O4-O8 completion)
```

## Promotion Pathways

### Pathway A: Full Green (All O0-O11 ✓)
Condition: Zero TOKEN_VAZIO entries
Action: Auto-promote with audit receipt
Gate: `claim_allowed=true`

### Pathway B: Partial (O0-O7 ✓, O8-O11 ⊘)
Condition: Device execution blocked
Action: Promote with limitations (local-only execution proof)
Gate: `claim_allowed=false` (requires human authorization)

### Pathway C: Recovery (Any O rank >= 1)
Condition: Fallback activated
Action: Log recovery attempt + preserve both success/failure paths
Gate: `claim_allowed=false` until O8 passes on recovered source

## Audit Queries

Find all observations in recovery state:
```bash
jq '.external_sources[] | select(.recovery_rank != "rank_0_original_pin")' data/control-plane/*.json
```

Find all TOKEN_VAZIO observations awaiting verification:
```bash
grep -r "TOKEN_VAZIO" data/ | grep "next_verifiable_step"
```

Find observations exceeding 7-day stale threshold:
```bash
jq '.[] | select(.observed_at < (now - 604800))' data/control-plane/current_state_snapshot.v1.json
```
