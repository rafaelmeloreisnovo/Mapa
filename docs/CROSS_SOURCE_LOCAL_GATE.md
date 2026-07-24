# Gate Local Cross-Source — Termux e Python 3

```yaml
schema: rafaelia.cross-source-local-gate-guide/v2
mode: OFFLINE
network_required: false
third_party_python_dependencies: false
quality_model: growth_safe_floor
claim_allowed: false
remote_ci_substituted: false
```

## Finalidade

Este gate reproduz localmente as validações estruturais da camada GitHub ↔ Google Drive e da cadeia de custódia, sem acessar rede, Drive ou GitHub durante a execução.

Ele verifica somente os artefatos já versionados no checkout atual:

- JSON Schema do registro cross-source;
- fixtures válidas e inválida;
- registry cross-source JSONL;
- ledger append-only de cadeia de custódia;
- invariantes semânticas de `TOKEN_VAZIO`;
- integridade do grafo e encadeamento temporal;
- contrato de segurança do próprio executor local;
- quantidade de testes realmente executada;
- piso de não regressão versionado.

O resultado local é evidência de reprodução estrutural. Ele **não substitui** o GitHub Actions e não autoriza merge sozinho.

## Problema que o piso resolve

Um gate não pode congelar um mapa vivo em números exatos. Por exemplo, exigir sempre exatamente dez registros faria uma expansão válida para onze registros falhar.

O arquivo `indices/CROSS_SOURCE_GATE_FLOOR.json` registra mínimos aceitos a partir do último snapshot fundido e validado:

```yaml
comparison: observed >= minimum
minimums:
  tests_run: 38
  valid_fixtures: 2
  invalid_fixtures: 1
  registry_records: 10
  provider_counts:
    github: 2
    google_drive: 8
  custody_events: 13
```

Assim:

- crescimento append-only é aceito;
- redução silenciosa é bloqueada;
- o número de testes é medido, não escrito manualmente;
- qualquer redução deliberada do piso exige revisão em mudança separada;
- `claim_allowed=false` permanece obrigatório.

## Execução no Termux

A partir da raiz do repositório:

```sh
sh scripts/run_cross_source_gate.sh
```

Diretório de saída padrão:

```text
.artifacts/cross-source-local/
```

Também é possível escolher outro diretório:

```sh
sh scripts/run_cross_source_gate.sh "$HOME/storage/shared/RAFAELIA_EVIDENCE/cross-source"
```

## Etapas executadas

```text
1. py_compile dos validadores, avaliadores e testes
2. parse do schema, piso e fixtures JSON
3. parse integral dos dois arquivos JSONL
4. execução e medição da suíte canônica
5. geração dos relatórios cross-source
6. validação e relatório da cadeia de custódia
7. comparação dos resultados com o piso de não regressão
8. verificação da fronteira claim_allowed=false
9. geração de manifesto e checksums SHA-256
```

O bytecode Python é redirecionado para o diretório de artefatos, evitando alteração acidental da árvore versionada.

## Artefatos produzidos

### `cross-source-test-validation.json`

Evidência medida da suíte canônica:

```yaml
status: PASS
tests_run: valor_observado
failures: 0
errors: 0
claim_allowed: false
remote_ci_substituted: false
```

O gate exige:

```text
tests_run >= CROSS_SOURCE_GATE_FLOOR.minimums.tests_run
```

Adicionar testes não exige editar um número fixo no executor.

### `cross-source-record-validation.json`

Validação das fixtures positivas e negativa.

Critérios essenciais:

```yaml
status: PASS
valid_fixture_count: >= piso
invalid_fixture_count: >= piso
unexpected_failures: 0
unexpected_passes: 0
claim_allowed: false
```

### `cross-source-registry-validation.json`

Validação do grafo completo.

Critérios essenciais:

```yaml
status: PASS
record_count: >= 10
provider_counts:
  github: >= 2
  google_drive: >= 8
defect_count: 0
claim_allowed: false
```

Esses valores são o piso atual, não um teto. Novos repositórios, documentos e relações podem ser anexados sem quebrar o gate.

