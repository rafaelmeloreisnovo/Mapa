# RAFAELIA — Observador, observação e caminhos multifilamento V1

Estado: `SYNTHETIC_KAT / APPEND_ONLY_PROPOSAL / claim_allowed=false`

## Fronteira de autoridade

Este é um pré-gate **semântico e topológico** para navegação humano–IA: não substitui `indices/RAFAELIA_RISK_OBSERVATION_LEDGER_V1.md`, `docs/FEEDBACK_EVENT_NO_REGRESSION_V1.md`, `schemas/proof-custody-receipt.schema.json`, nem as ontologias `data/semantics/typed-void-lattice.v1.json` e `data/semantics/empty-state-ontology.v1.json`.

Não contém observações pessoais, testemunhos reais, ciência empiricamente comprovada, segredos nem aprovações independentes. Datas e observadores no arquivo de fixtures são *fictícios e explicitamente sintéticos*. O objetivo é **falsificar colapsos indevidos**, não determinar a verdade de um evento externo.

## Cada nova observação: curso verificável

`INTENT → OBSERVER_SCOPE → SOURCE_LOCATOR + REVISION → OBSERVATION_TIME → EFFECTIVE_TIME_OR_TYPED_VOID → LEXICAL/SEMANTIC_KIND → EPISTEMIC_STATE → GRAPH_LINKS → FALSIFIER → GATE → RECEIPT → μWRITE → R3`

Registre os papéis separadamente: **observador** (humano, instrumento, serviço ou IA, com competência declarada), **sujeito/objeto observado**, **canal**, **tempo da leitura**, **tempo do fenômeno** (que pode continuar desconhecido), **fonte**, **revisão**, **hash quando os bytes realmente estiverem disponíveis**, **recibo**, **autoridade** e **risco de inferência**.

`NEWLY_OBSERVED` significa uma observação recém-registrada, **não** descoberta nova na realidade nem prova de novidade científica. `IGNORED` e `FORGOTTEN` são **estados de registro/atenção**, nunca prova de inexistência. `ATEMPORAL` significa vínculo temporal não estabelecido no escopo do registro, não a inexistência do tempo.

## Vocabulário de conduta e classificação

As áreas cobertas pelos oito casos sintéticos são `atencao, atendimento, atuacao, atualizacao, revisao, recusa, bug, erro, edicao, pensamento, permutacao, anomalia`.

Os marcadores são `POSSIBLE, VERBAL, ATEMPORAL, IGNORED, NONVERBAL, INCONSISTENT, FORGOTTEN, PARADOX, NONLINEAR, MULTIFILAMENT, NEWLY_OBSERVED, TOKEN_VAZIO, UNKNOWN`. `NONVERBAL` é o alias de entrada proposto para `averbal`; os termos originais ficam preservados no registro de ingestão real.

**Canal e incerteza não são a mesma variável.** Um evento verbal pode ser falso; uma medição não verbal pode ser válida ou ambígua. Observador ≠ testemunha independente ≠ aprovador ≠ autoridade de merge.

## Grafo com caminhos múltiplos

Cada `event_id` é imutável; cada `sequence` corresponde à ordem de ingestão. Os arcos tipados são `FOLLOWS, BRANCHES_FROM, PARALLEL_WITH, CONTRADICTS, SUPERSEDES, BLOCKED_BY, CAUSE_CANDIDATE`.

- `CONTRADICTS` preserva a oposição sem eleger vencedor pelo peso.
- `SUPERSEDES` aponta para um predecessor já existente; não o exclui.
- `CAUSE_CANDIDATE` registra apenas hipótese, não causalidade.
- `PARALLEL_WITH` e `MULTIFILAMENT` permitem caminhos concorrentes sem igualdade ou linearização forçada.

Neste V1 sintético, cada arco aponta para evento já ingerido; links futuros são `TOKEN_VAZIO_TARGET_NOT_YET_OBSERVED` até existir um identificador confirmado. A classe `MULTIFILAMENT` descreve topologia de registro, não um teorema de redes complexas.

## Contrato do recibo real

A primeira ingestão autorizada de uma observação real exigirá `observation_id`, ponteiro de fonte, revisão e hash ou `TOKEN_VAZIO_BYTES_NOT_OBSERVED`, ordinal/trecho, canal/gramática, `observer_id` pseudonimizado quando necessário, `observed_at`, `effective_at` ou vazio tipado, estado epistêmico, arestas, contradições, falsificador reproduzível, CI/execução por SHA, privacidade/autoria, autoridade, gate e caminho de rollback. **Não substituir um hash de conteúdo por um identificador de commit sem indicar a diferença.** Quando fonte, observador ou autoridade não puderem ser confirmados: `claim_allowed=false`.

## Testes e uso

```sh
python3 -m unittest -v tests.test_observer_paths_v1
python3 tools/validate_observer_paths_v1.py
```

O validador deve rejeitar: promoção artificial, revisor sintético tratado como humano, referência inexistente, aresta `SUPERSEDES` futura, contradição ocultada, timestamp ausente, tempo efetivo nulo não tipado, SHA-256 inventado, evidência real simulada, recusa promovida, categoria nova sem vetor e causalidade promovida por uma aresta.

## R3 / rollback

**F_ok**: oito casos sintéticos, categorias cobertas e falsificadores. **F_gap**: observações de corpus real, hashes dos bytes reais, revisões independentes, CodeScan, proteção e enforcement GitHub. **F_next**: obter recibo terminal exato desta branch; ligar primeiro evento externo de baixo risco apenas por fonte/autorização real; não fazer merge até requisitos administrativos vigentes estarem comprovados. **Rollback**: encerrar PR draft; nenhuma fonte histórica é apagada.
