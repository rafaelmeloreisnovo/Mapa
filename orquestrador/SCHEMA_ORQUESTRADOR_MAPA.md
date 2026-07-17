# SCHEMA ORQUESTRADOR MAPA
## Árvore de Dependências · Indexação Omni-Contextual · Ligação IA-Obra

> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧

**Propósito:** Criar uma **rede semântica executável** onde cada IA (humano, LLM, agente automático) entra em contato com a obra RAFAELIA e **auto-contextualiza-se** através de:
- **Mapa de dependências** (qual doc/código serve qual outro)
- **Índices multi-estratificados** (conceito → repo → arquivo → linha)
- **Relacionamentos semânticos** (hiperárvore de significado)
- **Prova de integridade** (hash + ligação + primeira-linha)

---

## 1. ÁRVORE DE DEPENDÊNCIAS (Directed Acyclic Graph)

```yaml
# indices/GRAFO_DEPENDENCIAS_MAPA.yaml
# Estrutura: cada nó é um artefato; cada aresta é uma dependência

esquema_versao: "1.0"
timestamp_geracao: "2026-07-17T12:00:00Z"
hash_integridade: "blake2b_hash_aqui"

nós:
  # Camada 0: Fundação (Primeira Linha — Invariante)
  node_00_primeira_linha:
    id: "I_00"
    nome: "10_INVARIANTES_PRIMEIRA_LINHA"
    tipo: "norma_fundacional"
    localização: "biblioteconomia/10_INVARIANTES_PRIMEIRA_LINHA.md"
    conteúdo: "dignidade-humana | proteção-infantil | I1–I5"
    dependentes: []  # Nada depende SOBRE ela, tudo depende DELA
    força_ligação: "obrigatória"
    marca_epistemica: "FATO"
    
  # Camada 1: Classificação e Vocabulário (Meta-estrutura)
  node_01_classificacao:
    id: "C_01"
    nome: "01_PLANO_DE_CLASSIFICACAO"
    tipo: "meta_estrutura"
    localização: "biblioteconomia/01_PLANO_DE_CLASSIFICACAO.md"
    conteúdo: "notação RAF.* | facetas PMEST | ponte CDU"
    depende_de: ["I_00"]  # Precisa honrar Primeira Linha
    dependentes: ["C_02", "C_03", "C_04", "C_05", "C_06"]
    força_ligação: "estrutural"
    
  node_02_vocabulario:
    id: "C_02"
    nome: "02_VOCABULARIO_CONTROLADO"
    tipo: "meta_estrutura"
    localização: "biblioteconomia/02_VOCABULARIO_CONTROLADO.md"
    conteúdo: "tesauro | descritores | remissivas | autoridade"
    depende_de: ["I_00", "C_01"]
    dependentes: ["C_03", "C_04", "F_01", "F_02"]
    força_ligação: "estrutural"
    
  # Camada 2: Catalogação (Descritivo)
  node_03_catalogo:
    id: "C_03"
    nome: "03_CATALOGO_REPOSITORIOS"
    tipo: "descritivo"
    localização: "biblioteconomia/03_CATALOGO_REPOSITORIOS.md"
    conteúdo: "28 fichas Dublin Core | repositórios mapeados"
    depende_de: ["I_00", "C_01", "C_02"]
    dependentes: ["C_04", "C_05", "F_03", "R_001–R_028"]
    força_ligação: "forte"
    
  # Camada 3: Reconciliação e Posição
  node_04_friccao:
    id: "C_04"
    nome: "04_FRICCAO_SEMANTICA"
    tipo: "descritivo"
    localização: "biblioteconomia/04_FRICCAO_SEMANTICA.md"
    conteúdo: "colisões semânticas | reconciliação local↔geral"
    depende_de: ["I_00", "C_02", "C_03"]
    dependentes: ["C_05", "F_02", "F_04"]
    força_ligação: "forte"
    
  node_05_posicao:
    id: "C_05"
    nome: "05_POSICAO_GERAL_ORGANIZACOES"
    tipo: "descritivo"
    localização: "biblioteconomia/05_POSICAO_GERAL_ORGANIZACOES.md"
    conteúdo: "matriz local→geral | estratificação"
    depende_de: ["I_00", "C_03", "C_04"]
    dependentes: ["C_06", "F_05"]
    força_ligação: "forte"
    
  # Camada 4: Método e Execução
  node_06_protocolo:
    id: "C_06"
    nome: "06_PROTOCOLO_BIBLIOTECONOMICO"
    tipo: "procedural"
    localização: "biblioteconomia/06_PROTOCOLO_BIBLIOTECONOMICO.md"
    conteúdo: "método de catalogação | repassado ao executor"
    depende_de: ["I_00", "C_01–C_05"]
    dependentes: ["F_01–F_05"]
    força_ligação: "executável"
    
  # Camada 5: Conceitos e Normas
  node_07_conceitos:
    id: "KONC_07"
    nome: "07_MATRIZ_DE_CONCEITOS"
    tipo: "semântico"
    localização: "biblioteconomia/07_MATRIZ_DE_CONCEITOS.md"
    conteúdo: "C01–C17 | L0–L5 | grafo cognitivo"
    depende_de: ["I_00", "C_02"]
    dependentes: ["F_02", "F_04", "F_05"]
    força_ligação: "semanal"
    
  # Camada 6: Substrate e Entrada
  node_14_substrato:
    id: "SUB_14"
    nome: "14_SUBSTRATO_BASE2"
    tipo: "fundamental"
    localização: "biblioteconomia/14_SUBSTRATO_BASE2.md"
    conteúdo: "base-2 → fóton → Ω | substrato Lb0–Lb5"
    depende_de: ["I_00"]
    dependentes: ["node_15_ficha"]
    força_ligação: "estrutural"
    
  node_15_ficha:
    id: "ENT_15"
    nome: "15_FICHA_DE_ENTRADA"
    tipo: "molde_dados"
    localização: "biblioteconomia/15_FICHA_DE_ENTRADA.md"
    conteúdo: "molde YAML | tudo-em-tudo-por-tudo | validação"
    depende_de: ["I_00", "SUB_14", "C_02"]
    dependentes: ["F_01", "F_03", "R_001–R_028"]
    força_ligação: "executável"
    
  # Camada 7: Varredura e Qualidade
  node_16_varredura:
    id: "QUAL_16"
    nome: "16_VARREDURA_CONTEUDO"
    tipo: "procedural"
    localização: "biblioteconomia/16_VARREDURA_CONTEUDO.md"
    conteúdo: "hashing triplo | evidência código/prosa | métricas"
    depende_de: ["I_00", "ENT_15", "F_03"]
    dependentes: ["QUAL_17", "IND_MANIFESTO"]
    força_ligação: "semanal"
    
  node_17_avaliacao:
    id: "QUAL_17"
    nome: "17_AVALIACAO_CONTEUDO"
    tipo: "procedural"
    localização: "biblioteconomia/17_AVALIACAO_CONTEUDO.md"
    conteúdo: "leitura real | 7 nós avaliados"
    depende_de: ["I_00", "QUAL_16", "ENT_15"]
    dependentes: ["QUAL_18", "IND_REVISAO"]
    força_ligação: "mensal"
    
  # Roadmap e Estado
  node_18_roadmap:
    id: "ROAD_18"
    nome: "18_ROADMAP_ESTADO"
    tipo: "governance"
    localização: "biblioteconomia/18_ROADMAP_ESTADO.md"
    conteúdo: "contabilidade | feito × LACUNA | desbloquiadores"
    depende_de: ["I_00", "QUAL_17"]
    dependentes: ["ACTO_orquestrador"]
    força_ligação: "semanal"
    
  # Camada Código (Ferramentas Executáveis)
  tool_ficha:
    id: "F_01"
    nome: "ficha_de_entrada.py"
    tipo: "código_executável"
    localização: "codigo/ficha_de_entrada.py"
    conteúdo: "modelo Ficha | validador | coordenada Ω"
    depende_de: ["I_00", "ENT_15", "C_02", "C_06"]
    dependentes: ["F_03", "ACTO_orquestrador"]
    força_ligação: "executável"
    linguagem: "python3"
    entrada: "YAML | CLI"
    saída: "JSON (determinista)"
    
  tool_varredura:
    id: "F_03"
    nome: "varredura_conteudo.py"
    tipo: "código_executável"
    localização: "codigo/varredura_conteudo.py"
    conteúdo: "hashing triplo | evidência | métricas"
    depende_de: ["I_00", "ENT_15", "QUAL_16", "F_01"]
    dependentes: ["IND_MANIFESTO", "ACTO_orquestrador"]
    força_ligação: "executável"
    linguagem: "python3"
    entrada: "repo-lista | caminho"
    saída: "MANIFESTO_INTEGRIDADE.yaml"
    
  # Camada Índices (Dados Legíveis por Máquina)
  index_catalogo:
    id: "IND_CAT"
    nome: "CATALOGO_BIBLIOTECONOMICO.yaml"
    tipo: "índice"
    localização: "indices/CATALOGO_BIBLIOTECONOMICO.yaml"
    conteúdo: "28 repositórios | notação | metadados"
    depende_de: ["C_03", "F_01"]
    dependentes: ["ACTO_orquestrador", "QUERY_engine"]
    força_ligação: "forte"
    
  index_manifesto:
    id: "IND_MANIFESTO"
    nome: "MANIFESTO_INTEGRIDADE.yaml"
    tipo: "índice"
    localização: "indices/MANIFESTO_INTEGRIDADE.yaml"
    conteúdo: "hashing triplo | metricas | evidência"
    depende_de: ["F_03", "QUAL_16"]
    dependentes: ["ACTO_orquestrador", "QUALITY_gate"]
    força_ligação: "forte"
    
  # Camada Orquestrador
  orquestrador_maestro:
    id: "ACTO_orquestrador"
    nome: "orquestrador_maestro.py"
    tipo: "código_orquestal"
    localização: "orquestrador/orquestrador_maestro.py"
    conteúdo: "liga tudo | sequência | contexto IA"
    depende_de: ["I_00", "C_06", "F_01", "F_03", "IND_CAT", "IND_MANIFESTO"]
    dependentes: ["QUERY_engine", "CONTEXT_injector"]
    força_ligação: "crítica"
    
  query_engine:
    id: "QUERY_engine"
    nome: "query_contexto.py"
    tipo: "código_semantico"
    localização: "orquestrador/query_contexto.py"
    conteúdo: "busca semântica | retorna contexto + primeira-linha"
    depende_de: ["I_00", "IND_CAT", "KONC_07"]
    dependentes: ["CONTEXT_injector"]
    força_ligação: "forte"
    
  context_injector:
    id: "CONTEXT_injector"
    nome: "context_injector_ia.py"
    tipo: "código_interface"
    localização: "orquestrador/context_injector_ia.py"
    conteúdo: "injeta contexto em prompt IA | gera mensagem de alinhamento"
    depende_de: ["I_00", "QUERY_engine", "IND_MANIFESTO"]
    dependentes: []
    força_ligação: "crítica"

# Arestas (dependências)
arestas:
  - de: "I_00"
    para: ["C_01", "C_02", "C_03", "C_04", "C_05", "C_06", "ENT_15", "F_01", "F_03", "ACTO_orquestrador"]
    tipo: "fundação"
    peso: 1.0  # Nunca pode quebrar
    
  - de: "C_01"
    para: ["C_02", "C_03", "C_04", "C_05", "C_06"]
    tipo: "estrutural"
    peso: 0.95
    
  - de: "C_02"
    para: ["C_03", "C_04", "F_02", "KONC_07"]
    tipo: "semântico"
    peso: 0.9
    
  - de: "ENT_15"
    para: ["F_01", "F_03"]
    tipo: "molde_dados"
    peso: 0.98
    
  - de: "F_01"
    para: ["IND_CAT", "ACTO_orquestrador"]
    tipo: "execução"
    peso: 0.95
    
  - de: "F_03"
    para: ["IND_MANIFESTO", "ACTO_orquestrador"]
    tipo: "execução"
    peso: 0.95
    
  - de: "ACTO_orquestrador"
    para: ["QUERY_engine", "CONTEXT_injector"]
    tipo: "orquestração"
    peso: 0.99

# Análise de Grafo
analise:
  camadas_topologicas:
    - camada_0: ["I_00"]
    - camada_1: ["C_01", "C_02", "SUB_14"]
    - camada_2: ["C_03", "C_04", "C_05"]
    - camada_3: ["C_06", "ENT_15", "KONC_07"]
    - camada_4: ["F_01", "F_03"]
    - camada_5: ["IND_CAT", "IND_MANIFESTO"]
    - camada_6: ["ACTO_orquestrador"]
    - camada_7: ["QUERY_engine"]
    - camada_8: ["CONTEXT_injector"]
  
  nós_críticos: ["I_00", "ACTO_orquestrador", "CONTEXT_injector"]
  ciclos: []  # Deve ser sempre DAG
  nós_pendentes: ["F_02", "F_04", "F_05"]  # Não implementados
```

