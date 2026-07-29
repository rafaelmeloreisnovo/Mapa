# Governança operacional de trabalhos conceituais — V1

## Propósito

Este contrato organiza objetos que podem coexistir no ecossistema sem serem confundidos:

```text
geometria sagrada
mandalas e símbolos
parábolas
música e frequências
biografia e testemunho
arte e imagens
hipótese científica
código e execução
direitos humanos
proteção infantil
liberdade de crença
```

A regra central é:

```text
conceito != implementação != execução != evidência != claim
```

Uma obra pode ser espiritualmente significativa, culturalmente rica e tecnicamente bem preservada sem ser apresentada como comprovação física. A separação protege tanto a ciência quanto a crença.

## Vinte camadas obrigatórias

O registro canônico usa L01–L20, desde origem, integridade e direitos até formalização, execução, evidência, ética, proteção infantil, dignidade, liberdade de crença, incidente, rollback e preservação.

Nenhuma média compensa uma camada obrigatória ausente. Um hash perfeito não compensa licença desconhecida; uma imagem bela não compensa mecanismo ausente; um teste local não compensa revisão independente.

## Prova operacional em sete degraus

```text
P0 conceito capturado
P1 ativo selado por hash
P2 metadados completos
P3 estrutura validada
P4 execução delimitada
P5 revisão independente
P6 claim público autorizado
```

O degrau P6 exige fechamento de todas as camadas obrigatórias e decisão humana explícita.

## Música, canto e Hz

Referências como `1008 Hz`, cantos gregorianos ou harmônicas podem ser catalogadas como objetos acústicos. Para qualquer afirmação técnica são necessários:

```text
arquivo de áudio-fonte
codec e taxa de amostragem
janela e método espectral
calibração
incerteza
baseline
resultado reproduzível
```

Significados espirituais podem coexistir em coluna própria. Efeitos físicos, psicológicos ou terapêuticos permanecem `TOKEN_VAZIO` até estudo adequado.

## Imagens e mandalas

A imagem entra com:

```text
hash
bytes
tipo real do arquivo
dimensões
criador/licença/consentimento
descrição observável
interpretação simbólica
claims proibidos
```

A descrição observável não tenta identificar pessoas reais nem atribuir origem histórica sem fonte. A interpretação simbólica é explicitamente separada.

## Livro que se escreve por dentro

A metáfora é implementável como ledger append-only:

```text
evento anterior
→ decisão
→ transformação
→ resultado
→ resíduo
→ próximo evento
```

Cada evento carrega `previous_event_sha256` e `event_sha256`. O sistema pode acrescentar e superseder, mas não reescrever silenciosamente o passado.

## Incidente: além da “linha que quebrou”

Uma tela azul antiga, como a lembrança do Windows 3.11, mostra o sintoma e não necessariamente a causa. O diário técnico registra:

- ambiente e versão;
- estado anterior;
- ação;
- sintoma;
- domínio provável da falha;
- logs disponíveis e ausentes;
- impacto;
- reprodução;
- rollback;
- reparo;
- aprendizado;
- resíduo ainda aberto.

## Direitos, dignidade, infância e crença

As referências internacionais funcionam como bússola de projeto, não como selo automático de conformidade. O contrato incorpora:

- dignidade e direitos humanos;
- liberdade de pensamento, consciência, religião e não religião;
- melhor interesse da criança como consideração primária;
- privacidade por desenho e minimização;
- supervisão humana, auditabilidade e contestação;
- diversidade cultural e inclusão.

A UNESCO trata dignidade, direitos humanos, privacidade, supervisão humana, diversidade, auditabilidade e avaliação de impacto como elementos de governança do ciclo de vida de IA. O contrato os transforma em gates locais, sem declarar certificação ou conformidade jurídica.

## Autoridades federadas

- `Mapa`: catálogo, camadas, estado e rotas.
- `LivroVivo_ThisBookLives`: obra, parábola, diário, mídia e preservação editorial.
- `CientiEspiritual`: ciência–espiritualidade, ética e fronteiras de interpretação.
- `RLL`/`papers`: claims físicos e validação científica.
- repositórios jurídicos/privacidade: controles legais especializados.

## Execução local

```bash
python3 -m py_compile scripts/validate_conceptual_work_control_plane.py
python3 -m unittest -v tests/test_conceptual_work_control_plane.py
python3 scripts/validate_conceptual_work_control_plane.py \
  --write-report build/conceptual-work-control-plane.json
```

## Fronteira

```text
estrutura local validada != CI remota observada
referência a direitos != conformidade legal
preservação de crença != validação científica
hash != verdade
```
