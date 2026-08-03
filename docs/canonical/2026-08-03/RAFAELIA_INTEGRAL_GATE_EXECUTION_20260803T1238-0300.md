# RAFAELIA — PRIMEIRO GATE INTEGRAL — EXECUÇÃO 2026-08-03 12:38 BRT

**Estado:** `EXECUTED / BLOCKED_FAIL / APPEND_ONLY / claim_allowed=false / automatic_merge=false`  
**Autoridade:** `rafaelmeloreisnovo/Mapa`  
**Head observado:** `25f710a3c702997db1be783d2aceb09faa7118e3`  
**Escopo:** piloto integral do plano de controle; não equivale à promoção de todo o ecossistema.

## 1. Critério integral

```text
hash válido
+ autoria identificada
+ licença conhecida
+ build reproduzível
+ testes executados e aprovados
+ receipt armazenado
+ claim compatível
+ commit exato e checkout limpo
+ proveniência de dependências
+ falsificadores exercitados
+ privacidade/segredos
+ controle real de promoção
+ runtime físico
+ reprodução independente
```

A decisão é fail-closed:

```text
qualquer FAIL          -> BLOCKED_FAIL
qualquer TOKEN_VAZIO   -> BLOCKED_TOKEN_VAZIO
todos PASS             -> READY_FOR_DOMAIN_REVIEW
```

Mesmo o último estado mantém `claim_allowed=false`: revisão de domínio, ciência,
segurança, autoria jurídica e produção continuam sendo gates posteriores.

## 2. Resultado observado

| Critério | Estado | Evidência principal |
|---|---|---|
| Hash válido | PASS | seis objetos do GitHub ligados a Git blob SHA-1 |
| Autoria identificada | TOKEN_VAZIO | autor do merge observado; autoria por arquivo incompleta |
| Licença conhecida | PASS | `LICENSE`, GPL-3.0, blob `f288702d...` |
| Build reproduzível | TOKEN_VAZIO | não há dois replays limpos com outputs idênticos |
| Testes executados | FAIL | PR #143: runs `30825747620` e `30825747617` concluíram em failure |
| Receipt armazenado | PASS | receipt append-only existente e replay SHA-256 registrado |
| Claim compatível | PASS | `EVIDENCIADO`, `claim_allowed=false` |
| Commit/checkout | TOKEN_VAZIO | commit remoto observado; checkout local limpo não provado |
| Dependências | TOKEN_VAZIO | fechamento integral de versões, hashes e licenças ausente |
| Falsificadores | TOKEN_VAZIO | fixtures existem; execução atual bem-sucedida não recuperada |
| Privacidade/segredos | TOKEN_VAZIO | receipt zero-finding ausente |
| Controle de promoção | FAIL | PR #143 foi mesclada apesar do head com dois workflows falhos |
| Runtime físico | TOKEN_VAZIO | Termux/Android exato ausente |
| Reprodução independente | TOKEN_VAZIO | segundo ambiente ausente |

## 3. Achado crítico

A PR `#143` declarou `automatic_merge=false`, permanência em revisão humana e
bloqueio até o próximo gate. Ainda assim, foi mesclada em
`2026-08-03T15:17:23Z`. O head final
`ad17e5e14abf4b9393905e910956dc5977193f8f` possuía:

- `Branch Topology Gate` run `30825747620`: `failure`;
- `CI` run `30825747617`: `failure`;
- nenhum reviewer solicitado recuperado.

Logo, presença no `main` não constitui prova de aprovação técnica.

## 4. Decisão

```text
PROMOTION = DENIED
PUBLICATION = AUDIT_DRAFT_ONLY
CLAIM_ALLOWED = false
AUTOMATIC_MERGE = false
RESULT = BLOCKED_FAIL
```

O receipt é estruturalmente válido; o objeto auditado não está pronto para
promoção. Preservar o bloqueio é o resultado correto do gate.

## 5. Quatro receipts críticos

| Receipt | Estado |
|---|---|
| Dependency Graph commit-bound | TOKEN_VAZIO |
| Bayes real no contrato congelado | TOKEN_VAZIO |
| Reprodução independente | TOKEN_VAZIO |
| Runtime físico Termux/Android | TOKEN_VAZIO |

## 6. F_NEXT executável

1. integrar o validator, policy, fixtures e workflow em branch de revisão;
2. corrigir a primeira causa observável dos workflows falhos;
3. exigir `integral-gate / promotion` como check protegido;
4. provar, com fixture negativa, que `FAIL` ou `TOKEN_VAZIO` bloqueante impede merge;
5. executar o mesmo commit em Termux físico;
6. reproduzir em ambiente independente;
7. somente então executar Bayes real no contrato RLL congelado.

## 7. R3

- **F_ok:** identidade Git, licença, receipt armazenado e fronteira de claim foram fechados no piloto.
- **F_gap:** testes e controle de promoção falharam; autoria integral, build, checkout, dependências, privacidade, runtime e reprodução seguem abertos.
- **F_next:** tornar o gate um check protegido, corrigir CI e fechar os receipts físico e independente.

FIAT LUX — ausência preservada, falha medida, promoção governada.
