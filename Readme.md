
# NYC Mobility Analytics

Projeto de Engenharia de Dados que implementa um pipeline de ponta a ponta para processar e analisar dados das corridas de táxis amarelos de Nova York (*NYC Yellow Taxi*), referentes a janeiro de 2024.

O projeto integra Python, PostgreSQL, dbt, Apache Airflow e Power BI, abrangendo desde a ingestão dos dados brutos até a disponibilização de indicadores em um dashboard analítico.

## Objetivo

Construir um pipeline de dados que automatiza a ingestão, o armazenamento, a transformação e a validação dos dados, disponibilizando informações analíticas para explorar o comportamento das corridas de táxi em Nova York.

## Tecnologias

- **Python:** download, exploração e carregamento dos dados.
- **PostgreSQL:** armazenamento dos dados brutos e dos modelos analíticos.
- **dbt:** transformação, modelagem e testes de qualidade dos dados.
- **Apache Airflow:** orquestração das etapas do pipeline.
- **Power BI:** visualização dos indicadores e análise das corridas.
- **Git e GitHub:** versionamento e disponibilização do projeto.

## Arquitetura

```text
NYC TLC (Parquet)
        |
        v
      Python
        |
        v
 PostgreSQL (RAW)
        |
        v
       dbt
        |
        +-- Staging
        |
        +-- Intermediate
        |
        +-- Marts
        |
        v
     Power BI
```

O Apache Airflow orquestra o download dos dados, o carregamento no PostgreSQL e a execução dos modelos e testes do dbt.

O Power BI consome as tabelas analíticas produzidas pelo dbt.

## Dataset

- **Fonte:** NYC Taxi & Limousine Commission (TLC)
- **Dataset:** Yellow Taxi Trip Records
- **Período:** janeiro de 2024
- **Formato original:** Parquet
- **Volume original:** 2.964.624 registros

Fonte oficial: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Arquivo utilizado:

```text
yellow_tripdata_2024-01.parquet
```

O script de ingestão baixa o arquivo oficial e o armazena em `data/raw/`.

## Dashboard

O dashboard foi desenvolvido no Power BI para analisar os principais indicadores das corridas de táxi de Nova York.

As análises incluem:

- Volume total de corridas.
- Receita total em dólares americanos (USD).
- Distância média das viagens.
- Duração média das viagens.
- Evolução diária do volume de corridas e da receita.
- Distribuição das corridas por horário.
- Distribuição por forma de pagamento.

O arquivo do dashboard está disponível em:

```text
powerbi/nyc_mobility_dashboard.pbix
```

A versão final do design e as capturas de tela serão adicionadas posteriormente.

**Observação:** o Power BI Desktop consome as tabelas analíticas do PostgreSQL. A atualização do dashboard é realizada separadamente e não faz parte da DAG do Airflow.

## Modelagem de dados com dbt

O projeto utiliza o dbt para transformar os dados brutos em tabelas analíticas, seguindo uma arquitetura de três camadas: Staging, Intermediate e Marts.

### Staging

**`stg_yellow_trips`**

Prepara os dados provenientes da tabela `raw.yellow_trips`, padronizando os campos utilizados nas etapas seguintes.

Materialização: `view`.

### Intermediate

**`int_yellow_trips`**

Aplica as transformações intermediárias e calcula métricas utilizadas nas análises das viagens.

Materialização: `view`.

### Marts

**`mart_yellow_trips`**

Disponibiliza os dados detalhados das viagens, incluindo duração, velocidade média, horário da corrida, forma de pagamento e indicadores de qualidade.

Materialização: `table`.

**`mart_daily_trips`**

Agrega os dados por dia, calculando o total de corridas, a receita válida, a distância média e a duração média.

Materialização: `table`.

A tabela `mart_yellow_trips` contém 2.963.754 registros após as transformações aplicadas pelo projeto.

## Qualidade dos dados

O pipeline executa 11 testes automatizados com dbt para validar os modelos e verificar a qualidade dos dados.

