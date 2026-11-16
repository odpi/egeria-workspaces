FROM prefecthq/prefect:3.9.3.dev2-python3.12@sha256:772b5518f469a4e02d6f00d768479b9e9c777b01e387d57a091e5af3f21baebc

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
