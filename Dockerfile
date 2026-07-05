FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install uv && \
    uv sync --no-dev

EXPOSE 9191

CMD ["uvicorn", "youtubedlapi_server_infusiblecoder.app:app", "--host", "0.0.0.0", "--port", "9191"]
