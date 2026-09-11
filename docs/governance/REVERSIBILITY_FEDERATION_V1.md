# RAFAELIA Reversibility Federation V1

Status: `FRAMEWORK_PRESENT / CLAIM_ALLOWED=false`

Invariant: **VISÃO ≠ ARTEFATO ≠ EXECUÇÃO ≠ EVIDÊNCIA ≠ CLAIM**.

## Purpose

This document binds the existing federation, receipt and authority-control structures to the append-only reversibility catalog. It is additive: historical receipts and reports are not rewritten. Missing reversibility metadata on legacy artifacts is migration debt and must be represented as `TOKEN_VAZIO`, not as PASS or FAIL by assumption.

## Existing federation surfaces observed

- `.github/workflows/federated-receipt-broker.yml` already validates repository-local receipts and explicitly keeps remote transport, production HMAC verification and external federation bounded/unfinished.
- `.github/workflows/federated-registry.yml` validates the authority registry and related governance documents.
- `indices/repository_authority_registry.json` defines repository roles and already states `claim_allowed=false` plus lineage invariants.
- `auditoria/FASE_5_FEDERATION_TRACE_20260822.md` records earlier lineage/topology validation while still preserving device/runtime gaps and `claim_allowed=false`.

## Reversibility binding

Every new reversible federated operation SHOULD emit or reference: stable `event_id`; producer repository and exact ref/SHA; `before_ref`; `after_ref`; `rollback_ref`; `evidence_ref`; predecessor event when applicable; `reversibility_state`; `risk_class`; and `claim_allowed=false` until an independent promotion gate exists.

The global Mapa registry is pointer-only. Authority stays in the producer repository. Mapa must not copy a producer's local state and then treat that copy as producer authority.

## Compatibility with legacy receipts

Legacy receipt without a `reversibility` block means:

`LEGACY_RECEIPT_PRESENT + REVERSIBILITY_METADATA=TOKEN_VAZIO`

not `LEGACY_RECEIPT_IRREVERSIBLE` and not `REVERSIBILITY_VERIFIED`.

Migration is monotonic: add a successor receipt/event or external pointer; never rewrite the historical receipt just to satisfy the new schema.

## Current operational boundaries

The repository-local broker states that remote receipt transport is not implemented, production HMAC verification is not implemented, and external federation remains `TOKEN_VAZIO`. Documentation or examples describing those surfaces as deployed production services are design/onboarding intent until provider-bound execution evidence exists.

`BROKER_DOCUMENTATION ≠ DEPLOYED_BROKER`

`HMAC_SCHEMA ≠ HMAC_VERIFICATION_EXECUTED`

`RECEIPT_PRESENT ≠ REMOTE_FEDERATION_PROVEN`

## Human/EIA navigation

Canonical local entry points:

- `auditoria/reversibility/README.md`
- `auditoria/reversibility/index.jsonl`
- `auditoria/reversibility/schema.v1.json`
- `auditoria/reversibility/federation/registry.v1.json`
- `auditoria/reversibility/federation/receipt-extension.v1.json`
- `tools/validate_reversibility_catalog.py`
- `.github/workflows/reversibility-catalog-gate.yml`

EIAs should traverse by stable ID and pointer. Humans may use summaries/maps, but derived maps are rebuildable views and are not source authority.

## Non-regression rule

A migration is accepted only when it preserves predecessor lineage, does not erase contradictory/negative history, does not promote `TOKEN_VAZIO`, and provides a rollback pointer for any mutation that can be reverted.

## Branch divergence recovery

PR #519 merged only its recorded two-commit head. Later work on `rafaelia/session-nibigiri-safe-20260905` continued independently and diverged from `main`. That history is preserved. The recovery branch `rafaelia/reversibility-federation-20260906` starts from the then-current `main` and reapplies only the still-unmerged reversibility state. No force-reset of the historical branch is required.

## Next verifiable step

Run the dedicated `Reversibility Catalog Gate` on the exact PR head and retain its checksum artifact. Only after that run exists may the new validator move from `ARTEFATO_PRESENT` to `EXECUTED_WITH_RECEIPT`.
