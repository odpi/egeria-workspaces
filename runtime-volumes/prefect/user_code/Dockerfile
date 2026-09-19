FROM prefecthq/prefect:3.8.6-python3.12@sha256:ec9e58deaf30002dd65ebb755ca3d9eb5f169902882abf18c79261a4aa95bfe3

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
