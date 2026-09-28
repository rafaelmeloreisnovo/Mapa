# ATLAS — RIVER-7 Gap Closure Delta V2 — 2026-09-28

**parent:** \`ATLAS_RIVER7_DUAL_TRANSPORT_ROUTING_20260928\`  
**mode:** \`POINTER_ONLY / APPEND_ONLY / FAIL_CLOSED\`  
**claim_allowed:** \`false\`

## Current state

The V1 routing PRs are merged:

- \`papers#110\` — merged.
- \`Matem-tica-#56\` — merged.
- \`ChipQuantum#85\` — merged.
- \`Mapa#690\` — merged.

The V2 successor PRs are:

- \`papers#111\` — research synthesis and notation correction.
- \`Matem-tica-#57\` — formal [7,4,3] erasure-code authority.
- \`ChipQuantum#86\` — executable offline simulator, tests and dedicated CI gate.

## Material delta

\`GAP:RIVER7-FEC-GENERAL\` is partially reduced by a finite systematic
\([7,4,3]\) code over \(GF(2)\).

Observed in the session-level finite execution:

\`\`\`text
d_min = 3
guaranteed_known_erasures = 2
loss=0:  1/1 recovered
loss=1:  7/7 recovered
loss=2: 21/21 recovered
loss=3: 28/35 recovered; 7 explicit failures
arrival permutations: 120/120 recovered for the selected 5-symbol set
synthetic independent timing fixture: MI = 0 bit
synthetic correlated detector fixture: MI = 1 bit
\`\`\`

The correlated timing fixture is a detector control only. It is not a permitted
network transport mechanism.

## Authority routing

\`\`\`text
PR:papers#111
  --SYNTHESIZES-->
PR:Matem-tica-#57
  --FORMALIZES-->
PR:ChipQuantum#86
  --EXECUTES_OFFLINE-->
EVD:RIVER7:CI_PENDING
\`\`\`

## Gap ledger

| Gap | State | Authority |
|---|---|---|
| RIVER7-NOTATION-CORRUPTION | FIXED_IN_PR | papers#111 / Matem-tica-#57 |
| RIVER7-FEC-743 | CLOSED_FINITE_DOMAIN | Matem-tica-#57 |
| RIVER7-REORDER | CLOSED_FINITE_DOMAIN | ChipQuantum#86 |
| RIVER7-LEAKAGE-SYNTHETIC | PARTIAL_CLOSED | ChipQuantum#86 |
| RIVER7-CI | PENDING | ChipQuantum#86 |
| RIVER7-FEC-GENERAL | OPEN | TOKEN_VAZIO |
| RIVER7-AUTH-SYMBOL | OPEN | TOKEN_VAZIO |
| RIVER7-LOSS-BURST | OPEN | TOKEN_VAZIO |
| RIVER7-LEAKAGE-PHYSICAL | NOT_RUN | TOKEN_VAZIO |
| RIVER7-PHYSICAL | NOT_RUN | TOKEN_VAZIO |
| RIVER7-WIRE | ROUTE_STATE_BLOCKED | depends on CI/auth/privacy gates |
| RIVER7-PRODUCTION | ROUTE_STATE_BLOCKED | depends on physical + governance evidence |

## Claim gate

\`\`\`text
SESSION_SIMULATION_PASS != CI_PASS
CI_PASS                 != PHYSICAL_PASS
PHYSICAL_PASS           != PRODUCTION_READY
\`\`\`

No hidden timing/loss/TTL/fragmentation carrier is promoted by this delta.

## F_next

1. Observe the dedicated \`RIVER-7 Offline Validation\` workflow for
   \`ChipQuantum#86\`.
2. If and only if it passes, bind the workflow run and artifact receipt here.
3. Keep physical network and production states blocked.
4. Next mathematical delta: deterministic burst-erasure model or authenticated
   symbol-envelope specification, whichever closes the highest-value open gap
   without network deployment.

## R3

\`F_ok\`: V1 merged; V2 formal and executable delta routed; finite-domain gaps
partially closed.  
\`F_gap\`: CI result, generalized FEC, authenticated envelope, burst-loss model,
physical leakage and physical execution.  
\`F_next\`: bind the dedicated CI evidence; do not promote beyond it.
