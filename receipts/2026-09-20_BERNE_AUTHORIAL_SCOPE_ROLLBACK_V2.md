# Receipt — Berne Authorial Scope Rollback V2 — 2026-09-20

state: CANONICAL_ROLLBACK_ACTIVE  
claim_allowed: false  
timestamp: 2026-09-20T02:19:00-03:00

## Intent
Restore Berne/authorship/provenance as the canonical primary route for RAFAELIA-original copyrightable expression and reattach all known knowledge classes to the provenance graph.

## Sources
- `docs/legal/INTERNATIONAL_AUTHORSHIP_TREATY_DOCTRINE_V1.md`
- `docs/legal/HUMANITY_PROTECTION_AND_ACCESS_COVENANT_V1.md`
- WIPO Berne Convention summary
- Brazil Decreto 75.699/1975
- Brazil Lei 9.610/1998
- Brazil Lei 9.609/1998

## Delta
- creates `docs/legal/BERNE_AUTHORIAL_SCOPE_ROLLBACK_V2.md`;
- restores Berne/authorship/provenance governance priority;
- subordinates the humanity-access overlay for new authorial-scope decisions;
- preserves all valid prior license grants and upstream rights;
- maps formulas/discoveries/models back into provenance without false abstract-copyright claims;
- requires federation pointers and Drive μWRITE.

## Invariants
```text
BERNE_PROTECTION != LICENSE_GRANT
ROLLBACK_GOVERNANCE != REVOCATION_OF_VALID_PRIOR_GRANTS
ABSTRACT_IDEA_METHOD_FACT != COPYRIGHTABLE_EXPRESSION
THIRD_PARTY_RIGHTS != RAFAELIA_RIGHTS
TOKEN_VAZIO != CLEARED
```

## R3
F_ok: canonical rollback materialized.  
F_gap: file-level rights inventory remains incomplete across the whole corpus.  
F_next: federate references + Drive canonical receipt.
