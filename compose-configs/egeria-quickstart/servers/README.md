<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Quickstart server configurations

This directory contains the server configurations for the four [OMAG Servers](https://egeria-project.org/concepts/omag-server/) that make up the quick start environment:

* **qs-metadata-store** is a [Metadata Access Store](https://egeria-project.org/concepts/metadata-access-store/)
  that supports both REST APIs for retrieving and maintaining open metadata along with
  event notifications each time there is change in the metadata.  It is storing its
  metadata in a PostgreSQL repository.  This means that any
  metadata that you create will still be in the repository when you restart this server.
  This server automatically loads the [Core ]

* **qs-integration-daemon** is an [Integration Daemon](https://egeria-project.org/concepts/integration-daemon/) that 
  runs [Integration Connectors](https://egeria-project.org/concepts/integration-connectors/).
  These integration connectors are responsible for cataloguing metadata from external (third party) systems.
  The configuration of these integration connectors is found in the qs-metadata-store.

* **qs-engine-host** is an [Engine Host](https://egeria-project.org/concepts/engine-host/) that is running the [governance engines](https://egeria-project.org/concepts/governance-engine/)
  used to create and manage metadata.  The configuration of these governance engines is found in the qs-metadata-store.

The final server provides the services for Egeria's python capabilities built around pyegeria.

* **qs-view-server** is a [View Server](https://egeria-project.org/concepts/view-server/) that calls the 
  qs-metadata-store to send and retrieve metadata from its repository.  Its services are designed to
  support calls from non-Java environments such as python and javascript.
  Egeria's user interfaces make calls to the view server.

These server configurations can be (re)created using the `BuildQuickstartConfigs.http` script.

> **Note:** When using the `quick-start-local` or `quick-start-multi-host` scripts, these configurations are copied to `runtime-volumes/egeria-platform-data/data/servers/`. Local modifications should be made in that runtime directory to persist and be ignored by Git.


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the Egeria project.