# Protocolo de Homeostase Operacional e Melhoria Contínua

**Aplicação:** ecossistema RAFAELIA, pesquisa, software, dados, documentação e experimentação  
**Estado:** `NORMATIVE_METAMODEL_DRAFT`  
**Data:** 2026-07-22  
**Limite:** este protocolo inspira-se em normas públicas; não declara certificação, conformidade auditada ou substituição do texto normativo oficial.

## 1. Princípio

Excelência operacional não é obedecer mecanicamente a uma norma congelada nem abandonar normas anteriores em nome de novidade. É manter uma rede complexa de processos em estado capaz de:

1. cumprir requisitos válidos;
2. perceber desvios e mudanças de contexto;
3. aprender com evidências;
4. corrigir sem apagar a história;
5. elevar desempenho sem aumentar risco oculto;
6. preservar pessoas, dados, autoria e reversibilidade.

Chamamos esse equilíbrio dinâmico de **homeostase operacional**:

\[
H_{op}(t)
=
Q(t)\times C(t)\times T(t)\times R(t)
-
E(t)-D(t)
\]

onde:

- \(Q\): qualidade do resultado;
- \(C\): coerência entre processos;
- \(T\): rastreabilidade;
- \(R\): resiliência e capacidade de recuperação;
- \(E\): entropia operacional;
- \(D\): dívida técnica, científica, documental ou ética.

A fórmula é um modelo de governança, não uma métrica validada. Pesos e escalas permanecem `TOKEN_VAZIO_CALIBRATION`.

---

## 2. Norma como piso, não como teto

Uma norma consolida conhecimento coletivo e requisitos mínimos. A melhoria não pode violar silenciosamente o requisito que pretendia superar.

\[
\boxed{
\text{evolução válida}
=
\text{baseline preservado}
+
\text{delta explícito}
+
\text{prova}
+
\text{controle de risco}
+
\text{rollback}
}
\]

Portanto:

- norma anterior não é apagada; torna-se baseline versionado;
- nova prática não é “melhor” por ser nova;
- ganho local não justifica dano sistêmico;
- exceção precisa de escopo, responsável, prazo e critério de saída;
- `TOKEN_VAZIO` impede preenchimento fictício de evidência.

---

## 3. Referenciais normativos

### ISO 9001

A abordagem por processos, liderança, avaliação de desempenho e melhoria contínua oferece a base de qualidade. Em 22 de julho de 2026, ISO 9001:2015 ainda era a edição publicada vigente; a sexta edição estava em fase final de publicação, prevista para substituir a de 2015 posteriormente. Nenhum documento deve declarar conformidade com uma edição ainda não publicada.

### ISO 31000:2018

Risco deve estar integrado a governança, estratégia, planejamento, decisão, operação e comunicação. O risco inclui ameaça e oportunidade, mas oportunidade não elimina salvaguarda.

### ISO/IEC 17025:2017

Para ensaios e medições: competência, imparcialidade, método, rastreabilidade metrológica, incerteza, equipamento, registros e validade dos resultados. Código executado não equivale automaticamente a ensaio competente.

### ISO 8000-61:2016

Qualidade de dados precisa de processos explícitos e capacidade mensurável. Dado ausente, zero, inválido, censurado e fora de domínio são estados diferentes.

### FAIR

Dados, software, modelos e workflows devem ser encontráveis, acessíveis sob regras declaradas, interoperáveis e reutilizáveis. FAIR não significa necessariamente “aberto”; acesso pode ser controlado por privacidade, segurança, licença ou consentimento.

### NIST AI RMF 1.0

Sistemas de IA devem ser governados, mapeados, medidos e gerenciados. Em 2026, o framework estava em revisão; o registro deve preservar a versão aplicada e monitorar substituições.

---

## 4. Célula operacional universal

Todo objeto relevante — claim, arquivo, dado, código, teste, modelo ou decisão — recebe:

\[
\mathcal C=
\langle
O,Rq,E,M,T,F,Rb,N
\rangle
\]

- \(O\): origem e autoria;
- \(Rq\): requisito aplicável;
- \(E\): evidência disponível;
- \(M\): método e ambiente;
- \(T\): teste e resultado;
- \(F\): falsificador ou critério de rejeição;
- \(Rb\): rollback/reversibilidade;
- \(N\): próximo gate verificável.

