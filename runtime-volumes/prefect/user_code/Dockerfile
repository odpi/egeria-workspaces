FROM prefecthq/prefect:3.8.7-python3.12@sha256:f15a7bda40608ee890ff97e963ec3403dc25d633810a4ef1fff93ff303f4ef5f

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
