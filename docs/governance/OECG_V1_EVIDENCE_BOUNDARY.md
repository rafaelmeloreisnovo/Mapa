# OECG V1 evidence boundary

Evidence is typed by what it can actually support:

`SOURCE -> ARTIFACT -> EXECUTION -> OBSERVATION -> EVIDENCE -> CLAIM`

Examples:

- file existence supports artifact existence, not execution;
- a unit-test PASS supports the tested invariant on the tested revision, not production behavior;
- a workflow PASS supports the workflow's bounded checks, not legal compliance;
- an author declaration supports `DECLARED_BY_AUTHOR`, not independent authorship proof;
- a repeated deterministic hash supports canonicalization/replay stability for that fixture, not semantic truth;
- a provider readback supports observed provider state at that time, not permanence.

Contradictory evidence is preserved and routed; it is not averaged away for a cleaner score.
