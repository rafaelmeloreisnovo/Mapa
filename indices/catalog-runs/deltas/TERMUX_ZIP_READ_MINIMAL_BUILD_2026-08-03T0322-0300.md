# Termux RAFCODEΦ — leitura do ZIP e build mínimo

Estado: `PASS_LOCAL_LIMITED / claim_allowed=false`

## Fonte

- ZIP: `termux-app-rafacodephi-master (4).zip`
- SHA-256: `c2549ba985b804dcda3a75261f97a28972aa1ededc873883156cb2e0f3cf05b5`
- Entradas observadas: `2461`
- Markdown/TXT observados: `347`

## Resultado material

```text
./build_termux.sh
→ clang
→ bootstrap_rafaelia/raf_selftest
→ ok=21 fail=0
```

Binário local de referência:

```text
SHA-256 55cb3e65ca794b81292364fe50215882141a7f0cbd436da7df8ceabfedb5beac
```

## Mudanças no repositório

| Repositório | Caminho | Commit | Papel |
|---|---|---|---|
| `rafaelmeloreisnovo/termux-app-rafacodephi` | `scripts/build_minimal_selftest.sh` | `b5d885c04f6c2ad8c927579482d8cb72b170df9e` | compilação mínima sem Gradle/Java/Python/Make/rede |
| `rafaelmeloreisnovo/termux-app-rafacodephi` | `docs/MINIMAL_SELFTEST_BUILD.md` | `2c397133331e479ad094c5171c2657fa01930044` | rota humana/IA, limites e próximo gate |

## Relações

```text
memória e documentação
→ contrato bootstrap
→ núcleo C bootstrap_rafaelia
→ build mínimo
→ self-test
→ receipt
→ próximo gate ARM físico
```

## Fronteira epistemológica

- `PROVADO`: ZIP, commits e self-test local.
- `EVIDENCIADO`: existe um núcleo C de baixa dependência coerente.
- `REFUTADO`: host self-test não prova APK, Android, ARM ou backend apt/dpkg.
- `TOKEN_VAZIO`: ARM32, ARM64, APK, instalação, pkg real, CI e replicação.

## Receipt

[`RAFAELIA_TERMUX_ZIP_READING_AND_MINIMAL_BUILD_2026-08-03T0322-0300.json`](../../../data/catalog_runs/RAFAELIA_TERMUX_ZIP_READING_AND_MINIMAL_BUILD_2026-08-03T0322-0300.json)
