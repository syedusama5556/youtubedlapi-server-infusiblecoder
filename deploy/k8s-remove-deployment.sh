#!/bin/bash

# Function to delete all resources of a given type
delete_resources() {
    local resource_type=$1
    echo "Deleting all ${resource_type}s..."
    kubectl get "${resource_type}" --no-headers | awk '{print $1}' | while read -r resource; do
        kubectl delete "${resource_type}" "$resource"
    done
}

# Function to scale down all resources
scale_down_resources() {
    local resource_type=$1
    echo "Scaling down all ${resource_type}s to zero replicas..."
    kubectl get "${resource_type}" --no-headers | awk '{print $1}' | while read -r resource; do
        kubectl scale "${resource_type}" "$resource" --replicas=0
    done
}

# Scale down deployments, stateful sets, and replica sets
scale_down_resources "deployments"
scale_down_resources "statefulsets"
scale_down_resources "replicasets"

# Delete daemon sets and jobs
delete_resources "daemonsets"
delete_resources "jobs"

# Optionally, delete all pods (if you want to stop everything, including pods not controlled by higher-level resources)
echo "Deleting all pods..."
kubectl get pods --no-headers | awk '{print $1}' | while read -r pod; do
    kubectl delete pod "$pod"
done

echo "All resources have been stopped."
