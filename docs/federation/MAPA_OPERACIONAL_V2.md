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
| Termux → Vectras | coletor não destrutivo + validador + 4 testes | contrato passou no CI; dispositivo `TOKEN_VAZIO` |
| Vectras guest | schema/validador do ciclo completo + 5 testes | estrutura passou; boot `BLOCKED` |

## Medições defensáveis

### ChipQuantum

```text
ChipQuantum.runtime = 2
```

A medição aponta para commit, fonte C, comando, artefato JSON, SHA-256, ambiente e limitações. Significa somente **execução local x86_64 para a identidade do Paper 6**. Não significa ARM32, Android, reprodução independente ou validação física.

### Termux RAFCODEΦ

```text
Termux.reproducibility = 2
```

Registro separado:

```text
data/federation/measurements/termux-reproducibility-20260717.json
```

O workflow `abi-policy-consistency` executou o coletor e o validador, e publicou o artefato `termux-runtime-evidence-contract-29550485275`, digest `sha256:2d4836d9bee88b7aa1119dcb1eee4388a9fb9ef994a816e087c16a4425c90899`.

Essa medição significa **reprodução do contrato no runner Linux do GitHub Actions**. Não significa APK instalado, shell Android funcional, backend `apt/dpkg` comprovado ou aparelho ARM32 aprovado. O gate ARM32 continua pendente/falhou.

Todos os demais pesos continuam `TOKEN_VAZIO`. Um teste apenas estrutural não recebe automaticamente peso 1, 2 ou 3. Cada mudança exige registro de medição com commit, caminho, comando, artefato, timestamp, limites e executor.

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
