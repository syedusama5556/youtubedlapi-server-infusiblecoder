FROM python:3-alpine

COPY ./ /app

WORKDIR /app

# Install git
RUN apk add --no-cache git

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

EXPOSE 9191

#ENTRYPOINT ["youtube-dl-server", "--number-processes", "1", "--host", "0.0.0.0"]
# gunicorn -w 4 -k gevent -b 0.0.0.0:9191 youtubedlapi_server_infusiblecoder.app:app

ENTRYPOINT ["gunicorn", "-w","4","-k","gevent","-b", "0.0.0.0:9191", "youtubedlapi_server_infusiblecoder.app:app"]
