# RAF HW Microarchitecture Benchmark Index V1

## Invariantes

- measured != inferred != simulated;
- benchmark effect != exact microarchitectural identity;
- `TOKEN_VAZIO` preservado para cache/TLB exatos;
- `claim_allowed_exact_topology=false` até evidência causal suficiente e replicação externa;
- resultados negativos e hipóteses rejeitadas permanecem no histórico.

## Linha atual

### Stage 7 — VA Color / Alias Isolation — 2026-08-15

Canônico:
`docs/canonical/2026-08-15/RAF_HW_STAGE7_VA_COLOR_ALIAS_ISOLATION_CHECKPOINT_V1.md`

Evidência:
- `data/evidence/hardware/raf_hw_stage7_va_color_alias_isolation_analysis_20260815.v1.txt`
- `data/evidence/hardware/raf_hw_stage7_va_color_alias_isolation_receipt_20260815.v1.txt`

Estado: `VERIFIED_LIMITED_PENDING_EXTERNAL_REPLICATION`.

Resultado-chave: `median(ALIAS_4K/ALIAS_64K)=0.549205`; `median(min(ALIAS_4K,ALIAS_64K)/SINGLEVA)=1.219893`; geometria/spacing VA é material, porém identidade TLB/cache exata permanece aberta.

Próxima rota: Stage 8 — varredura causal de stride 4K→256K com mesma página física, matching por CPU/frequência e análise por periodicidade.
