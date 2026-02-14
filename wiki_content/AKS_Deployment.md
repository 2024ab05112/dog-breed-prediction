# Azure Kubernetes Service (AKS) Deployment Guide

This guide details how the Dog Breed Prediction System is deployed to a production-grade Kubernetes environment using Azure Kubernetes Service (AKS) and GitHub Actions.

## Infrastructure Overview

The application runs on an AKS cluster (`DogBreedCluster`) within the `DogBreedRG` resource group. 
To optimize costs for development/student usage, the cluster is designed to be **started on demand** by the CI/CD pipeline and should be **stopped manually** when not in use.

## Unified Access Architecture
Unlike basic deployments that use multiple Public IPs, this system uses an **Nginx Ingress Controller** to route all traffic through a **single entry point**. This bypasses Azure Student subscription IP limits and provides a professional URL structure.

## CI/CD Pipeline (`deploy.yml`)

The project uses a sophisticated GitHub Actions workflow located at `.github/workflows/deploy.yml` that handles the entire deployment process.

### Triggers
The pipeline runs automatically on:
- **Push to `main` branch**: Only if changes are detected in `backend/` or `k8s/` directories (ignoring docs).
- **Manual Dispatch**: Can be triggered manually from the "Actions" tab in GitHub.

### Pipeline Stages

1.  **Check Changes (`check-changes`)**:
    - Analyzes which parts of the codebase (Backend or K8s manifests) have changed.
    - This creates a "Smart Build" process: we only rebuild docker images if the application code has changed.

2.  **Build and Push (`build-and-push`)**:
    - Runs only if backend code changes.
    - Builds Docker images and pushes to Docker Hub with `latest` and `<commit-sha>` tags.

3.  **Deployment Prep**:
    - **Azure Login**: Authenticates using the `AZURE_CREDENTIALS` secret.
    - **Cluster Power State**: Automatically starts the AKS cluster if it's currently stopped.
    - **Ingress Controller Management**: The pipeline checks for the presence of the Nginx Ingress Controller and installs it automatically if missing.
    - **Automated DNS Linking**: Dynamically finds the Ingress Public IP and assigns the `dog-breed-prediction` DNS label using Azure CLI.

4.  **Deploy (`deploy`)**:
    - **Dynamic Manifest Update**: Replaces image tags with the specific `<commit-sha>`.
    - **Apply Manifests**: Applies all configurations including Ingress, Monitoring, and Backend.

## Secrets Configuration

| Secret Name | Description |
|-------------|-------------|
| `DOCKER_USERNAME` | Your Docker Hub username. |
| `DOCKER_PASSWORD` | Your Docker Hub access token (or password). |
| `AZURE_CREDENTIALS` | The JSON output from creating an Azure Service Principal. |

## Manual Management

**Stop Cluster (To Save Costs):**
```bash
az aks stop --resource-group DogBreedRG --name DogBreedCluster
```

**Start Cluster (Manual):**
```bash
az aks start --resource-group DogBreedRG --name DogBreedCluster
```
