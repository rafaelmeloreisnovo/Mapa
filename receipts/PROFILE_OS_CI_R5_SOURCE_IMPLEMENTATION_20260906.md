# RAFAELIA PROFILE OS — CI R5 source implementation — 2026-09-06

state: SOURCE_IMPLEMENTED_LOCAL_VALIDATION_PASS_REMOTE_PENDING
mode: APPEND_ONLY / NO_DELETE
claim_allowed: false

## Cause observed

PROFILE OS Registry Gate run `33991817977` failed during `Set up job` before source validation because `actions/checkout@v4` and `actions/setup-python@v5` violated repository policy requiring full-length action commit SHAs.

## R5 delta

1. Pin checkout, setup-python and upload-artifact to full 40-hex SHAs already used/ratcheted by this repository.
2. Add typed CI policy and classify TOKEN_VAZIO as `NON_BLOCKING`, `BLOCKING_RUNTIME` or `POST_RUN_BLOCKING_FOR_CLAIM`.
3. Add deterministic CI evidence builder: source inventory, validator/test capture, full tracked-tree SHA-256 inventory, byte-for-byte PROFILE_OS composition, deterministic ZIP, round-trip verification and stage hash chain.
4. Upload evidence with `if: always()` so FAIL also leaves bounded evidence when the runner reaches the artifact step.
5. Keep artifact custody as TOKEN_VAZIO until provider ID/digest/download readback exists.

## Local preflight

- validator: PASS
- folders: 8
- objects: 8
- gaps typed: 8
- supersession relations: 1
- unit tests: 14/14 PASS
- composition: 18 paths
- deterministic ZIP round-trip: PASS

`PASS(job) != claim_allowed`

`TOKEN_VAZIO != 0`
