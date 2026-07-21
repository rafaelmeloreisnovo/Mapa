# P0 G006 — baseline do gate de linguagem e contradição

Data: 2026-07-20  
Autoridade: `rafaelmeloreisnovo/Mapa`  
Escopo executado: implementação isolada e testes adversariais locais  
Escopo não executado: varredura integral do branch remoto

## Entregas

```text
indices/CLAIM_VOCABULARY_POLICY.json
scripts/validate_claim_vocabulary.py
tests/test_claim_vocabulary.py
biblioteconomia/22_CLAIM_VOCABULARY_AND_CONTRADICTION_GATE.md
```

## Validação local

```text
policy integrity         = PASS
py_compile validator     = PASS
py_compile tests         = PASS
adversarial tests        = 10/10 PASS
stdlib-only              = true
external dependencies    = 0
```

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
scanner integral do repositório     = TOKEN_VAZIO
runner remoto observável            = TOKEN_VAZIO
portfolio G006 fechado              = false
claim_allowed                       = false
certification_claim                 = false
```

A implementação reduz risco, mas não substitui a execução real sobre o corpus
completo nem fecha contradições fora do `Mapa`.
