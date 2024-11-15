"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.


This script updates the configuration of the active-metadata-store to use postgres and restarts the server.

"""
import argparse
import json
import os
import sys

from click import password_option
from pyegeria import EgeriaConfig, CoreServerConfig, EgeriaTech
from rich.prompt import Prompt


from pyegeria import (
    InvalidParameterException,
    PropertyServerException,
    UserNotAuthorizedException,
    Client,
    ClassificationManager,
)


EGERIA_METADATA_STORE = os.environ.get("EGERIA_METADATA_STORE", "active-metadata-store")
EGERIA_KAFKA_ENDPOINT = os.environ.get("KAFKA_ENDPOINT", "localhost:9092")
EGERIA_PLATFORM_URL = os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443")
EGERIA_VIEW_SERVER = os.environ.get("VIEW_SERVER", "view-server")
EGERIA_VIEW_SERVER_URL = os.environ.get(
    "EGERIA_VIEW_SERVER_URL", "https://localhost:9443"
)
EGERIA_INTEGRATION_DAEMON = os.environ.get("INTEGRATION_DAEMON", "integration-daemon")
EGERIA_ADMIN_USER = os.environ.get("ADMIN_USER", "garygeeke")
EGERIA_ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "secret")
EGERIA_USER = os.environ.get("EGERIA_USER", "erinoverview")
EGERIA_USER_PASSWORD = os.environ.get("EGERIA_USER_PASSWORD", "secret")

def update_server_repository(server_name: str = EGERIA_METADATA_STORE,
                             platform_url:str = EGERIA_PLATFORM_URL,
                             user_id:str = EGERIA_ADMIN_USER,
                             password: str = EGERIA_ADMIN_PASSWORD):


    o_client = EgeriaConfig(
        server_name, platform_url, user_id, password
        )
    o_client.set_xtdb_local_kv_repository()
    o_client.activate_server_stored_config(server_name)
    print(f"Server {server_name} should now be set to the XTDB KV repository")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="Name of the server to update")
    parser.add_argument("--url", help="URL Platform to connect to")
    parser.add_argument("--userid", help="User Id")
    parser.add_argument("--password", help="User Password")

    args = parser.parse_args()

    server = args.server if args.server is not None else EGERIA_METADATA_STORE
    url = args.url if args.url is not None else EGERIA_VIEW_SERVER_URL
    userid = args.userid if args.userid is not None else EGERIA_USER
    user_pass = args.password if args.password is not None else EGERIA_USER_PASSWORD

    try:
        update_server_repository(server, url, userid, user_pass)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

