FROM python:3.11-slim

WORKDIR /app

# Install Deno (used by some yt-dlp extractors for JS runtime)
RUN apt-get update && apt-get install -y unzip curl && \
    curl -fsSL https://deno.land/install.sh | sh && \
    ln -s /root/.deno/bin/deno /usr/local/bin/deno && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install uv && \
    uv sync --no-dev

EXPOSE 9191

CMD ["uvicorn", "youtubedlapi_server_infusiblecoder.app:app", "--host", "0.0.0.0", "--port", "9191"]
