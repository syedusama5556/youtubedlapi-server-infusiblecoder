#!/bin/bash

# Kill processes containing "youtube" or "bgapi"
ps aux | grep -E '(youtube|bgapi)' | grep -v grep | awk '{print $2}' | xargs kill -9

# Restart bgapi.sh using nohup
nohup ./bgapi.sh &
