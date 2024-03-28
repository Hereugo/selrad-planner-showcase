FROM --platform=linux/amd64 python:3.9-slim  

WORKDIR /app

COPY requirements.txt . 

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r ./requirements.txt --no-cache-dir  

COPY . .

RUN chmod +x /app/docker/server-entrypoint.sh