Os testes incluem verificações de valores nulos em campos importantes e unicidade do identificador das viagens na tabela analítica.

**Resultado validado durante o desenvolvimento:**

```text
4 modelos executados
11 testes aprovados

PASS=15
WARN=0
ERROR=0
SKIP=0
```

Os resultados correspondem à execução completa do `dbt build`, incluindo os modelos e os testes.

## Orquestração com Apache Airflow

O Apache Airflow é responsável por orquestrar as etapas do pipeline por meio da DAG `nyc_mobility_pipeline`.

A DAG executa três tarefas sequenciais:

1. **`download_data`:** executa `python/download_data.py` para baixar o arquivo Parquet oficial da NYC TLC, caso ele ainda não exista localmente.
2. **`load_postgres`:** executa `python/load_raw.py` para carregar os dados na tabela `raw.yellow_trips`, evitando recarregamentos desnecessários.
3. **`run_dbt`:** executa `dbt build` para construir os modelos de staging, intermediate e marts, além dos testes de qualidade.

### Fluxo de execução

```text
download_data
      |
      v
load_postgres
      |
      v
   run_dbt
```

A DAG utiliza execução manual (`schedule=None`), permitindo iniciar o pipeline pela interface do Airflow.

O diretório raiz do projeto é identificado dinamicamente a partir da localização do arquivo da DAG, evitando a necessidade de configurar um caminho absoluto específico para cada usuário.

Os ambientes virtuais do Airflow e do dbt devem estar localizados nas pastas `airflow/.venv` e `dbt/.venv`, respectivamente.

## Como executar o projeto

As instruções a seguir consideram um ambiente Windows com WSL2 (Ubuntu), PostgreSQL instalado no Windows e Python, dbt e Airflow executados no Ubuntu.

### 1. Pré-requisitos

- Python 3.12
- PostgreSQL
- WSL2 com Ubuntu
- Git
- Power BI Desktop, caso queira abrir o dashboard

É necessário ter o PostgreSQL em execução e permitir conexões a partir do ambiente WSL2.

### 2. Clonando o repositório

No terminal do Ubuntu:

```bash
git clone https://github.com/RayranTech/nyc-mobility-analytics.git

cd nyc-mobility-analytics
```

### 3. Configurando o PostgreSQL

Crie um banco de dados chamado `nyc_mobility` no PostgreSQL:

```sql
CREATE DATABASE nyc_mobility;
```

O comando deve ser executado conectado a outro banco, como `postgres`, por meio do pgAdmin ou do `psql`.

Certifique-se de que o usuário configurado tenha permissão para criar tabelas e schemas no banco `nyc_mobility`.

### 4. Configurando as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as credenciais do PostgreSQL:

```dotenv
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=nyc_mobility
```

Substitua os valores de exemplo pelas credenciais do seu ambiente.

**Importante:** o arquivo `.env` contém credenciais locais e não deve ser enviado ao GitHub.

Como o PostgreSQL está instalado no Windows, a conexão a partir do WSL2 pode exigir o endereço IP do host Windows em vez de `localhost`.

Nos comandos de execução deste README, esse endereço é obtido automaticamente quando necessário.

### 5. Instalando o dbt

Na raiz do projeto, crie e ative um ambiente virtual exclusivo para o dbt:

```bash
python3 -m venv dbt/.venv

source dbt/.venv/bin/activate
```

Instale o dbt com o adaptador PostgreSQL:

```bash
pip install dbt-postgres
```

Instale as dependências do projeto dbt:

```bash
dbt deps \
  --project-dir dbt/nyc_mobility \
  --profiles-dir dbt/profiles
```

Desative o ambiente virtual:

```bash
deactivate
```

### 6. Instalando o Apache Airflow

Na raiz do projeto, crie e ative um ambiente virtual exclusivo para o Airflow:

```bash
python3 -m venv airflow/.venv

source airflow/.venv/bin/activate
```

