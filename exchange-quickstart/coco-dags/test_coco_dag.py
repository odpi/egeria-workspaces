from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello_coco():
    print("Hello from COCO DAGs!")

with DAG(
    dag_id='test_coco_bundle_dag',
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=['coco'],
) as dag:
    task1 = PythonOperator(
        task_id='hello_task',
        python_callable=hello_coco,
    )
