from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "vehicleops",
    "retries": 1,
}

dag = DAG(
    dag_id="vehicleops_pipeline",
    default_args=default_args,
    description="A simple fleet data pipeline for vehicle operations",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
)

generate_data = BashOperator(
    task_id="generate_data",
    bash_command="python /opt/airflow/scripts/generate_data.py",
    dag=dag,
)

validate_raw_data = BashOperator(
    task_id="validate_raw_data",
    bash_command="python /opt/airflow/scripts/validate_raw_data.py",
    dag=dag,
)

load_raw_data = BashOperator(
    task_id="load_raw_data",
    bash_command="python /opt/airflow/scripts/load_raw_data.py",
    dag=dag,
)

generate_data >> validate_raw_data >> load_raw_data