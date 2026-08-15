#!/bin/bash

set -e

# ==============================
# Update Ubuntu
# ==============================

echo "===== Updating Ubuntu ====="

sudo apt update
sudo apt-get upgrade -y


# ==============================
# Install required packages
# ==============================

echo "===== Installing packages ====="

sudo apt install -y \
  curl \
  git \
  wget \
  unzip \
  ca-certificates \
  apt-transport-https


# ==============================
# Install Docker
# ==============================

echo "===== Installing Docker ====="

sudo apt install -y docker.io

sudo systemctl enable docker
sudo systemctl start docker

sudo usermod -aG docker $USER

# Make docker group available in current shell
sudo newgrp docker


# ==============================
# Install kubectl
# ==============================

echo "===== Installing kubectl ====="

curl -LO "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

chmod +x kubectl

sudo mv kubectl /usr/local/bin/


# ==============================
# Install Kind
# ==============================

echo "===== Installing Kind ====="

curl -Lo kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64

chmod +x kind

sudo mv kind /usr/local/bin/


# ==============================
# Create Kubernetes Cluster
# ==============================

echo "===== Creating Kind Cluster ====="

kind create cluster \
  --name aditya-cluster \
  --config kind-config.yml


# ==============================
# Install Metrics Server
# ==============================

echo "===== Installing Metrics Server ====="

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

echo "===== Configuring Metrics Server ====="

kubectl patch deployment metrics-server \
  -n kube-system \
  --type='json' \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'


# Wait for Metrics Server
echo "===== Waiting for Metrics Server ====="

kubectl rollout status deployment/metrics-server \
  -n kube-system \
  --timeout=120s


# ==============================
# Basic Verification
# ==============================

echo "===== Installation Complete ====="

echo "Docker:"
docker --version

echo "kubectl:"
kubectl version --client

echo "Kind:"
kind version

echo "Kubernetes Nodes:"
kubectl get nodes

echo "Metrics Server:"
kubectl get pods -n kube-system | grep metrics-server

echo "===== Setup Complete ====="
