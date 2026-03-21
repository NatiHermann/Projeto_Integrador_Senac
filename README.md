# Projeto Integrador Senac - Desenvolvimento Low Code em Ciência de Dados

## Integrantes
- Natália Hetkowski Hermann
- Thalita Neves
- Vitória Rodrigues

## Visão geral da primeira entrega
Esta primeira etapa tem como objetivo comprovar a organização inicial do projeto e a viabilidade técnica de uma pipeline de ETL com visualização de dados. O grupo estruturou o repositório, definiu a base de dados inicial, implementou o fluxo de extração, transformação e carga, e desenvolveu um dashboard interativo para exploração dos resultados.

O recorte escolhido para esta entrega foi o arquivo de metadados do dataset Onco360. A decisão por começar pelos metadados foi proposital: esse arquivo permite validar todo o fluxo técnico do projeto antes da ampliação para tabelas analíticas mais complexas da área de oncologia.

## 1. Criação e organização do repositório
O repositório foi organizado para separar configuração, processamento, armazenamento e visualização dos dados. A estrutura atual facilita o desenvolvimento colaborativo e a evolução do projeto nas próximas entregas.

### Estrutura inicial
- app.py: aplicação Streamlit com o dashboard interativo
- pipeline.py: pipeline principal de ETL
- README.md: documentação da primeira entrega
- requirements.txt: dependências do projeto
- config/project.yaml: configurações da origem dos dados e destinos de carga
- data/processed/: arquivos tratados gerados pelo ETL
- database/: banco SQLite gerado pela carga

### Organização adotada
- separação entre código, configuração, dados processados e banco local
- README visível na raiz com contexto, escopo e instruções de execução
- estrutura simples o suficiente para a primeira entrega e expansível para as fases seguintes

## 2. Definição da base de dados e contextualização
### Base escolhida
Foi utilizada a base de metadados do dataset Onco360, disponibilizado no Kaggle. Para executar o projeto, baixe o dataset do Kaggle (https://www.kaggle.com/datasets/onco360) e coloque o arquivo raw_onco360_metadados.csv em data/raw/.

O caminho da origem pode ser alterado no arquivo de configuracao config/project.yaml ou diretamente pela barra lateral do dashboard.

### Contexto da base
O Onco360 reúne arquivos relacionados ao domínio de oncologia. Nesta primeira entrega, o grupo não utilizou ainda as tabelas de eventos clínicos ou diagnósticos, mas sim o arquivo de metadados do conjunto, que descreve os arquivos disponíveis, datas de extração, quantidade de registros e volume armazenado.

### Origem da base
- fonte externa: Kaggle
- dataset: Onco360
- arquivo utilizado na etapa: raw_onco360_metadados.csv

### Objetivo da análise nesta etapa
O objetivo da análise inicial foi responder perguntas operacionais sobre a base escolhida:

- quais arquivos possuem maior volume de registros
- quais arquivos ocupam mais espaço em armazenamento
- como os arquivos se distribuem por formato e porte
- qual a relação entre tamanho do arquivo e quantidade de registros

Esse recorte foi adequado para a primeira entrega porque valida a arquitetura do projeto sem exigir, neste momento, o tratamento completo de bases clínicas mais complexas.

## 3. Planejamento do processo de ETL
O processo foi estruturado em três etapas clássicas: extração, transformação e carga.

### Extração
- leitura do arquivo CSV configurado em config/project.yaml
- validação da existência do arquivo antes do processamento
- carregamento da base em DataFrame com pandas

### Transformação
As transformações implementadas em pandas foram planejadas para padronizar os dados e gerar indicadores iniciais para o dashboard:

- renomeação das colunas principais para um padrão de análise
- conversão da coluna de data para formato datetime
- conversão das colunas numericas de registros e tamanho
- identificação do nome base do arquivo sem extensão
- derivação da camada do dado: raw, silver ou gold
- derivação do domínio do arquivo
- identificação do formato do arquivo
- classificação do porte do arquivo com base no tamanho em MiB
- cálculo do indicador registros_por_mib
- criação das colunas de ano e mês de extração
- ordenação dos registros pelo maior volume de registros

### Carga
- exportação da base tratada para CSV em data/processed/onco360_metadata_tratado.csv
- gravação da base tratada no banco SQLite em database/onco360_metadata.db
- gravação de uma tabela resumo agregada por formato e porte do arquivo

### Fluxo do processo
1. Ler o arquivo bruto de metadados.
2. Padronizar tipos e nomes das colunas.
3. Gerar atributos derivados para análise.
4. Criar um resumo agregado para apoio ao dashboard.
5. Salvar os resultados em CSV e SQLite.
6. Consumir a base tratada no dashboard Streamlit.

### Resultado atual do ETL
Na execução atual do projeto, a base tratada gerada possui 84 registros de dados, além do cabeçalho do arquivo CSV exportado. Isso confirma a execução de ponta a ponta da pipeline nesta primeira fase.

## 4. Planejamento do dashboard
O dashboard foi planejado para permitir leitura rápida do comportamento da base escolhida. As métricas e visualizações foram definidas em coerência com o arquivo de metadados utilizado.

### Métricas principais
- quantidade de arquivos no painel
- total de registros
- tamanho total armazenado em MiB
- data da última extração dísponivel

### Indicadores derivados
- porte do arquivo
- formato do arquivo
- registros por MiB
- distribuição por camada e domínio

### Visualizações previstas e implementadas
- gráfico de barras horizontal com os 10 arquivos de maior volume de registros
- gráfico de dispersão relacionando tamanho do arquivo e número de registros
- tabela resumo agregada por formato e porte
- tabela detalhada da base tratada com filtros

### Filtros disponíveis
- filtro por formato do arquivo
- filtro por porte do arquivo
- campo para alterar o caminho do arquivo CSV de origem
- botao para reexecutar o ETL diretamente pela interface

### Objetivo do dashboard nesta etapa
O painel não foi pensado ainda como produto final, mas como uma prova de conceito funcional. O foco foi demonstrar que a base tratada pode ser explorada visualmente, com navegacao, métricas e gráficos coerentes com os dados processados.

## 5. Organizacão do README e planejamento das tarefas
Este README foi estruturado para cobrir explicitamente os itens exigidos na primeira entrega: repositório, definição da base, planejamento do ETL, planejamento do dashboard e divisão de tarefas.

### Cronograma da primeira parte
| Período | Entrega prevista |
| --- | --- |
| Semana 1 | Definição do tema, busca da base e criação do repositório |
| Semana 2 | Estruturação do pipeline e configuração do ambiente |
| Semana 3 | Implementação das transformações e carga em SQLite |
| Semana 4 | Montagem do dashboard, revisão do README e preparação para apresentação |

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

## Dependências principais
- pandas
- PyYAML
- streamlit
- plotly
- pyarrow

## Saídas geradas pela primeira entrega
- database/onco360_metadata.db
- data/processed/onco360_metadata_tratado.csv

## Conclusão da etapa
Esta primeira entrega comprova que o projeto possui base técnica organizada para continuar evoluindo. O repositório esta estruturado, a base escolhida foi contextualizada, o processo de ETL foi planejado e implementado, e o dashboard já oferece uma camada inicial de análise.

Nas proximas etapas, o grupo pretende ampliar o escopo para arquivos analiticos mais ricos do dataset Onco360, incluindo novas regras de limpeza, novos indicadores e visualizacoes mais proximas do problema de negocio.
