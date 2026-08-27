# Protocolo de Execução Semântica Contextual RAFAELIA v1

## Tese operacional

Uma resposta pode ser linguisticamente plausível e estruturalmente errada quando o fragmento depende de memória não recuperada, o rótulo é confundido com definição, camadas são fundidas ou confiança verbal substitui evidência.

O protocolo não altera pesos internos, atenção nativa ou tokenização privada de um modelo. Ele governa a camada externa e auditável:

```text
consulta
→ recuperação autorizada
→ fontes observadas
→ claims de memória com proveniência
→ entidades e relações
→ separação de camadas
→ hipóteses concorrentes
→ TOKEN_VAZIO tipado
→ gate da resposta
```

## Ponte para tokenização, embeddings e pesos

O `Model Semantic Context Rapport V1` torna a fronteira acima endereçável:

```text
texto observado
→ tokenizer/IDs [produtor ou TOKEN_VAZIO]
→ embeddings/camadas/pesos/ativações [produtor ou TOKEN_VAZIO]
→ saída observada
→ interpretação semântica externa
```

Contrato: `contracts/model-semantic-rapport.v1.json`.
Documento: `docs/architecture/MODEL_SEMANTIC_CONTEXT_RAPPORT_V1.md`.

Invariantes adicionais:

```text
semantic_token != tokenizer_token_id
external_semantic_vector != native_model_embedding
tensor != weight
context_conditioning != parameter_training
```

`LNN` permanece ambígua até declarar se significa uma rede Liquid
Time-constant ou uma Logical Neural Network. `LLM` descreve classe de
capacidade/escala e não prova, isoladamente, uma arquitetura Transformer.

## Invariante

\[
I_{sem}=O\times A\times P\times L\times E\times G
\]

- `O`: origem observada;
- `A`: autorização;
- `P`: proveniência;
- `L`: coerência entre camadas;
- `E`: evidência;
- `G`: gate.

Quando um termo necessário falta, a explicação pode continuar limitada, mas cálculo, causalidade ou execução ficam bloqueados.

## Três classes de memória

1. **Disponível:** claim e fonte recuperados.
2. **Alegada:** o usuário ou sistema lembra, mas a fonte não foi observada.
3. **Ausente:** não há claim nem fonte recuperável.

```text
lembrar != observar
observar != provar
provar localmente != generalizar
```

## Exemplo “Fórmula Vinho”

A expressão não é uma keyword autossuficiente. O pacote separa a cadeia candidata:

```text
clima / meteorologia
→ fenologia
→ rendimento e qualidade
→ mediações de mercado
→ preço
```

Isso permanece hipótese até recuperar origem, bibliografia, dados, unidades, baseline e falsificador.

## Proteção contra persuasão sem prova

O protocolo não atribui intenção psicológica. Ele reduz efeitos de invalidação por quatro controles:

- afirmação material referencia fonte observada;
- interpretação é marcada como interpretação;
- confiança não substitui evidência;
- acolhimento não promove claim.

## Uso

```bash
python3 scripts/validate_contextual_semantic_packet.py examples/contextual-semantic-packet.wine-formula.json
python3 -m unittest tests.test_contextual_semantic_packet
```

## R3

```text
F_ok   = contrato, camadas, proveniência, gaps e gate fail-closed
F_gap  = recuperação real das fontes e benchmark com casos do projeto
F_next = executar sobre 10 fragmentos dependentes de memória e medir reconstrução
```
