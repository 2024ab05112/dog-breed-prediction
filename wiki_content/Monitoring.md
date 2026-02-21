# Monitoring and Observability

The Dog Breed Prediction System includes a comprehensive monitoring stack based on Prometheus and Grafana.

## Monitoring Components

### 1. Prometheus UI
Prometheus is responsible for scraping metrics from the production API and storing them for analysis.
- **Endpoint**: `/prometheus`
- **Features**: Real-time metric querying, system health checks, and alerting rules.

### 2. Grafana Dashboard
Grafana provides a visual interface for the metrics collected by Prometheus.
- **Endpoint**: `/grafana`
- **Dashboards**: Features a dedicated "Dog Breed API Health" dashboard showing:
    - **Total Requests**: Number of predictions made.
    - **Success Rate**: Ratio of successful vs failed predictions.
    - **Latency**: 95th and 99th percentile response times.

### 3. MLflow Tracking server
MLflow tracks training experiments, parameters, and logs models.
- **Endpoint**: `/mlflow`
- **Features**: Visualizing experiment runs, comparing training vs validation loss/accuracy, model registry and artifacts downloading (`.h5` model files).

## How to Access
Once the system is deployed, the monitoring tools are available at:
`https://dog-breed-prediction.centralindia.cloudapp.azure.com/grafana/`
`https://dog-breed-prediction.centralindia.cloudapp.azure.com/prometheus/`
`https://dog-breed-prediction.centralindia.cloudapp.azure.com/mlflow/`

## Metrics Customization
Metrics are generated using the `prometheus-fastapi-instrumentator` library in the Backend FastAPI service. The key metrics tracked are:
- `http_requests_total`: A counter for every hit to the prediction endpoint.
- `http_request_duration_seconds`: A histogram of request processing times.

All metrics are exposed at the internal endpoint `/api/metrics` which is scraped by Prometheus every 15 seconds.
