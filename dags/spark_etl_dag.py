from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import os
import logging
import sys

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

def run_etl_script():
    project_dir = Variable.get("PROJECT_DIR")

    if not project_dir:
        raise EnvironmentError("❌ PROJECT_DIR Airflow Variable not set.")

    script_path = os.path.join(project_dir, "scripts", "spark_transform.py")

    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"❌ ETL script not found at: {script_path}")

    logging.info(f"✅ Running ETL script: {script_path}")
    subprocess.run([sys.executable, script_path], check=True)

with DAG(
    dag_id="etl_spark_transform",
    description="An ETL pipeline that transforms dialysis data using Spark and loads into PostgreSQL.",
    default_args=default_args,
    schedule_interval="@weekly",
    catchup=False,
    tags=["etl", "spark", "postgres"],
    max_active_runs=1,
) as dag:
    run_etl = PythonOperator(
        task_id="run_etl_spark_transform",
        python_callable=run_etl_script,
        execution_timeout=timedelta(minutes=10),
        retry_exponential_backoff=True,
    )
