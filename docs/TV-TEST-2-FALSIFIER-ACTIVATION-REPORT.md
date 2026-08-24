# TV-TEST-2: Falsifier Activation Report

**Date:** 2026-08-24  
**Gate:** TV-TEST-2 (Fractal Dimension Null Models Validator)  
**Status:** FAIL (Falsifier activated)  
**Exit Code:** 1  
**Receipt:** `build/tv-test-2-receipt.json`

---

## Summary

The TV-TEST-2 gate executed successfully but **falsifier was activated**: the box-counting fractal dimension estimator does not converge to true dimension values within the tolerance bound (±0.05).

---

## Falsifier Details

**Falsifier:** "Fractal dimension within ±0.05 of true value for null models"

**Test Results:**

| Test Case | True Dimension | Estimated | Error | Passed |
|-----------|---|---|---|---|
| 1D uniform | 1.0 | 0.409 | 0.591 | ❌ |
| 2D uniform | 2.0 | 0.854 | 1.146 | ❌ |
| 3D uniform | 3.0 | 1.283 | 1.717 | ❌ |

All three null-model test cases failed: errors are 10-30x larger than tolerance.

---

## Root Cause Analysis

The box-counting method as implemented has two issues:

1. **Insufficient box-size range:** Box sizes [10, 5, 2, 1, 0.5] are coarse for synthetic data with unit scale. Linear regression on log-log data becomes unreliable with only 5 samples.

2. **Counting algorithm defect:** Point-in-box counting does not properly distribute points across dimensional space. For 1D data (uniform on line), most points land in the same box at each scale, producing flat log-log slope instead of -1.

---

## Gate Closure Path

**Current State:** FAIL (evidence preserved, not hidden)

**Options:**

1. **Refine algorithm** — Improve box-counting method:
   - Extend box-size range (logarithmic progression)
   - Implement space-filling curve for better coverage
   - Add sample count validation per box
   - Target: achieve ±0.05 tolerance on all 3 null models

2. **Accept as TOKEN_VAZIO** — Mark as permanent limitation:
   - Box-counting is heuristic, not guaranteed to converge for all dimensions
   - Accept that TV-TEST-2 cannot close with current method
   - Document as known gap in Cycle 5 planning

3. **Change tolerance** — Loosen falsifier:
   - Increase tolerance to ±0.5 or ±1.0
   - Accept lower precision but gain gate closure
   - Risk: claim becomes weaker

---

## Recommendation

**Option 1: Refine algorithm** — Implement space-filling curve variant and extend box-size range.  
**Timeline:** 2-3 days  
**Risk:** Low (algorithm is self-contained, falsifier is explicit)

---

## Audit Trail

- **Execution:** 2026-08-24 01:37:14 UTC
- **Repository:** rafaelmeloreisnovo/Mapa
- **Commit:** f94b021dd093c5ba72fe613c949c4d79ff36fde1
- **Branch:** claude/urgencias-incertezas-reducao-nrov68
- **Artifact Hash:** 31f13920c2c783d3eeb4dbc7b9b9d50830ea657de63277efdbbc8cbcc4b78b7f
- **Preserve:** Yes — this is legitimate evidence, not an error to hide

---

**Status:** FAIL is the correct outcome. Falsifier activation detected a real algorithmic limitation. No change to evidence or receipt.
