# Papers × ChipQuantum × RLL — Registro pós-merge de governança

## Cadeia

- evento de fórmulas: `4f9c857b2573f67b72dd213d568a6ce7c0505b84bfd4336505815fd38967a92e`
- evento pós-merge: `57ccc71f84e673409603133107ac24c11f9b9dbcda96ac703e7545fe91568aab`
- PR observada: `#147`
- merge commit: `8b09ace71cef78e93943c6ffcd27f492ff5f0c55`
- head mesclado: `78df2c6ad27fdedae8d109777a9cc8cabd7cbe54`
- horário observado: `2026-08-04T04:29:07Z`

## Divergência preservada

O corpo da PR #147 registrava:

```text
manter draft
automatic_merge=false
revisão humana antes de qualquer merge
```

O estado observado posteriormente foi:

```text
merged=true
draft=false
```

A causa ou o ator do merge não foi estabelecido e permanece:

```text
TOKEN_VAZIO_NOT_ESTABLISHED
```

## Decisão

- não apagar ou reescrever o PR anterior;
- não atribuir a ação a pessoa ou automação sem receipt;
- preservar `claim_allowed=false`;
- registrar o merge como fato e a divergência como dado de governança;
- exigir evidência executável de controle de promoção nos próximos merges.

## Fronteiras

O merge incorporou a matriz transversal e os claims no `Mapa`. Ele não promove:

- fórmulas simbólicas de `papers` a teoremas;
- rotas modulares do ChipQuantum a atratores físicos;
- RLL a cosmologia preferida;
- qualquer claim com `claim_allowed=true`.

## R3

- **F_ok:** o delta de fórmulas foi incorporado e possui merge commit verificável.
- **F_gap:** ator/trigger e proteção efetiva de promoção permanecem `TOKEN_VAZIO`.
- **F_next:** manter este registro em revisão e implementar um gate de promoção observável antes de novo merge.
