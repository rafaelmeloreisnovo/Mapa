# Auditoria — Sistema Vivo de Mecanismos

> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧

## Escopo

Refatoração aditiva do repositório `Mapa` para representar cada repositório inventariado por mecanismos evidenciados, sem inferir comportamento pelo nome e sem transformar ausência em afirmação.

Branch auditada:

```text
refactor/sistema-vivo-mecanismos-v1
```

Base observada:

```text
main @ 6c91ef218986f335c7b7931a10262a9b73780bd0
```

## Entregas materializadas

- contrato JSON Schema para perfis de mecanismo;
- diretório de perfis evidenciados;
- primeiro perfil do próprio `rafaelmeloreisnovo/Mapa`;
- construtor determinístico de `LIVING_SYSTEM_INDEX.json`;
- validador independente fail-closed;
- cinco testes adversariais;
- arquitetura em camadas;
- visão Mermaid para desenvolvimento humano;
- README reposicionado como sistema vivo de conhecimento.

## Invariantes verificadas no código

1. identidade do repositório permanece `FATO` dentro do escopo do conector;
2. nome do repositório não implica finalidade ou mecanismo;
3. perfil órfão, sem identidade no inventário, é rejeitado;
4. `TOKEN_VAZIO` exige motivo, próxima ação e critério de saída;
5. `TOKEN_VAZIO` não aceita `value` nem `evidence`;
6. células resolvidas exigem evidência;
7. `HIPOTESE` exige confiança em `[0, 1)`;
8. IDs conflitantes interrompem a construção;
9. divergência da contagem do inventário interrompe a construção;
10. completude e estatísticas são derivadas;
11. digest BLAKE2b-256 é recalculado;
12. `claim_allowed` só pode ser verdadeiro com onze campos `FATO` e perfil explícito;
13. `global_claim_allowed=false` permanece preservado.

## Validação executada em ambiente isolado

Os arquivos exatos preparados para a branch foram executados com Python 3, sem bibliotecas externas:

```text
python3 -m py_compile ...                                      PASS
python3 -m unittest discover -s tests -v                      5/5 PASS
```

Casos cobertos:

- checkpoint + delta produzem identidades únicas;
- repositório não lido recebe onze `TOKEN_VAZIO`;
- perfil promove somente campos evidenciados;
- hipótese não libera alegação final;
- alegação escondida dentro de `TOKEN_VAZIO` é rejeitada;
- adulteração altera o digest;
- contagem divergente do inventário falha fechada.

## Limites preservados como TOKEN_VAZIO

| Lacuna | Motivo | Próxima ação | Critério de saída |
|---|---|---|---|
| índice completo gerado | o conector GitHub usado nesta execução lê e escreve arquivos, mas não fornece shell remoto no checkout privado | executar `build_living_system_index.py --write` em checkout autorizado | arquivo gerado, validado e diff revisado |
| relações produtor–consumidor | relações profundas entre repositórios não foram inferidas por nome | ler contratos, imports, artefatos e commits pinados | arestas com evidência e `claim_scope` |
| markdownlint integral | não foi acionado workflow remoto | executar lint local no checkout | zero erros no conjunto completo |
| suíte histórica completa | somente a nova unidade foi reproduzida isoladamente | executar testes existentes junto aos novos | zero regressões comprovadas |
| CI remoto | abrir PR acionaria workflow em `pull_request` | permanecer em branch até decisão explícita | execução autorizada e logs disponíveis |

## Estado de alegação

```text
claim_allowed = false
global_claim_allowed = false
```

A implementação é estruturalmente utilizável, mas sua integração final depende da geração do índice no checkout completo e da revisão das relações semânticas. O vazio restante está identificado, limitado e acionável.
