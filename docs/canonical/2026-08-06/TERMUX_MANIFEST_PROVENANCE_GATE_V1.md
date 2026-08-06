# Termux Manifest Provenance Gate — V1

```text
event_id=TERMUX-MANIFEST-PROVENANCE-GATE-20260806-V1
claim_allowed=false
release_allowed=false
append_only=true
```

## Síntese

A arquitetura deixou de possuir um único rótulo ambíguo para `termux-packages`.
Agora existem duas autoridades declaradas:

| Autoridade | Função | Estado |
|---|---|---|
| `termux/termux-packages@eb124b51...` | referência produtiva pinada | preservada |
| `rafaelmeloreisnovo/termux-packages` | construtor experimental RAFCODE-Φ | draft, não promovido |

O fork materializou compilação e payload de host, e o PR #4 acrescenta manifesto fail-closed. O `termux-app-rafacodephi` PR #331 registra essa evolução sem apagar o momento em que o fork estava vazio.

## Delta executável

### `termux-packages` PR #4

- carrega o manifesto antes do build;
- valida magic, versão, layout, bounds e strings;
- corrige `string_pool_offset`;
- reserva offset zero para ausência;
- rejeita truncamento silencioso de dependências;
- preserva falha real de `configure`;
- exige fonte materializada e payload não vazio;
- tipa patches, resume e pós-processamento ausentes como `TOKEN_VAZIO`.

### `termux-app-rafacodephi` PR #331

- mantém upstream como referência produtiva;
- registra o fork como `ACTIVE_EXPERIMENTAL_BUILDER`;
- fixa commits e PRs exatos;
- conserva `NDK_NOT_FOUND`;
- proíbe promoção sem duas ABIs, scan de prefixo e receipts físicos.

### RLL

O receipt existente preserva:

```text
924 testes PASS
7/7 workflows success
claim_allowed=false
next_gate=RLL-P0-TERMUX-PHYSICAL-REPLAY
```

Logo, a integração de software é evidência útil, mas não substitui replay físico.

## Sete direções

1. **Fato:** os dois PRs draft existem e contêm os gates.
2. **Lacuna:** NDK, fonte por hash, patches, fechamento de dependências e dispositivos.
3. **Invariante:** nenhuma promoção sem origem e receipt físico.
4. **Variante:** promover por pacote/ABI ou criar manifesto V2.
5. **Prova:** build, scan, instalação, execução e rollback.
6. **Parábola:** a estrada pública permanece aberta; a ponte experimental só recebe tráfego após testar os pilares nas duas margens.
7. **Retroalimentação:** fechar toolchain → ABIs → formato → dispositivo.

## Ordem de execução

```text
NDK 26.3.11579264 PASS
→ fonte + SHA-256
→ ARMv7
→ AArch64
→ scan de prefixo
→ decisão TAR/.deb
→ assinatura
→ instalação
→ execução
→ rollback
→ receipt
```

## TOKEN_VAZIO ativos

- `TOKEN_VAZIO_TOOLCHAIN_RECEIPT`
- `TOKEN_VAZIO_SOURCE_FETCH`
- `TOKEN_VAZIO_PATCH_EXECUTION`
- `TOKEN_VAZIO_MANIFEST_V2_REQUIRED`
- `TOKEN_VAZIO_DEPENDENCY_CLOSURE`
- `TOKEN_VAZIO_DEB_APT_DPKG_CONTRACT`
- `TOKEN_VAZIO_ARMV7_DEVICE_RECEIPT`
- `TOKEN_VAZIO_AARCH64_DEVICE_RECEIPT`
- `TOKEN_VAZIO_INSTALL_EXEC_ROLLBACK_RECEIPT`
- `TOKEN_VAZIO_RLL_TERMUX_PHYSICAL_REPLAY`

## R3

- **F_ok:** execução e custódia agora apontam para objetos reais e separados.
- **F_gap:** material Android e distribuição ainda não atravessaram todos os gates.
- **F_next:** produzir o primeiro receipt completo ARMv7/AArch64 e somente então decidir promoção.
