# Continuous memory append contract — Vertical Slice V1

Memory records are append-only and divided into typed carriers:

- `entities`: stable identities;
- `relations`: typed dependencies;
- `claims`: epistemic statements with falsifiers;
- `gaps`: explicit TOKEN_VAZIO states;
- `experiments`: executable methods;
- `receipts`: immutable observations;
- `decisions`: human/accountable interpretations.

Selective retroaction uses source ID, hash, revision and reverse dependencies. A new run appends a new receipt and decision; it never rewrites the prior receipt. Unaffected records are preserved.

```text
R3 = <F_ok, F_gap, F_next>
```
