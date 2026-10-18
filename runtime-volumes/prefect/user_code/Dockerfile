FROM prefecthq/prefect:3.8.9.dev2-python3.12@sha256:1bc752b2bc11e4ac4a4bec5a38220460408f52367a8180d55d3c59d8c69fc65e

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/prefect/flows

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variable to allow python to find custom modules
ENV PYTHONPATH=/opt/prefect/flows
