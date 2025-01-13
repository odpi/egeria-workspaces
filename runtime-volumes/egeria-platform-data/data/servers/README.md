<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Default server configurations

This directory contains the server configurations for four [OMAG Servers](https://egeria-project.org/concepts/omag-server/):

* **qs-metadata-store** is a [Metadata Access Store](https://egeria-project.org/concepts/metadata-access-store/)
  that supports both REST APIs for retrieving and maintaining open metadata along with
  event notifications each time there is change in the metadata.  It is storing its
  metadata in a repository stored in a Database Schema called egeria.repository_qs_metadata_store located on the local PostgreSQL Server.
  This means that any metadata that you create will still be in the repository when you restart this server.
  This server automatically loads the 
  [Core Content Pack](https://egeria-project.org/content-packs/core-content-pack/overview/) 
  to provide basic definitions for connectors and governance engines.

* **qs-integration-daemon** is an [Integration Daemon](https://egeria-project.org/concepts/integration-daemon/)
  that hosts the configured [Integration Connectors](https://egeria-project.org/concepts/integration-connector/).
  Typically, the configuration for these integration connectors found in the qs-metadata-store and is loaded via content packs.

* **qs-engine-host** is an [Engine Host](https://egeria-project.org/concepts/engine-host/) that is hosting the configured
  [governance engines](https://egeria-project.org/concepts/governance-engine/).  
  Typically, the configuration for these governance engines found in the qs-metadata-store and is loaded via content packs.

The final server provides the services for Egeria's UIs.

* **qs-view-server** is a [View Server](https://egeria-project.org/concepts/view-server/) that calls the 
  qs-metadata-store to send and retrieve metadata from its repository.  Its services are designed to
  support calls from non-Java environments such as python and javascript.
  Egeria's user interfaces and **pyegeria** make calls to the view server.

These server configurations can be (re)created using the `BuildQuickStartConfigs.http` script.

## Starting the servers

Ensure the OMAG Server Platform is running at `https://localhost:9443`.

You can start the servers one at a time using the following curl command,
replacing `{{server}}` with the name of the server to start.  Messages appear from the platform's stdout to indicate the
status of the server.

```bash
curl --location --request POST 'https://localhost:9443/open-metadata/platform-services/users/garygeeke/server-platform/servers/{{server}}/instance' \
--data ''
```
Alternatively you can edit the `application.properties` file in the `platform` directory and change the `startup.server.list` property to list the servers that should be automatically started when the platform is started:
```properties
# Comma separated names of servers to be started.  The server names should be unquoted.
startup.server.list=qs-metadata-store,qs-engine-host,qs-integration-daemon,qs-view-server
```
When the platform is restarted the servers start in the order listed.  
More information on the `application.properties` file can be found in the
[Configuring an OMAG Server Platform](https://egeria-project.org/guides/admin/configuring-the-omag-server-platform/) documentation.


## Loading the Coco Pharmaceuticals Metadata

Running the `AddCocoMetadataToQuickStartServers.http` script will add metadata from the Coco Pharmaceuticals scenarios.  This includes
activating the `ClinicalTrials@CocoPharmaceuticals` engine to the `qs-engine-host` server.

## Changing the implementation of the repository used by qs-metadata-store

The `ChangeQuickStartRepositoryToInMemory.http` and `ChangeQuickStartRepositoryToXTDB.http` scripts are used 
to change the implementation of the repository used by qs-metadata-store.



----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the Egeria project.