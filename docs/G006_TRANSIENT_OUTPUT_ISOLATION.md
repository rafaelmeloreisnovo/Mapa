# G006 — isolamento obrigatório de saídas transitórias

## Autoridade operacional

Este documento supersede exemplos anteriores que colocam `.evidence/` dentro do
clone durante a execução do scanner G006.

```text
saída dentro da árvore escaneada = proibida para recibo canônico
saída em diretório temporário externo = obrigatória
```

A razão é evitar autorreferência: uma segunda execução poderia ler relatórios da
execução anterior e incorporá-los às métricas de descoberta.

## Rota recomendada

```bash
sh scripts/run_g006_isolated.sh '<sha-de-40-caracteres>'
```

Sem argumento, o wrapper observa `git rev-parse HEAD` e usa esse commit como
identidade esperada.

A saída é criada em:

```text
${TMPDIR:-/tmp}/mapa-g006-audit/<commit>/
```

O wrapper rejeita:

- commit vazio, curto, não hexadecimal ou com letras maiúsculas;
- `TMPDIR` localizado dentro do repositório;
- reutilização de diretório de evidência existente;
- continuação depois de qualquer erro do runner.

## Invariantes

```text
output_dir ∉ repository_root
output_dir novo por execução
umask = 077
working tree limpa
commit observado = commit esperado
recibo anterior = imutável
```

O runner interno permanece `scripts/run_g006_local_gate.py`. O wrapper apenas
resolve e protege o local de saída; ele não muda a semântica do gate.

## Refresh do escopo

Depois do runner, use o mesmo diretório externo:

```bash
AUDIT_DIR="${TMPDIR:-/tmp}/mapa-g006-audit/<commit>"

python3 scripts/validate_claim_resolution_contract.py \
  --path indices/CLAIM_REVIEW_RESOLUTION_CC028.json \
  --write-report "$AUDIT_DIR/claim-resolution-contract-validation.json"

python3 scripts/build_claim_scope_refresh.py \
  --ledger indices/CLAIM_CONTRADICTION_LEDGER.json \
  --head indices/CLAIM_CONTRADICTION_HEAD.json \
  --claim-scan "$AUDIT_DIR/claim-vocabulary-validation.json" \
  --precision "$AUDIT_DIR/claim-discovery-precision-validation.json" \
  --current-commit '<commit>' \
  --write-report "$AUDIT_DIR/claim-scope-refresh-validation.json"

python3 scripts/validate_claim_scope_refresh.py \
  --path "$AUDIT_DIR/claim-scope-refresh-validation.json" \
  --write-report "$AUDIT_DIR/claim-scope-refresh-contract-validation.json"
```

## Limite

O isolamento impede contaminação por saídas anteriores. Ele não converte o scan
filtrado em varredura byte a byte e não autoriza claims.

```text
isolated execution = stronger receipt
isolated execution != portfolio closure
claim_allowed = false
certification_claim = false
```
