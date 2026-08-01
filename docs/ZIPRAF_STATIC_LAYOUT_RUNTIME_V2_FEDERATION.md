# ZIPRAF Static Layout Runtime V2 — Federação RAFAELIA

Status: `HOST_VERIFIED_LIMITED / ANDROID_BLOCKED_EXTERNAL`  
Data: `2026-08-01`  
Claim global: `claim_allowed=false`

## 1. Onde foi aplicado

A unidade executável foi aplicada no repositório `Vectras-VM-Android`, que já continha:

- parser ZIP clássico `STORE`;
- mapeamento por `FileChannel`;
- sessões de varredura;
- contrato C `rmr_static_layout`.

O `Mapa` recebe somente o plano federado de controle, receipt, schema, validador e testes. Não duplica o runtime Kotlin/C.

```text
Vectras/RMR/ZIPRAF -> implementação e gate focal
Mapa               -> governança, evidência e reconciliação
Drive               -> cânone humano e checkpoint longitudinal
Termux/GAIA/PCR     -> fontes e futuros adaptadores específicos
```

## 2. Resultado integrado

PR de origem:

```text
Vectras-VM-Android#1075
head  = 4138a0bf2a190d5eacb000dd22ffb6106c9c62c0
merge = e83836f5227afeeab99f474991fea9502067973d
```

A invariante executável é:

```text
ADDRESS = ZIP_PAYLOAD_BASE + REGION_OFFSET + LOCAL_OFFSET
```

ou:

```text
A(o,e) = B_zip(e) + Delta_region(o) + delta_local(o)
```

O endereço absoluto pertence à sessão/época de mapping. Os offsets pertencem ao manifesto.

## 3. Mudanças materializadas

```text
mmap integral na abertura      -> removido
mapping delimitado por L2      -> implementado
reuso do mapping ativo         -> implementado
CRC com scratch do chamador    -> implementado
SHA-256 direto sobre ByteBuffer-> implementado
p50/p95/p99 de mmap            -> implementado
manifesto C/Kotlin             -> implementado
FAULT como payload             -> bloqueado
FIXED_PHYSICAL no ZIPRAF       -> bloqueado
```

A remoção do mapping integral elimina o limite artificial causado por uma única `MappedByteBuffer` de tamanho `Int`. Isso não constitui, sozinho, prova de arquivo real acima de 2 GiB.

## 4. Identidade cruzada C/Kotlin

O manifesto Kotlin preserva os campos e a ordem alimentados pelo C:

```text
abi_version
layout_epoch
total_size
base_alignment
region_count
base_policy
regions[]
```

Vetor conhecido:

```text
FNV-1a 64 C      = dc16075f7047df36
FNV-1a 64 Kotlin = dc16075f7047df36
```

Essa igualdade demonstra identidade estrutural delimitada. FNV-1a não é assinatura criptográfica nem autenticação de origem.

## 5. Evidência focal

```yaml
workflow: ZIPRAF Static Layout Runtime
run_id: 30712981749
conclusion: success
checks: 31
artifact_id: 8822466423
artifact_sha256: daaaedfef2363fd4c0d95c543c5c63a91752bb315f40f36f0683af4e8c6a8d03
```

O receipt canônico encontra-se em:

```text
data/evidence/zipraf-static-layout-runtime.v2.json
```

## 6. Delimitação Android

O workflow Android não alcançou Gradle/Kotlin. O bloqueio ocorreu antes da compilação:

```text
qemu_rafaelia
pinned_sha = 2346c30c2ba77881c2930add83523ea903b173fe
resultado  = commit não encontrado no remoto
```

Portanto:

```yaml
host_reference: VERIFIED_LIMITED
android_compile: BLOCKED_EXTERNAL
android_device: TOKEN_VAZIO
```

A falha externa não é convertida em falha do ZIPRAF, mas também não autoriza promover Android para `PASS`.

## 7. Fronteira de claims

```yaml
fixed_offset: VERIFIED_LIMITED
fixed_virtual_android: TOKEN_VAZIO
fixed_physical: REJECTED_BY_POLICY
zip64: TOKEN_VAZIO
real_payload_over_2gib: TOKEN_VAZIO
zero_copy_global: false
zero_allocation_global: false
independent_reproduction: TOKEN_VAZIO
claim_allowed: false
```

## 8. Próximas aplicações por dependência

```text
F1 corrigir pin externo qemu_rafaelia
F2 executar compile Android canônico
F3 executar instrumented test em Android 10/14/15
F4 medir mapOperations, reuse, RSS e page faults
F5 testar arquivo real >2 GiB ou representação esparsa equivalente
F6 emitir receipt por dispositivo e ABI
F7 criar adaptador Termux/GAIA somente onde houver runtime próprio
```

Não se deve copiar `ZiprafStaticLayout.kt` para Termux ou GAIA. Esses repositórios devem implementar adaptadores compatíveis com o mesmo manifesto quando a plataforma exigir outra forma de binding.

## R3

```text
F_ok:
  unidade funcional integrada no Vectras;
  gate host PASS;
  receipt, schema e testes federados no Mapa.

F_gap:
  pin externo qemu_rafaelia;
  compile e execução Android;
  payload real >2 GiB;
  reprodução independente.

F_next:
  corrigir dependência externa -> compilar Android -> testar dispositivo -> medir.
```
