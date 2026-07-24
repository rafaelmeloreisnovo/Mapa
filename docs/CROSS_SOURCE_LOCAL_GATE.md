# Gate Local Cross-Source — Termux e Python 3

```yaml
schema: rafaelia.cross-source-local-gate-guide/v4
mode: OFFLINE
network_required: false
third_party_python_dependencies: false
quality_model: growth_safe_floor
required_test_files: 7
required_tests_discovered: 58
required_tests_executed: 58
required_skipped: 0
required_expected_failures: 0
required_unexpected_successes: 0
claim_allowed: false
remote_ci_substituted: false
```

## 1. Finalidade

O gate reproduz localmente a camada GitHub ↔ Google Drive ↔ Termux ↔ sessão e a cadeia de custódia usando somente arquivos versionados e Python standard library.

O PASS local demonstra reprodução estrutural. Não substitui o GitHub Actions, não autentica o executor e não autoriza merge sozinho.

## 2. Piso versionado

```text
indices/CROSS_SOURCE_GATE_FLOOR.json
```

Regras:

```text
observado >= mínimo versionado
tests_run == tests_discovered
skipped == 0
expected_failures == 0
unexpected_successes == 0
```

Contrato atual:

```yaml
test_file_count: ">= 7"
tests_discovered: ">= 58"
tests_run: ">= 58"
complete_execution: true
clean_outcomes: true
failures: 0
errors: 0
skipped: 0
expected_failures: 0
unexpected_successes: 0
```

Os 58 testes são uma exigência derivada da superfície governada declarada na PR #48. Enquanto não houver execução integral, não constituem afirmação de PASS.

```yaml
full_gate_execution: TOKEN_VAZIO
claim_allowed: false
```

## 3. Por que `unittest OK` não basta

O `unittest` pode finalizar com sucesso quando existem testes pulados ou falhas marcadas como esperadas. Para uma cadeia de custódia, esse resultado é ambíguo.

O executor canônico converte em FAIL qualquer execução com:

- skip;
- expected failure;
- unexpected success;
- contagem executada diferente da descoberta.

```yaml
unittest_display: "OK (skipped=1)"
gate_status: FAIL
process_exit_code: 1
```

## 4. Execução

```sh
sh scripts/run_cross_source_gate.sh
```

Saída padrão:

```text
.artifacts/cross-source-local/
```

Saída personalizada:

```sh
sh scripts/run_cross_source_gate.sh \
  "$HOME/storage/shared/RAFAELIA_EVIDENCE/cross-source-local"
```

## 5. Etapas

```text
1. compilar validadores, avaliadores, comparador e testes
2. validar schema, piso e fixtures JSON
3. validar parse dos registries JSONL
4. descobrir, contar e executar a suíte governada
5. gerar relatórios de records e registry
6. validar a cadeia de custódia append-only
7. comparar resultados com o piso v2
8. exigir execução completa, limpa e sem promoção
9. selar cinco relatórios, manifesto e checksums SHA-256
```

## 6. Pacote

```text
cross-source-test-validation.json
cross-source-record-validation.json
cross-source-registry-validation.json
chain-of-custody-validation.json
quality-floor-validation.json
LOCAL_GATE_STATUS.json
CHECKSUMS.sha256
```

### Relatório de testes v4

```yaml
schema_version: rafaelia.cross-source-test-report/v4
status: PASS
test_file_count: ">= 7"
tests_discovered: ">= 58"
tests_run: ">= 58"
complete_execution: true
clean_outcomes: true
failures: 0
errors: 0
skipped: 0
expected_failures: 0
unexpected_successes: 0
claim_allowed: false
remote_ci_substituted: false
```

### Avaliação do piso v3

```yaml
schema_version: rafaelia.cross-source-gate-evaluation/v3
status: PASS
failed_check_count: 0
promotion_state: LOCAL_PASS_REMOTE_TOKEN_VAZIO
claim_allowed: false
remote_ci_substituted: false
```

### Manifesto v3

```yaml
schema_version: rafaelia.cross-source-local-gate/v3
status: PASS
test_file_count: valor_observado
minimum_test_file_count: 7
test_count_discovered: valor_descoberto
test_count_observed: valor_executado
minimum_test_count: 58
complete_test_execution: true
clean_test_outcomes: true
report_count: 5
quality_floor:
  path: indices/CROSS_SOURCE_GATE_FLOOR.json
  schema_version: rafaelia.cross-source-gate-floor/v2
  sha256: valor_calculado_do_arquivo_real
  status: PASS
quality_floor_status: PASS
promotion_state: LOCAL_PASS_REMOTE_TOKEN_VAZIO
claim_allowed: false
remote_ci_substituted: false
```

## 7. Registry reproduzível

O relatório usa caminho canônico:

```yaml
registry: indices/CROSS_SOURCE_REGISTRY.jsonl
```

Checkouts distintos não alteram esse campo. Arquivos externos usam `external://<basename>` e não vazam o diretório do host.

## 8. Segurança

O gate bloqueia:

- rede e comandos privilegiados;
- mutação Git;
- exclusão ampla;
- bytecode na árvore versionada;
- redução silenciosa de testes, registros ou custódia;
- execução parcial apresentada como completa;
- skip apresentado como aprovação;
- claim ou CI remota substituída localmente.

## 9. Comparação Termux ↔ Actions

```sh
python3 scripts/compare_cross_source_evidence.py \
  --left .artifacts/cross-source-local \
  --right .artifacts/cross-source-remote \
  --floor indices/CROSS_SOURCE_GATE_FLOOR.json \
  --write-report .artifacts/cross-source-comparison.json
```

O comparador valida cada manifesto contra o arquivo real do piso no checkout.

Exigir:

```yaml
status: PASS
matching_report_count: 5
quality_floor_sha256_match: true
claim_allowed: false
```

Sem artifact remoto:

```yaml
remote_bundle: TOKEN_VAZIO
comparison: TOKEN_VAZIO
```

## 10. Próximo passo verificável

1. executar o gate no checkout integral do Termux;
2. provar sete arquivos e 58/58 testes limpos ou mais;
3. preservar o pacote local;
4. restaurar o runner privado;
5. obter artifact remoto associado ao commit;
6. comparar contra o piso real;
7. anexar evento `VALIDATE`;
8. somente então avaliar saída de `DRAFT`.

---

```text
Descoberto = superfície reconhecida
Executado = superfície percorrida
Limpo = nenhuma exceção silenciosa
Tempo sem evidência = TOKEN_VAZIO
```
