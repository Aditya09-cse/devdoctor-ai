# update ubuntu
sudo apt update
sudo apt-get upgrade -y

# install required packegs
sudo apt install -y \
curl \
git \
wget \
unzip \
ca-certificates \
apt-transport-https


# install docker
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
sudo newgrp docker


# install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# install kind
curl -Lo kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x kind
sudo mv kind /usr/local/bin/

# Create Kubernetes cluster
kind create cluster \
  --name aditya-cluster \
  --config kind-config.yml

# verify installation
docker --version
kubectl version --client
kind version
kubectl get nodes
