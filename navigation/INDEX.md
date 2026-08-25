# RAFAELIA — Universal Navigation Index

**State:** `IMPLEMENTED_INDEX_ROOT`  
**Coverage:** `TOKEN_VAZIO`  
**Authority:** federated navigation mirror in `Mapa`; longitudinal navigation authority remains Google Drive `RAFAELIA — Master Navigation Registry V1`.

## 1. Root graph

```text
Ω
└─ domains
   └─ repositories
      └─ artifacts
         └─ evidence
            └─ claims
               └─ gaps
                  └─ experiments
                     └─ timeslices
                        └─ sources
```

Canonical traversal:

`objective → domain → repository → artifact/PR → evidence → state → gap → falsifier/gate → F_next → source`

## 2. Stable identifiers

- `REP:<repo>` — repository
- `ART:<repo>:<path>` — artifact/path
- `PR:<repo>#<n>` — pull request
- `EVD:<type>:<hash-or-run>` — evidence/receipt/run
- `GAP:<id>` — gap/TOKEN_VAZIO
- `SRC:DRIVE:<document_id>` — Drive authority/source
- `CYCLE:<YYYY-MM-DD>:<n>` — federated lifecycle cycle
- `TS:<YYYY-MM-DD>:<window>` — temporal snapshot

## 3. Relations

`IMPLEMENTS | EVIDENCES | BLOCKS | DEPENDS_ON | SUPERSEDES | DERIVED_FROM | MIRRORS | INDEXES | ACTIVATES`

## 4. States

`REFERENCE | IMPLEMENTED | PASS | FAIL | OPEN | TOKEN_VAZIO | SUPERSEDED`

### Invariants

- `OPEN != CANONICAL`
- `TOKEN_VAZIO != PASS`
- `VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`
- `COHERENCE != CLAIM_AUTHORITY`
- absence of observation is not proof of absence
- incomplete inventory remains `coverage_complete=TOKEN_VAZIO`

## 5. Navigation routes

1. **By repository** — locate implementation owner first.
2. **By domain** — cross-repository thematic traversal.
3. **By evidence** — run/hash/receipt → producing artifact → claim/gap.
4. **By gap** — unresolved state → owner → falsifier → next gate.
5. **By time/cycle** — chronological deltas without turning snapshots into authority.
6. **By source** — Drive/GitHub authority and provenance.
7. **By claim state** — `PASS`, `FAIL`, `OPEN`, `TOKEN_VAZIO`, `SUPERSEDED`.
8. **By next gate** — execution queue ordered by falsifiability/unblocking value.
9. **Cross-repo causal route** — producer → consumer → evidence → federated state.
10. **By activation edge** — objective → component → condition → gate → output → TOKEN_VAZIO fallback.

## 6. GitHub inventory — observed pass

Observed repository count in the connected GitHub inventory: **84**. This is an observed inventory, not an exhaustive-account proof; `coverage_complete=TOKEN_VAZIO`.

### 6.1 Core / knowledge / memory

- `REP:Rafaelia`
- `REP:Rafaelia_Core`
- `REP:rafaeliacoreenterprise`
- `REP:CientiEspiritualRAFCODE`
- `REP:CientiEspiritualBook`
- `REP:verbumindex`
- `REP:ZIPRAF`
- `REP:ZIPRAF_CORE`
- `REP:Mapa`
- `REP:MemRa`
- `REP:MemRafcode`
- `REP:OMEGAGIT`
- `REP:Recipt`
- `REP:Catalogo`
- `REP:Geral`
- `REP:RAIAREIS-core`
- `REP:newrafaelreia`
- `REP:PrivateRafaea`
- `REP:rafaelia_privado`
- `REP:privadoFazendoDeus`

### 6.2 Android / Termux / systems / runtime

- `REP:termux-app-rafacodephi`
- `REP:termux-packages`
- `REP:termux-api`
- `REP:Vectras-VM-Android`
- `REP:qemu`
- `REP:UserLAnd`
- `REP:UserLAnd2`
- `REP:Shizuku`
- `REP:androidx`
- `REP:androidRom`
- `REP:frameworks`
- `REP:ROMS`
- `REP:frida`
- `REP:linuxkernel`
- `REP:openssl`
- `REP:LuaJIT`
- `REP:actions`
- `REP:gradle`
- `REP:home-assistant`
- `REP:florisboard`

