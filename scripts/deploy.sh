#!/bin/bash

set -e

echo "========== Kubernetes Deployment Started =========="

# ------------------------------------------------
# 1. Check Kubernetes
# ------------------------------------------------

echo "Checking Kubernetes cluster..."

kubectl get nodes


# ------------------------------------------------
# 2. Create namespace
# ------------------------------------------------

echo "Creating namespace..."

kubectl apply -f ~/k8s/namespace.yml

kubectl wait \
  --for=jsonpath='{.status.phase}'=Active \
  namespace/ai-incident-namespace \
  --timeout=60s


# ------------------------------------------------
# 3. Create / update database secret
# ------------------------------------------------

echo "Creating database secret..."

kubectl create secret generic db-secrets \
  --from-literal=DB_PASSWORD="$DB_PASSWORD" \
  -n ai-incident-namespace \
  --dry-run=client \
  -o yaml | kubectl apply -f -


# ------------------------------------------------
# 4. ConfigMaps
# ------------------------------------------------

echo "Applying ConfigMaps..."

kubectl apply -f ~/k8s/ConfigMap.yml
kubectl apply -f ~/k8s/postgres-init.yml


# ------------------------------------------------
# 5. Storage
# ------------------------------------------------

echo "Applying storage..."

kubectl apply -f ~/k8s/pv.yml
kubectl apply -f ~/k8s/pvc.yml

kubectl apply -f ~/k8s/ollama-pv.yml
kubectl apply -f ~/k8s/ollama-pvc.yml


# ------------------------------------------------
# 6. PostgreSQL
# ------------------------------------------------

echo "Deploying PostgreSQL..."

kubectl apply -f ~/k8s/postgres-deployment.yml
kubectl apply -f ~/k8s/postgres-service.yml


# ------------------------------------------------
# 7. Ollama
# ------------------------------------------------

echo "Deploying Ollama..."

kubectl apply -f ~/k8s/ollama-deployment.yml
kubectl apply -f ~/k8s/ollama-service.yml


# ------------------------------------------------
# 8. Application
# ------------------------------------------------

echo "Deploying application..."

kubectl apply -f ~/k8s/app-deployment.yml
kubectl apply -f ~/k8s/flask-service.yml


# ------------------------------------------------
# 9. HPA
# ------------------------------------------------

echo "Applying HPA..."

kubectl apply -f ~/k8s/app-hpa.yml
kubectl apply -f ~/k8s/ollama-hpa.yml


# ------------------------------------------------
# 10. Update application image
# ------------------------------------------------

echo "Updating application image..."

kubectl set image deployment/ai-incident-deployment \
  ai-incident-manager="$DOCKER_IMAGE:$IMAGE_TAG" \
  -n ai-incident-namespace


# ------------------------------------------------
# 11. Wait for rollout
# ------------------------------------------------

echo "Waiting for application rollout..."

kubectl rollout status deployment/ai-incident-deployment \
  -n ai-incident-namespace \
  --timeout=180s


# ------------------------------------------------
# 12. Final status
# ------------------------------------------------

echo ""
echo "========== Pods =========="

kubectl get pods -n ai-incident-namespace

echo ""
echo "========== Services =========="

kubectl get svc -n ai-incident-namespace

echo ""
echo "========== HPA =========="

kubectl get hpa -n ai-incident-namespace

echo ""
echo "========== Deployment Successful =========="