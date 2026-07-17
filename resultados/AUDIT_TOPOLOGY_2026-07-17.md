> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — a auditoria registra o que foi observado, sem promover ausência de execução como aprovação.

# Auditoria da Topologia Determinística — 2026-07-17

Branch: `fix/topologia-deterministica-20260717`  
PR: `#18`  
Estado: `IMPLEMENTED / CI_STARTUP_FAILURE / claim_allowed=false para prova remota`

## Pacote implementado

1. `orquestrador/QUALITY_GATE_POLICY.md`;
2. `scripts/validate_mapa_topology.py`;
3. `tests/test_topology.py`;
4. `.github/workflows/topology-validation.yml`;
5. `indices/GRAFO_DEPENDENCIAS_MAPA.yaml` versão 2.0.0.

## Resultado estrutural da fonte canônica

```text
nodes = 33
edges = 108
active = 23
planned/LACUNA = 10
cycles = 0
orphans = 0
max_depth = 15
critical_path_nodes = 16
blake2b-256 = a01069c0fc0b10c4fa195399a0f4f07a1a9f33d55cb96be5f883739033b67ad1
```

A relação circular anterior foi removida:

```text
ANTES: QUAL_16 <-> F_03
AGORA: QUAL_16 -> F_03 -> IND_MANIFESTO
```

## Pré-validação do pacote

O validador e os testes foram executados no ambiente de preparação com o mesmo conteúdo versionado:

```text
unittest_count = 5
unittest_result = PASS
validator_result = ok=true
```

Isso comprova coerência interna do pacote preparado. Não substitui a prova de execução no runner do GitHub.

## Estado observado no GitHub Actions

### Workflow novo

```text
run_id = 29589927220
workflow = Topology Structural Validation
job_id = 87916166786
status = completed
conclusion = failure
steps_returned = 0
logs = unavailable / BlobNotFound
classification = STARTUP_FAILURE_OR_INFRASTRUCTURE_FAILURE
validator_execution_proven = false
```

### Workflow geral

```text
run_id = 29589927184
workflow = CI
job_id = 87916166720
status = completed
conclusion = failure
steps_returned = 0
logs = unavailable
classification = STARTUP_FAILURE_OR_INFRASTRUCTURE_FAILURE
```

Os dois workflows falharam antes do primeiro step. Portanto, não existe evidência de erro produzido pelo código, mas também não existe prova remota de aprovação.

## Regra de honestidade

```text
estrutura_versionada = true
validacao_local_preparatoria = PASS
validacao_runner_github = NOT_EXECUTED
claim_allowed_prova_remota = false
```

## Próxima condição de promoção

A prova remota somente muda para `claim_allowed=true` quando uma execução apresentar simultaneamente:

- pelo menos um step iniciado;
- logs observáveis;
- testes concluídos com sucesso;
- relatório `topology-validation.json` gerado;
- checksum publicado como artefato.

## Resultado

A topologia deixou de ser uma declaração manual contraditória e passou a possuir fonte canônica, hash real, métricas derivadas, marcação FATO/LACUNA, testes e gate de CI. A indisponibilidade do runner permanece registrada como lacuna externa, sem bloquear a integração da correção documental e computacional nem permitir alegação falsa de CI aprovada.
