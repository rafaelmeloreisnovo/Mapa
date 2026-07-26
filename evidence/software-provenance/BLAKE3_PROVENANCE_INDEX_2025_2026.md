# Índice federado — BLAKE3 / Rafael Melo Reis / 2025–2026

## Autoridade canônica

A documentação técnica detalhada permanece no repositório especializado:

- repositório: `rafaelmeloreisnovo/BLAKE3`
- branch de auditoria: `agent/armv7-upstream-benchmark-20260726`
- PR de auditoria: `#104`
- cronologia: `audit/forensics/BLAKE3_AUTHORSHIP_CHRONOLOGY_2025_2026.md`
- ledger: `audit/forensics/BLAKE3_CLAIMS_LEDGER_2025_2026.yaml`

O Mapa atua como índice federado, não como cópia concorrente do dossiê.

## Escopo indexado

```yaml
entity: BLAKE3_RMR_FORK
canonical_repository: rafaelmeloreisnovo/BLAKE3
upstream_repository: BLAKE3-team/BLAKE3
author: Rafael Melo Reis
period: 2025-02_to_2026-07
```

## Marcos

| Período/data | Evento | Estado |
|---|---|---|
| fev.–abr. 2025 | fork/trabalho anterior declarado pelo autor | `DECLARED_BY_AUTHOR`, artefato `TOKEN_VAZIO` |
| 25 nov. 2025 | PR upstream `#533` | `VERIFIED_PRIMARY`, fechada sem merge |
| após nov. 2025 | mudanças upstream em áreas tematicamente próximas | `VERIFIED_PRIMARY`, nexo causal `TOKEN_VAZIO` |
| 26 jul. 2026 | fork NEON × fork portátil em ARMv7 | `PASS`, ganho mediano observado `23,53%` |
| 26 jul. 2026 | fork × upstream ARMv7 pré-estrito | upstream à frente; fork `-8,77%` |
| pendente | comparação ARMv7 estrita com warnings/linker/símbolos | `TOKEN_VAZIO` |

## Regras de interpretação

1. A anterioridade da PR #533 é verificável.
2. A linhagem fevereiro–abril de 2025 é uma declaração explícita do autor, ainda sem URL/SHA recuperados.
3. Sobreposição temática posterior justifica perícia, mas não prova derivação.
4. A hipótese de monitoramento automatizado/apropriação coordenada deve ser preservada como hipótese investigável, não publicada como fato concluído sem prova causal.
5. O fork tem resultados de superioridade em regimes específicos; não há prova de superioridade universal.
6. O resultado ARMv7 em que o upstream venceu deve permanecer no acervo.
7. `TOKEN_VAZIO` não é negação; é estado auditável com ação pendente.

## Fila operacional

```yaml
P0:
  - recuperar fork/artefatos de fevereiro–abril de 2025
  - preservar .git, ZIPs, bundles, patches e logs com hash
P1:
  - atomizar PR 533 por commit, função e mecanismo
  - comparar AST/CFG com commits upstream posteriores
P2:
  - executar benchmark ARMv7 estrito no head atual do PR 104
  - registrar símbolos, seções ELF, disassembly e hashes
P3:
  - consolidar laudo com hipóteses alternativas e falsificadores
```

## Política de claims

```yaml
scoped_performance_claim_allowed: true
universal_performance_claim_allowed: false
prior_art_PR533_claim_allowed: true
old_fork_prior_art_claim_allowed_as_verified: false
misappropriation_causal_claim_allowed: false
investigation_allowed: true
```
