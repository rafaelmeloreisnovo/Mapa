# Ledger corretivo — GitHub Actions, billing e controle positivo RLL

## Estado corrigido

```text
controle positivo verificado:
  instituto-Rafael/relativity-living-light
  run 29566816023 / job 87841176605
  success / 14 steps

observações bloqueadas:
  rafaelmeloreisnovo/Mapa
  rafaelmeloreisnovo/RafGitTools
  failure / 0 steps / logs ausentes
```

## Declaração do responsável

O responsável informa que o GitHub exibiu mensagem relacionada a pagamento nos repositórios bloqueados das instalações pessoal e institucional, enquanto o RLL institucional continuou executando.

Também relata a cronologia:

```text
pagamento via Google Play
→ Actions inicialmente operacionais
→ interrupção dos CIs fora do RLL
→ mensagem de billing
→ devolução unilateral aproximadamente cinco dias depois
→ GitHub para Google
→ Google para a conta do responsável
```

## Classificação

```text
non_rll_execution = ZERO_STEP_NO_LOGS
billing_scope = DECLARED_BY_OWNER
billing_message_artifact = TOKEN_VAZIO
refund_artifact = TOKEN_VAZIO
rll_execution = WORKFLOW_PASS / VERIFIED
root_cause_of_rll_exception = TOKEN_VAZIO
```

## Hipótese operacional prioritária

Como o RLL institucional é público, o seu sucesso é compatível com a regra do GitHub de que runners padrão em repositórios públicos são gratuitos, enquanto repositórios privados dependem da cota e da cobrança do proprietário.

Estado:

```text
public_vs_private_billing_hypothesis = PLAUSIBLE_NOT_PROVEN_FOR_FULL_SCOPE
```

A hipótese precisa ser testada contra outros repositórios públicos das duas instalações antes de virar explicação causal.

## Privacidade

Não registrar neste repositório público ou compartilhável:

- número de pedido do Google Play;
- IDs de transação;
- forma de pagamento completa;
- dados bancários;
- documentos pessoais;
- capturas sem redação de informações sensíveis.

## Autoridade

```text
RafGitTools corrective merge:
996ae2192f5011911d5b0fbd6d757777c546cef5
```
