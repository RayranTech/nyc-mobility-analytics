from pathlib import Path
from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


PROJECT_DIR = Path(__file__).resolve().parents[2]

with DAG(
    dag_id="nyc_mobility_pipeline",
    description="Pipeline de dados NYC Mobility Analytics",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["nyc", "data-engineering"],
) as dag:

    download_data = BashOperator(
        task_id="download_data",
        bash_command=f"""
            set -e
            cd {PROJECT_DIR}
            {PROJECT_DIR}/airflow/.venv/bin/python python/download_data.py
        """,
    )

    load_postgres = BashOperator(
        task_id="load_postgres",
        bash_command=f"""
            cd {PROJECT_DIR}
            export POSTGRES_HOST=$(ip route show default | awk '{{print $3}}')
            {PROJECT_DIR}/airflow/.venv/bin/python python/load_raw.py
        """,
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command=f"""
            set -e
            cd {PROJECT_DIR}

            set -a
            source .env
            set +a

            export POSTGRES_HOST=$(ip route show default | awk '{{print $3}}')

            {PROJECT_DIR}/dbt/.venv/bin/dbt build \
                --project-dir {PROJECT_DIR}/dbt/nyc_mobility \
                --profiles-dir {PROJECT_DIR}/dbt/profiles
        """,
    )

    download_data >> load_postgres >> run_dbt
