---
name: execution-evidence
description: Separate code/artifact/build/runtime/physical execution and prevent fixture or narrative from becoming runtime proof.
version: 1.0.0
status: DRAFT_FAIL_CLOSED
---

# D3 — Execution Evidence

## Execution ladder

`SPECIFIED → IMPLEMENTED → BUILT → TEST_EXECUTED → RUNTIME_OBSERVED → PHYSICAL_OBSERVED → REPRODUCED`.

No level implies the next.

## Required evidence

- implementation: exact source/ref/path;
- build: toolchain, flags, environment, exit code, artifact digest;
- test: fixture identity, command/gate, expected/observed result;
- runtime: environment/device/VM identity, logs/metrics, timestamp;
- physical: physical-device evidence and scope;
- reproduction: independent or explicitly same-environment rerun.

## Fail-closed rules

`fixture != live`, `workflow != execution`, `sandbox_pass != production_pass`, `artifact_exists != runtime_pass`.

Missing execution evidence produces a typed `TOKEN_VAZIO_EXECUTION_*`, never a narrative PASS.

## Output

`execution_level`, `environment`, `artifact_digest`, `gate`, `exit_code`, `logs_or_receipt`, `scope`, `reproducibility`, `F_ok/F_gap/F_next`.
