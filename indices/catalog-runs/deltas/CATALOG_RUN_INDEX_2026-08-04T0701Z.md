# RAFAELIA — Catálogo incremental — 2026-08-04T0701Z

Estado: `APPEND_ONLY / CLAIM_ALLOWED=false`

## Checkpoint

- anterior: `Mapa@8fe7b63fd766785a8560f8c052c6ea235059a1fd`
- receipt: `data/catalog_runs/RAFAELIA_CATALOG_CYCLE_2026-08-04T0701Z.json`
- referência: Google Drive `1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88`

## Delta navegável

`NOVOexport` — Drive `1P7hJq5R4fgYGEQIVNgRvllAad2lGxWEv`

```text
NOVOexport/
├── chat.html                     [EVIDENCIADO; conteúdo/hash TOKEN_VAZIO]
└── img/
    ├── file_00000000a0a4720e95d5006333f6f1b2.dat
    ├── file_000000000e9071f5a5da8d9ca4ce458f.dat
    ├── file_000000000a9071f59cf18fb09618b54f.dat
    ├── file_000000000ad471f5a9cb4ef49f9ea03e.dat
    └── file_000000000a70720eb64e8dab3e3a2182.dat
```

Os cinco objetos `.dat` existem (`PROVADO`), mas tipo de mídia, conteúdo, integridade e relação com o HTML permanecem `TOKEN_VAZIO`.

## Rotas por pergunta

- **Onde está o export bruto?** `NOVOexport` no Drive.
- **Onde está a superfície textual?** `chat.html`, Drive `1NwPpd_CYpwjrb7qOn8Pqw-d_b4Qmut1D`.
- **Onde estão anexos candidatos?** pasta `img`, Drive `1BYq9jv5hci2rigfvD2qVkhcPH1-ZKmnQ`.
- **Há hashes de conteúdo?** Não; `TOKEN_VAZIO_EXPORT_HASH`.
- **Há métricas de conversas/interações/datas?** Não; exige parsing verificável do HTML.
- **Pode ser publicado ou usado como dataset?** Ainda não; faltam privacidade, licença, proveniência byte a byte e deduplicação.

## Classificação

- `PROVADO`: hierarquia e IDs dos objetos.
- `EVIDENCIADO`: estrutura compatível com export bruto contendo HTML e anexos.
- `HIPÓTESE`: material pode alimentar corpus navegável após validação.
- `REFUTADO`: presença de pasta ou extensão prova semântica, completude ou integridade.
- `TOKEN_VAZIO`: bytes, MIME, hashes, métricas, privacidade, licença e referências internas.

## Próximo gate verificável

```text
exportar bytes sem transformação
→ SHA-256 por objeto
→ identificar MIME por magic bytes
→ analisar chat.html
→ reconciliar referências de anexos
→ contar conversas, interações e intervalo temporal
→ deduplicar por hash preservando provider_id
→ emitir receipt sucessor
```

Nenhuma escrita foi feita no Drive e nenhum conteúdo bruto foi copiado para o GitHub.