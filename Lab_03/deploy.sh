#!/bin/bash
# Script to apply all manifests for Lab 03 Variant 2

# Check if kubectl is available directly or via microk8s
if command -v kubectl &> /dev/null
then
    KCMD="kubectl"
elif command -v microk8s &> /dev/null
then
    KCMD="microk8s kubectl"
else
    echo "Error: kubectl or microk8s not found. Please install Kubernetes cli."
    exit 1
fi

echo "Using command: $KCMD"

echo "Applying secrets..."
$KCMD apply -f secrets.yaml

echo "Applying services..."
$KCMD apply -f services.yaml

echo "Applying deployments..."
$KCMD apply -f db-deployment.yaml
$KCMD apply -f adminer-deployment.yaml

echo "Waiting for pods to be ready..."
$KCMD get pods -w
