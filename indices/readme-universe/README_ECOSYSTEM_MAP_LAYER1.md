# RAFAELIA — README Ecosystem Map — Layer 1

**Estado:** `CANONICAL_DRAFT`
**Escopo:** leitura direta dos READMEs; sem inspeção estrutural completa da árvore de arquivos.
**Política:** append/versionado; fontes preservadas; `claim_allowed=false`.

## Objetivo

Construir uma visão navegável do ecossistema a partir dos READMEs reais de cada repositório. Cada nó registra o significado declarado, autoridade, fronteiras, relações e lacunas. Esta camada precede a análise da árvore de arquivos.

## Invariantes

```text
README ≠ prova de execução
README ≠ árvore completa do repositório
roadmap ≠ implementação
commit ≠ runtime PASS
nome do repositório ≠ função comprovada
```

## Tipos de README

- `README_ROOT`: porta principal do repositório.
- `README_SUBSYSTEM`: entrada de um subsistema.
- `README_EVIDENCE`: descreve receipts, provas ou resultados.
- `README_OPERATIONAL`: comandos, build, execução e manutenção.
- `README_REFERENCE`: pesquisa, conceito ou documentação auxiliar.
- `README_ARCHIVE`: histórico, legado ou material congelado.

## Nós lidos — Lote 001

### rafaelmeloreisnovo/Mapa

- README: `README.md`
- ref observado: `57781f253ec2f529737aa798d27af1d4c27f109f`
- papel declarado: plano federado de controle, organização do conhecimento, autoridade, proveniência e roteamento entre repositórios.
- autoridade: catálogo, governança, índices, relações, estado epistemológico.
- fronteira: não substitui a verdade técnica do repositório produtor.
- relações declaradas: controla/roteia `RafGitTools`, `termux-app-rafacodephi`, `RafPolimata`, `llamaRafaelia`, `relativity-living-light`, `papers`, `Vectras-VM-Android` e `qemu_rafaelia`.
- estado: `KNOWS_README_DIRECT`.

### rafaelmeloreisnovo/RafGitTools

- README: `README.md`
- papel declarado: cliente Android unificado para Git/GitHub e múltiplos provedores, com JGit, sincronização offline, autenticação, UI Android e JNI.
- autoridade: roteamento operacional e operações Git móveis.
- fronteiras declaradas: componentes `implemented`, `partial`, `planned` e `experimental` não são equivalentes.
- estado: `KNOWS_README_DIRECT`.

### rafaelmeloreisnovo/RafPolimata

- README: `README.md`
- blob observado: `0b5b0a3a16979a29485972fc88d7474ecbfe8c9f`
- papel declarado: arquitetura semântica, matemática, tecnológica e jurídica para baixo nível, Android, ARM32/ARM64, APK/DEX/ELF, criptografia, memória e governança de evidência.
- autoridade: produção de evidência, contratos de compilação e estados runtime.
- invariante declarada: `conceito ≠ implementação ≠ execução ≠ evidência ≠ validação runtime`.
- taxonomia interna de READMEs: `CANONICAL`, `ACTIVE`, `EVIDENCE`, `REFERENCE`.
- estado: `KNOWS_README_DIRECT`.

## Mapa inicial de responsabilidades

```text
Mapa                 --CONTROLS/INDEXES--> ecossistema
RafGitTools           --ROUTES/OPERATES--> Git e provedores
RafPolimata           --PRODUCES_EVIDENCE--> compilação/runtime/contracts
termux-app            --EXECUTES_LOCAL--> Android/Termux
RLL + papers          --VALIDATES/PUBLISHES--> ciência/editorial
Vectras + qemu        --VIRTUALIZES--> runtime/VM
llamaRafaelia         --INTERPRETS--> memória/modelos
```

## Cobertura

```yaml
repositories_accessible_observed: ">60"
root_readmes_read_directly: 3
internal_readmes_discovered: ">100 candidates"
file_tree_analysis_started: false
claim_allowed: false
```

## Próxima fila de leitura

1. `instituto-Rafael/relativity-living-light`
2. `rafaelmeloreisnovo/papers`
3. `rafaelmeloreisnovo/termux-app-rafacodephi`
4. `rafaelmeloreisnovo/Vectras-VM-Android`
5. `rafaelmeloreisnovo/qemu_rafaelia`
6. `rafaelmeloreisnovo/Rafaelia_Private`
7. `rafaelmeloreisnovo/X0`
8. `rafaelmeloreisnovo/CientiEspiritual`
9. `rafaelmeloreisnovo/Cosmos`
10. `rafaelmeloreisnovo/GAIA_phi`
11. `rafaelmeloreisnovo/llamaRafaelia`
12. `rafaelmeloreisnovo/ZIPRAF_CORE`
13. `rafaelmeloreisnovo/ZIPRAF_OMEGA_FULL`
14. `rafaelmeloreisnovo/MemRafcode`
15. `rafaelmeloreisnovo/Semente`
16. `rafaelmeloreisnovo/templo-vivo-arcs`

## F_next

Ler cada README diretamente, registrar seu blob/ref, produzir nó machine-readable e tipar relações. Não descer para a árvore de arquivos até autorização da camada seguinte.
