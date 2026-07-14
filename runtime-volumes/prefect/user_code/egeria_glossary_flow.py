import os
import pyegeria
from prefect import flow, task, get_run_logger
from pyegeria import GlossaryManager
from rich.console import Console
from rich.table import Table

# Disable SSL verification for self-signed certificates in local quickstart
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True

@task(name="Fetch Egeria Glossaries")
def fetch_glossaries(platform_url: str, view_server: str, user_id: str, user_pwd: str):
    logger = get_run_logger()
    logger.info(f"Connecting to Egeria OMAG Platform at {platform_url} via {view_server}...")
    
    try:
        # Initialize GlossaryManager
        mgr = GlossaryManager(
            view_server=view_server,
            platform_url=platform_url,
            user_id=user_id,
            user_pwd=user_pwd
        )
        
        # Create token
        mgr.create_egeria_bearer_token()
        logger.info("Successfully authenticated with Egeria OMAG Platform.")
        
        # Fetch glossaries using the standard search
        raw_glossaries = mgr.find_glossaries(
            search_string="*",
            starts_with=True,
            output_format="JSON"
        )
        
        logger.info(f"Retrieved {len(raw_glossaries) if raw_glossaries else 0} glossaries.")
        return raw_glossaries if raw_glossaries else []
    except Exception as e:
        logger.error(f"Failed to fetch glossaries from Egeria: {e}")
        return []

@flow(name="Egeria Glossary Inspector")
def egeria_glossary_flow(
    platform_url: str = "https://host.docker.internal:9443",
    view_server: str = "qs-view-server",
    user_id: str = "erinoverview",
    user_password: str = "secret"
):
    logger = get_run_logger()
    logger.info("Starting Egeria Glossary Inspector flow...")
    
    # 1. Fetch Glossaries
    glossaries = fetch_glossaries(platform_url, view_server, user_id, user_password)
    
    # 2. Print Summary Table
    console = Console(record=True)
    table = Table(title="Egeria Active Glossaries")
    table.add_column("Glossary Name", style="cyan", no_wrap=True)
    table.add_column("GUID", style="magenta")
    table.add_column("Qualified Name", style="green")
    table.add_column("Description", style="white")

    if not glossaries:
        table.add_row("[italic red]No glossaries found or platform unreachable[/italic red]", "", "", "")
    else:
        for gloss in glossaries:
            # Handle structure of returned elements
            if isinstance(gloss, dict):
                props = gloss.get("properties") or {}
                header = gloss.get("elementHeader") or {}
                name = props.get("displayName") or props.get("name") or "Unnamed"
                guid = header.get("guid") or "N/A"
                qname = props.get("qualifiedName") or "N/A"
                desc = props.get("description") or ""
            else:
                name = getattr(gloss, "displayName", None) or getattr(gloss, "name", "Unnamed")
                guid = getattr(gloss, "guid", "N/A")
                qname = getattr(gloss, "qualifiedName", "N/A")
                desc = getattr(gloss, "description", "")
            
            table.add_row(name, guid, qname, desc)
            
    console.print(table)
    logger.info("Egeria Glossary Inspector completed successfully.")
    return glossaries

if __name__ == "__main__":
    # If run locally outside Docker, default to host localhost:9443
    egeria_glossary_flow(platform_url="https://localhost:9443")
