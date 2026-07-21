# Protocolo de Execução com Excelência

## Objetivo

Garantir que cada trabalho tenha entrada clara, processamento coerente, saída
verificável, cadeia de custódia e documentação evolutiva.

## Ciclo

1. Receber a entrada.
2. Identificar origem, responsável e referência.
3. Separar a unidade de trabalho.
4. Classificar o estado epistêmico.
5. Definir método, risco e critério de aceitação.
6. Executar a ação mínima verificável.
7. Validar a saída estrutural e semanticamente.
8. Registrar evidência, alteração e evento de custódia.
9. Registrar `TOKEN_VAZIO` quando faltar evidência suficiente.
10. Definir o próximo passo verificável.
11. Medir defeitos e retroalimentar o processo.

## Estados

| Estado | Definição | Claim |
|---|---|---|
| `FATO` | Item sustentado por evidência direta e referenciada. | permitido dentro do alcance da evidência |
| `HIPOTESE` | Item plausível ainda não demonstrado. | somente como hipótese |
| `SIMBOLICO` | Leitura filosófica ou espiritual, não prova experimental. | somente como simbólico |
| `TOKEN_VAZIO` | Evidência ainda insuficiente, com contexto preservado. | `claim_allowed=false` |
| `RISCO` | Ponto que pode gerar erro, dano, confusão ou falso positivo. | não aplicável |
| `ACAO` | Procedimento executável com entrada e critério de saída. | não aplicável |
| `RESULTADO` | Saída produzida, rastreável e sujeita a validação. | depende da evidência |

## Regra de `TOKEN_VAZIO`

Quando o tempo necessário ainda não produziu evidência suficiente:

```yaml
estado: TOKEN_VAZIO
claim_allowed: false
contexto_preservado: true
proximo_passo_verificavel: obrigatorio
```

A ausência não deve ser preenchida por inferência silenciosa. `TOKEN_VAZIO` é
estado válido, útil e auditável; não significa erro, descarte nem conclusão
negativa.

## Cadeia de custódia

Toda alteração material deve produzir ou referenciar um evento conforme:

- `governanca/CADEIA_DE_CUSTODIA_DADOS.md`;
- `schemas/cadeia_custodia_evento.schema.json`;
- `indices/CADEIA_CUSTODIA_EVENTOS.jsonl`;
- `scripts/validate_chain_of_custody.py`;
- `scripts/measure_custody_baseline.py`.

`previous_event_id` preserva o encadeamento linear entre eventos válidos.
Correções são append-only e usam `supersedes_event_id` para apontar o evento
corrigido sem apagar o histórico.

## Six Sigma / DMAIC

DMAIC é usado como método de melhoria, não como certificação automática:

- **Define:** escopo, usuário, defeito e risco;
- **Measure:** universo, oportunidades, baseline e qualidade da medição;
- **Analyze:** causas sustentadas, hipóteses e lacunas;
- **Improve:** mudança mínima, teste e rollback;
- **Control:** gate, métrica, amostragem e revisão.

DPMO observado pode ser medido em um snapshot piloto. Nível sigma e certificação
permanecem `TOKEN_VAZIO` até existir estabilidade do processo, janelas repetidas
e convenção estatística aprovada.

## Critério de excelência

Uma saída só pode ser considerada completa quando responde:

- O que foi usado?
- De onde veio?
- Quem ou qual serviço executou?
- O que foi feito?
- O que mudou?
- Qual evidência sustenta o resultado?
- Qual estado epistêmico foi atribuído?
- O que não foi possível confirmar?
- Qual risco residual permanece?
- Qual é a próxima ação verificável?

## Gates mínimos

```bash
python3 -S scripts/validate_chain_of_custody.py \
  indices/CADEIA_CUSTODIA_EVENTOS.jsonl --repo-root .

python3 -S -m unittest discover -s tests -p 'test_*.py'

python3 -S scripts/measure_custody_baseline.py \
  indices/CADEIA_CUSTODIA_EVENTOS.jsonl --repo-root .
```

A execução observada deve ser registrada em
`auditoria/PR39_EXECUTION_EVIDENCE.json`. Falha em gate bloqueia claim, não apaga
o trabalho: registra defeito ou `TOKEN_VAZIO`, preserva o contexto e direciona a
correção.
