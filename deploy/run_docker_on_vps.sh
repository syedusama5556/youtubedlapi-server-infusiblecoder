#!/bin/bash

# Function to install Docker on Debian/Ubuntu systems
install_docker() {
    # Update and upgrade packages
    sudo apt update
    sudo apt upgrade -y

    # Install necessary dependencies
    sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

    # Add Docker GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # Add Docker repository
    if [[ $(lsb_release -is) == "Ubuntu" ]]; then
        echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    elif [[ $(lsb_release -is) == "Debian" ]]; then
        echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    fi

    # Install Docker
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io

    # Enable Docker to start on boot
    sudo systemctl enable docker

    # Start Docker service
    sudo systemctl start docker
}

# Pull and run the Docker container
run_docker_container() {
    sudo docker pull syedusama5556/youtubedlapi_server_infusiblecoder:latest
    sudo docker run -d -p 9191:9191 --name youtubedlapi_container syedusama5556/youtubedlapi_server_infusiblecoder:latest
}

# Configure UFW Firewall
configure_ufw() {
    sudo ufw allow 9191
    sudo ufw allow ssh
    sudo ufw allow http
    sudo ufw allow https
    sudo ufw enable
    sudo ufw status
}

# Install Docker
install_docker

# Run Docker container
run_docker_container

# Configure UFW Firewall
configure_ufw

echo "Docker installation and setup completed. The Docker container is running on port 9191."
