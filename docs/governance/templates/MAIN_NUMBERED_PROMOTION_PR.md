# Promoção de lane numerada para `main`

> Copie este bloco para o corpo da Pull Request. Não remova campos; use `TOKEN_VAZIO` quando a evidência ainda não existir.

```text
source: <fonte, commit, dataset ou artefato de origem>
claim_state: <PROVADO|EVIDENCIADO|HIPOTESE|MODELO_ANALOGICO|PARABOLA|REFUTADO|TOKEN_VAZIO>
evidence: <receipt, hash, teste, log, artefato ou TOKEN_VAZIO>
falsifier: <teste negativo, condição de refutação ou TOKEN_VAZIO>
rollback: <commit/reversão/caminho de restauração>
decision: <READY_FOR_HUMAN_REVIEW|REJECTED|BLOCKED_TOKEN_VAZIO>
```

## Checklist

- [ ] A branch de origem é uma das `main_00_*` até `main_09_*` registradas.
- [ ] A base da PR é `main`.
- [ ] A lane foi sincronizada com o estado atual de `main`.
- [ ] Testes positivos e adversariais foram executados.
- [ ] Os hashes/receipts apontam para entradas e ambiente identificáveis.
- [ ] Segurança, privacidade e dependências foram avaliadas quando aplicável.
- [ ] O rollback é executável e não depende de memória conversacional.
- [ ] A promoção recebeu autorização humana explícita.

```text
claim_allowed=false até decisão humana e checks observáveis.
```
