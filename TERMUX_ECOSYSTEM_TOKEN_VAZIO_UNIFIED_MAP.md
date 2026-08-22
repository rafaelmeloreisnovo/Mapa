# Mapa Unificado de TOKEN_VAZIO — RAFAELIA Ecosystem

**Data:** 2026-08-21  
**Escopo:** termux-packages, termux-app-rafacodephi, Mapa (6-repo federation)  
**Objetivo:** Documentar e priorizar todos TOKEN_VAZIO para closure ordenado

---

## CRÍTICO (P0 - Bloqueadores de ciclo)

### termux-packages P0 (9 itens) — Ciclo 2

| ID | Componente | Descrição | Ciclo | Bloqueador de |
|----|-----------|-----------|-------|---|
| TV-01 | SOURCE_FETCH | Real download + SHA-256 verification | 2 | TV-02, TV-03, TV-05 |
| TV-02 | SOURCE_EXTRACT | Safe tarball extraction + tree validation | 2 | TV-04, deps |
| TV-03 | PATCH_APPLY | Patch application com hash binding | 2 | build integrity |
| TV-04 | MANIFEST_BINDING | Manifesto V2 com offsets/bounds checking | 2 | package lookup |
| TV-05 | DEP_GRAPH | Real dependency resolution from manifest | 2 | build order |
| TV-06 | ARMV7_ELF | Physical ARM32 build no device + readelf | 3 | D8 gate |
| TV-07 | AARCH64_ELF | Physical ARM64 build no device + readelf | 3 | D8 gate |
| TV-13 | CI_GATE | GitHub Actions observable steps + artifacts | 5 | handoff proof |
| TV-20 | SECURITY | Path injection + shell escape tests | 2 | build safety |

### termux-app-rafacodephi Critical (4 itens) — Ciclo 3

| ID | Componente | Descrição | Ciclo | Bloqueador de |
|----|-----------|-----------|-------|---|
| BUG-02 | VOID #22 paradox | Attractor #22 state encoding unresolvable | 3 | BUG-01 |
| BUG-01 | attractor_table | 40/42 missing; depends on BUG-02 choice | 3 | BUG-03, BUG-08 |
| BUG-05 | ZrManifest stack | 59KB on 1MB stack = overflow risk | 2 | release safety |
| BUG-03 | vectra_pulse.S | 4 AArch64 ASM bugs | 3 | runtime proof |

### Mapa Critical (6 itens) — Ciclo 4-5

| ID | Classe | Descrição | Ciclo | Bloqueador de |
|----|--------|-----------|-------|---|
| TV-CODE-1 | DAG_CAUSAL | DAG causal engine (association vs. mechanism) | 4 | TV-TEST, validation |
| TV-CODE-2 | BOOTSTRAP_UQ | Bootstrap + uncertainty quantification | 4 | TV-DATA, model comparison |
| TV-INDEPENDENCE-1 | LINEAGE_AUTHORITY | lineage_id schema + authority mapping | 5 | federation cert |
| TV-INDEPENDENCE-2 | DEDUP_RULES | Cross-repo deduplication rules | 5 | federation cert |
| TV-TEST-1 | LOG_LOG_BENCHMARK | Log-log model comparison fixture | 4 | TV-CODE-1 validation |
| TV-TEST-2 | FRACTAL_NULL | Fractal dimension null models fixture | 4 | TV-CODE-2 validation |

---

## IMPORTANTE (P1 - Não bloqueadores de ciclo)

### termux-packages P1

| ID | Componente | Descrição | Impacto |
|----|-----------|-----------|--------|
| TV-08 | ANDROID_API29 | Device execution on Android API 29 | Cycle 3 compatibility |
| TV-09 | MOTO_E7 | Device execution on Moto E7 (ARM32) | Cycle 3 baseline |
| TV-10 | REALME | Device execution on Realme (ARM64) | Cycle 3 baseline |
| TV-15 | PKG_INSTALL | dpkg installation on device | Cycle 4 ops |
| TV-16 | PKG_REMOVE | dpkg removal + cleanup on device | Cycle 4 ops |
| TV-19 | PROVENANCE | Commit + source + binary hash binding | Cycle 2 audit |

