# AGENTS.md — Mapa — Federated Control Plane Router

## Federation entry

This repository is the RAFAELIA **federated control plane & knowledge organization**. Enter through authority mapping and contracts, not through repository crawl or broad search.

Federated role: **authority mapper, state curator, and cross-repository router** for 6 producer repositories:
1. termux-packages (source authority)
2. termux-app-rafacodephi (build + runtime authority)
3. rafpolimata (compiler authority)
4. rafgittools (versioning authority)
5. llamarafaelia (model authority)
6. mapa (this repo: federation + validation authority)

Detailed protocol: `docs/AGENTES.md` (inherited from RafPolimata)

### Mandatory service preflight — Q01..Q12

Before mutating or promoting federation state, answer with exact pointers or typed `TOKEN_VAZIO`:

1. **Quem sou?** — Federated control plane agent + knowledge organization curator
2. **Qual repo/ref/path/hash estou lendo?** — Exact commit, repository, claim origin, and evidence scope
3. **Qual minha autoridade?** — Mapa owns federated routing, state reconciliation, and gap documentation; each repo owns its domain (source/build/runtime/versioning/models)
4. **Qual minha fronteira?** — Claims from producer repos remain tied to that repo's evidence; Mapa validates coherence and federation, not individual implementation proof
5. **Quais índices locais devo abrir?** — Operational ontology, authority pyramid, lineage schema, federated topology, relevant audit trail
6. **Qual rota/agente no produtor corresponde?** — Explicit producer route + commit + gate, or typed `TOKEN_VAZIO`
7. **Que lacunas já existem?** — Documented TOKEN_VAZIO (12 instances), unresolved dependencies, cross-repo handoff gaps
8. **Qual evidência é atual?** — Source commit, gate that produced it, timestamp, schema version, scope/staleness assessment
9. **Qual gate posso executar?** — Lineage validation, topology check, deduplication audit, federation coherence with falsifier
10. **Quando devo parar?** — Stop on authority boundary, security/privacy block, stale evidence, or unresolved producer dependency
11. **Onde registro o delta?** — Federated state file + audit trail; cross-repo deltas routed to producer; reconciliation receipt appended
12. **Quais regras de governança, dados, privacidade e segurança?** — Classify before mutation; TOKEN_VAZIO not erased; security/privacy claims inherited from producers

### Local governance/data/privacy/security defaults

- **Governance:** Federation state, authority assignments, handoff contracts are local authority. Producer handoff cannot be promoted from Mapa alone; must retain link to producer + gate.
- **Data:** Ontology records, lineage IDs, audit trails must have explicit schema and immutable identity. Cross-repository evidence requires source repo authority.
- **Privacy:** Federation records contain hashes, versions, structured metadata, and scope bounds — not credentials, device identifiers, user data, or unrelated environment. Unknown sensitivity blocks federation edge publication.
- **Security:** Authority pyramid, lineage validation, deduplication rules, cross-repo handoff contracts, and producer dependency chains are security surfaces. Authority conflicts, circular dependencies, or unresolved lineage fail closed.

Sequence:

`bind exact producer commit → federated authority boundary → local state indices → producer route resolution → open TOKEN_VAZIO gaps → cross-repo validation → falsifier/gate → federation closure → append immutable receipt → recompute topology`

## Local role and entry routes

**Role:** Route cross-repository claims, maintain authority pyramid, document TOKEN_VAZIO, and drive federation to FEDERATION_CERTIFIED state from current VERIFICATION_PENDING.

Start with:

- `README.md` (five-layer architecture)
- `AGENTS.md` (this file)
- `CLAUDE.md` (Claude Code adapter)
- `data/control-plane/RAFAELIA_AUTHORITY_PYRAMID_FAIL_CLOSED_V1.json` (authority mapping)
- `data/ontology/rafaelia-operational-ontology.v1.json` (concepts, relations, TOKEN_VAZIO)
- `auditoria/federated-doctor-pass-20260821/OBSERVACAO-FINAL.md` (current state audit)
- The specific producer route/claim/gate being reconciled

## Critical truth corrections

### TOKEN_VAZIO is NOT zero

12 documented gaps (as of 2026-08-21 audit) across all categories.

```yaml
TV-CODE:         2  # DAG causal engine, Bootstrap UQ
TV-TEST:         2  # Log-log benchmark, Fractal dimension
TV-DATA:         2  # Vector corpus, Calibration weights
TV-INDEPENDENCE: 2  # Lineage authority, Dedup rules
TV-BOUNDARY:     1  # Antiderivative boundary condition
TV-ACCESS:       1  # Vector corpus access control
```

**Do NOT:**
- Erase TOKEN_VAZIO without implementing + executing the corresponding gate
- Promote stale producer evidence to federation state without reconciliation
- Hide dependencies between repos to make topology look complete

**DO:**
- Preserve all TOKEN_VAZIO with closure path/cycle/owner
- Link every federation claim to source repo + commit + gate that produced it
- Record deltas when producer evidence is younger/older than federation snapshot

### Fixture ≠ current state

`ECOSYSTEM_RUNTIME_STATE.json` is a versioned snapshot. If `observed_at` < HEAD of any producer, record reconciliation delta.

