import os
import psycopg2
from prefect import flow, task, get_run_logger
from rich.console import Console
from rich.table import Table

@task(name="Get Databases")
def get_databases(host: str, port: str, user: str, password_env: str):
    logger = get_run_logger()
    logger.info(f"Connecting to master database at {host}:{port}...")
    
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password_env,
        database="postgres"
    )
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            dbs = [row[0] for row in cur.fetchall()]
            logger.info(f"Found databases: {dbs}")
            return dbs
    finally:
        conn.close()

@task(name="Get Schema and Tables")
def get_database_schema(db_name: str, host: str, port: str, user: str, password_env: str):
    logger = get_run_logger()
    logger.info(f"Connecting to database '{db_name}' to retrieve schema...")
    
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password_env,
            database=db_name
        )
        try:
            with conn.cursor() as cur:
                # Query tables and their schemas, excluding system schemas
                query = """
                SELECT table_schema, table_name 
                FROM information_schema.tables 
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
                ORDER BY table_schema, table_name;
                """
                cur.execute(query)
                rows = cur.fetchall()
                logger.info(f"Retrieved {len(rows)} tables/views in database '{db_name}'")
                return [{"schema": row[0], "table": row[1]} for row in rows]
        finally:
            conn.close()
    except Exception as e:
        logger.error(f"Failed to query database '{db_name}': {e}")
        return []

@flow(name="PostgreSQL Schema Inspector")
def postgres_schema_flow(
    host: str = "egeria-shared-postgres",
    port: str = "5442",
    user: str = "postgres",
    password: str = "egeria"
):
    logger = get_run_logger()
    logger.info("Starting PostgreSQL Schema Inspector flow...")
    
    # 1. Fetch all databases
    databases = get_databases(host, port, user, password)
    
    # 2. Iterate through each database and get schema details
    results = {}
    for db in databases:
        results[db] = get_database_schema(db, host, port, user, password)
        
    # 3. Print a beautiful summary table
    console = Console(record=True)
    table = Table(title="PostgreSQL Databases & Schema Catalog")
    table.add_column("Database", style="cyan", no_wrap=True)
    table.add_column("Schema", style="magenta")
    table.add_column("Table/View", style="green")
    
    for db, schema_list in results.items():
        if not schema_list:
            table.add_row(db, "[italic red]No tables or permissions[/italic red]", "")
        else:
            for item in schema_list:
                table.add_row(db, item["schema"], item["table"])
                
    with console.capture() as capture:
        console.print(table)
    logger.info("\n" + capture.get())
    logger.info("PostgreSQL Schema Inspector completed successfully.")
    return results

if __name__ == "__main__":
    # If run locally outside Docker, default to host localhost:5442
    postgres_schema_flow(host="localhost")
