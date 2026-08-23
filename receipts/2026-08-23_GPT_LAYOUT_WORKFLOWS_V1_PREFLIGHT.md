# Receipt GPT Layout Workflows V1 Preflight

**Receipt ID:** `EVD:RECEIPT:GPT_LAYOUT_WORKFLOWS_V1:PREFLIGHT:20260823`

**Repository:** `rafaelmeloreisnovo/Mapa`

**Base:** `main@19d93251341d78d7def96b355ff360995d7a544f`

**Branch:** `rafaelia/gpt-layout-workflows-v1-20260823`

**State:** `IMPLEMENTED_PROPOSED`

**Claim ceiling:** `REFERENCE` before remote CI evidence.

## Objective

Materialize the ChatGPT operating layout as a federated routing contract.
Keep mutable state outside custom instructions and preserve authority boundaries.

## Drive source

`SRC:DRIVE:1tKGN2zBCaIuqTPJbIBEgjD6WjNO28YYyVn6ZDDfGYsA`

Title:
`RAFAELIA — GPT Layout, Instruções Personalizadas e Workflows — V1 — 2026-08-23`.

## GitHub delta before this receipt

Observed compare against `main`:

```text
status        = ahead
ahead_by      = 5
behind_by     = 0
files_changed = 5
```

Commits:

- `1c490b40cc9f98a0172dc5513ae861f5ddd64d11` machine contract.
- `e3ac1ad0d8c486334a8d2a00f8c72cf9ae203daf` fail-closed validator.
- `60cefde782a50d0399225b03a832251861fdaf49` dedicated CI gate.
- `cc7bf7e3045f17fc0743d3124bda37f52d2754a9` human contract.
- `cf188f61702d526dfa922192a34bcf5ec7324be9` navigation leaf.

Files:

- `.github/workflows/gpt-layout-contract.yml`.
- `docs/GPT_LAYOUT_WORKFLOWS_V1.md`.
- `governance/GPT_LAYOUT_WORKFLOW_V1.json`.
- `navigation/GPT_LAYOUT_WORKFLOWS_V1.md`.
- `tools/validate_gpt_layout_workflow.py`.

## Invariants

```text
SESSION != LONGITUDINAL_MEMORY != EVIDENCE
MASCOTE != AGENTE != AUTORIDADE != EXECUTOR
VISAO != ARTEFATO != EXECUCAO != EVIDENCIA != CLAIM
TOKEN_VAZIO != PASS
```

The new artifacts do not create a competing master registry.
Drive remains longitudinal/editorial authority.
Mapa remains federated navigation and state authority.
Producer repositories remain implementation authorities.

## Evidence boundary

The repository can test structural routing invariants.
It cannot prove hidden model behavior or all future ChatGPT runtime behavior.

Remote CI is not claimed by this preflight receipt.

## R3

**F_ok:** human and machine GPT layout contracts are materialized and navigable.

**F_gap:** remote CI and pull-request gate evidence are pending.

**F_next:** open a pull request, observe the dedicated GPT Layout Contract gate,
and record remote evidence without promoting runtime claims.
