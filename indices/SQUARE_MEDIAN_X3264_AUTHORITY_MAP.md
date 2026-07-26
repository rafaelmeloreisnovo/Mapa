# Square-Median x32/x64 — Authority and Evidence Map

## Canonical route

```text
papers PR #26 comment 5085010125
  ↓ authorial geometric request
papers PR #28
  ↓ formal mathematics, claims and falsifiers
qemu_rafaelia PR #65
  ↓ exact C kernel, ELF32/ELF64 and QEMU linux-user workflow
Vectras-VM-Android PR #1072
  ↓ Android consumer boundary and profile mismatch
Mapa
  ↓ authority, state, evidence pointers and next gates
```

## Responsibility table

| Object | Canonical repository | Current pointer | State |
|---|---|---|---|
| Mathematical definitions and proofs | `papers` | PR #28 / `9bdf0383...` | `OPEN_UNMERGED_VERIFIED_LOCAL` |
| Claims and falsifiers | `papers` | `claims.jsonl` in PR #28 | `VERIFIED_LOCAL` |
| Exact executable kernel | `qemu_rafaelia` | PR #65 / `97e1e4ef...` | `OPEN_UNMERGED_LOCAL_RECEIPT` |
| Determinant and area gate | `qemu_rafaelia` | C + rational reference | `VERIFIED_LOCAL` |
| x86-64 native execution | `qemu_rafaelia` receipt | exit `0` | `VERIFIED_LOCAL` |
| x86-32 ELF construction | `qemu_rafaelia` receipt | ELF32 i386 | `VERIFIED_LOCAL_BUILD_ONLY` |
| source-built QEMU i386/x86_64 execution | `qemu_rafaelia` workflow | PR #65 | `TOKEN_VAZIO_PENDING_WORKFLOW` |
| Android consumer profile | `Vectras-VM-Android` | PR #1072 / `f74ad1ed...` | `BLOCKED_PROFILE_MISMATCH` |
| Cross-repository custody | `Mapa` | evidence packet V1 | `ACTIVE_DRAFT` |

## Mathematical invariant

```text
T+ = 1/2 [[ 1,-1],[ 1,1]]
T- = 1/2 [[ 1, 1],[-1,1]]
```

The operators rotate by `±45°`, contract by `1/sqrt(2)`, map vertices to
side midpoints, and satisfy:

```text
T±ᵀT± = (1/2)I
det(T±) = 1/2
T+T- = T-T+ = (1/2)I
T-⁴ = -(1/4)I
T-⁸ = (1/16)I
```

The circumcircle of square `n+1` is the incircle of square `n`.

## Integration finding

The Vectras IPC v3 is a typed full-system QEMU profile. The PoC requires QEMU
linux-user executors. Adding `qemu-i386` and `qemu-x86_64` to the existing
allowlist without a separate argument profile is forbidden because the bridge
would prepend full-system arguments to linux-user binaries.

Required transition:

```text
IPC v3 SYSTEM_VM only
  ↓ explicit schema/version change
IPC v4
  ├── SYSTEM_VM
  └── LINUX_USER
```

## Promotion gates

A claim may be promoted only when its own evidence closes:

1. paper and claim ledger validate;
2. QEMU fork builds both linux-user executors;
3. both payloads return exit code `0` through those executors;
4. artifacts and executors receive hashes;
5. Vectras receives a typed linux-user profile before Android dispatch;
6. performance, ECC and physical-memory statements remain separate experiments.

```yaml
claim_allowed: false
source_built_qemu_execution: TOKEN_VAZIO
vectras_linux_user_dispatch: TOKEN_VAZIO
full_system_guest_boot: NOT_IN_SCOPE
```
