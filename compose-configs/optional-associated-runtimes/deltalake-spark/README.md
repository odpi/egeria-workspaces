# Delta Lake + Spark + Hive Metastore + MinIO (Docker Compose)

This stack brings up a complete local Delta Lake environment:
- MinIO (S3-compatible) for object storage
- Hive Metastore (backed by the Postgres that runs in egeria-quickstart on host:5442)
- Spark 3.5.x (master + worker) pre-configured for Delta and S3A

It is designed so you can access it from:
- The egeria-quickstart Jupyter (running on host port 7888), or
- Local Python (PyCharm) on your Mac

## Prerequisites
- Ensure `egeria-quickstart` is running, specifically its Postgres on `127.0.0.1:5442`.
- Ensure Postgres has a database `hive_metastore` with user `egeria_admin` and password `admin4egeria`.
  - If you haven't created it yet, run:
    ```bash
    psql postgresql://postgres:egeria@localhost:5442/postgres -c "CREATE DATABASE hive_metastore; ALTER DATABASE hive_metastore OWNER TO egeria_admin; GRANT ALL PRIVILEGES ON DATABASE hive_metastore TO egeria_admin;"
    ```
- Download the Postgres JDBC driver jar once into `drivers/` next to this compose file:
  ```bash
  mkdir -p drivers
  curl -L -o drivers/postgresql-42.7.4.jar \
    https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar
  ```

## Files
- `.env` — MinIO credentials, default bucket, and Spark worker sizing
- `spark/conf/spark-defaults.conf` — Spark defaults enabling Delta + S3A + Hive Metastore
- `docker-compose.yml` — services for MinIO, Hive Metastore, Spark master/worker

## Start the stack
```bash
cd compose-configs/deltalake-spark
# first start will download images and jars
docker compose up -d
```

## Services & Ports
- MinIO Console: http://localhost:8201 (login: `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` from `.env`)
- MinIO S3 API: http://localhost:8200
- Spark Master UI: http://localhost:8080
- Spark Worker UI: http://localhost:8081
- Hive Metastore Thrift: thrift://localhost:9083

A default bucket `${S3_BUCKET}` (default `datalake`) is created automatically.

## Using from egeria-quickstart Jupyter (port 7888)
Create a Python notebook and run either a local Spark session or connect to the standalone master. Both work.

### Option A — Local Spark session inside the Jupyter container
```python
from pyspark.sql import SparkSession
spark = (
    SparkSession.builder
      .appName("delta-local")
      .config("spark.sql.extensions", "org.apache.spark.sql.delta.extensions.DeltaSparkSessionExtension")
      .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
      .config("spark.sql.catalogImplementation", "hive")
      .config("spark.hadoop.hive.metastore.uris", "thrift://host.docker.internal:9083")
      .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0,org.apache.hadoop:hadoop-aws:3.3.4")
      .config("spark.hadoop.fs.s3a.endpoint", "http://host.docker.internal:8200")
      .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
      .config("spark.hadoop.fs.s3a.secret.key", "minioadmin123")
      .config("spark.hadoop.fs.s3a.path.style.access", "true")
      .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
      .getOrCreate()
)
```

### Option B — Connect to the standalone Spark master
```python
from pyspark.sql import SparkSession
spark = (
    SparkSession.builder
      .appName("delta-remote")
      .master("spark://host.docker.internal:7077")
      .config("spark.sql.extensions", "org.apache.spark.sql.delta.extensions.DeltaSparkSessionExtension")
      .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
      .config("spark.sql.catalogImplementation", "hive")
      .config("spark.hadoop.hive.metastore.uris", "thrift://host.docker.internal:9083")
      .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0,org.apache.hadoop:hadoop-aws:3.3.4")
      .config("spark.hadoop.fs.s3a.endpoint", "http://host.docker.internal:8200")
      .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
      .config("spark.hadoop.fs.s3a.secret.key", "minioadmin123")
      .config("spark.hadoop.fs.s3a.path.style.access", "true")
      .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
      .getOrCreate()
)
```

## Using from local PyCharm (macOS)
Install PySpark in your venv, then use the same configs as Option A, but without `host.docker.internal` if you prefer `localhost` for MinIO and Hive Metastore:
```python
from pyspark.sql import SparkSession
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
      .getOrCreate()
)
```

## Quick Delta tests
```python
from pyspark.sql import functions as F

spark.sql("CREATE DATABASE IF NOT EXISTS demo")
spark.sql("USE demo")

# Managed table
spark.sql("""
CREATE TABLE IF NOT EXISTS demo.people (
  id INT,
  name STRING
) USING DELTA
""")

spark.sql("INSERT INTO demo.people VALUES (1, 'alice'), (2, 'bob')")
spark.table("demo.people").show()

# External table on MinIO
spark.sql("""
CREATE TABLE IF NOT EXISTS demo.events
USING DELTA
LOCATION 's3a://datalake/events'
""")

spark.range(0, 10).withColumn("ts", F.current_timestamp()) \
    .write.format("delta").mode("overwrite").save("s3a://datalake/events")

spark.read.format("delta").load("s3a://datalake/events").show()
```

## Notes & Troubleshooting
- Ports used here (9000/9001 for MinIO, 9083 for Hive, 7077/8080/8081 for Spark) do not collide with egeria-quickstart defaults.
- If jars fail to download in Spark, check that the container can reach Maven Central, or bake the jars into a custom image.
- Unity Catalog is not applicable here; use the Hive Metastore provided by this stack for shared table metadata.
- If you later enable TLS on MinIO, set `spark.hadoop.fs.s3a.connection.ssl.enabled=true` and update `endpoint` to `https://...`.


## Image notes
- This stack now uses official Apache Spark images (`apache/spark:3.5.1`) instead of Bitnami.
- Spark configuration is mounted to `/opt/spark/conf` inside the containers.
- If your network restricts access to Maven Central, pre-download or mirror the packages set in `spark.jars.packages`.
