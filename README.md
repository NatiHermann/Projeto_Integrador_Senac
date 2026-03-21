# Projeto Integrador Senac - Desenvolvimento Low Code em Ciência de Dados

## Integrantes
- Natalia Hetkowski Hermann
- Thalita Neves
- Vitoria Rodrigues

## Visao geral da primeira entrega
Esta primeira etapa tem como objetivo comprovar a organizacao inicial do projeto e a viabilidade tecnica de uma pipeline de ETL com visualizacao de dados. O grupo estruturou o repositorio, definiu a base de dados inicial, implementou o fluxo de extracao, transformacao e carga, e desenvolveu um dashboard interativo para exploracao dos resultados.

O recorte escolhido para esta entrega foi o arquivo de metadados do dataset Onco360. A decisao por comecar pelos metadados foi proposital: esse arquivo permite validar todo o fluxo tecnico do projeto antes da ampliacao para tabelas analiticas mais complexas da area de oncologia.

## 1. Criacao e organizacao do repositorio
O repositorio foi organizado para separar configuracao, processamento, armazenamento e visualizacao dos dados. A estrutura atual facilita o desenvolvimento colaborativo e a evolucao do projeto nas proximas entregas.

### Estrutura inicial
- app.py: aplicacao Streamlit com o dashboard interativo
- pipeline.py: pipeline principal de ETL
- README.md: documentacao da primeira entrega
- requirements.txt: dependencias do projeto
- config/project.yaml: configuracoes da origem dos dados e destinos de carga
- data/processed/: arquivos tratados gerados pelo ETL
- database/: banco SQLite gerado pela carga

### Organizacao adotada
- separacao entre codigo, configuracao, dados processados e banco local
- README visivel na raiz com contexto, escopo e instrucoes de execucao
- estrutura simples o suficiente para a primeira entrega e expansivel para as fases seguintes

