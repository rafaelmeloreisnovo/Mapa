# README Universe — Pendências, Autorizações e Gaps

**Estado:** `ACTIVE_QUEUE`
**Política:** nenhuma alteração nos READMEs produtores sem revisão específica.
**claim_allowed:** `false`

## Sem autorização adicional

Podem ser executados em branch de trabalho:

- leitura direta de READMEs;
- criação de nós e relações no índice do `Mapa`;
- registro de refs, blob SHAs e estados epistemológicos;
- classificação de README raiz, subsistema, evidência, operacional, referência e arquivo;
- criação de receipts append-only;
- correção do próprio índice quando preservado o histórico Git.

## Exigem decisão humana ou PR específico

- alterar README de repositório produtor;
- mover conteúdo filosófico, jurídico, espiritual ou científico entre arquivos;
- instalar ou executar scripts de build;
- promover roadmap para `IMPLEMENTED`;
- expor conteúdo privado em índice público;
- introduzir `AGENTS.md`, `MCP.md` ou instruções automáticas em repositórios que ainda não possuam contrato de governança;
- mudar autoridade primária de uma classe de objeto;
- publicar claims científicos, jurídicos, financeiros ou de segurança.

## Fila

| ID | Repositório/Classe | Gap | Risco | Próximo gate |
|---|---|---|---|---|
| `PEND-README-001` | demais repositórios | README raiz ainda não lido diretamente | médio | leitura + blob/ref |
| `PEND-README-002` | READMEs internos | relevância e autoridade não classificadas | médio | leitura por taxonomia |
| `PEND-AGENTS-001` | ecossistema | cobertura de `AGENTS.md` desconhecida | alto | inventariar antes de criar |
| `PEND-MCP-001` | ecossistema | necessidades MCP não determinadas | alto | derivar após mapa de interfaces |
| `PEND-PUBLIC-001` | repositórios públicos | risco de exposição de memória privada | crítico | revisão de sensibilidade |
| `PEND-TREE-001` | árvore de arquivos | camada ainda não autorizada nesta fase | baixo | aguardar próximo prompt |

## Regra de criação futura

Um novo arquivo de governança somente será proposto quando houver:

```text
necessidade observada
+ autoridade definida
+ escopo limitado
+ ausência de duplicata
+ rollback Git
+ revisão de sensibilidade
```

## F_next

Continuar o lote de leitura; alimentar `readme_nodes.v1.jsonl`; criar relações somente a partir do que o README declara ou de metadados verificáveis.
