FROM apache/airflow:3.1.7

USER root

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates libssl-dev libsasl2-dev libcurl4-openssl-dev gcc make g++ build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

RUN curl -L "https://github.com/confluentinc/librdkafka/archive/refs/tags/v2.0.2.tar.gz" -o librdkafka.tar.gz && tar -xzf librdkafka.tar.gz && cd librdkafka-2.0.2 && ./configure --prefix=/usr && make && make install && cd .. && rm -rf librdkafka*

WORKDIR /opt/airflow
USER airflow

COPY --chown=airflow:0 requirements.txt .

RUN pip install --no-cache-dir --user apache-airflow-providers-openlineage>=1.2.0 apache-airflow-providers-postgres apache-airflow-providers-apache-kafka --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.7/constraints-3.12.txt"

RUN pip install --no-cache-dir --user confluent-kafka>=2.0.2 pyegeria>=5.5.3.15 unitycatalog