Estados permitidos:

```text
PROVADO_NO_DOMINIO
EVIDENCIADO_EXTERNAMENTE
EVIDENCIADO_LOCALMENTE
HIPOTESE_TESTAVEL
ESTIMATIVA
CONJECTURA
TOKEN_VAZIO
REFUTADO
NOT_APPLICABLE
OUT_OF_DOMAIN
```

Um único rótulo não substitui o vetor completo de estado.

---

## 5. Ciclo de homeostase

```text
OBSERVAR
  ↓
CLASSIFICAR
  ↓
FIXAR INVARIANTES
  ↓
MEDIR BASELINE
  ↓
PROPOR DELTA
  ↓
ANALISAR RISCO
  ↓
TESTAR EM ESCOPO CONTROLADO
  ↓
COMPARAR COM BASELINE
  ↓
PROMOVER | REVERTER | MANTER TOKEN_VAZIO
  ↓
REGISTRAR E RETROALIMENTAR
```

### 5.1 Observar

Registrar estado antes da intervenção, inclusive ambiente, versão, data, autor, hardware, dataset e limitações.

### 5.2 Classificar

Separar fato, hipótese, estimativa, metáfora, risco, anomalia, ausência e inaplicabilidade.

### 5.3 Fixar invariantes

Antes de otimizar:

- segurança;
- integridade;
- privacidade;
- autoria e licença;
- unidade e domínio;
- rastreabilidade;
- capacidade de rollback.

### 5.4 Medir baseline

A primeira observação é baseline, não novidade. O baseline deve possuir método, amostra, incerteza e hash quando aplicável.

### 5.5 Propor delta

Toda mudança declara:

```yaml
change_id: identificador
origin: requisito, risco, gap ou oportunidade
baseline: versão e métrica anterior
proposed_delta: alteração exata
expected_benefit: resultado esperado
risk: riscos e pessoas afetadas
falsifier: condição de rejeição
rollback: caminho de retorno
owner: responsável
expiry: data de revisão da exceção
```

### 5.6 Testar em escopo controlado

Usar piloto, branch, feature flag, sandbox, amostra bloqueada ou ambiente de homologação. Não testar tese científica em produção humana sem governança ética adequada.

### 5.7 Promover, reverter ou suspender

- **Promover:** benefício relevante, risco aceitável e invariantes preservadas.
- **Reverter:** regressão, dano, violação de requisito ou falsificador atingido.
- **Suspender:** evidência insuficiente; registrar `TOKEN_VAZIO_TEST`.

---

## 6. Sete réguas de decisão

| Régua | Pergunta |
|---|---|
| Direta | O que foi realmente alterado? |
| Inversa | Que dependências e condições tornaram a mudança possível? |
| Recíproca | O benefício em um processo produz custo em outro? |
| Contrária | Que teste tentaria destruir a alegação de melhoria? |
| Antiderivada | De qual incidente, requisito, dado ou decisão surgiu? |
| Derivada | Que novos riscos, métricas e obrigações aparecem? |
| Retroalimentação | Como o resultado modifica o próximo ciclo sem apagar o anterior? |

---

## 7. Critérios de promoção

Uma prática só pode ser chamada de melhoria operacional quando:

\[
\Delta U>\delta_{min}
\land
I_{preservadas}=1
\land
R_{residual}\leq R_{aceitavel}
\land
P_{proveniência}=1
\land
Rb=1
\]

- \(\Delta U\): utilidade mensurada em relação ao baseline;
- \(\delta_{min}\): ganho mínimo relevante definido antes do teste;
- \(I\): invariantes;
- \(R\): risco residual;
- \(P\): proveniência completa;
- \(Rb\): rollback testado.

Os limiares são específicos por domínio e permanecem `TOKEN_VAZIO_CALIBRATION` até definição por responsáveis competentes.

---

## 8. Anomalias e não conformidades

Uma anomalia não é automaticamente falha do núcleo. Classificar provisoriamente:

