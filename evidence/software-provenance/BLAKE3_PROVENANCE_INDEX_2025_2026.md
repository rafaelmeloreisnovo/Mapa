# Índice federado — BLAKE3 / Rafael Melo Reis / 2025–2026

## Autoridade canônica

A documentação técnica detalhada permanece no repositório especializado:

- repositório: `rafaelmeloreisnovo/BLAKE3`
- branch de auditoria: `agent/armv7-upstream-benchmark-20260726`
- PR de auditoria: `#104`
- cronologia geral: `audit/forensics/BLAKE3_AUTHORSHIP_CHRONOLOGY_2025_2026.md`
- ledger geral: `audit/forensics/BLAKE3_CLAIMS_LEDGER_2025_2026.yaml`
- passe documental 01: `audit/forensics/BLAKE3_DOCUMENTARY_TIMELINE_PASS_01_20260726.md`
- eventos legíveis por máquina: `audit/forensics/BLAKE3_DOCUMENTARY_EVENTS_PASS_01_20260726.yaml`

O Mapa atua como índice federado, não como cópia concorrente do dossiê.

## Escopo indexado

```yaml
entity: BLAKE3_RMR_FORK
canonical_repository: rafaelmeloreisnovo/BLAKE3
upstream_repository: BLAKE3-team/BLAKE3
author: Rafael Melo Reis
period: 2025-02_to_2026-07
latest_documentary_pass: 2026-07-26_PASS_01
```

## Marcos

| Período/data | Evento | Estado |
|---|---|---|
| fev.–abr. 2025 | fork/trabalho anterior declarado pelo autor | `DECLARED_BY_AUTHOR`, artefato `TOKEN_VAZIO` |
| mar.–abr. 2025 | atividade técnica pública do autor em outros repositórios | `VERIFIED_PRIMARY`, não prova BLAKE3 |
| 25 nov. 2025 00:42:22Z | abertura da PR upstream `#533` | `VERIFIED_PRIMARY` |
| 25 nov. 2025 00:47:16Z | três comentários recuperados do Copilot | `VERIFIED_PRIMARY_IN_RETRIEVED_TIMELINE` |
| 25 nov. 2025 03:29:05Z | PR #533 fechada sem merge | `VERIFIED_PRIMARY`, snapshot `mergeable=true` |
| 9 dez. 2025 | correção upstream AVX-512/Cygwin | sobreposição temática, causalidade `TOKEN_VAZIO` |
| 8 jan. 2026 | release 1.8.3 cita correções C/CMake | sobreposição temática |
| jan.–jul. 2026 | PRs upstream sobre símbolos, CMake, warnings, LTO e TBB | `VERIFIED_PRIMARY`, não identidade direta de patch |
| 26 jul. 2026 | fork NEON × fork portátil em ARMv7 | `PASS`, ganho mediano observado `23,53%` |
| 26 jul. 2026 | fork × upstream ARMv7 pré-estrito | upstream à frente; fork `-8,77%` |
| pendente | comparação ARMv7 estrita com warnings/linker/símbolos | `TOKEN_VAZIO` |
| pendente | recuperação do fork fev.–abr. 2025 | `P0` |
| pendente | comparação AST/CFG/git-blame | `P1` |

## Resultado do passe documental 01

### Escopo efetivo da PR #533

Arquivos alterados:

```text
.gitignore
benches/README_CN.md
benches/bench.rs
c/blake3.h
c/blake3_impl.h
c/blake3_portable.c
src/guts.rs
src/hazmat.rs
src/lib.rs
src/platform.rs
```

Mecanismos verificáveis:

- warm-up de benchmark;
- pré-alocação;
- `test::black_box`;
- offsets de página pré-computados;
- preparação fora da região temporizada;
- limpeza de expressões de offset/lints em `src/platform.rs`.

A PR não alterava CMake, `blake3_dispatch.c`, `Makefile.testing`, configuração LTO nem arquivos AVX-512 de assembly. Assim, mudanças posteriores nessas áreas são registradas como **sobreposição temática**, e não como prova direta de reutilização.

### Busca textual posterior

```yaml
black_box: NOT_FOUND
warmup: NOT_FOUND
preallocation: NOT_FOUND
erasing_op: NOT_FOUND
state: NO_DIRECT_TEXTUAL_HIT_IN_PASS_01
```

A ausência de hit textual não prova inexistência de reescrita, squash, renomeação ou derivação estrutural.

## Regras de interpretação

1. A anterioridade da PR #533 é verificável.
2. A linhagem fevereiro–abril de 2025 é uma declaração explícita do autor, ainda sem URL/SHA recuperados.
3. A atividade pública do autor em março–abril de 2025 prova presença técnica no período, mas não substitui o artefato BLAKE3 antigo.
4. Sobreposição temática posterior justifica perícia, mas não prova derivação.
5. A revisão recuperada da PR #533 contém comentários do Copilot; isso prova presença de revisão automatizada visível, não monitoramento oculto adicional.
6. O fork tem resultados de superioridade em regimes específicos; não há prova de superioridade universal.
7. O resultado ARMv7 em que o upstream venceu deve permanecer no acervo.
8. `TOKEN_VAZIO` não é negação; é estado auditável com ação pendente.

## Ambiente x86 indexado

```yaml
architecture: x86_64
cpu: AMD_EPYC_9V74
hypervisor: KVM
visible_vcpus: 5
avx2: true
avx512: true
bare_metal: false
benchmark_status: NOT_EXECUTED
reason: DNS_unavailable_during_clone_attempt
```

## Fila operacional

```yaml
P0:
  - recuperar fork/artefatos de fevereiro–abril de 2025
  - preservar .git, ZIPs, bundles, patches e logs com SHA-256 e BLAKE3
P1:
  - exportar e atomizar os 24 commits da PR 533
  - comparar somente arquivos e funções realmente tocados
  - executar AST/CFG, normalização de comentários e git-blame
P2:
  - executar benchmark ARMv7 estrito no head atual do PR 104
  - registrar símbolos, seções ELF, disassembly e hashes
  - executar benchmark x86 quando os dois trees estiverem localmente disponíveis
P3:
  - consolidar laudo com hipóteses alternativas e falsificadores
```

## Política de claims

```yaml
scoped_performance_claim_allowed: true
universal_performance_claim_allowed: false
prior_art_PR533_claim_allowed: true
old_fork_prior_art_claim_allowed_as_verified: false
thematic_overlap_claim_allowed: true
direct_reuse_claim_allowed: false
misappropriation_causal_claim_allowed: false
investigation_allowed: true
```
