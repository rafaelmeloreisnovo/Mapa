# Sementeira — Mapa de Sustentação Contextual 5×7 V1

Estado: `IMPLEMENTED_LOCAL / CLAIM_ALLOWED=false / NO_NEW_WORKFLOW`

## Finalidade

Materializar o protocolo cognitivo em um contrato executável que limite a superfície humana a cinco variáveis e atravesse sete direções epistemológicas antes de produzir um receipt.

```text
prompt/snapshot
→ origem e delta
→ cinco variáveis humanas
→ sete direções
→ claims + evidências
→ gate fail-closed
→ receipt SHA-256
→ F_ok / F_gap / F_next
```

## Cinco variáveis humanas

1. `intention`
2. `evidence`
3. `human_state`
4. `execution_capacity`
5. `next_falsifiable_gate`

A limitação é de interface cognitiva, não de profundidade interna. `human_state` pode modificar prioridade, tamanho, ritmo e segurança da resposta, mas não conta como evidência de um claim.

## Sete direções

1. `fact`
2. `gap`
3. `invariant`
4. `variant`
5. `proof_or_falsifier`
6. `parable`
7. `feedback`

A parábola permanece marcada como explicação; não promove mecanismo físico ou claim científico.

## TOKEN_VAZIO

```text
TOKEN_VAZIO != 0
TOKEN_VAZIO != false
TOKEN_VAZIO != not_applicable
TOKEN_VAZIO != licença para preencher
```

Um objeto em `TOKEN_VAZIO*` deve conservar `value=null` e `weight=null` quando a quantidade ainda não foi observada ou calibrada.

Peso de evidência atual:

```text
W_claim(TOKEN_VAZIO) = 0
```

Valor prospectivo pode ser não nulo, porém precisa permanecer separado do peso probatório.

## Gate de promoção

Um claim só alcança `LOCAL_EVIDENCE_CANDIDATE` quando possui:

```text
SOURCE + METHOD + TEST_RECEIPT + falsifier
```

Replicação exige ainda:

```text
REPLICATION independente
```

Mesmo nesses estados, o motor mantém:

```text
claim_allowed=false
```

A promoção final pertence a um gate posterior, específico do domínio.

## Pesos

Pesos numéricos são bloqueados sem `calibration_receipt_ref`. Elegância, repetição, emoção ou concordância não são calibração.

## Uso

```bash
python3 scripts/sementeira_cognitive_gate.py \
  examples/sementeira-cognitive-gate-example.json \
  --output auditoria/SEMENTEIRA_5X7_LOCAL_RECEIPT_2026-07-27.json \
  --strict

python3 -m unittest discover -s tests -p 'test_sementeira_cognitive_gate.py' -v
```

## Invariantes

- exatamente cinco variáveis humanas;
- exatamente sete direções;
- ausência não vira zero;
- emoção não vira evidência;
- claim sem falsificador permanece lacuna de teste;
- duplicidade ou referência ausente bloqueia o gate;
- receipt é determinístico para o mesmo input;
- nenhum YAML, execução automática, merge ou publicação é criado por este pacote.

## Parábola

O carpinteiro mantém muitas medidas na oficina, mas entrega ao aprendiz apenas as cinco necessárias para o próximo corte. A régua não inventa a madeira ausente e o sino não transforma uma mesa incompleta em obra concluída.

## R₃

- `F_ok`: contrato, motor, exemplo, schema e testes locais materializados.
- `F_gap`: ground truth, pesos, limiares e revisão independente permanecem `TOKEN_VAZIO_CALIBRATION`.
- `F_next`: congelar um pequeno corpus rotulado e medir falsos positivos, falsos negativos e concordância entre revisores.