### termux-app-rafacodephi P1

| ID | Componente | Descrição | Impacto |
|----|-----------|-----------|--------|
| BUG-04 | PACKAGE_HARDCODE | com.termux hardcoded → configurable | Release config |
| BUG-06 | RACE_CONDITION | CtiScanner race condition + sync barrier | Concurrency safety |
| BUG-07 | BLAKE3_SILENT | BLAKE3 mismatch silent → exit(1) | Build integrity |
| BUG-08 | LYAPUNOV_INVALID | φ = (1-H)·C not validated at gates | Invariant assertion |

### Mapa P1

| ID | Classe | Descrição | Impacto |
|----|--------|-----------|--------|
| TV-DATA-1 | VECTOR_CORPUS | Vector corpus frozen + checksummed | Fixture reproducibility |
| TV-DATA-2 | CALIBRATION | Calibration weights + blocked benchmark | Model reproducibility |
| TV-BOUNDARY | ANTIDERIVATIVE | Antiderivative boundary condition schema | Integration constant recovery |
| TV-ACCESS | CORPUS_ACCESS | Vector corpus access control contract | Data governance |

---

## CADEIA DE DEPENDÊNCIAS

### Critical Path: Bloqueadores em cascata

```
termux-packages:
  TV-01 (SOURCE_FETCH)
    → TV-02 (SOURCE_EXTRACT)
      → TV-03 (PATCH_APPLY)
        → TV-04 (MANIFEST_BINDING)
          → TV-05 (DEP_GRAPH)
            → TV-06/07 (DEVICE BUILD)

termux-app-rafacodephi:
  BUG-02 (VOID #22 decision)
    → BUG-01 (attractor_table)
      → BUG-03 (vectra_pulse.S)
        → BUG-08 (lyapunov validation)

Mapa:
  TV-CODE (DAG causal, Bootstrap UQ)
    → TV-TEST (fixtures)
      → TV-INDEPENDENCE (lineage)
        → FEDERATION_CERTIFIED
```

### Cross-repo dependencies

```
termux-packages TV-01..05 (Ciclo 2)
  ↓
termux-app BUG-01/03 (Ciclo 3)
  ↓
Mapa TV-CODE (Ciclo 4)
  ↓
Federation topology (Ciclo 6)
  ↓
FEDERATION_CERTIFIED
```

**Critical decision point:** BUG-02 (BUG-02 choice) blocks BUG-01 which blocks Mapa validation chain.

---

## PRIORIZAÇÃO EXECUTÁVEL

### Week 1 (Dias 1-7): FASE 1 BOOTSTRAP

**Semana de:** 2026-08-21 (atual)

- **Dia 1-3:** Create CLAUDE.md (3 repos) + AGENTS.md (Mapa)  ✅ CONCLUÍDO
- **Dia 3-4:** BUG-02 decision (human authorization required)
- **Dia 4-7:** TV-01..05 prep (structure test fixtures, download verification schema)

**Gate:** All CLAUDE.md files created and committed; AGENTS.md in Mapa functional

### Week 2 (Dias 8-14): FASE 2 CICLO 2

**Semana de:** 2026-08-28

- **Dia 8-10:** Implement TV-01 (source_download.c real) + TV-02 (safe extraction)
- **Dia 11-12:** Close TV-03, TV-04, TV-05 gates
- **Dia 13-14:** BUG-04, BUG-05, BUG-07 fixes (parallel)

**Gate:** `make cycle2-source-gate` PASS; 5 test packages validated

### Week 3 (Dias 15-21): FASE 3 BUG RESOLUTION

**Semana de:** 2026-09-04

- **Dia 15-16:** BUG-01 completion (2 attractors from BUG-02 decision)
- **Dia 17-18:** BUG-03 fix (4 AArch64 issues)
- **Dia 19-21:** BUG-08 validation (Lyapunov assertion)

**Gate:** `make attractor-table-complete-gate` PASS; `make aarch64-vectorpulse-gate` PASS

