#!/bin/bash

SERVICE_NAME=${SERVICE_NAME:-"youtubedlapi_server"}
SERVICE_DESCRIPTION="Uvicorn application for Youtube Data API server"
SERVICE_USER=${SERVICE_USER:-"youtubedlapiuser"}
SERVICE_LOG_DIR=${SERVICE_LOG_DIR:-"/var/log/youtubedlapi_server_logs"} 


stop_service_on_port() {
  local port=5000
  local pids=$(lsof -t -i:$port -sTCP:LISTEN)
  if [[ ! -z "$pids" ]]; then
    echo "Stopping service(s) using port $port..."
    for pid in $pids; do
      kill -9 $pid
      echo "Killed $pid"
    done
  fi
}

create_stop_service_file() {
    cat <<EOF > /stop_service_on_port.sh
#!/bin/bash
port=5000
pids=\$(lsof -t -i:\$port -sTCP:LISTEN)
if [[ ! -z "\$pids" ]]; then
  echo "Stopping service(s) using port \$port..."
  for pid in \$pids; do
    kill -9 \$pid
    echo "Killed \$pid"
  done
fi
EOF

    echo "Stop Service file created."
    chmod +x /stop_service_on_port.sh
}


create_service_user() {
    if ! id "$SERVICE_USER" &>/dev/null; then
        useradd --system --create-home --shell /bin/false "$SERVICE_USER"
        echo "User '$SERVICE_USER' created."
    else
        echo "User '$SERVICE_USER' already exists."
    fi
}


create_service_file() {
    cat <<EOF > /etc/systemd/system/${SERVICE_NAME}.service
[Unit]
Description=${SERVICE_DESCRIPTION}
After=network.target

[Service]
User=${SERVICE_USER}
WorkingDirectory=/
ExecStartPre=/bin/bash -c /stop_service_on_port.sh
ExecStop=/bin/bash -c /stop_service_on_port.sh
ExecStart=uvicorn youtubedlapi_server_infusiblecoder.app:app_asgi --host 0.0.0.0 --port 5000 --workers 4 --log-level info
Restart=on-failure
RestartSec=10s
StartLimitInterval=300
StartLimitBurst=3
StandardOutput=file:${SERVICE_LOG_DIR}/output.log
StandardError=file:${SERVICE_LOG_DIR}/error.log
Environment="PATH=$PATH"

[Install]
WantedBy=multi-user.target
EOF

    echo "Service file /etc/systemd/system/${SERVICE_NAME}.service created."
    systemctl daemon-reload
}


check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo "This script must be run as root. Please use sudo."
        exit 1
    fi
}


check_root
create_service_user
mkdir -p "$SERVICE_LOG_DIR"
chown "$SERVICE_USER":"$SERVICE_USER" "$SERVICE_LOG_DIR"
stop_service_on_port
create_stop_service_file
create_service_file

echo "Service file created for '${SERVICE_NAME}'. You can now manage the service with:"
echo "  systemctl status ${SERVICE_NAME}"
echo "  systemctl stop ${SERVICE_NAME}"
echo "  systemctl start ${SERVICE_NAME}"
echo "  systemctl enable ${SERVICE_NAME} (to start automatically on boot)"
echo "  systemctl disable ${SERVICE_NAME} (to prevent automatic start)"
