# RAFAELIA — Pending Authorization and Gaps

**Estado:** ACTIVE_QUEUE  
**Escopo:** mudanças que não devem ser promovidas automaticamente  
**claim_allowed:** false

## Princípio

A indexação e a governança podem avançar por branches de trabalho, índices derivados, manifests, receipts e mapas. Mudanças nos repositórios produtores, autoridades canônicas ou superfícies públicas permanecem nesta fila até revisão adequada.

## Pendências atuais

### P-001 — Alterações em READMEs produtores

Requer leitura direta, comparação com estado material, avaliação de risco e PR específico por repositório. Não alterar em massa apenas para padronização estética.

### P-002 — AGENTS.md, CLAUDE.md, GEMINI.md e instruções de IA

Inventariar primeiro os arquivos existentes, escopo, precedência, conflitos e autoridade. Criar novo arquivo somente quando houver lacuna comprovada e necessidade operacional clara.

### P-003 — MCP e integrações de ferramentas

Não criar configuração MCP genérica. Mapear interfaces, dados, permissões, fronteiras de privacidade, autenticação, operações permitidas e rollback antes de propor qualquer arquivo.

### P-004 — Mudança de autoridade canônica

Qualquer promoção de repositório, documento, índice ou dataset para fonte primária exige decisão humana registrada, predecessores e impacto.

### P-005 — Conteúdo privado ou sensível

Não copiar para índice público. Criar apenas referência tipada, classificação de sensibilidade e localização restrita quando autorizado.

### P-006 — Workflows, releases e automação

Workflow novo, alteração operacional, release, tag, merge ou publicação requer gate próprio, risco, rollback e receipt.

## Lacunas técnicas

- cobertura integral dos repositórios ainda incompleta;
- documentos prioritários localizados, mas vários permanecem `PRESENT_UNREAD`;
- blob SHA e commit não capturados para todos os objetos;
- árvore estrutural de arquivos ainda não iniciada;
- cruzamento entre documentação declarada e estado material ainda parcial;
- classificação de privacidade e autoridade por repositório ainda parcial.

## Próximo gate

Continuar a leitura por lotes, aplicar o protocolo universal de indexação e produzir PRs específicos apenas quando a mudança no produtor for necessária, segura e reversível.
