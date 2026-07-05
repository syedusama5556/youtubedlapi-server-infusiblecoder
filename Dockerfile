FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends xz-utils unzip curl ca-certificates && \
    curl -fsSL "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz" -o /tmp/ffmpeg.tar.xz && \
    tar -xf /tmp/ffmpeg.tar.xz -C /tmp/ --strip-components=1 && \
    cp /tmp/bin/ffmpeg /usr/local/bin/ && \
    rm -rf /tmp/* && \
    curl -fsSL https://deno.land/install.sh | sh && \
    ln -s /root/.deno/bin/deno /usr/local/bin/deno && \
    apt-get purge -y xz-utils unzip && apt-get autoremove -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md MANIFEST.in ./

RUN pip install --no-cache-dir uv && \
    uv sync --no-dev --no-cache && \
    rm -rf /root/.cache/*

COPY youtubedlapi_server_infusiblecoder/ youtubedlapi_server_infusiblecoder/

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 9191

CMD ["uvicorn", "youtubedlapi_server_infusiblecoder.app:app", "--host", "0.0.0.0", "--port", "9191"]
