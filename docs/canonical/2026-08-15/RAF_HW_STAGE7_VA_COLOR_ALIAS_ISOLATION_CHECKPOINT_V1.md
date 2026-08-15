# RAF_HW_STAGE7_VA_COLOR_ALIAS_ISOLATION — Checkpoint V1 — 2026-08-15

## Estado

- ambiente físico: Android/Termux ARM32, sem root;
- build observado: ELF 32-bit ARM EABI5 PIE, Android 24, NDK r29, clang 21.1.8;
- estado: `VERIFIED_LIMITED_PENDING_EXTERNAL_REPLICATION`;
- `claim_allowed_exact_topology=false`;
- `PURE_TLB_IDENTITY=FALSE`;
- `CACHE_EXACT_SIZE=TOKEN_VAZIO`;
- `TLB_EXACT_ENTRIES=TOKEN_VAZIO`.

Invariantes: measured != inferred != simulated; benchmark effect != exact microarchitectural identity; geometry sensitivity != proof of TLB set mapping; negative results are preserved.

## Contratos físicos testados

1. `SINGLEVA`: um endereço virtual / uma página física file-backed de 4 KiB.
2. `ALIAS_4K`: N endereços virtuais distintos para a mesma página física; stride VA de 4 KiB; bits VA 12..15 percorrem 16 classes.
3. `ALIAS_64K`: N endereços virtuais distintos para a mesma página física; stride VA de 64 KiB; low16 congruente.
4. `DISTINCT_64K`: N endereços virtuais distintos para N páginas físicas distintas; stride VA de 64 KiB; low16 congruente.

Contrastes predeclarados:

- color/geometry: `ALIAS_4K / ALIAS_64K`;
- conservative multi-VA: `min(ALIAS_4K, ALIAS_64K) / SINGLEVA`;
- physical footprint: `DISTINCT_64K / ALIAS_64K`.

## Cobertura e qualidade da execução

- samples: 11,520;
- migração: 11,520/11,520 PASS;
- samples com frequência estável dentro da medição: 11,479/11,520;
- quartetos completos: 2,880;
- quartetos strict same-frequency: 2,838;
- CPUs: 0, 3, 4, 7;
- pontos: 96,104,112,116,120,124,128,132,136,140,144,148,152,160,176,192,208,224 páginas;
- 8 seeds, 5 repeats, 256 rounds.

## Resultado central

A sensibilidade à geometria VA foi material e reproduzida em todas as CPUs medidas.

Métricas globais, apenas quartetos strict same-frequency:

- `median(ALIAS_4K/ALIAS_64K) = 0.549205`;
- `median(min(ALIAS_4K,ALIAS_64K)/SINGLEVA) = 1.219893`;
- `median(DISTINCT_64K/ALIAS_64K) = 1.108896`;
- `color_within_5pct_pages = 0/18`.

Por CPU, `ALIAS_4K/ALIAS_64K` mediano:

- CPU0 = 0.527012;
- CPU3 = 0.551269;
- CPU4 = 0.530942;
- CPU7 = 0.562633.

A razão conservadora multi-VA `min(ALIAS_4K,ALIAS_64K)/SINGLEVA` permaneceu aproximadamente 1.22 em todas as CPUs: 1.219502, 1.219804, 1.220781 e 1.219933.

## Interpretação permitida

O Stage 7 mostra que a penalidade grande observada com aliases 64 KiB-congruentes é fortemente dependente da geometria/spacing do endereço virtual. Portanto, a interpretação simplista "muitos VAs por si só explicam ~2–2.6x" não é sustentada.

O que os dados suportam neste corte:

- existe um custo multi-VA residual e extremamente estável de aproximadamente 22% no modo menos penalizado (`ALIAS_4K`);
- a configuração 64 KiB-congruente adiciona uma penalidade muito maior;
- o efeito de geometria aparece nos quatro CPUs observados;
- footprint físico adicional (`DISTINCT_64K/ALIAS_64K`) tem efeito mediano menor que a diferença de geometria, embora seja material em parte dos pontos.

## O que NÃO foi demonstrado

Não promover para claim:

- número exato de entradas de TLB;
- associatividade/set count de TLB;
- tamanho exato de cache;
- que bits 12..15 sejam diretamente os bits de índice de uma estrutura específica;
- que o efeito seja TLB puro;
- que cache synonyms, page-walk caches ou outras estruturas indexadas por VA estejam eliminadas.

`CACHE_SYNONYM_CONFOUND=BOUNDED_BY_COLOR_SWEEP_NOT_ELIMINATED`.

## Relação com Stage 6

Stage 6 havia encontrado `ALIAS_64K/SINGLEVA` aproximadamente 2.17–2.66x e rejeitado novamente o candidato de joelho 136→140 como replicação global. Stage 7 resolve uma lacuna causal dessa leitura: ao introduzir `ALIAS_4K`, a penalidade cai para ~1.22x, enquanto `ALIAS_64K` permanece ~2.1–2.59x. Logo, spacing/congruência VA é uma variável dominante no efeito observado.

## Evidência e proveniência

Arquivos canônicos nesta branch:

- `data/evidence/hardware/raf_hw_stage7_va_color_alias_isolation_analysis_20260815.v1.txt`;
- `data/evidence/hardware/raf_hw_stage7_va_color_alias_isolation_receipt_20260815.v1.txt`.

Hashes independentes observados na ingestão dos uploads:

- analysis: `e063bd8e58b7211a03e7e7402fd058516ea111f026827f60f9855e26faf3c954`;
- all: `75e29b345d08d938dc804bf94c527d0dc9021ba9a026bc133b7f00538af17e1a`;
- build: `dd649e9ffc5c80d3cf71ee966f216fdaa68095cc3e0173475c6479f664725ed3`;
- cpu0: `ae388c144fcada4635be8b4dc5157f795291241ab7c87edec7dfdb43b76d22ae`;
- cpu3: `fa35e85948442821647a6e1b6da46eb25ec2bbe6dcdea46db59c084c37523cb2`;
- cpu4: `3442096d4574c688801ddb2a36e2c492ecd0f5c51ebf4098bd219daedda91e5d`;
- cpu7: `a6c4211d1a0ea369ad4dd9d49f43bddc647a01586067ffba8fec5b2ff1298b54`;
- disassembly: `09f25b9bc5cf9e74153b0a015f8989bfef3731785f9e48134f1505f40ee49b0f`;
- receipt upload: `705505f553864c2a95aea3cb01cb6d9bdc27316f209e334b4720d5d0fe76a798`.

Os hashes de source/binary/analyzer presentes no receipt permanecem `RECEIPT_DECLARED` nesta ingestão porque os três arquivos exatos não foram re-hasheados aqui.

## F_ok / F_gap / F_next

- **F_ok:** geometria VA identificada como variável causal material; execução com forte cobertura e matching de frequência.
- **F_gap:** identidade da estrutura microarquitetural responsável permanece aberta.
- **F_next:** Stage 8 deve mapear `latency(stride)` em 4K, 8K, 16K, 32K, 64K, 128K, 256K, preservando mesma página física, CPU e frequência, para procurar periodicidades sem promover topologia exata por inferência.
