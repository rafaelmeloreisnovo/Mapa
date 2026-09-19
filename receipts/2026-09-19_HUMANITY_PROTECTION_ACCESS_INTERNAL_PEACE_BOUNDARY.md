# Successor Receipt — Humanity Protection & Access — Internal Peace Boundary — 2026-09-19

state: INTERNAL_SCOPE_CLOSED_EXTERNAL_AUTHORITIES_OPEN  
claim_allowed: false  
publication_ready: false  
merge_allowed_by_this_receipt: false

## Fresh authoritative-source verification

Verified on 2026-09-19 against:

- [WIPO Berne Convention summary](https://www.wipo.int/en/web/treaties/ip/berne/summary_berne)
- [Brazil Lei 9.610/1998](https://www.planalto.gov.br/ccivil_03/leis/l9610.htm)
- [Brazil Lei 9.609/1998](https://www.planalto.gov.br/ccivil_03/leis/l9609.htm)
- [Creative Commons software guidance](https://creativecommons.org/chooser/)

Observed legal boundaries remain consistent with the draft:

- Berne protection is based on national treatment, automatic protection, and independence of protection; it is not a blanket private relicense.
- Brazilian copyright law and software law remain distinct authorities; software protection is governed by Lei 9.609/1998 with copyright-law linkage.
- Creative Commons does not recommend CC licenses for software; standard software licenses should govern software release.
- Rights in third-party or mixed works cannot be granted merely by repository ownership or authorial intent.

## Exact-head gate observation before this successor

PR #652 head: `25ab015c68a9d29be6d3104c83701b7683614fbd`

PASS:

- CI run 35427703457
- Legal Governance Gates run 35427703444
- Workflow Supply-Chain Ratchet run 35427703447
- Human Dignity Ethics Gate V1 run 35427703455
- SecurityCodeScan run 35427703466
- CodeQL Advanced run 35427703456
- Branch Topology Gate run 35427703478
- Workflow Graph Audit run 35427703460
- main-hardening-gate run 35427703471

OPEN / correctly fail-closed:

- Provider Protection Gate run 35427703509: no effective applicable default-branch ruleset observed.
- Server Merge Enforcement run 35427703475: required status/review enforcement not observed.
- CodeScan run 35427703463: required credential presence failed; analysis intentionally did not run.
- Promotion Control run 35427703433: negative tests PASS; enforce blocked at manual promotion / independent-authority boundary.

## Boundary

`BERNE_PROTECTION != LICENSE_GRANT`  
`AUTHORIAL_INTENT != THIRD_PARTY_RELICENSE_AUTHORITY`  
`TECHNICAL_GATES_PASS != LEGAL_OPINION`  
`SELF_REVIEW != INDEPENDENT_APPROVAL`  
`NO_RULESET != RULESET_PASS`  
`MISSING_CREDENTIAL != CODESCAN_RESULT`  
`TOKEN_VAZIO != CLEARED`

## Peace criterion

No further internal code/document change should manufacture:

1. an independent human approval;
2. GitHub repository or organization ruleset administration;
3. server-side required-check enforcement;
4. CodeScan account credentials;
5. licensed-counsel legal opinion;
6. file-level rights facts not evidenced by source records.

The PR remains a draft until a real external authority changes one of those states. When that occurs, rerun the corresponding gate and append a successor receipt.

## R3

F_ok = legal text structure + machine validator + CI/legal/security/CodeQL source checks + authoritative-source cross-check.  
F_gap = external reviewer/provider/credential/counsel and file-level rights evidence.  
F_next = event-driven only: rerun after genuine external state change; do not create synthetic approval or synthetic rights.
