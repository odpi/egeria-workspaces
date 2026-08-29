FROM prefecthq/prefect:3-python3.12@sha256:6c0dc14195cae814eddeb66104a8333810a0a9886a5d7f0c45443136f167b3e0

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