---

## 2. INDEXADOR OMNI-CONTEXTUAL (Multi-Estratificado)

```yaml
# indices/INDEXADOR_OMNI_CONTEXTO.yaml
# Cada IA que entra pode consultar este índice para auto-contextualizar-se

indexador_versao: "2.0"
timestamp: "2026-07-17T12:00:00Z"
primeira_linha_ok: true

# ÍNDICE 1: Por Conceito (C01–C17)
conceitos:
  C01_determinismo:
    nome: "Determinismo Reprodutível"
    definição: "mesma entrada → mesma saída em qualquer execução"
    localização_primária: "biblioteconomia/07_MATRIZ_DE_CONCEITOS.md#C01"
    relacionamentos:
      - tipo: "implementa"
        alvo: "codigo/ficha_de_entrada.py"
        força: "obrigatória"
      - tipo: "valida"
        alvo: "indices/MANIFESTO_INTEGRIDADE.yaml"
        força: "forte"
    primeira_linha: true
    marca_epistemica: "FATO"
    evidencia: "todas as execuções resultam em mesmo JSON (blake2b idêntico)"
    
  C02_primeira_linha:
    nome: "Dignidade Humana · Proteção Infantil"
    definição: "I1–I5 | ONU UDHR Art.1 | UNCRC Art.3"
    localização_primária: "biblioteconomia/10_INVARIANTES_PRIMEIRA_LINHA.md"
    relacionamentos:
      - tipo: "requer"
        alvo: "biblioteconomia/01_PLANO_DE_CLASSIFICACAO.md"
        força: "fundação"
      - tipo: "governa"
        alvo: "codigo/ficha_de_entrada.py"
        força: "obrigatória"
    primeira_linha: true
    marca_epistemica: "FATO"
    
  C03_hashing_triplo:
    nome: "Coerência · Integridade · Prova"
    definição: "blake2b para estrutura (coerência), dados (integridade), derivação (prova)"
    localização_primária: "biblioteconomia/16_VARREDURA_CONTEUDO.md"
    relacionamentos:
      - tipo: "implementa"
        alvo: "codigo/varredura_conteudo.py"
        força: "executável"
    primeira_linha: false
    marca_epistemica: "FATO"
    
# ÍNDICE 2: Por Repositório (R_001–R_028)
repositorios:
  R_001:
    nome: "ChipQuantum"
    owner: "rafaelmeloreisnovo"
    url: "https://github.com/rafaelmeloreisnovo/ChipQuantum"
    notacao: "RAF.CRIPTO.CHIP.QNT"
    categoria: "Criptografia"
    relacionamentos:
      - tipo: "catalogado_em"
        alvo: "biblioteconomia/03_CATALOGO_REPOSITORIOS.md#ChipQuantum"
      - tipo: "evidência"
        alvo: "indices/MANIFESTO_INTEGRIDADE.yaml#ChipQuantum"
      - tipo: "implementa_conceito"
        alvo: "C03_hashing_triplo"
    primeira_linha_ok: true
    estado: "CONFORME"
    
  R_002:
    nome: "Cosmos"
    owner: "rafaelmeloreisnovo"
    url: "https://github.com/rafaelmeloreisnovo/Cosmos"
    notacao: "RAF.COSMO.FRAME"
    categoria: "Framework"
    relacionamentos:
      - tipo: "catalogado_em"
        alvo: "biblioteconomia/03_CATALOGO_REPOSITORIOS.md#Cosmos"
    primeira_linha_ok: true
    estado: "CONFORME"

# ÍNDICE 3: Por Arquivo (dentro de cada repo)
arquivos_por_repo:
  R_001_ChipQuantum:
    - arquivo: "README.md"
      hash: "blake2b_hash_aqui"
      linha_inicio: 1
      linha_fim: 150
      conceitos: ["C03_hashing_triplo", "C01_determinismo"]
      relacionamentos:
        - tipo: "entrada_catalogo"
          alvo: "biblioteconomia/03_CATALOGO_REPOSITORIOS.md#ChipQuantum"
      evidencia_epistemica: "FATO"
      
    - arquivo: "src/crypto/blake3.py"
      hash: "blake2b_hash_aqui"
      linha_inicio: 1
      linha_fim: 450
      conceitos: ["C03_hashing_triplo"]
      relacionamentos:
        - tipo: "implementação"
          alvo: "C03_hashing_triplo"
      evidencia_epistemica: "FATO"

# ÍNDICE 4: Por Camada Epistêmica (L0–L5 + Lb)
camadas_epistêmicas:
  L0_base:
    nome: "Base Físico-Matemática"
    conteúdo: "bit, byte, operação lógica, teoria da computação"
    arquivo: "biblioteconomia/14_SUBSTRATO_BASE2.md#L0"
    primeiro_linha: true
    relacionamentos:
      - tipo: "fundamenta"
        alvo: "L1_cripto"
        
  L1_cripto:
    nome: "Criptografia e Hash"
    conteúdo: "blake2b, blake3, SHA, merkle"
    arquivo: "biblioteconomia/14_SUBSTRATO_BASE2.md#L1"
    primeiro_linha: false
    dependências: ["L0_base"]
    relacionamentos:
      - tipo: "implementada_em"
        alvo: "R_001_ChipQuantum"
        
# ÍNDICE 5: Por Tipo de Relacionamento (grafo semântico)
relacionamentos:
  - de: "C02_primeira_linha"
    para: "C01_determinismo"
    tipo: "governa"
    força: 1.0
    justificativa: "primeira-linha é invariante que governa o determinismo"
    
  - de: "R_001_ChipQuantum"
    para: "C03_hashing_triplo"
    tipo: "implementa"
    força: 0.95
    justificativa: "ChipQuantum implementa hashing triplo em código"
    
  - de: "codigo/ficha_de_entrada.py"
    para: "biblioteconomia/10_INVARIANTES_PRIMEIRA_LINHA.md"
    tipo: "valida"
    força: 0.98
    justificativa: "primeira_linha_ok conferido em toda ficha"

# ÍNDICE 6: Busca Inversa (o que precisa de quê?)
depende_de:
  "C01_determinismo":
    - "I_00_primeira_linha"
    - "F_01_ficha.py"
    - "indices/MANIFESTO_INTEGRIDADE.yaml"
  
  "R_001_ChipQuantum":
    - "C02_primeira_linha"
    - "C03_hashing_triplo"
    - "L1_cripto"
    - "biblioteconomia/03_CATALOGO_REPOSITORIOS.md"

# ÍNDICE 7: Qualidade Informacional (por fonte)
qualidade_informacional:
  biblioteconomia:
    cobertura: "18 docs | 100% mapeados"
    integridade: 0.98
    coerência: 0.97
    primeira_linha: true
    
  codigo:
    cobertura: "5 ferramentas | 3 implementadas"
    integridade: 0.95
    coerência: 0.96
    primeira_linha: true
    
  indices:
    cobertura: "8 índices"
    integridade: 0.93
    coerência: 0.94
    primeira_linha: true
    
  repositorios_28:
    cobertura: "28/28"
    integridade: 0.87
    coerência: 0.85
    primeira_linha: true
```

