FROM --platform=linux/amd64 python:3.9-slim  

WORKDIR /app

COPY requirements.txt . 

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    binutils libproj-dev gdal-bin python3-gdal \
    && rm -rf /var/lib/apt/lists/*

# This installs chromium for exporting dispatch lists from html to png
# https://github.com/assafelovic/gpt-researcher/issues/658
RUN apt-get update \
    && apt-get install -y gnupg wget ca-certificates --no-install-recommends \
    && wget -qO - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable chromium-driver \
    && google-chrome --version && chromedriver --version

RUN pip3 install -r ./requirements.txt --no-cache-dir  

COPY . .

RUN chmod +x /app/docker/server-entrypoint.sh
