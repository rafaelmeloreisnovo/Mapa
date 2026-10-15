# Dispositivo RAFAELIA — rota de reconstrução BITRAF8000 → W20 → ARM32

**Status:** `ROUTE_SOURCE_BOUND / NÃO PROMOVER` · 2026-10-14 · `claim_allowed=false`.

Este documento é um **roteador**, não é o núcleo do dispositivo. O contrato navegável está em `data/devices/mobile_bitraf_w20_reconstruction_route.v1.json`. Autoridade de implementação: **RafPolimata**. Autoridade dos dados privados e anterioridade: **Google Drive**.

## Entrada em até três leituras

1. **Drive START HERE V2.2 / HOTSTATE V4.5:** `MOBILE BITRAF RECONSTRUCTION`. O Realme Note 50 foi declarado destruído/indisponível; não presumir extração, firmware, execução física ou recuperação de seus bytes.
2. **Drive documento autoral W20:** “Icosfera f=2 × Fibonacci × Palavra 20-bit × Paridade Dual — V1”; preserva `A10 | V8 | pA | pV`, `K64`, `f=2,42/120/80`, os recibos históricos e suas limitações.
3. **RafPolimata fontes exatas:** `rafaelia/bitraf_matrix.h`, `docs/BITRAF_MATRIX_8000_4096_V1.md` e [PR #436](https://github.com/rafaelmeloreisnovo/RafPolimata/pull/436) (DRAFT).

## O que é montagem comprovável no software

```text
SOURCE_PRIVATE_W20_SPEC (Drive, não replicar)
      |           BITRAF_MATRIX8000 (RafPolimata, fonte C)
      |                     |
      +-- candidate design ---+
                    |
    S=(x,y,z,vertex2,phase1), subvalue5
                    |
         W20=(A10|V8|pA|pV)
                    |
      2xW20 → exactly 5 bytes
                    |
    ARMv7 freestanding object (CI)
                    |
          [HOST ADAPTER]      TOKEN_VAZIO
                    |
          [APK EMBEDDED]      TOKEN_VAZIO
                    |
          [DEVICE ARM32]      TOKEN_VAZIO
                    |
          [RECEIPT]           TOKEN_VAZIO
```

`MATRIX8000=CORE4096+SHELL3904`; `W20=8000×32=256000` ao incluir subvalor de 5 bits. São **espaços de tipos distintos**. Paridade `pV` não é `phase`; igualdade de contagens não é identidade de circuito ou dispositivo. Paridades duplas detectam erros isolados, mas duas inversões no mesmo campo podem não ser detectadas. Não chamar recuperação de 56% de perdas, corrigir pixels ocultos ou ECC sem decodificador validado.

## Os sete filtros antes de fechamento

| Rota | Falsificador mínimo | Evidência atual |
| --- | --- | --- |
| D1 identidade | commit, código e executável divergem | SHA de PR/CI |
| D2 semântica | alias Unicode/bit `phase` confundido com `pV` | contrato tipado; ratificação pendente |
| D3 privacidade | conteúdo/ID privado em diff público | no raw no Mapa |
| D4 tempo | snapshot de provedor vencido usado como atual | gate separado / `TOKEN_VAZIO` |
| D5 falsificação | inversão falha ou bit simples não detectado | exaustão C sob CI |
| D6 governo | PR mesclada sem regras de servidor | `HOLD` até proteção real |
| D7 aparelho | compilar ARM object equivale a instalar APK | `TOKEN_VAZIO_PHYSICAL` |

**Entrada mínima humana/IA:** `START HERE → HOTSTATE → this route → PR#436 exact HEAD → evidence → μWRITE`. Versões históricas continuam acessíveis, nenhuma cópia privada para GitHub. Cada passo requer recibo explícito; construir um novo dispositivo físico, elétrico ou microeletrônico exigirá esquemático, alimentação, interfaces, tolerâncias, medições e prova de segurança que **não estão demonstrados neste artefato**.

**R3:** `F_ok` = fontes reais ligadas por rota tipada + experimento independente; `F_gap` = contato físico, protocolo APK, código de correção, circuito e proveniência por aparelho; `F_next` = decidir perfil binário, validar serialização e falsificadores, capturar artefato ARMv7, ligar adaptador Android somente após decisão de autoridade; `rollback` = fechar PR de rota e a PR produtora sem apagar arquivos anteriores.
