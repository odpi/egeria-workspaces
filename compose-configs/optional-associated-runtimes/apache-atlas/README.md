# Apache Atlas + Hadoop + Hive + Hive Metastore (Docker Compose)

This stack brings up a simple Apache Atlas/Hadoop/Hive environment:
- Atlas—2.3.0 including the web console
- Hive Metastore (backed by the Postgres that runs in egeria-quickstart on host:5442)
- Hadoop—basic storage
- Hive Server


It is designed so you can access it from:
- The egeria-quickstart Jupyter (running on host port 7888), or
- Local Python (PyCharm) on your Mac

## Prerequisites
- Ensure `egeria-quickstart` is running, specifically its Postgres on `127.0.0.1:5442` and Kafka on 9192.
- Ensure Postgres has a database `metastore` with user `egeria_admin` and password `admin4egeria`.
  - If you haven't created it yet, run:
    ```bash
    psql postgresql://postgres:egeria@localhost:5442/postgres -c "CREATE DATABASE metastore; ALTER DATABASE metastore OWNER TO egeria_admin; GRANT ALL PRIVILEGES ON DATABASE metastore TO egeria_admin;"
    ```

## Start the stack
```bash
cd compose-configs/apache-atlas
# first start will download images and jars
docker compose up -d
```

## Services & Ports
- Atlas Console: http://localhost:21000 (login: admin, password: admin)
- Hive Metastore Thrift: thrift://localhost:9183

