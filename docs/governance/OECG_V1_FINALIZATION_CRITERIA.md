# OECG V1 bounded finalization criteria

V1 can move from `IMPLEMENTED_DRAFT` to `VERIFIED_LIMITED` only when all are observed on the exact candidate head:

1. OECG contract validator PASS.
2. Positive receipt fixture PASS.
3. Invalid-authority negative fixture FAILS as expected.
4. Semantic-event v2 fixture PASS.
5. Deterministic canonical hash repeats identically in two executions.
6. Governance unit/CLI tests PASS.
7. Branch head/revision is captured in a successor receipt.
8. Rollback/supersession route is recorded.
9. Drive router/book-memory receives only a pointer/μWRITE after evidence exists.
10. `claim_allowed=false` remains; global compliance/safety/authorship claims are not promoted.

Anything not tested remains a typed gap.
