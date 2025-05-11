from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import include.pipeline_tasks as tasks


# Define dbt project directory
dbt_project_directory = "/usr/local/airflow/dbt"

# Load Snowflake credentials
creds = Variable.get("snowflake", deserialize_json=True)

# Build env vars for dbt
env_vars = {
    "CSV_DATA_URL": creds["CSV_DATA_URL"],
    "SF_ACCOUNT": creds["SF_ACCOUNT"],
    "SF_USER": creds["SF_USER"],
    "SF_PASSWORD": creds["SF_PASSWORD"],
    "SF_SERVICE_USER_KEY": creds["SF_SERVICE_USER_KEY"],
    "SF_ROLE": creds["SF_ROLE"],
    "SF_WAREHOUSE": creds["SF_WAREHOUSE"],
    "SF_DATABASE": creds["SF_DATABASE"],
    "SF_SCHEMA": creds["SF_SCHEMA"],
    "SF_RAW_SCHEMA": creds["SF_RAW_SCHEMA"],
    "SF_RAW_DB_TABLE": creds["SF_RAW_DB_TABLE"],
    "DBT_LOG_PATH": f"{dbt_project_directory}/logs",
    "DBT_TARGET_PATH": f"{dbt_project_directory}/target"
}

# Airflow template variables
TEMPLATE_VARS = [
    "data_interval_start",
    "data_interval_end",
    "ds",
    "ds_nodash",
    "ts",
    "ts_nodash_with_tz",
    "ts_nodash",
    "prev_data_interval_start_success",
    "prev_data_interval_end_success",
    "prev_start_date_success",
]
env_vars.update({var: "{{ " + var + " }}" for var in TEMPLATE_VARS})


@dag(
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["dbt", "snowflake", "pipeline"],
    description="Load customer orders from CSV and run dbt models"
)
def customer_orders_dag():
    def load():
        df = tasks.download_csv(env_vars['CSV_DATA_URL'])
        
        conn = tasks.create_snowflake_connection(env_vars)
        tasks.load_to_snowflake(env_vars, df, conn)

    def run_dbt():
        tasks.run_dbt(dbt_project_directory, env_vars)

    load_task = PythonOperator(task_id="load_data", python_callable=load)
    dbt_task = PythonOperator(task_id="run_dbt", python_callable=run_dbt)
    
    load_task >> dbt_task

dag = customer_orders_dag()
