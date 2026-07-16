# RAFAELIA Federated Repository Map v1

**Role:** human-readable navigation projection.  
**Machine source of truth:** `rafaelmeloreisnovo/RafGitTools/configs/rafaelia-federation.json`.  
**Rule:** this map may explain routes; it must not override repository-local status or the control-plane manifest.

## Sustaining path

```text
expression
  -> atomic claim
  -> owner repository
  -> source path/commit
  -> implementation or proof
  -> test/falsifier
  -> evidence artifact
  -> decision
  -> rollback anchor
```

## Primary routes

| Need | Enter through | Then route to | Exit evidence |
|---|---|---|---|
| Operate GitHub/Android app | `RafGitTools` | repository-specific contract | PR, commit, CI/test artifact |
| Boot VM on Android | `Vectras-VM-Android` | `termux-app-rafacodephi`, `qemu_rafaelia` | preflight + guest boot evidence |
| Local shell/runtime | `termux-app-rafacodephi` | `UserLAnd` only as bounded availability failover | device smoke + package/backend gates |
| Classify a broad statement | `RafPolimata` | exact owner repository | atomic claim record |
| Index/store evidence | `GAIA_phi` | `ZIPRAF_OMEGA_FULL` for bounded serialization | manifest digest + source commit |
| Run local model | `llamaRafaelia` | `TinyGPT` only as interface failover | runtime/model/tokenizer/config hashes |
| Store restricted evidence | `Rafaelia_Private` | encrypted/immutable backup under same policy | opaque receipt + audit entry |
| Low-level kernel/crypto/geometry | `ChipQuantum` | `Matem-tica-` for formal proof fragments | strict build/test/vector artifacts |
| Formal theorem/proof | `Matem-tica-` | `RafPolimata` for routing; `ChipQuantum` for finite tests | proof commit + verifier output |
| Scientific RLL claim | `relativity-living-light` | real-data workflow + GAIA evidence storage | claim ledger + dataset/result hashes |

## Vector model

Each route is described by the vector:

```text
v = (evidence, reproducibility, runtime, formal_rigor, privacy, reversibility)
```

Each coordinate uses an ordinal weight:

- `0`: absent / `TOKEN_VAZIO`;
- `1`: declared or structurally present;
- `2`: locally tested;
- `3`: independently reproducible or externally validated within its domain.

Weights are **status indicators**, not value judgments and not interchangeable across domains. A formal proof weight cannot substitute runtime evidence; a successful build cannot substitute scientific validation.

## Repository vector expectations

| Repository | Evidence | Reproducibility | Runtime | Formal rigor | Privacy | Reversibility |
|---|---:|---:|---:|---:|---:|---:|
| RafGitTools | 2 | 2 | 2 | 1 | 2 | 3 |
| Vectras-VM-Android | 2 | 2 | 2 | 1 | 2 | 3 |
| termux-app-rafacodephi | 2 | 2 | 1 | 1 | 2 | 3 |
| RafPolimata | 2 | 2 | 1 | 2 | 2 | 3 |
| GAIA_phi | 2 | 2 | 2 | 1 | 2 | 3 |
| ZIPRAF_OMEGA_FULL | 2 | 2 | 1 | 1 | 2 | 3 |
| llamaRafaelia | 1 | 1 | 1 | 1 | 2 | 2 |
| Rafaelia_Private | 2 | 1 | 1 | 1 | 3 | 3 |
| ChipQuantum | 2 | 2 | 2 | 2 | 2 | 3 |
| Matem-tica- | 2 | 2 | 1 | 2 | 2 | 3 |
| relativity-living-light | 2 | 2 | 1 | 2 | 2 | 3 |

These initial values are `DECLARED_MAP_BASELINE`. They must be regenerated from repository evidence before being called current. A missing measurement is reduced to `0`, never guessed upward.

## Edge semantics

- `depends_on`: execution cannot complete without the target.
- `validates_with`: target provides an independent proof/test layer.
- `stores_in`: target stores/indexes evidence without validating meaning.
- `fails_over_to`: target preserves bounded availability without inheriting claims.
- `governed_by`: target defines routing/claim rules but not local implementation truth.

## Anti-inference rules

1. Similar terminology does not create an edge.
2. A link does not prove compatibility.
3. A failover does not inherit claims.
4. “Latest” requires commit/timestamp evidence.
5. Missing source path/command/artifact is `TOKEN_VAZIO`.
6. Public navigation never exposes private payloads.

## Friendly operator path

```text
1. Choose the concrete need in Primary routes.
2. Open the owner repository's local contract/status.
3. Capture commit, path, command and expected artifact.
4. Run the smallest gate.
5. Record F_ok, F_gap, F_next and rollback_anchor.
6. Update the control-plane manifest/status; regenerate this projection.
```

## Rollback

This map is documentation only. Rollback is closing/reverting its PR. It cannot roll back code or evidence in another repository; follow that repository's local rollback anchor.
