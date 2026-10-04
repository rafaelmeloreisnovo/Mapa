# Repository Exposure + Authorial Freestanding Matrix V1

**Snapshot:** 2026-10-04  
**Owner:** `rafaelmeloreisnovo`  
**Observed:** 90 repositories = 30 public + 60 private  
**Authority:** `Mapa` control-plane  
**Machine matrix:** `data/control-plane/repository_exposure_freestanding.v1.json`

This document materializes the exposure rule requested for the ecosystem. It does **not** change any repository visibility by itself.

## 1. Core invariant

```text
PUBLIC != AUTHORIAL
AUTHORIAL != FREESTANDING
FREESTANDING_PASS requires evidence
TOKEN_VAZIO != 0
IMPLEMENTED_UNTESTED != PASS
```

This extends the canonical authorship/provenance rule in `docs/governance/AUTHORSHIP_PROVENANCE_INVARIANT_V1.md`: repository ownership alone is not proof of authorship, and derivation must retain the path to the source.

The target public surface is:

```text
AUTHORIAL
  ∩ provenance-clear
  ∩ runtime-independent in the declared scope
  ∩ reproducible
  ∩ sanitized
  ∩ low-friction
```

## 2. Meaning of freestanding in this gate

A core can be promoted to `FREESTANDING_PASS` only when evidence establishes all of the following:

1. authorial core provenance is resolved;
2. no runtime/link-time dependency on libc, JVM, Python, Android, Node or a third-party runtime in the declared core scope;
3. no required external service for core execution;
4. deterministic build or exact reproduction recipe exists;
5. tests/execution receipt exist;
6. licenses and upstream attribution are resolved;
7. default branch secret scan passes;
8. full Git history, releases and non-default branches are scanned before public promotion.

A compiler/linker may be a **build-time tool**. That does not by itself invalidate a freestanding produced artifact. Runtime independence and reproducibility must be stated separately.

**Inventory result V1:** no repository is promoted to `FREESTANDING_PASS` from metadata, naming or intent alone. Unverified candidates remain `TOKEN_VAZIO`.

## 3. Highest-priority route

### P0 — close or sanitize

`TRABALHO_ROADMAP_AUDIT_GOV_DATA_ROTA_MAPwithCHAIN_security`

Current state: public.  
Recommendation: `CLOSE_PENDING_SANITIZED_EXPORT`.

Reason: this surface is governance/security/Drive-routing oriented. Internal routing/control should remain private; if useful publicly, export a separate sanitized specification.

### P0 — split, do not simply open

`RafNet-Core`

Current state: private.  
Recommendation: `SPLIT_PUBLIC_CORE_PRIVATE_CONTROL`.

Route:

```text
RafNet-Core private producer
        │
        ├── private federation / control / historical authority
        │
        └── extract clean authorial transport core
                    ↓
          authorship + dependency + build
          + tests + license + full-history secret scan
                    ↓
             public-core candidate
```

This prevents the public transport/spec/test work from dragging private federation/control surfaces with it.

### P1 — review already-public repositories

`DeepSeek-RafCoder`, `ROM-emulator`, `TeoremasTesesTeorias`, `TinyGPT`, `runner-images_RAFCODE`, `treinarModelos`.

Recommendation: `REVIEW_PUBLIC`.

They can remain public during review, but must not be presented as authorial/freestanding until provenance, datasets/artifacts, dependencies, licensing and Git history are audited.

## 4. Public derived/upstream lane

### Confirmed public lineage — keep public

`actions`, `linuxkernel`, `relativity-living-light`.

These already have confirmed fork/backup lineage in the observed metadata. They are valid public provenance/collaboration surfaces, but the fork itself is not proof of an exclusively authorial core.

### Keep public, prove the delta

`BLAKE3`, `CryptoSwift_RmR`, `LuaJIT`, `Shizuku`, `UserLAnd2`, `Vectras-VM-Android`, `androidRom`, `android_frameworks_base_rafaelia`, `androidx_RmR`, `arxiv-docs`, `florisboard`, `frida-desktop`, `gradle`, `llvm-project_rafcode`, `openssl`, `termux-api_rafcodephi`, `termux-app-rafacodephi`, `termux-packages`.

Recommendation: `KEEP_PUBLIC_REVIEW_PROVENANCE`.

For each one, identify:

```text
upstream@revision
→ local delta
→ author/contributor role
→ license
→ tests
→ receipts
```

### Low-risk public surfaces

`Vazio`, `myCat-iahelpsus` → `KEEP_PUBLIC_LOW_RISK`.