### `chain-of-custody-validation.json`

Validação do ledger append-only:

```yaml
status: PASS
event_count: >= 13
defect_count: 0
claim_allowed: false
```

O relatório exige:

- IDs de evento únicos;
- timestamps UTC monotônicos;
- `previous_event_id` apontando para o evento válido imediatamente anterior;
- hash canônico correto quando declarado;
- objeto versionado existente;
- `TOKEN_VAZIO` sem promoção de claim.

### `quality-floor-validation.json`

Compara os quatro relatórios anteriores com o piso versionado.

```yaml
status: PASS
failed_check_count: 0
comparison: observed_greater_than_or_equal_to_minimum
promotion_state: LOCAL_PASS_REMOTE_TOKEN_VAZIO
claim_allowed: false
remote_ci_substituted: false
```

`LOCAL_PASS_REMOTE_TOKEN_VAZIO` significa:

- a reprodução local passou;
- o piso de não regressão foi preservado;
- a confirmação remota independente continua ausente;
- nenhuma promoção de claim foi autorizada.

### `LOCAL_GATE_STATUS.json`

Manifesto do ambiente e dos relatórios:

```yaml
schema_version: rafaelia.cross-source-local-gate/v2
status: PASS
test_count_observed: valor_medido
minimum_test_count: 38
report_count: 5
quality_floor_status: PASS
promotion_state: LOCAL_PASS_REMOTE_TOKEN_VAZIO
claim_allowed: false
remote_ci_substituted: false
```

O manifesto também registra o SHA-256 do piso usado, impedindo ambiguidade sobre qual baseline governou a execução.

### `CHECKSUMS.sha256`

Hashes SHA-256 dos cinco relatórios principais.

Verificação manual:

```sh
cd .artifacts/cross-source-local
sha256sum -c CHECKSUMS.sha256
```

## Segurança

O script é protegido por testes estáticos que rejeitam comandos de:

- rede (`curl`, `wget`);
- mutação Git (`git push`, `git commit`, `git reset`);
- exclusão ampla (`rm -rf`);
- privilégio (`sudo`);
- GitHub CLI (`gh`).

Ele não altera:

- Google Drive;
- branches;
- commits;
- pull requests;
- configurações da conta;
- arquivos versionados.

Somente o diretório de saída é criado ou atualizado.

## Interpretação

```yaml
local_status_PASS:
  significa:
    - estrutura e custódia reproduzidas localmente
    - testes medidos acima do piso
    - mapa livre para crescer sem redução silenciosa
  nao_significa:
    - CI remota aprovada
    - sincronizacao automatica implementada
    - claim cientifico validado
    - merge autorizado
remote_status_TOKEN_VAZIO:
  acao: preservar contexto e corrigir o bloqueio do runner
```

## Alteração legítima do piso

O piso não deve ser reduzido no mesmo commit que remove registros, provedores, eventos ou testes.

Uma alteração legítima exige:

1. justificativa explícita;
2. diff isolado de `CROSS_SOURCE_GATE_FLOOR.json`;
3. evidência de que a redução não apagou custódia ou conhecimento;
4. revisão humana;
5. novo evento append-only, quando aplicável.

Sem isso, a redução é tratada como regressão.

## Próximo passo depois do PASS local

1. preservar `LOCAL_GATE_STATUS.json` e `CHECKSUMS.sha256`;
2. restaurar a inicialização do GitHub Actions em repositórios privados;
3. executar `Actions Runner Smoke` até aparecer `RUNNER_STARTED=true`;
4. executar `Cross-Source Record Validation`;
5. comparar os cinco relatórios locais e remotos;
6. anexar um novo evento `VALIDATE` à cadeia, sem reescrever o evento de merge;
7. somente então avaliar a saída de `DRAFT`.

---

```text
Piso = memória mínima verificável
Crescimento = permitido
Regressão silenciosa = bloqueada
Local = reprodução
Custódia = história imutável
Remoto = confirmação independente
Merge = decisão governada
```
