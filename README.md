# Dog Breed Prediction MLOps Project

This repository contains an end-to-end MLOps solution for predicting dog breeds from images. It uses a FastAPI backend for inference, a Django-based frontend for user interaction, and is deployed on Azure Kubernetes Service (AKS) with full monitoring capabilities using Prometheus and Grafana.

## Features
- **Frontend**: Django web application allowing users to upload dog images via a drag-and-drop interface.
- **Backend**: High-performance FastAPI service hosting a TensorFlow/Keras CNN model.
- **Infrastructure**: Production-grade Kubernetes deployment on Azure (AKS).
- **Automation**: CI/CD pipelines using GitHub Actions for automated testing, building, and deployment.
- **Observability**: Real-time monitoring with Prometheus metrics and Grafana dashboards.

## Tech Stack
- **Languages**: Python (FastAPI, Django)
- **Containerization**: Docker
- **Orchestration**: Kubernetes (AKS)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus, Grafana, prometheus-fastapi-instrumentator
- **Cloud Provider**: Microsoft Azure

## Live Demo
- **App URL**: [http://dog-breed-prediction.centralindia.cloudapp.azure.com/](http://dog-breed-prediction.centralindia.cloudapp.azure.com/)
- **API Docs**: [http://dog-breed-prediction.centralindia.cloudapp.azure.com/docs](http://dog-breed-prediction.centralindia.cloudapp.azure.com/docs)
- **Grafana**: [http://dog-breed-prediction.centralindia.cloudapp.azure.com/grafana/](http://dog-breed-prediction.centralindia.cloudapp.azure.com/grafana/)

## Project Structure
```
.
├── backend/            # FastAPI application and model code
├── frontend/           # Django web application
├── k8s/                # Kubernetes manifests
│   ├── backend/        # Backend deployment & service
│   ├── frontend/       # Frontend deployment & service
│   ├── monitoring/     # Prometheus & Grafana config
│   └── common/         # Ingress controller config
├── .github/workflows/  # CI/CD pipelines
└── wiki_content/       # Documentation source files
```

## Documentation
Detailed documentation is available in the [Project Wiki](../../wiki). Key sections include:
- [Setup and Installation](../../wiki/Setup)
- [Architecture Overview](../../wiki/Architecture)
- [Deployment Guide (AKS)](../../wiki/AKS_Deployment)
- [API Documentation](../../wiki/API)
- [Monitoring Guide](../../wiki/Monitoring)

## Quick Start (Local)

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
pip install -r requirements.txt
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to view the app locally.

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
