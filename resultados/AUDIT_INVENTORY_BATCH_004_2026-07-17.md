# Auditoria do lote 4 — integração, Android e proteção

## Propósito

Continuar a materialização incremental do inventário por capacidade operacional, sem promover o maestro e sem misturar o incidente de billing com a validade estrutural do lote.

## Decisão arquitetural

O snapshot `indices/REPOSITORY_INVENTORY.json` permanece como checkpoint imutável de `41/126`.

O estado corrente passa a ser derivado por:

```text
checkpoint 41/126
+ indices/inventory_deltas/BATCH_004_2026-07-17.json
= indices/REPOSITORY_INVENTORY_HEAD.json
= 51/126
```

Essa separação evita reescrever um JSON monolítico crescente, preserva os digests históricos e permite que os próximos lotes sejam aplicados atomicamente.

## Entrada

```text
batch_id = BATCH_004_2026-07-17
observed_at = 2026-07-17T19:03:45Z
source = github_connector.get_repo
records = 10
owner split = 5 pessoais + 5 institucionais
batch digest = 9398980523037b7390717b4d65eaccc57fb5db54bf8dc1afa8a58d2dd116e151
```

## Registros pessoais

- `rafaelmeloreisnovo/GAIA_phi`
- `rafaelmeloreisnovo/Rafaelia_Core`
- `rafaelmeloreisnovo/ZIPRAF_OMEGA_FULL`
- `rafaelmeloreisnovo/androidRom`
- `rafaelmeloreisnovo/termux-api_rafcodephi`

## Registros institucionais

- `instituto-Rafael/Firewall`
- `instituto-Rafael/apk-antitrust-rafaelia`
- `instituto-Rafael/apk-gboard-insight`
- `instituto-Rafael/apk-js-zrf-privacy`
- `instituto-Rafael/manifesto-antioligopolio-rafaelia`

## Resultado derivado pelo HEAD

```text
checkpoint_materialized = 41
delta_added = 10
head_materialized = 51
accessible_total_observed = 126
remaining_TOKEN_VAZIO = 75
completeness_ratio = 0.404761904762
public = 29
private = 22
archived = 0
instituto-Rafael = 24
rafaelmeloreisnovo = 27
inventory_state = PARTIAL
claim_allowed = false
```

## Integridade

```text
checkpoint digest =
204b310de7ecbfc0e4df316d126748b03cb4ed624a3e0eff8914a3a1e8018d48

batch 004 digest =
9398980523037b7390717b4d65eaccc57fb5db54bf8dc1afa8a58d2dd116e151

derived inventory digest =
ac88b804985b79a1310e794b10294d83ac2e01e7f33bd7338bbb4aacea84d2a2

HEAD digest =
f30a5bc299e3d786b4e90099a9598273c1b965186da3665004225b6f4009824c
```

## Prova de continuidade

A reconstrução determinística reproduziu os três estados oficiais anteriores:

```text
BATCH_001 state digest = 1e9fa96ea2651e385fd095e2a72b3dfba7a675a6701c78f2ba63139b183952e9
BATCH_002 state digest = 3151f39d5d9021cdcfa21a57b9a603325b86d5d668916389433e4ac8a8e99641
BATCH_003 state digest = 204b310de7ecbfc0e4df316d126748b03cb4ed624a3e0eff8914a3a1e8018d48
```

Depois, 46 verificações locais cobriram:

- unicidade de nomes e IDs;
- identidade exata lote ↔ estado derivado;
- estatísticas e ausência derivadas;
- digest do lote, HEAD e inventário resultante;
- ordem temporal;
- replay idempotente;
- preservação de `PARTIAL`;
- preservação de `claim_allowed=false`.

O novo teste adversarial também rejeita adulteração do HEAD, checkpoint, digest do delta, contagem derivada e repetição de lote.

## Gate

O workflow existente foi ampliado, sem criar outro YAML.

Ele passa a validar separadamente:

```text
topologia
checkpoint 41/126
cadeia histórica BATCH_001–003
HEAD
delta BATCH_004
claim boundary
checksums
```

## Fronteira de claim

O lote prova somente identidade e metadados retornados pelo conector GitHub:

- owner e nome;
- ID estável;
- clone URL;
- branch padrão;
- visibilidade;
- estado de arquivamento;
- tamanho em KiB observado.

Não prova conteúdo, autoria integral, maturidade, funcionamento, segurança, eficácia, valor científico ou valor comercial.

## GitHub Actions

O incidente de Actions permanece em eixo separado:

```text
Mapa execution classification = ZERO_STEP_NO_LOGS
billing block outside RLL = reported by owner
billing message artifact captured = false
RLL positive control = VERIFIED
RLL exception root cause = TOKEN_VAZIO
```

A validação local não é promovida a `remote PASS`.

## Rollback

Reverter os commits do lote remove:

```text
REPOSITORY_INVENTORY_HEAD.json
inventory_deltas/BATCH_004_2026-07-17.json
validador e testes do HEAD
recibos do lote 4
extensão do workflow
```

O checkpoint permanece intacto em `41/126`, com três lotes históricos e digest oficial preservado.
