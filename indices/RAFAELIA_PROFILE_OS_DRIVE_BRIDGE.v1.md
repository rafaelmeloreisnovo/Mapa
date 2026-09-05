# RAFAELIA PROFILE OS — Drive Bridge V1

**observed_at:** 2026-09-05  
**repository:** `rafaelmeloreisnovo/Mapa`  
**branch:** `audit/profile-os-20260905`  
**claim_allowed:** `false`

## Contract

`SOURCE → TRANSFORM → CLAIM → TEST/EVIDENCE → RECEIPT → INDEX → MEMORY`

Preserve:

`VISÃO ≠ ARTEFATO ≠ EXECUÇÃO ≠ EVIDÊNCIA ≠ CLAIM`

`filename/title ≠ identidade`

`índice ≠ autoridade`

`ausência de evidência ≠ evidência de ausência`

`TOKEN_VAZIO` is a valid auditable state until a closure gate is proven.

## Canonical Drive control plane

- Root folder: `00_RAFAELIA_PROFILE_OS — Estratégia→Tática→Ciclos`
- Drive folder ID: `1hBGmocMIvWbMdSga3j4rlMGWp3N54y_8`

### Subfolders

- `00_INDEX_E_MAPA` → `1xKP24ExovK2Oaha6ATcHGSkBE9Ac71h5`
- `01_ESTRATEGIA_DO_PERFIL` → `1DEHFV-74AOhBSoja8G5Cb1Uy25CmEPIn`
- `02_TATICAS_OPERACIONAIS` → `1cj8RlUrdd9KBwUj3dv6FFLQhX5yBx-1q`
- `03_CICLOS_E_RECEIPTS` → `1MGWVstxZW35cez3JjiTQhjDZGzmebm9Q`
- `04_BIBLIOTECA_E_BIBLIOTECARIA` → `1aKaJ48Yaq-Gi2w_TyqiM-DGWLnTM4KHm`
- `05_INVENTARIO_E_MEMORIA_LOTCP` → `1JqIyQ6zIWbEa8Ngwm80McJyuy_hd8V5l`
- `06_INTEGRACOES_GMAIL_CALENDAR_GITHUB` → `1XGxEy1VjL1f8EgWwJ0kT5CX_jVYMQX16`
- `07_CIRURGIA_INSTRUCOES_PERSONALIZADAS` → `1QRZ3DFPmDi3V4rbnc0uam5u1OziR-U3u`

## Native Drive objects

- Architecture Doc ID: `1qgAo7SwfhGPyssYNThfrwXgoJOq8wp5byRAn8aQS2m8`
- Strategy Doc ID: `16GDThsOeQdQrNtpuovsa84CNYqmU4ZZEb-H7oKzsO8c`
- Tactics Doc ID: `1rZIvII75dduQ51iYnVDwjAkY9wTUTfv5lfyvfitxIYs`
- Cycle Template Doc ID: `1JLFl4op0rT6mj1rim0YGsU6kcct91t2ih-TKoO7u0vs`
- Inventory Sheet ID: `1soYdtdfdLlbzX1esHaFh5rr1Ew-DzvzDfiNNJ5A8IbU`

## Provider roles

| Provider | Role | Canonical anchor | Write policy |
|---|---|---|---|
| Google Drive | operational memory, navigation, receipts | root folder ID above | ID-first, append-only where applicable |
| Gmail | signal inbox / triage | `Label_7` | label-first; no indiscriminate bulk mutation |
| Google Calendar | review cadence | `j3156kcp55s348js1ud3s8mae0` | points to Drive; does not replicate memory |
| GitHub | execution/versioning bridge | this file on audit branch | branch-first; no direct default/protected write |

## Operational consolidation R4 — provider-bound

- Strategy/Tactics are materialized as native Google Docs in folders 01/02.
- Machine registry: `data/control-plane/PROFILE_OS_REGISTRY.v1.json`.
- Supersession ledger: `data/control-plane/PROFILE_OS_SUPERSESSION.v1.jsonl`.
- Gap ledger: `data/control-plane/PROFILE_OS_GAPS.v1.jsonl`.
- Schema: `schemas/profile_os_registry.v1.schema.json`.
- Validator: `scripts/validate_profile_os_registry.py`.
- Regression tests: `tests/test_profile_os_registry.py`.
- CI gate: `.github/workflows/profile-os-registry.yml`.
- Receipt: `receipts/PROFILE_OS_CONSOLIDATION_R4_20260905.md`.

Dedup relation: baseline Sheet `1sHO6_VCwIx0UozZU0h5ziBU0B7-hmLUQBNlsx3TIt2U` `SUPERSEDED_BY` expanded Sheet `1-13h93Q_iOyuuGvrMNt5AG4-vYWPLux2UIWbk8khaLk`; both preserved, no delete.

## Governance

- No merge or release is authorized by this bridge.
- No automatic promotion of custom-instruction claims.
- `claim_allowed=false` remains the fail-closed default.
