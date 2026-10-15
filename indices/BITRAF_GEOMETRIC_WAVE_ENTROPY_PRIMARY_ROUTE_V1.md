# BitRafa · mapa geométrico-vetorial da informação e senoides — correção de rota

**Correção autoral solicitada, 14/10/2026.** Esta é a rota **primária** da reconstrução; a PR experimental do codec/serializador W20 é uma rota **secundária e não equivalente**. Não inferir necessidade de APK, chip ou compressão pela palavra “dispositivo”. O objeto solicitado é a composição de estados binários em pontos, relações geométricas, direções e campos de fase.

**Fonte humana do conceito:** texto da conversa corrente do autor. **Fontes implementadas/históricas:** as quatro referências com commit e path no contrato [bitraf_geometric_wave_entropy_route.v1.json](../data/geometry/bitraf_geometric_wave_entropy_route.v1.json); não copiar conversas do Drive.

## O caminho que realmente interessa

```text
BIT ORIGINAL + IDENTIDADE + SENTIDO
    |
    v
ponto / segmento / quadrado
    |
    +--> dois triângulos equiláteros
    |                |
    +--> círculo / fase / senoide <-- ângulo e frequência
    |                |
    +--> cubo / esfera / toro (cada qual com incidência própria)
                     |
          duas pirâmides triangulares
          = dois tetraedros de 4 vértices
                     |
          8 vértices (se distintos)
          + teste de colagem/posicionamento
                     |
           campo vetorial de fase
        amplitude / peso / direção / tempo
                     |
          organização de informação
         + manutenção do bit original
         + métrica antes/depois
```

A construção `PG-Ω7` do repositório `Matem-tica-` já distingue **(a)** colagem por base, **(b)** compartilhamento apenas de ápice, e **(c)** dobra medial numa pirâmide quadrangular. A expressão “oito pontos” não permite escolher automaticamente a topologia. São propostas distintas:

| Interpretação | Vértices geométricos distintos | O que realmente existe |
| --- | ---: | --- |
| Dois tetraedros regulares sobrepostos como tetraedros complementares do cubo, sem vértices compartilhados | **8** | exemplo exato reprodutível; quatro vértices em cada tetraedro |
| Dois tetraedros colados pela face triangular/base | **5** | bipirâmide triangular; 6 faces externas |
| Dois tetraedros colados apenas por um ápice | **7** | união pinçada; dois componentes volumétricos no mesmo vértice |
| Pirâmide quadrangular de Gizé, faces laterais subdivididas ao meio | **5** | 8 painéis triangulares de superfície, **não** 8 vértices |

Na leitura de **oito vértices**, uma projeção exata e sem decimais usa os oito cantos de um cubo com `(x,y,z) ∈ {−1,+1}³`. A paridade de três etiquetas binárias reparte-os em dois tetraedros regulares de quatro vértices cada:

```text
T+ = (+++), (+--), (-+-), (--+)
T- = (---), (-++), (+-+), (++-)
```

Em cada tetraedro, toda aresta tem comprimento `sqrt(8)`, existem seis arestas e quatro faces equiláteras. O par possui oito pontos e oito faces triangulares **contadas separadamente**, mas os tetraedros interpenetram e **não** constituem, por essa contagem, uma esfera com oito faces externas nem a Grande Pirâmide histórica. Sua envoltória convexa é o cubo de seis faces quadradas. A analogia com Gizé fica `ARCHITECTURAL_ANALOGY`, não identidade arqueológica.

A identidade de três bits `b=(b0,b1,b2)` é convertida em `(1−2b0,1−2b1,1−2b2)`. Isso é uma **bijeção de oito rótulos**, não a demonstração de que oito pontos equivalem a oito bits independentes. A paridade `b0 XOR b1 XOR b2` seleciona o tetraedro; preservar o rótulo `b` evita a perda de identidade por mero agrupamento de paridade.

## Onda, tensão e entropia: três planos que não se confundem

