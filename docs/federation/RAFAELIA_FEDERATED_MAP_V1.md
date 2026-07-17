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

Each coordinate uses an ordinal weight only after evidence collection:

- `0`: directly established absence;
- `1`: declared or structurally present;
- `2`: locally tested for a named commit/artifact;
- `3`: independently reproduced or externally validated within its domain;
- `TOKEN_VAZIO`: not measured, inaccessible or insufficiently specified.

Weights are **status indicators**, not value judgments and not interchangeable across domains. A formal proof weight cannot substitute runtime evidence; a successful build cannot substitute scientific validation.

## Initial repository vectors

No numeric baseline is assigned by documentation reading alone. Every coordinate begins as `TOKEN_VAZIO` until a measurement record identifies the repository commit, source path, command, artifact and timestamp.

| Repository | Evidence | Reproducibility | Runtime | Formal rigor | Privacy | Reversibility |
|---|---|---|---|---|---|---|
| RafGitTools | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO |
| Vectras-VM-Android | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO |
| termux-app-rafacodephi | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO |
| RafPolimata | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO |
| GAIA_phi | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO |
| ZIPRAF_OMEGA_FULL | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO |
| llamaRafaelia | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO |
| Rafaelia_Private | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO |
| ChipQuantum | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO |
| Matem-tica- | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO |
| relativity-living-light | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO |

## Measurement record

A coordinate may change from `TOKEN_VAZIO` only with a record containing:

```yaml
repository: owner/name
commit: exact-sha
coordinate: evidence | reproducibility | runtime | formal_rigor | privacy | reversibility
weight: 0 | 1 | 2 | 3
source_path: exact/path
command_or_method: exact command or review method
artifact: path/hash/URL identifier
timestamp: ISO-8601
limitations: explicit limits
reviewer_or_runner: human, CI runner or device identity
```

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
7. No coordinate receives a numeric weight from README language alone.

## Friendly operator path

```text
1. Choose the concrete need in Primary routes.
2. Open the owner repository's local contract/status.
3. Capture commit, path, command and expected artifact.
4. Run the smallest gate.
5. Record F_ok, F_gap, F_next and rollback_anchor.
6. Create the measurement record.
7. Update the control-plane status and regenerate this projection.
```

## Rollback

This map is documentation only. Rollback is closing/reverting its PR. It cannot roll back code or evidence in another repository; follow that repository's local rollback anchor.
