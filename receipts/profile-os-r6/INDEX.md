# PROFILE OS R6 — Provider-bound Evidence Index

R6 is the post-merge custody layer for the immutable PROFILE_OS source snapshot validated by GitHub Actions run `34016118690`.

`claim_allowed=false`

## 1. Immutable source snapshot

- R5 PR: `#524`
- R5 source head: `a8ae8964b19356eaaefba79b2626ec69aa483f2e`
- R5 merge commit: `dc6e674ad0ce35e6c2be7fd17ad25daa87479e17`
- Workflow: `PROFILE OS Registry Gate`
- Run: `#8` / `34016118690`
- Artifact: `profile-os-evidence-34016118690`
- Artifact ID: `9983936395`
- Artifact bytes: `730020`
- Provider artifact digest SHA-256: `6e7aa02798e8ae11c5b154fb77c2aebaa98c98a46193b917ce859ead0200a0c7`

## 2. What the artifact contains

`ARTIFACT_FILE_TREE.txt` enumerates all 29 files uploaded by the workflow. The artifact itself contains, without post-run rewriting:

- `TREE.txt` — all 2,584 Git-tracked paths in the validated source head;
- `TREE.json` — the same inventory with per-file bytes + SHA-256;
- `REPOSITORY_TRACKED_SHA256SUMS.txt` — SHA-256 for every tracked file;
- `COMPOSITION_SHA256SUMS.txt` — SHA-256 for the 18-file PROFILE_OS composition;
- `source/` — byte-for-byte copies of all 18 composition files, including hidden `.github/workflows/profile-os-registry.yml`;
- `PROFILE_OS_EVIDENCE.zip` + `.sha256` — deterministic inner evidence ZIP and its digest;
- `gate-result.json`, `STAGE_CHAIN.jsonl`, `token-resolution.jsonl`, `validator.log`, `tests.log`.

## 3. Whole-file identities read back outside the runner

- `TREE.txt`: `904d652f1b76ee6c94ce4e9cbe609737c67e71ac2dbc411ac698482a2e024268`
- `REPOSITORY_TRACKED_SHA256SUMS.txt`: `e4c55973013c930986f2fa5e1c1b7805ef416b90845e505ceee722c95a7de732`
- `COMPOSITION_SHA256SUMS.txt`: `2c6f2336bda5ac3b885c1ab2a72e64038c1362c6caf262c6af408de7f3d773dc`
- `ARTIFACT_FILE_TREE.txt`: `4d9226aedbd112257172b2e380a9039b44fac6b3ad270e2e99da4733a18f4868`
- Inner `PROFILE_OS_EVIDENCE.zip`: `7df164fd3329fcf63acacb5d8e1a0c803b40cbcbfcea59cfd7ef3cc39fa9980a`

## 4. Why the 2,584-path manifest is not re-committed as a new source file

The manifest describes the exact source head `a8ae8964...`. Committing that manifest back into the source tree would create a new tree with extra files and would no longer be the state described by the manifest. R6 therefore keeps an append-only provider-bound pointer and hashes to the immutable Actions artifact instead of creating a self-referential false equivalence.

The raw manifests are preserved in the Actions artifact and in the final local evidence capsule. Local reconstruction fragments are byte-identical to the raw files and are verified by the whole-file hashes above.

## 5. R6 repository-side records

- `PROFILE_OS_REMOTE_CI_R6_PROVIDER_BOUND_RECEIPT.md`
- `TOKEN_RESOLUTION_POST_RUN.jsonl`
- `COMPOSITION_SHA256SUMS.txt`
- `ARTIFACT_FILE_TREE.txt`
- `PROVIDER_BOUND_SNAPSHOT.v1.json`

These records index the immutable artifact; they do not replace it.

## 6. Boundary

`VISÃO ≠ CÓDIGO ≠ ARTEFATO ≠ EXECUÇÃO ≠ EVIDÊNCIA ≠ CLAIM`

The PROFILE_OS CI/ZIP evidence is provider-bound PASS. Repository-wide provider protection, server-side enforcement, CodeScan credential availability, and independent promotion approval remain separate governance gates.
