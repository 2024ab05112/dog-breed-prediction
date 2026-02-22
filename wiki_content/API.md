# API Documentation

The backend service is built using **FastAPI** and exposes RESTful endpoints for prediction and monitoring.

## Base URL
Public Entry Point (via Ingress): `https://dog-breed-prediction.centralindia.cloudapp.azure.com/`

## Endpoints

### 1. Predict Dog Breed
Classifies an uploaded image as either a Cat or a Dog.

- **URL**: `/predict`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`

#### Request Parameter
| Field | Type | Description |
|-------|------|-------------|
| `file` | File (Upload) | Image file (JPEG/PNG) to classify. |

**Example Request:**
Upload an image file using `curl` or Postman to the endpoint.

```bash
curl -X POST "https://dog-breed-prediction.centralindia.cloudapp.azure.com/api/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.jpg"
```

#### Response (JSON)
| Field | Type | Description |
|-------|------|-------------|
| `predicted_label` | string | "Dog" or "Cat" |
| `confidence` | float | Confidence score (0.0 - 1.0) for the predicted label |
| `probabilities` | object | Raw probabilities for each class |

**Example Response:**
```json
{
  "predicted_label": "Dog",
  "confidence": 0.985,
  "probabilities": {
    "cat": 0.015,
    "dog": 0.985
  }
}
```

### 2. Interactive Documentation (Swagger UI)
FastAPI automatically generates interactive Swagger documentation.
- **URL**: `/docs` (Full path: `https://dog-breed-prediction.centralindia.cloudapp.azure.com/docs`)
- **Use Case**: Test API endpoints directly from the browser.

### 3. Health Check
Checks if the API is running (used by Kubernetes Liveness/Readiness probes).
- **URL**: `/health` (at root, not /api/health)
- **Method**: `GET`
- **Response**: `{"status": "healthy"}`

### 4. Metrics
Exposes Prometheus metrics.
- **URL**: `/metrics`
- **Method**: `GET`
- **Response**: Plain text Prometheus format.
