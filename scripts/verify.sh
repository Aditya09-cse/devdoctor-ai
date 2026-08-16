#!/bin/bash

set -e

echo "===== Docker ====="

docker --version


echo ""
echo "===== kubectl ====="

kubectl version --client


echo ""
echo "===== Kind ====="

kind version


echo ""
echo "===== Kubernetes Nodes ====="

kubectl get nodes


echo ""
echo "===== Kubernetes Pods ====="

kubectl get pods -A


echo ""
echo "===== Metrics Server ====="

kubectl get pods -n kube-system | grep metrics-server


echo ""
echo "===== Metrics API ====="

kubectl get apiservice v1beta1.metrics.k8s.io


echo ""
echo "===== Node Metrics ====="

# Give Metrics Server some time to provide metrics

for i in {1..12}
do
    if kubectl top nodes >/dev/null 2>&1
    then
        kubectl top nodes
        break
    fi

    echo "Waiting for metrics... ($i/12)"
    sleep 10
done


echo ""
echo "===== Application Pods ====="

kubectl get pods -n ai-incident-namespace


echo ""
echo "===== Application Metrics ====="

kubectl top po -n ai-incident-namespace


echo ""
echo "===== HPA ====="

kubectl get hpa -n ai-incident-namespace


echo ""
echo "===== Docker Containers ====="

docker ps


echo ""
echo "===== Verification Complete ====="
