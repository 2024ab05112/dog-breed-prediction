# Setup and Installation Guide

## Prerequisites

Before starting, ensure you have the following tools installed:
- **Docker**: For building container images.
- **Minikube**: Local Kubernetes cluster (optional, for local testing).
- **Kubectl**: Command-line tool for Kubernetes.
- **Python 3.12+**: For local development.

## Quick Start (Kubernetes)

### 1. Start Minikube
Initialize your local Kubernetes cluster:
```bash
minikube start
```

### 2. Build Docker Images
To build the images locally:

```bash
docker build -t 2024ab05112/dog-breed-api:latest backend/
docker build -t 2024ab05112/dog-breed-frontend:latest frontend/
```

> **Note**: If using Minikube on Linux/Mac, point your shell to Minikube's Docker daemon:
> `eval $(minikube -p minikube docker-env)`

### 3. Deploy to Kubernetes
Apply the configuration files located in the `k8s/` directory.

```bash
# Deploy Common Resources (Ingress)
kubectl apply -f k8s/common/

# Deploy Backend and Frontend
kubectl apply -f k8s/backend/
kubectl apply -f k8s/frontend/

# Deploy Monitoring (Prometheus & Grafana)
kubectl apply -f k8s/monitoring/
```

### 4. Access the Application
Get the URL for the Frontend service if using NodePort/LoadBalancer locally, or access via Ingress.

## Local Development (Run without Docker)

**Backend:**
1. Navigate to `backend/`.
2. Create virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`.
4. Run server: `uvicorn main:app --reload`.

**Frontend:**
1. Navigate to `frontend/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Update `API_URL` in `webapp/views.py` to point to localhost.
4. Run server: `python manage.py runserver`.
