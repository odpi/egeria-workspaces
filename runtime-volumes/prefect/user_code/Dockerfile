FROM prefecthq/prefect:3.8.7.dev4-python3.12@sha256:f2515ed61c5c32dc0a5bf7a1afb215c1f9002beda1db6b083b31759bfd4e5aa9

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
