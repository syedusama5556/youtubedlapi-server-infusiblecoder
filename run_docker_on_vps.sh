#!/bin/bash

# Update and upgrade packages
sudo apt update
sudo apt upgrade -y

# Install necessary dependencies
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Enable Docker to start on boot
sudo systemctl enable docker

# Start Docker service
sudo systemctl start docker

# Pull Docker container
sudo docker pull syedusama5556/youtubedlapi_server_infusiblecoder:v2

# Run Docker container, expose port 9191, and map it to the host machine
sudo docker run -d -p 9191:9191 --name youtubedlapi_container syedusama5556/youtubedlapi_server_infusiblecoder:v2

# Allow incoming traffic on port 9191
sudo ufw allow 9191

# Allow Ports
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https

# Enable UFW
sudo ufw enable

# Display firewall status
sudo ufw status

echo "Docker installation and setup completed. The Docker container is running on port 9191."
