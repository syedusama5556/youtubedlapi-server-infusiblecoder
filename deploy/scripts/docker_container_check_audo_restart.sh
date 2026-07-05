#!/bin/bash

# Define your container name
CONTAINER_NAME="youtubedlapi_container"

while true; do
    # Check if the container is running
    if [ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME" 2>/dev/null)" == "true" ]; then
        echo "Container $CONTAINER_NAME is running."
    else
        echo "Container $CONTAINER_NAME is not running. Restarting..."
        docker restart "$CONTAINER_NAME"
        echo "Container $CONTAINER_NAME restarted."
    fi

    sleep 600  # Sleep for 10 minutes (600 seconds)
done
