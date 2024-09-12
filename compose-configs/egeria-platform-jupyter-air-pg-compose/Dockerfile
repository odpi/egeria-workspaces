# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.

# This build script corrects some permission issues needed to run
# on some enterprise k8s environments. see https://github.com/odpi/egeria-jupyter-notebooks/issues/9

# The published image tag is taken from the numerical version of
# our base image, and appended with the contents of .tag-append (file)
FROM apache/airflow
ARG env_name=python312
ARG py_ver=3.12


RUN pip install --no-cache-dir 'pyegeria>=0.8.1'
RUN pip install --no-cache-dir 'unitycatalog'
RUN pip install --no-cache-dir 'pipx'
RUN pip install --no-cache-dir 'apache-airflow-providers-openlineage'
RUN pip install --no-cache-dir 'apache-airflow-providers-openlineage[common.sql]'


RUN pipx ensurepath
RUN pipx install pyegeria
RUN pipx ensurepath

