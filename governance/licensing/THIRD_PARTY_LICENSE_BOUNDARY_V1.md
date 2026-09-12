# RAFAELIA — Fronteira Obrigatória de Licenças de Terceiros V1

**Status:** `DRAFT_AUDITABLE`

## 1. Invariante

```text
REPOSITORY_OWNER
!=
AUTHOR_OF_EVERY_FILE
!=
COPYRIGHT_HOLDER_OF_EVERY_FILE
!=
RIGHT_TO_RELICENSE_EVERY_FILE
```

A licença RAFAELIA somente pode alcançar material sobre o qual exista autoridade de licenciamento.

## 2. Regra para forks e código herdado

Em forks ou repositórios derivados:

- a licença upstream continua regendo o material upstream;
- avisos de copyright e NOTICE não devem ser removidos;
- requisitos de disponibilização de fonte, modificação, atribuição e redistribuição devem ser preservados;
- contribuições originais RAFAELIA podem receber licença própria apenas quando juridicamente separáveis e compatíveis.

## 3. Fontes já identificadas pelo controle de copyright

O `governance/authorship/COPYRIGHT_AUDIT_V1.jsonl` já registra exemplos de superfícies com obrigações de terceiros, incluindo Termux, BLAKE3, OpenSSL, Gradle, Linux e outros.

Esses registros são **auditoria**, não autorização automática de relicenciamento.

## 4. Ordem de decisão por caminho

Para cada arquivo/componente:

```text
source/upstream
→ copyright holder
→ SPDX/license text
→ NOTICE
→ local modifications
→ compatibility
→ authorial authority
→ destination license
```

Qualquer lacuna crítica permanece `TOKEN_VAZIO`.

## 5. Proibição de sobreposição

É proibido inserir aviso do tipo "todo este repositório é RAFAELIA-NC-ATTR-V1" quando existirem componentes sob GPL, Apache, MIT, BSD, CC, domínio público ou qualquer outro regime incompatível com essa generalização.

## 6. NOTICE composto

Quando um pacote contiver material misto, o NOTICE deverá separar no mínimo:

- material original RAFAELIA;
- material de terceiros;
- origem/repositório;
- copyright holder, quando conhecido;
- licença e versão;
- arquivos/caminhos abrangidos;
- modificações;
- obrigações de redistribuição;
- hash/commit de evidência, quando disponível.

## 7. Comercialização

A proibição comercial RAFAELIA não pode ser usada para retirar permissões comerciais que uma licença de terceiro já conceda sobre o material de terceiro.

De modo inverso, uma licença permissiva de terceiro não concede automaticamente direitos comerciais sobre contribuições originais RAFAELIA separadamente licenciadas.

O produto combinado deverá ser analisado por compatibilidade antes de distribuição.
