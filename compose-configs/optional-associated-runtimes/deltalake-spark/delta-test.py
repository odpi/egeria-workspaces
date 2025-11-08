from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import sys

# Enable verbose logging
import logging

logging.basicConfig(level=logging.INFO)

print("Creating Spark session...")
try:
    spark = (
        SparkSession.builder
        .appName("delta-local-mac")
        .config("spark.sql.extensions", "org.apache.spark.sql.delta.extensions.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.catalogImplementation", "hive")
        .config("spark.hadoop.hive.metastore.uris", "thrift://localhost:9083")
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0,org.apache.hadoop:hadoop-aws:3.3.4")
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:8200")
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin123")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        # Add these for better error messages
        .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse")
        .config("spark.driver.extraJavaOptions", "-Dlog4j.configuration=file:log4j.properties")
        .getOrCreate()
    )
    print("Spark session created successfully!")
    print(f"Spark version: {spark.version}")
except Exception as e:
    print(f"Failed to create Spark session: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

# Test database creation with detailed error handling
print("\nTesting database creation...")
try:
    spark.sql("CREATE DATABASE IF NOT EXISTS demo")
    print("Database 'demo' created successfully!")
except Exception as e:
    print(f"Failed to create database: {e}")
    if hasattr(e, 'java_exception'):
        print(f"\nJava exception details:")
        print(e.java_exception)
    import traceback

    traceback.print_exc()
    sys.exit(1)

# Continue with other operations...
try:
    spark.sql("USE demo")
    print("Using database 'demo'")

    # Show databases
    print("\nAvailable databases:")
    spark.sql("SHOW DATABASES").show()

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()