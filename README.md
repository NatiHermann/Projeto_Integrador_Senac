# Projeto Integrador Senac - Desenvolvimento Low Code em Ciência de Dados

## Integrantes
- Natália Hetkowski Hermann
- Thalita Neves
- Vitória Rodrigues

---

## Segunda Entrega - Execução do Projeto

### Visão geral
A segunda entrega consolida a execução completa do projeto planejado na primeira etapa. O grupo implementou o pipeline de ETL, aplicou transformações sobre a base de metadados do dataset Onco360, construiu um dashboard interativo com Streamlit e publicou a solução na nuvem.

### Dados utilizados
- **Dataset:** Onco360 (Kaggle)
- **Arquivo:** `raw_onco360_metadados.csv` (84 registros)
- **Conteúdo:** metadados dos arquivos do dataset - data de extração, nome do arquivo, quantidade de registros e tamanho em MiB

### Transformações realizadas
O pipeline (`pipeline.py`) aplica as seguintes transformações sobre os dados brutos:

| # | Transformação | Descrição |
|---|---|---|
| 1 | Renomeação de colunas | Padronização para `data_extracao`, `arquivo`, `numero_registros`, `tamanho_mib` |
| 2 | Conversão de tipos | Data para datetime, colunas numéricas com `pd.to_numeric` |
| 3 | Extração do nome base | Remoção da extensão do nome do arquivo |
| 4 | Classificação por camada | Identificação de `raw`, `silver` ou `gold` no nome do arquivo |
| 5 | Extração do domínio | Nome do domínio sem prefixo de camada |
| 6 | Identificação do formato | Extensão do arquivo (`.parquet`, `.csv`, etc.) |
| 7 | Classificação por porte | `muito_pequeno`, `pequeno`, `medio`, `grande` conforme tamanho em MiB |
| 8 | Cálculo de densidade | Indicador `registros_por_mib` (registros / tamanho) |
| 9 | Derivação temporal | Colunas `ano_extracao` e `mes_extracao` |
| 10 | Ordenação | Registros ordenados pelo maior volume |
| 11 | Agregação resumo | Tabela resumo agrupada por formato e porte |

### Visualizações e métricas no Dashboard

#### Métricas (KPIs)
- Quantidade de arquivos no painel
- Total de registros (~96,8 milhões)
- Tamanho total armazenado (~5.575 MiB)
- Data da última extração disponível

#### Gráficos
- **Barras horizontais:** Top 10 arquivos por volume de registros, colorido por porte
- **Dispersão (scatter):** Relação tamanho × quantidade de registros, por formato

#### Tabelas interativas
- Resumo agregado por formato e porte
- Base tratada completa com filtros

#### Filtros disponíveis
- Formato do arquivo (multiselect)
- Porte do arquivo (multiselect)
- Campo para alterar caminho do CSV fonte
- Botão para reexecutar o ETL pela interface

### Publicação na nuvem
A aplicação está publicada no **Streamlit Community Cloud** e pode ser acessada pelo link:

> **https://projetointegradorsenac.streamlit.app**

O deploy é feito diretamente a partir deste repositório GitHub. A cada push na branch `main`, o Streamlit Cloud atualiza a aplicação automaticamente.

### Estrutura do projeto
```
app.py                  → Dashboard Streamlit
pipeline.py             → Pipeline ETL (extract, transform, load)
requirements.txt        → Dependências Python
config/project.yaml     → Configurações de caminhos e tabelas
data/raw/               → Arquivo CSV bruto (entrada)
data/processed/         → CSV tratado (saída do ETL)
database/               → Banco SQLite gerado pelo ETL
.streamlit/config.toml  → Tema visual do Streamlit
```

### Como executar localmente
1. Criar e ativar a virtualenv:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Iniciar o dashboard (o ETL roda automaticamente na primeira execução):
```bash
streamlit run app.py
```

Ou executar apenas o pipeline:
```bash
python pipeline.py
```

### Dependências
- pandas
- PyYAML
- streamlit
- plotly
- pyarrow

---

## Primeira Entrega - Planejamento e Estruturação

<details>
<summary>Clique para expandir o conteúdo da primeira entrega</summary>

