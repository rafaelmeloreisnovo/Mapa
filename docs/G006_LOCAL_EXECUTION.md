# G006 — execução local observável em Termux/Linux

## Objetivo

Executar o gate de claims sem depender de GitHub Actions, produzindo recibos
pinados ao commit, logs, relatórios e checksums. O procedimento não promove
claims e não fecha automaticamente o portfólio.

## Pré-condições

```text
clone integral do rafaelmeloreisnovo/Mapa
Python 3.10+
git disponível
working tree limpa
commit esperado conhecido
```

Confirme antes da execução:

```bash
git status --short
git rev-parse HEAD
```

O commit observado deve coincidir com o commit que será informado ao runner.
Não use um valor calculado silenciosamente como substituto de revisão humana.

## Materialização GitHub fail-closed

Para arquivos privados ou respostas diretas truncadas, o materializador usa a
API de conteúdo do GitHub, decodifica Base64, calcula a identidade de objeto Git
e só grava o arquivo depois que todas as verificações passam.

### Token sem eco

```bash
read -rsp 'GitHub token: ' GITHUB_TOKEN
printf '\n'
export GITHUB_TOKEN
```

O token não é colocado nos argumentos, no recibo ou nos logs do programa.
Depois da operação:

```bash
unset GITHUB_TOKEN
```

### Reprodução do CC028

```bash
mkdir -p .evidence/g006

python3 tools/materialize_github_blob.py \
  --repository rafaelmeloreisnovo/Mapa \
  --path indices/REPOSITORY_INVENTORY.json \
  --ref 4016c51e024573a3875457fceb6d05926e07a07b \
  --expected-blob-sha1 b43554096f00c0918997dd9f9b11787cec4d4e52 \
  --expected-size 19542 \
  --expected-sha256 b19d27084e5be35a2597f07346450745abfd7084c0a831b48e0eef4c57058e02 \
  --output .evidence/g006/REPOSITORY_INVENTORY.json \
  --receipt .evidence/g006/CC028-materialization-receipt.json
```

O materializador:

```text
rejeita encoding diferente de Base64
rejeita SHA Git divergente
rejeita tamanho divergente
rejeita SHA-256 divergente
escreve por arquivo temporário + fsync + replace
usa modo 0600
não registra a credencial
mantém claim_allowed=false
```

## Runner local do gate

Defina explicitamente o commit revisado:

```bash
EXPECTED_COMMIT='<sha-de-40-caracteres-revisado>'
```

Execute:

```bash
python3 scripts/run_g006_local_gate.py \
  --root . \
  --output-dir ".evidence/g006/${EXPECTED_COMMIT}" \
  --expected-commit "${EXPECTED_COMMIT}"
```

Sem `--allow-dirty`, o runner rejeita uma árvore modificada. A opção existe
somente para diagnóstico; um recibo dirty não deve ser usado como evidência de
release ou integração.

## Cadeia executada pelo runner

```text
observar commit e limpeza Git
→ py_compile dos validadores e testes G006
→ executar suítes positivas e adversariais
→ scanner de vocabulário
→ ledger-base
→ cadeia de três lotes
→ residual histórico + resolução CC028
→ precisão substring/token exato
→ verificar invariantes 36/36
→ gerar checksums dos controles
→ preservar stdout/stderr por comando
→ emitir recibo agregado BLAKE2b-256
```

## Saídas

```text
claim-vocabulary-validation.json
claim-contradiction-ledger-validation.json
claim-review-chain-validation.json
claim-review-residual-validation.json
claim-discovery-precision-validation.json
G006_CHECKSUMS.sha256
logs/*.stdout.log
logs/*.stderr.log
g006-local-gate-receipt.json
```

Os arquivos são escritos em modo `0600` pelo runner.

## Validação do recibo auxiliar já existente

```bash
python3 scripts/validate_g006_auxiliary_receipt.py \
  --receipt resultados/G006_AUXILIARY_LOCAL_VALIDATION_2026-07-21.json \
  --root . \
  --write-report .evidence/g006/auxiliary-receipt-validation.json
```

Esse recibo cobre apenas o materializador e o runner como componentes isolados:

```text
py_compile = 4 arquivos PASS
unittest   = 15/15 PASS
```

Ele não afirma execução da suíte integral do control plane. O validador do
recibo possui ainda uma suíte adversarial própria, executada separadamente com
6/6 testes PASS no ambiente de preparação.

## Critérios do recibo local válido

```text
commit observado = commit esperado
working tree dirty = false
todos os comandos returncode = 0
cinco relatórios status = PASS
reviewed safe = 36
reviewed blocking = 0
current residual = 0
CC028 exact strong tokens = 0
claim_allowed = false
certification_claim = false
```

## Limites

Um recibo local válido demonstra a execução naquele commit, runtime e máquina.
Ele não demonstra:

- execução em GitHub Actions;
- revisão independente;
- ausência de candidatos posteriores ao snapshot sem scope refresh;
- conformidade ou certificação;
- fechamento dos 126 repositórios.

```text
local PASS != remote PASS
snapshot review != current portfolio scan
Mapa closure != portfolio closure
```

## Rollback e custódia

Para remover uma execução local, apague somente o diretório de saída criado para
o commit. Não altere os ledgers versionados nem reescreva recibos históricos.

Para atualizar o controle:

```text
novo commit
→ nova execução
→ novo diretório de evidência
→ novo recibo
```

Nunca reutilize um recibo anterior depois de alterar qualquer arquivo ligado aos
checksums.
