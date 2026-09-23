# RAFAELIA Manifold Machine-Readable V1

State: `IMPLEMENTED_UNTESTED_REMOTE / VALIDATED_BY_THREE_ROUTE_FIXTURES / claim_allowed=false`

This branch freezes the **registry structure**, not any scientific or runtime claim.

## Provenance
- Drive START HERE LITE: `1l2hhCHYFBouU4qNU-WFY3kqI1wEzfJ64EDvi2iH1mbI`
- Drive EDGES_OMEGA_V1: `17u2uFDRFPn4h75WtQdR9kRXU1BbS1KRNWhCFuw7HBCo`
- Drive ROUTES_OMEGA_V1: `1fPelyCM24WCmfZDs1wjz7MWRW2q6ww44hcPuTEu5k2g`
- Drive route fixtures: `1qE0TD_yWa7Qfpy_ZOxM9oBLkDtQs3IFn0R6KKfFl-fA`
- Drive invariant hotset: `1G20pRX_hojvzoYTUoBixKVArBpyNYwcjtkcBaPQFFwo`

## Files
- `schemas/manifold-edge-v1.schema.json`
- `schemas/manifold-route-v1.schema.json`
- `data/manifold/edges_omega_v1.jsonl`
- `data/manifold/routes_omega_v1.jsonl`
- `tools/validate_manifold_registry.py`
- `tests/test_manifold_registry.py`

## Gates
`SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`
`TOKEN_VAZIO != 0`
`IMPLEMENTED_UNTESTED != PASS`
`ROUTE_VALIDATED != CLAIM_VALIDATED`

The three fixtures exercise geometry/WORLD69, RLL/science and RAFCODEPHI/runtime. Route validation passed while unresolved scientific/device states remained explicitly blocked.

## Reproduction
```bash
python tools/validate_manifold_registry.py data/manifold/edges_omega_v1.jsonl data/manifold/routes_omega_v1.jsonl
python -m unittest tests.test_manifold_registry
```

Expected registry counts: 15 edges, 10 routes.

Rollback: drop this branch/PR; Drive source registries remain unchanged.
