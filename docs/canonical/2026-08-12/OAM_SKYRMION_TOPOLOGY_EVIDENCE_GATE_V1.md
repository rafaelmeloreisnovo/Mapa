# OAM–Skyrmion Topology Evidence Gate V1 — 2026-08-12

Status: `VERIFIED_LIMITED`

`claim_allowed=false`

## 1. Boundary of the claim

Primary result under review: Kleine et al., **Topological Robustness of Orbital Angular Momentum Entanglement in Stochastic Channels**, *Physical Review Letters* 137, 050602 (2026), DOI `10.1103/9pdm-1d27`, arXiv `2603.10618`.

The paper reports that OAM modes/correlations are sensitive to turbulence while a topological observable built from the OAM-entangled state, quantified by a skyrmion number, remains robust over the investigated stochastic channels. The paper does **not** establish that OAM itself is unchanged, that information is universally indestructible, or that arbitrary perturbations preserve topology.

Canonical observable:

\[
N=\frac{1}{4\pi}\int_{\mathbb{R}^2}\epsilon_{ijk}\tilde b_i\,\partial_x\tilde b_j\,\partial_y\tilde b_k\,dx\,dy.
\]

Invariant boundary preserved here:

`paper result != local toy reproduction != independent experiment != RAFAELIA hypothesis`.

## 2. What was independently tested now

A dependency-free Python test was created at:

`experiments/oam_skyrmion_topology/skyrmion_invariant_test.py`

SHA-256:

`31adaf0118b0409d47e0becb30512bde9a71da1d9d3a9b9a437dbb10f70582b3`

Execution environment: Python 3.13.5, Linux x86_64, standard library only.

Command:

```sh
python3 skyrmion_invariant_test.py --grid 181
```

The command was executed twice. Stdout was byte-identical both times.

Stdout SHA-256:

`97f9c1d21f9e0b7d26d3b0a9324ce8efb53287a8629e6ffa3d1581f2cb82833c`

### 2.1 Base winding test

The selected texture has a sign convention in which positive input winding gives negative computed charge; evidence is assessed through `|Q|`.

| Input | Computed Q | Relative |Q| error |
|---:|---:|---:|
| +1 | -0.9694232561 | 3.0577% |
| +2 | -1.9872533477 | 0.6373% |
| +3 | -2.9661656980 | 1.1278% |
| +5 | -4.8523210779 | 2.9536% |
| -1 | +0.9694232561 | 3.0577% |
| -2 | +1.9872533477 | 0.6373% |
| -3 | +2.9661656980 | 1.1278% |
| -5 | +4.8523210779 | 2.9536% |

Interpretation: `PASS_LIMITED`. The integer degree is approached but is not rounded into evidence. Residual error is retained as numerical uncertainty.

### 2.2 Smooth coordinate deformation

For the `N=3` texture, smooth warps with amplitudes `0, 0.3, 0.7, 1.2, 2.0` yielded Q from `-2.9661656980` to `-2.9659527260`.

Interpretation: within this toy model and discretization, smooth coordinate deformation leaves the global charge essentially unchanged even while local coordinates are distorted.

### 2.3 Global Bloch-space rotation

A global `SO(3)` rotation of the `N=3` field yielded:

`Q = -2.9661656979955175`

which is numerically identical to the unrotated value at displayed precision.

Interpretation: `PASS_LIMITED`, as expected for an orientation-preserving rotation of the target sphere.

### 2.4 Deliberate failure boundary: Bloch-field displacement

Adding a constant displacement to the Bloch field and renormalizing without recovering the center eventually destroys the measured winding:

| shift | Q without recenter | Q after known recenter |
|---:|---:|---:|
| 0.2 | -2.96429 | -2.96617 |
| 0.5 | -2.94616 | -2.96617 |
| 0.9 | -2.55913 | -2.96617 |
| 1.2 | -0.07453 | -2.96617 |
| 1.5 | -0.00863 | -2.96617 |

This is a useful counterexample to the phrase “indestructible”. Robustness depends on the allowed deformation class and on having a well-defined normalized field/map. Recentring here uses the **known imposed displacement**, so it is a controlled toy recovery, not an experimentally inferred correction.

## 3. Primary-paper evidence retained

