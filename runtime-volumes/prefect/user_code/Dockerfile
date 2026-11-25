FROM prefecthq/prefect:3.9.5.dev3-python3.12@sha256:23c17600ab26ed001015c8187f74aa6b218fcdf025452cff9a32907bce065236

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
