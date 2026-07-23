# Ontologia Operacional RAFAELIA — v1

## Estado

```text
status = DRAFT_AUDITABLE
claim_allowed = false
automatic_merge = false
automatic_execution = false
```

A ontologia transforma o inventário da sessão em uma estrutura executável de
biblioteconomia computacional, governança de dados e auditoria de ciência de
fronteira. Ela não tenta executar todas as possibilidades: fixa invariantes,
classifica lacunas e seleciona o próximo gate verificável.

## Oito braços operacionais

| Braço | Função |
|---|---|
| 1. Catálogo | identidade, versão e tipo do objeto |
| 2. Contexto | língua, domínio, época, escala e autoridade terminológica |
| 3. Proveniência | fonte, caminho, commit, dataset, run e hash |
| 4. Evidência | evidência externa/local/replicada, oposição e falsificador |
| 5. Operadores | direta, inversa, indireta, reversiva, derivadas e logs |
| 6. Vazios | desconhecido, não medido, contraditório, ignorado, abortado e retido |
| 7. Governança | finalidade, privacidade, risco, rollback e revisão humana |
| 8. Retroalimentação | resultado negativo, aprendizado e próximo gate |

Esses braços não são oito processos isolados. Formam uma célula auditável:

\[
\mathcal C=\langle
origem,claim,contexto,estado,evidência,falsificador,limite,F_{next}
\rangle
\]

## Artefatos

```text
schemas/operational-ontology.schema.json
data/ontology/rafaelia-operational-ontology.v1.json
scripts/operational_ontology_engine.py
tests/test_operational_ontology_engine.py
docs/HEURISTICAS_DINAMICAS_E_VAZIOS.md
indices/ONTOLOGIA_OPERACIONAL_RAFAELIA.md
```

## Registros iniciais

A primeira versão inclui os vazios já identificados:

- DAG causal executável;
- pesos e limiares calibrados;
- bootstrap e propagação de incerteza;
- contrato de condições de contorno das antiderivadas;
- comparação automática de modelos log-log;
- independência automática das fontes;
- reconstrução integral do corpus vetorial;
- estudo humano de compreensão semântica;
- dimensão fractal física validada;
- replicação independente.

Cada vazio possui classe, motivo, proveniência, falsificador e próximo gate.

## Estados editoriais

```text
ACTIVE
ABORTED
CENSORED
IGNORED
POTENTIAL
SUGGESTED
WITHHELD
CLOSED
```

### Regra contra inferência indevida

`CENSORED` exige evidência documental de supressão. Um arquivo não encontrado,
privado ou inacessível deve ser registrado como `WITHHELD`, `TV-ACCESS` ou
`TOKEN_VAZIO_PROVENANCE`, nunca promovido automaticamente a censura.

## Execução local

```bash
python3 scripts/operational_ontology_engine.py \
  --ontology data/ontology/rafaelia-operational-ontology.v1.json \
  --output-json build/ontology/report.json \
  --output-md build/ontology/report.md \
  --generated-at 2026-07-23T00:00:00Z

python3 -m unittest tests/test_operational_ontology_engine.py
```

O modo bloqueante existe, mas não é acionado automaticamente:

```bash
python3 scripts/operational_ontology_engine.py \
  --ontology data/ontology/rafaelia-operational-ontology.v1.json \
  --output-json build/ontology/report.json \
  --output-md build/ontology/report.md \
  --generated-at 2026-07-23T00:00:00Z \
  --strict
```

## Invariantes

```text
TOKEN_VAZIO != 0
heurística != prova
not found != censored
ponte metodológica != equivalência física
hash prova integridade, não verdade científica
uma relação inversa não prova causalidade reversa
uma reta log-log não prova lei de potência
um ciclo sem saída é reclusão estéril
```

## Limites

O motor é um validador e detector conservador. Ele não:

- infere intenção humana;
- declara censura sem documento;
- atribui causalidade a caminhos de grafo;
- escolhe pesos científicos;
- transforma metáfora em mecanismo físico;
- promove resultados sem evidência local e replicação.

## Fechamento

\[
F_{ok}=ontologia+schema+motor+testes
\]

\[
F_{gap}=dados+calibração+causalidade+replicação
\]

\[
F_{next}=executar\ relatório\ local\ e\ revisar\ os\ vazios\ de\ maior\ ganho\ informacional
\]