The primary paper reports eight turbulence strengths `Omega=0.25..2.00`, ten independent experimental realizations per strength, ten prepared topologies with charges in `{±1, ±2, ±3, ±5}`, and numerical simulations with 100 realizations per strength. In the ensemble-averaged dynamic-channel treatment, purity decreases toward about 33% while the measured skyrmion number remains stable over the tested range.

The paper states explicitly that its data are **not publicly available** and may be obtained from the authors upon reasonable request.

Therefore these statements have status `SUPPORTED_BY_PRIMARY_SOURCE`, not `INDEPENDENTLY_REPRODUCED_HERE`.

## 4. Uncertainty / TOKEN_VAZIO ledger

| ID | State | Urgency | Importance | Meaning / next evidence |
|---|---|---:|---:|---|
| `TV_RAW_DATA` | `TOKEN_VAZIO_PUBLIC_DATA` | P0 | critical | Obtain authors' exact dataset; hash bytes; recompute N, purity and error bars. |
| `TV_EXACT_REALISATIONS` | `TOKEN_VAZIO` | P0 | critical | Obtain/generate exact turbulence screens or seeds and confirm statistical equivalence. |
| `TV_FULL_CHANNEL_REPRO` | `TOKEN_VAZIO` | P0 | critical | Implement Supplementary turbulence-channel model over Omega 0.25..2.00 with seeded Monte Carlo. |
| `U_GRID_BOUNDARY` | `MEASURED` | P1 | high | Run domain/grid convergence and an independent geometric lattice-charge estimator. |
| `TV_QST_COUNTS` | `TOKEN_VAZIO` | P1 | high | Raw coincidence counts / tomography inputs unavailable in this audit. |
| `TV_HARDWARE_REPLICATION` | `TOKEN_VAZIO` | P2 | critical | Requires independent SPDC/SLM/SMF/QST optical-lab reproduction. |
| `TV_RAFAELIA_EQUIVALENCE` | `TOKEN_VAZIO_HYPOTHESIS` | P1 | critical | Define an explicit state-space map and invariant-preserving transformation class before claiming mathematical equivalence. |
| `TV_REAL_WORLD_GENERALISATION` | `TOKEN_VAZIO` | P2 | high | Atmospheric free-space/underwater/turbid-field deployment is not demonstrated by this local test. |

## 5. Claims gate

### Allowed at this checkpoint

- The PRL paper and its primary claims are real and precisely identifiable.
- A local toy computation reproduces the expected stability of a skyrmion-degree integral under smooth coordinate deformations and global `SO(3)` rotation.
- The toy computation also exposes a failure regime, supporting a scoped rather than absolute interpretation of topological robustness.
- Local toy execution is deterministic for the recorded runtime and command.

### Not allowed

- “The OAM is unaffected by turbulence.”
- “The information cannot be destroyed.”
- “The paper proves RAFAELIA.”
- “RAFAELIA's invariant is the same skyrmion invariant.”
- “The PRL experiment has been independently reproduced here.”
- “The result already proves an inviolable quantum network.”

## 6. Provenance chain

1. APS record: DOI `10.1103/9pdm-1d27`, published 2026-07-28.
2. arXiv record: `2603.10618`, including Supplementary Information and data-availability statement.
3. Local dependency-free test: SHA-256 `31adaf0118b0409d47e0becb30512bde9a71da1d9d3a9b9a437dbb10f70582b3`.
4. Deterministic stdout: SHA-256 `97f9c1d21f9e0b7d26d3b0a9324ce8efb53287a8629e6ffa3d1581f2cb82833c`.
5. Structured receipt: `data/evidence/oam_skyrmion_topology_receipt_2026-08-12.v1.json`.
6. Git branch: `audit/oam-skyrmion-topology-20260812`.

## 7. F_OK / F_GAP / F_NEXT

**F_OK** — primary provenance is strong; topological mechanism independently reproduced at toy level; deterministic output recorded; negative/failure test preserved.

**F_GAP** — public raw data, exact experimental realizations, full stochastic-channel reproduction, hardware replication and RAFAELIA equivalence remain unresolved.

**F_NEXT** — highest-information next step is the full seeded turbulence-channel simulation plus grid/lattice convergence. If exact authors' raw data become available, independent reanalysis outranks further analogy-building.

`TOKEN_VAZIO` is preserved wherever evidence is absent; no missing observation is converted into a conclusion.
