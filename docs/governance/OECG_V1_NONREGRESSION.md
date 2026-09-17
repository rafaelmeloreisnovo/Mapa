# OECG V1 non-regression invariants

A successor must not reduce these controls without an explicit human-approved supersession:

- TOKEN_VAZIO remains distinct from zero/false/null/missing.
- source/artifact/execution/evidence/claim remain distinct.
- actor/authorship/sense/claim authority remain distinct.
- historical receipts remain immutable observations.
- contradictions remain preserved.
- privacy and child-safety remain fail-closed when applicable.
- producer repositories retain implementation authority.
- corrections are append + supersedes.
- rollback/supersession is navigable.
- no autonomous goal creation.

A simpler implementation is welcome only if these invariants remain reconstructible and tested.
