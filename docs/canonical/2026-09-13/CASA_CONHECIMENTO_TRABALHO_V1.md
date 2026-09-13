# Casa de Conhecimento e Trabalho — Contrato V1

Estado: DRAFT_AUDITABLE  
Autoridade: Mapa / control-plane  
claim_allowed: false por padrão

## Intenção

Transformar pesquisa, trabalho, sessão, arquivo, hipótese, código ou tarefa em uma unidade reconstruível e auditável, sem confundir SOURCE, ARTEFATO, EXECUÇÃO, EVIDÊNCIA e CLAIM.

Fluxo:

```text
ENTRADA
→ CONTEXTO
→ AUTORIDADE
→ TRABALHO
→ EVIDÊNCIA
→ CONTRADIÇÃO/INCERTEZA
→ REPRODUÇÃO
→ ROLLBACK
→ RECEIPT
→ MEMÓRIA
```

## Oito guardiões

1. **Reconstruibilidade** — outra pessoa deve conseguir refazer a rota com entradas, versões, comandos e saídas identificáveis.
2. **Proveniência** — toda unidade precisa apontar para origem, autoridade, transformação e hash/ref quando disponível.
3. **Contexto** — registrar intenção, escopo, tempo, domínio, dependências e fronteira do que não está sendo afirmado.
4. **Evidência** — distinguir documento, teste, execução, dado, hash e resultado; presença de artefato não equivale a evidência do claim.
5. **Contradição** — conflito comparável deve permanecer explícito até resolução ou supersessão; não escolher silenciosamente a versão conveniente.
6. **Incerteza** — lacunas e ausência de observação viram TOKEN_VAZIO/BLOCKED/PARTIAL, nunca zero ou PASS.
7. **Reprodução** — claim operacional somente sobe quando houver replay/reexecução compatível com a fronteira declarada.
8. **Rollback** — toda mutação material precisa de predecessor, condição de reversão ou supersessão append-only.

## Estados

- DRAFT
- TOKEN_VAZIO
- BLOCKED
- CONTRADICTION
- VERIFIED_LIMITED
- REPRODUCED
- ROLLBACK_READY
- CLOSED

## Regra de promoção

```text
claim_allowed=true
somente se:
  provenance.complete
  context.complete
  evidence.present
  contradiction.unresolved == false
  uncertainty.typed == true
  reproduction.status == PASS
  rollback.ready == true
  reconstructibility.status == PASS
```

Nenhum gate isolado promove o claim.

## Serviço de casa

A "Casa" não é um novo depósito. É uma superfície humana para operar a rota canônica:

- **Entrada**: intenção, pergunta, tarefa ou material.
- **Estante de fontes**: ponteiros para Drive/GitHub/fontes, sem duplicação desnecessária.
- **Mesa de trabalho**: unidade ativa com owner, escopo e próximos passos.
- **Sala de evidência**: testes, execuções, hashes, receipts, resultados negativos.
- **Sala de conflito**: contradições e versões concorrentes.
- **Sala do vazio**: TOKEN_VAZIO e dependências bloqueantes.
- **Oficina de reprodução**: comandos, ambiente, fixtures, replays.
- **Arquivo de retorno**: rollback, supersedes, predecessor/successor.
- **Mapa da casa**: índice que liga tudo sem virar fonte da verdade de cada produtor.

## Relação com START HERE

```text
START HERE
→ READ
→ INDEX
→ CONTEXT
→ ROUTE
→ ACT
→ RECEIPT
→ LEARN
```

A Casa consome esta rota; não a substitui.

## Unidade mínima

Cada unidade de trabalho/conhecimento deve conter:

```text
id
intent
authority
sources[]
context
artifact_refs[]
execution_refs[]
evidence[]
contradictions[]
uncertainty[]
reproduction
rollback
reconstructibility
state
claim_allowed
next
```

## Fronteiras

- INDEX != SOURCE
- SOURCE != ARTIFACT
- ARTIFACT != EXECUTION
- EXECUTION != EVIDENCE
- EVIDENCE != CLAIM
- REPRODUCED != UNIVERSAL_TRUTH
- ROLLBACK_READY != ROLLBACK_EXECUTED
- TOKEN_VAZIO != 0

## Critério de fechamento

Uma rodada fecha quando:
- objetivo ficou determinado;
- fontes e autoridade estão pinadas;
- delta material foi registrado;
- evidência/contradição/incerteza estão tipadas;
- reprodução e rollback têm estado explícito;
- next step está definido;
- receipt/μWRITE aponta para predecessor e evidência.

R3 = <F_ok, F_gap, F_next>.
