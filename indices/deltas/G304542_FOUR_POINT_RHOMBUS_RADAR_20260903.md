# G30/45/42 — four-point rhombus formalization and reading radar

Date: 2026-09-03  
Route ID: `ATLAS:G304542-FOUR-POINT-RHOMBUS-20260903`  
Parent hypothesis: `HYP-M2-G304542-002`  
State: `APPEND_ONLY / SIMULATED_LOCAL_MODEL / claim_allowed=false`

## Scope

This delta fixes one **minimal** interpretation chosen for this round:

```text
four labeled points of a rhombus
× all 24 label permutations
× three projection frames {0°, 30°, 45°}
```

It does not assert a physical model, a universal invariant, an emergent 42-cycle,
or a solution in any external mathematical/physical domain.

`RxNorm` is explicitly out of scope:

```text
TOKEN_VAZIO_SCOPE_RXNORM_NO_CLINICAL_INTEGRATION
```

No clinical vocabulary, patient information, medicine mapping, or health claim is
introduced by this route.

## Defined geometric kernel

Let

\[
u=(1,0),\qquad v=(1/2,\sqrt3/2),
\]

and define the centered rhombus in boundary order by

\[
V=\left\{-\frac{u+v}{2},\frac{u-v}{2},\frac{u+v}{2},\frac{-u+v}{2}\right\}.
\]

All four sides have length `1`.  The squared pair-distance spectrum is

\[
D(z)=\prod_{i<j}(z-\lVert p_i-p_j\rVert^2)=(z-1)^5(z-3).
\]

The two squared diagonal lengths are `3` and `1`; the long diagonal is at `30°`.
The special coincidence of one short diagonal with the side length is a property
of this chosen 60° rhombus, not a general property of a rhombus.

For a projection direction

\[
e_\alpha=(\cos\alpha,\sin\alpha),\qquad
P_\alpha(t)=\prod_{p\in V}(t-e_\alpha\cdot p),
\]

the three chosen images are:

\[
\begin{aligned}
P_0(t) &= t^4-\frac58t^2+\frac9{256},\\
P_{30}(t) &= t^4-\frac34t^2,\\
P_{45}(t) &= t^4-\frac{4+\sqrt3}{8}t^2+\frac3{256}.
\end{aligned}
\]

The requested polynomial overlay is therefore

\[
\Omega_V(t)=P_0(t)P_{30}(t)P_{45}(t).
\]

`D` and `Ω_V` are invariant under reordering the four labels because their roots
and pair distances are merely permuted.  This is a formal symmetry fact, not a
claim that they determine every rhombus up to every geometric equivalence.

## Minimal finite-state coupling

The finite state space is

\[
\mathcal S=S_4\times\mathbb Z/3\mathbb Z,
\]

with `24 × 3 = 72` states.  A state contains a label permutation and one active
projection frame.  The deliberately minimal transition is

\[
T(\pi,j)=(\operatorname{left\_rotate}(\pi),(j+1)\bmod 3).
\]

This is a symbolic observation schedule, not a physical rotation law.  Since the
left rotation has order `4` on a permutation and the frame advance has order `3`,

\[
T^{12}=\operatorname{id}.
\]

Every state has period `12`; the 72-state graph decomposes into six directed
12-cycles.  Thus the declared minimal rule has no 42-cycle:

```text
G304542_MINIMAL_MODEL_PERIOD = 12
G304542_PERIOD_42_OBSERVED = false
```

This is a counterexample **only to a claim that this exact minimal transition
produces 42**.  It neither proves nor disproves a different, fully specified
`G_{30,45,42}` rule.

## CMS Coverage

`CMS Coverage` is a route-local coverage label in this delta; no pre-existing
global Mapa schema with that exact name was located.

| Dimension | Covered now | Boundary |
|---|---:|---|
| Four-point geometry | yes | fixed unit-side 60° rhombus only |
| Pair distances / diagonals | 6 pairs | no general classification |
| Label permutations | 24 / 24 | label symmetry is not novelty |
| Projection images | 3 / 3 | frames only `{0°,30°,45°}` |
| Finite states | 72 / 72 | one declared transition only |
| Cycle test | all states | no endogenous 42-cycle under this `T` |
| Exact algebra | partial | local verifier uses IEEE-754 checks |
| Cross-host reproduction | no | `TOKEN_VAZIO` |

## NPI Registry

`NPI` is used here only as a route-local **Non-Promoted Invariant** registry.
It is not a novelty registry and does not establish priority.