```text
A_PROCESSO
A_DADO
A_SENSOR
A_AMBIENTE
A_SOFTWARE
A_MODELO
A_SEGURANCA
A_DOCUMENTACAO
A_SEMANTICA
A_GOVERNANCA
TOKEN_VAZIO_CAUSE
```

Cada registro precisa de:

- detecção;
- impacto;
- contenção;
- causa conhecida ou vazia;
- evidência;
- ação corretiva;
- ação preventiva;
- verificação de eficácia;
- risco residual;
- encerramento ou próximo gate.

---

## 9. Não conformidade versus inovação

| Situação | Tratamento |
|---|---|
| requisito descumprido | não conformidade; conter e corrigir |
| requisito inadequado ao novo contexto | abrir revisão normativa, sem ignorá-lo |
| solução superior demonstrada | extensão controlada com compatibilidade |
| ganho sem prova | hipótese, não melhoria |
| prova local sem transportabilidade | evidência local, não regra universal |
| ausência de dado | `TOKEN_VAZIO`, nunca zero |
| norma em transição | versionar edição vigente e edição futura separadamente |

---

## 10. Rede complexa de processos

A excelência local pode degradar o sistema. Portanto, modelar dependências:

\[
G=(V,E)
\]

- \(V\): processos, dados, pessoas, sistemas e controles;
- \(E\): dependência, produção, consumo, risco, autorização e evidência.

Para cada mudança em \(v_i\), medir impacto em vizinhos:

\[
Impacto(v_i)
=
\sum_{j} w_{ij}\,\Delta x_j
\]

Os pesos não devem ser inventados. Enquanto não calibrados:

```text
weights = TOKEN_VAZIO_CALIBRATION
```

A análise qualitativa de dependências continua obrigatória mesmo sem pesos.

---

## 11. Indicadores mínimos

### Qualidade

- defeitos por unidade;
- taxa de retrabalho;
- cobertura de requisitos;
- resultados reproduzíveis;
- claims com fonte e falsificador.

### Fluxo

- lead time;
- tempo de espera;
- trabalho em progresso;
- frequência de rollback;
- gargalos e loops sem ganho.

### Dados

- completude;
- validade;
- consistência;
- unicidade;
- atualidade;
- proveniência.

### Risco

- incidentes;
- quase-incidentes;
- risco residual;
- exceções vencidas;
- controles sem teste.

### Aprendizado

- ações corretivas verificadas;
- resultados negativos preservados;
- hipóteses reclassificadas;
- tempo para fechar `TOKEN_VAZIO`;
- reincidência de causa.

Nenhum indicador isolado autoriza otimização cega.

---

## 12. Cadeia de custódia

Para cada artefato:

```text
origem
→ versão
→ transformação
→ executor
→ ambiente
→ teste
→ hash
→ resultado
→ decisão
→ próximo gate
```

O commit prova existência e conteúdo em certo ponto da história; não prova execução, validade científica ou desempenho. O Drive preserva documentação e revisão; não substitui o histórico Git. Os dois devem apontar um ao outro por IDs, URLs, hashes ou manifestos.

---

## 13. Gate humano e ético

Automação não pode promover sozinha mudanças que afetem:

- saúde;
- crianças ou vulneráveis;
- privacidade;
- direitos;
- segurança física;
- alegações científicas públicas;
- licenças e autoria;
- exclusão irreversível de dados;
- produção ou merge de alto impacto.

Nesses casos:

```text
human_review_required = true
claim_allowed = false
```

---

## 14. Invariante final

\[
\boxed{
\text{excelência operacional}
\neq
\text{máximo desempenho local}
}
\]

\[
\boxed{
\text{excelência operacional}
=
\text{melhoria contínua}
\cap
\text{coerência sistêmica}
\cap
\text{prova}
\cap
\text{ética}
\cap
\text{capacidade de retorno}
}
\]

### R₃

- **F_ok:** norma, baseline, risco, evidência, dados e rollback foram integrados num único ciclo.
- **F_gap:** pesos, limiares e donos de processo ainda precisam ser calibrados por domínio.
- **F_next:** aplicar o protocolo primeiro ao fluxo `papers ↔ Mapa ↔ Drive`, medir uma rodada e corrigir a própria régua.
