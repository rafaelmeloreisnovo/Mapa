# ZIPRAF Real Archive — Control Plane Federado V2

Status: `CANONICAL_DRAFT / PRODUCER_PR_OPEN`  
Data: `2026-08-01`  
Claim global: `claim_allowed=false`

## 1. Papel do Mapa

O repositório Mapa não duplica o parser C. Ele registra a relação entre:

```text
conceito autoral
→ produtor técnico
→ commit/PR
→ gate
→ limites
→ próximo falsificador
```

O produtor técnico desta etapa é `rafaelmeloreisnovo/Vectras-VM-Android`, PR `#1078`. Enquanto a PR estiver aberta e o gate remoto não estiver verde, o estado federado permanece `PR_OPEN_REMOTE_GATE_PENDING`.

## 2. Invariante central

```text
ZIP compatibility
≠ direct-map layout
≠ digest verification
≠ executable authorization
≠ DMA authorization
≠ physical zero-copy
```

A geometria de uma entrada `STORE` alinhada autoriza somente a classificação `DIRECT_MAP_LAYOUT`. A promoção para bloco compartilhável exige digest externo, imutabilidade e verificação. Execução e DMA exigem gates independentes.

## 3. Álgebra das entradas

```text
EntryAction ::= DIRECT_MAP_LAYOUT
              | COPY_STORE
              | DECOMPRESS
              | REJECT
```

A álgebra impede tratar todos os arquivos ZIP como se fossem extraíveis, executáveis ou mapeáveis da mesma forma.

## 4. Permutação lógica

```text
core(i)      = nth_set_bit(mask, i mod popcount(mask))
phase(i)     = floor(i / popcount(mask))
direction(p) = FORWARD quando p é par; REVERSE quando p é ímpar
```

Essa permutação é reproduzível e auditável. Não representa ainda uma harmônica física do clock. Ciclos, cache misses, page faults, migração de core e latência pertencem ao futuro receipt de benchmark.

## 5. Segurança estrutural

O control-plane exige rejeição de:

- caminhos absolutos;
- travessia `..`;
- segmentos vazios;
- nomes terminados em ponto ou espaço;
- dispositivos reservados;
- colisões portáveis por caixa ou separador;
- symlink como payload vinculável;
- conteúdo criptografado no perfil atual;
- overlaps e aliases não demonstrados.

## 6. Urgência por dependência

```text
U0 real ZIP spans
→ U1 digest criptográfico
→ U2 corpus ZIP/APK
→ U3 Termux/Android mmap
→ U4 DEFLATE delimitado
→ U5 scheduler 1/2/4/8 cores
→ U6 BitRafa/FEC provado
→ U7 DMA/IOMMU/IRQ físico
→ U8 autoridade Merkle/ledger
```

A ordem não é decorativa. Um estágio não pode herdar autoridade de outro:

```text
host mmap PASS
↛ Android mmap PASS
↛ DMA PASS
↛ execução PASS
↛ FEC 45% PASS
```

## 7. Gate adversarial federado

O validador e os testes impedem:

- `claim_allowed=true`;
- registrar PR aberta como mesclada;
- promover CRC32 a identidade criptográfica;
- promover DEFLATE a direct-map;
- transformar o receipt host em zero-copy físico;
- promover Android, octa-core ou DMA sem evidência;
- declarar 35–45% de recuperação BitRafa;
- enfraquecer a política de nomes;
- reordenar silenciosamente a matriz U0–U8.

## 8. Estado atual

```yaml
producer_pr: 1078
producer_merged: false
producer_remote_gate: PENDING
host_local_kat: PASS_37
host_mmap_receipt: VERIFIED_LIMITED_LOCAL
android_mmap: TOKEN_VAZIO
dma_iommu_irq: TOKEN_VAZIO
bitraf_35_45: NOT_AUTHORIZED
claim_allowed: false
```

## R3

```text
F_ok:
  evidência local do produtor, matriz de urgência, limites de promoção,
  política de segurança e gate federado foram materializados.

F_gap:
  conclusão remota da PR produtora, digest real, corpus APK,
  Termux/Android e medições multicore.

F_next:
  reconciliar o head/resultado remoto da PR #1078 e iniciar U1:
  SHA-256/BLAKE3 por payload com vetores conhecidos e receipts por entrada.
```
