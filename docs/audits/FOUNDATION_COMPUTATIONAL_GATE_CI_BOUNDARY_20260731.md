# Foundation computational gate — CI boundary event 2026-07-31

**Registro:** `TOKEN_VAZIO_CI_EXECUTION_NOT_OBSERVED`  
**Repositório:** `rafaelmeloreisnovo/Mapa`  
**PR:** #102 — `Foundation V1: computational gate and RafPolimata adapter`  
**HEAD observado:** `d713d884c7174d37aceb642f80149e037426686e`  
**Claim permitido:** `false`

## Fato observado

Na consulta de 2026-07-31, o run de Actions associado ao HEAD da PR foi:

| Campo | Valor |
|---|---|
| Workflow | `RAFAELIA Foundation V1 Contract` |
| Run | `30618443272` |
| Conclusão reportada | `failure` |
| Job | `contract` (`91117019359`) |
| Steps retornados | `[]` |
| URL de logs retornada | `null` |

Portanto, não há step observável nem log disponível que permita atribuir uma
causa ao estado `failure`. A falha não é evidência de defeito do runner, de
falha de compilação, nem de execução Termux.

## Separação de evidências

| Camada | Estado |
|---|---|
| Suite local Foundation | `PASS_11_OF_11` antes do envio da PR |
| Arquivos de branch reconsultados | correspondência byte a byte confirmada |
| Actions deste run | `TOKEN_VAZIO_CI_EXECUTION_NOT_OBSERVED` |
| Receipt Termux do RafPolimata | `TOKEN_VAZIO` |
| Promoção de claim | `false` |

O limite já registrado para CI privada/billing pode explicar parte do contexto,
mas este evento isolado não fornece logs suficientes para afirmá-lo como causa
raiz.

## Decisão

Não reexecutar, não fazer merge automático, não alterar a implementação em
resposta a uma causa não observada. Manter este registro append-only e tratar o
workflow como verificação auxiliar, nunca como substituto do receipt local.

## Próximo passo verificável

1. Quando houver steps/logs observáveis, diagnosticar a falha a partir do
   trecho concreto; ou
2. executar `compiler-local-gate` no checkout Termux limpo do RafPolimata e
   anexar o receipt + gate do commit exato numa mudança de evidência separada.

## R3

`F_ok`: limite de CI documentado sem inferir causa.  
`F_gap`: runner/logs e receipt Termux continuam não observados.  
`F_next`: evidência local exata, seguida de revisão específica de domínio.
