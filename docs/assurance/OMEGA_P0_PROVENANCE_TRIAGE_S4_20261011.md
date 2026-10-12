# Auditoria Ω — triagem profunda de proveniência, lacunas e urgências S4

**Escopo:** revisão adversarial do ledger privado e das três PRs draft:
Mapa #752; RafPolimata #435; RafGitTools #667. Integra a rota de autoria
Mapa #751 / RafPolimata #434 / RafGitTools #666 sem promover código.
**Regra:** urgência ordena execução, **não aumenta a verdade**.

## Resultado de reanálise

A classificação anterior de charts de busca global como pertencentes ao
NOVOexport foi **falsificada** por metadados `parent_ids` do Drive:
a rota Office vai ao pacote de teste de segurança de terceiros;
a rota Dart vai a componentes upstream Flutter; a rota DOT vai a
`RAFAELIA_UPLOAD/DIAGRAMAS`. O snapshot histórico foi preservado;
o sucessor classifica cada origem de forma explícita.

A correção não fornece um vínculo entre o gráfico e uma planilha
autêntica, não prova licença/autoria e não autentica os metadados contra
um ator que forje a árvore inteira. Esses elos permanecem **P0**.

O código L0 agora acrescentou `raf_fs_typed_gap.h`: dez tipos
de zero/vazio e vínculo de recibo **CANDIDATO**. CI dedicada inicial
passou com 33 verificações e seis compilações freestanding sem
símbolos externos; não substitui SHA, rights, device e revisão.
O executor hosted de RafGitTools agora possui
`verify_chart_source_ancestry_v1.py`, 21 testes sintéticos:
`PASS_STRUCTURAL_ONLY` não significa provider-authenticated.

O validador do Mapa teve uma incerteza detectada por falsificação:
aceitava campos extras capazes de sugerir aprovações implícitas,
troca de responsável sem autorização e rótulos causais inventados.
Agora possui whitelists de campos S1, vínculos de ownership e
epistemologia de arestas; um teste encontrou conflito real entre
`receipt` de evidência e `receipt` de rollback, reparado por dois
esquemas distintos. O resultado do novo HEAD precisa de CI terminal.

## Matriz integral de 25 ausências

| ID | Prioridade | Estado documental | Evidência para encerramento |
| --- | --- | --- | --- |
| G001 | P1 | OPEN | 51 shards varridos com coverage e fonte privada |
| G002 | P1 | OPEN | first-seen exato por mensagem/role/time |
| G003 | P1 | OPEN | separação user/assistant e fonte dos counts |
| G004 | P1 | OPEN | aliases com namespaces, não coocorrência |
| G005 | P1 | OPEN | expressão→domínio→mensagem→oráculo |
| G006 | P1 | OPEN | conceito→repo→commit→path do produtor |
| G007 | P1 | OPEN | equivalência matemática independente por domínio |
| G008 | P1 | OPEN | chunk chain sem perda de contexto, round-trip |
| G009 | **P0** | PARTIAL | hash bytes RAW por shard/source, reconsulta |
| G010 | **P0** | OPEN | run + artifact + SHA no HEAD exato |
| G011 | **P0** | PARTIAL | XML→rels→pacote→workbook real; ancestry externa |
| G012 | **P0** | OPEN | direitos/avisos por arquivo, revisão independente |
| G013 | **P0** | FAIL_OBSERVED | branch protection, enforcement e CodeScan provider |
| G014 | **P0** | OPEN | aprovação independente do HEAD exato |
| G015 | **P0** | NOT_RUN | binário→APK/device→log+recibo físico |
| G016 | **P0** | OPEN | RLL fit/covariância/priors/backends/ΛCDM comparáveis |
| G017 | P1 | PARTIAL | junta 137 zonas a 136 métricas sem preenchimento fictício |
| G018 | **P0** | OPEN | vínculo da sessão composta ao ID real de export |
| G019 | P1 | OPEN | origem/código do plugin LAMA-barro, não LLaMA |
| G020 | P1 | NOT_RUN | execução física de saída áudio com receipt |
| G021 | P1 | OPEN | replay independente de eventos e corrupção adversarial |
| G022 | P1 | OPEN | cada fonte de fala/data ligada ao evento real |
| G023 | **P0** | NOT_RUN | SAF/Drive consent e política privada fonte a fonte |
| G024 | P1 | OPEN | producer e consumer com recebimentos compatíveis |
| G025 | **P0** | OPEN | ancestralidade/copyleft upstream e licenças por trecho |

