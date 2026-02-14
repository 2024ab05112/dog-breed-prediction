import io
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

# IMPORTANT: import AFTER mocking
with patch("tensorflow.keras.models.load_model") as mock_load_model:
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([[0.8]])
    mock_load_model.return_value = mock_model

    from main import app  # adjust if filename differs

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict_endpoint():
    # Create fake image
    img = Image.new("RGB", (224, 224))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    response = client.post(
        "/predict",
        files={"file": ("test.jpg", buf, "image/jpeg")}
    )

    assert response.status_code == 200
    body = response.json()

    assert body["predicted_label"] == "Dog"
    assert "confidence" in body
    assert "probabilities" in body
    assert body["probabilities"]["dog"] > 0.5
