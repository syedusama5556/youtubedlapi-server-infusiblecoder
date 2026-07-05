#!/bin/bash

# Stop and remove all Docker containers
docker container stop $(docker container ls -aq) > /dev/null 2>&1
docker container rm $(docker container ls -aq) > /dev/null 2>&1

# Run the Docker container
sudo docker run -d -p 9191:9191 --name youtubedlapi_container syedusama5556/youtubedlapi_server_infusiblecoder:latest

echo "The Docker container is restarted."