# P0 G006 — baseline do gate de linguagem e contradição

Data: 2026-07-20  
Autoridade: `rafaelmeloreisnovo/Mapa`  
Escopo executado: implementação isolada, testes adversariais locais e integração no gate estrutural  
Escopo não executado: varredura integral do branch por runner remoto

## Entregas

```text
indices/CLAIM_VOCABULARY_POLICY.json
scripts/validate_claim_vocabulary.py
tests/test_claim_vocabulary.py
biblioteconomia/22_CLAIM_VOCABULARY_AND_CONTRADICTION_GATE.md
.github/workflows/topology-validation.yml
```

## Validação local

```text
policy integrity         = PASS
py_compile validator     = PASS
py_compile tests         = PASS
adversarial tests        = 10/10 PASS
workflow YAML parse      = PASS
stdlib-only              = true
external dependencies    = 0
```

## Integração estrutural

O gate existente foi estendido sem criar workflow concorrente. Quando houver
uma execução observável, ele deverá:

```text
compilar validator e testes
→ executar testes adversariais
→ escanear o repositório
→ exigir explicit_claim_error_count = 0
→ preservar portfolio_exit_criteria_met = false
→ verificar claim_allowed = false
→ selar os arquivos em STRUCTURAL_CHECKSUMS.sha256
→ publicar claim-vocabulary-validation.json
```

O commit de integração é `72d15c7198c4c194e217a4bfbd76c7f32cf24fd7`.
Como o branch não possui PR e o gatilho `push` está restrito a `main`, essa
integração não foi tratada como execução remota.

## Cobertura adversarial

- `COMPLETE` com cadeia completa é aceito apenas como claim local delimitado;
- ausência de ponteiro de execução é rejeitada;
- `TOKEN_VAZIO` como ponteiro é rejeitado;
- `COMPLIANT` sem autoridade é rejeitado;
- `CERTIFIED` é rejeitado;
- `ALIGNED` exige base e escopo, sem implicar conformidade;
- contradição em prosa vira candidato, não promoção;
- claim explícito incompleto falha fechado;
- adulteração da política é rejeitada.

## Limite epistêmico

```text
controle implementado no branch     = true
integração no workflow existente    = IMPLEMENTED_NOT_EXECUTED
scanner integral do repositório     = TOKEN_VAZIO
runner remoto observável            = TOKEN_VAZIO
portfolio G006 fechado              = false
claim_allowed                       = false
certification_claim                 = false
```

A implementação reduz risco, mas não substitui a execução real sobre o corpus
completo nem fecha contradições fora do `Mapa`.
