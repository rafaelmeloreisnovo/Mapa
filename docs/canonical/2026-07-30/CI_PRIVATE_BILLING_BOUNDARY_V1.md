# CI Private Billing Boundary V1

**Evento:** `RAFAELIA-CI-PRIVATE-BILLING-BOUNDARY-V1-20260730T054800Z`  
**Predecessores:** Mapa `b193792df10581f8b4b32b36a9511bc8585f6611` (PR #95) e `d8bf643236a86e77cbbf4b08271da51ae86e118a` (PR #96)  
**Tempo:** 2026-07-30 05:48 UTC / 02:48 BRT  
**Política:** `APPEND_ONLY · NON_DESTRUCTIVE · CLAIM_ALLOWED=false · NO_AUTO_MERGE`

## Correção de classificação

Para repositórios privados sem cobertura de pagamento de GitHub Actions, o titular informa que a execução remota não é disponibilizada. Portanto, uma execução retornada sem steps e sem logs deve ser registrada como:

```text
CI_UNAVAILABLE_PRIVATE_BILLING
```

e **não** como falha de código, resultado de teste, causa-raiz técnica ou evidência negativa do artefato.

Essa classificação substitui, para esse limite operacional informado, a interpretação anterior `TOKEN_VAZIO_CI_ROOT_CAUSE_UNRESOLVED`. `TOKEN_VAZIO` continua obrigatório para aquilo que realmente não foi executado: Termux/Android, hardware, benchmark, revisão humana ou reprodução independente.

## Autoridade e separação

| Camada | Decisão |
|---|---|
| GitHub privado sem Actions pagas | `CI_UNAVAILABLE_PRIVATE_BILLING` |
| Receipt local observável | evidência limitada ao ambiente e comando registrados |
| RLL com steps observáveis | `EVIDENCIADO_WORKFLOW_SCOPE_ONLY`; não generalizar para outros repositórios |
| Ciência, direito, segurança e produção | `CLAIM_ALLOWED=false` até prova própria |

## Aplicação no Mapa

O Mapa conserva esta fronteira como regra de ontologia operacional: `workflow_conclusion=failure` sem steps/logs não é um `CODE_FAILURE`. O registro deve preservar `repository`, `head_sha`, `run_id`, `billing_boundary`, `local_receipt`, `runtime_state` e `F_next`.

Nenhum workflow foi reexecutado, nenhum merge foi disparado e nenhum dado bruto foi publicado por esta correção.

## F_next

1. Executar localmente ou no Termux quando os bytes-fonte e o ambiente estiverem presentes.
2. Produzir receipt com commit, input hash, comando, ambiente, exit code e digest.
3. Tratar GitHub Actions como capacidade opcional, não como pré-requisito para reconhecer uma execução local válida.

\[
R_3=\langle F_{ok}:\text{limite operacional nomeado},\;F_{gap}:\text{receipts reais},\;F_{next}:\text{execução local vinculada}\rangle
\]
