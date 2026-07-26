# QR Custody Receipt V1

Estado: `CANONICAL_DRAFT`  
Claim boundary: `claim_allowed=false`

## Propósito

`QR-CUSTODY-RECEIPT.v1` é uma superfície portátil de verificação para ligar um objeto físico ou digital a uma edição já registrada na cadeia de custódia.

```text
fonte pública/permitida
→ normalização canônica
→ projeção por edição
→ manifesto de época
→ recibo QR
→ verificação
→ evidência de auditoria
```

O QR não contém o dataset, nomes pessoais, valores comerciais, credenciais, chaves, regras secretas de projeção ou identidade clara do destinatário.

## Invariante

```text
QR != fonte de verdade
QR -> ponte verificável para o manifesto
manifesto + registro de emissão + custódia -> evidência
```

O QR isolado não prova autoria, posse, horário do vazamento ou responsabilidade jurídica.

## Payload lógico

```text
version
receipt_id
edition_id
epoch_id
manifest_sha256
canonical_root_sha256
projection_root_sha256
source_registry_root_sha256
recipient_scope_commitment
issued_at
expires_at | null
nonce
authentication_method
authenticator
claim_allowed=false
```

### Recipient scope commitment

A equipe, estação ou destinatário não aparece em texto claro:

```text
recipient_scope_commitment = SHA-256(
  tenant_id || station_id || user_scope || edition_id || salt
)
```

O `salt` permanece no registro privado de emissão. O compromisso serve para comparação controlada; não substitui autenticação.

## Transporte compacto

Forma textual proposta:

```text
RAFCUST1:<base64url(zlib(canonical-json))>
```

A compressão reduz o tamanho do QR, mas não fornece confidencialidade. Todo conteúdo do QR deve ser considerado publicamente legível.

## Autenticação

### Laboratório interno

```text
HMAC-SHA-256
```

Adequado apenas quando emissor e verificador compartilham segredo. Não oferece verificação pública independente.

### Produção ou verificação pública

```text
Ed25519 ou outro esquema aprovado após revisão criptográfica
```

A chave privada fica somente no emissor; verificadores recebem chave pública versionada e revogável.

## Canais de uso

- etiqueta física de relatório, mídia ou pacote;
- rodapé de PDF;
- tela de auditoria;
- recibo de exportação;
- checkpoint de reindexação/rotação de época;
- navegação para registro público ou privado de evidência.

## Estados de verificação

| Estado | Significado |
|---|---|
| `VALID_AUTHENTICATOR` | conteúdo intacto e autenticador válido |
| `KNOWN_RECEIPT` | receipt_id existe no ledger |
| `ROOTS_MATCH` | raízes conferem com o manifesto registrado |
| `REVOKED` | edição/chave/recibo revogado |
| `EXPIRED` | validade encerrada |
| `UNKNOWN_RECEIPT` | QR sintaticamente válido, mas sem registro |
| `INVALID` | adulteração ou estrutura inválida |
| `TOKEN_VAZIO` | evidência ou verificador indisponível |

`VALID_AUTHENTICATOR` não implica automaticamente `KNOWN_RECEIPT` ou `ROOTS_MATCH`.

## Segurança e privacidade

- não incorporar PII desnecessária;
- não usar QR como credencial de acesso;
- não colocar segredo no QR;
- não executar URL automaticamente;
- exigir confirmação humana antes de navegar;
- limitar tamanho descomprimido para evitar zip bomb;
- rejeitar campos extras não previstos;
- registrar scanner, instante, resultado e versão do verificador;
- manter decoys totalmente separados dos registros reais de pessoas públicas.

## Relação com os cinco planos

```text
M_C: raízes do dado canônico
M_D: inventário/raiz de deception, quando aplicável, nunca dados decoy no QR
M_F: edition_id, projection_root e recipient commitment
M_R: decodificação em buffer limitado e efêmero
M_A: receipt ledger, verificação, revogação e recibos de scan
```

## Falsificadores

A proposta falha se:

- dois payloads semanticamente diferentes produzirem o mesmo `receipt_id` operacional;
- conteúdo adulterado for aceito;
- o QR expuser nomes, dados sensíveis ou segredo de geração;
- o verificador aceitar raiz ausente como zero;
- recibo revogado continuar aparecendo como válido;
- a leitura depender somente da aparência visual do QR;
- HMAC for apresentado como assinatura pública.

## Fronteira atual

```text
schema e protocolo: IMPLEMENTED_DOCUMENTAL
payload/verify em laboratório sintético: destino RafPolimata
renderização Android: destino RafGitTools
assinatura pública: TOKEN_VAZIO_CRYPTO_REVIEW
uso InterBase/produção: BLOCKED
claim_allowed: false
```

---

`F_ok`: QR definido como ponte compacta de custódia.  
`F_gap`: assinatura pública, revogação e scanner Android ainda sem gate.  
`F_next`: gerar e verificar um QR sintético a partir do manifesto do laboratório.