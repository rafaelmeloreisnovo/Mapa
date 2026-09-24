# Manifold Gap Subgraph V1

State: `MATERIALIZED_ON_DRAFT_BRANCH / CI_PENDING`

This successor leaves the original 15-edge registry history intact and appends a typed gap subgraph.

## Materialized relations

- 11 `HAS_GAP` edges bind top-level gaps to their observed `origin_ref`.
- 1 `GAP_OF` edge binds `gap:G0011` to its observed parent `gap:G0002`.
- Total registry size becomes 27 edges: 15 predecessor/core + 12 gap-subgraph.

No `CLOSED_BY`, `BLOCKS`, or evidence-node edges are asserted in this version. Those require stable observed targets first.

## Cross-validation

The registry validator now accepts the gap registry as a third input and enforces:

- every top-level gap has exactly one origin-consistent `HAS_GAP`;
- every nested gap has exactly one parent-consistent `GAP_OF`;
- every referenced gap exists;
- a nested gap cannot be silently represented as a top-level `HAS_GAP`;
- child `origin_ref` and `parent_gap_id` must agree.

## Reproduction

```bash
python tools/validate_manifold_registry.py \
  data/manifold/edges_omega_v1.jsonl \
  data/manifold/routes_omega_v1.jsonl \
  data/manifold/gaps_omega_v1.jsonl

python -m unittest discover -s tests -p 'test_manifold*.py'
```

## Boundaries

`GAP_BOUND != GAP_CLOSED`

`NAVIGABLE != FILLED`

`SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`

`claim_allowed=false`
