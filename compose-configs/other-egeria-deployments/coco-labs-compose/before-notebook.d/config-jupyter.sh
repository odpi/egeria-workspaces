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

export EGERIA_METADATA_STORE="active-metadata-store"
export EGERIA_KAFKA_ENDPOINT='host.docker.internal:8192'
export EGERIA_PLATFORM_URL='https://host.docker.internal:8443'
export EGERIA_VIEW_SERVER='view-server'
export EGERIA_VIEW_SERVER_URL='https://host.docker.internal:8443'
export EGERIA_INTEGRATION_DAEMON='integration-daemon'
export EGERIA_INTEGRATION_DAEMON_URL='https://host.docker.internal:8443'
export EGERIA_ENGINE_HOST='engine-host'
export EGERIA_ENGINE_HOST_URL='https://host.docker.internal:8443'
export EGERIA_ADMIN_USER='garygeeke'
export EGERIA_ADMIN_PASSWORD='secret'
export EGERIA_USER='erinoverview'
export EGERIA_USER_PASSWORD='secret'
export EGERIA_JUPYTER='True'
export EGERIA_WIDTH='200'
export EGERIA_HOME_GLOSSARY_GUID=
export EGERIA_GLOSSARY_PATH='/home/jovyan/loading-bay/glossary'

#rm -rf ./__pychache__
export PYTHONDONTWRITEBYTECODE=1
python3 /home/jovyan/labs/common/config_coco_core.py
#python3 /home/jovyan/labs/common/config_coco_datalake.py
#python3 /home/jovyan/labs/common/config_coco_development.py
echo "Launching Jupyter notebook server.."
