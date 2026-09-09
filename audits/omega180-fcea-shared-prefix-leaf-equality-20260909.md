# Ω180 — FCEA shared-prefix leaf equality

Date: 2026-09-09
Predecessor: Ω179 / PR #586
Claim gate: `claim_allowed=false`

## Verified delta

Provider-distinct Drive occurrences A/B/C were traversed at shared loose-object prefixes `d3`, `d1`, and `d0`.

- `d3`: one leaf in each A/B/C: `de278f1460c256b39f2e8000d64f174317dfdf`, 51 B → full object id `d3de278f1460c256b39f2e8000d64f174317dfdf`.
- `d1`: one leaf in each A/B/C: `62741da3bb510acbb374f289ebd8d876e47156`, 204 B → full object id `d162741da3bb510acbb374f289ebd8d876e47156`.
- `d0`: one leaf in each A/B/C: `9f4c9d66b39c40053d4a0ab33cce3defc29f15`, 43 B → full object id `d09f4c9d66b39c40053d4a0ab33cce3defc29f15`.

Thus, only for these three prefixes:

`LEAF_SET(A)=LEAF_SET(B)=LEAF_SET(C)`.

Raw bytes for the A/d3 object were fetched from Drive, zlib-decoded, and canonical Git SHA-1 recomputed as `d3de278f1460c256b39f2e8000d64f174317dfdf`; this witness is `REPRODUCED`.

## Boundary

This does **not** establish full loose-object-set subset/superset/equivalence. G031 remains `TOKEN_VAZIO` globally until all remaining shared-prefix leaves are enumerated and reachability is computed.

Next deterministic cursor: `ca → c1 → c0 → remaining shared prefixes → SHA40 sets → intersections/differences → reachability`.

Provider reconciliation: PR #586 was observed merged externally at `2026-09-09T09:27:51Z`, merge commit `ee527db68df27724ccd49a2e54f98e89029f311b`. Ω180 did not merge, approve, or release it.
