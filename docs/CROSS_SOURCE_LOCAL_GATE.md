# Gate Local Cross-Source — Termux e Python 3

```yaml
schema: rafaelia.cross-source-local-gate-guide/v1
mode: OFFLINE
network_required: false
third_party_python_dependencies: false
claim_allowed: false
remote_ci_substituted: false
```

## Finalidade

Este gate reproduz localmente as validações estruturais da camada GitHub ↔ Google Drive sem acessar rede, Drive ou GitHub durante a execução.

Ele verifica somente os artefatos já versionados no checkout atual:

- JSON Schema do registro cross-source;
- fixtures válidas e inválida;
- registry JSONL;
- invariantes semânticas de `TOKEN_VAZIO`;
- integridade do grafo;
- contrato de segurança do próprio executor local.

O resultado local é evidência de reprodução estrutural. Ele **não substitui** o GitHub Actions e não autoriza merge sozinho.

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
1. py_compile dos validadores e testes
2. parse do schema e fixtures JSON
3. parse integral do registry JSONL
4. execução de 22 testes
5. geração dos dois relatórios de validação
6. verificação da fronteira claim_allowed=false
7. geração de manifesto e checksums SHA-256
```

## Artefatos produzidos

### `cross-source-record-validation.json`

Validação das fixtures positivas e negativa.

Critérios essenciais:

```yaml
status: PASS
unexpected_failures: 0
unexpected_passes: 0
claim_allowed: false
```

### `cross-source-registry-validation.json`

Validação do grafo completo.

Critérios essenciais:

```yaml
status: PASS
record_count: 10
provider_counts:
  github: 2
  google_drive: 8
token_vazio_count: 1
defect_count: 0
claim_allowed: false
```

### `LOCAL_GATE_STATUS.json`

Manifesto do ambiente e dos relatórios:

```yaml
status: PASS
test_count_expected: 22
report_count: 2
claim_allowed: false
remote_ci_substituted: false
```

### `CHECKSUMS.sha256`

Hashes SHA-256 dos dois relatórios principais.

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
  significa: estrutura reproduzida no ambiente local
  nao_significa:
    - CI remota aprovada
    - sincronizacao automatica implementada
    - claim cientifico validado
    - merge autorizado
remote_status_TOKEN_VAZIO:
  acao: preservar contexto e corrigir o bloqueio do runner
```

## Próximo passo depois do PASS local

1. preservar `LOCAL_GATE_STATUS.json` e `CHECKSUMS.sha256`;
2. restaurar a inicialização do GitHub Actions em repositórios privados;
3. executar `Actions Runner Smoke` até aparecer `RUNNER_STARTED=true`;
4. executar `Cross-Source Record Validation`;
5. comparar os relatórios locais e remotos;
6. somente então avaliar a saída de `DRAFT`.

---

```text
Local = reprodução
Remoto = confirmação independente
Merge = somente após ambos produzirem evidência observável
```
