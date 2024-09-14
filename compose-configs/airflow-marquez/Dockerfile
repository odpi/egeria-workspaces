USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    wget libssl-dev libsasl2-dev libcurl4-openssl-dev \
    software-properties-common gcc make libz-dev \
    libzstd-dev g++ \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /root
RUN wget -qO - https://github.com/confluentinc/librdkafka/archive/refs/tags/v2.0.2.tar.gz | tar -xz
WORKDIR /root/librdkafka-2.0.2
RUN ./configure
RUN make && make check && make install
WORKDIR /opt/airflow

USER airflow