### Week 4 (Dias 22-28): FASE 4 MAPA IMPLEMENTATIONS

**Semana de:** 2026-09-11

- **Dia 22-24:** TV-CODE implementations (DAG causal, Bootstrap UQ)
- **Dia 25-26:** TV-DATA fixtures frozen (4 files + SHA-256)
- **Dia 27-28:** TV-BOUNDARY schema + TV-TEST gates

**Gate:** `python3 -m unittest tests.test_dag_causal` PASS

### Week 5 (Dias 29-35): FASE 5 FEDERATION

**Semana de:** 2026-09-18

- **Dia 29-31:** TV-INDEPENDENCE implementation (lineage authority)
- **Dia 32-33:** Cross-repo dedup audit
- **Dia 34-35:** Topology validation (6 repos)

**Gate:** `python3 scripts/validate_federation_topology.py --repos 6 --check` PASS

### Week 6 (Dias 36-40): FASE 6 PHYSICAL

**Semana de:** 2026-09-25

- **Dia 36-37:** Allocate devices (Moto E7, Realme)
- **Dia 38-39:** D8 gate execution (TV-06, TV-07)
- **Dia 40:** Promote VERIFICATION_PENDING → FEDERATION_CERTIFIED

**Gate:** Device logcat + exit receipt; all gates PASS

---

## ESTRATÉGIA DE CLOSURE

### Por repositório

**termux-packages:**
- Priority: TV-01, TV-02, TV-03, TV-04, TV-05 (Ciclo 2 bloqueador)
- Close in sequence (dependencies strict)
- Device validation (TV-06/07) follows Ciclo 3

**termux-app-rafacodephi:**
- Priority: BUG-02 decision (human gate, prerequisite)
- BUG-01, BUG-03, BUG-08 in sequence (cascata)
- BUG-04, 05, 07 paralelo (independent)

**Mapa:**
- Priority: TV-CODE (DAG, Bootstrap UQ)
- TV-DATA (fixtures), TV-TEST (gates)
- TV-INDEPENDENCE (lineage + federation cert)

### Critérios de sucesso

| Milestone | Criteria | Owner |
|-----------|----------|-------|
| **FASE 1 Complete** | 3× CLAUDE.md created; Mapa/AGENTS.md created | All 3 repos |
| **FASE 2 Complete** | Ciclo 2 gates (TV-01..05) PASS | termux-packages |
| **FASE 3 Complete** | BUG-02 decided; BUG-01/03 fixed; BUG-08 validated | termux-app |
| **FASE 4 Complete** | TV-CODE + TV-DATA + TV-TEST gates PASS | Mapa |
| **FASE 5 Complete** | Cross-repo topology validated; lineage authority defined | Mapa |
| **FASE 6 Complete** | Device receipts collected (arm32 + arm64) | termux-packages + termux-app |
| **FEDERATION_CERTIFIED** | All gates PASS; zero open TOKEN_VAZIO | All 6 repos |

---

## REGRAS DE NÃO-VIOLAÇÃO

1. **Nunca erase TOKEN_VAZIO sem implementação + gate PASS**
2. **Nunca skip gate com `|| true` ou unconditional success**
3. **Nunca ignore cadeia de dependências (BUG-02 → BUG-01 → BUG-03 é obrigatória)**
4. **Nunca promova producer TOKEN_VAZIO para federation claim**
5. **Nunca altere binary layouts ou schema silenciosamente**
6. **Nunca exclua or arquivo sem provenance + rollback**

---

## RASTREAMENTO E REPORTING

**Artefatos de progresso:**
- Commit messages com `F_ok`, `F_gap`, `F_next` format
- Gate execution receipts com timestamp + exit code
- Weekly sync on TOKEN_VAZIO closure state
- PR status linked to phase gates

**Audit trail:**
- `git log` per repo com gate evidence
- `auditoria/` folder in Mapa with dated receipts
- Cross-repo tracing in federated state

---

**Plano criado:** 2026-08-21  
**Próximo checkpoint:** Dia 3 (CLAUDE.md + AGENTS.md merged)
