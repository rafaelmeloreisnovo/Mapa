# NOVOexport — Memória longitudinal `000 → 002`

- **Modo:** `INCREMENTAL_APPEND_ONLY_FAIL_CLOSED`
- **Claim permitido:** `false`
- **Privacidade:** agregado público seguro; localizadores privados retidos
- **Cobertura fechada:** `3/51` lotes de conversas
- **Próximo cursor:** `conversations-003.json`

## F_ok

A cadeia privada fechada agora é:

```text
conversations-000
  → conversations-001
  → conversations-002
  → conversations-003 [PENDING_CATALOG]
```

Foram reconciliados:

| Medida cumulativa | Valor |
|---|---:|
| Conversas | 300 |
| IDs únicos de conversa | 300 |
| IDs únicos de mensagem | 20.059 |
| Ocorrências de nós | 20.359 |
| IDs únicos de nós | 20.175 |
| Lotes pendentes | 48 |

Os lotes `001` e `002` possuem duas formas privadas:

1. índice compatível com o contrato legado;
2. índice de custódia anonimizado, sem títulos ou corpos crus.

O lote `000` mantém, neste estado, somente o índice legado. Sua forma de custódia anonimizada permanece `TOKEN_VAZIO`.

Os **cinco pacotes de índice/custódia** materializados e as **duas reconciliações adjacentes** passaram por recuperação no Drive, decodificação Base64, SHA-256 e comparação byte a byte. Total: **7 envelopes privados verificados**.

## Correção append-only

Uma contagem anterior registrava incorretamente seis pacotes de índice/custódia. Ela incluía implicitamente um pacote anonimizado do lote `000` que não foi materializado. A contagem foi corrigida antes do merge, sem apagar o evento privado histórico:

- índices/custódia materializados: `5`;
- reconciliações materializadas: `2`;
- envelopes privados totais: `7`;
- custódia anonimizada do lote `000`: `TOKEN_VAZIO`.

## Limites entre lotes

### `000 ↔ 001`

- conversa sobreposta: `0`;
- mensagem sobreposta: `0`;
- nó sobreposto: `1`, classificado como sentinela nula sem mensagem;
- hash de título sobreposto: `0`;
- hash estrutural sobreposto: `0`;
- hashes de conteúdo recorrentes: `46`;
- intervalo temporal: `131,602216 s`.

### `001 ↔ 002`

- conversa sobreposta: `0`;
- mensagem sobreposta: `0`;
- nó sobreposto: `1`, classificado como sentinela nula sem mensagem;
- hash de título sobreposto: `1`;
- hash estrutural sobreposto: `0`;
- hashes de conteúdo recorrentes: `39`;
- intervalo temporal: `274,34068 s`.

Recorrência de hash é sinal estrutural. Não foi promovida a equivalência semântica.

## Privacidade

Este delta não contém:

- IDs de arquivos do Google Drive;
- títulos de conversas;
- corpos de mensagens;
- nomes de assets;
- URLs ou localizadores privados.

Os hashes de origem são usados somente como fingerprints de custódia.

## F_gap

- a custódia anonimizada do lote `000` ainda não foi materializada;
- `48` lotes de conversa ainda não foram fechados;
- `21` lotes Codex permanecem sem ingestão;
- manifest de assets, `img/` e `chat.html` ainda não foram reconciliados;
- sem classificação semântica dos hashes recorrentes;
- CI com passos observáveis e receipt físico ARM continuam `TOKEN_VAZIO`.

## F_next

1. Catalogar `conversations-003.json` privadamente.
2. Gerar os dois índices e testar a recuperação.
3. Reconciliar `002 ↔ 003`.
4. Opcionalmente materializar a custódia anonimizada do lote `000` em delta separado e verificável.
5. Publicar somente o agregado sanitizado sucessor.

## Autoridade

Registro estruturado:

`data/catalog_runs/RAFAELIA_NOVOEXPORT_MEMORY_000_002_2026-08-04.json`