### 6.3 Science / mathematics / AI / security

- `REP:Cosmos`
- `REP:Fisica`
- `REP:GEOM`
- `REP:GAIA-PDS`
- `REP:GAIA_phi_RAF`
- `REP:Gaia`
- `REP:RafGitTools`
- `REP:RafPolimata`
- `REP:RafaelCiencias`
- `REP:Crypto`
- `REP:IA_nist`
- `REP:Seguranca`
- `REP:Matem`
- `REP:TeoremasTeses`
- `REP:teoremas`
- `REP:papers`
- `REP:arxiv-docs`
- `REP:ChipQuantumIA`
- `REP:Clay-Millennium-Problems`
- `REP:relativity`
- `REP:DeepSeek-V3`
- `REP:TinyGPT-V`
- `REP:llama.cpp`
- `REP:nano-bench`
- `REP:BLAKE3`
- `REP:X0`
- `REP:PCR`

### 6.4 Culture / publishing / apps / auxiliary domains

- `REP:V79`
- `REP:IaFceaBook`
- `REP:templo_vivo`
- `REP:fceabook`
- `REP:RafNet`
- `REP:RAFNATIONS`
- `REP:Espiritual`
- `REP:Judicial`
- `REP:Img`
- `REP:Graditao`
- `REP:myCat`
- `REP:CONVERSATIONSALAR`
- `REP:ClimaHondaSS`
- `REP:CreFe`
- `REP:Tora`
- `REP:treinar24h`
- `REP:Semente`

## 7. Canonical source bridge

- `SRC:DRIVE:1x_5x3_NdSaHtPLF9hbu8M1i0kvza_MnhtWeZycav19Y` → **RAFAELIA — Master Navigation Registry V1** — longitudinal navigation authority.
- `SRC:DRIVE:1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88` → **RAFAELIA — Implementação Latentes e Papers — Drive GitHub V1** — operational/evidence memory.
- `ART:Mapa:navigation/INDEX.md` → GitHub federated navigation mirror.
- `ART:Mapa:navigation/RAFAELIA_MASTER_REGISTRY.v1.json` → machine-readable registry.
- `ART:Mapa:navigation/SOURCES.md` → authority/provenance rules.
- `ART:Mapa:governance/ACTIVATION_REGISTRY_V1.json` → subordinate machine-readable activation registry.
- `ART:Mapa:docs/ACTIVATION_REGISTRY_V1.md` → human-readable activation contract.

## 8. Current cross-repository causal chain

### Termux ARM32 / APK route

```text
REP:termux-app-rafacodephi
  → PR:termux-app-rafacodephi#380 [MERGED]
  → PR:termux-app-rafacodephi#381 [MERGED]
  → PR:termux-app-rafacodephi#382 [MERGED]
  → EVD:RUN:32531572529
  → REP:termux-packages
       → PR:termux-packages#89 [MERGED: libLLVM18 closure]
       → deeper ARM32 execution
       → GAP:TERMUX_ARM32_LIBXML2_RUNTIME
       → PR:termux-packages#92 [OPEN]
       → F_next: rerun ARM32 only
```

Observed failure evidence for the current edge:

- run `32531572529`
- job `96924467031`
- log SHA-256 `614d8d39698aad19818bfae956f46dd056e06b4e8f868c2092248b3afb7b1ccf`
- terminal loader failure: missing `libxml2.so.2`
- `physical_android=TOKEN_VAZIO`

### Federated governance route

- `PR:Mapa#335` → federated Ω lifecycle ledger; provider/server barrier remains P0.
- `PR:RafGitTools#370` → deterministic source-gap triage; observed baseline `257 files / 82 blockers / 34 warnings` remains debt, not closure.
- `PR:Vectras-VM-Android#1104` → coherence classification separated from claim authority.

## 9. Temporal leaves

The previous 5-hour index is retained as historical evidence only:

- `TS:2026-08-21:5H` → `navigation/GITHUB_DELTA_5H_20260821.md`
- relation: `INDEXES`
- authority: `REFERENCE/TIMESLICE`, **not** master index.

## 10. Coverage ledger

