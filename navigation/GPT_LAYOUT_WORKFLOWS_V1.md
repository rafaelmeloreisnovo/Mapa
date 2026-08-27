# GPT Layout Workflows V1 Navigation

**State:** `IMPLEMENTED_PROPOSED`

**Authority:** subordinate navigation leaf under `Mapa`.

## Objective route

```text
objective
-> bootstrap
-> authority
-> navigation
-> activation
-> execution/evidence
-> retrofeedback
```

## Human contract

`ART:Mapa:docs/GPT_LAYOUT_WORKFLOWS_V1.md`

## Machine contract

`ART:Mapa:governance/GPT_LAYOUT_WORKFLOW_V1.json`

## Validator

`ART:Mapa:tools/validate_gpt_layout_workflow.py`

## CI gate

`ART:Mapa:.github/workflows/gpt-layout-contract.yml`

## Model semantic boundary

- Contract: `ART:Mapa:contracts/model-semantic-rapport.v1.json`
- Navigation leaf: `ART:Mapa:navigation/MODEL_SEMANTIC_RAPPORT_V1.md`
- Invariant: contextual conditioning is not evidence of parameter training.
- Closed provider: hidden tokenizer, embeddings, weights, activations and decoder remain `TOKEN_VAZIO` until producer evidence exists.

## Drive mirror

`SRC:DRIVE:1tKGN2zBCaIuqTPJbIBEgjD6WjNO28YYyVn6ZDDfGYsA`

## Upstream authorities

- Bootstrap: `ART:Mapa:bootstrap/RAFAELIA_CHATGPT_BOOTSTRAP_V1.md`.
- Authority matrix: `ART:Mapa:governance/AUTHORITY_MATRIX_V1.yaml`.
- Activation registry: `ART:Mapa:governance/ACTIVATION_REGISTRY_V1.json`.
- Universal navigation root: `ART:Mapa:navigation/INDEX.md`.

## Invariants

```text
SESSION != LONGITUDINAL_MEMORY != EVIDENCE
MASCOTE != AGENTE != AUTORIDADE != EXECUTOR
VISAO != ARTEFATO != EXECUCAO != EVIDENCIA != CLAIM
TOKEN_VAZIO != PASS
```

This leaf does not create a competing master registry.
It only makes the GPT layout contract addressable from `navigation/`.

## R3

**F_ok:** GPT layout now has a stable navigation leaf.

**F_gap:** CI evidence is pending until the pull request runs.

**F_next:** open the pull request and observe the dedicated contract gate.
