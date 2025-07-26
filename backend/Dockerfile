FROM --platform=linux/amd64 python:3.9-slim  

WORKDIR /app

COPY requirements.txt . 

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    binutils libproj-dev gdal-bin python3-gdal

# # This installs chromium for exporting dispatch lists from html to png
# # https://github.com/assafelovic/gpt-researcher/issues/658
# # 07/12/2024 (Amir N): For some reason it stopped building, and complained that packages where not installed.
# # Probably the issue was that apt-key was deprecated (see apt-key(8)), and some packages weren't able to be found/installed beforehand.
# RUN apt-get update \
#     && apt-get install -y gnupg wget ca-certificates --no-install-recommends \
#     && wget -qO - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
#     && apt-get update \
#     && apt-get install -y google-chrome-stable chromium-driver \
#     && google-chrome --version && chromedriver --version

# 07/12/2024: Alternative solution to install chromium  
# This script uses an alternative proper way for apt-key by using gpg instead.
# https://blog.logrocket.com/setting-headless-chrome-node-js-server-docker/ 
RUN apt-get update && apt-get install gnupg wget -y && \
    wget --quiet --output-document=- https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google-archive.gpg && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update && \
    apt-get install google-chrome-stable -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*


RUN pip3 install -r ./requirements.txt --no-cache-dir  

COPY . .

ENV PYTHONUNBUFFERED 1

RUN chmod +x /app/docker/server-entrypoint.sh
