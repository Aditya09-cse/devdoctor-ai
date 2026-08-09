#!/bin/bash

echo "===== Docker ====="
docker --version

echo "===== kubectl ====="
kubectl version --client

echo "===== Kind ====="
kind version

echo "===== Nodes ====="
kubectl get nodes

echo "===== Pods ====="
kubectl get pods -A

echo "===== Docker Containers ====="
docker ps

