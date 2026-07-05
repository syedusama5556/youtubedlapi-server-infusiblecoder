#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Installing Python..."
    sudo apt update
    sudo apt install -y software-properties-common
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt install -y python3.9
    sudo apt install -y wget
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3.9 get-pip.py
else
    echo "Python is already installed."
fi

echo "Installing pip..."
sudo python3 -m pip install --upgrade pip

echo "Installing dependencies..."
pip3 install youtubedlapi-server-infusiblecoder --ignore-installed

echo "Configuring firewall..."
sudo apt install -y ufw
sudo ufw allow https
sudo ufw allow http
sudo ufw allow 80
sudo ufw allow 9191
sudo ufw allow 5000
sudo ufw allow 22
sudo ufw allow ssh
sudo ufw --force enable



# Find the process ID (PID) of the server
pid=$(ps aux | grep '[y]outubedlapi-server-infusiblecoder' | awk '{print $2}')

# Check if the server is already running
if [ -n "$pid" ]; then
    echo "Server is already running with PID: $pid"
    exit 0
fi

# Start the server
echo "Starting the server..."
nohup ./bgapi.sh &
echo "Server started in background."

echo "The setup is complete!"
