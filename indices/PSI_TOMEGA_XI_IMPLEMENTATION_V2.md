# Índice federado — Ψv–TΩ–Ξ V2

**Data de observação:** 2026-08-06  
**Estado:** `VERIFIED_LIMITED_WITH_NEGATIVE_BENCHMARK`  
**Claim gate:** `claim_allowed=false`  
**Identificador:** `RAFCODE-PSI-TOMEGA-XI-SCAN-V2-20260806`

## 1. Autoridades

| Camada | Autoridade | Ponteiro observado | Papel |
|---|---|---|---|
| Runtime | `rafaelmeloreisnovo/GAIA_phi` | PR #70, head `27ec3e208793c79bf690cfa9a0edf6120313f123` | código, testes, scanner, benchmark e receipt |
| Matemática/epistemologia | `rafaelmeloreisnovo/papers` | PR #43, head `a6c2aace7499013a8763240a227a25964831cee9` | definição de Ψv–TΩ–Ξ e limites de claim |
| Memória editorial | Google Drive | documento `1It5dDGCudbhZljhjtQd26KIm5HVEcpdNpJ1HFC9mhYs`, revisão V2 append-only | navegação longitudinal e síntese |
| Custódia/reentrada | `rafaelmeloreisnovo/MemRafcode` | branch `audit/psi-tomega-xi-scan-20260806` | receipt federado e cadeia de reentrada |
| Controle federado | `rafaelmeloreisnovo/Mapa` | este índice | autoridade, estado, rota e gaps |

## 2. Artefatos executáveis

Autoridade: `GAIA_phi` PR #70.

- `dados/cognitive_symbiotic.py`;
- `dados/cognitive_compression.py`;
- `tools/scan_cognitive_artifacts.py`;
- `benchmarks/benchmark_cognitive_symbiotic.py`;
- `tests/test_cognitive_symbiotic.py`;
- `tests/test_cognitive_compression.py`;
- `tests/test_scan_cognitive_artifacts.py`;
- `reports/evidence_runs/psi_tomega_xi_synthetic_20260806.json`;
- `docs/PSI_TOMEGA_COMPLEX_FEEDBACK_V1.md`;
- `docs/PSI_TOMEGA_XI_SCAN_IMPLEMENTATION_V2.md`.

## 3. Evidência observada

```yaml
local_tests: 19_PASS
python: 3.13.5
torch: 2.10.0_CPU
benchmark_scope: SYNTHETIC_CONTROLLED_ONLY
baseline_final_loss: 0.44701594
candidate_final_loss: 0.54565597
baseline_p50_ms: 0.14967
candidate_p50_ms: 0.48248
synthetic_result: BASELINE_BETTER_IN_THIS_RUN
architecture_advantage: NOT_ESTABLISHED
claim_allowed: false
```

O resultado negativo é parte da evidência e não deve ser apagado em versões posteriores.

## 4. Método de varredura

```text
README
→ árvore
→ branches e PRs
→ arquivos
→ digest
→ termos controlados
→ claim/fonte/evidência/falsificador
→ autoridade
→ estado
→ próximo teste
```

Invariantes:

```text
nome != conteúdo
metadado != leitura integral
keyword != evidência
commit != execução
local PASS != reprodução independente
TOKEN_VAZIO != zero
resultado negativo != falha de custódia
```

## 5. Estados abertos

| Estado | Classificação |
|---|---|
| tarefa-alvo real | `TOKEN_VAZIO_TARGET_DATASET` |
| múltiplas sementes | `TOKEN_VAZIO_MULTI_SEED` |
| igualdade de parâmetros/FLOPs | `TOKEN_VAZIO_BUDGET_MATCH` |
| reprodução independente | `TOKEN_VAZIO_REPRODUCTION` |
| GPU/fp16/bf16 | `TOKEN_VAZIO_PLATFORM` |
| ARM64/Android/Termux | `TOKEN_VAZIO_PLATFORM` |
| variante head-aware | `TOKEN_VAZIO_HEAD_AWARE` |
| significado cognitivo | `NOT_CLAIMED` |
| correspondência física | `NOT_CLAIMED` |
| produção | `TOKEN_VAZIO_PRODUCTION` |

## 6. Rota autorizada

1. revisar GAIA_phi PR #70 e papers PR #43;
2. executar CI e registrar estado remoto sem converter ausência de runner em falha de código;
3. realizar benchmark multi-semente com orçamento comparável;
4. integrar tarefa real e baselines GRU/LSTM/atenção;
5. produzir novo receipt append-only;
6. atualizar Mapa e Drive por ponteiros imutáveis;
7. somente então avaliar merge ou nova versão.

## 7. R3

```text
F_ok   = implementação, 19 testes, scanner, benchmark e Drive atualizados
F_gap  = vantagem real, multi-semente, plataformas e reprodução
F_next = revisão dos PRs + benchmark equilibrado + receipt independente
```
