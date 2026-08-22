# RAFAELIA — Calculation Memory E1 Structural + Spiral Route Delta — 2026-08-22

**State:** `E1_STRUCTURAL_PARTIAL_PASS / SPIRAL_RADIAL_EXECUTED / ANGULAR_MISMATCH / claim_allowed=false`  
**Mode:** `APPEND_ONLY / EVIDENCE_FIRST`  
**Predecessor:** `indices/RAFAELIA_CALCULATION_MEMORY_INDEX_V2_20260822.md`

## E1 structural gate

Starting denominator: `356` bounded E0 representatives.

- structurally parsed: `339 / 356` (`95.225%`);
- typed failures: `17`;
- failure classes: `16 MIXED_NATURAL_LANGUAGE`, `1 UNSUPPORTED_CHAR` (`🆕`);
- structural AST identities inside parsed subset: `331`;
- E1 merge groups: `8`;
- E1 duplicate extra occurrences: `8`.

The merges are limited to lexical/syntactic normalization such as whitespace, `φ↔phi`, `√↔sqrt`, `->↔→` and operator spacing. No algebraic reordering or semantic promotion is allowed by this pass.

A conservative E2 rational-assignment subset inspected `19` candidates and produced `19` unique canonical forms, with `0` new merges beyond E1. This is a bounded negative result, not global E2 closure.

Persistent Drive checkpoint:

- spreadsheet: `1HDaHo5IBj42rr-iyxftG1zfaEzzCI9xC4s_0W_-1vR8`;
- sheet: `E1_STRUCTURAL_V2_20260822`.

## End-to-end route: Spiral√3/2

Memory unit: `MCM:TEO:SPIRAL_R:003:v1`.

Source authority:

- repo: `rafaelmeloreisnovo/teoremas`;
- path: `docs/rafaelia/04-spiral-raiz3-sobre-2.md`;
- blob: `eaa831155fcfac79fa72d1cd6fd13f5d5d9aecb8`;
- radial source law: `r_{n+1}=(√3/2)r_n`;
- angular source law: `θ_{n+1}=θ_n+π/φ`.

Implementation candidate bound by code search:

- repo: `rafaelmeloreisnovo/GAIA_phi`;
- path: `dados/RAFAELIA_TRIG_CORE2.py`;
- blob: `cccf5f7da96e2f867fbb5cdec07a45da6e380994`;
- function: `generate_spiral_sqrt3_over_2`;
- implemented radius: `r0*(SQRT3_OVER_2**k)`;
- implemented angle: `sign*2π*k/steps_per_turn`.

Executed portable harness:

- `tools/audit/verify_spiral_route_v1.py`;
- SHA-256: `5b3c186daf1db9ebece164ecc92f7689e393b5aa363c9926fab688e2a128eedf`;
- receipt: `data/receipts/spiral_route_execution_20260822.v1.json`;
- receipt SHA-256: `32546c4ebb006debd51092113b2b170754fc08bba31bb208a7970179b8be48ba`.

Observed gates:

| Gate | Result |
|---|---|
| radial recurrence | `PASS_NUMERIC_LIMITED`, max abs error `5.551115123125783e-17` |
| radial closed form | `PASS_NUMERIC_LIMITED`, max abs error `2.7755575615628914e-17` |
| Yin-Yang point count | `PASS`, `42` |
| angular equivalence | `FAIL_NOT_SAME_FORM` |
| full source-pair equivalence | `TOKEN_VAZIO_NOT_ESTABLISHED` |

The radial source→implementation→execution route is therefore materially closed within the numerical test boundary. The complete two-equation Spiral source is **not** implementation-equivalent to this GAIA_phi generator because the angular laws differ.

## R3

**F_ok:** E1 structural coverage materially increased while keeping typed failures; the radial Spiral formula was routed from Drive memory to source blob, to a real implementation blob, to a deterministic executed harness and receipt.  
**F_gap:** `17` E1 representatives remain typed `TOKEN_VAZIO`; global E2 remains open; the source angular `π/φ` recurrence is not the angular law in the GAIA_phi generator.  
**F_next:** split radial and angular Spiral variants in calculation memory or bind a producer implementation for `θ_{n+1}=θ_n+π/φ`; only then execute the dedicated angular gate and consider full-formula equivalence.
