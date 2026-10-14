# 24 — Biblioflow federado: tokens simbólicos, custódia privada, ARM32 e gates (sucessor V1)

**Estado:** `DRAFT_SOURCE_BOUND / HOLD_NO_PROMOTION` · **Função:** extensão de rota e vocabulário, não novo codec nem prova de runtime · **Autoridade:** Mapa = roteador. **Data:** 2026-10-14.

## 0. Predecessores obrigatórios

Ler `biblioteconomia/INDICE_GERAL.md`, `biblioteconomia/23_NOVOEXPORT_BIBLIOTECA_SEMANTICA.md`, `biblioteconomia/02_VOCABULARIO_CONTROLADO.md`, `biblioteconomia/06_PROTOCOLO_BIBLIOTECONOMICO.md`, `data/biblioteconomia/novoexport_library_model.v1.json`, `indices/CROSS_SOURCE_REGISTRY.jsonl`, `indices/CADEIA_CUSTODIA_EVENTOS.jsonl` e `AGENTS.md`. Este documento **não** substitui tais instrumentos ou os modifica.

## 1. Fronteiras e superfícies

- **GitHub público (Mapa):** contrato, esquema, rotas genéricas, teste reprodutível e classificação. Nada de texto bruto, IDs privados, nomes de coleções pessoais, caminhos internos privados ou hashes que funcionem como identificadores de conversas.
- **GitHub privado:** cada produtor mantém código, histórico, testes e evidências em seu repositório autorizado; o controle público usa referência opaca sem capacidade de abrir dados privados. Nada de replicação implícita.
- **Drive público:** somente objetos explicitamente classificados como públicos e aprovados por revisão de divulgação.
- **Drive privado — NOVOexport:** fonte de shards, genealogia literal, datas, identidade de mensagem/conversa, recibos de custódia, assuntos e relações; indexação sem duplicar corpus. O novo lote recontado 2026-10-14 já tem quatro CSVs privados em `RAFAELIA_NOVOEXPORT_DRIVE_FULL_INDEX_20261012`: fonte por shard, genealogia de famílias lexicais, distribuição shard×mês, e localizadores de conversas. O Mapa **não importa seus identificadores nem seus conteúdos**.
- **alphaXiv:** bibliografia, papers, anotações e folders com acesso conforme `sharing_status` real; um paper público não torna privada anotação/folder público. DOI/arXiv ID prova rota bibliográfica, não valida automaticamente claim.
- **ARM32 / APK:** núcleo puro pode calcular índices/hashes sobre bytes autorizados e produzir receipts locais, mas OAuth, TLS, armazenamento persistente, Android SAF, sincronização e permissões são funções do host Android; execução física em aparelho é gate separado. Sem secrets embutidos no APK ou logs.

## 2. Entrada humana/IA

`START_HERE → HOTSTATE → ROUTE_PIN → SOURCE_MIN → AUTHORIZE → INDEX → TYPED_EDGES → EVIDENCE → RECEIPT → R3`.
Cada leitura distingue `SOURCE`, `ARTIFACT`, `EXECUTION`, `EVIDENCE` e `CLAIM` como classes diferentes. Restringir por assunto, tempo e autoridade, sem crawl global. Human/IA devem encontrar em no máximo três roots a fonte mínima; se não encontrarem, devolver `TOKEN_VAZIO` tipado e `next_probe` concreto, sem fabricar texto.

## 3. Biblioteca: dicionário, mapa, atlas, scaffold e biblio-manifold

- `dictionary`: superfície literal exata (UTF-8), Unicode code points opcionais, aliases apenas comprovados, contexto linguístico e jurídico, tradução separada de transliteração, glossário de escopo, versão de sentido.
- `map`: arestas dirigidas `appears_in`, `defined_by`, `similar_literal`, `co_occurs_with`, `derived_from`, `implements`, `tested_by`, `evidenced_by`, `supersedes`, `routes_to`; `similar_literal` e coocorrência não implicam equivalência/implementação.
- `atlas`: visão por provedor, licença, idioma, cultura, domínio, temporalidade (fonte/evento/observação), evidência, privacidade e estado epistemológico.
- `scaffold`: pacote mínimo `intent,source_locator,authority,source_hash_scope,typed_edges,gates,receipt_refs,gaps,rollback`.
- `biblioflow`: `DISCOVER → IDENTITY_BIND → DESCRIBE → AUTHORITY_CHECK → CLASSIFY → INDEX → RELATE → ROUTE → EVIDENCE_CHECK → APPEND_RECEIPT`. Executar sob orçamento bounded, sem loops desnecessários.

## 4. Léxico simbólico sem falsa tokenização

O módulo independente `data/biblioteconomia/federated_biblio_contract.v1.json` acrescenta tipos de dados; não substitui `data/semantics/semantic-dictionary.v1.jsonl`.

Para as superfícies `§, ∆, ∅, Π, Ω, ★, †, ‡, 4bit|4bit`:

