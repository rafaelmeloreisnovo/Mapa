# RAFAELIA Catalog Run — 2026-08-04T1003Z

State: incremental · append-only · non-destructive · `claim_allowed=false`

Checkpoint: `Mapa@4b411f73a59f67070a895fee929f4a9f5ff19938`

Canonical reference: **RAFAELIA — Implementação Latentes e Papers — Drive GitHub V1** (`1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88`).

## New navigable surfaces

### GGML and compute backends

- `ggml` — `1EzIQ11QVWBHod6YSp-CAUU8H2jL8f7NB`
  - `src` — `1B_827MYIH6mD-9XZb4f1GYD80hnZVwJC`
  - `CMakeLists.txt` — `1NDw_Tp9796vZTOIF8Hc8RjcLfrjapVXi` — 19,043 bytes
- Vulkan: `ggml-vulkan` → `vulkan-shaders`
- WebGPU: `ggml-webgpu` → `wgsl-shaders`
- Other observed families: `ggml-zdnn`, `gguf`, `gguf-py`, `grammars`, `tests`, `examples`, `scripts`.

### GPU feature probes

`feature-tests` (`1H400lFzsWMyX3Lx1fNPqNxPxu2zWcQD-`):

- `coopmat.comp` — 78 bytes
- `coopmat2.comp` — 78 bytes
- `integer_dot.comp` — 79 bytes

These files are cataloged as test inputs only. No compilation or GPU execution was observed.

### NOVOexport index package

- Folder: `NOVOexport_INDEX` — `1_AVO3UWZU7r469YS06SnXoI5dZaH1v_l`
- Artifact: `NOVOexport_INDEX_v1.zip` — `1dn4XaKBBzhms1FSO5kBit5b4fCGD6yvt`
- MIME: `application/zip`
- Size: 437,367 bytes

The ZIP was not opened, exported or hashed in this cycle.

## Semantic routes

| Question | Route |
|---|---|
| Where is the core compute surface? | `ggml/` → `src/` → `CMakeLists.txt` |
| Where are GPU backends? | `ggml-vulkan/`, `vulkan-shaders/`, `ggml-webgpu/`, `wgsl-shaders/`, `ggml-zdnn/` |
| Where are format tools? | `gguf/`, `gguf-py/` |
| Where are validation surfaces? | `tests/`, `feature-tests/`, `grammars/` |
| Where is the export-navigation artifact? | `NOVOexport_INDEX/NOVOexport_INDEX_v1.zip` |

## Claims

- **PROVADO:** enumerated Drive objects, IDs, sizes and MIME metadata exist.
- **EVIDENCIADO:** names and build anchors are consistent with a GGML source tree and multiple compute backends.
- **HIPÓTESE:** the tree can become a complete navigable code catalog after byte-level inventory.
- **MODELO_ANALÓGICO:** backend families form a portability map.
- **REFUTADO:** folder names, shaders or a CMake file alone prove compilation or runtime.
- **TOKEN_VAZIO:** exact upstream/revision, licenses, dependency versions, SHA-256, CI, device execution and ZIP integrity.

## F_ok

Reference read; incremental delta isolated; provider IDs preserved; GGML/GPU and NOVOexport families indexed; no producer commit recataloged.

## F_gap

Root/upstream unresolved; complete file inventory absent; Drive hashes absent; licenses/dependencies unresolved; build/runtime receipts absent; ZIP integrity unverified.

## F_next

Resolve upstream and root parent → read README/CMake manifests → inventory by parent/type/size → export and SHA-256 → map dependencies/tests → inspect ZIP safely → append successor receipt.

## Receipt

`data/catalog_runs/RAFAELIA_CATALOG_CYCLE_2026-08-04T1003Z.json`
