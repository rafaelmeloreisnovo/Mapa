# Gate Local Cross-Source — Termux e Python 3

```yaml
schema: rafaelia.cross-source-local-gate-guide/v3
mode: OFFLINE
network_required: false
third_party_python_dependencies: false
quality_model: growth_safe_floor
required_test_files: 7
required_tests_discovered: 58
required_tests_executed: 58
claim_allowed: false
remote_ci_substituted: false
```

## 1. Finalidade

O gate reproduz localmente as validações estruturais da camada GitHub ↔ Google Drive ↔ Termux ↔ sessão e da cadeia de custódia.

Ele usa somente arquivos versionados e Python standard library. Não acessa GitHub, Google Drive ou qualquer outra rede durante a execução.

O resultado local é evidência de reprodução estrutural. Ele não substitui o GitHub Actions e não autoriza merge sozinho.

## 2. Regra de crescimento

O piso versionado está em:

```text
indices/CROSS_SOURCE_GATE_FLOOR.json
```

A regra geral é:

```text
observado >= mínimo versionado
```

Para a suíte de testes, há uma regra adicional:

```text
tests_run == tests_discovered
```

Portanto, o gate exige simultaneamente:

```yaml
test_file_count: ">= 7"
tests_discovered: ">= 58"
tests_run: ">= 58"
complete_execution: true
tests_run_equals_tests_discovered: true
failures: 0
errors: 0
```

Os 58 testes representam a superfície governada declarada na PR #48. Enquanto o gate integral não for executado, esse número é uma exigência a provar, não uma afirmação de PASS.

```yaml
full_gate_execution: TOKEN_VAZIO
claim_allowed: false
```

## 3. Execução no Termux

Na raiz do repositório:

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

## 4. Etapas

```text
1. compilar validadores, avaliadores, comparador e testes
2. validar schema, piso e fixtures JSON
3. validar parse dos registries JSONL
4. descobrir, contar e executar a suíte governada
5. gerar relatórios de records e registry
6. validar a cadeia de custódia append-only
7. comparar resultados com o piso v2
8. exigir execução completa e bloquear promoção indevida
9. selar cinco relatórios, manifesto e checksums SHA-256
```

## 5. Pacote produzido

```text
cross-source-test-validation.json
cross-source-record-validation.json
cross-source-registry-validation.json
chain-of-custody-validation.json
quality-floor-validation.json
LOCAL_GATE_STATUS.json
CHECKSUMS.sha256
```

### Relatório de testes

```yaml
schema_version: rafaelia.cross-source-test-report/v3
status: PASS
test_file_count: ">= 7"
tests_discovered: ">= 58"
tests_run: ">= 58"
complete_execution: true
failures: 0
errors: 0
claim_allowed: false
remote_ci_substituted: false
```

### Relatório do registry

O caminho é normalizado para permitir hashes idênticos em checkouts diferentes:

```yaml
registry: indices/CROSS_SOURCE_REGISTRY.jsonl
status: PASS
record_count: ">= 10"
provider_counts:
  github: ">= 2"
  google_drive: ">= 8"
defect_count: 0
claim_allowed: false
```

### Relatório da cadeia de custódia

```yaml
status: PASS
event_count: ">= 13"
defect_count: 0
claim_allowed: false
```

### Avaliação do piso

```yaml
schema_version: rafaelia.cross-source-gate-evaluation/v2
status: PASS
failed_check_count: 0
promotion_state: LOCAL_PASS_REMOTE_TOKEN_VAZIO
claim_allowed: false
remote_ci_substituted: false
```

### Manifesto selado

```yaml
schema_version: rafaelia.cross-source-local-gate/v3
status: PASS
test_file_count: valor_observado
minimum_test_file_count: 7
test_count_discovered: valor_descoberto
test_count_observed: valor_executado
minimum_test_count: 58
complete_test_execution: true
report_count: 5
quality_floor:
  path: indices/CROSS_SOURCE_GATE_FLOOR.json
  schema_version: rafaelia.cross-source-gate-floor/v2
  sha256: valor_calculado
  status: PASS
quality_floor_status: PASS
promotion_state: LOCAL_PASS_REMOTE_TOKEN_VAZIO
claim_allowed: false
remote_ci_substituted: false
```

## 6. O que o PASS local significa

```yaml
significa:
  - sete ou mais arquivos de teste governados descobertos
  - cinquenta_e_oito ou mais testes descobertos
  - todos os testes descobertos executados
  - zero falhas e zero erros
  - registry e custódia acima do piso
  - cinco relatórios selados
  - nenhum claim promovido
nao_significa:
  - CI remota aprovada
  - executor remoto autenticado pelo hash
  - sincronização automática implementada
  - certificação externa
  - merge autorizado
```

## 7. Segurança

O executor local é protegido contra:

- comandos de rede;
- mutação Git;
- `sudo`;
- `rm -rf`;
- GitHub CLI;
- escrita fora do diretório de artefatos;
- bytecode Python na árvore versionada;
- redução silenciosa do piso;
- execução parcial apresentada como completa.

## 8. Comparação Termux ↔ Actions

Depois de existir artifact remoto real:

```sh
python3 scripts/compare_cross_source_evidence.py \
  --left .artifacts/cross-source-local \
  --right .artifacts/cross-source-remote \
  --write-report .artifacts/cross-source-comparison.json
```

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
claim_allowed: false
```

## 9. Próximo passo verificável

1. executar o gate no checkout integral do Termux;
2. confirmar sete arquivos e 58/58 testes ou mais;
3. preservar os cinco relatórios, manifesto e checksums;
4. restaurar o início do runner privado;
5. obter artifact remoto associado ao commit exato;
6. comparar os pacotes;
7. anexar evento `VALIDATE` à cadeia;
8. somente então avaliar saída de `DRAFT`.

---

```text
Piso = memória mínima
Descoberto = superfície reconhecida
Executado = superfície realmente percorrida
Descoberto == Executado = completude operacional
Tempo sem evidência = TOKEN_VAZIO
```
