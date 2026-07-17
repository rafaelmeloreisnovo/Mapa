# Auditoria do segundo lote natural — BATCH_002

## Propósito

Ampliar o inventário canônico por relevância operacional e remover o acoplamento do workflow a um lote específico.

## Entrada

```text
batch_id = BATCH_002_2026-07-17
source = github_connector.get_repo
records = 10
owner split = 5 pessoais + 5 institucionais
batch digest = 55f300edb1ac5d9ffdbe9a673fe1c1c93e468ded239b84616e632cba1ec703a5
```

## Autoridades pessoais materializadas

- `rafaelmeloreisnovo/RafPolimata`
- `rafaelmeloreisnovo/llamaRafaelia`
- `rafaelmeloreisnovo/papers`
- `rafaelmeloreisnovo/Vectras-VM-Android`
- `rafaelmeloreisnovo/qemu_rafaelia`

## Autoridades institucionais materializadas

- `instituto-Rafael/RAFNET_CORE`
- `instituto-Rafael/Etica-nas-Intelig-ncia-artificial-`
- `instituto-Rafael/Tegmark`
- `instituto-Rafael/apk-guardian-rafaelia`
- `instituto-Rafael/cienti-espiritual-verbo-vivo`

## Resultado

```text
before_materialized = 21
added = 10
after_materialized = 31
accessible_total_observed = 126
remaining_TOKEN_VAZIO = 95
completeness_ratio = 0.246031746032
public = 17
private = 14
archived = 0
claim_allowed = false
inventory digest = 3151f39d5d9021cdcfa21a57b9a603325b86d5d668916389433e4ac8a8e99641
```

## Correção do processo

O aplicador anterior recalculava `generated_at` mesmo quando um lote histórico era reaplicado sem adicionar registros. Isso fazia um replay antigo tentar retroceder o timestamp e o digest do inventário atual.

A nova regra é:

```text
added_count > 0  → recalcular, ordenar e selar
added_count = 0  → preservar inventário byte a byte
```

O workflow deixou de conhecer `BATCH_001` pelo nome. Agora ele:

1. descobre todos os arquivos em `indices/inventory_batches`;
2. valida contratos e digests;
3. rejeita repetição de nome ou ID entre lotes;
4. confirma que cada registro está idêntico no inventário;
5. reaplica cada lote como ponto fixo;
6. deriva contagens sem números manuais.

## Evidência local

```text
py_compile = PASS
inventory batch tests = 11 PASS
batch chain tests = 7 PASS
total = 18 PASS
chain status = PASS
batch_count = 2
total_batch_records = 20
baseline_unbatched_records = 11
all_batches_fixed_points = true
```

## Limite

O inventário permanece `PARTIAL`. A cadeia de lotes prova somente identidade, metadados do conector, integridade e ingestão determinística. Não prova maturidade funcional dos repositórios nem autoriza claims sobre seu conteúdo.
