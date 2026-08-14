# RAFAELIA — Operational Work-Item Lattice V1

State: `CANONICAL_DRAFT / VERIFIED_LIMITED_LOCAL / claim_allowed=false`

## 1. Invariante

Um item de trabalho não possui um único status. Ele ocupa simultaneamente coordenadas ortogonais:

`W = <origem, urgência, importância, atenção, epistemologia, proveniência, contrato, execução, janela, SixSigma, bibliotecnia, fechamento>`

Isso impede colapsos semânticos como:

- urgente != provado;
- esquecido != refutado;
- ignorado != desnecessário;
- abortado != inválido;
- censurado/bloqueado != falha lógica;
- óbvio != evidenciado;
- sugerido != autorizado;
- executado != verificado;
- ausência != zero;
- TOKEN_VAZIO != conclusão negativa.

## 2. Eixos

### Origem

`EXPLICIT_USER | OBSERVED | DERIVED | SUGGESTED | INFERRED | LATENT | OBVIOUS_CANDIDATE | RECOVERED | IMPORTED`

`OBVIOUS_CANDIDATE` significa que um passo parece natural ou necessário por estrutura, mas ainda precisa ser materializado e validado.

### Prioridade

Urgência: `CRITICAL | URGENT | SOON | ROUTINE | UNSCHEDULED`.

Importância: `MUST | IMPORTANT | SHOULD | SUGGESTED | OPTIONAL`.

Urgência e importância são independentes. Um item pode ser `URGENT+OPTIONAL` ou `ROUTINE+MUST`.

### Atenção

`ACTIVE | FORGOTTEN_RECOVERED | IGNORED_INTENTIONAL | IGNORED_UNRESOLVED | DEFERRED | LEFT_INCOMPLETE | ABORTED | BLOCKED_BY_CONTROL | SUPPRESSED_BY_POLICY | SUPERSEDED | COMPLETED`.

A palavra informal “censurado” não é armazenada como conclusão genérica. O ledger exige distinguir `SUPPRESSED_BY_POLICY` de `BLOCKED_BY_CONTROL`, com `reason_code` e, quando aplicável, `policy_ref`.

### Epistemologia

`VERIFIED | EVIDENCED | HYPOTHESIS | MODEL_ANALOGICAL | SYMBOLIC | TOKEN_VAZIO | ABSENT | CONFLICTING | INVALIDATED | SUPERSEDED`.

Este eixo responde “o que sabemos?”, não “o que devemos fazer?”.

### Proveniência

`BOUND | PARTIAL | MISSING | CONFLICTING`.

Uma afirmação não pode ser promovida a evidenciada/verificada com proveniência ausente.

### Contrato

`SATISFIED | PARTIAL | UNSATISFIED | BREACHED | TOKEN_VAZIO | NOT_APPLICABLE`.

O estado global `SATISFIED` exige que cada requisito esteja `SATISFIED` ou `NOT_APPLICABLE`.

### Execução

`NOT_STARTED | PLANNED | IN_PROGRESS | BLOCKED | EXECUTED | VERIFIED | FAILED | ABORTED | DEFERRED`.

`EXECUTED` registra ocorrência. `VERIFIED` exige evidência associada.

### Janela temporal

Todo item recebe `discovered_at`, e pode receber `due_at` e `next_check_at`. Ausência de prazo não autoriza inventar urgência.

### Six Sigma

Cada item pode ocupar `DEFINE | MEASURE | ANALYZE | IMPROVE | CONTROL` e recebe `severity`, `occurrence`, `detectability` em 1..5.

`RPN = severity × occurrence × detectability` é validado semanticamente; divergência falha fechada.

### Bibliotecnia

Cada item registra `authority_refs`, `relation_refs`, `index_terms` e `access_class`.

O objetivo é que uma pendência possa ser recuperada por autoridade, relação, assunto e classe de acesso sem depender do nome do arquivo ou da memória da sessão.

### Fechamento

