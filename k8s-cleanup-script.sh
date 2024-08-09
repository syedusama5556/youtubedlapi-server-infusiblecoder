#!/bin/bash

# Define the resource names
DEPLOYMENT_NAME="ytdlp-server"
SERVICE_NAME="ytdlp-server"
HPA_NAME="ytdlp-server-autoscaler"

# Delete the HorizontalPodAutoscaler
echo "Deleting HorizontalPodAutoscaler: $HPA_NAME..."
kubectl delete hpa "$HPA_NAME"

# Delete the Service
echo "Deleting Service: $SERVICE_NAME..."
kubectl delete service "$SERVICE_NAME"

# Delete the Deployment
echo "Deleting Deployment: $DEPLOYMENT_NAME..."
kubectl delete deployment "$DEPLOYMENT_NAME"

echo "All specified resources have been deleted."
