# RAFAELIA — Context Route Index — 2026-08-13

State: `VERIFIED_LIMITED / APPEND_ONLY / claim_allowed=false`

## Invariante operacional

`kernel invariants -> index -> minimal relevant subgraph -> evidence -> append-only delta`

Não carregar o universo indiscriminadamente. Resolver primeiro a rota mínima e abrir bytes brutos apenas quando a pergunta exigir.

## A. Âncora longitudinal de conversas

- ID: `ART-CTX-20260813-001`
- SHA-256: `53fbfbc52d110d5815024ca851868555d23c3180cd73bb5433dd5f5bade9d93f`
- bytes ZIP: `305843744`
- integridade ZIP: `PASS`
- conversas: `2573`
- mensagens com payload: `239506`
- intervalo de criação UTC: `2025-02-12T00:08:06.258886Z` → `2025-10-06T16:30:36.847311Z`
- privacidade: conteúdo/títulos privados brutos não são copiados para este índice.
- estado: `VERIFIED_AGGREGATES_LOCAL`

Rota: `IDX-08 MEMORY -> custody -> hash -> filtro temporal/semântico -> conversa selecionada -> chunks -> nodes/edges -> Session Ledger/Mapa`.

## B. Âncora runtime Termux

- ID: `ART-RUNTIME-20260813-001`
- SHA-256: `e6265a57eb5ca363808488e3b01955958bed93bc0c8a0d281849b363b11027ec`
- bytes: `113880067`
- integridade ZIP/APK: `PASS`
- package string observada: `com.termux`
- certificado estático observado: `FDroid`
- ABIs: `arm64-v8a`, `armeabi-v7a`, `x86`, `x86_64`
- estado: `VERIFIED_STATIC`

Limite: relação com build custom RAFCODEphi e execução física deste SHA permanecem `TOKEN_VAZIO`.

Rota: `IDX-05 RUNTIME -> exact SHA -> static provenance -> compare build manifest -> physical receipt when required`.

## C. Família visual fractal

- família: `VIS-RAFAELIA-FRACTAL-20260813`
- itens: `7`
- estado: `SYMBOLIC_VISUAL_ARTIFACTS`
- scientific claim: `false`

Rota: `visual term -> exact image hash -> generator/parameter manifest -> formula relation only after provenance`.

Fronteira: `visual semantic carrier != generator provenance != mathematical derivation != scientific evidence`.

## Sete vértices de reconstrução

1. identidade — bytes/hash/tipo;
2. temporalidade — origem e intervalo;
3. privacidade — raw privado permanece fora do índice público;
4. semântica — conceito e relação sem promoção indevida;
5. execução — estático não equivale a runtime;
6. proveniência — fonte -> índice -> receipt;
7. fechamento — `TOKEN_VAZIO + closure gate + F_next`.

## Regra de ativação futura

1. resolver termos para `IDX/ROUTE`;
2. carregar invariantes compactos;
3. carregar somente âncoras/receipts relevantes;
4. abrir raw somente se necessário;
5. separar `SOURCE != INDEX != EXECUTION != EVIDENCE != CLAIM`;
6. preservar contradições/superseded;
7. gravar delta append-only com `F_ok/F_gap/F_next`.

## F_ok

- export longitudinal ancorado por SHA e métricas agregadas;
- APK Termux ancorado por SHA, certificado e ABIs;
- família visual ancorada por hashes;
- raw privado não replicado no índice.

## F_gap

- `TOKEN_VAZIO_CONVERSATION_ID_INDEX_REMOTE`;
- `TOKEN_VAZIO_CHUNK_GRAPH_MATERIALIZATION`;
- `TOKEN_VAZIO_CROSS_EXPORT_DEDUP`;
- `TOKEN_VAZIO_RELATION_TO_CUSTOM_RAFCODEPHI_APK`;
- `TOKEN_VAZIO_DEVICE_INSTALL_RECEIPT_THIS_EXACT_SHA`;
- `TOKEN_VAZIO_VISUAL_GENERATOR_SOURCE_BINDING`;
- `TOKEN_VAZIO_PARAMETER_MANIFESTS`.

## F_next

1. materializar índice de conversa privacy-preserving por ID/tempo/tópico;
2. ligar somente IDs selecionados ao grafo existente;
3. comparar o SHA do APK com manifests conhecidos RAFCODEphi;
4. localizar e ligar fonte/parâmetros dos visuais fractais.

Sem merge/release/promoção de claim por este índice.
