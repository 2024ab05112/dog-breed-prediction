#!/bin/bash
SERVICE_PORT=$(kubectl get svc mlops-assignment-service -o jsonpath='{.spec.ports[0].nodePort}')
SERVICE_IP=$(minikube ip)

# Check health endpoint
curl -f http://$SERVICE_IP:$SERVICE_PORT/ || exit 1

# Example prediction test
curl -f -X POST http://$SERVICE_IP:$SERVICE_PORT/predict -H "Content-Type: application/json" -d '{"input": "test data"}' || exit 1

echo "Smoke tests passed ✅"
