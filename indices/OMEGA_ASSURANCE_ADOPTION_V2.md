# Ω Assurance Adoption V2 — Drive-First Pilot

Status: `DRAFT_FAIL_CLOSED`  
Policy: `claim_allowed=false`  
Baseline: `rafaelmeloreisnovo/Mapa@1da6932b7a90215dda5fd8c2e2b1d27b114e6538`

## Outcome

This wave adopts the already-materialized Ω Assurance Skills V1 without creating a second watchdog. It binds the seven assurance axes, attention/evidence aging, the Serpent–Dove conduct rule, a bounded quiet-watchdog model, producer authority, CrossFail cases and primary sources into one validated control-plane manifest.

## Drive-first receipt

The canonical traceability Matrix received five append-only tabs before this branch was materialized:

- `OMEGA7_ADOCAO`;
- `TRILHAS_PRODUTORAS`;
- `CROSSFAIL_OMEGA`;
- `FONTES_PRIMARIAS`;
- `SESSAO_OMEGA_20260824`.

The public repository records only the opaque reference `DRIVE_MATRIX_CANONICAL`; it does not embed raw private Drive content or a new Drive locator.

## Three-world route

1. **Complete model:** represent all seven axes and cross-cutting attention, decay, risk and operator-conduct contracts.
2. **Minimum reversible mutation:** add append-only Matrix tabs and a scoped Mapa branch; do not mutate producers or merge.
3. **Executable pilot:** validate structure and run adversarial negative tests that reject fabricated PASS, missing authority, P0 compensation, unbounded meta-watch and secondary-source substitution.

## Producer tracks

The manifest contains 15 routes. Mapa and Drive have session evidence. Known producer repositories remain `CONTRACT_ONLY` until their own gates run. Geometry/state, cache/distribution, network and query/compression retain `TOKEN_VAZIO_PRODUCER` because this wave did not establish their exact implementation authority.

`producer route != producer execution`

## Primary-source boundary

The registry uses official specifications, standards and original papers only. References include W3C PROV, JSON Schema, RFC 8785, SLSA, in-toto, OpenTelemetry, NIST, Arm AAPCS64, QEMU, LZ4, CRDT and linearizability papers, the Benettin Lyapunov method, and DESI DR2 Results II/IV.

`reference != local adoption != execution != certification`

## CrossFail seed

Twelve cases are intentionally born as `SPECIFIED_NOT_EXECUTED`. The dedicated validator tests the manifest's fail-closed policy; it does not pretend the producer fault injections already happened.

After this PR runs, a successful dedicated gate proves only:

- manifest and ledger structural integrity;
- exact axis/track/case/source coverage;
- preservation of `TOKEN_VAZIO` and `claim_allowed=false`;
- behavior of the validator against its owned negative fixtures.

It does not prove production watchdog operation, physical failover, producer runtime adoption, geometric claims, performance claims, cosmological truth or standards certification.

## Verification

```sh
python3 -m py_compile tools/validate_omega_assurance_adoption_v2.py
python3 -m py_compile tests/test_omega_assurance_adoption_v2.py
python3 -m unittest tests/test_omega_assurance_adoption_v2.py
python3 tools/validate_omega_assurance_adoption_v2.py
```

## F_ok / F_gap / F_next

`F_ok`: Drive Matrix delta verified; adoption manifest, append-only event ledger, validator, negative fixtures, workflow and index materialized.

`F_gap`: producer runtime adoption and CrossFail execution remain `TOKEN_VAZIO`; independent approval and server-side merge enforcement remain external governance blockers.

`F_next`: observe dedicated/general CI on the draft PR, append exact run receipts if needed, and select one producer track only after reading its `AGENTS.md` and resolving the smallest executable gate.
