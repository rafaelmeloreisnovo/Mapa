# Mapa Operacional RAFAELIA v2

Esta é a projeção humana do índice mestre do `RafGitTools`. A fonte de máquina permanece:

```text
rafaelmeloreisnovo/RafGitTools
agent/master-index-runtime-recovery-v2-20260716
b2ea2e731fdecb5effd0af929b26233876140513
configs/workflow-master-index.json
blob bc7ad055ae2e89bf474e5dc9eaf4de45489717e0
```

## Rotas materializadas nesta passagem

| Rota | Artefato implementado | Estado honesto |
|---|---|---|
| RafPolimata → RLL | manifesto formal + validador + 5 testes | estrutura passou; cosmologia `TOKEN_VAZIO` |
| GAIA → RLL | recibo pointer-only + validador + 5 testes | estrutura passou; replay `TOKEN_VAZIO` |
| Matemática → ChipQuantum | C float64/Q16 + runner + artefato + teste | `TESTED_LOCAL_X86_64`; ARM/Android `TOKEN_VAZIO` |
| Termux → Vectras | coletor não destrutivo + validador + 4 testes | coletor passou; dispositivo `TOKEN_VAZIO` |
| Vectras guest | schema/validador do ciclo completo + 5 testes | estrutura passou; boot `BLOCKED` |

## Regra de pesos

Todos os seis pesos continuam `TOKEN_VAZIO`. Um teste estrutural ou local não recebe automaticamente peso 1, 2 ou 3. Cada mudança exige registro de medição com commit, caminho, comando, artefato, timestamp, limites e executor.

## Próxima sequência

```text
1. Executar o coletor Termux no Android alvo.
2. Usar a evidência Termux como preflight do Vectras.
3. Executar o smoke de guest boot sem mutar a imagem antes do gate.
4. Resolver o SHA real do artefato RLL e produzir o recibo GAIA.
5. Executar CAMB/RECFAST sob o manifesto RafPolimata.
6. Reproduzir o runtime ChipQuantum em ARM32/Android.
```

`claim_allowed=false` permanece global.
