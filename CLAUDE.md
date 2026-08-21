# CLAUDE.md — Claude Code adapter for Mapa

@AGENTS.md (to be created)
@docs/AGENTES.md (reference: RafPolimata)
@README.md
@auditoria/federated-doctor-pass-20260821/OBSERVACAO-FINAL.md

This file is a Claude Code adapter, not a second source of architectural truth.
The repository-wide contract is `AGENTS.md` (federated governance); detailed protocol is in `docs/AGENTES.md` (from RafPolimata).

## Session start

Before editing:

1. Read `AGENTS.md` and `README.md` for repository mission and five-layer architecture.
2. Read `auditoria/federated-doctor-pass-20260821/OBSERVACAO-FINAL.md` for current TOKEN_VAZIO state.
3. Inspect branch, HEAD and working tree:
   ```sh
   git branch --show-current
   git rev-parse HEAD
   git status --short
   ```
4. Identify TOKEN_VAZIO gaps (12 documented in audit trail) and their dependency chains.
5. Do not merge without explicit human authorization.

## Project orientation

Mapa is the federated knowledge organization and control plane for the RAFAELIA ecosystem (6 repositories):

1. **termux-packages** — source authority
2. **termux-app-rafacodephi** — build + runtime authority
3. **Mapa** — federation + validation authority (this repo)
4. **rafpolimata** — compiler authority
5. **rafgittools** — versioning authority
6. **llamarafaelia** — model authority

**Five-layer architecture:**
- Layer 1: Biblioteconomic KOS (cataloging, vocabulary, authority control)
- Layer 2: Operational ontology (concepts, relations, trajectories, gaps)
- Layer 3: Federated control plane (modules, products, procedures, gates)
- Layer 4: Evidence and custody (typed pointers, checksums, audit trails)
- Layer 5: Visual navigation (diagrams, indices, reports)

**Do not reduce Mapa to one subsystem.** Cross-repository federation requires layer-by-layer coherence.

## Critical truth corrections

### TOKEN_VAZIO vs. VERIFICATION_PENDING

**Current state (as of 2026-08-21 audit):**

```yaml
control_plane_state: VERIFICATION_PENDING  # not FEDERATION_CERTIFIED
claim_allowed: false                       # fail-closed by default
```

**12 documented TOKEN_VAZIO instances:**

| Gap Class | Count | Examples | Cycle |
|-----------|-------|----------|-------|
| **TV-CODE** | 2 | DAG causal engine, Bootstrap UQ | 4 |
| **TV-TEST** | 2 | Log-log benchmark, Fractal dimension null models | 4 |
| **TV-INDEPENDENCE** | 2 | Lineage authority, Dedup rules | 5 |
| **TV-DATA** | 2 | Vector corpus frozen, Calibration weights blocked | 4 |
| **TV-BOUNDARY** | 1 | Antiderivative boundary condition schema | 4 |
| **TV-ACCESS** | 1 | Vector corpus access control | 4 |

**Closure path to FEDERATION_CERTIFIED:**
1. **Cycle 4:** Implement TV-CODE (DAG causal, Bootstrap UQ), freeze TV-DATA fixtures
2. **Cycle 5:** Define TV-INDEPENDENCE (lineage authority, dedup rules)
3. **Cycle 6:** Cross-repo tracing + topological validation (6 repos in TOROID)

### Do NOT confuse fixture state with current truth

**ECOSYSTEM_RUNTIME_STATE.json is a snapshot**, not live state.

```text
fixture (!= current
config   (!= executed
workflow (!= remote gate PASS
local    (!= cross-repository evidence
```

If `observed_at` in a fixture is older than HEAD, record the delta. Do not automatically promote stale snapshots to current state.

### Do NOT claim "42 fixed-point attractors"

Correct: "42-state phase space in termux-app-rafacodephi (reference implementation)"  
Incorrect: "Proven mathematical attractor theorem"

Cross-repository claims inherit the evidence boundaries of each source. If termux-app-rafacodephi has TOKEN_VAZIO on attractor_table (BUG-01), Mapa cannot claim it as validated federation evidence.

### Evidence separation

```text
REFERENCE    = specification/explanatory material
IMPLEMENTED  = code exists
PASS         = named gate executed and passed in declared scope
FAIL         = named gate executed and failed
TOKEN_VAZIO  = evidence absent/insufficient/stale/inaccessible
```

Preserve all four states. Do not erase TOKEN_VAZIO without implementing the gate.

## Coding discipline

- **Bounds checks:** Schema offsets, buffer limits, array indices explicit
- **Error paths:** NULL/lookup errors explicit; no silent fallbacks
- **Ontology coherence:** Concepts must remain semantically distinct (e.g., `similar_to` ≠ `depends_on`)
- **Signature binding:** Lineage IDs must be immutable; dedup rules must be reversible
- **Gate failures:** Never suppress with `|| true`; preserve evidence trails
- **Cross-repo tracing:** All claims must link to source repository + commit + gate that produced them

## Documentation discipline

When editing prose:

- Distinguish REFERENCE, IMPLEMENTED, PASS, FAIL, TOKEN_VAZIO
- Bind PASS statements to the specific repo/commit/gate that produced them
- Label heuristic claims separately from executed-gate claims
- Update stale onboarding when cycles have superseded earlier text
- Prefer canonical statements + links over duplicated instructions
- **Never erase documented TOKEN_VAZIO without closure evidence**

## Federation gates (reference)

### Cycle 4 (Implementations + frozen fixtures)
```sh
python3 -m unittest tests.test_dag_causal               # TV-CODE: DAG engine
python3 -m unittest tests.test_bootstrap_uq             # TV-CODE: Bootstrap UQ
python3 scripts/validate_fixtures.py --check            # TV-DATA: frozen checksums
```

### Cycle 5 (Cross-repo federation)
```sh
python3 scripts/validate_lineage_authority.py --check   # TV-INDEPENDENCE: lineage
python3 scripts/compare_cross_source_evidence.py        # Dedup validation
```

### Cycle 6 (Topological validation)
```sh
python3 scripts/validate_federation_topology.py --repos 6 --check
```

## Invariants (non-negotiable)

```text
TOKEN_VAZIO != 0
fixture != live state
heuristic != proof
analogy != mechanism
commit != execution
merge != remote gate PASS
local_path != cross_repository_evidence
claim_allowed = false until corresponding gate closes
```

## Useful entrypoints

```sh
# Ground truth on current federation state:
cat README.md
cat auditoria/federated-doctor-pass-20260821/OBSERVACAO-FINAL.md

# Operational ontology:
cat data/ontology/rafaelia-operational-ontology.v1.json

# Authority mapping:
cat data/control-plane/RAFAELIA_AUTHORITY_PYRAMID_FAIL_CLOSED_V1.json

# Lineage (to be implemented):
cat data/control-plane/lineage_authority_v1.json  # TOKEN_VAZIO until Cycle 5
```

## Handoff

Finish with:

```text
F_ok   = what was actually changed/executed/demonstrated
F_gap  = what remains unknown, blocked, contradicted or unexecuted
F_next = smallest reproducible next action
```

**Important:** TOKEN_VAZIO and cross-repository evidence gaps remain visible. Do not hide federation blockers.
