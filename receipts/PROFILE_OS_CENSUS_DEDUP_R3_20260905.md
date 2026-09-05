# RAFAELIA PROFILE OS — Censo Interno + DEDUP — R3 — 2026-09-05

state: VERIFIED_LIMITED
mode: APPEND_ONLY / NO_DELETE
claim_allowed: false
root_id: 1hBGmocMIvWbMdSga3j4rlMGWp3N54y_8

## Recursive census

- level_1_folders: 8
- level_2_folders: 1
- level_3_or_deeper_observed: 0
- internal_materialized_files: 6
- empty_observed_folders: 01_ESTRATEGIA_DO_PERFIL; 02_TATICAS_OPERACIONAIS; 06_INTEGRACOES_GMAIL_CALENDAR_GITHUB/01_PRODUCT_TOKEN_CYCLES__BILLING_METADATA_ONLY

### Tree

- 00_INDEX_E_MAPA [1xKP24ExovK2Oaha6ATcHGSkBE9Ac71h5]
  - Modular Addressing canonical doc [1FQMPS8mNVwf1QEwj2aUMPm1QBs8ia-M4oy2b4bPnomc]
  - Arquitetura e Protocolo de Evolução V1 [1qgAo7SwfhGPyssYNThfrwXgoJOq8wp5byRAn8aQS2m8]
- 01_ESTRATEGIA_DO_PERFIL [1DEHFV-74AOhBSoja8G5Cb1Uy25CmEPIn] — EMPTY_OBSERVED_NOT_SEMANTIC_ABSENCE
- 02_TATICAS_OPERACIONAIS [1cj8RlUrdd9KBwUj3dv6FFLQhX5yBx-1q] — EMPTY_OBSERVED_NOT_SEMANTIC_ABSENCE
- 03_CICLOS_E_RECEIPTS [1MGWVstxZW35cez3JjiTQhjDZGzmebm9Q]
  - TEMPLATE Ciclo de Evolução Profile OS V1 [1JLFl4op0rT6mj1rim0YGsU6kcct91t2ih-TKoO7u0vs]
- 04_BIBLIOTECA_E_BIBLIOTECARIA [1aKaJ48Yaq-Gi2w_TyqiM-DGWLnTM4KHm]
  - Bibliotecária Operacional V1 [1UtiHIRF-7lt7LiHsfjcoDg_umJEC_cP_K8s4b_KSktw]
- 05_INVENTARIO_E_MEMORIA_LOTCP [1JqIyQ6zIWbEa8Ngwm80McJyuy_hd8V5l]
  - Inventário e Ciclos V1 [1soYdtdfdLlbzX1esHaFh5rr1Ew-DzvzDfiNNJ5A8IbU]
- 06_INTEGRACOES_GMAIL_CALENDAR_GITHUB [1XGxEy1VjL1f8EgWwJ0kT5CX_jVYMQX16]
  - 01_PRODUCT_TOKEN_CYCLES__BILLING_METADATA_ONLY [1AJYPhZYkF2bbVCItD4xoWrat1eqkx6Ev] — EMPTY_OBSERVED
- 07_CIRURGIA_INSTRUCOES_PERSONALIZADAS [1QRZ3DFPmDi3V4rbnc0uam5u1OziR-U3u]
  - CHG-20260905-001 [1_zg3bPUFuYUl2E45XtdNcQDiT1sma9FPFgv6aNz1UCQ]

## DEDUP contract

identity_key = provider + provider_id + repository + commit + path
dedup_key = provider_id when available; otherwise content_hash + canonical_path
same_title != duplicate
TOKEN_VAZIO != 0

## Findings

1. PROFILE_OS internal exact-title scan: 6/6 UNIQUE_BY_PROVIDER_ID; duplicate deletable count=0.
2. MASTER_INDEX_CORPUS_000_050 homonym:
   - baseline snapshot: 1sHO6_VCwIx0UozZU0h5ziBU0B7-hmLUQBNlsx3TIt2U; 6818 bytes; 1 sheet CONCEITOS; modified 2026-08-23.
   - expanded successor: 1-13h93Q_iOyuuGvrMNt5AG4-vYWPLux2UIWbk8khaLk; 407819 bytes; 33 sheets; modified 2026-09-02.
   - relation: BASELINE_SNAPSHOT -> EXPANDED_SUCCESSOR.
   - action: preserve both; no delete. SUPERSEDED_BY may be appended only with explicit custody receipt.

## Provider bridge readback

- GitHub bridge predecessor: commit 33870cf391fe2ddec5831e8560caeaca95b4eff7; blob f05d66344697d0809370d0dc5bde1fbcaa5c7600; eight Drive folder IDs match current readback.
- Gmail: Label_7 / RAFAELIA/Profile-OS/Inbox; 0 messages; 0 threads.
- Calendar: j3156kcp55s348js1ud3s8mae0; weekly Monday 18:30–19:00 America/Sao_Paulo; private.
- Template Creator reference: Drive doc 1JLFl4op0rT6mj1rim0YGsU6kcct91t2ih-TKoO7u0vs; no template package created in this census/DEDUP round.

## Local custody

full_json_sha256: fa3254ec29b0b8dc64203857eedd26e4abd640e017f2b95bb174cd3f16bd801e
markdown_sha256: 3b32d63b4eb83109cf3847a762fe70c7a42ceda5d5a946a4211faeed6dd5eead

## F_NEXT

1. Persist provider-bound Drive receipt under 03_CICLOS_E_RECEIPTS when a valid file-reference bridge is available.
2. Optionally append SUPERSEDED_BY for the MASTER_INDEX snapshot without deletion.
3. Populate strategy/tactics folders only from promoted durable material, never by copying transient project state.

VISÃO ≠ ARTEFATO ≠ EXECUÇÃO ≠ EVIDÊNCIA ≠ CLAIM