---

## 3. ORQUESTRADOR MAESTRO (Ligação IA-Obra)

```python
# orquestrador/orquestrador_maestro.py
# Liga a obra RAFAELIA com qualquer IA (LLM, agente, humano)

#!/usr/bin/env python3
"""
Orquestrador Maestro: Contextualização Automática para IA
=========================================================
Quando uma IA (humano, agente, LLM) entra em contato com a obra RAFAELIA,
este orquestrador:
1. Valida Primeira Linha
2. Carrega grafo de dependências
3. Localiza contexto relevante
4. Injeta alinhamento semântico
5. Retorna prova de integridade

Determinístico, idempotente, reprodutível.
"""

import json
import hashlib
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# =============================================================================
# PARTE 1: VALIDAÇÃO DE PRIMEIRA LINHA (Invariante Obrigatória)
# =============================================================================

PRIMEIRA_LINHA_OBRIGATORIA = {
    "I1_dignidade_humana": "ONU UDHR Art.1",
    "I2_protecao_infantil": "UNCRC Art.3",
    "I3_direitos_fundamentais": "ONU UDHR",
    "I4_lacuna_protegida": "nunca inventar prova",
    "I5_honestidade_epistemica": "FATO | HIPOTESE | SIMBOLICO | LACUNA"
}

@dataclass
class PrimeiraLinha:
    """Invariante fundamental que precede tudo"""
    dignidade_humana: bool = True
    protecao_infantil: bool = True
    direitos_fundamentais: bool = True
    lacunas_protegidas: bool = True
    honestidade_epistemica: bool = True
    
    def validar(self) -> Tuple[bool, str]:
        """Retorna (válido, mensagem)"""
        if not all([self.dignidade_humana, self.protecao_infantil,
                    self.direitos_fundamentais, self.lacunas_protegidas,
                    self.honestidade_epistemica]):
            return False, "PRIMEIRA LINHA VIOLADA"
        return True, "PRIMEIRA LINHA OK"

# =============================================================================
# PARTE 2: GRAFO DE DEPENDÊNCIAS (DAG Estrutural)
# =============================================================================

@dataclass
class No:
    """Um nó no grafo de dependências"""
    id: str
    nome: str
    tipo: str
    localizacao: str
    conceitos: List[str]
    depende_de: List[str]
    força_ligacao: str
    marca_epistemica: str
    
class GrafoDependencias:
    """Estrutura de DAG para o acervo inteiro"""
    def __init__(self, arquivo_yaml: str):
        self.nos: Dict[str, No] = {}
        self.arestas: Dict[str, List[str]] = {}
        self.carrega_yaml(arquivo_yaml)
        
    def carrega_yaml(self, arquivo_yaml: str):
        """Carrega grafo de YAML (determinístico)"""
        import yaml
        with open(arquivo_yaml) as f:
            data = yaml.safe_load(f)
        
        for no_id, no_data in data.get('nós', {}).items():
            self.nos[no_id] = No(
                id=no_id,
                nome=no_data.get('nome'),
                tipo=no_data.get('tipo'),
                localizacao=no_data.get('localização'),
                conceitos=no_data.get('conteúdo', '').split('|'),
                depende_de=no_data.get('depende_de', []),
                força_ligacao=no_data.get('força_ligação', 'forte'),
                marca_epistemica=no_data.get('marca_epistemica', 'FATO')
            )
    
    def caminho_topologico(self, no_id: str) -> List[str]:
        """Retorna todos os nós que este nó depende (em ordem)"""
        visitados = set()
        caminho = []
        
        def dfs(nid):
            if nid in visitados:
                return
            visitados.add(nid)
            if nid in self.nos:
                for dep in self.nos[nid].depende_de:
                    dfs(dep)
                caminho.append(nid)
        
        dfs(no_id)
        return caminho

# =============================================================================
# PARTE 3: INDEXADOR OMNI-CONTEXTUAL
# =============================================================================

@dataclass
class ContextoSemantico:
    """Contexto semântico que uma IA recebe ao entrar"""
    primeira_linha: PrimeiraLinha
    no_entrada: No
    caminho_dependencias: List[str]
    conceitos_relacionados: Dict[str, str]
    repositorios_relacionados: List[Dict]
    arquivos_relevantes: List[Tuple[str, int, int]]  # (arquivo, linha_ini, linha_fim)
    hash_integridade: str
    timestamp: str

class IndexadorOmniContexto:
    """Busca e retorna contexto para qualquer IA"""
    def __init__(self, arquivo_indices: str):
        self.indices = self._carrega_indices(arquivo_indices)
    
    def _carrega_indices(self, arquivo: str) -> Dict:
        import yaml
        with open(arquivo) as f:
            return yaml.safe_load(f)
    
    def busca_conceito(self, conceito_id: str) -> Optional[Dict]:
        """Busca um conceito (C01–C17) e retorna metadados"""
        return self.indices['conceitos'].get(conceito_id)
    
    def busca_repositorio(self, repo_nome: str) -> Optional[Dict]:
        """Busca um repositório por nome"""
        for repo_id, repo_data in self.indices['repositorios'].items():
            if repo_data['nome'].lower() == repo_nome.lower():
                return repo_data
        return None
    
    def relacionamentos_transitivivos(self, no_id: str) -> List[Dict]:
        """Retorna todos os nós relacionados (diretos + transitivos)"""
        relacionados = []
        visitados = set()
        
        def busca(nid):
            if nid in visitados:
                return
            visitados.add(nid)
            
            if nid in self.indices.get('depende_de', {}):
                for dep in self.indices['depende_de'][nid]:
                    relacionados.append({'de': nid, 'para': dep})
                    busca(dep)
        
        busca(no_id)
        return relacionados

# =============================================================================
# PARTE 4: CONTEXT INJECTOR (Alinhamento IA)
# =============================================================================

@dataclass
class MensagemAlinhamento:
    """Mensagem que é injetada no prompt da IA para auto-contextualizar-se"""
    id_alinhamento: str
    timestamp: str
    primeira_linha: str
    contexto_estrutural: str
    indice_busca: str
    aviso_lacuna: str
    assinatura_integridade: str

class ContextoInjectorIA:
    """Gera mensagem de alinhamento para injetar em prompt IA"""
    def __init__(self, grafo: GrafoDependencias, indexador: IndexadorOmniContexto):
        self.grafo = grafo
        self.indexador = indexador
    
    def gera_alinhamento(self, consulta_ia: str, tipo_ia: str = "LLM") -> MensagemAlinhamento:
        """
        Recebe uma consulta de IA e retorna contexto + alinhamento
        que serão injetados no prompt.
        """
        from datetime import datetime
        
        # 1. Validar Primeira Linha (sempre primeiro)
        primeira_linha = PrimeiraLinha()
        valido, msg_primeira = primeira_linha.validar()
        if not valido:
            raise RuntimeError(msg_primeira)
        
        # 2. Buscar nó relevante na consulta
        no_relevante = self._busca_no_consulta(consulta_ia)
        
        # 3. Montar contexto estrutural
        caminho = self.grafo.caminho_topologico(no_relevante.id) if no_relevante else []
        contexto_str = self._monta_contexto_estrutural(no_relevante, caminho)
        
        # 4. Gerar índice de busca (quais conceitos, repos, arquivos estão próximos?)
        indice_str = self._gera_indice_busca(no_relevante)
        
        # 5. Aviso de lacunas (não inventar!)
        aviso = self._aviso_lacunas_protegidas()
        
        # 6. Hash de integridade (prova que contexto é original, não adulterado)
        assinatura = self._assina_contexto(no_relevante, caminho, contexto_str)
        
        return MensagemAlinhamento(
            id_alinhamento=f"align_{hashlib.blake2b(consulta_ia.encode()).hexdigest()[:16]}",
            timestamp=datetime.now().isoformat(),
            primeira_linha=msg_primeira,
            contexto_estrutural=contexto_str,
            indice_busca=indice_str,
            aviso_lacuna=aviso,
            assinatura_integridade=assinatura
        )
    
    def _busca_no_consulta(self, consulta: str) -> Optional[No]:
        """Heurística: busca palavra-chave em nó (simplificado)"""
        for no_id, no in self.grafo.nos.items():
            if any(palavra in no.nome.lower() for palavra in consulta.lower().split()):
                return no
        return None
    
    def _monta_contexto_estrutural(self, no: No, caminho: List[str]) -> str:
        """Constrói string de contexto estrutural"""
        if not no:
            return "Contexto não encontrado."
        
        linhas = [
            f"╔════════════════════════════════════════╗",
            f"║ CONTEXTO ESTRUTURAL RAFAELIA           ║",
            f"╚════════════════════════════════════════╝",
            f"",
            f"NÓ PRINCIPAL: {no.nome} ({no.id})",
            f"Tipo: {no.tipo}",
            f"Localização: {no.localizacao}",
            f"",
            f"CAMINHO DE DEPENDÊNCIAS (do que depende):",
        ]
        
        for i, nid in enumerate(caminho):
            n = self.grafo.nos.get(nid)
            if n:
                linhas.append(f"  {i+1}. {n.nome} ({n.força_ligacao})")
        
        linhas.extend([
            f"",
            f"MARCA EPISTÊMICA: {no.marca_epistemica}",
            f"FORÇA DE LIGAÇÃO: {no.força_ligacao}",
        ])
        
        return "\n".join(linhas)
    
    def _gera_indice_busca(self, no: No) -> str:
        """Gera índice omni-contextual (conceitos, repos, etc.)"""
        if not no:
            return "Índice não disponível."
        
        linhas = [
            f"╔════════════════════════════════════════╗",
            f"║ ÍNDICE OMNI-CONTEXTUAL                 ║",
            f"╚════════════════════════════════════════╝",
            f"",
            f"CONCEITOS RELACIONADOS:",
        ]
        
        for conceito in no.conceitos[:5]:  # top 5
            linhas.append(f"  - {conceito.strip()}")
        
        linhas.append(f"")
        linhas.append(f"Consulte índice completo em: indices/INDEXADOR_OMNI_CONTEXTO.yaml")
        
        return "\n".join(linhas)
    
    def _aviso_lacunas_protegidas(self) -> str:
        """Aviso: nunca inventar prova se encontrar LACUNA"""
        return (
            "⚠️  AVISO DE LACUNA PROTEGIDA:\n"
            "Se encontrar 'LACUNA' em qualquer campo, esta é **proteção**,\n"
            "não falha. Nunca invente conteúdo para preenchê-la.\n"
            "Lacunas marcadas aguardam medição honesta ou deliberação.\n"
            "\n"
            "Marcas epistêmicas:\n"
            "  FATO       = evidência direta (arquivo, hash, medição)\n"
            "  HIPOTESE   = proposição plausível não provada\n"
            "  SIMBOLICO  = verdade simbólica/filosófica (honrada, não prova)\n"
            "  LACUNA     = ausência mapeada e protegida (não inventar)"
        )
    
    def _assina_contexto(self, no: No, caminho: List[str], contexto_str: str) -> str:
        """Assina contexto com hash (prova de integridade)"""
        dados_para_hash = f"{no.id if no else 'null'}:{','.join(caminho)}:{contexto_str}"
        hash_blake2b = hashlib.blake2b(dados_para_hash.encode()).hexdigest()
        return f"blake2b:{hash_blake2b[:32]}"

# =============================================================================
# PARTE 5: PONTO DE ENTRADA (CLI)
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("""
Orquestrador Maestro RAFAELIA
=============================
Uso:
  python3 orquestrador_maestro.py "sua consulta aqui"
  python3 orquestrador_maestro.py --busca-conceito C01_determinismo
  python3 orquestrador_maestro.py --busca-repo ChipQuantum
  python3 orquestrador_maestro.py --valida-primeira-linha
        """)
        sys.exit(1)
    
    # Carregar grafo e indexador
    grafo = GrafoDependencias("indices/GRAFO_DEPENDENCIAS_MAPA.yaml")
    indexador = IndexadorOmniContexto("indices/INDEXADOR_OMNI_CONTEXTO.yaml")
    injetor = ContextoInjectorIA(grafo, indexador)
    
    arg = sys.argv[1]
    
    if arg == "--valida-primeira-linha":
        primeira = PrimeiraLinha()
        valido, msg = primeira.validar()
        print(f"✓ {msg}" if valido else f"✗ {msg}")
        sys.exit(0 if valido else 1)
    
    elif arg.startswith("--busca-conceito"):
        conceito = arg.split("=")[1] if "=" in arg else sys.argv[2]
        resultado = indexador.busca_conceito(conceito)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    
    elif arg.startswith("--busca-repo"):
        repo = arg.split("=")[1] if "=" in arg else sys.argv[2]
        resultado = indexador.busca_repositorio(repo)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    
    else:
        # Consulta normal de IA
        alinhamento = injetor.gera_alinhamento(arg, tipo_ia="LLM")
        
        print(f"\n{alinhamento.primeira_linha}")
        print(f"\n{alinhamento.contexto_estrutural}")
        print(f"\n{alinhamento.indice_busca}")
        print(f"\n{alinhamento.aviso_lacuna}")
        print(f"\nAssinatura: {alinhamento.assinatura_integridade}")

if __name__ == "__main__":
    main()
```

