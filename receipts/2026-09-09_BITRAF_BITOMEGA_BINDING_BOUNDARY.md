# Receipt — BitRAF ↔ BitOmega binding boundary — 2026-09-09

State: `SOURCE_CONFLICT_REFINED / BINDING_TOKEN_VAZIO`  
Route: `ATLAS-X-ZIPRAF-FREESTANDING-GEO-COMPILER-20260909`  
Claim gate: `claim_allowed=false`

## Observation

The previously broad `BitRAF <-> BitOmega exact state binding` gap was re-searched against current producer/public source families.

### BitOmega authority observed

Vectras `engine/rmr/include/bitomega.h` defines ten **named semantic states**:

`NEG, ZERO, POS, MIX, VOID, EDGE, FLOW, LOCK, NOISE, META`.

It also defines explicit direction semantics and invariants.

### BitRAF authorities observed

Vectras `engine/rmr/include/bitraf.h` exposes codec/hash/reconstruction APIs and diagnostics, but no ten-state semantic enum.

A publicacientiespiritual source `bitrafmd.md` describes a numerical `RafBit r in {0..9}` tensor-base, but does not assign those ten ordinals to the ten BitOmega semantic names.

A separate technical source `bitraf_especificacao.md` models each Bitraf cell as `(canal, forma, paridade, spin, peso)` and, at the 468 marker, states `N_estados_por_forma=8`. This is not equivalent to the numerical ten-state tensor declaration and must not be silently normalized.

## Result

Cardinality similarity is insufficient for semantic identity:

`10 numeric slots != 10 named BitOmega states`.

The source family itself also contains a `10-state` versus `8-states-per-form` distinction that may represent different layers/models, not necessarily an error. Therefore a forced 1:1 table would be invented evidence.

The gap is refined as:

`GF006_BITRAF_BITOMEGA_EXACT_STATE_BINDING = TOKEN_VAZIO_SEMANTIC_AUTHORITY`.

## Closure gate

GF006 closes only when a source authority explicitly supplies:

1. the BitRAF state namespace/version being bound;
2. a mapping from each BitRAF state to BitOmega state or an explicit non-bijective relation;
3. transformation/invariant rules;
4. positive and negative KAT vectors;
5. a receipt tied to exact source commits.

Until then, GeoWord64 routes the two families as separate module identities.
