FROM prefecthq/prefect:3.9.4.dev2-python3.12@sha256:86a8025c3e47e5773093d04660b5eb14fa137788e77104b65e402e5464bbd9a7

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
