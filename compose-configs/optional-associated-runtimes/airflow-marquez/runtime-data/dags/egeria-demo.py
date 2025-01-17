import json
from datetime import datetime, timedelta
import logging
from json5 import host
from pyegeria import EgeriaTech, Platform
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

from unitycatalog import Unitycatalog
from unitycatalog.types import (catalog_info, catalog_list_response,
                                schema_info, schema_list_response,
                                volume_info, volume_list_response,
                                )

# A DAG represents a workflow, a collection of tasks
with DAG(
        "egeria-1",
        default_args={
            "owner": "airflow",
            "depends_on_past": False,
            "email": ["dan.wolfson@pdr-associates.com"],
            "email_on_failure": False,
            "email_on_retry": False,
            "retries": 1,
            "retry_delay": timedelta(minutes=5),
            },
        description = "An Egeria/UC Demo Dag",
        start_date=datetime.now(),
        schedule=timedelta(minutes=5),
        catchup=False,
        tags=["egeria"],
        ) as dag:

    # Tasks are represented as operators
    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task()
    def get_server_info():
        # p = Platform("active-metadata-store","https://host.docker.internal:9443","garygeeke")
        # print(p.get_platform_origin())
        logger = logging.getLogger("egeria-demo-task")
        r_client = EgeriaTech(
            'view-server',
            'https://host.docker.internal:9443',
            'garygeeke',
            "secret"
            )
        token = r_client.create_egeria_bearer_token()
        filter = "simple-metadata-store"
        response = r_client.get_servers_by_name(filter)
        logger.info(f"Servers:\n{json.dumps(response, indent=4)}")


    @task()
    def list_catalogs():
        # url = "http://egeria.pdr-associates.com:8070"
        url = "http://host.docker.internal:8081"
        base_url = url + "/api/2.1/unity-catalog"
        uc_client = Unitycatalog(base_url=base_url, )
        c_list = uc_client.catalogs.list()
        catalogs = c_list.catalogs
        for catalog in catalogs:
            print(catalog.name)
    # Set dependencies between tasks
    hello >> get_server_info() >> list_catalogs()