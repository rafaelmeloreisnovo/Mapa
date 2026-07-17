# Auditoria — Control Plane Federado Ω³

Data de referência: `2026-07-17`  
Branch: `docs/federated-control-plane-20260717`  
Estado: `IMPLEMENTED_NOT_MERGED / CI_STARTUP_FAILURE / claim_allowed=false`

## Objetivo

Converter a leitura holística dos repositórios em contratos versionados, sem copiar código entre projetos e sem promover integração, produção ou verdade científica não demonstrada.

## Cadeia de commits

1. arquitetura federada e planos de responsabilidade;
2. registro machine-readable de autoridade por domínio;
3. contrato fail-closed de sincronização de claims;
4. quarentena de padrões inseguros encontrados em runtimes históricos;
5. validador determinístico com biblioteca padrão;
6. workflow CI com permissões mínimas, timeout, checksum e artifact;
7. ledger final de auditoria;
8. registro do resultado real da CI.

## Artefatos

```text
arquitetura/ARQUITETURA_FEDERADA_OMEGA3.md
indices/repository_authority_registry.json
protocolos/CLAIM_SYNC_CONTRACT.md
protocolos/LEGACY_RUNTIME_SECURITY_BOUNDARY.md
scripts/validate_federated_registry.py
.github/workflows/federated-registry.yml
resultados/AUDIT_FEDERATED_CONTROL_PLANE_2026-07-17.md
```

## Invariantes implantados

- um domínio canônico possui um proprietário;
- consumidor não eleva o estado do produtor;
- ausência de evidência permanece `TOKEN_VAZIO`;
- metáfora não valida mecanismo;
- presença de código não prova execução;
- protótipo não é produção;
- resultado negativo é preservado;
- bridge remoto com shell arbitrário permanece bloqueado;
- nenhum claim é liberado por esta mudança.

## Relação inicial selecionada

```text
relativity-living-light
  -> exporta estado limitado de claims RLL
llamaRafaelia
  -> consome sem elevar o estado
Mapa
  -> registra autoridade, pin e divergência
```

## Estado observado da CI

```text
run_id = 29557273842
workflow = Federated Authority Registry
status = completed
conclusion = failure
job = validate
steps_returned = 0
logs = unavailable / BlobNotFound
classification = STARTUP_FAILURE_OR_INFRASTRUCTURE_FAILURE
validator_execution_proven = false
claim_allowed = false
```

O workflow geral `CI` do mesmo commit também falhou com zero steps retornados. Como nenhum step foi iniciado e nenhum log de comando foi disponibilizado, não há evidência de falha específica do validador ou do conteúdo. Também não há prova de aprovação.

## Lacunas protegidas

- o inventário ainda não cobre todos os repositórios existentes;
- vários papéis estão em `VERIFIED_LIMITED` ou `DECLARED_BY_AUTHOR`;
- não existe ainda sincronizador automático cross-repo;
- não existe assinatura externa dos exports;
- a CI precisa ser reexecutada em runner funcional;
- integração real de runtime/dispositivo depende de artefato do aparelho;
- a classificação dos módulos legados é auditoria de segurança, não teste de cada arquivo histórico.

## Critério de promoção

Este pacote só pode sair de `claim_allowed=false` após:

```text
CI PASS com steps e logs observáveis
revisão dos proprietários dos repositórios
verificação dos caminhos canônicos
correção de autoridade ambígua
exports do produtor versionados
consumidores pinados por ref/digest
registro de rollback
```

## Resultado

A federação deixou de ser apenas interpretação narrativa e passou a possuir uma primeira camada executável de governança: registro validável, CI, checksums, fronteiras de claim e trilha de auditoria. A execução da CI permanece não provada por falha de inicialização/infraestrutura. Isso organiza o ecossistema; não declara que todas as ligações já funcionam.