Instale o Apache Airflow 3.0.6 utilizando o arquivo de restrições correspondente à versão do Python:

```bash
AIRFLOW_VERSION=3.0.6

PYTHON_VERSION=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')

pip install "apache-airflow==${AIRFLOW_VERSION}" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
```

Instale também as bibliotecas utilizadas pelos scripts Python de ingestão e carregamento:

```bash
pip install pandas pyarrow sqlalchemy psycopg2-binary python-dotenv requests
```

Configure o diretório do Airflow:

```bash
export AIRFLOW_HOME="$HOME/airflow"

mkdir -p "$AIRFLOW_HOME/dags"
```

Crie um link simbólico para disponibilizar a DAG do projeto ao Airflow:

```bash
ln -s "$(pwd)/airflow/dags" \
  "$AIRFLOW_HOME/dags/nyc-mobility-analytics"
```

O link simbólico permite que o Airflow encontre a DAG armazenada no repositório sem precisar duplicar seus arquivos.

Desative o ambiente virtual:

```bash
deactivate
```

### 7. Executando o dbt separadamente

O dbt pode ser executado separadamente para reconstruir os modelos analíticos e validar os dados.

**Importante:** antes de executar o dbt, o PostgreSQL deve conter a tabela `raw.yellow_trips`, criada pelo script `python/load_raw.py` ou pela execução completa da DAG do Airflow.

Com o PostgreSQL em execução, carregue as variáveis de ambiente:

```bash
set -a
source .env
set +a
```

Se o PostgreSQL estiver instalado no Windows e o dbt for executado pelo WSL2, configure o endereço do host:

```bash
export POSTGRES_HOST=$(ip route show default | awk '{print $3}')
```

Execute os modelos e os testes:

```bash
dbt/.venv/bin/dbt build \
  --project-dir dbt/nyc_mobility \
  --profiles-dir dbt/profiles
```

O comando `dbt build` executa as transformações e os testes de qualidade definidos no projeto.

### 8. Executando o Apache Airflow

Com o PostgreSQL em execução e os ambientes virtuais configurados, inicie o Airflow pelo terminal do WSL2:

```bash
airflow/.venv/bin/airflow standalone
```

Acesse a interface web:

http://localhost:8080

Na interface do Airflow, localize a DAG `nyc_mobility_pipeline` e inicie uma execução manual.

O pipeline executará as seguintes etapas, nesta ordem:

1. Download do arquivo Parquet da NYC TLC.
2. Carregamento dos dados na tabela `raw.yellow_trips` do PostgreSQL.
3. Execução dos modelos e testes do dbt.

O pipeline foi desenvolvido para evitar downloads e carregamentos desnecessários quando os dados já estão disponíveis localmente.

### 9. Testando a DAG pelo terminal

Também é possível executar um teste da DAG sem iniciar a interface web do Airflow.

Com o Airflow standalone desligado, execute:

```bash
airflow/.venv/bin/airflow dags test nyc_mobility_pipeline 2026-09-22
```

O comando executa as três tarefas da DAG e apresenta o resultado no terminal.

**Resultado validado durante o desenvolvimento:** as três tarefas foram concluídas com sucesso, incluindo a construção dos quatro modelos e a aprovação dos 11 testes do dbt.

## Limitações e possíveis melhorias

Este projeto foi desenvolvido como um estudo prático de Engenharia de Dados e apresenta algumas limitações:

- O dataset utilizado corresponde apenas a janeiro de 2024.
- A DAG é executada manualmente, sem agendamento periódico.
- O pipeline foi configurado e validado em um ambiente local com Windows e WSL2.
- A atualização do Power BI Desktop não é automatizada pelo Airflow.

Possíveis evoluções incluem processamento de múltiplos meses, execução agendada, melhorias na observabilidade e implantação em ambiente de nuvem.

## Fonte dos dados

Os dados utilizados neste projeto são disponibilizados publicamente pela NYC Taxi & Limousine Commission (TLC).

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
