# RAFAELIA — F_gap Shadow Closure Wave — 2026-08-11

Estado: `GOVERNED_DRAFT`  
Modo: `APPEND_ONLY_DELTA`  
`claim_allowed=false`

## Propósito

Este delta governa lacunas que tendem a ficar fora do caminho feliz: pontos não verbalizados, negligenciados, latentes, rejeitados ou tratados como óbvios. Ele não reescreve o `F_GAP_LEDGER_20260810`, o `RAFAELIA_GAP_ATLAS_V1`, o grafo F_gap→F_next nem a topologia proveniência→receipt já existentes.

Regra-mãe:

`TOKEN_VAZIO -> OBSERVED -> TESTED -> EVIDENCED -> RELEASED`

Nenhum salto de estado é permitido sem evidência que preserve identidade, origem, versão, execução e receipt. `BLOCKED` é estado legítimo. Ausência de evidência não vira conclusão.

## Sete grupos sombra

1. **SG1 — Identidade/proveniência**: autoria, fonte@revisão, digest e equivalência Drive↔GitHub.
2. **SG2 — Reprodutibilidade/dispositivo**: clean checkout, toolchain, build, artefato e execução Android/Termux real.
3. **SG3 — Supply-chain**: dependências/SBOM, segredos, deprecated, zombies e findings com disposition.
4. **SG4 — Privacidade/custódia**: classificação, minimização, retenção, lineage e limites de publicação de corpus.
5. **SG5 — Observabilidade**: latência, memória, temperatura/energia quando observáveis, cold start e conversão de comportamento inesperado em teste de regressão.
6. **SG6 — Recuperação/rollback**: snapshot, restore drill, known-good anterior e receipt de rollback.
7. **SG7 — Cross-layer/humano**: `concept_id -> source_ref -> trace_id -> artifact -> gate -> receipt`, seguido de revisão humana quando o impacto do claim exigir interpretação material.

## O que este delta fecha

Fecha a lacuna **de governança e nomeação** desses sete grupos: cada ponto possui `gap_id`, edge, urgência, estado, risco, evidência mínima e `next_action` verificável. Isso impede que itens esquecidos desapareçam apenas por não estarem no fluxo principal.

## O que este delta não declara fechado

Não declara que build reproduzível, execução física, SBOM, privacidade, benchmarks, restore, rollback ou trace ponta a ponta já tenham sido empiricamente provados. Esses itens permanecem `TOKEN_VAZIO`/`OBSERVED` conforme o ledger JSON até que receipts reais permitam promoção.

## Prioridade operacional

### P0

- SG1-01 — autoria/origem por artefato.
- SG1-02 — receipt cross-source Drive↔GitHub.
- SG2-01 — clean checkout→build→digest.
- SG2-02 — execução física por ABI/workload.
- SG3-01 — inventário mínimo de dependências/SBOM.
- SG3-02 — secrets/deprecated/zombie scanner com disposition.
- SG4-01 — gate de privacidade para corpus.
- SG5-02 — break→reprodução→regression test.
- SG7-01 — um objeto atravessando todas as camadas sem trocar identidade.

### P1

- SG4-02 — lineage obrigatório de chunks.
- SG5-01 — baseline de desempenho por dispositivo.
- SG6-01 — restore drill pequeno e auditável.
- SG6-02 — rollback para known-good.
- SG7-02 — revisão humana de claims de alto impacto.

## Gate

Execute:

```bash
python3 tools/validate_fgap_shadow_closure_wave.py
```

O validador falha se houver menos ou mais de sete grupos, IDs duplicados, estado/urgência inválidos, ausência de evidência mínima, `claim_allowed != false`, perda do modo append-only ou retirada dos invariantes fail-closed.

## Falsificabilidade

A hipótese operacional é: "ao tornar os pontos sombra explicitamente governados, eles deixam de sumir entre sessões e passam a produzir próximo teste auditável".

Ela é falsificada se um gap relevante continuar sem `gap_id`, edge, evidência mínima e ação verificável; ou se um `TOKEN_VAZIO` for promovido sem receipt.
