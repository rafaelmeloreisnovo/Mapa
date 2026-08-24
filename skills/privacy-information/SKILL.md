---
name: privacy-information
description: Classify information exposure/custody and block cross-surface disclosure when sensitivity is unknown.
version: 1.0.0
status: DRAFT_FAIL_CLOSED
---

# D5 — Privacy & Information

## Classes

`PUBLIC | INTERNAL | PRIVATE | REDACTED | SEALED | TOKEN_VAZIO_SENSITIVITY`.

Unknown sensitivity defaults to `PRIVATE_DEFAULT_DENY` for publication or cross-surface movement.

## Procedure

1. Identify data subject/context and source authority.
2. Minimize data: move commitments/hashes instead of raw content when sufficient.
3. Separate public receipt from private locator/content.
4. Record redaction basis; never infer `CENSORED` from mere absence.
5. Check whether destination changes privacy/security boundary.

## Hard rules

- credentials/secrets never enter public receipts;
- private Drive locators do not enter public GitHub unless explicitly authorized and necessary;
- unknown protected-subject/privacy context blocks promotion/disclosure;
- `WITHHELD_BY_POLICY` or `REDACTED_PRIVACY` requires documented basis; otherwise use `TOKEN_VAZIO_REASON`.

## Output

`data_class`, `disclosure_allowed`, `minimum_data`, `redaction_state`, `destination_boundary`, `authority_basis`, `F_ok/F_gap/F_next`.
