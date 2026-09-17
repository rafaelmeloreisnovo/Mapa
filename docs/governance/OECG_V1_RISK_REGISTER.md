# OECG V1 bounded risk register

> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧

This register records current bounded risks. It is not a claim that unlisted risks do not exist.

| ID | Risk | Current state | Mitigation | Closing evidence |
| --- | --- | --- | --- | --- |
| R1 | `primeira_linha_ok=true` can be asserted rather than recomputed | OPEN | machine-readable first-line gates + negative controls | execution receipt showing unresolved gate fails |
| R2 | actor identity may be mistaken for authorship authority | MITIGATED_DRAFT | μ-event v2 separates actor/authorship/sense/claim authority | schema/checker fixture + CI PASS |
| R3 | missing source interpreted as absence/false | CONTROLLED_BY_POLICY | `TOKEN_VAZIO != 0`; search miss != absence | validator/receipt review |
| R4 | Nibiguiri used to infer censorship/hidden weighting without evidence | MITIGATED_DRAFT | restricted evidence-backed recovery states | tests + review |
| R5 | CI PASS treated as global compliance/safety claim | OPEN_CONTROL | explicit scope boundary and `claim_allowed=false` | independent applicable gates |
| R6 | deterministic replay incomplete | OPEN | fixture canonicalization then operator-version-locked replay | repeat hash + replay receipt |
| R7 | rollback defined only narratively | PARTIAL | branch-only additive delta + successor/supersedes rule | tested revert/supersession receipt |
| R8 | provider rulesets/approval/security state differs from repository content | EXTERNAL_OPEN | keep provider governance separate/fail-closed | provider readback + rejection test |
| R9 | privacy/minor status inferred from absent data | MITIGATED_DRAFT | explicit privacy/minor fields; unknown remains TOKEN_VAZIO | negative privacy fixtures |
| R10 | continuous improvement becomes endless mutation | CONTROLLED_BY_POLICY | bounded exit conditions + single F_next | receipt shows stop condition |

## Priority

P0: R1, R2, R6.  
P1: R7, R8, R9.  
P2: R4, R5, R10 ongoing governance controls.
