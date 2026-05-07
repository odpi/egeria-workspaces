#!/bin/bash
#
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
#
# Coco Pharmaceuticals Lab Docker Compose configuration
#
# This shell script is automatically invoked when the Jupyter Container is initiated as part of the Docker Compose
# configuration.The script configures and activates the Egeria OMAG servers on each of the three Egeria OMAG Server
# Platforms that are part of the sample Coco Pharmaceuticals deployment environment.
#
#
# The following line is useful if you want to configure an alternate version of python - note that you need to make
# corresponding changes in the Dockerfile-jupyter file.
#
#/opt/conda/bin/activate python312

export EGERIA_METADATA_STORE="qs-metadata-store"
export EGERIA_KAFKA_ENDPOINT='host.docker.internal:9192'
export EGERIA_PLATFORM_URL='https://host.docker.internal:9443'
export EGERIA_VIEW_SERVER='qs-view-server'
export EGERIA_VIEW_SERVER_URL='https://host.docker.internal:9443'
export EGERIA_JUPYTER='True'
export EGERIA_WIDTH='200'
export EGERIA_HOME_GLOSSARY_GUID=
export EGERIA_GLOSSARY_PATH='/home/jovyan/loading-bay/glossary'
export EGERIA_MERMAID_FOLDER='/home/jovyan/work/mermaid_graphs'
export EGERIA_ROOT_PATH='/home/jovyan'
export DR_EGERIA_INBOX_PATH='loading-bay/dr-egeria-inbox'
export DR_EGERIA_OUTBOX_PATH='distribution-hub/dr-egeria-outbox'
export EGERIA_LOCAL_QUALIFIER='CocoPharma'
export EGERIA_USER='erinoverview'
export EGERIA_USER_PASSWORD='secret'
export PYEGERIA_ROOT_PATH='/home/jovyan'
export PYEGERIA_CONFIG_FILE='config_workspaces.json'
export PYEGERIA_CONSOLE_WIDTH=260
export PYEGERIA_PUBLISHING_ROOT='/home/jovyan/config/report_specs'
export PYEGERIA_CONFIG_DIRECTORY='/home/jovyan/config'
