# ATLAS:X Ω202 — Markdown debt dispersion

cycle_id: OMEGA-FED-20260910-202
predecessor: OMEGA-FED-20260910-201
mode: BULK-FIRST | CURSOR-FIRST | EVIDENCE-FIRST
claim_allowed: false

## Source

- GitHub Actions run: 34474374627
- job: 102861505709 (`Validate Repository Structure`)
- measured tool: markdownlint-cli2 0.23.2
- baseline ceiling: 890 issues / 95 files_with_issues

## Measurement

- files_linted: 675
- issues: 857 / 890 => PASS on total-issue ceiling (`-33`)
- files_with_issues: 107 / 95 => FAIL on spread ceiling (`+12`)
- changed-file gate: 0 issues in 0 files for the Ω200-corrected Atlas file

## Gap transition

`G200-05`: `BLOCKED_GLOBAL_DEBT_RATCHET_REPRODUCED_FAIL` -> `MEASURED_DISPERSION_EXCESS`

The blocker is not total issue count. The observed failure is debt spread across too many files. This measurement does not authorize increasing the baseline or bulk-normalizing historical Markdown.

### Typed gap

- gap_id: G202-01
- state: MEASURED + BLOCKED_GLOBAL_DEBT_DISPERSION
- source_pointer: run 34474374627 / job 102861505709
- missing_field: minimum safe set of historical files whose remediation can reduce files_with_issues from 107 to <=95 without increasing total issues
- blocking_dependency: bounded remediation plan preserving historical content and no-increase ratchet
- evidence_needed: changed-file lint PASS plus repository ratchet PASS on a proposed bounded delta
- falsifier: files_with_issues remains >95 or total issues rises above 890
- next_probe: rank the 12+ lowest-risk one-issue historical files and test a proposed remediation set on an audit branch
- owner/authority: rafaelmeloreisnovo/Mapa
- urgency: high
- closure_gate: issues<=890 AND files_with_issues<=95 on provider CI
- claim_allowed: false
- predecessor/lineage: Ω200/G200-05 -> Ω201 -> Ω202/G202-01

## Current provider boundary

At observation time, `GET /branches/main` reports `protected=false` and enforcement off for the returned branch summary. This is a current-state observation only and does not prove the protection state at the historical merge instant; `G201-01` therefore remains open for historical enforcement-at-merge evidence.

## R3

- F_ok: exact ratchet counts measured; failure dimension isolated; changed-file lint remains clean.
- F_gap: safe bounded remediation set not yet tested; historical enforcement-at-merge remains TOKEN_VAZIO.
- F_next: select a minimum low-risk remediation set sufficient to reduce spread by at least 12 files, then test on a separate audit branch without raising baseline.
