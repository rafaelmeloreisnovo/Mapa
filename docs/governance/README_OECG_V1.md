# OECG V1 execution route

> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧

## Purpose

Run the smallest deterministic governance checks for the Operational Excellence Control Plane without changing producer repositories or promoting claims.

## Local/repository commands

```bash
python3 scripts/governance/validate_operational_excellence_gate.py
python3 scripts/governance/validate_operational_excellence_gate.py \
  --receipt tests/fixtures/operational-excellence.receipt.valid.json

# Expected fail-closed negative control: non-zero exit
python3 scripts/governance/validate_operational_excellence_gate.py \
  --receipt tests/fixtures/operational-excellence.receipt.invalid-authority.json

python3 scripts/governance/check_semantic_event_v2.py \
  tests/fixtures/mu-semantic-event.v2.valid.json

python3 -m unittest discover tests/governance -p 'test_*.py' -v
```

## Interpretation

- A PASS means only that the bounded governance contract/fixture passed its exact checks.
- It does not prove legal compliance, system-wide safety, scientific truth, human consent, physical runtime, repository ruleset enforcement or independent approval.
- The invalid-authority fixture MUST fail. If it passes, fail the gate.
- A repeated canonical semantic-event hash demonstrates deterministic canonicalization of the fixture only; it is not evidence of semantic truth.

## Rollback

All V1 changes are additive on `audit/omega-operational-excellence-20260917`. Before merge, rollback is branch/commit revert. After any authorized merge, correction remains append-only through successor contract/receipt; do not rewrite historical receipts.
