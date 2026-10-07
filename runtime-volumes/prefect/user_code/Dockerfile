FROM prefecthq/prefect:3.8.8.dev3-python3.12@sha256:60d13e3ae731230a2ef8341c3a7b646ad63863fce998c0058ca3601fd8d3c72d

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
