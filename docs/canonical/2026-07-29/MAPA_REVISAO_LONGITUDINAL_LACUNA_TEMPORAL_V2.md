# Mapa — Revisão longitudinal e contrato de lacuna temporal V2

**Evento:** `TG2-20260729T041846024360Z`  
**Observado UTC:** `2026-07-29T04:18:46.024360Z`  
**Observado BRT:** `2026-07-29T01:18:46.024360-03:00`  
**Estado:** `DRIVE_ANCHORED_PRECOMMIT_REVIEW`  
**claim_allowed:** `false`

## Veredito

O Mapa já possui ontologia operacional, custódia contextual, `TOKEN_VAZIO` tipado e memória append-only. O gap crítico é temporal e topológico: a `main` atual e a linha de custódia V1 são ramos divergentes com ancestral comum `596ceaff5c5b1932c3649bd44af5f03468075f04`.

```text
pai Git       = 84cb0b2e752761211ed81a8a13895a6206265d44
pai custódia  = 14e3ce20b4ab445ac65381222205566e5352a30f
ancestral     = 596ceaff5c5b1932c3649bd44af5f03468075f04
relação       = diverged; custody ahead 2 / behind 4
```

O novo evento não deve fingir uma ancestralidade Git inexistente. Ele carrega dois pais semânticos:

\[
P_n=\langle git\_parent,custody\_parent\rangle
\]

## Lacuna temporal medida

\[
\Delta t_n=t_{observed,n}-t_{custody,parent}
\]

```text
origem do intervalo = 2026-07-29T04:06:26Z
fim observado        = 2026-07-29T04:18:46.024360Z
Delta t segundos     = 740.024360
Delta t nanos        = 740024360000
```

O commit-base da `main` foi produzido 82 segundos antes do selo V1. Isso não é tempo negativo do sistema: é evidência de ramos concorrentes. A ordem causal precisa ser armazenada separadamente da ordem linear de uma única branch.

## Contrato matemático

```text
E_n = CanonicalJSON(P_n, Delta_t_n, D_n, R_n, A_n, seq_n)
C_n[a] = H_a(C_(n-1)[a] || H_a(E_n) || encode(Delta_t_ns) || seq_n)
```

```text
H_a ∈ {SHA3-256, BLAKE3-256}
MD5 = compatibilidade legada, sem autoridade criptográfica forte
UTC = relógio canônico
America/Sao_Paulo = projeção humana
```

Gate temporal:

```text
t_custody_parent <= t_observed <= t_drive <= t_precommit <= t_commit <= t_post
```

Quando plataformas retornarem tempos com granularidades diferentes, o sistema registra a precisão e não inventa nanos inexistentes.

## Cinco revisões prioritárias do Mapa

1. **P0 — Duplo parentesco:** separar `git_parent` de `custody_parent`.
2. **P0 — Schema temporal:** tipar `observed_at`, `drive_anchored_at`, `committed_at` e `post_observed_at`.
3. **P1 — Política de relógio:** UTC canônico, BRT para leitura, precisão declarada.
4. **P1 — Registro federado:** ligar evento, hashes, Drive, branch, PR e commits.
5. **P1 — Terminologia:** `HASH_CHAINED_TIMESTAMP_LEDGER`, não blockchain pública.

## Âncoras do Drive

```text
folder_id = 1kweK_UZGcNph3eLjEcDJr7JqVPULUuNA
document_id = 1bp7h468s_W1VXs7ACvcH0ZBewY3QTZwRk5_IX39JMeU
precommit_revision = AIroW34MM10NbjFhxJylXO1sxpx57_mKXrQ0jZdCHN1bqXN_-Jlp1vhHr0w353Wywr7YjhXF_V7t3tLsSkgfrj_8k26ukLzJ7xie907-H6bN
canonical_memory_id = 1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88
canonical_memory_revision = AIroW379ybDEEJXl4EvqfiOob3bCjcQM0Y2wUn2ZcWc1fngIRad-C4mdM1kyVkZMe7D4quj9fLxf6704QbGcWeqf9XZnoxjOC49Y-yDJRk0
```

## Invariantes preservadas

- nenhuma transformação apaga a origem;
- eventos são append-only;
- `claim_allowed=false`;
- merge automático proibido;
- SHA3-256 e BLAKE3-256 são digests fortes;
- MD5 é somente índice legado;
- timestamp não prova autoria jurídica absoluta nem consenso distribuído.

## Hashes do artefato local anterior ao GitHub

```text
bytes        = 3124
SHA3-256     = bdc1a95d9f6705c4b514fe309dd1a44bf825433def3ff552e7266acf60f412eb
BLAKE3-256   = ead8a9e4ba82f56226a8fb60d41b5e2680e312db95a86e631f2417ac4e22ef01
MD5 legado   = f51e600780e7aaa6214724c43d61dcf2
```

## R3

- **F_ok:** âncora V1 verificada; divergência entre ramos medida; contrato temporal definido; Drive V2 e memória canônica atualizados.
- **F_gap:** PR e timestamps reais dos commits V2 ainda não estavam disponíveis ao escrever esta revisão.
- **F_next:** abrir PR draft, reler os commits produzidos pelo GitHub e fechar um receipt pós-commit.
