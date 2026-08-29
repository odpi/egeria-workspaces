FROM python:3.11-slim@sha256:1042b61448fef4ba92d16a8c7eb4996d027568ce64792a7877fd88511e0af7c6

# Install system dependencies needed for compiling python packages (if any) and curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/dagster/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4000

# Start the gRPC server for code location
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "repo.py"]
