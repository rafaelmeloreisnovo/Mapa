# NOVOexport / charts / rotas / índices — reconstrução de auditoria v1

**Estado:** RECONSTRUCTED_SCOPED_METADATA / DRAFT / NÃO PROMOVER  
**Autoridade:** Mapa roteia, não governa a fonte original nem promove prova.  
**Fonte:** Drive oficial lido na sessão de 2026-10-11, sem copiar corpus nem
  fontes privadas para este repositório público.  
**Payload público:** `data/assurance/novoexport-chart-route-audit.v1.json`
é projeção sanitizada, sem nomes privados, bytes, IDs internos do Drive,
hashes brutos de corpus nem alegações de execução de software/dispositivo.

## 1. Roteamento vigente e drift dos índices

- **START HERE CANONICAL V2.2** é bootstrap ativo, aponta e não vira ledger.
- **CANONICAL INDEX MINIMUM** ainda contém prefixo histórico V2.1, e
  **INVARIANTS HOTSET** mantém o antigo START LITE em uma descrição
  de rota. Estes apontamentos são material histórico: resolver sucessor V2.2;
  **não reescrever nem apagar predecessores**.
- **ROUTES_OMEGA R0001V2** estabelece CURRENT_STATE → índice → manifold
  → contexto mínimo → source owner → evidência/gap → receipt → μWRITE.
- Leitura larga do corpus somente em via privada e autorização de origem;
  `INDEX ≠ FULL_SEMANTIC_READ`; `FILE_NAME ≠ IDENTITY`.

## 2. Reconstrução de família de charts

| Domínio | Observação real | Estado / contraprova |
| --- | --- | --- |
| Office chart caches | seis XMLs `chart1.xml`–`chart6.xml`: bar3D (1–4), line3D (5), surface3D (6), referências a `Sheet1!A2:D5`; cinco usam `Series 1/Category 1`, um tem `Sales` | representações de exemplo, workbook/dataset original não lido: `TOKEN_VAZIO_WORKBOOK`; não aceitar como benchmark |
| `charts/` arquivos Dart | `vertical_fraction_bar.dart`, `line_chart.dart`, `pie_chart.dart` | componentes de interface, origem/licença/código de renderização não auditados por bloco |
| Graphviz | `camada_sem_nome.dot`: Z0→Intenção→Ciclo→Espelho→FCEA→Ω | diagrama topológico, não execução do grafo |
| Diagrama toroidal | `diagrama_fractal_toroidal.md`, loop ψχρΔΣΩ, fórmulas e figuras Mermaid | contém símbolos e constantes exemplares: hipótese/documento ≠ medição |
| Formula Memory / grafo namespace | `GRAPH_NAMESPACE_CROSSWALK_V2` e `JUNCTION_MATRIX_V1` | icosfera f=2: V42 E120 F80, vs C42 ±6±7: V42 E84 grau4; mesma cardinalidade ≠ mesmo grafo |
| RLL Figures F1–F10 | F1 diagrama claim-gated, F2–F10 manifesto histórico | RLL produtor precisa de parâmetros/covariâncias/fit/posterior/backend por figura; não propagar smoke para claim |

Chart XML foi examinado localmente a partir de arquivos individualmente
baixados do Drive; somente tipos, contagens, ranges e status agregados são
incluídos aqui. Para custódia fechada faltam: arquivo OOXML pai e suas
relationships, workbook real, hash e licença em receipts privados. Os XMLs
isolados não identificam qual obra/autor/dataset os gerou.

## 3. Nova matriz de implementação por repositório

**RafGitTools** = pipeline privado de seleção de arquivo e consentimento,
staging read-only, autenticação externa, origem, fileId/private digest,
relationship parent→chart/workbook/data range, status do produtor, recibo
e projeção pública com zero dados privados. O conteúdo não entra no log
público do Mapa. Recibo com rollback e sucessor.

**RafPolimata** = núcleo C freestanding autoral sem libc/heap/syscalls:
parser/validador determinístico de memória entregue pelo chamador,
representação Q16.16 quando válida e estatísticas tipadas. Grupos matemáticos
separados por namespace e invariantes. Nenhum loop/símbolo sob comando de
comentário; flags reais e verificação de codegen. Não fingir suporte a
ZIP/OOXML/CSV completo só porque existe um gráfico cache.

**Mapa** = graph/route/atlas/gap public sanitized metadata. Relações
`OBSERVED_IN`, `SOURCE_OF`, `DERIVED_FROM`, `DEPICTS`, `IMPLEMENTS`,
`EVIDENCES`, `CANDIDATE_ALIAS` têm semânticas diferentes. Associação de
título, número 42, SVG ou fórmula não deve gerar equivalência ou causalidade.

