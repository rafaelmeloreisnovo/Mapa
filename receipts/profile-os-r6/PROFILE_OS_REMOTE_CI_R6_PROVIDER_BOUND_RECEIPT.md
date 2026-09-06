# PROFILE OS — Remote CI R6 — Provider-bound custody receipt

## Provenance

- Repository: `rafaelmeloreisnovo/Mapa`
- R5 PR: `#524`
- R5 source head: `a8ae8964b19356eaaefba79b2626ec69aa483f2e`
- R5 merge commit: `dc6e674ad0ce35e6c2be7fd17ad25daa87479e17`
- R6 base observed on `main`: `0209437b7a8b480728daeca7542bb8a441c33ffc`
- R6 branch: `audit/profile-os-provider-bound-r6-20260906`
- Workflow: `PROFILE OS Registry Gate`
- Validated run: `#8` / `34016118690`
- Actions artifact ID: `9983936395`

## Provider-bound readback

- Workflow result: **PASS**
- `checked_out_sha == expected_sha == R5 source head`: **true**
- Validator: **PASS**
- Tests: **17/17 PASS**
- Git tracked inventory: **2,584 files enumerated and SHA-256 hashed**
- PROFILE_OS composition: **18/18 files present with byte-wise SHA-256 equality**
- Hidden workflow path preserved in uploaded artifact: **yes**
- Inner deterministic ZIP: **PASS**
- Inner ZIP SHA-256: `7df164fd3329fcf63acacb5d8e1a0c803b40cbcbfcea59cfd7ef3cc39fa9980a`
- Provider artifact digest SHA-256: `6e7aa02798e8ae11c5b154fb77c2aebaa98c98a46193b917ce859ead0200a0c7`
- Artifact size: `730020` bytes

## TOKEN_VAZIO closure

`TV-PROFILE-OS-CI-ARTIFACT-CUSTODY` transitions from `TOKEN_VAZIO_POST_RUN` to `F_OK_PROVIDER_BOUND` because the artifact was enumerated through the provider, downloaded, opened, its hidden workflow path observed, its source composition compared, and its ZIP/hash manifests independently re-read.

This closes artifact custody only. It does **not** promote any scientific, operational, deployment, governance, or merge claim.

`claim_allowed=false`

## Parallel gates / explicit F_GAP

1. `CodeScan`: provider credential absent; analysis and SARIF did not run.
2. `Server Merge Enforcement Assurance`: fixtures passed; live main server-side enforcement check failed.
3. `Provider Protection Gate`: live default-branch ruleset verification failed.
4. `RAFAELIA Promotion Control V1`: negative tests and invariant checks passed, but promotion was denied because independent approval was missing; manual merge only.
5. Live `main` observation after R5 merge showed branch protection disabled at that observation point. This is a repository-governance gap, not a PROFILE_OS ZIP/YAML defect.

## Scope boundary

R6 is append-only post-merge custody/materialization. No delete, release, force-push, automatic promotion, or claim elevation is performed by this receipt.