Esta primeira etapa tem como objetivo comprovar a organização inicial do projeto e a viabilidade técnica de uma pipeline de ETL com visualização de dados. O grupo estruturou o repositório, definiu a base de dados inicial, implementou o fluxo de extração, transformação e carga, e desenvolveu um dashboard interativo para exploração dos resultados.

O recorte escolhido para esta entrega foi o arquivo de metadados do dataset Onco360. A decisão por começar pelos metadados foi proposital: esse arquivo permite validar todo o fluxo técnico do projeto antes da ampliação para tabelas analíticas mais complexas da área de oncologia.

## 1. Criação e organização do repositório
O repositório foi organizado para separar configuração, processamento, armazenamento e visualização dos dados. A estrutura atual facilita o desenvolvimento colaborativo e a evolução do projeto nas próximas entregas.

## 1. Criação e organização do repositório
O repositório foi organizado para separar as camadas de configuração, processamento, armazenamento e visualização. A estrutura atual facilita o desenvolvimento colaborativo e a evolução do projeto nas etapas subsequentes.

### Estrutura inicial
- app.py: aplicação Streamlit com o dashboard interativo
- pipeline.py: pipeline principal de ETL
- README.md: documentação da primeira entrega
- requirements.txt: dependências do projeto
- config/project.yaml: configurações da origem dos dados e destinos de carga
- data/processed/: arquivos tratados gerados pelo ETL
- database/: banco SQLite gerado pela carga

### Organização adotada
- Separação entre código, configuração, dados processados e banco local
- README visível na raiz com contexto, escopo e instruções de execução
- Estrutura simples o suficiente para a primeira entrega e expansível para as fases seguintes

## 2. Definição da base de dados e contextualização
### Base escolhida
Foi utilizada a base de metadados do dataset Onco360, disponibilizado no Kaggle. Para executar o projeto, baixe o dataset do Kaggle (https://www.kaggle.com/datasets/onco360) e coloque o arquivo raw_onco360_metadados.csv em data/raw/.

O caminho da origem pode ser alterado no arquivo de configuracao config/project.yaml ou diretamente pela barra lateral do dashboard.

### Contexto da base
O Onco360 reúne arquivos relacionados ao domínio de oncologia. Nesta primeira entrega, o grupo ainda não utilizou as tabelas de eventos clínicos ou diagnósticos, mas sim o arquivo de metadados do conjunto, que descreve os arquivos disponíveis, datas de extração, quantidade de registros e volume armazenado.

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
- Leitura do arquivo CSV configurado em config/project.yaml
- Validação da existência do arquivo antes do processamento
- Carregamento da base em DataFrame com pandas

### Transformação
As transformações implementadas em pandas foram planejadas para padronizar os dados e gerar indicadores iniciais para o dashboard:

- Renomeação das colunas principais para um padrão de análise
- Conversão da coluna de data para formato datetime
- Conversão das colunas numericas de registros e tamanho
- Identificação do nome base do arquivo sem extensão
- Derivação da camada do dado: raw, silver ou gold
- Derivação do domínio do arquivo
- Identificação do formato do arquivo
- Classificação do porte do arquivo com base no tamanho em MiB
- Cálculo do indicador registros_por_mib
- Criação das colunas de ano e mês de extração
- Ordenação dos registros pelo maior volume de registros

### Carga
- Exportação da base tratada para CSV em data/processed/onco360_metadata_tratado.csv
- Gravação da base tratada no banco SQLite em database/onco360_metadata.db
- Gravação de uma tabela resumo agregada por formato e porte do arquivo

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
- Quantidade de arquivos no painel
- Total de registros
- Tamanho total armazenado em MiB
- Data da última extração dísponivel

### Indicadores derivados
- Porte do arquivo
- Formato do arquivo
- Registros por MiB
- Distribuição por camada e domínio

### Visualizações previstas e implementadas
- Gráfico de barras horizontal com os 10 arquivos de maior volume de registros
- Gráfico de dispersão relacionando tamanho do arquivo e número de registros
- Tabela resumo agregada por formato e porte
- Tabela detalhada da base tratada com filtros

### Filtros disponíveis
- Filtro por formato do arquivo
- Filtro por porte do arquivo
- Campo para alterar o caminho do arquivo CSV de origem
- Botao para reexecutar o ETL diretamente pela interface

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

</details>
