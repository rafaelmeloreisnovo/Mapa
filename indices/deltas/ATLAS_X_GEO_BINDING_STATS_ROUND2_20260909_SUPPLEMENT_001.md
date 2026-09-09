# SUPPLEMENT 001 — GF006 Semantic-Authority Input Gate

Parent object: `ATLAS-X-GEO-BINDING-STATS-R2-20260909`  
Date: `2026-09-09`  
Mode: `APPEND_ONLY / NO_PREDECESSOR_REWRITE / claim_allowed=false`

## New bounded closure

The unresolved semantic mapping now has a versioned external-input contract without inventing mapping values.

Materialized:

- `schemas/rafaelia_geo_binding_authority_v1.schema.json`;
- `tools/validate_geo_binding_authority.py`;
- `data/fixtures/geo_binding_authority_token_vazio_v1.json`;
- `data/evidence/geo-binding-authority-input-gate-20260909.v1.json`.

Canonical BitOmega codes are bound to the Vectras `zero.h` source:

```text
0 NEG
1 ZERO
2 POS
3 MIX
4 VOID
5 EDGE
6 FLOW
7 LOCK
8 NOISE
9 META
```

No equivalent RafBit semantic labels are inferred.

## Fail-closed behavior

A typed unresolved authority input is valid:

```text
status=TOKEN_VAZIO
mapping=[]
exact=false
runtime_binding_allowed=false
=> PASS / VALID_TOKEN_VAZIO_NO_RUNTIME_BINDING
```

A false promotion attempt is rejected:

```text
status=EVIDENCED
mapping=[]
exact=true
=> FAIL / EVIDENCED authority requires exact 10x10 bijection
```

The latter control exited nonzero (`rc=1`) in the local bounded replay.

Therefore:

```text
GF006_BINDING_MECHANISM      = CLOSED_IMPLEMENTED_TESTED_LOCAL
GF006_AUTHORITY_INPUT_SCHEMA = CLOSED_IMPLEMENTED_TESTED
GF006_SEMANTIC_AUTHORITY     = TOKEN_VAZIO_SEMANTIC_AUTHORITY
```

## Runtime promotion contract

`runtime_binding_allowed=true` requires all of:

1. `status=EVIDENCED`;
2. `exact=true`;
3. exactly 10 unique RafBit state codes 0..9;
4. exactly 10 unique canonical BitOmega codes 0..9;
5. code/symbol agreement for BitOmega;
6. non-empty source identity;
7. non-empty semantic basis per pair;
8. evidence refs per pair;
9. non-`TOKEN_VAZIO` authority receipt;
10. `claim_allowed=false` remains invariant at this stage.

The schema does not itself authenticate the receipt and does not decide authorial/scientific truth. Those remain EVIDENCE/governance concerns.

`FORMAT_DEFINED != AUTHORITY_SUPPLIED`

`VALID_TOKEN_VAZIO != VALID_MAPPING`
