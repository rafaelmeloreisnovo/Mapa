# Metodologia Mapa — Private CI Bridge V1

## Intenção

Permitir que um CI selecionado de um repositório privado seja **reproduzido** pelo plano público de controle do RafGitTools quando o runner do privado não estiver disponível, sem tornar o código privado público e sem transportar o valor do segredo para o processo que executa o código privado.

A unidade de execução é:

```text
(target_id, exact_commit_sha, workflow_id)
```

Nunca `branch latest`, nunca YAML arbitrário e nunca um comando livre enviado pelo usuário.

## Autoridades

| Plano | Autoridade | O que prova |
|---|---|---|
| Método, rota, relações e gaps | `Mapa` | contrato/topologia |
| Executor e CI pública | `RafGitTools` | execução do replay e receipt |
| Fonte e manifesto replayável | repositório privado alvo | quais comandos representam aquele workflow |
| Credencial | GitHub Actions secret store do RafGitTools | acesso ao alvo, não resultado |
| Evidência | receipt sanitizado | resultado daquela execução exata |
| Claim | revisão humana | promoção, se os gates fecharem |

Portanto:

```text
SOURCE ≠ ARTIFACT ≠ EXECUTION ≠ EVIDENCE ≠ CLAIM
```

## Rota determinística

```text
DISCOVER
  ↓
PUBLIC ALLOWLIST ∩ PRIVATE MANIFEST
  ↓
EXACT SHA ACCESS            ← PAT_ACTIONS existe somente aqui/checkout
  ↓
VERIFY SOURCE IDENTITY
  ↓
SECRETLESS REPLAY           ← argv; shell=false; PAT ausente
  ↓
SANITIZE                    ← stdout/stderr → hash + bytes + return code
  ↓
PUBLIC RECEIPT
  ↓
REVIEW / PROMOTION
```

### DISCOVER

O catálogo no RafGitTools registra nomes de repositórios e caminhos de workflows encontrados no branch padrão. Ele é um mapa de descoberta, **não uma autorização**. A observação atual tem 35 repositórios privados e 233 workflows descobertos, com `exhaustive=false` porque a busca é limitada e pode perder casos.

### ALLOWLIST

Para executar, duas autoridades precisam concordar:

```text
workflow_allowed =
  public_registry_allows(workflow_id)
  AND
  private_manifest_allows(workflow_id)
```

O público pode revogar sem escrever no privado; o privado pode revogar sem escrever no público. Uma autorização unilateral não executa.

### EXACT_SHA_ACCESS

A credencial abre somente o repositório/commit autorizado. O SHA deve ser 40-hex minúsculo e a identidade observada precisa coincidir.

A credencial não é prova de build nem de teste.

### SECRETLESS_REPLAY

O PAT não é variável global do job. Os comandos privados são executados somente depois do checkout e com ambiente reconstruído sem `PAT_ACTIONS`, `PROVIDER_ACTIONS_TOKEN`, `GH_TOKEN` ou `GITHUB_TOKEN`.

O manifesto não contém shell livre. Cada passo é vetor `argv[]`, executável allowlisted, diretório relativo e timeout limitado.

### EVIDÊNCIA PÚBLICA

O receipt pode publicar:

- repositório/commit/workflow;
- SHA-256 do YAML e manifesto;
- hash do vetor argv;
- exit code;
- quantidade de bytes stdout/stderr;
- SHA-256 de stdout/stderr;
- hashes de artefatos privados explicitamente declarados;
- estado/gaps.

Ele não publica:

- conteúdo-fonte privado;
- conteúdo cru de stdout/stderr;
- valores de segredos;
- artefatos privados crus.

## ZIPRAF

ZIPRAF entra como possível envelope futuro do **receipt sanitizado**. Container não equivale a criptografia.

```text
ZIPRAF_RECEIPT_PROFILE = TOKEN_VAZIO_NOT_IMPLEMENTED
EXTERNAL_SIGNATURE = TOKEN_VAZIO_NOT_IMPLEMENTED
RAW_PRIVATE_LOG_CONTAINER = TOKEN_VAZIO_NOT_IMPLEMENTED
```

Se houver assinatura, a chave privada fica fora do objeto. O PAT não é reaproveitado como chave criptográfica do ZIPRAF.

## Limite de segurança atual

A remoção da credencial do subprocesso reduz a exposição do PAT. Porém V1 ainda não impõe isolamento de saída de rede ao código privado. Portanto não se afirma proteção contra uma fonte privada deliberadamente hostil que tente exfiltrar o próprio conteúdo por rede:

```text
NETWORK_EGRESS_ISOLATION = TOKEN_VAZIO_NOT_ENFORCED
```

Esse limite é deliberadamente público no receipt.

## Rollback

A implementação é aditiva e reversível: remover/desabilitar a lane `private_ci`, retirar o alvo do registry público e/ou retirar o workflow do manifesto privado. Receipts históricos não são reescritos.

## Estado

```text
METHOD = MATERIALIZED
RAFGITTOOLS_IMPLEMENTATION = IMPLEMENTED_UNTESTED
PRIVATE_MANIFEST = IMPLEMENTED_UNTESTED
GENERIC_PRIVATE_REPLAY = NOT_RUN
CLAIM_ALLOWED = false
```

## R3

**F_ok:** método, dupla autorização, exact-SHA, fronteira do PAT, execução sem segredo e receipt hash-only estão definidos e materializados.

**F_gap:** replay genérico real ainda não foi executado; isolamento de egress e perfil ZIPRAF assinado continuam abertos.

**F_next:** executar primeiro `documentation-std-mil` em um SHA exato do `Rafaelia_Private`; comparar o receipt com os comandos-fonte e só então promover essa rota específica.