| Layer | Observed state | Completeness |
|---|---|---|
| GitHub repository names | 84 observed | `TOKEN_VAZIO` |
| GitHub per-repo artifacts | partial | `TOKEN_VAZIO` |
| Drive RAFAELIA search space | candidates observed | `TOKEN_VAZIO` |
| Drive deduplication | not closed | `TOKEN_VAZIO` |
| Evidence/run/hash linking | partial | `TOKEN_VAZIO` |
| Claim-to-falsifier linking | partial | `TOKEN_VAZIO` |
| Activation edge coverage | registry implemented, runtime enforcement partial | `TOKEN_VAZIO` |

## 11. Append-only expansion order

1. repository → README/AGENTS/index/workflows/tests/receipts inventory;
2. artifact → stable `ART:` IDs + hashes/ref;
3. Drive candidate → authority/dedupe/source classification;
4. evidence → run/hash/receipt → producer/consumer links;
5. unresolved item → `GAP:` + falsifier + executable gate;
6. completed gate → append new state and `SUPERSEDES`; never erase prior state;
7. update longitudinal Drive registry and GitHub mirror together when authority permits;
8. activation edge → condition + input + gate + output + fallback TOKEN_VAZIO.

## 12. Activation Registry

Activation is now represented as a subordinate state machine rather than an implicit prompt convention:

```text
objective
  → bootstrap
  → authority_resolution
  → route_resolution
  → evidence_collection
  → gate_evaluation
  → execution
  → receipt
  → delta
  → index_feedback
  → retrofeedback
```

Machine contract: `governance/ACTIVATION_REGISTRY_V1.json`  
Human contract: `docs/ACTIVATION_REGISTRY_V1.md`

Pointer reconciliation:

- `GAP:ACTIVATION_MASTER_NAV_POINTER_DRIFT` — `PASS/FECHADO` on 2026-08-25. Drive Master Navigation Registry received an append-only supersession that binds the current federated mirror `navigation/INDEX.md`; readback passed and provenance is recorded at `data/receipts/navigation/2026-08-25-master-nav-pointer-drift.v1.json`.
- Legacy `docs/RAFAELIA_MASTER_NAV_REGISTRY_V1.md` is retained only as `SUPERSEDED` history; it is not the current mirror.

## R3

- `F_ok`: universal navigation root exists; activation semantics are explicitly indexed; the master-navigation pointer drift is reconciled with Drive readback + GitHub receipt; the 5h snapshot remains correctly demoted to a temporal leaf.
- `F_gap`: full-content coverage, Drive/GitHub deduplication, runtime activation enforcement, and other unresolved evidence gates remain `TOKEN_VAZIO`/open where applicable.
- `F_next`: validate this reconciliation delta in CI, merge it, verify `main`, then continue with the highest-unblocking unresolved evidence/runtime gap.

## 13. RafCode freestanding federation route

- `REP:RafGitTools` → [`PR:RafGitTools#381`](https://github.com/rafaelmeloreisnovo/RafGitTools/pull/381) → `OPEN_DRAFT_UNMERGED`;
- `ART:RafGitTools:native/rafcode_federation_v1` → implementation commit `7e72713da20b849a0d975d3dbefedd3d65ca0443`;
- [`EVD:RUN:32868449710`](https://github.com/rafaelmeloreisnovo/RafGitTools/actions/runs/32868449710) → dedicated x86-64/ARMv7/AArch64 gate `PASS`;
- `ART:Mapa:indices/runtime/RAFCODE_FEDERATION_V1.md` → human evidence-bound route;
- `ART:Mapa:data/federation/rafcode-federation-v1.json` → machine route;
- state: `EVIDENCED_SCOPED_DRAFT_UNMERGED`, limited to compile/link/ELF/hotpath and x86-64 smoke evidence;
- `GAP:RAFCODE:DEVICE_ARMV7`, `GAP:RAFCODE:DEVICE_AARCH64`, `GAP:RAFCODE:HMAC`, producer merge/main and repository-wide health remain `TOKEN_VAZIO`/open.

The route binds the three exact Drive/Mapa memory indices `LONGITUDINAL | ORTHOGONAL | TRANSVERSAL` with required mask `0x07`. Dedicated workflow success does not promote physical execution, global health, merge readiness or claim authority.
