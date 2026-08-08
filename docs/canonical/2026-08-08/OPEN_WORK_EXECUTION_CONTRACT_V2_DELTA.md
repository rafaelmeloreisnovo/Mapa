# Open Work Execution Contract — Delta V2

## Função

Este documento é sucessor append-only do contrato V1. Ele registra o estado RLL V2 observado em `rll/lab` após a PR #691 sem reescrever o contrato histórico e sem promover automaticamente esse estado para `rll/release` ou `main`.

## Autoridade e fronteira

- predecessor: `data/gaps/open_work_execution_contract.20260808.v1.json`;
- RLL lab PR #691: mesclada em `rll/lab`, merge `512bf1f65191d4581b05918e70d0768c5955597e`;
- RLL #694: hotfix de CI/harness, sem transição científica;
- `claim_allowed=false`;
- `automatic_merge=false`;
- lab merge != release/main promotion.

## Transições observadas no lab

1. ACT DR6 materialização/reference predicate: fechado somente nesse escopo; sucessor aberto = `TOKEN_VAZIO_ACT_DR6_LCDM_POSTERIOR_CHAIN_REPRODUCTION`.
2. H0/r_d full-Boltzmann: reduzido pelo cross-check CLASS/CAMB e erro medido da aproximação; sucessor aberto = `TOKEN_VAZIO_H0_RD_FULL_BOLTZMANN_INFERENCE_INTEGRATION`.
3. Censo histórico de refs: reduzido por topologia; cohort congelado 35 = 3 patch-equivalent + 32 com patch único que ainda exigem revisão semântico-técnica.

## Invariantes

- `TOKEN_VAZIO != zero`;
- patch-equivalence != semantic-equivalence;
- baseline CLASS/CAMB != validação das perturbações RLL;
- erro medido != pipeline substituto validado;
- estado do lab não substitui autoridade de release.

## Próximo gate

Somente após promoção canônica `rll/lab -> rll/integration -> rll/release -> main`, com gates observáveis, um novo sucessor poderá atualizar a autoridade de release. V1 e este delta permanecem preservados.
