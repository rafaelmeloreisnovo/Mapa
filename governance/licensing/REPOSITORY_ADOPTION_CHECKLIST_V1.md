# RAFAELIA — Checklist de Adoção de Licença por Repositório V1

**Status:** `DRAFT_COUNSEL_REVIEW_REQUIRED`

Nenhuma licença RAFAELIA deve ser aplicada em massa sem esta sequência.

## 1. Identidade e autoridade

- [ ] Repositório e branch/commit identificados.
- [ ] Autor/titular de cada família material relevante identificado.
- [ ] Fork/upstream identificado.
- [ ] Material original RAFAELIA separado de material herdado.
- [ ] Direitos suficientes para licenciamento comercial verificados.

## 2. Inventário de licenças

- [ ] Root LICENSE lido.
- [ ] LICENSES/ e COPYING lidos quando existentes.
- [ ] SPDX por arquivo inventariado quando aplicável.
- [ ] NOTICE upstream preservado.
- [ ] Dependências/bibliotecas/datasets/assets inventariados.
- [ ] Obrigações de atribuição registradas.
- [ ] Obrigações de disponibilização de fonte registradas.
- [ ] Restrições de marcas/patentes/dados registradas.

## 3. Compatibilidade

- [ ] Licença original de terceiro permanece intacta.
- [ ] RAFAELIA-NC-ATTR-V1 aplicada somente a material juridicamente controlado pelo Licenciante.
- [ ] Nenhuma cláusula RAFAELIA reduz direitos já concedidos por terceiro sobre componente de terceiro.
- [ ] Distribuição combinada revisada quanto a incompatibilidades.

## 4. Superfícies obrigatórias

- [ ] LICENSE ou ponteiro de licença.
- [ ] NOTICE.
- [ ] THIRD-PARTY NOTICES, quando aplicável.
- [ ] bloco de atribuição/citação.
- [ ] registro de modificações.
- [ ] source/ref/hash.
- [ ] direitos comerciais = ALLOWED / BLOCKED / TOKEN_VAZIO.

## 5. Gates

```text
G_RIGHTS_AUTHORITY
G_THIRD_PARTY
G_ATTRIBUTION
G_COMMERCIAL_SCOPE
G_NOTICE
G_COUNSEL
G_CI
```

Qualquer gate crítico não resolvido bloqueia a declaração de que o repositório inteiro está coberto pela licença RAFAELIA.

## 6. Receipt

Registrar ao final:

```text
repository
commit
paths covered
paths excluded
license versions
third-party notices
counsel state
CI state
F_ok
F_gap
F_next
hash/ref
```
