from datetime import datetime
from pyegeria import Platform
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator


# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="demo-e", start_date=datetime(2024, 8, 19), schedule="0 0 * * *") as dag:

    # Tasks are represented as operators
    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task()
    def origin():
        p = Platform("active-metadata-store","https://host.docker.internal:9443","garygeeke")
        print(p.get_platform_origin())
    # Set dependencies between tasks
    hello >> origin()