`OPEN | PARTIAL | CLOSED | TOKEN_VAZIO`.

`CLOSED` exige todos os closure gates em `PASS`. Cada item preserva falsificador, `F_ok`, `F_gap`, `F_next` e `claim_allowed=false`.

## 3. Tradução operacional dos termos recorrentes

| Termo humano | Eixo principal | Regra |
|---|---|---|
| urgente | priority.urgency | não altera epistemologia |
| importante | priority.importance | não altera execução |
| necessário | priority.importance=MUST | exige contrato/closure gate próprio |
| deveria | priority.importance=SHOULD | não é autorização automática |
| sugerido | origin=SUGGESTED e/ou importance=SUGGESTED | precisa de triagem |
| óbvio | origin=OBVIOUS_CANDIDATE | continua sujeito a prova |
| esquecido | attention=FORGOTTEN_RECOVERED | preserva origem e tempo de recuperação |
| ignorado | attention=IGNORED_* | deve registrar se foi intencional ou não resolvido |
| deixado/incompleto | attention=LEFT_INCOMPLETE | exige F_gap/F_next |
| abortado | attention/execution=ABORTED | exige reason_code; não implica INVALIDATED |
| bloqueado | attention=BLOCKED_BY_CONTROL ou execution=BLOCKED | infraestrutura/controle != code fail |
| censurado/suprimido | attention=SUPPRESSED_BY_POLICY | exige policy_ref; não inferir além da evidência |
| ausência | epistemic=ABSENT ou TOKEN_VAZIO | ausência observada != valor zero |
| proveniência faltante | provenance=MISSING | impede promoção de claim |
| contrato incompleto | contract=PARTIAL/UNSATISFIED | closure não pode ser CLOSED |
| feito | execution=EXECUTED | não equivale a VERIFIED |
| excelência operacional | composição dos eixos + gates | não é rótulo autoatribuído |

## 4. Geometria operacional

A “geometria multidimensional” deste contrato é uma geometria de estados e relações, não uma alegação física:

`G_operacional = Priority × Attention × Epistemic × Provenance × Contract × Execution × Time × Control`

Uma mudança em um eixo gera um evento append-only, não reescrita silenciosa dos demais eixos.

Exemplo:

`TOKEN_VAZIO + MUST + LEFT_INCOMPLETE + PARTIAL_PROVENANCE + PLANNED`

pode evoluir para:

`EVIDENCED + MUST + ACTIVE + BOUND_PROVENANCE + EXECUTED`

sem fingir que a etapa intermediária nunca existiu.

## 5. Aplicação ao C80

O primeiro ledger materializa três itens reais:

1. privacy review para semantic topics;
2. chunk graph materialization;
3. cross-export dedup.

Eles permanecem gaps reais, mas agora possuem coordenadas de prioridade, atenção, proveniência, contrato, Six Sigma, bibliotecnia, falsificador e F_next.

## 6. Gates semânticos

O validator rejeita, entre outros:

- RPN inconsistente;
- VERIFIED sem evidência;
- execution VERIFIED sem evidence ref;
- TOKEN_VAZIO sem F_gap/F_next;
- ABORTED/BLOCKED/SUPPRESSED sem razão;
- SUPPRESSED_BY_POLICY sem policy_ref;
- contrato SATISFIED com requisito aberto;
- CLOSED com gate não PASS;
- EVIDENCED/VERIFIED com provenance MISSING;
- claim_allowed=true;
- campos inesperados fora do contrato.

## 7. R3

`F_ok = linguagem operacional convertida em eixos ortogonais + schema + validator + adversarial tests`.

`F_gap = ainda não existe inventário global de todos os work-items do ecossistema; prioridades históricas precisam ser ingeridas sem inferência retroativa`.

`F_next = ingerir work-items de receipts/Gap Atlas de forma append-only; produzir mapas por urgência, contrato, proveniência e closure gate; usar o lattice como interface de redução contínua de incerteza`.
