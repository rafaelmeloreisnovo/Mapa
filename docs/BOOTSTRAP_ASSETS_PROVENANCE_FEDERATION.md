# Bootstrap Assets Provenance — Federação V1

Status: `PRODUCER_GATE_PASS / BETA_BLOCKED`  
Data: `2026-08-01`  
Claim: `claim_allowed=false`  
Release: `release_allowed=false`

## Evidência

Produtor: `Vectras-VM-Android#1080`  
Head: `94f114b5674d10395159103cef9c3f0269b25aa4`  
Gate: `Bootstrap Assets Provenance V1`  
Run: `30723165995 = success`

O gate verde demonstra que o bloqueio está descrito e falsificável. Não demonstra presença dos payloads nem runtime Android.

## Realidade observada

```text
loader.apk = gerado
arm64-v8a.tar = ausente
armeabi-v7a.tar = ausente
x86.tar = ausente
x86_64.tar = ausente
```

Logo:

```text
loader.apk ≠ bootstrap completo
blocked-state gate PASS ≠ beta pronta
APK build ≠ dispositivo
Drive copy ≠ fonte original
SHA-256 ≠ proveniência
```

## Evidência mínima por TAR

```text
ABI + filename + source URI + immutable source ref
+ license/provenance + SHA-256 + size + safe TAR
```

A sequência de promoção termina obrigatoriamente em uma decisão separada de release, depois de build, assinatura e receipt físico.

## Privacidade

O materializador não faz download. Arquivos privados podem ser fornecidos localmente e validados; somente receipts sanitizados devem ser federados. O Drive pode armazenar uma cópia verificada, mas não substitui a fonte e a licença.

## R3

```text
F_ok:
  ausência, contrato, schema, validador, testes e materializador offline
  foram materializados; produtor passou.

F_gap:
  quatro TARs reais, origem, licença, hashes, build Android e dispositivo.

F_next:
  localizar ou produzir um TAR por vez, preencher manifesto ready,
  validar offline e só então materializar/buildar.
```
