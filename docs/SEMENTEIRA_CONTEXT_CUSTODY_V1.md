# Sementeira — Motor de Custódia Contextual, Derivadas e Antiderivadas V1

**Estado:** `DRAFT_AUDITABLE`  
**Modo:** `BRAINSTORM_THEN_FALSIFY`  
**Execução automática:** não  
**Dependências externas:** nenhuma  
**Claim:** `claim_allowed=false`

## 1. Objeto

O Projeto Sementeira reúne conversas, arquivos e fontes compartilhadas entre sessões. Essas fontes podem orientar uma resposta, mas não devem ser confundidas automaticamente com memória validada, verdade factual ou estado interno demonstrável do Transformer.

A unidade de entrada é:

```text
SOURCE_SNAPSHOT
```

A unidade de trabalho é:

```text
BRAINSTORM_CANDIDATE
```

A unidade promovível no futuro é uma cápsula que tenha atravessado origem, transformação, oposição, falsificador, evidência e revisão.

```text
SOURCE_SNAPSHOT
→ BRAINSTORM_CANDIDATE
→ TESTABLE_CANDIDATE
→ TESTED_LOCAL
→ EVIDENCED
→ REPLICATED_OR_REFUTED
```

Nenhuma etapa pode ser pulada silenciosamente.

## 2. Invariantes

```text
source snapshot != validated memory
brainstorm != claim
derivative != causality
antiderivative != magical recovery of lost content
correlation != mechanism
symbolic != physical proof
TOKEN_VAZIO != zero
repetition != independent evidence
```

A fonte original deve permanecer acessível por:

```text
source_id
source_sha256
line_start
line_end
fragment_sha256
```

## 3. Derivada operacional

A derivada não tenta prever metafisicamente o futuro de uma ideia. Ela mede a mudança observável dentro de uma janela textual ou entre dois snapshots.

Para uma janela dividida em três terços:

\[
W=W_0\cup W_1\cup W_2
\]

são calculados:

- termos adicionados e removidos;
- Jaccard entre terços consecutivos;
- mudança de entropia lexical;
- invariantes mencionados;
- surgimento de novos vazios ou testes.

\[
D(W_t)=\Delta(tokens, relações, entropia, estados)
\]

Essa derivada produz uma **assinatura de mudança**, não uma prova causal.

## 4. Antiderivada operacional

A antiderivada é um retorno de proveniência:

\[
A^{-1}(evento)
=
\langle fonte, hash, linhas, hash\_do\_fragmento\rangle
\]

Ela responde:

- de qual fonte veio;
- qual trecho sustenta o evento;
- qual transformação foi aplicada;
- quais invariantes foram conservados;
- quais partes não podem ser reconstruídas.

O round-trip inicial prova apenas que a coordenada e o hash recuperam o mesmo fragmento. Não prova que uma síntese recompõe todo o significado original.

## 5. Tokenização evolutiva

O token não recebe um peso único e permanente. Ele atravessa estados:

```text
OBSERVED_LITERAL
→ NORMALIZED
→ CONNECTED
→ HYPOTHESIS
→ TEST_DEFINED
→ EVIDENCED | REFUTED | TOKEN_VAZIO
```

A evolução deve preservar:

```text
forma literal
forma normalizada
fonte
coordenada
relações
estado anterior
motivo da transição
próximo teste
```

Um token raro pode funcionar como ponte entre regiões. Frequência baixa não autoriza descarte.

## 6. Rapport e transdisciplinaridade

Uma ponte entre áreas só é admitida como relação metodológica inicial:

```text
METHOD_BRIDGE
ANALOGY
SHARED_INVARIANT
SHARED_MEASUREMENT_FORM
HEURISTIC_CORRELATION
```

Ela não vira automaticamente:

```text
PHYSICAL_EQUIVALENCE
HISTORICAL_EQUIVALENCE
THEOLOGICAL_EQUIVALENCE
CAUSAL_MECHANISM
```

Cada ponte deve declarar o eixo comum. Exemplos:

- origem e transformação;
- conservação e perda;
- repetição e memória;
- sinal, ruído e detecção;
- estabilidade e ruptura;
- compressão e reconstrução.

## 7. Correlações ocultas, anomalias e paradoxos

O motor pode sugerir relações quando houver:

- sobreposição lexical significativa;
- termos raros compartilhados;
- invariantes comuns;
- oposição simultânea;
- mudança incomum de entropia ou estado.

Todas as relações automáticas começam como:

```text
FELTS
causality_claimed=false
claim_allowed=false
```

Um paradoxo é fértil somente quando produz uma nova pergunta, regra, separação de camadas ou teste. Contradição sem ganho permanece registrada, mas não aumenta a espiral.

## 8. Falsificabilidade

Toda hipótese candidata precisa de um falsificador explícito. Sem ele:

```text
state = HYPOTHESIS_CANDIDATE
gap = TV-TEST
```

Toda métrica precisa de unidade, domínio e faixa válida. Sem isso:

```text
gap = TV-BOUNDARY
```

Todo resultado proveniente de fonte do Projeto permanece candidato até que a evidência apontada seja aberta e verificada.

## 9. Exemplo pedagógico: Regressão de Júlia

A história da Regressão de Júlia é usada apenas como exemplo do ciclo correto:

```text
observação de uma estudante
→ escuta do professor
→ formalização
→ demonstração e comunicação acadêmica
→ crítica e próximos testes
```

O exemplo não autoriza declarar, sem benchmark, que o método reduz complexidade computacional, energia ou instruções de máquina. Essa alegação exigiria implementação comparável, entradas definidas e medição de tempo, operações, memória e energia.

## 10. Integração com o Mapa

O motor complementa a ontologia operacional já existente:

```text
operational_ontology_engine
  classifica claims, trajetórias e vazios

sementeira_context_engine
  ingere snapshots, preserva coordenadas,
  calcula deltas, retorna à fonte e propõe relações FELTS
```

Um não substitui o outro.

## 11. Execução

```bash
python3 -m unittest -v tests/test_sementeira_context_engine.py

python3 scripts/sementeira_context_engine.py \
  --manifest data/sementeira/source-manifest-2026-07-27.json \
  --source-root /CAMINHO/DAS/FONTES \
  --output-json build/sementeira/context-baseline.json \
  --output-md build/sementeira/context-baseline.md \
  --strict
```

Não foi criado workflow novo. O comando é manual e read-only.

## 12. Gate de continuidade entre interações

A próxima interação deve começar pelo delta, não pela repetição integral:

```text
novo snapshot
→ verificar hash
→ localizar blocos novos ou alterados
→ recalcular somente relações afetadas
→ preservar eventos anteriores
→ registrar promoção, refutação ou TOKEN_VAZIO
```

### F_ok

- contrato formal criado;
- scanner read-only stdlib-only;
- derivada local determinística;
- antiderivada de proveniência com round-trip;
- correlações bloqueadas como `FELTS`;
- hipóteses sem falsificador bloqueadas;
- baseline das fontes fornecidas executado.

### F_gap

- ground truth semântico independente;
- calibração dos thresholds;
- revisão humana dos paradoxos;
- acesso nativo programático à memória interna do Projeto GPT;
- delta longitudinal de um segundo snapshot.

### F_next

Congelar um conjunto de calibração revisado, medir falsos positivos e falsos negativos e usar o próximo lote do Projeto como primeiro teste de evolução longitudinal.