Estados nesta tabela são os estados observados **do manifesto S1/S3**.
Um algoritmo implementado **não** extingue automaticamente o gap
externo correspondente.

## Ordens de dependência, sem bypass

**Raiz da legitimidade:** G023 autorização de leitura → G009 hash dos
bytes lidos → G001/G008 cobertura → G002/G003 genealogia → G018
vínculo da conversa real → G022 cronologia completa.

**Raiz de chart:** G025 upstream/autor → G012 direitos e avisos →
G011 fonte OOXML por relacionamento (a ancestralidade de pastas é
só filtro; não é autorização) → resultado de plot/RLL que continua
dependente de G016 para validação científica.

**Raiz de promoção:** G010 execução no HEAD exato → G013 provider
enforcement → G014 revisão independente → decisão humana por PR.
Um script Python PASS nunca substitui os controles do GitHub.

**Raiz de runtime:** construir não equivale a executar G015/G020.
O L0 `raf_fs_typed_gap` só captura candidatos, com direitos,
dispositivo e receipts externos ainda desconhecidos.

## Evidências materiais versus inferências

| Evidência | Escopo real | Não prova |
| --- | --- | --- |
| Drive `parent_ids` de charts | encadeamento de pastas consultado | bytes/autoria/licença ou pertencimento ao NOVOexport |
| Gate Mapa de 70+ falsificadores | consistência de metadados públicos | identidade histórica da sessão ou cobertura de corpus |
| Host C O0/O2/O3 + seis objetos ISA | semântica sintética e compile zero-runtime | hardware ARM, app instalado ou ciência |
| RGT ancestry `PASS_STRUCTURAL_ONLY` | integridade topológica de um snapshot fornecido | autenticação do provedor, consent, metadata assinada |
| RLL F1–F10 manifest | artefato de planejamento de figuras | posterior/chi²/reprodução independente |

## Contraprovas prioritárias e resposta operacional

- **Falsificar origem:** trocar parent de chart para um diretório fora do root; o
  verificador deve bloquear, e nunca transportar bytes ao Mapa.
- **Falsificar confiança:** acrescentar `approved=true` a nó, aresta,
  gap ou recibo; schema S1 deve rejeitar.
- **Falsificar responsável:** mudar G011 de RafGitTools para Mapa;
  validação deve recusar reatribuição sem nova versão/proveniência.
- **Falsificar ciência:** fazer `F10/RLL` retornar PASS a partir de
  gráfico de exemplo; gate independente deve bloquear.
- **Falsificar runtime:** trocar `CROSS_COMPILED` por `DEVICE_PASS`;
  sempre barrar na ausência de receipt físico.
- **Falsificar vazio:** converter TOKEN_VAZIO→0 ou
  STRUCTURALLY_BOUND_CANDIDATE→PROVEN; L0 recusa.
- **Falsificar cadeia de custódia:** corromper um único byte após
  SHA privado e verificar recusa do receipt. Ainda **NOT_RUN** em
  fontes reais, portanto não declarar fechamento.

## F_ok, F_gap, F_next e rollback

F_ok = matrizes, IDs G001–G025, rotas, correção de charts, alterações
source-side e gate adversarial escopado, vinculados aos PRs draft.

F_gap = fontes reais e autorizações, workbook/relationships,
autoria/redistribuição, revisão independente, enforcement provider,
temporalidade exata de mensagens, RLL robust e dispositivo físico.

F_next = obter autorização, identificar **um** chart real sob root
correto, validar metadados de provider e bytes em custódia privada,
relacionar o workbook/intervalo, obter oracle independente e
integrar pelo contrato sem copiar obra upstream. Repetir em lotes
pequenos e só depois ampliar cobertura do corpus.

Rollback = fechamento das PRs drafts sem merge, retenção de
predecessores e receipts, substituição apenas por sucessor versionado.
Nenhum dado fonte foi apagado, movido ou publicado pela triagem.
