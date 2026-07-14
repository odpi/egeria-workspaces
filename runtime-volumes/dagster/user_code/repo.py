import os
from dagster import asset, Definitions, job, op, get_dagster_logger
from dagster_openlineage import openlineage_sensor

# Initialize standard Dagster logger
logger = get_dagster_logger()

@asset
def sample_egeria_asset():
    """
    A sample asset indicating Dagster is running and connected.
    You can map this asset to metadata in Egeria using Pyegeria.
    """
    logger.info("Running sample_egeria_asset materialization...")
    # This list represents databases or resources surveyed
    datasets = ["postgres_coco_pharma", "kafka_shared_topics", "unity_catalog_tables"]
    
    # Example of utilizing pyegeria within the asset
    try:
        from pyegeria import EgeriaRuntime
        logger.info("Successfully imported pyegeria library.")
        # In a real pipeline, you could connect to Egeria here:
        # egeria = EgeriaRuntime("https://localhost:9443")
    except ImportError:
        logger.warning("pyegeria library not available in Python environment.")

    return datasets

@op
def run_resource_survey():
    """
    An operation to profile/survey a specific resource.
    """
    logger.info("Surveying resource: coco_pharma_db")
    return "Survey results for coco_pharma_db: Clean"

@job
def egeria_survey_job():
    """
    Job that runs a dynamic survey operation.
    """
    run_resource_survey()

# Definitions object that Dagster loads
defs = Definitions(
    assets=[sample_egeria_asset],
    jobs=[egeria_survey_job],
    sensors=[
        # Sensor that listens to asset/job events and publishes OpenLineage metadata.
        # This will auto-route to the target set in the OPENLINEAGE_URL environment variable.
        openlineage_sensor(include_asset_events=True)
    ]
)
