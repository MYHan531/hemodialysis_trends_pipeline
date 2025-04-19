from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
import os
import logging

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

def run_etl_script():
    project_dir = os.getenv("PROJECT_DIR")

    if not project_dir:
        raise EnvironmentError("❌ PROJECT_DIR environment variable not set.")

    script_path = os.path.join(project_dir, "scripts", "spark_transform.py")

    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"❌ ETL script not found at: {script_path}")

    logging.info(f"✅ Running ETL script: {script_path}")
    subprocess.run(["python", script_path], check=True)

with DAG(
    dag_id="etl_spark_transform",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["etl", "spark", "postgres"],
) as dag:
    run_etl = PythonOperator(
        task_id="run_etl_spark_transform",
        python_callable=run_etl_script
    )