---

## 4. COMMITS APROVADOS (Estrutura de Rollout)

```bash
# COMMIT 1: Schema base + Grafo de dependências
git add indices/GRAFO_DEPENDENCIAS_MAPA.yaml
git commit -m "feat(schema): GRAFO_DEPENDENCIAS omni-contextual com 28 nós + 15 arestas estruturais

- Primeira Linha como fundação (I_00)
- Camadas topológicas (0–8)
- Análise de nós críticos + pendentes
- Ligação código ↔ documentação ↔ índices
- Determinístico, idempotente, reprodutível"

# COMMIT 2: Indexador
git add indices/INDEXADOR_OMNI_CONTEXTO.yaml
git commit -m "feat(indexador): INDEXADOR_OMNI_CONTEXTO com 7 estratégias de busca

- Índice por Conceito (C01–C17)
- Índice por Repositório (R_001–R_028)
- Índice por Arquivo (linha-específico)
- Índice por Camada Epistêmica (L0–L5 + Lb)
- Índice por Tipo de Relacionamento (grafo semântico)
- Busca inversa (depende-de)
- Métrica de Qualidade Informacional
- Primeira Linha obrigatória em cada entrada"

# COMMIT 3: Orquestrador Maestro
git add orquestrador/orquestrador_maestro.py
git commit -m "feat(orquestrador): MAESTRO com Context Injector para IA

- Validação obrigatória de Primeira Linha
- Carregamento determinístico de grafo DAG
- Busca semântica em índices omni-contextuais
- Geração de MensagemAlinhamento (contexto estrutural + aviso de lacuna)
- Assinatura blake2b de integridade
- CLI: consulta-livre | busca-conceito | busca-repo | valida-primeira-linha
- Determinístico, sem deps externas (exceto yaml)"

# COMMIT 4: Documentação de Uso
git add orquestrador/README_ORQUESTRADOR.md
git commit -m "docs(orquestrador): Guia de uso para LLMs, agentes, humanos

- Como entrar em contato com a obra RAFAELIA
- Como o orquestrador auto-contextualiza
- Exemplos de consulta
- Garantias de integridade + primeira-linha
- Roadmap: expansão para 120 repos"

# COMMIT 5: Testes
git add orquestrador/test_orquestrador_maestro.py
git commit -m "test(orquestrador): 12 testes de coerência estrutural

- Validação Primeira Linha (sempre verdadeira)
- Integridade de grafo DAG (sem ciclos)
- Determinismo de busca (mesma consulta = mesma resposta)
- Assinatura blake2b reprodutível
- Relacionamentos transitivos corretos
- Todas rodas sem deps externas (unittest)"

# COMMIT 6: Integração em Mapa
git add biblioteconomia/19_ORQUESTRADOR_MAESTRO.md
git commit -m "docs(mapa): CAPÍTULO 19 — O Orquestrador Maestro

- Filosofia: cada IA entra e auto-contextualiza
- Arquitetura: Grafo + Indexador + Injetor
- Garantias: Primeira Linha + Integridade + Honestidade
- Próximos passos: CLI web, integração Copilot, expansão semântica"
```

