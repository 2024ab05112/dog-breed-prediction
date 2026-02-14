from django.shortcuts import render
import requests
import json

# URL of the internal Kubernetes service
# Service Name: dog-breed-api, Port: 80
# Endpoint: /api/predict
API_URL = "http://dog-breed-api:80/api/predict"

def index(request):
    prediction = None
    confidence = None
    probabilities = None
    error = None

    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            
            # Prepare file for upload
            files = {'file': (image_file.name, image_file.read(), image_file.content_type)}
            
            # Send request to FastAPI backend
            response = requests.post(API_URL, files=files, timeout=10)
            response.raise_for_status()
            
            # Parse result
            data = response.json()
            prediction = data.get("predicted_label")
            confidence_val = data.get("confidence")
            probabilities = data.get("probabilities")

            if confidence_val:
                confidence = f"{confidence_val * 100:.2f}%"

        except Exception as e:
            error = f"Error connecting to API: {str(e)}"

    return render(request, 'index.html', {
        'prediction': prediction,
        'confidence': confidence,
        'probabilities': probabilities,
        'error': error
    })
