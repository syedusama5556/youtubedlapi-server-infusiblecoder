FROM python:3-alpine

RUN pip3 install Flask gunicorn yt-dlp

RUN pip3 install --upgrade pip

COPY ./ /app

WORKDIR /app

EXPOSE 9191

#ENTRYPOINT ["youtube-dl-server", "--number-processes", "1", "--host", "0.0.0.0"]
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:9191", "youtubedlapi_server_infusiblecoder.app:app"]
