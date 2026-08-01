# RAFAELIA — Catálogo Operacional — Ciclo 2026-07-31 23:44 BRT

Status: `EXECUTED_NON_DESTRUCTIVE`  
Branch: `automation/catalog-cycle-20260731-2344`  
Claim boundary: `claim_allowed=false`

## Fontes verificadas

- Google Drive: `RAFAELIA — Implementação Latentes e Papers — Drive GitHub V1`.
- Mapa: `indices/RAFAELIA_IMPLEMENTACAO_LATENTES_PAPERS_V1.md`.
- Mapa: `data/latents/latents.index.jsonl`.
- Mapa: `data/claims/paper_claims.index.jsonl`.
- Produtores localizados: `RafGitTools`, `RafPolimata`, `papers` e `instituto-Rafael/relativity-living-light`.
- RLL PR #627: `MERGED`, merge commit `dc5fcfb3b786bf59d32ebfa22ad6f4eed15f738e`.
- RLL PR #628: `OPEN_DRAFT`, head `79ec35f5fdb275645e89d3a685d9b44a6bb6f45d`.

## Delta catalogado

### 1. Pantheon+SH0ES full-covariance — PR #627

A rota model-bound foi executada com a matriz STAT+SYS oficial, dimensão original `1701×1701`, seleção `1657×1657`, cinco seeds por modelo, simetrização determinística limitada a `5e-8`, Cholesky sem jitter e receipt verificável.

```yaml
operational_execution: PASS
merge_state: MERGED
claim_allowed: false
publication_effect: NONE
independent_replication: TOKEN_VAZIO
joint_real_bayes: TOKEN_VAZIO
```

Custódia:

```text
covariance_sha256 = abf806d966485e64afdb359c87bffc0ecc00d05eff0a31ced66f247385df0fdc
result_sha256     = e23066e8445f940cf28b651a29c49789d8a3cdd1d492c00afe63a5247b9ce5ba
receipt_sha256    = 9756233073dac1b7fcba266604f655e5823e22119513880cf0fd8d41d98754c7
semantic_sha256   = d7681b6426a106953a834b33d45e9b64c29272fb41c3a7d7cbbce16343de00cf
```

Resultado limitado ao bloco Pantheon+SH0ES:

| métrica RLL−ΛCDM | valor |
|---|---:|
| Δχ² | `+4.547473508864641e-13` |
| ΔAIC | `+6.000000000000455` |
| ΔAICc | `+6.036390034648093` |
| ΔBIC | `+22.23829205228003` |

O RLL não reduz χ² e é penalizado pelos parâmetros adicionais. A execução é evidência de funcionamento da rota, não validação externa da cosmologia.

### 2. Estado dual da matriz

O readiness do checkout e o runtime não são estados contraditórios:

```text
checkout sem matriz grande
  → TOKEN_VAZIO_FULL_COVARIANCE

runtime materializa fonte pinada + verifica hash/dimensão + executa + remove
  → PASS operacional

interpretação física/publicação
  → claim_allowed=false
```

### 3. Fase 24.1 — PR #628

A PR permanece aberta e draft. A branch declara:

```text
run             30658727866
artifact        8804497381
artifact_sha256 65806334cea799f77977dbf040eb7a32819f9d28bb5189d30751a4b1aaaf51b4
manifest        107 files
steps           38 OK / 1 TOKEN_VAZIO / 0 FAIL
suite           870 passed + 3 subtests passed
```

Estado correto no catálogo:

```yaml
artifact_integrity: PASS_DECLARED_AND_BRANCH_BOUND
canonical_merge: TOKEN_VAZIO
scientific_gate: BLOCKED
publication_ready: false
real_bayes_inference: TOKEN_VAZIO
```

## Decisões

1. Registrar PR #627 como `PASS` operacional com `claim_allowed=false`.
2. Preservar o claim de preferência empírica ampla do RLL como `FAIL/BLOCKED`.
3. Registrar PR #628 como `PARTIAL/DRAFT`, sem promovê-la a estado canônico de `main`.
4. Manter reprodução independente, Bayes real conjunto e composição BAO/H(z)/growth/CMB como `TOKEN_VAZIO`.

## R₃

- **F_ok:** delta reconciliado com commits, hashes, receipts, métricas e limites.
- **F_gap:** PR #628 ainda não mesclada; não há reprodução independente nem inferência Bayes real conjunta.
- **F_next:** revisar esta PR de catálogo; revisar a PR #628; reproduzir o receipt em segunda implementação/máquina sem sobrescrever históricos.

FIAT LUX — identidade de artefato não é verdade física; lacuna explícita é ciência auditável.
