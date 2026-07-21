# Escopo Ativo CI/CD — RAFAELIA Ecosystem

**Atualizado:** 2026-07-21  
**Gap:** M1 — KOS cataloga 28 repositórios; apenas 6 têm CI ativo

---

## Repositórios com CI Ativo (6/28)

Estes repositórios têm workflows GitHub Actions ativos, PRs monitorados e código
diretamente integrado ao ecossistema de gaps-audit:

| # | Repositório | Domínio | CI | PRs Ativos |
|---|-------------|---------|----|----|
| 1 | `rafaelmeloreisnovo/Vectras-VM-Android` | Plataforma/VM/Android | ✅ | ✅ |
| 2 | `rafaelmeloreisnovo/qemu_rafaelia` | QEMU/Emulação | ✅ | ✅ |
| 3 | `rafaelmeloreisnovo/termux-app-rafacodephi` | Terminal/Bootstrap | ✅ | ✅ |
| 4 | `rafaelmeloreisnovo/RafGitTools` | GitHub Client/Android | ✅ | ✅ |
| 5 | `rafaelmeloreisnovo/androidx_RmR` | AndroidX fork (rmr/) | ✅ | ✅ |
| 6 | `rafaelmeloreisnovo/Mapa` | KOS/Documentação | ✅ | ✅ |

---

## Repositórios Catalogados fora do Escopo CI Ativo (22/28)

Estes repositórios estão documentados no KOS (`biblioteconomia/03_CATALOGO_REPOSITORIOS.md`)
mas não têm CI automático integrado nesta sessão de desenvolvimento:

| Repositório | Domínio | Status KOS |
|-------------|---------|-----------|
| `rafaelmeloreisnovo/ChipQuantum` | Criptografia/Hashing | ATV (FATO) |
| `rafaelmeloreisnovo/DeepSeek-RafCoder` | Runtime/NDK | ATV (FATO) |
| `rafaelmeloreisnovo/GAIA_phi` | Determinismo/Custódia | ATV (FATO) |
| `rafaelmeloreisnovo/BLAKE3` | Hashing/Fork | CAN (FATO) |
| `rafaelmeloreisnovo/RafPolimata` | Cognição/Classificação | ATV |
| `rafaelmeloreisnovo/MemRafcode` | Memória/Dados | ATV |
| `rafaelmeloreisnovo/home` | Hub pessoal | ATV |
| `rafaelmeloreisnovo/Manifesto-publico` | Publicação/Espiritual | ATV |
| `rafaelmeloreisnovo/papers` | Pesquisa/Dados | ATV |
| `rafaelmeloreisnovo/rafaelia` | Repositório raiz | CAN |
| `rafaelmeloreisnovo/UserLAnd` | Userspace Linux | ATV |
| `rafaelmeloreisnovo/Magisk_Rafaelia` | Root/Kernel | ATV |
| `rafaelmeloreisnovo/llamaRafaelia` | IA/LLM | ATV |
| `rafaelmeloreisnovo/Rafaelia_Private` | Extensões privadas | PRIV |
| `rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE` | Dados/Corpus | PRIV |
| `rafaelmeloreisnovo/rafaelia-arm32` | ARM32/NDK | ATV |
| `rafaelmeloreisnovo/engine-rmr` | Motor/Runtime | ATV |
| `rafaelmeloreisnovo/CODEX_RAFAELIA` | Documentação | ATV |
| `rafaelmeloreisnovo/instituto-rafaelia` | Organização | ATV |
| `rafaelmeloreisnovo/rafaelia-docs` | Documentação pública | ATV |
| `rafaelmeloreisnovo/rafaelia-core` | Core biblioteca | ATV |
| *(outros repos privados/espirituais)* | Diverso | PRIV |

> **Nota:** A lista acima é reconstituída do KOS e pode não ser exaustiva.
> O `03_CATALOGO_REPOSITORIOS.md` é a fonte canônica para fichas completas.

---

## Por que apenas 6?

A sessão atual de desenvolvimento (gaps-audit) opera com acesso concedido a:

- 6 repositórios via GitHub App instalado em `rafaelmeloreisnovo`
- CI configurado via `claude/vectra-vm-gaps-audit-pvtiki` em cada um

Os 22 repos restantes podem ser adicionados ao escopo quando necessário via
`add_repo` — mas não têm gaps ativos mapeados neste ciclo.

---

## Relação com o CI M4

O step `M4 — Internal repo link verification` em `.github/workflows/ci.yml`
já conhece o escopo de 6 repos e reporta referências fora do escopo como `INFO`
(não-bloqueante). Este documento complementa esse step com documentação humana.

---

## Próxima Ação (M1)

- [ ] **Rafael:** confirmar se os 22 repos listados acima são completos e corretos
- [ ] Atualizar esta lista quando novos repos forem adicionados ao escopo CI
- [ ] Considerar criar ficha KOS para repos que ainda não têm (`engine-rmr`, `instituto-rafaelia`, etc.)
