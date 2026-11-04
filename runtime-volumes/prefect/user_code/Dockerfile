FROM prefecthq/prefect:3.9.2.dev1-python3.12@sha256:4c3432afd6c7e83b53d543871872b3b46676cb5fb01d4268ca942d82c119a9cd

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
