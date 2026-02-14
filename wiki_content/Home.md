# Welcome to the Dog Breed Prediction System Wiki

## Project Overview
This project is an end-to-end MLOps solution designed to predict the breed of a dog from an image. It demonstrates a complete production pipeline, from model serving to deployment on a Kubernetes cluster.

## Key Features
- **High-Performance API**: FastAPI microservice for real-time image classification.
- **Deep Learning Model**: Convolutional Neural Network (CNN) for accurate breed identification.
- **Scalable Infrastructure**: Deployed on Azure Kubernetes Service (AKS) with auto-scaling capabilities.
- **Robust Monitoring**: Integrated Prometheus and Grafana for system observability.
- **Automated CI/CD**: GitHub Actions pipeline for continuous integration and deployment.

## Tech Stack
| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI, Uvicorn, Python |
| **ML Model** | TensorFlow / Keras (CNN) |
| **Containerization** | Docker |
| **Orchestration** | Azure AKS |
| **CI/CD** | GitHub Actions |
| **Monitoring** | Prometheus, Grafana |

## Documentation Index
- **[[Setup and Installation|Setup]]**: Step-by-step guide to get the project running locally.
- **[[Cloud Deployment (AKS)|AKS_Deployment]]**: Production deployment guide using Azure and GitHub Actions.
- **[[Architecture Details|Architecture]]**: Deep dive into the system design and workflows.
- **[[API Documentation|API]]**: Details on the backend endpoints and usage.
- **[[Monitoring Guide|Monitoring]]**: How to use Prometheus and Grafana dashboards.
