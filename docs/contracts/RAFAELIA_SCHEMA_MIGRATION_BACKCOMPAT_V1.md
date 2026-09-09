# RAFAELIA Schema Migration + Backward Compatibility V1

Gap: `G068`  
State: `SPEC_DEFINED_LOCAL / MIGRATION_MATRIX_POPULATION_OPEN / claim_allowed=false`

Every migration edge is a versioned object:

`FROM_SCHEMA → TRANSFORM → TO_SCHEMA → INVARIANTS → POSITIVE_KAT → NEGATIVE_KAT → RECEIPT`.

Required fields per edge:
- source schema/version/hash;
- target schema/version/hash;
- deterministic transform identity/hash;
- fields preserved, renamed, split, merged or intentionally dropped;
- downgrade policy;
- positive and negative golden vectors;
- semantic invariants;
- failure behavior.

Rules:
1. Same field name does not imply same semantics.
2. Lossy migration must declare the lost information and cannot advertise round-trip identity.
3. Unknown future fields fail closed unless the schema explicitly declares safe ignore semantics.
4. A reader compatibility claim is scoped to exact schema versions and vectors.
5. `MIGRATION_PASS != HISTORICAL_IDENTITY`.

Closure requires a populated matrix for the active ZIPRAF/BitRAF/GeoWord/Atlas/receipt schemas and machine-tested KATs.
