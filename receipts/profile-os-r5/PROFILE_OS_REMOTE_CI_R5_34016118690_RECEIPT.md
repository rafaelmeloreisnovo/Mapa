# PROFILE OS — Remote CI R5 — Provider-bound receipt

- PR: `#524`
- Source head: `a8ae8964b19356eaaefba79b2626ec69aa483f2e`
- Workflow: `PROFILE OS Registry Gate`
- Run: `#8` / `34016118690`
- Result: **PASS**
- `checked_out_sha == expected_sha == source_head`: **true**
- Validator: **PASS**
- Tests: **17/17 PASS**
- Git tracked tree: **2,584 files enumerated + SHA-256**
- PROFILE_OS composition: **18/18 present + byte-wise hash match**
- Inner ZIP: **PASS**, SHA-256 `7df164fd3329fcf63acacb5d8e1a0c803b40cbcbfcea59cfd7ef3cc39fa9980a`
- Actions artifact: ID `9983936395`, 730020 bytes
- Provider/download digest: `6e7aa02798e8ae11c5b154fb77c2aebaa98c98a46193b917ce859ead0200a0c7`
- Hidden `.github/workflows/profile-os-registry.yml` preserved in outer artifact: **yes**
- Artifact custody: `TOKEN_VAZIO_POST_RUN -> F_OK_PROVIDER_BOUND`
- `claim_allowed=false`

## Parallel gates

These are not PROFILE_OS YAML/ZIP defects:

1. CodeScan: provider credential absent; analysis/SARIF not run.
2. Server Merge Enforcement: live server-side main enforcement check failed after fixtures passed.
3. Provider Protection: live default-branch ruleset verification failed.
4. Promotion Control: fail-closed denial because PR is draft/unknown and independent approval is missing; manual merge only.

No merge, delete, release or claim promotion performed.
