from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="test_nyc_mobility",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    test_task = BashOperator(
        task_id="test_task",
        bash_command="echo 'NYC Mobility Analytics - Airflow funcionando!'",
    )