## 2. Definicao da base de dados e contextualizacao
### Base escolhida
Foi utilizada a base de metadados do dataset Onco360, disponibilizado no Kaggle. Para executar o projeto, baixe o dataset do Kaggle (https://www.kaggle.com/datasets/onco360) e coloque o arquivo raw_onco360_metadados.csv em data/raw/.

O caminho da origem pode ser alterado no arquivo de configuracao config/project.yaml ou diretamente pela barra lateral do dashboard.

### Contexto da base
O Onco360 reune arquivos relacionados ao dominio de oncologia. Nesta primeira entrega, o grupo nao utilizou ainda as tabelas de eventos clinicos ou diagnosticos, mas sim o arquivo de metadados do conjunto, que descreve os arquivos disponiveis, datas de extracao, quantidade de registros e volume armazenado.

### Origem da base
- fonte externa: Kaggle
- dataset: Onco360
- arquivo utilizado na etapa: raw_onco360_metadados.csv

### Objetivo da analise nesta etapa
O objetivo da analise inicial foi responder perguntas operacionais sobre a base escolhida:

- quais arquivos possuem maior volume de registros
- quais arquivos ocupam mais espaco em armazenamento
- como os arquivos se distribuem por formato e porte
- qual a relacao entre tamanho do arquivo e quantidade de registros

Esse recorte foi adequado para a primeira entrega porque valida a arquitetura do projeto sem exigir, neste momento, o tratamento completo de bases clinicas mais complexas.

## 3. Planejamento do processo de ETL
O processo foi estruturado em tres etapas classicas: extracao, transformacao e carga.

### Extracao
- leitura do arquivo CSV configurado em config/project.yaml
- validacao da existencia do arquivo antes do processamento
- carregamento da base em DataFrame com pandas

### Transformacao
As transformacoes implementadas em pandas foram planejadas para padronizar os dados e gerar indicadores iniciais para o dashboard:

- renomeacao das colunas principais para um padrao de analise
- conversao da coluna de data para formato datetime
- conversao das colunas numericas de registros e tamanho
- identificacao do nome base do arquivo sem extensao
- derivacao da camada do dado: raw, silver ou gold
- derivacao do dominio do arquivo
- identificacao do formato do arquivo
- classificacao do porte do arquivo com base no tamanho em MiB
- calculo do indicador registros_por_mib
- criacao das colunas de ano e mes de extracao
- ordenacao dos registros pelo maior volume de registros

### Carga
- exportacao da base tratada para CSV em data/processed/onco360_metadata_tratado.csv
- gravacao da base tratada no banco SQLite em database/onco360_metadata.db
- gravacao de uma tabela resumo agregada por formato e porte do arquivo

### Fluxo do processo
1. Ler o arquivo bruto de metadados.
2. Padronizar tipos e nomes das colunas.
3. Gerar atributos derivados para analise.
4. Criar um resumo agregado para apoio ao dashboard.
5. Salvar os resultados em CSV e SQLite.
6. Consumir a base tratada no dashboard Streamlit.

### Resultado atual do ETL
Na execucao atual do projeto, a base tratada gerada possui 84 registros de dados, alem do cabecalho do arquivo CSV exportado. Isso confirma a execucao de ponta a ponta da pipeline nesta primeira fase.

## 4. Planejamento do dashboard
O dashboard foi planejado para permitir leitura rapida do comportamento da base escolhida. As metricas e visualizacoes foram definidas em coerencia com o arquivo de metadados utilizado.

### Metricas principais
- quantidade de arquivos no painel
- total de registros
- tamanho total armazenado em MiB
- data da ultima extracao disponivel

### Indicadores derivados
- porte do arquivo
- formato do arquivo
- registros por MiB
- distribuicao por camada e dominio

### Visualizacoes previstas e implementadas
- grafico de barras horizontal com os 10 arquivos de maior volume de registros
- grafico de dispersao relacionando tamanho do arquivo e numero de registros
- tabela resumo agregada por formato e porte
- tabela detalhada da base tratada com filtros

### Filtros disponiveis
- filtro por formato do arquivo
- filtro por porte do arquivo
- campo para alterar o caminho do arquivo CSV de origem
- botao para reexecutar o ETL diretamente pela interface

### Objetivo do dashboard nesta etapa
O painel nao foi pensado ainda como produto final, mas como uma prova de conceito funcional. O foco foi demonstrar que a base tratada pode ser explorada visualmente, com navegacao, metricas e graficos coerentes com os dados processados.

## 5. Organizacao do README e planejamento das tarefas
Este README foi estruturado para cobrir explicitamente os itens exigidos na primeira entrega: repositorio, definicao da base, planejamento do ETL, planejamento do dashboard e divisao de tarefas.

### Cronograma da primeira parte
| Periodo | Entrega prevista |
| --- | --- |
| Semana 1 | Definicao do tema, busca da base e criacao do repositorio |
| Semana 2 | Estruturacao do pipeline e configuracao do ambiente |
| Semana 3 | Implementacao das transformacoes e carga em SQLite |
| Semana 4 | Montagem do dashboard, revisao do README e preparacao para apresentacao |

## Como executar o projeto
1. Criar e ativar a virtualenv.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Executar a pipeline de ETL.

```bash
python pipeline.py
```

3. Iniciar o dashboard.

```bash
streamlit run app.py
```

## Dependencias principais
- pandas
- PyYAML
- streamlit
- plotly
- pyarrow

## Saidas geradas pela primeira entrega
- database/onco360_metadata.db
- data/processed/onco360_metadata_tratado.csv

## Conclusao da etapa
Esta primeira entrega comprova que o projeto possui base tecnica organizada para continuar evoluindo. O repositorio esta estruturado, a base escolhida foi contextualizada, o processo de ETL foi planejado e implementado, e o dashboard ja oferece uma camada inicial de analise.

Nas proximas etapas, o grupo pretende ampliar o escopo para arquivos analiticos mais ricos do dataset Onco360, incluindo novas regras de limpeza, novos indicadores e visualizacoes mais proximas do problema de negocio.
