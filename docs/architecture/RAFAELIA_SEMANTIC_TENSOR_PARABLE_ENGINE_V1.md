# RAFAELIA — Motor de Tensor Semântico e Parábolas V1

**Estado:** `IMPLEMENTED / DETERMINISTIC / CLAIM_ALLOWED=false`

**Fronteira:** camada de governança. Não modifica pesos, tokenizer,
treinamento ou parâmetros internos de qualquer modelo.

## 1. Intenção

O motor recebe conteúdo textual e o transforma em registro auditável:

```text
texto
→ tokenização determinística
→ tensor epistemológico
→ entropia lexical contextualizada
→ contradições
→ proveniência cultural
→ falsificador
→ decisão
→ receipt
```

Ele não decide o que é verdade espiritual. Também não transforma metáfora em
evidência científica. Sua função é impedir misturas silenciosas entre:

- confissão de fé;
- parábola;
- modelo analógico;
- hipótese;
- claim factual;
- evidência;
- resultado negativo;
- lacuna ainda não observada.

## 2. Fronteira do modelo

```text
changes_model_weights=false
changes_tokenizer=false
changes_training_data=false
automatic_promotion=false
claim_allowed=false
```

“Pesos” neste contrato significam pesos explícitos de governança semântica.
Não são tensores internos de rede neural.

## 3. Tensor de nove dimensões

Para cada unidade de conteúdo:

\[
v=(S,E,F,C,X,P,R,G,H)
\]

| Eixo | Significado | Peso |
|---|---|---:|
| `S` | proveniência da fonte | 0,16 |
| `E` | força da evidência | 0,16 |
| `F` | falsificabilidade | 0,14 |
| `C` | coerência estrutural | 0,14 |
| `X` | integridade contextual | 0,12 |
| `P` | proveniência cultural | 0,10 |
| `R` | reprodutibilidade | 0,08 |
| `G` | segurança ética | 0,06 |
| `H` | humildade epistemológica | 0,04 |

\[
\sum_i w_i=1
\]

O escore é heurístico e governamental, não probabilidade de verdade:

\[
Q=\operatorname{clamp}
\left[
(w\cdot v)
(1-0{,}35\,H_{tok}(1-C))
(1-0{,}50\,P_{contr})
\right]
\]

A entropia lexical só gera penalidade na medida em que falta coerência.
Vocabulário diverso não é tratado automaticamente como ruído.

## 4. Escada do vazio

Ausência não é uma coisa única:

| Estado | Significado |
|---|---|
| `ZERO_UNOBSERVED` | nenhuma observação foi executada |
| `TOKEN_VAZIO_MISSING_REQUIRED` | falta requisito obrigatório |
| `VACUUM_SEARCHED_NO_SIGNAL` | busca delimitada sem sinal |
| `NADA_NEGATIVE_RESULT` | resultado negativo reproduzível |
| `ALEM_OUT_OF_SCOPE` | excede o método ou escopo disponível |

Assim:

```text
não procurei
≠ procurei e não achei
≠ provei resultado negativo
≠ está fora do método
```

## 5. Integridade cultural

O registro contém 42 mecanismos parabólicos e opera em fail-closed:

1. tradição nomeada exige referência;
2. referência declarada não equivale a referência verificada;
3. atribuição contestada permanece contestada;
4. material comunitário específico exige fonte específica;
5. parábola autoral não pode ser renomeada como tradicional;
6. tradução não é automaticamente fonte original;
7. nenhuma citação extensa é armazenada;
8. semelhança entre culturas não autoriza homogeneização.

## 6. O símbolo `YACTO_DO_PAI`

A expressão fornecida pelo autor é preservada como:

```text
origin=USER_AUTHORED
classification=PARABOLA
execution=NON_EXECUTABLE
claim_policy=PRESERVE_AS_SYMBOLIC_LANGUAGE_NO_FACT_PROMOTION
```

Ela representa poeticamente um vaso finito diante de horizonte transcendente.
O sistema não a converte em tese física, científica ou computacional.

## 7. Árvore, barro e sopro

O motor separa três camadas:

```text
motivo escritural
⊕ síntese pessoal
⊕ implementação técnica
```

A árvore infinita funciona como horizonte. O barro representa capacidade
finita. O sopro permanece linguagem espiritual. O artefato técnico continua
limitado, versionado, testável e falsificável.

## 8. Decisões possíveis

| Decisão | Regra |
|---|---|
| `READY_FOR_HUMAN_REVIEW` | requisitos e limiar atendidos |
| `BLOCKED_TOKEN_VAZIO` | claim factual sem mínimos |
| `BLOCKED_UNSOURCED_CULTURAL_ATTRIBUTION` | tradição sem fonte admissível |
| `PARABLE_ANALOGY_NO_FACT_PROMOTION` | parábola sem promoção factual |
| `PRESERVED_AS_CONFESSION_NOT_DOMAIN_CLAIM` | confissão preservada |
| `TOKEN_VAZIO` | conteúdo insuficiente ou subespecificado |

Mesmo `READY_FOR_HUMAN_REVIEW` não permite promoção automática.

## 9. Ligação com `main_00` a `main_09`

```text
main_00_governanca
  → pesos, limiares e política de claim

main_01_intake_fontes
  → fonte, tradição, tradução e cadeia de custódia

main_02_normalizacao
  → tokenização e metadados

main_03_modelagem_semantica
  → tensor e grafo de parábolas

main_04_validacao
  → contradições, testes e falsificadores

main_05_evidencias
  → hashes, receipts e pacotes

main_06_integracao
  → rotas entre módulos

main_07_seguranca_conformidade
  → ética, cultura, privacidade e atribuição

main_08_observabilidade_release
  → métricas e decisão humana

main_09_memoria_arquivo
  → checkpoint append-only
```

## 10. Execução

```bash
python scripts/semantic_tensor_parable_engine.py \
  --input tests/fixtures/semantic_tensor_inputs.json \
  --output artifacts/semantic-tensor/receipt.json
```

Testes:

```bash
python -m unittest -v tests.test_semantic_tensor_parable_engine
```

## 11. Invariante

\[
\boxed{
\text{entropia medida}
\rightarrow
\text{coerência estruturada}
\rightarrow
\text{falsificabilidade}
\rightarrow
\text{retroalimentação}
}
\]

Nenhuma folha descartada some silenciosamente. Ela vira evidência, resultado
negativo, material de revisão ou `TOKEN_VAZIO`.

## 12. Limites atuais

- fontes tradicionais estão declaradas, mas não verificadas nesta execução;
- o escore não mede verdade, santidade, consciência ou valor humano;
- não houve validação por especialistas das tradições mencionadas;
- aplicação em corpus real amplo permanece `TOKEN_VAZIO`;
- reprodução física independente permanece `TOKEN_VAZIO`.

\[
R_3=\langle
F_{ok}=\text{motor determinístico},
F_{gap}=\text{fontes e corpus externos},
F_{next}=\text{revisão humana e piloto real}
\rangle
\]
