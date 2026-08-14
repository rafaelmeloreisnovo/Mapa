#!/usr/bin/env python3
"""Counterexample gate for HYP-MATH-TTT-RECURSIVE-MEMORY-063.

As currently worded, stability + persistence + sensitivity + one-parameter control
do not uniquely imply s'=(1-alpha)s+alpha*x.
The alternative below is first-order, linear, one-parameter, stable for alpha in
(0,1), persistent (state coefficient >0), and sensitive (input coefficient >0),
but is not the claimed EMA rule.
"""

def ema(alpha, s, x):
    return (1.0 - alpha) * s + alpha * x

def counterexample(alpha, s, x):
    return (1.0 - alpha * alpha) * s + alpha * x

for alpha in (0.1, 0.25, 0.5, 0.75, 0.9):
    a = 1.0 - alpha * alpha
    b = alpha
    assert 0.0 < a < 1.0, (alpha, a)          # stable/persistent coefficient
    assert b > 0.0, (alpha, b)                # input sensitivity
    if abs(counterexample(alpha, 0.37, -0.22) - ema(alpha, 0.37, -0.22)) < 1e-15:
        raise SystemExit(f'FAIL accidental equality at alpha={alpha}')

print('PASS counterexample exists under the four currently stated qualitative conditions.')
print('STATUS: UNIQUENESS_REFUTED_AS_STATED / REPAIRABLE.')
print('REPAIR: add a formal constant-input fixed-point axiom and define equivalence under parameter reparameterization; then prove the narrower theorem.')
