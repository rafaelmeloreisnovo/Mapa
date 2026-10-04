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
   - executes the validator on relevant push/PR changes;
   - GitHub Actions dependencies are pinned to repository-approved full commit SHAs;
   - checkout uses `persist-credentials: false`.

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

## Supply-chain gate observation

The first dedicated workflow attempt, run `37226538155`, failed **before** the matrix validator executed because the repository supply-chain policy rejected floating action tags:

- `actions/checkout@v4`;
- `actions/setup-python@v5`.

The policy required full 40-character action commit SHAs. This was treated as a valid fail-closed supply-chain result, not as matrix-validation evidence.

The workflow was corrected without relaxing the policy:

- `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1`;
- `actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97`;
- `persist-credentials: false`;
- Python `3.12`.

Corrected exact PR head:

`0dd2bb2a53693f284860cc97982481f7ae925bb1`

## Executed matrix gate

- pull request: `#729`;
- exact tested head: `0dd2bb2a53693f284860cc97982481f7ae925bb1`;
- dedicated workflow: `repository-exposure-matrix`;
- workflow run: `37226577690`;
- job: `validate`;
- `Set up job`: `SUCCESS`;
- pinned `actions/checkout`: `SUCCESS`;
- pinned `actions/setup-python`: `SUCCESS`;
- step `Validate repository exposure matrix`: `SUCCESS`;
- job conclusion: `SUCCESS`;
- workflow conclusion: `SUCCESS`.

The exact validated PR head was observed as `mergeable=true` before promotion. The PR changed only these five paths:

- `.github/workflows/repository-exposure-matrix.yml`;
- `auditoria/receipts/2026-10-04_REPOSITORY_EXPOSURE_FREESTANDING_V1.md`;
- `data/control-plane/repository_exposure_freestanding.v1.json`;
- `docs/governance/REPOSITORY_EXPOSURE_FREESTANDING_V1.md`;
- `scripts/validate_repository_exposure_matrix.py`.

Promotion:

- method: squash merge;
- merge commit: `89af3739b4775cdb35938c0e66ed1005dc39e287`.

## Claim result

`CLAIM_STATE = EXPOSURE_MATRIX_GATE_PASS`

This PASS establishes only that the V1 repository inventory/exposure matrix is structurally coherent under its documented validator at the exact tested head and that the gated control-plane artifacts were promoted.

It does **not** establish, repo by repo:

- authorship;
- `FREESTANDING_PASS`;
- absence of runtime dependencies;
- full-history secret cleanliness;
- release/non-default-branch cleanliness;
- publication readiness;
- scientific validity;
- production readiness.

Those states remain `TOKEN_VAZIO`, `PENDING`, or their existing producer-specific state until separately evidenced.

Other pre-existing workflows on the same PR head may have independent failures outside this dedicated matrix gate. They are not silently promoted to PASS by this receipt and must retain their own authority/evidence chain.

## Mutation boundary

This V1 does not change GitHub repository visibility.

Any future `public -> private` or `private -> public` mutation requires an explicit action against the reviewed matrix state. Private control/memory/custody repositories should prefer a separate sanitized public export rather than exposing the original repository.

## R3

`R3=<F_ok: 90-repository 30/60 decision matrix + human policy + machine JSON + stdlib validator + SHA-pinned remote gate promoted; F_gap: per-repo authorship/freestanding/full-history-secret evidence remains TOKEN_VAZIO where not audited; F_next: execute P0 close/sanitize for TRABALHO... and split/gate an authorial public core from RafNet-Core before broader visibility changes>`
