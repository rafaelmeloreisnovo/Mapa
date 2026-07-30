# Acceptance criteria — Vertical Slice V1

The branch may be reviewed when:

- the registry remains `claim_allowed=false`;
- all claims have an explicit falsifier;
- the reference receipt is preserved unchanged;
- tests and the fail-closed gate pass on the exact head;
- no raw conversation bodies or secrets are committed;
- Termux replication and human review remain TOKEN_VAZIO until actually observed.

Merge does not imply S5, S6 or S7. Promotion of maturity requires append-only evidence for each missing gate.