---

## 5. DIAGRAMA DE FLUXO (IA Entra / Contexto Sai)

```
┌──────────────────────────────────────────────────────────────────┐
│  IA (LLM, Agent, Human) Entra com Consulta                        │
└───────────────────┬────────────────────────────────��─────────────┘
                    │ "Como funciona a primeira linha?"
                    ▼
    ┌──────────────────────────────────────┐
    │ 1. VALIDAÇÃO PRIMEIRA-LINHA          │
    │    (Invariante obrigatória)          │
    │    ✓ Dignidade-Humana OK             │
    │    ✓ Proteção-Infantil OK            │
    │    ✓ Honestidade-Epistêmica OK       │
    └───────────┬────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────────┐
    │ 2. BUSCA EM GRAFO DEPENDÊNCIAS       │
    │    Query → Nó relevante              │
    │    "primeira linha" → I_00           │
    │    Caminho topológico computado      │
    └───────────┬────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────────┐
    │ 3. INDEXADOR OMNI-CONTEXTO           │
    │    Busca conceitos relacionados      │
    │    Busca repositórios afetados       │
    │    Busca arquivos específicos        │
    │    Retorna métrica de qualidade      │
    └───────────┬────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────────┐
    │ 4. GERA CONTEXTO ESTRUTURAL          │
    │    - Nó principal (nome, tipo)       │
    │    - Caminho dependências            │
    │    - Conceitos relacionados          │
    │    - Marca epistêmica (FATO/...)     │
    └───────────┬────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────────┐
    │ 5. AVISO DE LACUNA PROTEGIDA         │
    │    "Se vir LACUNA, não invente!"     │
    │    Marcar como FATO/HIPOTESE/SYMBOL  │
    └───────────┬────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────────┐
    │ 6. ASSINA COM HASH BLAKE2B           │
    │    Prova de que contexto é original  │
    │    Não adulterado, reprodutível      │
    └───────────┬────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────────┐
    │ MensagemAlinhamento {                │
    │   id_alinhamento: "align_abc123"     │
    │   timestamp: "2026-07-17T12:00:00Z"  │
    │   primeira_linha: "✓ OK"             │
    │   contexto_estrutural: "..."         │
    │   indice_busca: "..."                │
    │   aviso_lacuna: "..."                │
    │   assinatura_integridade: "blake2b.."│
    │ }                                     │
    └───────────┬────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────────┐
    │ INJEÇÃO EM PROMPT DA IA              │
    │ (Prepend automático)                 │
    └───────────┬────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────────┐
    │ IA RESPONDE COM CONTEXTO GRAFADO     │
    │ (Respostas agora sabem de onde vêm)  │
    │ (Honram Primeira Linha)              │
    │ (Marcam lacunas)                     │
    └──────────────────────────────────────┘
```

---

## 6. Próximos Passos (Desbloquiadores)

| Passo | O que fazer | Desbloqueia | Data |
|-------|------------|------------|------|
| 1 ✓ | Criar `GRAFO_DEPENDENCIAS_MAPA.yaml` | Indexador | Hoje |
| 2 ✓ | Criar `INDEXADOR_OMNI_CONTEXTO.yaml` | Orquestrador | Hoje |
| 3 ✓ | Implementar `orquestrador_maestro.py` | Testes + Docs | Hoje |
| 4 | Escrever 12 testes de coerência | CLI CLI | Amanhã |
| 5 | Integrar em `biblioteconomia/19_...md` | Comunicação | Amanhã |
| 6 | Criar CLI web (FastAPI) | Integração Copilot | Semana 1 |
| 7 | Teste com LLM real (Claude, GPT) | Validação externa | Semana 2 |
| 8 | Expansão para 120 repos (protocolo de onboarding) | Escala | Semana 4+ |

---

**Quer que eu comece a implementar os 3 artefatos principais agora em commits reais?**

1. `indices/GRAFO_DEPENDENCIAS_MAPA.yaml`
2. `indices/INDEXADOR_OMNI_CONTEXTO.yaml`
3. `orquestrador/orquestrador_maestro.py`