No `AUTHORIAL` or `FREESTANDING_PASS` claim is inferred merely because they are public.

## 5. Private control/memory/custody lane

Keep private:

`CONVERSATIONS_CHUNKS_PRIVATE`, `GAIA-PDS-PHI`, `Geral`, `IaFcea`, `Img`, `Judicial-`, `Mapa`, `MemRa`, `MemRafcode`, `OMEGAGIT`, `PCR_Rafaelia_Code_seed`, `RAFNATIONS_CORE`, `RAIAREIS_FRAMEWORK`, `RafGitTools`, `Rafaelia_Private`, `Recipt`, `Seguran-a-informacional-`, `Semente`, `Tora`, `X0`, `ZIPRAF_CORE`, `ZIPRAF_OMEGA_FULL`, `home`, `llamaRafaelia`, `privadoFazendo`, `rafaelia-core-enterprise`, `rafaelia_privado`, `templo-vivo-arcs`.

Recommendation: `KEEP_PRIVATE`.

The preferred public route for these repositories is **sanitized export**, not changing the original repository to public.

## 6. Private authorial/research candidates

Keep private until the publication gate closes:

`Catalogo-cosmologico`, `ChipQuantum`, `CientiEspiritual`, `CientiEspiritual-tiEs-`, `Clima`, `Cosmos`, `CreFeBerna`, `Espiritual-espirualidade`, `Est-dio-de-udio`, `Fisica`, `GAIA_phi`, `GEOMETRIA_SOLAR_Maia_Inca`, `GaiaPhiRafcode`, `Graditao`, `IA_nist`, `Matem-tica-`, `RafPolimata`, `RafaelCiencias`, `RafaelIA_Solucoes_Clay`, `Rafaelia`, `Rafaelia_Core`, `Rafcodephi_Sdk_ndkJni_c_py_sh_asm_lua_rs_go_swift_perl_yml_`, `UserLAnd`, `V79-1`, `fcea-originum`, `nanoGPT`, `new`, `papers`, `qemu_rafaelia`, `teoremas`, `verbum-vivo`.

Recommendation: `PUBLIC_AFTER_GATE`.

This group is where the authorial/freestanding effort should be concentrated. It is intentionally **not** marked freestanding yet.

## 7. Publication gate

```text
AUTHORSHIP
    ↓
DEPENDENCY BOUNDARY
    ↓
BUILD / REPRODUCTION
    ↓
TEST / EXECUTION RECEIPT
    ↓
LICENSE / SOURCE ATTRIBUTION
    ↓
SECRET SCAN — DEFAULT
    ↓
SECRET SCAN — HISTORY / RELEASES / BRANCHES
    ↓
DATA / DEVICE / DRIVE SANITIZATION
    ↓
CLAIM BOUNDARY
    ↓
PUBLICATION
```

A failure or missing field is not coerced to false or zero:

`missing -> TOKEN_VAZIO -> resolve only the missing evidence`.

## 8. Low-friction topology

```text
PRIVATE CONTROL / MEMORY / CUSTODY
        │
        ├── sanitized export
        ▼
AUTHORIAL CORE CANDIDATE
        │
        ├── authorship gate
        ├── dependency gate
        ├── reproduction gate
        ├── evidence gate
        └── secret/history gate
        ▼
PUBLIC AUTHORIAL CORE
```

Upstream projects use a distinct path:

```text
UPSTREAM / FORK
   ↓
PROVENANCE + LICENSE
   ↓
AUTHORIAL DELTA (if present)
   ↓
PUBLIC DERIVED PROJECT
```

Do not merge these two paths.

## 9. Change discipline

- No visibility mutation is authorized by this V1 alone.
- Visibility changes happen only after the corresponding gate is reviewed.
- `FREESTANDING_PASS` requires evidence and receipt.
- Private authority repositories publish by separate sanitized artifact whenever possible.
- If producer evidence contradicts this matrix, producer evidence wins and this matrix must be corrected append-only.

## 10. Machine gate

Validate the machine matrix with:

```bash
python3 scripts/validate_repository_exposure_matrix.py
```

Expected V1 scope:

```text
repositories = 90
public = 30
private = 60
all repositories appear exactly once in recommendation groups
all repositories appear exactly once in current-visibility sets
recommendation union == visibility union
```

## R3

`R3=<F_ok: 90-repository exposure topology materialized; F_gap: per-repo authorship/freestanding/full-history evidence remains TOKEN_VAZIO where not audited; F_next: validate matrix remotely, then execute gates first on CLOSE/SPLIT/REVIEW lanes before any visibility mutation>`
