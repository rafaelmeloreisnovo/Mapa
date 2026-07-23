# Índice cruzado — Neurociência e Homeostase Operacional

**Data lógica:** 2026-07-22  
**Estado:** `CROSS_REPOSITORY_INDEX_DRAFT`  
**Gate:** revisão humana antes de merge.

## 1. Núcleo científico

### GitHub

- Repositório: [`rafaelmeloreisnovo/papers`](https://github.com/rafaelmeloreisnovo/papers)
- Branch: `docs/neurociencia-recorrencia-20260722`
- Draft PR: [`papers #19`](https://github.com/rafaelmeloreisnovo/papers/pull/19)
- Head registrado: `bcd6676aeacd082c199f53344b09d6224ed1f630`

Artefatos:

| Caminho | Função | Estado |
|---|---|---|
| `docs/neurociencia/RECORRENCIA_PLASTICIDADE_ELETROFISIOLOGIA.md` | Síntese científica defensável, hipóteses, falsificadores e bibliografia | `DRAFT_DEFENSAVEL` |
| `docs/neurociencia/RECORRENCIA_PLASTICIDADE_CLAIMS.json` | Ledger atômico de claims e lacunas | `claim_allowed=false` |
| `README.md` | Navegação e limite de autoridade | `INDEXED_IN_BRANCH` |

Commits de origem:

```text
paper      ddd0575fee071fcbda55cd09e5cadf906bd851fe
claims     c450ff3efbc7ca05a4d4fd061072328c6679ef2f
indexação  bcd6676aeacd082c199f53344b09d6224ed1f630
```

SHA-256 das fontes locais que originaram os artefatos:

```text
paper     a13b802b313e54f8d24ca90cc1eb846ccb2b60e91fd02d649d687b9a24a0b490
claims    56fcbb4bd1de910bd994df5cfb5b22452aaababa2fca2df2b6b5ad2fc0a179ab
```

## 2. Núcleo de governança

### GitHub

- Repositório: [`rafaelmeloreisnovo/Mapa`](https://github.com/rafaelmeloreisnovo/Mapa)
- Branch: `protocol/homeostase-operacional-20260722`
- Draft PR: [`Mapa #41`](https://github.com/rafaelmeloreisnovo/Mapa/pull/41)
- Commit do protocolo: `c3488939c7ddc27ba45bff8487683e3cfd76d5fa`

Artefatos:

| Caminho | Função | Estado |
|---|---|---|
| `protocolos/HOMEOSTASE_OPERACIONAL_MELHORIA_CONTINUA.md` | Régua de melhoria contínua em rede, risco, baseline e rollback | `NORMATIVE_METAMODEL_DRAFT` |
| `indices/NEUROCIENCIA_HOMEOSTASE_OPERACIONAL.md` | Este índice de ligação | `CROSS_REPOSITORY_INDEX_DRAFT` |

SHA-256 da fonte local do protocolo:

```text
1ccc6c8a09d47db3414a162e4a688a8939fdc92880e002f05d8528adf0c78589
```

O SHA do commit que contém este índice é deliberadamente lido no histórico Git, e não gravado no próprio arquivo, evitando autorreferência impossível.

## 3. Cópias editoriais no Google Drive

Pasta canônica:

- [`RAFAELIA/Papers — Neurociência e Homeostase Operacional`](https://drive.google.com/drive/folders/1n74otSJEGsmI9I2W7-hg2mYec6d-6Sl5)

Documentos:

1. [`Recorrência, Plasticidade, Eletrofisiologia e Regulação Cardiorrespiratória — DRAFT DEFENSÁVEL`](https://docs.google.com/document/d/1TnvOiODLlZBBipyLKRaDaLFvveBzvu_IXbzNEaf9DSs)
2. [`Protocolo de Homeostase Operacional e Melhoria Contínua — NORMATIVE METAMODEL DRAFT`](https://docs.google.com/document/d/1niFaWjcyE_3PbUdrnd0SFM16LbWJelrgUJybwUuZvFw)
3. [`Manifesto de Proveniência GitHub ↔ Drive`](https://docs.google.com/document/d/15GwDmvm89wcGEOoSa5lwzIIZ_vuGi2m3vhximFrTsPE)

## 4. Autoridade e limites

```text
Git = autoridade de versão, autoria, diff e histórico
Drive = autoridade de leitura, revisão e memória editorial
literatura externa ≠ evidência local
commit ≠ execução
hipótese ≠ resultado
metáfora ≠ mecanismo
TOKEN_VAZIO ≠ zero
```

Nenhum artefato declara:

- certificação ISO;
- diagnóstico ou recomendação clínica;
- resultado experimental local;
- causalidade eletromagnética semântica;
- validação por pares concluída;
- merge autorizado.

## 5. Referenciais de processo

O protocolo usa, sem alegar certificação:

- ISO 9001:2015 e registra a edição futura separadamente;
- ISO 31000:2018;
- ISO/IEC 17025:2017;
- ISO 8000-61:2016;
- princípios FAIR;
- NIST AI RMF 1.0.

A regra de promoção é:

\[
\text{melhoria válida}
=
\text{baseline preservado}
\cap
\text{delta explícito}
\cap
\text{prova}
\cap
\text{risco tratado}
\cap
\text{rollback}
\cap
\text{rastreabilidade}
\]

## 6. Próximos gates

1. revisar referências e linguagem com especialista em neurofisiologia;
2. validar links e arquivos nos dois PRs;
3. manter ambos em draft até revisão humana;
4. criar pré-registro e análise de potência apenas se houver estudo local;
5. registrar correções como novos commits, sem reescrever a origem;
6. preservar dados negativos e `TOKEN_VAZIO`.

### R₃

- **F_ok:** GitHub e Drive estão ligados por artefato, branch, commit, PR e manifesto.
- **F_gap:** revisão especializada, execução experimental e replicação continuam ausentes.
- **F_next:** revisar os dois drafts e decidir separadamente sobre cada merge.
