<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview
This directory contains sample Docker Compose scripts for companion runtimes that can be used with Egeria. They are provided for
convenient, supporting experimentation, development, and learning. 
Currently there are compose configurations for:

    * Airflow & Marquez - used for demonstrating Open Lineage and other metadata integrations.
    * Milvus - a vector database used in AI workloads.
    * Superset—an analytics and reporting dashboard that we use to present Egeria survey results.
    * Unity Catalog—The Open Source version of Unity Catalog—we use for demonstrating Egeria's integration with other catalogs.
        * Two deployments - one using Postgres and one native.
    * Deltalake-Spark - a data lake framework for storing and processing data - this is a small sandbox configuration but includes
        other components that may be useful for additional experiments such as:
        * Spark - a distributed computing framework for processing large datasets
        * Delta Lake - a storage layer for Apache Spark that provides ACID transactions, scalable metadata handling, and more
        * Minio - an S3 compatible object store
        * Hive metastore - a metadata store for managing tables and databases
        

As always, your feedback and participation are welcome. 


License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.