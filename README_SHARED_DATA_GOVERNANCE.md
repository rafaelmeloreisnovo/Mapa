# Shared Data Governance — Entry Point

Start here for governed sharing between Drive and repository workflows.

- Human/governance contract: `docs/governance/SHARED_DATA_GOVERNANCE_V1.md`
- Machine policy: `data/governance/shared_data/criticality_policy.v1.json`
- Release schema: `schemas/shared_data/share_release_manifest.v1.schema.json`
- Validator: `tools/validate_shared_data_release.py`
- Synthetic positive/negative fixtures: `examples/shared_data/`
- Adversarial tests: `tests/test_shared_data_release.py`
- CI gate: `.github/workflows/shared-data-release-gate.yml`
- Bootstrap receipt: `data/receipts/SHARED_DATA_GOVERNANCE_BOOTSTRAP_20260821.v1.json`

Operational boundary: `DRIVE_BRIDGE_ENABLED=false`.

Do not add Drive credentials, raw C3/C4 data, personal source material, tokens, secrets or OAuth/PAT values to this repository or to CI artifacts/logs.

`fragmentation != anonymization` and `unknown_effect != zero_risk`.
