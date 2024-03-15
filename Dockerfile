FROM python:3-alpine

COPY ./ /app

WORKDIR /app

# Install git and build dependencies for certain Python packages if necessary
RUN apk add --no-cache git gcc musl-dev

RUN pip3 install --upgrade pip

# Install dependencies
RUN pip3 install -r requirements.txt

EXPOSE 9191

#ENTRYPOINT ["youtube-dl-server", "--number-processes", "1", "--host", "0.0.0.0"]
# gunicorn -b 0.0.0.0:9191 youtubedlapi_server_infusiblecoder.app:app

# Use CMD instead of ENTRYPOINT to easily override the command if needed
CMD ["uvicorn", "youtubedlapi_server_infusiblecoder.app:app_asgi", "--host", "0.0.0.0", "--port", "9191", "--workers", "1", "--log-level", "info"]
