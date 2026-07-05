#!/bin/bash
set -e

IMAGE="syedusama5556/youtubedlapi_server_infusiblecoder:latest"
PORT=${1:-9191}

echo "========================================"
echo " yt-dlp API Server - Docker Install"
echo "========================================"
echo ""

# --- Docker ---
echo "==> Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker "$USER"
    echo "Docker installed. Log out and back in, then re-run this script."
    exit 0
fi

echo "==> Pulling image..."
docker pull "$IMAGE"

echo "==> Stopping old container if exists..."
docker stop youtubedlapi_container 2>/dev/null || true
docker rm youtubedlapi_container 2>/dev/null || true

echo "==> Starting server on port $PORT..."
docker run -d \
    --name youtubedlapi_container \
    --restart unless-stopped \
    -p "$PORT":9191 \
    "$IMAGE"

echo ""
echo "Server is running on port $PORT!"
echo "  Test: curl http://localhost:$PORT/api/version"

# --- Firewall ---
echo ""
echo "==> Configuring firewall (optional)..."
if command -v ufw &> /dev/null; then
    sudo ufw allow "$PORT" 2>/dev/null || true
    sudo ufw allow http 2>/dev/null || true
    sudo ufw allow https 2>/dev/null || true
    sudo ufw allow ssh 2>/dev/null || true
    sudo ufw --force enable 2>/dev/null || true
    echo "  Firewall configured."
else
    echo "  ufw not found, skipping."
fi

# --- Nginx reverse proxy (optional) ---
echo ""
read -p "==> Set up Nginx reverse proxy with a domain? (y/N): " setup_nginx
if [ "$setup_nginx" = "y" ] || [ "$setup_nginx" = "Y" ]; then
    echo "Installing Nginx..."
    sudo apt-get update -qq
    sudo apt-get install -y -qq nginx

    read -p "Enter your domain name (e.g. api.example.com): " domain_name

    cat <<EOF | sudo tee /etc/nginx/sites-available/ytdlp-api > /dev/null
map \$http_upgrade \$connection_upgrade {
    default         upgrade;
    ''              close;
}

server {
    server_name $domain_name;

    location / {
        proxy_pass         http://127.0.0.1:$PORT;
        proxy_http_version  1.1;
        proxy_set_header    Upgrade     \$http_upgrade;
        proxy_set_header    Connection  \$connection_upgrade;
    }
}
EOF

    sudo ln -sf /etc/nginx/sites-available/ytdlp-api /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl reload nginx
    echo "Nginx configured for $domain_name"
fi

echo ""
echo "========================================"
echo " Setup complete!"
echo ""
echo "  API:      http://localhost:$PORT"
echo "  Version:  curl http://localhost:$PORT/api/version"
echo "  YouTube:  curl 'http://localhost:$PORT/api/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&flatten=true'"
echo "  Logs:     docker logs -f youtubedlapi_container"
echo "  Stop:     docker stop youtubedlapi_container"
echo "  Restart:  docker restart youtubedlapi_container"
echo "========================================"