**RLL** = autoridade de domínio científico: F1 documenta pipeline, F2–F6
exigem outputs com source/parameters, F7/F9/F10 aguardam robust fit,
covariâncias/datasets/backends; CLAIM_ALLOWED=FALSE sem gate global.

## 4. Cobertura NOVOexport: baseline ≠ leitura integral

Roteador NOVOexport declara 51 shards 000..050, 5054 raízes, 5052 conversas
não vazias, 111367 mensagens user e 185427 assistant. São números de
**índice derivado**, ainda sem varredura independente integral neste audit.

`G001` literal scan, `G002` first-seen, `G003` divisão de papéis,
`G004` aliases, `G005` fórmula, `G006` repo,
`G007` equivalência, `G008` chunks, `G009` hashes parciais,
`G010` runtime/CI permanecem governados.

O manifesto de genealogia requer
`raw_shard→conversation_id→message_id→role→timestamp→context→token→
concept→formula→project→commit→artifact→evidence→claim gate`.
Coocorrência não é causalidade; índice não é leitura semântica;
similaridade não é igualdade de bytes, autoria nem fórmula.

## 5. Falsificadores novos

Validador/tabela sintética (não leitor de Drive):

- impede promover gráfico Office cache sem workbook;
- impede rotular RLL robusta/posterior a partir de manifesto ou smoke;
- impede confundir C42 e icosfera F2;
- impede trocar contagem de shards por genealogia completa;
- impede atribuir autoridade a Mapa em lugar do produtor;
- impede introduzir URLs internas privadas no índice público;
- impede tratar LAMA plugin de barro como upstream LLaMA;
- impede usar `rapport` como evidência;
- impede `claim_allowed=true` sem prova externa.

Validação da matriz é **somente conformidade interna de metadados**,
não prova de autoria, completude, integridade criptográfica, revisão,
licenciamento, execução física, superioridade de algoritmo ou ciência.

## 6. Matriz F_ok / F_gap / F_next

F_ok = rotas Drive lidas, famílias chart classificadas e fontes de
fórmulas/riscos verificadas com leitura delimitada; índice sanitizado,
testes adversariais e CI dedicados adicionados em PR isolada.

F_gap = lineage OOXML/workbook/dataset dos seis charts, proveniência dos
Dart e imagens; full scan de shards e first-seen, privacidade e consentimento
para export; índice histórico drift, reviewer P0, source licenses, integridade
de provider, aparelhos, RLL robust, evidência externa.

F_next = **uma fatia vertical verificável**: selecionar 1 chart autorizado
com arquivo pai + workbook + dados; registrar hash/parent e vínculo exato;
ler fonte privada sem publicar bytes; testar serialização/roundtrip com oracle;
criar endpoint de contrato L0 em PR produtor; comparar pares de cálculos;
registrar CI exact-head e rollback. Só depois ampliar famílias.

Rollback = fechar esta PR draft; nenhum dado raw, branch main,
provider rules, release ou hardware alterado.

## S3 — contraprova de proveniência observada no Drive

A busca global do Drive retornou charts que, após inspeção de
`parent_ids` até seus ancestrais, **não pertencem ao ramo NOVOexport
verificado**. A associação anterior era inferência indevida e fica
explicitamente corrigida, com predecessor preservado.

| Família | Ancestral observado | Regra de admissão |
| --- | --- | --- |
| XML Office chart1..6 | `metasploit-framework/data/exploits/CVE-2013-3906/word/charts` | Amostra de fixture de segurança de terceiros, jamais fonte científica/autorais sem novo vínculo |
| Dart `charts/` | `dev/integration_tests/new_gallery/lib/studies/rally` | Exemplo upstream Flutter UI, não motor matemático RAFAELIA |
| Graphviz DOT/PNG | `RAFAELIA_UPLOAD/DIAGRAMAS` | Diagrama roteável, autoria/execução não demonstradas |

**Escopo da observação:** metadados e caminho de pastas do provedor,
não análise jurídica/licença, abertura segura do pacote OOXML original,
prova criptográfica completa ou inspeção de conteúdo executável.

**Segurança:** não abrir/executar payload CVE, não processar macro,
externalData, script ou extração automática fora de sandbox de origem.
É proibido copiar a fixture de terceiros para implementação autoral.
Sem consentimento e direitos, G011/G012 permanecem abertos.
As seis amostras são **out-of-scope de NOVOexport** salvo novo
`source_ref` independente e verificável. `GLOBAL_SEARCH !=
NOVOEXPORT_MEMBERSHIP`.
