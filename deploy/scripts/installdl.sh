#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Installing Python..."
    sudo apt update
    sudo apt install -y software-properties-common
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt install -y python3.11
    sudo apt install -y wget
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3.11 get-pip.py
else
    echo "Python is already installed."
fi

echo "Installing pip..."
sudo python3.11 -m pip install --upgrade pip
pip install uv

echo "Installing dependencies..."
pip install youtubedlapi-server-infusiblecoder --ignore-installed
pip install curl-cffi yt-dlp-ejs brotli websockets pycryptodomex mutagen

echo "Configuring firewall..."
sudo apt install -y ufw
sudo ufw allow https
sudo ufw allow http
sudo ufw allow 80
sudo ufw allow 9191
sudo ufw allow 22
sudo ufw allow ssh
sudo ufw --force enable

echo "Installing Nginx..."
sudo apt-get install -y nginx

echo "Configuring Nginx..."
read -p "Enter your domain name: " domain_name

cat <<EOF | sudo tee /etc/nginx/sites-available/default > /dev/null
map \$http_upgrade \$connection_upgrade {
    default         upgrade;
    ''              close;
}

server {
    server_name $domain_name;

    location / {
        # Backend nodejs server
        proxy_pass         http://127.0.0.1:9191;
        proxy_http_version  1.1;
        proxy_set_header    Upgrade     \$http_upgrade;
        proxy_set_header    Connection  \$connection_upgrade;
    }
}
EOF

echo "Testing Nginx configuration..."
sudo nginx -t

echo "Reloading Nginx..."
sudo systemctl reload nginx

# Find the process ID (PID) of the server
pid=$(ps aux | grep '[y]outubedlapi-server-infusiblecoder' | awk '{print $2}')

# Check if the server is already running
if [ -n "$pid" ]; then
    echo "Server is already running with PID: $pid"
    exit 0
fi

# Start the server
echo "Starting the server..."
nohup uvicorn youtubedlapi_server_infusiblecoder.app:app --host 0.0.0.0 --port 9191 --workers 1 --log-level info &
echo "Server started in background."

echo "The setup is complete!"