**Plano matemático (proposta):** para cada vértice/estado `b`, projetar um campo de deslocamento ou orientação:

\[
\vec R_b(t)=\vec V_b+\sum_{k=1}^{7} a_{b,k}\sin(\omega_k t+\varphi_{b,k})\hat u_{b,k}.
\]

Aqui `a` é amplitude, `φ` fase, `ω` frequência, `u` direção e `t` tempo. **Nenhum desses coeficientes é automaticamente calibrado ou conhecido pelo código histórico.** “Tensionar os vetores” é linguagem de projeto: sem modelo de força, energia ou material não equivale à tensão mecânica medida.

**Plano source-side:** `termux-app-rafacodephi/rmr/Rrr/rafaelia_bitraf.c` contém a matriz 1000+8, valores de 42 bits particionados em sete grupos, travessia com stride 7 e campos de controle. `rafaelia_b8.S` tem sete camadas senoidais Q16.16 e pesos adaptativos. Isso mostra componentes de código relacionados; não demonstra ainda a ligação `bit → posição vetorial → senoide → tensor → recuperação do bit` com testes. A implementação de BitRAF usa `uint64_t` para os 42 bits lógicos, sem demonstrar o empacotamento compacto; inclui `string.h/unistd.h` e usa `write`, portanto essa implementação não é freestanding L0 puro. Em `bf_write`, um campo chamado `par_xor` recebe CRC32C, o que exige falsificador antes de qualquer reivindicação de preservação da paridade XOR.

**Plano informacional:** uma bijeção de representação **preserva a entropia conjunta de Shannon** do conjunto de estados, para uma mesma distribuição. Organizar bits geometricamente pode permitir busca, navegação, reconhecimento de correlação, operadores espectrais e consulta por direção mais úteis; isso deve ser medido em custo/memória/latência e precisão sem alegar diminuição física da entropia ou compressão. Se o estado original não é recuperável, a mudança é uma projeção possivelmente com perdas; marcar explicitamente.

A relação com a função de onda quântica permanece `TOKEN_VAZIO_QUANTUM_MODEL`: o código de senoides aqui é **oscilação clássica/aproximação numérica**, não uma função de onda quântica validada.

## Sete direções e falsificadores exequíveis

1. **Fonte e anterioridade:** localizar referência/commit de cada camada, sem substituir a pirâmide triédrica por W20.
2. **Geometria e incidência:** conferir o tipo exato da junção (8, 5 ou 7 vértices), as faces/arestas, dualidades e coordenadas.
3. **Identidade bit↔vetor:** round-trip dos três bits do exemplo; investigar o mapa completo da palavra histórica de 42 bits sem inventá-lo.
4. **Fase, amplitude e direção:** declarar domínio, unidades, Q16.16, limites, erros numéricos e invariantes sob rotação.
5. **Entropia e desempenho:** estimar/medir distribuições, preservação de informação, correlações, latência, footprint e baselines.
6. **Custódia/privacidade:** manter dados brutos do Drive privados; os operadores públicos só contêm metadados e testes sintéticos.
7. **Execução/CI/gates:** validar exemplo exato, testar os vetores históricos no produtor, comparar ARM32 somente quando existir executável e recibo físico; nenhum merge sob gates de provider OFF.

O novo contrato e os testes são **controle de precisão do conceito**, não código que já conecta todas as formas a um único grafo físico. `glue_map`, `sinusoidal_bit_operator`, `source_to_wave_roundtrip`, `entropy_performance_delta` e `physical_tension` continuam `TOKEN_VAZIO` tipados.

**R3:** `F_ok` = fonte histórica PG-Ω7 e código bitraf/B8 identificados, alternativa de oito vértices exata formalizável. `F_gap` = colagem autoral definitiva, operador de fase/código, métricas, execução em produtor, física. `F_next` = extrair do produtor as regras binárias e construir um operador vetorial reversible sem compressão; depois medir invariantes e qualidade. `rollback` = documentação de correção por sucessor sem apagar a rota experimental W20.
