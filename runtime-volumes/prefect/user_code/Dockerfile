FROM prefecthq/prefect:3.8.8.dev1-python3.12@sha256:226abced084c35d1e0650026421dbedcbdcb6d7d2ae375fe86e3eee4e111dc03

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
