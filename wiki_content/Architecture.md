# Service Architecture & Workflow

This document details the architecture and request flow of the Dog Breed Prediction System, optimized for Azure cloud hosting.

## Architecture Diagram

The system utilizes an Nginx Ingress Controller as a unified gateway to manage traffic across all services using a single Public IP.

```mermaid
graph TD
    subgraph External_Traffic [External Traffic]
        User([User])
    end

    subgraph Azure_Network [Azure Infrastructure]
        LB[Nginx Ingress LoadBalancer]
    end

    subgraph AKS_Cluster [Kubernetes Cluster]
        
        subgraph Gateway [Gateway Layer]
            Ingress[Nginx Ingress Controller]
        end

        subgraph Applications [Application Layer]
            Django[Django Frontend]
            FastAPI[Dog Breed API]
        end
        
        subgraph Monitoring [Observability]
            Prometheus[Prometheus Server]
            Grafana[Grafana Dashboards]
        end

        %% Routing
        Ingress -->|/| Django
        Ingress -->|/api| FastAPI
        Ingress -->|/prometheus| Prometheus
        Ingress -->|/grafana| Grafana

        %% Logic
        Django -->|Synchronous POST| FastAPI
        Prometheus -->|Scrape Metrics| FastAPI
        Grafana -->|Query Datasource| Prometheus
    end

    User --> LB
    LB --> Ingress
```

## Service Communication Details

### 1. Unified Access (Ingress)
All external requests are handled by the **Nginx Ingress Controller**. This architectural choice provides:
- **Cost Efficiency**: Uses only one Azure Public IP.
- **Simplified SSL/TLS**: A centralized place to handle security.
- **Path-Based Routing**: Clean URLs for all tools under a single domain.

### 2. Implementation Overview
- **Routing**: Traffic is routed based on the URL path (`/` for Frontend, `/api` for Backend).
- **Security & Access**: Uses **cert-manager** in the cluster to automatically provision **Let's Encrypt SSL Certificates**, enabling secure HTTPS access.
- **Isolation**: Each component runs in separate pods, ensuring fault tolerance.

### 3. Model Training Pipeline (CI/CT)
- **Architecture**: Uses **MobileNetV2** (pre-trained on ImageNet) as a feature extractor with a custom classification head.
- **Dataset**: Automatically downloads a subset of the "Cats vs Dogs" dataset using `tensorflow_datasets` (TFDS).
- **Automation**: The model is retrained on every backend code push within the GitHub Actions runner before building the Docker image. This ensures the deployed model is always fresh and reproducible.

### 4. Monitoring Workflow
- **Metrics Collection**: Prometheus automatically scrapes telemetry from the FastAPI pods.
- **Visualization**: Grafana queries Prometheus and displays real-time health data (RPS, Latency) on a pre-configured "Dog Breed API" dashboard.
- **Access**: Both tools are accessible at the `/prometheus` and `/grafana` endpoints respectively.
