# Torre da Informacao

Este documento define a arquitetura principal do repositorio Mapa.

## Objetivo

Transformar materiais dispersos em unidades rastreaveis de trabalho.

## Camadas

1. Entrada: conversa, arquivo, imagem, repositorio, Drive, Dropbox, banco ou zip.
2. Normalizacao: nome, origem, data, tipo e status.
3. Classificacao: fato, hipotese, lacuna, risco, acao ou resultado.
4. Ligacao: conectar item com sessao, arquivo, commit, pasta ou evidencia.
5. Execucao: criar tarefa objetiva para ferramenta humana ou IA.
6. Validacao: checar se a saida tem prova e caminho de origem.
7. Documentacao: registrar resultado sem apagar lacunas.

## Regra

Nenhuma inferencia deve substituir evidencia. Quando faltar prova, registrar lacuna.
