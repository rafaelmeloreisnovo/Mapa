# ATLAS:X — NOVO → CTI → ContextBundle: execução local

ID: `ATLAS:X-NOVO-CTI-LOCAL-20260906`.
Predecessor: `ATLAS:X-NOVO-RMRCTI-LLM-NAV-20260906`.
Estado: `IMPLEMENTED / MEASURED_LOCAL / APPEND_ONLY / claim_allowed=false`.

## Entrega e custódia

O contrato ganhou um adapter executável no Termux, com recuperação nativa do
produtor fixado `llamaRafaelia`. Mapa registra a relação e os limites do receipt;
a autoridade da implementação continua no produtor correspondente.

| Elemento | Ponteiro fixado |
|---|---|
| Termux — implementação | `1161f49de0ab0635420bab82144b7303c1e1a487` |
| Termux — hotfix anterior | `2ba17355776b6c974252e4f9c78fb2d220944444` |
| Termux — PR draft | [#423](https://github.com/rafaelmeloreisnovo/termux-app-rafacodephi/pull/423) |
| CTI — produtor privado | `llamaRafaelia@3dac5fd2c23a9c55361672d5d593d3e875146da3` |
| Rota usada no replay | `Mapa@9535ca98c8d87a35ac97f87283014b1ea5179078` |
| Receipt federado | [ATLAS_NOVO_CTI_LOCAL_ADAPTER_V1.json](../../receipts/2026-09-06_ATLAS_NOVO_CTI_LOCAL_ADAPTER_V1.json) |
| Guia e receipt do produtor | [Adapter V1](https://github.com/rafaelmeloreisnovo/termux-app-rafacodephi/blob/1161f49de0ab0635420bab82144b7303c1e1a487/docs/contracts/ATLAS_NOVO_CONTEXT_ADAPTER_V1.md) |
| L:X | `L:ATLAS-NOVO-CTI-LOCAL-20260906` |
| LEARN:X | `LEARN:ATLAS-NOVO-CTI-LOCAL-20260906` |

Rota executada: `ATLAS → export anexado delimitado → L → RMRCTI → ContextBundle → LEARN`.
O vínculo atual com o provider NOVOexport permanece `TOKEN_VAZIO`.

## Resultados medidos

| Gate | Resultado | Alcance |
|---|---|---|
| Build CTI fixado | PASS, exit 0 | C++17, GCC 13.3, Linux x86_64 |
| Envelope e integração nativa | 18/18 PASS, zero skips | 8 controles de contrato e 10 de integração |
| Export real: CTI ligado | 312 mensagens, 1 hit, 451 bytes de contexto | Uma conversa extraída do ZIP anexado |
| Mesma consulta: CTI desligado | Zero hits, nenhum ContextBundle | Controle de ausência do contexto |
| Consulta sem correspondência | Zero hits, nenhum ContextBundle | Controle negativo |
| Integridade da fonte | Bytes inalterados | Hash antes/depois; ZIP, membro e recorte ligados |
| CI público do envelope | PASS | [run 34050254430](https://github.com/rafaelmeloreisnovo/termux-app-rafacodephi/actions/runs/34050254430), commit da entrega |
| Proteção do provider | FAIL, exit 4 | [run 34050254402](https://github.com/rafaelmeloreisnovo/termux-app-rafacodephi/actions/runs/34050254402), configuração externa |
| Topologia declarada | PASS | 6 repositórios, 5 arestas, DAG conectado; sem prova de runtime |

O controle sintético usa um marcador único e seu fato associado. O recorte real
usa um termo observado na fonte; o trecho recuperado contém esse termo e texto
adicional da mensagem. A consulta e o corpo privado não são publicados.
Estes controles demonstram presença/ausência de recuperação; o uso causal por
uma **resposta gerada pelo LLaMA** ainda não foi executado.

## Correções sustentadas

1. O validator anterior aceitava a remoção de campos obrigatórios. O sucessor
   aplica as assertions do schema, integridade dos hashes e referências únicas.
2. O Mapa apontava para `docs/AGENTES.md` ausente. A entrada foi materializada
   em `9535ca98...`, com autoridade raiz preservada, e o lint dos arquivos
   alterados foi corrigido.
3. O comando `--lineage-check` do AGENTS não existe no comparator atual.
   A entrada agora exige os dois bundles selados e o quality floor; `--help`
   não é apresentado como execução desse gate.
4. A declaração nativa `g_opencl_handle` não era usada e quebrava o build com
   warnings como erros. Sua remoção passou em compilação local e preservou os
   bytes de `.text` no controle x86_64. Isso não certifica um APK ARM64.
5. Um teste multibyte expôs corte UTF-8 inválido no renderizador do produtor.
   A ponte deixou de serializar esse resultado não utilizado e monta o contexto
   com corte seguro. O caminho original do renderizador no servidor LLaMA
   permanece como lacuna própria; a falha inicial não foi apagada do receipt.

## Avaliação do GitHub e capacidades

O inventário retornou **86 repositórios** da conta. A leitura operacional desta
entrega foi delimitada ao Mapa, Termux e ao caminho CTI do llamaRafaelia; houve
conferência do contrato de entrada de RafGitTools e da identidade canônica RLL.
Isso não equivale a auditoria integral dos 86 repositórios.

| Skill solicitada | Aplicação concreta |
|---|---|
| rafaelia-query-system | Contrato de consulta limitado; ranking real do produtor; no-hit explícito |
| evoluidor-sistema | Baseline, falhas reproduzidas, hotfix, controles e rollback |
| rafaelia-evidence-gate | Separação entre fixture, recorte real, build, geração e dispositivo |
| mestre-zen | Fechamento do adapter delimitado e indicação do próximo gate executável |
| roteador-universo-rafaelia | Mapa → Termux → CTI, com autoridades e capacidades mínimas |
| rafaelia-omega-orchestrator | Bootstrap canônico, gates locais e retorno à memória |
| rafaelia-master-architecture | Entradas/saídas, dependências, privacidade e limites de implantação |
| rafaelia-toroidal-geometry | Nenhum ΔP, recorrência ou imagem foi promovido a atrator/prova física |
| rastreador-origem | Commit, blob, SHA-256, membro do ZIP, recorte e predecessor longitudinal |

GitHub, Google Drive e execução local foram usados onde havia uma ação concreta.
Plugins recomendados mas não instalados não foram apresentados como executados.
Não se acionaram serviços de mensagens, treinamento ou geração de imagens.

## Preflight federado Q01..Q12

| Questão | Resposta desta entrega |
|---|---|
| Q01 — identidade | Curadoria federada e implementação delimitada autorizada pelo usuário |
| Q02 — fonte | Commits e hashes no receipt; leitura source-first dos produtores citados |
| Q03 — autoridade | Mapa roteia; Termux orquestra; llamaRafaelia extrai/rankeia CTI |
| Q04 — fronteira | Medição local hospedada não promove geração, Android ou federação certificada |
| Q05 — índices | AGENTS, bootstrap ChatGPT, ontology, authority pyramid, Atlas Routing Index e auditoria federada |
| Q06 — produtor | Termux PR #423 e oito blobs CTI fixados pelo manifesto do build |
| Q07 — lacunas | Provider atual, corpus integral, geração, privacidade específica, visual, device e proteção remota |
| Q08 — evidência | Receipt de 18 testes, três controles reais, build e CI do envelope no commit publicado |
| Q09 — gate | Validator, testes adversariais/nativos, hashes, topologia declarada e lint dos arquivos alterados |
| Q10 — parada | Sem pesos/modelo executável, device ou provider verificável, preservar TOKEN_VAZIO correspondente |
| Q11 — registro | Receipt no produtor, este delta/índice, L:X e LEARN:X append-only |
| Q12 — governança | Sem divulgar corpus privado, sobrescrever NOVOexport, alterar pesos, forçar refs ou fazer merge |

## Sete direções de leitura

| Direção | Evidência ou limite |
|---|---|
| Identidade | Fonte, commit e hash explícitos |
| Epistêmica | Recuperação medida; geração não executada |
| Execução | Host x86_64; Python/C++ hospedados, não freestanding |
| Segurança | Schema fail-closed, limites, processos sem shell, saídas exclusivas |
| Privacidade | Gate nativo obrigatório antes do contexto; payload público minimizado |
| Autoridade | Dono do dado/ranking/orquestração/federação separado |
| Transição | Receipt local e CI do envelope não removem gates de provider/dispositivo |

## Lacunas preservadas e reconciliação

As PRs originais #422 e #533 foram mescladas por outra operação durante esta
entrega. A checagem anterior à publicação detectou a mudança; as árvores dos
novos defaults eram idênticas às baselines. Esta entrega foi então direcionada
a drafts sucessoras, sem force push e sem realizar merge.

O gate remoto de proteção encontrou ausência de `required_status_checks`,
inadequação da regra de pull request ao contrato do gate e ausência do contexto
obrigatório `provider-protection`. A configuração não foi enfraquecida.

Os três caminhos de bootstrap de skills abaixo não foram localizados no Mapa
nem por título exato na busca Drive desta sessão. Não foram inventados:

- `memory_bridge/contracts/PERMANENT_MEMORY_INVARIANT_V1.md`;
- `memory_bridge/indexes/PERMANENT_MEMORY_INDEX.md`;
- `memory_bridge/contracts/OMEGA_ACTIVATE_POLICY_V1.md`.

Gates ainda abertos: geração LLaMA off/on/no-hit, provider NOVOexport atual,
replay GAIA, Private/Voynich e RLL, renderizador UTF-8 original, execução Android,
Vectras físico, comparação de bundles independentes e proteção remota. Os sete
PNGs anexados estão presentes; seus bytes não foram usados como prova física.

`retrieval != training`; `model_output != evidence`; `ΔP != attractor`;
`visual_similarity != physical_equivalence`; `TOKEN_VAZIO != 0`.

F_ok: implementação, controles e receipts locais com retorno navegável.
F_gap: gates acima com escopo e autoridade preservados.
F_next: executar a geração LLaMA fixada consumindo o ContextBundle, repetir
off/on/no-hit e registrar resposta/hash, sem atualizar pesos.
