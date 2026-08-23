<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Pre-built server configurations

This directory contains the server configurations for the [OMAG Servers](https://egeria-project.org/concepts/omag-server/) that make up the both the Quickstart and Freshstart environments:

* The [Quickstart server configuration](#quickstart-server-configurations) are used with the quickstart environment.  These servers are configured for the Coco Pharmaceuticals use cases and demos.
* The [Freshstart server configuration](#freshstart-server-configurations) are used with the freshstart environment.  These servers are configured with the standard connectors, ready for you to set up your own Egeria environment.

## Quickstart server configurations

The quickstart servers are as follows:

* **qs-metadata-store** is a [Metadata Access Store](https://egeria-project.org/concepts/metadata-access-store/)
  that supports both REST APIs for retrieving and maintaining open metadata along with
  event notifications each time there is change in the metadata.  It is storing its
  metadata in a PostgreSQL repository.  This means that any
  metadata that you create will still be in the repository when you restart this server.
  This server automatically loads the CoreContentPack plus a set of additional
  [content packs](https://egeria-project.org/content-packs/) (Organization Insight, Egeria, Files,
  Postgres, MSSQL, Oracle, DB2LUW, DuckDB, OpenLineage, Open Metadata Digital Products, APIs, Unity
  Catalog, the Coco Pharmaceuticals combo archive, and Simple Catalog) — see
  `qs-metadata-store/config/qs-metadata-store.config` for the full, current list.

* **qs-integration-daemon** is an [Integration Daemon](https://egeria-project.org/concepts/integration-daemon/) that 
  runs [Integration Connectors](https://egeria-project.org/concepts/integration-connectors/).
  These integration connectors are responsible for cataloguing metadata from external (third party) systems
  (databases, files, Apache Atlas, Apache Kafka, OpenLineage, OpenAPIs, etc.).
  The configuration of these integration connectors is found in the qs-metadata-store.

* **qs-nanny-daemon** is a second [Integration Daemon](https://egeria-project.org/concepts/integration-daemon/),
  separate from qs-integration-daemon, that runs integration connectors which monitor, extract, and analyse
  metadata already in the repository to create new insight and digital products (the Egeria, Jacquard, Babbage,
  Liskov, and SmartCollections integration groups) rather than cataloguing external systems.

* **qs-engine-host** is an [Engine Host](https://egeria-project.org/concepts/engine-host/) that is running the [governance engines](https://egeria-project.org/concepts/governance-engine/)
  used to create and manage metadata.  The configuration of these governance engines is found in the qs-metadata-store.

The final server provides the services for Egeria's python capabilities built around pyegeria.

* **qs-view-server** is a [View Server](https://egeria-project.org/concepts/view-server/) that calls the 
  qs-metadata-store to send and retrieve metadata from its repository.  Its services are designed to
  support calls from non-Java environments such as python and javascript.
  Egeria's user interfaces make calls to the view server.

These server configurations can be (re)created using the `BuildQuickstartConfigs.http` script.

> **Note:** When using the `quick-start-local` or `quick-start-multi-host` scripts, these configurations are copied to `runtime-volumes/quickstart-platform-data/data/servers/`. Local modifications should be made in that runtime directory to persist and be ignored by Git.

## Freshstart server configurations

The freshstart servers mirror the quickstart set one-for-one (`fs-*` instead of `qs-*`), configured with the
standard connectors rather than the Coco Pharmaceuticals demo setup, ready for you to build your own environment:

* **fs-metadata-store** is a [Metadata Access Store](https://egeria-project.org/concepts/metadata-access-store/)
  that supports both REST APIs for retrieving and maintaining open metadata along with
  event notifications each time there is change in the metadata.  It stores its metadata in a PostgreSQL
  repository, so anything you create is still there when you restart this server. This server automatically
  loads the CoreContentPack plus a set of additional [content packs](https://egeria-project.org/content-packs/)
  (Organization Insight, Egeria, Files, Postgres, MSSQL, Oracle, DB2LUW, DuckDB, OpenLineage, Open Metadata
  Digital Products, and APIs) — see `fs-metadata-store/config/fs-metadata-store.config` for the full, current
  list.

* **fs-integration-daemon** is an [Integration Daemon](https://egeria-project.org/concepts/integration-daemon/)
  that runs [Integration Connectors](https://egeria-project.org/concepts/integration-connectors/) responsible
  for cataloguing metadata from external (third party) systems (databases, files, Apache Atlas, Apache Kafka,
  OpenLineage, OpenAPIs, etc.). The configuration of these integration connectors is found in the
  fs-metadata-store.

* **fs-nanny-daemon** is a second Integration Daemon, separate from fs-integration-daemon, that runs
  integration connectors which monitor, extract, and analyse metadata already in the repository to create new
  insight and digital products (the Egeria, Jacquard, Babbage, Liskov, and SmartCollections integration groups)
  rather than cataloguing external systems.

* **fs-engine-host** is an [Engine Host](https://egeria-project.org/concepts/engine-host/) that runs the
  [governance engines](https://egeria-project.org/concepts/governance-engine/) used to create and manage
  metadata. The configuration of these governance engines is found in the fs-metadata-store.

* **fs-view-server** is a [View Server](https://egeria-project.org/concepts/view-server/) that calls the
  fs-metadata-store to send and retrieve metadata from its repository. Its services are designed to support
  calls from non-Java environments such as python and javascript.

These server configurations can be (re)created using the `BuildFreshstartConfigs.http` script.

> **Note:** When using the `fresh-start-local` or `fresh-start-multi-host` scripts, these configurations are copied to `runtime-volumes/freshstart-platform-data/data/servers/`. Local modifications should be made in that runtime directory to persist and be ignored by Git.


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the Egeria project.