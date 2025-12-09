# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project

# Use a lightweight official Python image as the base
FROM python:3.11-slim

# Set environment variables to silence dependency warnings
ENV PIP_ROOT_USER_ACTION=ignore \
    PYTHONUNBUFFERED=1

# Install required Python packages for MLflow, PostgreSQL, and MinIO connectivity:
# 1. mlflow: The core MLflow package.
# 2. psycopg2-binary: Python client for PostgreSQL (used by the backend store).
# 3. boto3: AWS SDK for Python, required for S3-compatible storage like MinIO.
# 4. minio: Optional, but good practice for connecting to MinIO.
RUN pip install --no-cache-dir \
    mlflow==2.11.3 \
    psycopg2-binary \
    boto3

# MLflow runs on port 5000 inside the container
EXPOSE 5000

# Create a non-root user and switch to it for better security (optional but recommended)
RUN adduser --disabled-password --gecos "" mlflow_user
USER mlflow_user

# Define the working directory for the mlflow user
WORKDIR /home/mlflow_user

# The 'command' in docker-compose.yml will override the ENTRYPOINT, 
# so we don't need to define one here.
# The command from the docker-compose.yml is:
# mlflow server --backend-store-uri $BACKEND_STORE_URI --default-artifact-root $ARTIFACT_ROOT --host 0.0.0.0 --port 5000