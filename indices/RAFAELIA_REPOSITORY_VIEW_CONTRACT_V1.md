# RAFAELIA — Repository View Contract V1

Estado: `CANONICAL_DRAFT / STRUCTURE_ONLY / claim_allowed=false`  
Data: 2026-08-14

## 1. Problema

O inventário de repositórios existente responde **quais repositórios existem** e preserva a cobertura/ausência no nível de metadados. Isso não basta para navegação interna.

A lacuna observada é distinta:

```text
repositório conhecido
  ≠ árvore interna conhecida
  ≠ arquivos descobríveis
  ≠ diretórios indexados
  ≠ documentação semanticamente atualizada
```

Um repositório pode estar corretamente presente no inventário e ainda conter código, dados, scripts, artefatos ou documentação sem uma rota local de descoberta.

## 2. Novo objeto: Repository View

`RAFAELIA-REPOSITORY-VIEW-1` é uma visão estrutural recursiva do checkout.

Saída canônica esperada:

```text
docs/repository-map/
  INDEX.yml
  TREE.md
  RECEIPT.json
  DIRECTORIES_*.yml
  FILES_*.yml
```

O gerador de referência fica no RafGitTools:

```text
scripts/navigation/repository_view.py
```

O contrato JSON Schema do índice fica em:

```text
schemas/repository_view_index.schema.json
```

## 3. Invariantes

1. **Recursividade:** caminhos rastreados devem ser observados até subdiretórios, não apenas na raiz.
2. **Sharding:** árvores grandes não devem ser forçadas a um único YAML monolítico.
3. **Semântica conservadora:** papel desconhecido = `TOKEN_VAZIO`, nunca conclusão inventada.
4. **Dívida documental é candidato:** ausência de README/INDEX local sinaliza revisão, não prova defeito.
5. **Arquivos soltos são candidatos:** arquivos de raiz fora dos anchors usuais entram em triagem.
6. **Presença != uso:** estar no Git não prova runtime reachability.
7. **Mapa != documentação de domínio:** o mapa revela onde olhar; README/arquitetura/status explicam o significado.
8. **Mapa != custódia de bytes:** hashes e inventário byte-a-byte continuam no streaming inventory.
9. **Mapa != execução:** nenhum claim funcional/científico é promovido por presença estrutural.
10. **Histórico preservado pelo Git:** regeneração do mapa corrente não apaga a cadeia histórica de commits.

## 4. Relação com o inventário existente

Camadas:

```text
REPOSITORY_INVENTORY_HEAD.json
    ↓ identifica repositórios / cobertura externa
Repository View
    ↓ identifica caminhos / diretórios / lacunas de navegação
CODE_TO_DOC / README / ARCHITECTURE / STATUS
    ↓ atribui significado humano
TEST / BUILD / CI / EXECUTION
    ↓ observa comportamento
EVIDENCE / CLAIM LEDGER
    ↓ permite ou bloqueia claims
```

Portanto o Repository View é uma **extensão ortogonal**, não substituição do inventário v2.

## 5. Sinais produzidos

### 5.1 `source_without_local_index`

Diretório com arquivo fonte/teste diretamente presente, mas sem anchor local semelhante a README/INDEX/MANIFEST/NAVIGATION/MAP/CATALOG/STATUS.

Interpretação correta:

```text
candidate_for_documentation_review = true
claim_directory_is_badly_documented = false
```

### 5.2 `root_loose_file_candidates`

Arquivos na raiz que não pertencem ao conjunto mínimo de anchors usuais entram em triagem para responder:

- deve permanecer na raiz?
- deve ser movido? (não automaticamente)
- deve ser indexado em README/INDEX?
- é artefato histórico?
- é duplicado?
- sua função é `TOKEN_VAZIO`?

Nenhum movimento destrutivo é autorizado por esse sinal.

### 5.3 `unknown_semantic_role_files`

Arquivos cuja extensão/caminho não fornecem classificação estrutural suficiente.

Estado obrigatório: `TOKEN_VAZIO` até revisão.

## 6. Modos de documentação por tipo de repositório

### A — autoral / núcleo ativo

Gerar mapa completo e usar a dívida estrutural para atualizar README, arquitetura, status e índices locais.

### B — fork/upstream muito grande

Não reescrever documentação upstream inteira. Adicionar um **overlay RAFAELIA** explicando:

- deltas locais;
- caminhos alterados;
- integrações RAFAELIA;
- build/testes relevantes;
- mapa recursivo como apoio de navegação.

### C — memória/dados/corpus

Prioridade em:

- proveniência;
- índice;
- shards;
- formato;
- cadeia de custódia;
- evitar leitura semântica automática de payload sensível.

### D — papers/ciência/matemática

Mapa estrutural deve levar a:

- hipóteses;
- fórmulas;
- evidências;
- falsificadores;
- claims ledgers;
- reproduções.

## 7. Gate de promoção

Um repositório só pode ser marcado `NAVIGATION_COVERED` quando:

1. o mapa recursivo foi gerado para um commit conhecido;
2. `INDEX.yml` referencia todos os shards produzidos;
3. o número de arquivos nos shards fecha com a estatística do índice;
4. diretórios foram mapeados;
5. truncamentos são explícitos;
6. desconhecidos permanecem `TOKEN_VAZIO`;
7. pelo menos os candidatos P0 de documentação foram triados.

Antes disso:

```text
navigation_state = PARTIAL | TOKEN_VAZIO
claim_allowed = false
```

## 8. F_ok / F_gap / F_next

**F_ok**
- inventário de repositórios existente preservado;
- nova camada interna formalizada;
- gerador stdlib implementado no RafGitTools;
- sharding definido para grandes árvores;
- lacunas semânticas preservadas.

**F_gap**
- execução do gerador em cada repositório ainda precisa de receipt por commit;
- relação arquivo→feature→documento ainda não existe para todos os caminhos;
- repositórios upstream gigantes exigem política de overlay antes de qualquer reescrita ampla;
- cobertura completa do universo externo ao owner atual continua dependente do inventário longitudinal.

**F_next**
- usar `data/governance/repository_view_rollout_2026-08-14.v1.yml` como ledger de rollout;
- começar por Mapa, RafGitTools, RafPolimata, papers, RLL, Termux, Vectras/QEMU, ZIPRAF e núcleos de memória;
- gerar receipts e promover cada repositório individualmente sem inferir os restantes.
