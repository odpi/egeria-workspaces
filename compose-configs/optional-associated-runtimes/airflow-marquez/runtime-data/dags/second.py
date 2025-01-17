from datetime import datetime
from pyegeria import Platform
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from unitycatalog import Unitycatalog
from unitycatalog.types import (catalog_info, catalog_list_response,
                                schema_info, schema_list_response,
                                volume_info, volume_list_response,
                                )

# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="demo-u", start_date=datetime(2024, 8, 19), schedule="0 0 * * *") as dag:

    # Tasks are represented as operators
    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task()
    def origin():
        p = Platform("active-metadata-store","https://laz.local:9443","garygeeke")
        print(p.get_platform_origin())
    @task()
    def list_catalogs():
        url = "http://egeria.pdr-associates.com:8070"
        base_url = url + "/api/2.1/unity-catalog"
        uc_client = Unitycatalog(base_url=base_url, )
        c_list = uc_client.catalogs.list()
        catalogs = c_list.catalogs
        for catalog in catalogs:
            print(catalog.name)
    # Set dependencies between tasks
    hello >> origin() >> list_catalogs()