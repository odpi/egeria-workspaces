FROM prefecthq/prefect:3.8.9.dev6-python3.12@sha256:3b3357b4d50272837ed10ad90aba548b23e552077d2f711aebe6cd7041877fe6

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
