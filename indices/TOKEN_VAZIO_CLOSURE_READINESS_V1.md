# TOKEN_VAZIO Closure Readiness Gate V1

## Intent

Turn a documented gap into a falsifiable closure contract **without filling the missing value by inference**.

This gate is a precondition layer. It does not execute provider mutations, close gaps, approve claims, or convert CI success into scientific validation.

## Boundary

```text
SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM
TOKEN_VAZIO != 0
CONTRACT_READY != EXECUTED
EXECUTED != CLOSED
CI_PASS != SCIENTIFIC_VALIDATION
REPRODUCIBLE_SAME_DATA != REPLICATED_NEW_DATA
```

Scientific-method anchor: NASEM, *Reproducibility and Replicability in Science* (2019), DOI 10.17226/25303. The project uses the distinction operationally: same-data/code recomputation is computational reproducibility; a new-data study addressing the same scientific question is replication. Uncertainty remains explicit in either case.

## Why this gate is next

The source gap registry already contains provenance, falsifiers, next gates, urgency and non-compensatory P0 blockers. Reclassifying TOKEN_VAZIO again would add structure without reducing the main uncertainty.

The new gate instead asks, per gap:

1. What exact source binds the gap?
2. Who has authority?
3. What is the execution target?
4. Is the execution path actually available?
5. What evidence would count?
6. What observation would falsify the current state or hypothesis?
7. What is the decision rule?
8. Which uncertainty remains after the test?
9. What reproducibility/replication rule applies?
10. Is the evidence independent enough for the intended claim?
11. How is rollback/supersession handled?
12. Are external dependencies or version bumps truly necessary?

Any unknown required answer remains `TOKEN_VAZIO`; the validator never invents it.

## Priority rule

No weighted scalar is claimed. Priority is lexicographic and non-compensatory:

```text
P0 > P1 > P2 > P3
then authority/safety blocker
then GLOBAL > CROSS_REPO > REPO > LOCAL
then uncertainty reduction
then information gain
then lower declared effort
```

Unknown effort/calibration remains `TOKEN_VAZIO`, so it cannot be disguised as a precise number.

## Current first candidate

`GAP-MAPA-SERVER-ENFORCEMENT`

Reason grounded in the source registry: it is P0 and its TRANSVERSE relation affects promotion semantics across Mapa producer routes. The observed main state at the bootstrap ref reports server-side protection/enforcement off.

Current readiness: `TOKEN_VAZIO_BLOCKED`.

Known blocker dimensions:

- `execution_path_state = TOKEN_VAZIO`
- `effort_class = TOKEN_VAZIO`

Therefore the next action is not to pretend the provider change has been performed. It is to resolve the authorized/reversible provider execution path, perform the mutation only when that authority exists, and then obtain exact-state independent readback.

## Freestanding / dependency policy

The gate implementation uses the Python standard library only.

Default:

```text
external_runtime_dependencies = false
version_bumps = false
```

An exception must carry necessity evidence, bounded scope, impact, rollback, and an exact source/version reference.

## Files

- `data/control-plane/omega-assurance/token-vazio-closure-readiness.v1.json`
- `tools/validate_token_vazio_closure_readiness_v1.py`
- `tests/test_token_vazio_closure_readiness_v1.py`
- `.github/workflows/serpent-dove-gap-metabolism-v1.yml`

## Local validation

```bash
python3 -m py_compile tools/validate_token_vazio_closure_readiness_v1.py
python3 -m py_compile tests/test_token_vazio_closure_readiness_v1.py
python3 -m unittest tests/test_token_vazio_closure_readiness_v1.py
python3 tools/validate_token_vazio_closure_readiness_v1.py
```

A validator `PASS` means only that the readiness mechanism is structurally valid. It does **not** mean a gap is closed.

## Promotion

Do not merge merely because CI is green. Exact-head CI, independent review, authority and any subject-specific scientific evidence remain distinct gates.
