FROM prefecthq/prefect:3.9.1.dev4-python3.12@sha256:21b6da5c3e56252c7a9e777902b0a4e4d01d6d7891a1977934d15d6abb6f9d78

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