```text
fixture:         point-in-time measurement
config:          user-provided input
workflow:        build process
local execution: this machine
          ALL ≠ cross-repository current truth
```

### Authority boundaries

Each repository owns its domain:
- **termux-packages:** source verification, recipe correctness, package handoff
- **termux-app-rafacodephi:** build artifact, binary correctness, runtime behavior
- **rafpolimata:** compiler validation, AArch64 instruction correctness
- **Mapa:** federation routing, authority coherence, cross-repo validation

Do NOT:
- Promote producer implementation detail into federation claim (e.g., "42 fixed-point attractors" from implementation parameter)
- Bypass producer authority to directly validate internal implementation
- Claim evidence when producer has TOKEN_VAZIO on that same claim

DO:
- Link federation claim to producer's gate that closes it
- Respect producer's TOKEN_VAZIO — inherit it into federation state
- Record producer dependencies explicitly (e.g., "termux-app BUG-02 decision blocks Mapa TV-CODE closure")

## States and transitions

| State | Meaning | Allowed Next |
|-------|---------|---|
| `REFERENCE` | Specification/explanatory | IMPLEMENTED |
| `IMPLEMENTED` | Code/data exists | PASS / FAIL / TOKEN_VAZIO |
| `PASS` | Named gate executed, passed | (immutable; may have TOKEN_VAZIO companions) |
| `FAIL` | Named gate executed, failed | Fix + re-run, or BLOCKED |
| `TOKEN_VAZIO` | Evidence absent/insufficient | Implement gate + PASS, or accept as permanent |
| `VERIFICATION_PENDING` | Federation state incomplete | Close TOKEN_VAZIO → FEDERATION_CERTIFIED |
| `FEDERATION_CERTIFIED` | All cross-repo gates pass | (immutable until new TOKEN_VAZIO documented) |

**Do NOT transition without evidence.** No state should change without a recorded gate execution.

## Working rules

- Work on a non-protected branch (`claude/termux-package-bugs-gaps-sr2o1c` or equivalent per plan)
- Do not merge without explicit human authorization
- Keep changes scoped; federation cleanup belongs in separate work
- Never erase TOKEN_VAZIO without implementing + executing the corresponding gate
- Never edit generated outputs in `docs/generated/` or `results/` by hand; change source + regenerate
- Never expose detected secrets; record only detector + masked result for audit
- Preserve rollback and immutability when moving/replacing/deleting federated records
- Do not silently change schemas, lineage IDs, authority assignments, or handoff contracts

## Before editing

Record or inspect:

```sh
git branch --show-current
git rev-parse HEAD
git status --short

# Current federation state:
cat auditoria/federated-doctor-pass-20260821/OBSERVACAO-FINAL.md

# Ontology state:
cat data/ontology/rafaelia-operational-ontology.v1.json | python3 -m json.tool | head -100
```

Identify:

- Task class: federation/governance/documentation/research
- Source repo(s) affected
- TOKEN_VAZIO being addressed
- Applicable gates/validators
- Unavailable tools/external repos as `TOKEN_VAZIO`

## Subsystem minimums

### Federation ontology

Read `data/ontology/rafaelia-operational-ontology.v1.json` before editing concepts, relations, or epistemic states.

Preserve semantic distinctions:
- `similar_to` ≠ `depends_on` ≠ `implements` ≠ `tests` ≠ `falsifies`

### Cross-repo tracing

Before linking producer evidence to federation claim, verify:
- Producer repo + commit present
- Gate that produced evidence documented + exit code recorded
- Scope (local/physical/third-party) explicit
- Staleness (if any) reconciled against HEAD

### Lineage authority (TV-INDEPENDENCE)

When defining deduplication rules or source independence, consult:
- Each repo's authority pyramid
- Producer handoff contracts
- Federated topology (6 repos in TOROID)

### Topological validation (Cycle 6)

Run federation coherence checks:

```sh
python3 scripts/validate_federation_topology.py --repos 6 --check
python3 scripts/compare_cross_source_evidence.py --lineage-check
```

## Gates and closure sequence

### Cycle 4 (Implementations + fixtures)
- Close TV-CODE (DAG causal, Bootstrap UQ)
- Freeze TV-DATA fixtures (4 files with SHA-256)
- Implement TV-TEST gates

### Cycle 5 (Federation backbone)
- Define TV-INDEPENDENCE (lineage authority + dedup rules)
- Validate cross-repo deduplication

### Cycle 6 (Topological certification)
- Validate 6-repo TOROID topology
- Cross-repo tracing complete
- Promote VERIFICATION_PENDING → FEDERATION_CERTIFIED

## Evidence discipline

Cross-repository receipt must capture:

```text
repository + commit (source of truth)
producer role (who owns this claim)
gate identifier (which validation produced it)
execution timestamp
environment/architecture (where it ran)
exit code + pass/fail
evidence scope (local/device/third-party)
staleness/reconciliation delta (if any)
immutable hash (integrity)
```

Promotion scope: **Limited to what the gate actually demonstrated in that scope.**

## Session close

End work with:

```text
F_ok   = what was actually changed/executed/demonstrated
F_gap  = what remains unknown, blocked, contradicted or unexecuted
F_next = smallest reproducible next action
```

**Important:** Preserve all TOKEN_VAZIO and federation blockers. Do not invent merit to make F_ok look complete.
