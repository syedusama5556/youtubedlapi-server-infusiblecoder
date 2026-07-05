#!/bin/bash

# Kill processes containing "youtube"
ps aux | grep youtube | awk '{print $2}' | xargs kill -9

# Kill processes containing "bgapi"
ps aux | grep bgapi | awk '{print $2}' | xargs kill -9

# Restart bgapi.sh using nohup
nohup ./bgapi.sh &
