# RAFAELIA Claim ↔ Evidence Matrix V1

State: `CONTRACT_DEFINED_LOCAL / POPULATION_OPEN / claim_allowed=false`

Every promotable claim must resolve the chain:

`CLAIM → SOURCE → ARTIFACT → EXECUTION → EVIDENCE → REVIEW → SCOPE`

## Required fields

- `claim_id`
- exact claim text
- source refs
- artifact refs
- execution refs
- evidence refs
- review state
- promotion state
- allowed scope

## Rules

1. A source reference alone never fills execution or evidence.
2. A historical receipt is not silently rewritten as current execution.
3. Missing execution/evidence keeps promotion `BLOCKED`.
4. Independent review requires an authority outside the same author/assistant/CI trust boundary.
5. Rejected or falsified claims remain addressable and route to the Negative Claim Registry.
6. Promotion is scoped. No row can silently imply global `claim_allowed=true`.
7. A claim can be `ALLOWED_SCOPED` for a software property while remaining blocked for a physical or scientific interpretation.

## Example separation

`ELF has no dynamic section` may be evidence-backed without implying `physical ARM runtime occurred`.

`custom shrink score = 0.94235199` may be arithmetically reproduced without implying `R²=0.942` or `94.2% confidence`.

`SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`
