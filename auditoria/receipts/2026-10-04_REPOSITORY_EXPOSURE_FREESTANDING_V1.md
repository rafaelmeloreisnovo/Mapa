# Repository Exposure + Freestanding V1 — Receipt

## Intent

Materialize a fail-closed map for deciding which repositories remain public/private and which authorial cores may later be published as freestanding/self-contained artifacts, without mutating repository visibility during the mapping step.

## Source observation

Connected GitHub owner-affiliation inventory observed on 2026-10-04:

- owner: `rafaelmeloreisnovo`;
- repositories observed: `90`;
- public: `30`;
- private: `60`.

This is an inventory/control receipt, not a proof of authorship or runtime independence.

## Parent authority

- `Mapa` is the federated control-plane authority;
- `docs/governance/AUTHORSHIP_PROVENANCE_INVARIANT_V1.md` remains the canonical authorship/provenance boundary;
- ownership of a repository does not by itself prove authorship;
- `TOKEN_VAZIO_AUTHORSHIP` remains valid where origin/delta is unresolved.

## Delta

1. `docs/governance/REPOSITORY_EXPOSURE_FREESTANDING_V1.md`
   - human policy and route;
   - separates public, authorial and freestanding states;
   - defines publication and full-history secret gates.
2. `data/control-plane/repository_exposure_freestanding.v1.json`
   - machine-readable 90-repository snapshot;
   - recommendation groups;
   - exact current public/private sets;
   - freestanding fail-closed gate.
3. `scripts/validate_repository_exposure_matrix.py`
   - stdlib-only structural validator;
   - checks unique inventory, group/visibility equality, 90/30/60 counts, authority paths and invariants;
   - pins P0 close/split lanes for this V1.
4. `.github/workflows/repository-exposure-matrix.yml`
   - executes the validator on relevant push/PR changes.

## P0 decisions materialized

- `TRABALHO_ROADMAP_AUDIT_GOV_DATA_ROTA_MAPwithCHAIN_security`
  - current: public;
  - route: `CLOSE_PENDING_SANITIZED_EXPORT`;
  - no visibility mutation performed by this receipt.

- `RafNet-Core`
  - current: private;
  - route: `SPLIT_PUBLIC_CORE_PRIVATE_CONTROL`;
  - do not open whole producer; extract a separately gated public authorial core.

## Freestanding boundary

No repository is marked `FREESTANDING_PASS` from metadata/name/intent alone.

Promotion requires at least:

- authorial-core provenance;
- runtime/link-time dependency boundary;
- no required external service for core execution;
- deterministic build/reproduction recipe;
- execution/test receipt;
- license/source attribution;
- default branch secret scan;
- Git history/releases/non-default branch secret scan.

`PUBLIC != AUTHORIAL != FREESTANDING`.

## Mutation boundary

This V1 does not change GitHub repository visibility.

Any future `public -> private` or `private -> public` mutation requires an explicit action against the reviewed matrix state. Private control/memory/custody repositories should prefer a separate sanitized public export rather than exposing the original repository.

## Pre-remote state

`CLAIM_STATE = EXPOSURE_MATRIX_IMPLEMENTED_REMOTE_PENDING`

Promotion to PASS is allowed only after the dedicated workflow validates the exact PR head.

## R3

`R3=<F_ok: 90-repository decision matrix materialized; F_gap: remote matrix gate and per-repo authorship/freestanding/history-secret evidence; F_next: run CI, promote only if PASS, then execute P0 close/split lane before broader publication work>`
