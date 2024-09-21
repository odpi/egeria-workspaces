<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->


# Setting up XTDB to use Postgres with Egeria Workspaces
## Pre-reqs 
* local clone of Egeria Workspaces
* Docker and Docker Compose

## Background

Egeria supports several repository technologies including XTDB. XTDB itself can be configured to use different backend storage mechanisms including Key-Value (KV) stores, Kafka and databases such as Postgres. XTDB is typically configured to use multiple technologies for different purposes. XTDB capabilities can use different technologies for:

* index - store 
* search
* tx-log
* document-store

For development, our default configuration uses XTDB with the KV stores for the index-store, tx-log and document-store. However, sometimes it is useful to change the configuration to Postgres for the tx-log and document-store, in particular, for testing. Many other configurations are possible.

This note describes how to switch the repository for the **active-metadata-store** from the default to Postgres.

## Approach

**Egeria Workspaces** contains several different **Docker Compose** scripts that configure different combinations of technologies to for use in development and experimentation. One of these configurations is called **egeria-platform-jupyter-proxy-pg-compose** which, as the name suggests, deploys an environment that includes Egeria, Jupyter Server, the Open Lineage Proxy Backend and Postgres. With a minor configuration change we can have Egeria use Postgres with XTDB for the **active-metadata-store** server repository. 

## Steps
1) Download a clone of egeria-workspaces
2) Within the egeria-workspaces directory, navigate to:
`compose-configs/egeria-platform-jupyter-proxy-pg-compose/data/servers/active-metadata-store/config`
3) Now replace the default configuration file for the active-metadata-store with  the postgres enabled version. The server configuration file must be named:
`active-metadata-store.config` 
and the postgres enabled contents are in:
`pg_active-metadata-store.config`
4) Start the environment - you can do this from a shell within the `compose-configs/egeria-platform-jupyter-proxy-pg-compose` directory by typing:

`docker compose -f egeria-platform-jupyter-proxy-pg-compose up  --build`


This command should start up all the servers. Please note that it can take several minutes for Egeria to come up the first time since it is pre-loading its repository with common configuration data.

# Reverting 

You can easily revert the configuration back to the default use of KV stores with XTDB. By doing so, you will lose the contents of the metadata store you have been using and starting fresh. Here are the steps:

1) Bring down the docker compose configuration by typing:

`docker compose -f egeria-platform-jupyter-proxy-pg-compose down`

2) copying the `kv_active-metadata-store.config` file to `active-metadata-store.config` 

3) delete `compose-configs/egeria-platform-jupyter-proxy-pg-compose/data/servers/active-metadata-store/repository` and its sub-directories.

4) Restart your environment with:
`docker compose -f egeria-platform-jupyter-proxy-pg-compose`


