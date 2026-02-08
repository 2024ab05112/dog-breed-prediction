from fastapi import FastAPI, UploadFile, File
import tensorflow as tf
import numpy as np
from PIL import Image
import io

import uvicorn

app = FastAPI(title="Cats vs Dogs Inference API")

# Load model once at startup
model = tf.keras.models.load_model("model.h5")

CLASS_NAMES = ["Cat", "Dog"]
IMG_SIZE = (224, 224)


def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(IMG_SIZE)
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = preprocess_image(image_bytes)

    prob = model.predict(image)[0][0]
    label = CLASS_NAMES[int(prob > 0.5)]

    return {
        "predicted_label": label,
        "confidence": float(prob if label == "Dog" else 1 - prob),
        "probabilities": {
            "cat": float(1 - prob),
            "dog": float(prob)
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    