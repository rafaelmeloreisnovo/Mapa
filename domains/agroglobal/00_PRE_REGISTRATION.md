# AGROGLOBAL Ω — pré-registro da cadeia de custódia

Registro inicial: 2026-10-09 (America/Sao_Paulo); confirmação temporal autoritativa = GitHub commit timestamp e provedores.
Escopo autorizado: atlas documental agrícola (Brasil e mundo), câmbio USD/EUR/GBP/CNY/BRL, commodities, sacas, produtividade, safras, certificações, logística, riscos e consórcios biológicos.
Autoridade: Mapa = roteamento/ontologia/evidência federada; NOVOexport no Drive = memória documental/recibos; alphaXiv = biblioteca de papers, não commits Git.
Política: SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM; TOKEN_VAZIO != 0; IMPLEMENTED_UNTESTED != PASS; direitos/licenças antes de redistribuir.

## Ordem obrigatória de cada delta
1. PRE-RECORD: evento, timestamp observado, fonte anterior, escopo, autorizações e idempotency_key.
2. ACT: operação mínima reversível; preservar entrada bruta e converter somente em derivado identificado.
3. OBSERVE: readback do provedor, commit completo, arquivo/blob SHA Git, metadata e relógio com origem.
4. HASH: SHA-256 dos bytes exatos (UTF-8 ou binário), além de Git SHA-1 do blob/commit; usar SHA-512 apenas quando houver necessidade e bytes disponíveis.
5. RECEIPT: append-only (event_id, parent_event_hash, repo/branch/commit, drive_file_id, alpha_folder_id, evidências, lacunas e rollback).
6. INDEX: atualizar rota sem substituir o histórico.

## Fronteiras probatórias
- Registro criado != atestação independente; timestamp de autor != carimbo temporal confiável por terceiro.
- Metadado do Drive não comprova SHA-256 de bytes se download/readback não for executado.
- Contrato futuro internacional != preço no balcão/porto; câmbio spot != PTAX; projeção != colheita observada.
- Três superfícies não suportam transação distribuída atômica: registrar sucessores e operações incompletas, sem apagar rastros.

GATE_INICIAL=PRE_REGISTERED | DATASET_VALIDATED=FALSE | CI=NOT_RUN | CLAIM_ALLOWED=FALSE.
ROLLBACK=fechar PR/abandonar branch sem mutar main, mantendo ledger e recibos históricos.
