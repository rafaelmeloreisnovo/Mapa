# Checklist externo — Rulesets para `main` e `main_##`

Estado inicial: `TOKEN_VAZIO_EXTERNAL_SETTING`

Este checklist descreve configurações administrativas que não são materializadas por arquivos do repositório. Cada item só muda para `EVIDENCIADO` após observação na interface/API do GitHub e teste de bloqueio.

## Ruleset A — `main-canonical`

Alvo: branch `main`.

- [ ] exigir Pull Request antes de merge;
- [ ] exigir resolução de conversas;
- [ ] exigir check `branch-topology / validate` após o workflow existir em `main`;
- [ ] bloquear force-push;
- [ ] bloquear exclusão;
- [ ] exigir branch atualizada antes de merge, quando compatível com os checks;
- [ ] aplicar a administradores ou registrar bypass de recuperação;
- [ ] avaliar commits assinados conforme disponibilidade operacional;
- [ ] testar uma alteração rejeitada e guardar receipt.

## Ruleset B — `main-numbered-lanes`

Alvo por padrão: `main_[0-9][0-9]_*`.

- [ ] restringir criação a nomes registrados no manifesto;
- [ ] exigir Pull Request para atualização;
- [ ] bloquear force-push;
- [ ] bloquear exclusão;
- [ ] exigir check `branch-topology / validate`;
- [ ] impedir bypass silencioso;
- [ ] testar branch não registrada (`main_10_*`) e guardar receipt;
- [ ] testar promoção de lane para base diferente de `main` e guardar receipt.

## Evidência mínima

```text
ruleset_id
ruleset_target
ruleset_status
observed_at
actor
negative_test
check_result
receipt_hash
```

Sem esses campos, o estado permanece `TOKEN_VAZIO_EXTERNAL_SETTING`.
