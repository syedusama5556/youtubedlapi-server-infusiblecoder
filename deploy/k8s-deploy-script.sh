#!/bin/bash

# Exit on any error
set -e

# Apply Kubernetes configuration
kubectl apply -f k8s-config.yaml

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/ytdlp-server

# Get deployment status
echo "Deployment status:"
kubectl get deployments

# Get pod status
echo "Pod status:"
kubectl get pods

# Get service status
echo "Service status:"
kubectl get services

# Get HPA status
echo "HorizontalPodAutoscaler status:"
kubectl get hpa

# Get external IP (if using LoadBalancer)
echo "Waiting for external IP..."
external_ip="192.168.0.100"
while [ -z $external_ip ]; do
  echo "Waiting for end point..."
  external_ip=$(kubectl get svc ytdlp-server --template="{{range .status.loadBalancer.ingress}}{{.ip}}{{end}}")
  [ -z "$external_ip" ] && sleep 10
done
echo "End point ready: $external_ip"

echo "Your yt-dlp server is now running!"
echo "You can test it using:"
echo "curl -G 'http://$external_ip/api/info' --data-urlencode 'url=https://www.youtube.com/watch?v=dQw4w9WgXcQ'"
