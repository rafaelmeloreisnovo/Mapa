# Arquitetura do Sistema Vivo de Conhecimento

> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧

## 1. Intenção

O repositório **Mapa** não é um espelho de código nem um catálogo passivo. Ele é a camada de organização que reconhece, para cada repositório do ecossistema, cinco coisas diferentes:

1. **identidade observada**;
2. **mecanismos comprovados**;
3. **interpretações ainda testáveis**;
4. **linguagem filosófica ou parabólica**;
5. **conhecimento ainda ausente**.

A refatoração introduz um contrato executável para impedir que essas cinco classes sejam misturadas.

## 2. Separação de camadas

| Camada | Autoridade | Exemplo | Pode gerar alegação? |
|---|---|---|---|
| L0 — identidade | conector GitHub | nome, ID, branch, visibilidade | apenas sobre identidade |
| L1 — perfil de mecanismo | leitura evidenciada | entradas, transformação, saída | dentro do `claim_scope` |
| L2 — lacuna | `TOKEN_VAZIO` | propósito ainda não lido | não |
| L3 — índice derivado | construtor determinístico | completude, contagens, hash | apenas derivação reproduzível |
| L4 — visualização | Markdown/Mermaid | fluxo e estado do conhecimento | não substitui evidência |
| L5 — decisão | revisão humana + gate | promoção, prioridade, publicação | somente após validação |

## 3. Unidade mínima: célula epistêmica

Cada mecanismo é uma célula com um dos estados:

```text
FATO | HIPOTESE | PARABOLA | TOKEN_VAZIO
```

Uma célula resolvida exige `value` e `evidence`. Uma célula vazia exige:

```text
reason + next_action + exit_criteria
```

Logo:

\[
\text{ausência observada} \neq \text{erro descartável}
\]

\[
\text{ausência observada} = \text{TOKEN\_VAZIO acionável}
\]

## 4. Os onze mecanismos

Cada repositório pode ser reconhecido pelos mesmos onze eixos, sem forçar que todos estejam preenchidos:

1. propósito;
2. entradas;
3. transformações;
4. saídas;
5. interfaces;
6. invariantes;
7. controles de qualidade;
8. riscos;
9. relações;
10. contexto filosófico;
11. modelo visual.

A uniformidade está no **contrato**, não na imposição de conteúdo igual.

## 5. Fluxo determinístico

```text
REPOSITORY_INVENTORY_HEAD
        │
        ├── checkpoint
        └── deltas
                │
                ▼
      identidade normalizada
                │
                ├── perfil evidenciado existe ──▶ células promovidas
                └── perfil ausente ─────────────▶ TOKEN_VAZIO
                │
                ▼
       LIVING_SYSTEM_INDEX
                │
                ├── estatísticas derivadas
                ├── BLAKE2b-256
                └── claim_allowed fail-closed
```

## 6. Regras que impedem alucinação estrutural

- O nome do repositório nunca determina sua função.
- Um perfil sem identidade no inventário é rejeitado.
- Um `TOKEN_VAZIO` não aceita valor nem evidência.
- `FATO`, `HIPOTESE` e `PARABOLA` exigem evidência localizável.
- `HIPOTESE` exige confiança numérica inferior a 1.
- Divergência entre `materialized_count` e registros fundidos interrompe a construção.
- IDs duplicados ou conflitantes interrompem a construção.
- O hash cobre toda a representação, exceto o próprio campo de digest.
- A completude é derivada, nunca editada manualmente.
- O índice global permanece com `claim_allowed=false` enquanto o inventário for parcial.

## 7. Organização física

```text
schemas/repository_mechanism.schema.json
    contrato descritivo

data/mechanisms/profiles/*.json
    conhecimento manual evidenciado

scripts/build_living_system_index.py
    fusão, normalização, TOKEN_VAZIO, métricas e hash

scripts/validate_living_system_index.py
    validação independente e fail-closed

indices/LIVING_SYSTEM_INDEX.json
    produto determinístico gerado

visual/SISTEMA_VIVO.md
    leitura humana e rota de desenvolvimento
```

## 8. Operação

```bash
python3 scripts/build_living_system_index.py --write
python3 scripts/build_living_system_index.py --check
python3 scripts/validate_living_system_index.py
python3 -m unittest tests/test_living_system_index.py -v
```

A geração não lê código remoto automaticamente. A coleta remota continua sendo responsabilidade do inventário/conector; o Mapa consome apenas identidades já materializadas e perfis revisados.

## 9. Critério de evolução

Um repositório progride quando um campo deixa de ser vazio por evidência, não quando recebe texto em maior volume.

\[
Q = \frac{\text{células resolvidas com evidência}}{\text{células contratadas}}
\]

`Q` mede cobertura documental, não verdade científica do conteúdo. A verdade de cada alegação continua limitada por seu estado e por seu `claim_scope`.

## 10. Próxima fronteira preservada

O campo `relations` do próprio Mapa permanece sem promoção completa até que as relações entre repositórios sejam reconstruídas a partir de commits, caminhos e contratos de produtor/consumidor. Essa ausência é intencional: é o próximo `TOKEN_VAZIO` de maior valor estrutural.
