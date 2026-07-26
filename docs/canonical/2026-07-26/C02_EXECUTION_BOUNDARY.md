# C02 — Limite de execução

O Ciclo 2 verifica a verdade local do RafPolimata no ambiente host. Ele não verifica Android, dispositivo físico, Termux, QEMU, guest boot, assinatura de APK ou desempenho.

## Promoção máxima permitida

```text
IMPLEMENTED
→ TESTED_LOCAL
→ EVIDENCE_LINKED_LOCAL
```

## Promoções proibidas neste ciclo

```text
TESTED_LOCAL ≠ VERIFIED_DEVICE
HOST_COMPILE ≠ ANDROID_RUNTIME
CROSS_COMPILE ≠ PHYSICAL_EXECUTION
BUILD_DOCTOR_PASS ≠ GENERAL_CORRECTNESS
```

## Segurança operacional

O wrapper de receipt deve ser read-only sobre o código-fonte, exceto pela criação do diretório de artefatos indicado. Não deve instalar pacotes, baixar dependências, modificar Git, apagar diretórios externos ou acessar corpus privado.