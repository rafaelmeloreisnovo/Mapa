# GitHub Delta 5h — 2026-08-21

Estado: NAVIGABLE_INDEX_V1
Janela observada: ~15:20–20:20 BRT (2026-08-21)
Princípio: VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM

## Rota principal

objetivo → repo → PR → evidência → estado → F_gap → F_next

## Índice por objetivo

### 1. Produzir RAFCODEPHI ARM utilizável
- Repo: `rafaelmeloreisnovo/termux-app-rafacodephi`
- PR #380 — `ci(beta): execute libLLVM18-unblocked usable build`
  - Estado: MERGED
  - Merge: `f7cea13d01cc80cb7afc4a3d5c2cce10083f8ace`
  - Função: executar caminho patched de source-build e matriz de APKs.
- PR #381 — `ci: execute usable RAFCODEPHI ARM APK build`
  - Estado: MERGED
  - Merge: `c57ceec62bba4058cb9ab7b9008a93aed992e6c9`
  - Gate: exigir ARM32 + ARM64 + APKs assinados + SHA256 antes de sucesso.
- PR #382 — `ci: localize RAFCODEPHI bootstrap failure by ABI`
  - Estado: MERGED
  - Merge: `a7a511db0d500d20a15fbecdf01d27de58f028fc`
  - Evidência: `apk_count=0`, `bootstrap_build=failure`, `physical_android=TOKEN_VAZIO`.
  - F_gap: APK utilizável ainda não provado.
  - F_next: rerun ARM32 isolado após correção da host closure.

### 2. Fechar dependências host do Termux build
- Repo: `rafaelmeloreisnovo/termux-packages`
- PR #89 — `fix(libxml2): restore libLLVM18 host runtime on current main`
  - Estado: MERGED
  - Merge: `8a3587789c415912c04b83fc4bb82fe69c55d595`
  - Antes: Doxygen falhava por `libLLVM.so.18.1` ausente.
  - Depois: build avançou além desse mecanismo.
- PR #92 — `fix(libxml2): close host Doxygen libxml2 runtime`
  - Estado: OPEN
  - Head: `69c6959004f2fefe13b4a2122bbdfd0a66f3e8b0`
  - Evidência causal: run `32531572529`, job `96924467031`, Meson `[37/111]`, exit `127`.
  - Erro: `libxml2.so.2: cannot open shared object file`.
  - Log SHA256: `614d8d39698aad19818bfae956f46dd056e06b4e8f868c2092248b3afb7b1ccf`.
  - F_gap: rerun após patch.
  - F_next: ARM32 before→after; só depois AArch64.
- PR #91 — `FASE 1: Add CLAUDE.md bootstrap governance`
  - Estado: OPEN / DRAFT
  - Head: `2a2e7298d24236b098873e200a100884eb5194f0`
  - Nota: não tratar como estado canônico de `main`.

### 3. Navegação federada / Mapa
- Repo: `rafaelmeloreisnovo/Mapa`
- PR #335 — `audit: federated Ω lifecycle cycle after adaptive watchdog merge`
  - Estado: MERGED
  - Merge: `96c21ef0dd221c0f6bdf1da06834116729c7ffd6`
  - Conteúdo: lifecycle ledger, impact radius, gaps, incerteza before→after, hazards, F_next, validator fail-closed.
  - P0 preservado: `PROVIDER_SERVER_BARRIER_FIELD_FAILURE_20260821`.
  - F_gap: proteção server-side real ainda não provada.

### 4. Triagem determinística de source gaps
- Repo: `rafaelmeloreisnovo/RafGitTools`
- PR #370 — `audit: turn source-gap baseline into deterministic triage registry`
  - Estado: MERGED
  - Merge: `5890ae0a1753072e38dff440041dcad04186797c`
  - Baseline: `257 files / 82 blockers / 34 warnings`.
  - Navegação: `priority × structural_owner × marker`.
  - Invariante: triage PASS != source-gap PASS.
  - F_gap: 82 blockers continuam dívida real.

### 5. Coerência ≠ autoridade de claim
- Repo: `rafaelmeloreisnovo/Vectras-VM-Android`
- PR #1104 — `governance: separate VC coherence from federated claim authority`
  - Estado: MERGED
  - Merge: `bcb2947e02855a99b0842c39b2f9d4669da6a1c0`
  - Invariantes:
    - `COHERENCE_SCORE != CLAIM_AUTHORITY`
    - `CLASSIFICATION_FORTE != CLAIM_ALLOWED`
    - `VECTOR_VALIDATION != FEDERATED_EVIDENCE`
  - F_gap: IPC integrity, QEMU execution-time identity, data minimization, physical Android E2E.

## Índice por estado

### MERGED / canônico
- Mapa #335
- RafGitTools #370
- Vectras #1104
- termux-app #380
- termux-app #381
- termux-app #382
- termux-packages #89

### OPEN / ainda não canônico
- termux-packages #92 — correção `libxml2.so.2`; rerun ARM32 pendente.
- termux-packages #91 — governança CLAUDE.md; draft.

### TOKEN_VAZIO / não promover
- `APK_USABLE`
- `PHYSICAL_ANDROID`
- `PROVIDER_SERVER_BARRIER`
- `QEMU_EXECUTION_TIME_IDENTITY`
- `IPC_INTEGRITY_E2E`
- `SCIENTIFIC_REPLICATION`

## Índice causal

```text
TERMUX APK
  └─ source-build bootstrap
      └─ ARM32 first failure
          ├─ libLLVM.so.18.1 missing
          │   └─ #89 MERGED
          └─ libxml2.so.2 missing
              └─ #92 OPEN
                  └─ rerun ARM32
                      ├─ PASS → AArch64 → APK matrix → SHA256 → physical install
                      └─ FAIL → capture first new stderr → bounded correction

FEDERATION
  ├─ Mapa #335 → lifecycle ledger + P0 preservation
  ├─ RafGitTools #370 → 82 blockers become deterministic triage
  └─ Vectras #1104 → coherence separated from claim authority
```

## Rota de navegação recomendada

1. `TERMUX_BUILD` → termux-packages #92
2. `ARM32_GATE` → run 32531572529 / log SHA256 614d8d39…
3. `APK_GATE` → termux-app #381/#382
4. `FEDERATED_STATE` → Mapa #335
5. `SOURCE_GAPS` → RafGitTools #370
6. `CLAIM_BOUNDARY` → Vectras #1104
7. `PROVIDER_BARRIER` → manter P0 até prova server-side

## R3

- F_ok: delta de 5h transformado em rotas navegáveis por objetivo, repo, PR, estado, evidência e próximo gate.
- F_gap: #92 ainda sem rerun; provider barrier e physical Android continuam `TOKEN_VAZIO`.
- F_next: executar #92 → rerun ARM32 → registrar before→after → atualizar este índice append-only.
