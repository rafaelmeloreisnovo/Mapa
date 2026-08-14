# RAFAELIA — MetricObservationV1 — Contrato Canônico

Data: 2026-08-14  
Modo: APPEND_ONLY / FAIL_CLOSED  
Estado global: `VERIFIED_IMPLEMENTATION_PENDING_EXECUTION`  
`claim_allowed=false` por padrão.

## Invariante

`número encontrado != medição != medição reproduzível != claim geral`

Cada valor quantitativo deve preservar, no mínimo:

`identidade + nome da métrica + valor original + unidade original + normalização + ambiente + workload + configuração + fonte + evidência + classe epistemológica + próximo passo verificável`.

## Classes epistemológicas

- `MEASURED_WITH_RECEIPT`: valor vinculado a artefato/receipt/raw result.
- `HISTORICAL_RUN_OUTPUT`: saída histórica recuperada, ainda sujeita a reconciliação de identidade.
- `MEASUREMENT_PATH_IMPLEMENTED`: instrumento existe, mas o valor físico atual pode ser `TOKEN_VAZIO`.
- `DOCUMENTED_BENCHMARK_UNBOUND`: tabela/documentação sem ligação suficiente ao raw run.
- `ESTIMATE_CODE_ANALYSIS`: estimativa derivada de análise de código; nunca promovida silenciosamente.
- `EXPECTED_REFERENCE_RANGE`: faixa de referência/expectativa; não é medição.
- `OPERATIONAL_THRESHOLD`: limiar de máquina de estados/política; não é medição.
- `TOKEN_VAZIO`: ausência explicitamente preservada.

## Normalização sem perda semântica

O valor original nunca é apagado. O normalizador adiciona uma representação canônica.

Exemplos:

- `594.881 ns/sector -> 5.94881e-7 s/sector`
- `163.45 MiB/s -> 171389747.2 B/s`
- `111.956 MOPS -> 111956000 ops/s`
- `1.522 GB/s -> 1522000000 B/s`

`MB/s != MiB/s`.

`IOPS` permanece `IOPS`; não é rebatizado como `ops/s`, pois o domínio de operação de I/O é parte da semântica.

## Promotion gate

Uma observação não pode ter `claim_allowed=true` apenas por possuir um número.

Para promoção, o validador exige:

1. classe `MEASURED_WITH_RECEIPT`;
2. evidência material (`artifact_sha256`, receipt ou raw result ref);
3. ambiente não vazio;
4. workload não vazio;
5. `promotion_gate.status=APPROVED`;
6. `promotion_gate.receipt_ref` preenchido.

As demais classes são fail-closed.

## TOKEN_VAZIO

Se `value_state=TOKEN_VAZIO`:

- `observed_value=null`;
- `normalization.status=TOKEN_VAZIO`;
- `normalization.canonical_value=null`;
- `claim_allowed=false`.

Exemplo atual: o código do Vectras implementa random 4K IOPS, mas o valor físico do dispositivo alvo permanece `TOKEN_VAZIO_DISK_BENCHMARK_DEVICE_RECEIPT` até execução e receipt.

## Arquivos

- `schemas/benchmarks/metric-observation.v1.schema.json`
- `tools/validate_metric_observation_v1.py`
- `data/benchmarks/metric-observation-v1.examples.json`
- `tests/test_metric_observation_v1.py`

## Execução prevista

```bash
python3 tools/validate_metric_observation_v1.py data/benchmarks/metric-observation-v1.examples.json
python3 -m unittest tests.test_metric_observation_v1
```

A presença desses comandos no documento não equivale a execução. Até existir receipt de runtime/CI desta branch:

`TOKEN_VAZIO_METRIC_OBSERVATION_TEST_RECEIPT`.

## R₃

`F_ok`: contrato, normalização e regras fail-closed implementados.  
`F_gap`: execução dos testes, binding de raw runs antigos, deduplicação semântica e coleta física atual ainda abertas.  
`F_next`: executar testes em CI/runtime, produzir receipt, então iniciar ingestão automática dos 79 slots Vectras e dos históricos recuperados.
