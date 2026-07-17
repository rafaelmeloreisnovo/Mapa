# Auditoria do lote 3 — memória, modelo, Ω e ética

## Propósito

Ampliar o inventário por famílias de autoridade ainda sub-representadas, mantendo cada fragmento ligado diretamente ao conector GitHub.

## Entrada

```text
batch_id = BATCH_003_2026-07-17
source = github_connector.get_repo
records = 10
owner split = 5 pessoais + 5 institucionais
batch digest = 9dd4998d19c58273c8c7541a9871125eb3d46b466301e4015f7789b8910a4597
```

## Registros pessoais

- `rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE`
- `rafaelmeloreisnovo/MemRa`
- `rafaelmeloreisnovo/MemRafcode`
- `rafaelmeloreisnovo/nanoGPT`
- `rafaelmeloreisnovo/Semente`

## Registros institucionais

- `instituto-Rafael/Particula-Omega-`
- `instituto-Rafael/PlamaticGravity-`
- `instituto-Rafael/omega-rafaelia`
- `instituto-Rafael/apk-privacy-rafaelia`
- `instituto-Rafael/apk-ethics-rafaelia`

## Resultado

```text
before_materialized = 31
added = 10
after_materialized = 41
accessible_total_observed = 126
remaining_TOKEN_VAZIO = 85
completeness_ratio = 0.325396825397
public = 22
private = 19
archived = 0
claim_allowed = false
inventory digest = 204b310de7ecbfc0e4df316d126748b03cb4ed624a3e0eff8914a3a1e8018d48
```

## Prova de continuidade

A reconstrução local, iniciada nos 11 registros não cobertos por lotes, reproduziu os selos oficiais antes da aplicação nova:

```text
BATCH_001 state digest = 1e9fa96ea2651e385fd095e2a72b3dfba7a675a6701c78f2ba63139b183952e9
BATCH_002 state digest = 3151f39d5d9021cdcfa21a57b9a603325b86d5d668916389433e4ac8a8e99641
```

Depois, 24 asserções locais verificaram digest, unicidade, identidade lote↔inventário, estatísticas e fronteira de claim.

## Correção de classificação da CI

O rótulo causal amplo `STARTUP_FAILURE_OR_INFRASTRUCTURE_FAILURE` foi depreciado pela autoridade canônica `RafGitTools` no merge `2d013358fc4861cad46caf71ab48d2365abfa0b7`.

Até aparecer mensagem causal explícita, o estado dos jobs observados no `Mapa` é:

```text
ZERO_STEP_NO_LOGS
billing_block_proven = false
policy_block_proven = false
workflow_code_failure_proven = false
```

A mensagem de pagamento informada para `instituto-Rafael/relativity-living-light` não é propagada por analogia aos demais repositórios.

## Limite

Este lote prova identidade e metadados retornados pelo conector. Não prova conteúdo, autoria integral, maturidade, funcionamento, segurança ou valor científico dos repositórios materializados.
