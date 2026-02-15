from fastapi import FastAPI, UploadFile, File, APIRouter
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Dog Breed Inference API")

# Attempt to load model (with Git LFS support)
try:
    model = tf.keras.models.load_model("model.h5")
    CLASS_NAMES = ["Cat", "Dog"] # Default from user provided code
except Exception as e:
    print(f"Warning: Model load failed: {e}")
    model = None
    CLASS_NAMES = ["Cat", "Dog"]

IMG_SIZE = (224, 224)

def preprocess_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize(IMG_SIZE)
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0) # (1, 224, 224, 3)
        return image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# Router for API endpoints
router = APIRouter(prefix="/api")

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        return {"error": "Model not loaded"}
        
    content = await file.read()
    image = preprocess_image(content)
    
    if image is None:
        return {"error": "Invalid image"}

    # Binary classification logic from user code
    prob = model.predict(image)[0][0]
    is_dog = prob > 0.5
    label = CLASS_NAMES[int(is_dog)]

    return {
        "predicted_label": label,
        "confidence": float(prob if is_dog else 1.0 - prob),
        "probabilities": {
            "cat": float(1.0 - prob),
            "dog": float(prob)
        }
    }

# Health check at root for K8s probes
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include the router
app.include_router(router)

# Instrumentation
Instrumentator().instrument(app).expose(app, endpoint="/api/metrics")