| ID | Candidate invariant / method | Current status |
|---|---|---|
| `NPI-G304542-001` | squared distance polynomial `D(z)` | formal for fixed `V` |
| `NPI-G304542-002` | three-frame overlay `Ω_V(t)` | formal; label-invariant by construction |
| `NPI-G304542-003` | `T^12=id` for `S4×Z3` minimal rule | formal + locally simulated |
| `NPI-G304542-004` | period-42 counterexample for this `T` | formal + locally simulated |
| `NPI-G304542-005` | invariant beyond label symmetry | `TOKEN_VAZIO` |

## Reading radar

| Source | Concrete contribution to NPI / method | Direct use or counterexample |
|---|---|---|
| Domenico Lippolis, *Spatiotemporal stability of synchronized coupled map lattice states* (2026) | orbit-Jacobian eigenvalue analysis over space-time modes | Freeze any future coupling matrix, then test its spectrum rather than infer stability from a drawing. [Source](https://arxiv.org/abs/2510.12532) |
| Alexandr Prishlyak, *Algorithms and topological invariants for dynamic systems II* (2025) | simplicial complexes, Euler characteristic, homology, discrete Morse data | Give the 72-state transition graph a declared complex/invariant before calling its structure topological. [Source](https://arxiv.org/abs/2502.00506) |
| Hibiki Kato et al., *Finite Invariant Sets with Bridging Points in Logistic IFS* (2026) | exact conditions for finite invariant sets; bridge-point versus shared-intersection mechanisms | A future 30°↔45° two-map model must exhibit an actual bridge/intersection; otherwise it is not evidence of a new coupled invariant set. [Source](https://arxiv.org/abs/2604.13124) |
| Ievgen Bondarenko, Rostislav Grigorchuk, Alina Vdovina, *Ramanujan subshifts* (2026) | adjacency-spectrum bound and non-backtracking subshift method | Compute the actual transition graph spectrum first; do not call a 72-state graph mixing/Ramanujan without regularity and eigenvalue evidence. [Source](https://arxiv.org/abs/2602.22356) |
| Francesco Caravelli and Jean-Charles Delvenne, *Analog and Symbolic Computation through the Koopman Framework* (2025) | transition cycles impose algebraic constraints on operator spectra | Build the `72×72` permutation matrix for `T`; a 42-cycle requires a different operator spectrum from the present 12-cycle rule. [Source](https://arxiv.org/abs/2510.05863) |

## Formalization step executed

The local standard-library verifier:

```text
tools/verify_g304542_four_point_rhombus_v1.py
```

enumerates all 24 permutations and all 72 finite states, checks the distance and
projection-polynomial invariants, and emits the receipt:

```text
data/receipts/G304542_FOUR_POINT_RHOMBUS_LOCAL_20260903.v1.json
```

Observed local output:

```json
{"finite_states":72,"model_id":"G304542:FOUR_POINT_RHOMBUS:V1","period":12,"period_42_observed":false}
```

This is `SIMULATED_LOCAL_MODEL`, not `PROVEN` or `CROSS_HOST`.

```text
script_sha256  = 514f5cce2da2bf17d239652cc08b16e56e4d329f45077e1d2e1b9144cc450716
receipt_sha256 = 418ce64a3dda93ba86d584f42f0ba89c5d19a15ba7a13f47badea5330ea64eee
```

## Gates and next probe

```text
RLL_SCOPE_GUARD = NO_LIKELIHOOD_OR_COSMOLOGY_INPUT
SMART_GUARD_SCOPE = RESEARCH_FORMALIZATION_ONLY
claim_allowed = false
```

Open gates:

- `TOKEN_VAZIO_G304542_CANONICAL_COUPLING_BEYOND_MINIMAL_RULE`
- `TOKEN_VAZIO_G304542_ENDOGENOUS_42_CYCLE`
- `TOKEN_VAZIO_G304542_NONTRIVIAL_INVARIANT_BEYOND_LABEL_SYMMETRY`
- `TOKEN_VAZIO_G304542_EQUIVALENCE_AND_PRIOR_ART`
- `TOKEN_VAZIO_G304542_EXACT_SYMBOLIC_PROOF`
- `TOKEN_VAZIO_G304542_CROSS_HOST_REPRODUCTION`
- `TOKEN_VAZIO_SCOPE_RXNORM_NO_CLINICAL_INTEGRATION`

**Next falsifiable step:** propose exactly one alternative transition
`T' : S_4×Z_3 → S_4×Z_3`, declare its parameters and initial-state domain, then
enumerate every state.  A period-42 claim is admissible for review only if the
enumeration contains a 42-cycle and the same serialized receipt reproduces on an
independent host.

`VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`
