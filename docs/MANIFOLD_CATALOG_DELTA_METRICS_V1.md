# Manifold Catalog Delta Metrics V1

State: `IMPLEMENTED_ON_DRAFT_BRANCH / CI_PENDING`

This contract measures only the route resolver's own search reduction. It does not measure computational-complexity classes and does not turn residual text into evidence.

For a fixed registry with `|R|` routes:

```text
ΔNP_catalog = |R| - |C_after|
ΔP_catalog  = 1 if a unique deterministic route is resolved, else 0
Δ§RUIDO     = count(normalized query tokens not covered by matched route triggers)
```

Units:

- `ΔNP_catalog`: `route_candidates_removed`
- `ΔP_catalog`: `deterministic_resolution_flag`
- `Δ§RUIDO`: `normalized_query_tokens`

Interpretation:

- a resolved route may have non-zero lexical residual noise;
- an ambiguous query keeps `ΔP_catalog=0`;
- an unknown query conservatively keeps the full route universe as unresolved, so `ΔNP_catalog=0`;
- `Δ§RUIDO` is lexical routing residue only, not semantic, physical, statistical or scientific noise;
- every delta output carries `complexity_claim=false` and `evidence_claim=false`.

Therefore:

```text
measured catalog delta != proof
measured lexical noise != semantic meaning
NP_CATALOG -> P_CATALOG != P = NP
```

Gap-node delta fields remain `null` until a domain-specific baseline, unit and procedure exist. This route-level metric does not backfill them.

R3:

`F_ok`: route-level candidate reduction and lexical residual are measurable with explicit units.

`F_gap`: semantic-noise, runtime-noise and scientific residual metrics remain TOKEN_VAZIO.

`F_next`: only bind another noise metric after declaring its layer, unit, baseline and falsifier.

`claim_allowed=false`
