# Auditoria de correção do inventário — 2026-07-17

## Limite epistemológico

```text
inventory_state = PARTIAL
accessible_total_observed = 126
materialized_records = 11
missing_materialized_records = 115
claim_allowed = false
```

A validação `PASS` significa somente que o snapshot parcial é internamente coerente, determinístico e fail-closed. Não significa que 126 registros foram materializados.

## Defeitos encontrados no commit anterior

O commit `ecc1a50ceee99b6aeeeadee3b29a935a484c9b56` declarava inventário derivado de 126 repositórios, mas:

1. materializava apenas 11 entradas;
2. declarava `124 public / 2 private / 3 archived`, divergindo das 11 entradas;
3. atribuía ao `Mapa` o ID `1088281710`, enquanto o conector retorna `1267885874`;
4. marcava `Mapa`, `UserLAnd`, `ChipQuantum`, `publicacientiespiritual`, `QUANTUM_source_code` e `RafGitTools` como públicos, embora o conector os retorne privados;
5. gravava `BLAKE3` e `UserLAnd` com branch `main`, embora o conector retorne `master`;
6. usava o campo `size_bytes`, apesar de o valor retornado pelo GitHub ser `size` em KiB;
7. inventava datas, linguagem, descrição, tópicos e métricas que não estavam presentes na resposta usada;
8. dependia do pacote externo `jsonschema`;
9. tolerava divergência entre total declarado e lista materializada;
10. dizia “37 testes” no commit, mas o arquivo continha 25 métodos de teste e nenhum resultado executado;
11. referenciava scripts de coleta e digest que não existiam;
12. mantinha o relatório inteiro em `PENDING`.

## Correção aplicada

- somente campos observados por `github_connector.get_repo` foram preservados;
- `repository_id`, owner, nome, branch, visibilidade, archived e `size_kib` foram conferidos individualmente;
- owners homônimos permanecem distintos;
- contagens da amostra são derivadas da lista;
- o total acessível observado é derivado das instalações `85766350` e `91630826`;
- os 115 registros não materializados permanecem em ledger `TOKEN_VAZIO`;
- o digest BLAKE2b-256 cobre o documento canônico sem o próprio campo de digest;
- o validador usa apenas Python stdlib;
- 12 testes adversariais verificam identidade, contagens, promoção, adulteração, ledger e integridade;
- o workflow estrutural existente foi ampliado, sem criar YAML concorrente.

## Evidência local

```text
validator status = PASS
inventory state = PARTIAL
claim_allowed = false
unit tests = 12 PASS
py_compile = PASS
digest = ea3fddc116e94be88deb1c2b477013ed49ab0d16f4d442ffd8f0469b9d7677da
```

## Evidência remota

```text
Topology and Inventory Structural Validation
run_id = 29597945148
job_id = 87942811687
conclusion = failure
steps = 0
logs = BlobNotFound

CI geral
run_id = 29597945190
job_id = 87942811420
conclusion = failure
steps = 0
logs = unavailable
```

Classificação:

```text
STARTUP_FAILURE_OR_INFRASTRUCTURE_FAILURE
validator_execution_proven = false
contract_failure_proven = false
remote_PASS_proven = false
```

A falha remota ocorreu antes de qualquer etapa observável. Ela não é reinterpretada como falha do código nem como aprovação.

## Critério de saída da lacuna

O inventário só poderá mudar para `COMPLETE` quando:

1. `materialized_count == accessible_total_observed`;
2. todos os registros forem obtidos do conector;
3. nenhum campo não observado for preenchido por aproximação;
4. o validador e os testes passarem;
5. a CI remota produzir steps e logs observáveis;
6. o snapshot for selado com novo digest.

Até lá, `claim_allowed=false` permanece obrigatório.
