# Shared Data Governance — Authorial Entry Point

Start here for governed sharing between Drive and repository workflows.

- Current human/governance authority: `docs/governance/SHARED_DATA_GOVERNANCE_V2.md`
- Historical V1 pointer: `docs/governance/SHARED_DATA_GOVERNANCE_V1.md`
- Machine policy: `data/governance/shared_data/criticality_policy.v1.json`
- Release schema: `schemas/shared_data/share_release_manifest.v1.schema.json`
- Validator: `tools/validate_shared_data_release.py`
- Synthetic positive/negative fixtures: `examples/shared_data/`
- Adversarial tests: `tests/test_shared_data_release.py`
- CI gate: `.github/workflows/shared-data-release-gate.yml`

Operational identity is authorial. External study is not operational authority, product identity, certification or release authority.

Operational boundary: `DRIVE_BRIDGE_ENABLED=false`.

Do not add Drive credentials, raw C3/C4 data, personal source material, tokens, secrets or OAuth/PAT values to this repository or to CI artifacts/logs.

Core invariants:

- `fragmentation != anonymization`
- `small_fragment != small_impact`
- `hash != authorization`
- `unknown_effect != zero_risk`
- `CI_pass != human_authorization`
- `research != operational_authority`
