#!/bin/bash

while true; do
    # Kill processes containing "youtube" or "bgapi"
    ps aux | (grep youtube || grep bgapi) | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1

    # Start the youtubedlapi-server-infusiblecoder
    uvicorn youtubedlapi_server_infusiblecoder.app:app --host 0.0.0.0 --port 5000 --workers 1 --log-level info
    # Sleep for 600 seconds (10 minutes)
    sleep 600
done
