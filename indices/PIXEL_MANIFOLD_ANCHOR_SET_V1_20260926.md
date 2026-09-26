# Pixel Manifold Anchor Set V1 — 2026-09-26

Status: `SPEC + SESSION_POC + MANUAL_VISUAL_ANCHORS`  
Claim gate: `claim_allowed=false`

## Authority

- `Mapa` owns this schema, validation fixture, semantic relations and federation state.
- Runtime implementation remains `TOKEN_VAZIO` until routed to an executor/producer.
- Source image bytes are not committed to this public repository.
- Private provider/Drive locators are intentionally absent.

## What this delta adds

- 10 immutable source identities by SHA-256 + dimensions only.
- 22 normalized visual regions.
- 13 positive and 13 negative cross-image visual-motif anchor pairs.
- Current `PIXEL_DESC_V1` Jaccard observations attached to each pair.
- Fail-closed validator with adversarial self-tests.
- T1..T6 gate matrix with T1 explicitly unresolved because source bytes are outside the repository.

## Baseline diagnostic

- positive mean Jaccard: `0.103884034589`
- negative mean Jaccard: `0.053529364131`
- pairwise rank AUC: `0.751479289941`
- acceptance threshold: `TOKEN_VAZIO_NOT_TUNED`

The AUC is a diagnostic on this tiny manually curated set, **not an accuracy claim**. The positive wireframe-cube pair currently scores 0.0 under the palette/texture descriptor. That is useful negative evidence: `PIXEL_DESC_V1` does not capture all shape identity, so V1 intentionally does not tune a decision threshold.

## Gate

```bash
python3 -m py_compile scripts/validate_pixel_manifold_anchor_set.py
python3 scripts/validate_pixel_manifold_anchor_set.py \
  --artifact data/multimodal/pixel_manifold_anchor_set.v1.json \
  --self-test
```

Expected bounded result:

- `T1 = TOKEN_VAZIO_SOURCE_BYTES_NOT_IN_REPOSITORY`
- `T2 = PASS_STATIC`
- `T3..T6 = PASS_STRUCTURAL`
- `claim_allowed = false`

## F_gap / F_next

`F_gap`: external labeled ground truth, runtime producer, physical ARM execution, and source-byte reproduction outside session remain open.

`F_next`: freeze `PIXEL_DESC_V1`. Build a successor shape/topology descriptor only if it improves this fixed anchor set without relabeling the benchmark or copying private source bytes.
