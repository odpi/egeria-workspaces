#!/usr/bin/env python3
"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

A simple UC catalog viewer using the RICH textual interface.


"""
import argparse
import time

from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.text import Text
from rich.live import Live


from unitycatalog import Unitycatalog
from unitycatalog.types import (catalog_info, catalog_list_response,
                                schema_info, schema_list_response,
                                volume_info, volume_list_response,
                                )


def display_catalog(url:str = "http://egeria.pdr-associates.com:8070"):
    base_url = url + "/api/2.1/unity-catalog"
    uc_client = Unitycatalog(base_url=base_url)

    def generate_table() -> Table:
        """Make a new table."""
        table = Table(
            title=f"UC OSS Catalog @ {time.asctime()}",
            header_style="white on dark_blue",
            show_lines=True,
            box=box.ROUNDED,
            caption=f"Running on {url}",
            expand=True
        )
        table.add_column("Catalog Name")
        table.add_column("Catalog Comment")
        table.add_column("Schema Name")
        table.add_column("Schema Comment")
        table.add_column("Vol/Tab")
        table.add_column("Details")

        c_list = uc_client.catalogs.list()
        catalogs= c_list.catalogs
        for catalog in catalogs:
            # cat_info = catalog.CatalogInfo
            cat_name = catalog.name
            cat_comment = catalog.comment

            s_list = uc_client.schemas.list(catalog_name = cat_name)
            schemas = s_list.schemas
            for schema in schemas:
                schema_name = schema.name
                schema_comment = schema.comment
                v_list = uc_client.volumes.list(catalog_name = cat_name, schema_name = schema_name)
                volumes = v_list.volumes
                volume_md = " "
                volumes_m = "Volumes"
                volume_m = " "
                tab_list = uc_client.tables.list(catalog_name = cat_name, schema_name = schema_name)
                tables = tab_list.tables
                tables_m = "Tables"

                func_list = uc_client.functions.list(catalog_name = cat_name, schema_name = schema_name)
                functions = func_list.functions
                if (functions is not None) and (len(functions) > 0):
                    function_m = "Functions"
                    for function in functions:
                        function_name = function.name
                        function_comment = function.comment
                        function_sql = function.sql_data_access
                        function_id = function.function_id
                        function_type = function.full_data_type
                        function_m = (f"{function_m}\n* name: {function_name}\n"
                                      f"\t* comment: {function_comment}\n"  
                                      f"\t* function_id: {function_id}\n"
                                      f"\t* function_type: {function_type}\n"
                                      f"\t* sql_access: {function_sql}\n")
                        table.add_row(cat_name, cat_comment, schema_name, schema_comment, Text(function_m))
                if (volumes is not None) and (len(volumes) > 0):
                    for volume in volumes:
                        volume_name = volume.name
                        volume_comment = volume.comment
                        volume_created_at = volume.created_at
                        volume_updated_at = volume.updated_at
                        volume_id = volume.volume_id
                        volume_type = volume.volume_type
                        volume_storage_location = volume.storage_location
                        volume_m = (f"{volume_m}\n* name: {volume_name}\n"
                                    f"\t* comment: {volume_comment}\n"
                                    f"\t* created_at: {volume_created_at}\n"
                                    f"\t* updated_at: {volume_updated_at}\n"
                                    f"\t* volume_id: {volume_id}\n"
                                    f"\t* volume_type: {volume_type}\n"
                                    f"\t* storage_location: {volume_storage_location}\n")
                    volumes_m = f"{volumes_m}\n{volume_m}"
                    table.add_row(cat_name, cat_comment, schema_name, schema_comment, Text(volumes_m))
                tab_m = " "
                if (tables is not None) and (len(tables) > 0):
                    for tab in tables:
                        tab_name = tab.name
                        tab_comment = tab.comment
                        tab_created_at = tab.created_at

                        tab_src_format = tab.data_source_format
                        tab_id = tab.table_id
                        tab_type = tab.table_type
                        tab_updated_at = tab.updated_at
                        columns = tab.columns
                        col_m = " "
                        col_tab = Table()
                        col_tab.add_column("name")
                        col_tab.add_column("type")
                        col_tab.add_column("nullable")
                        col_tab.add_column("comment")

                        for col in columns:
                            col_nullable = "true" if col.nullable else "false"
                            col_tab.add_row(col.name, col.type_text, col_nullable, col.comment)

                        table_m = (f"{tab_m}\n* name: {tab_name}\n"
                                   f"\t* comment: {tab_comment}\n"
                                   f"\t* created_at: {tab_created_at}\n"
                                   f"\t* updated_at: {tab_updated_at}\n"
                                   f"\t* table_id: {tab_id}\n"
                                   f"\t* table_type: {tab_type}\n"
                                   f"\t* src_format: {tab_src_format}\n"
                                   )

                    tables_m = f"{tables_m}\n{table_m}"
                    table.add_row(cat_name, cat_comment, schema_name, schema_comment, Text(tables_m), col_tab)
                fcn_m = " "



        return table

    try:
        console = Console(width=200)
        with console.pager():
            console.print(generate_table())

    except Exception as e:
        print()
        console.print_exception()

    finally:
        uc_client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="Name of the server to display status for")
    parser.add_argument("--url", help="URL Platform to connect to")
    parser.add_argument("--userid", help="User Id")
    args = parser.parse_args()

    server = args.server if args.server is not None else "engine-host"
    url = args.url if args.url is not None else "http://localhost:8080"
    userid = args.userid if args.userid is not None else 'garygeeke'
    display_catalog(url)