- guardar `literal_utf8`, `codepoints` quando derivados exatamente, `language,script,jurisdiction` somente com fontes;
- guardar `lexical_presence`, `speaker_role`, `first_observed_event_time` e `source_ref` em livro **privado**, não no catálogo público;
- `UNDEFINED_SENSE` / `TOKEN_VAZIO_SEMANTIC` quando não existe definição desambiguada;
- `SIMBOLICO` para interpretação filosófica/cultural, `MATHEMATICALLY_DERIVED` para relação demonstrada, `SOURCE_ASSERTED` para afirmação sem execução;
- `U+2205 EMPTY SET` ≠ string vazia ≠ JSON null ≠ token ausente ≠ zero numérico. `U+00A7 SECTION SIGN` não é permissão jurídica geral; contexto, língua e jurisdição são facetas independentes;
- código de 8 bits formado por nibble alto + nibble baixo é aritmética exata. Palavra hipotética `10-bit address + 8-bit value + 2-bit parity = 20 bits` é `DESIGN_HYPOTHESIS` até formato, função de paridade e testes serem definidos;
- numa malha 10×10×10 há 1000 células, endereçáveis com 10 bits (24 códigos excedentes). Relações `21×2=42` e `70×7=490` são exatas; **`70×7=14` é falso como aritmética**, preservar como `SOURCE_LITERAL_MATH_CONTRADICTION`, não apagar nem reinterpretar sem testemunho;
- glifos e sequências não significam chaves criptográficas, tokens OAuth ou comandos executáveis.

## 5. Gates críticos e falsificadores

| Gate | Condição mínima (não presumir PASS) | Falsificador |
|---|---|---|
| SOURCE_IDENTITY | provider + conta autorizada + ID/ref + digest de bytes quando lidos + escopo | título similar, ID ausente ou digest divergente |
| ACCESS | público/privado/restrito/unknown e revisão de divulgação | link público para conteúdo privado; UNKNOWN → HOLD |
| CODE | produtor + exato commit + teste reproduzível sobre mesmo SHA | código inexistente no SHA ou teste fail |
| CI_PROVIDER | jobs/chaves/revisão independentes no exact HEAD; enforcement efetivo | branch sem proteção, check ausente, bypass ativo |
| LITERAL | bytes originais preservados, sem normalização destrutiva | alias colapsa dois símbolos/sentidos |
| SEMANTIC | cada aresta tem fonte; nenhuma promoção de coocorrência | falta fonte para `implements` |
| DEVICE_ARM32 | binário/APK hash + ABI32 + instalação + execução e receipt físico | build em x64/ARM64 apresentado como ARM32 |
| PRIVACY | nenhum ID secreto / corpo de conversa em repo público | vazamento detectado em diff |
| ALPHAXIV | ID de paper + folder sharing_status + claim citada | confusão entre public paper e nota privada |
| ROLLBACK | branch isolada + antecessor íntegro + reversão escopada | mutação da fonte primária ou perda de histórico |

Estados: `PASS_SCOPED`, `FAIL`, `HOLD`, `TOKEN_VAZIO`, `NOT_APPLICABLE`, `IMPLEMENTED_UNTESTED`. `TOKEN_VAZIO != 0`, `IMPLEMENTED_UNTESTED != PASS`. Publicação, merge e promoção sempre gates separados.

## 6. Dupla entrada bibliográfica / μWRITE

**ENTRY_A_SOURCE:** `provider,surface,authority,source_identity,byte_digest+scope,source_time,observed_time,access`.

**ENTRY_B_TRANSITION:** `operation,edge_type,from_state,to_state,evidence_refs,receipt_id,actor_authority,priority,rollback,next_probe`.

Toda ação com dado privado grava a dupla entrada **somente no ledger autorizado do Drive**. No GitHub, gravar exclusivamente a declaração pública desidentificada. Não excluir, mover, compartilhar ou sobrescrever os originais; correção por sucessor com o predecessor verificável.

## 7. Gradação de urgência

`P0`: vazamento, alteração sem autorização, quebra de custódia, falsa promoção → HOLD imediato.
`P1`: hash, identidade, CI ou dispositivo divergentes → bloqueia integração.
`P2`: alias/semântica, cronologia, índice inconsistente → corrigir por sucessor antes de claim.
`P3`: novos vínculos transdisciplinares e scaffolds → pesquisa sem elevar estado epistemológico.

## 8. R3 desta mudança

`F_ok`: biblioteconomia anterior localizada; auditoria de 51 shards com índices privados já executada; roteamento e fronteiras escritos.
`F_gap`: nenhuma prova nova de execução no aparelho, provider enforcement, revisão independente ou equivalência de todas as expressões; não dar PASS global.
`F_next`: validar contract JSON, revisão humana de divulgação e CI do SHA exato, depois vincular as provas via μWRITE; PR permanece DRAFT/NÃO PROMOVER.
`rollback`: fechar PR/reverter apenas estes novos arquivos, preservar conteúdo e commit histórico dos predecessores.
